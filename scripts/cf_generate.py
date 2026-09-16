#!/usr/bin/env python3
"""
cf_generate — generate every Third Eye Events image with Cloudflare Workers AI.

Why this exists
---------------
The site's imagery was previously sourced from Wikimedia Commons. That pipeline
was licence-clean and free, but Commons is a keyword index, not a visual search,
so the picks were frequently off-brand: a Boldini oil painting as the founder
hero, a 1925 Charlie Chaplin still for Feature Films, an anti-Putin rally for
Political & Public. See scripts/IMAGE_RULESET.md for the full post-mortem.

This script replaces the sourcing step with generation. It calls Workers AI
directly over the REST API using the OAuth token that `wrangler login` already
stored, so there is no API key to manage and no per-image cost: Workers AI
includes 10,000 Neurons/day on the free plan, and FLUX.2 klein 4B costs ~132
Neurons for a 1536x864 image, i.e. roughly 75 images/day free.

Model choice
------------
@cf/black-forest-labs/flux-2-klein-4b. The video that prompted this work pins
@cf/stabilityai/stable-diffusion-xl-base-1.0, which is a 2023-era SDXL model
tagged Beta and absent from Cloudflare's current Neuron price table. klein 4B is
current-generation, accepts arbitrary width/height (so 16:9 comes out native
rather than centre-cropped from a square), and is fast.

Note: klein 4B takes **multipart/form-data**, not JSON. A JSON body returns
`Bad input: required properties at '/' are 'multipart'`.

Art direction
-------------
Prompts are written from the *page copy itself* — src/data/destinations.ts,
eventIPs.ts, signatureEntries.ts, production.ts, concepts.ts and the
`<PageHero>` props in src/pages/**. Not from the category a page belongs to.

That distinction is the whole point. "A palace in Rajasthan" is a stock photo.
Rajasthan's page says *"lakeside pheras at dusk"* and *"shehnai in sandstone
corridors"* — so the image is a lakeside palace pier at dusk. Switzerland's page
defines its concept as Agni-Him, *"fire and snow — opposing elements in one
union"*, with *"the homa kund glowing at the foot of glaciers"* — so the image is
a brass fire on a snowfield below a glacier, not a postcard of the Matterhorn.
The Shiva Entry's own sequence reads *"Smoke spreads across the pathway. Blue +
gold lighting cuts through the haze. Silhouette appears"* with trishul carriers —
so the image is a trishul standing in blue-and-gold lit smoke.

All 56 assets then share one house style (see HOUSE) so they read as a single
commissioned shoot: low-key cinematic light, warm gold and amber, dark charcoal
and earth, negative space at the top of the frame where PageHero sets its title.

Deliberately no visible faces. AI-rendered faces at this tier read as synthetic,
and for a luxury events brand the faceless editorial convention is both the
premium choice and the honest one — we are not fabricating photographs of real
clients, real weddings, or the founder.

Usage
-----
  python scripts/cf_generate.py                 # all slots
  python scripts/cf_generate.py --only dest-kyoto sig-shiva-entry
  python scripts/cf_generate.py --cards         # only the 11 portrait cards
  python scripts/cf_generate.py --force         # regenerate even if present

Output: /tmp/imgwork/gen/<slot>.jpg — then run scripts/apply_generated.py.
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import threading
import time
import tomllib
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from image_manifest import MANIFEST, CARD_DERIVATIONS, SUPPLIED_CARDS  # noqa: E402

WORK = "/tmp/imgwork"
OUT = os.path.join(WORK, "gen")
os.makedirs(OUT, exist_ok=True)

WRANGLER_CFG = os.path.expanduser(
    "~/Library/Preferences/.wrangler/config/default.toml"
)
# Cloudflare account that owns this Workers AI allocation.
#
# HISTORY — do not hard-code this without checking `npx wrangler whoami` first.
# The OAuth login is account-scoped: if the human re-runs `npx wrangler login`
# and picks a different account, this ID silently becomes stale and every call
# returns HTTP 401 "Authentication error" (code 10000) — which looks exactly
# like an expired/dead token but is not. That is what broke the Sep 15 23:39 UTC
# run: the session was fine, the account had changed underneath this constant.
#   2a3a56d332f390c0d38a694ab4f5055b  — old, now 401s
#   905a54b83934b6eefb57642b34996fd4  — current (Thirdeyevedic@gmail.com)
# Override with CLOUDFLARE_ACCOUNT_ID when the login changes again.
ACCOUNT_ID = os.environ.get(
    "CLOUDFLARE_ACCOUNT_ID", "905a54b83934b6eefb57642b34996fd4"
)
MODEL = "@cf/black-forest-labs/flux-2-klein-4b"
WORKERS = 3
RETRIES = 3

# ── House style ──────────────────────────────────────────────────────────────
# Appended to every subject prompt. This is what makes 56 separately generated
# images look like one shoot rather than a stock grab-bag.
#
# LUMINANCE CONTRACT — read this before changing the palette words.
#
# The site is a near-black canvas (--bg: #0a0a0a) and EVERY image is darkened
# again by the layout before it is seen:
#
#   homepage hero  .hero__veil     black 0.55 -> 0.25 -> 0.88   (~75% shows mid-band)
#   inner heroes   .phero__bg      opacity .85 + black 0.72 -> 0.55 -> opaque
#   cards          .ph__scrim      black 0.30 -> 0.52 -> 0.88   (~70% shows at top)
#
# The CSS therefore already supplies the darkness and the mood. An earlier
# version of this constant ALSO asked for "deep shadow, dark charcoal and earthy
# palette, muted desaturation" — doing the same job twice. Those images came back
# pre-darkened and were then crushed by the scrim into grey-black mush: no
# chromatic separation from the background, no focal pull, reading as generic
# stock. That is the exact failure this layer now exists to prevent.
#
# So the contract is inverted: the IMAGE supplies the light and the colour, the
# LAYOUT supplies the dark. Ask for luminous, richly saturated source frames —
# they are going to be darkened by CSS anyway, so they must start far brighter
# and far more chromatic than the intended final look.
HOUSE = (
    ", cinematic editorial photograph for a luxury Indian events house, "
    "richly saturated colour, luminous glowing highlights, deep dimensional shadow "
    "for chromatic contrast, premium colour grading, physically believable lighting, "
    "realistic fabric, realistic architecture, natural atmospheric depth, "
    "subtle film grain, high dynamic range, photorealistic, ultra detailed, "
    "no text, no watermark, no logo, no lettering"
)

# ── Colour story ─────────────────────────────────────────────────────────────
# VIBRANT IS NOT THE SAME AS COLOURFUL. The brand is "cinematic minimalism x
# Indian cultural depth" — a rainbow frame reads as cheap stock, which is the
# opposite of what was asked for. Vibrant here means HIGH CHROMA IN A DELIBERATE,
# LIMITED PALETTE: two or three colours per frame with one clearly dominant.
#
# Why a per-slot story rather than one brand palette: the interface is already
# gold (#b89b5e) on near-black. Photography that is also gold-on-black has zero
# chromatic separation from its own UI. The imagery has to carry the hue range
# the interface cannot — marigold, vermilion, emerald, peacock, indigo, magenta
# — so the page reads as colour-rich rather than uniformly sepia.
#
# Brand anchors to stay inside: gold #b89b5e, agni/terracotta #a9552b,
# ivory #f5f1e8. Everything else is drawn from the page's own copy (the Shiva
# Entry literally specifies "blue + gold lighting"; Rajasthan's line is "where
# royal memory is still alive"; Switzerland's is "fire meets ice").
DEFAULT_COLOR = "warm gold and agni orange as the dominant colour with ivory highlights"
COLOR = {
    "hero-cinematic": "gold and burnt agni orange dominant, ivory highlights, a single vermilion accent",
    "dest-maldives": "turquoise and aquamarine water dominant, white sand, sunset gold sky",
    "dest-rajasthan": "marigold and saffron dominant, rose-pink sandstone, royal crimson accents",
    "dest-switzerland": "glacier ice-blue and white dominant, one saturated fire-orange flame as the sole warm accent",
    "dest-kyoto": "deep moss emerald and wet cedar green dominant, one vivid lacquer-red accent",
    "dest-italy": "cypress green and terracotta dominant, honey-gold stone, lavender accents",
    "dest-bali": "emerald terrace green dominant, frangipani white, burning sunset vermilion",
    "dest-cruises": "deep ocean blue dominant, warm gold deck light, dusk magenta sky",
    "sig-shiva-entry": "electric cobalt dominant, rich gold highlights, deep indigo shadow, white haze",
    "sig-royal-entry": "marigold and gold dominant, candle amber, deep crimson shadow",
    "sig-floral-entry": "blush pink and cream dominant, soft jade, marigold accents, bright daylight",
    "sig-celestial-entry": "cosmic blue and cool white dominant, silver-blue mist, pale gold aura",
    "weddings-index": "gold and agni orange dominant, ivory light, deep earth shadow",
    "weddings-vaidik": "gold and saffron dominant, sacred ivory white, vermilion accent",
    "weddings-destination": "sunset gold dominant, ocean turquoise, palm green",
    "weddings-concepts": "royal indigo and magenta dominant, jewel-tone gold accents",
    "weddings-experiences": "gold and deep amber dominant, agni orange, ivory highlights",
    "vaidik-pure": "pure ivory white and gold dominant, the barest saffron tint",
    "vaidik-dining": "brass gold dominant, banana-leaf green, copper and ivory",
    "about-index": "gold and ivory dominant, warm amber, deep charcoal shadow",
    "about-dance": "stage gold and warm amber dominant, deep indigo backdrop",
    "about-story": "gold and agni orange dominant, ivory light, earth shadow",
    "about-philosophy": "warm gold and saffron dominant, ivory, a soft emerald accent",
    "about-vision": "dawn gold and horizon amber dominant, deep blue distance",
    "about-founder": "gold and amber dominant, deep indigo rehearsal hall",
    "destinations-index": "turquoise, gold and emerald together, one saturated hue per world",
    "destinations-india": "saffron, marigold and emerald dominant, vermilion accents",
    "ip-index": "saturated stage colour — magenta, cyan and gold on deep black",
    "ip-exhibitions": "bright LED white dominant, brand cyan and gold accents",
    "ip-automotive": "deep saturated blue dominant, electric cyan rim light, vivid reflections pooling on the floor",
    "ip-awards": "gold and deep royal blue dominant, warm spotlight cone",
    "ip-products": "brass gold dominant, ivory, terracotta textile, emerald accents",
    "ip-sports": "vivid pitch green dominant, floodlight white, deep blue night",
    "ip-fashion": "brilliant white dominant, magenta and cyan stage light in the air",
    "ip-political": "dusk amber and deep blue dominant, warm stage glow at distance",
    "ip-devotional": "fire orange and gold dominant, deep blue night water",
    "ip-concerts": "magenta, cyan and gold beams dominant on deep black, white haze",
    "production-index": "tungsten amber and cool moonlight blue in contrast, coloured practicals",
    "production-feature-films": "tungsten amber dominant, blue HMI contrast, saturated set practicals",
    "production-short-films": "warm tungsten dominant against teal shadow",
    "production-documentaries": "natural warm daylight dominant, earthy green and sky blue",
    "production-digital-content": "bright saturated LED set colour, clean white balance",
    "production-branded-content": "bold brand-led saturated colour, clean white light",
    "production-ad-shoots": "saturated product colour dominant, gold, clean white light",
    "contact": "gold and agni dominant, deep rose red, candle amber",
    "cinematic-beat1-threshold": "deep burgundy and gold dominant, warm amber light, ivory highlights",
    "cinematic-beat2-invocation": "crimson and burnished gold dominant, marigold orange, deep violet dusk sky",
    "cinematic-beat3-anticipation": "deep crimson and burnished gold dominant, ivory, one emerald accent",
    "cinematic-beat4-revelation": "vivid scarlet and gold dominant, warm backlight, marigold orange",
    "about-team-vision": "warm amber and gold dominant, blueprint blue accents, ivory",
    "pathways-vaidik": "fire orange and gold dominant, marigold yellow, deep crimson",
    "pathways-destination": "twilight gold and deep blue dominant, warm lantern amber",
    "pathways-concepts": "deep crimson and gold dominant, ivory, one emerald accent",
}

# Split out so the face decision is a one-line flip rather than 56 edits.
# Currently ON: AI faces at this model tier read synthetic, and a generated
# couple presented as Third Eye's own work is a disclosure problem. The client's
# brief mandates visible faces; that is being settled with a matched-pair test
# rather than by argument. Set to "" to adopt the brief's direction.
NO_FACES = ", no visible faces, nobody facing the camera, no portrait"

# ── Cinematography layer ─────────────────────────────────────────────────────
# Lifted from the client's master brief, which specifies a lens per image rather
# than one blanket focal length. This is the single biggest upgrade over the
# first-pass prompts: focal length drives perspective distortion, depth
# compression and how much environment reads around the subject.
DEFAULT_LENS = "35mm cinematic lens"
LENS = {
    "hero-cinematic": "28-35mm anamorphic wide lens, low-to-medium viewpoint",
    "dest-maldives": "28mm cinematic environmental lens",
    "dest-rajasthan": "24mm architectural cinematic lens, long vanishing point",
    "dest-switzerland": "24mm cinematic landscape lens",
    "dest-kyoto": "35mm cinematic lens, strong horizontal layering",
    "dest-italy": "35mm cinematic lens",
    "dest-bali": "28mm cinematic wide lens",
    "dest-cruises": "24mm cinematic wide-angle lens, strong deck leading lines",
    "sig-shiva-entry": "35mm anamorphic lens, low eye-level perspective",
    "sig-royal-entry": "40mm cinematic lens, centred architectural perspective, slight low angle",
    "sig-floral-entry": "50mm cinematic editorial lens, shallow depth of field",
    "sig-celestial-entry": "50mm anamorphic lens, slightly elevated perspective",
    "weddings-index": "35mm cinematic lens",
    "weddings-vaidik": "50mm cinematic lens",
    "weddings-destination": "35mm cinematic lens",
    "weddings-concepts": "50mm cinematic lens, long table perspective",
    "weddings-experiences": "35mm cinematic lens, motion blur",
    "vaidik-pure": "50mm fine-art cinematic lens",
    "vaidik-dining": "50mm macro food-editorial lens",
    "about-index": "35mm cinematic lens",
    "about-dance": "85mm portrait lens",
    "about-story": "50mm cinematic lens",
    "about-philosophy": "50mm macro cinematic lens",
    "about-vision": "24mm cinematic landscape lens",
    "about-founder": "35mm cinematic lens",
    "destinations-index": "24mm aerial lens, high vantage",
    "destinations-india": "35mm cinematic lens",
    "ip-index": "24mm cinematic architectural lens",
    "ip-exhibitions": "20-24mm ultra-wide architectural lens",
    "ip-automotive": "24mm cinematic architectural lens",
    "ip-awards": "35mm cinematic event lens",
    "ip-products": "50mm museum lens",
    "ip-sports": "35mm professional sports editorial lens",
    "ip-fashion": "50mm editorial fashion lens",
    "ip-political": "24mm documentary-event lens, elevated vantage",
    "ip-devotional": "35mm cinematic documentary lens",
    "ip-concerts": "24mm wide cinematic concert lens",
    "production-index": "28mm cinematic behind-the-scenes lens",
    "production-feature-films": "28mm cinematic behind-the-scenes lens",
    "production-short-films": "50mm cinematic lens",
    "production-documentaries": "35mm documentary lens",
    "production-digital-content": "35mm cinematic studio lens",
    "production-branded-content": "35mm cinematic documentary lens",
    "production-ad-shoots": "35mm documentary-commercial lens",
    "contact": "50mm cinematic lens",
    "cinematic-beat1-threshold": "35mm anamorphic lens, deep perspective compression",
    "cinematic-beat2-invocation": "28mm cinematic wide lens, low viewpoint",
    "cinematic-beat3-anticipation": "50mm macro cinematic lens, shallow depth of field",
    "cinematic-beat4-revelation": "85mm cinematic lens, compressed perspective",
    "about-team-vision": "35mm cinematic lens, over-the-shoulder perspective",
    "pathways-vaidik": "50mm macro cinematic lens, shallow depth of field",
    "pathways-destination": "28mm cinematic wide lens",
    "pathways-concepts": "50mm top-down lens, shallow depth of field",
}

# Composition, tied to the actual layout. `.hero__content` and `.phero__content`
# both use `justify-items: start`, so every hero's copy is left-aligned and
# overlays the LEFT of the frame. The subject therefore belongs right of centre
# and the left third must stay uncluttered.
DEFAULT_FRAME = (
    "subject placed right of centre, uncluttered negative space across the left third"
)

# Every scrim darkens from the bottom edge upward (.ph__scrim 0.30 -> 0.88,
# .phero__bg fading to opaque ink). Whatever is composed into the bottom of a
# frame is therefore thrown away. This clause is appended to every hero so the
# base stays calm and the luminance lives higher in the frame — it is a property
# of the LAYOUT, not of any one subject, which is why it is not baked into the
# per-slot entries below.
SCRIM_BASE = (
    "a calm darker base along the bottom edge where the page fades to black"
)

FRAME = {
    # These read better centred or symmetrical — the architecture is the subject.
    "dest-rajasthan": "strong symmetry, subject right of centre, open space at left",
    "dest-kyoto": "subject right of centre, generous empty atmospheric space at left",
    "dest-italy": "subject right of centre, open lake and sky at left",
    "dest-switzerland": "mountains filling the upper frame, ceremony in the lower middle, space at left",
    "hero-cinematic": "leading lines from the pathway, major visual action in the right two-thirds, space at left",
    "about-vision": "layered ridgelines filling the frame, space at left",
    "destinations-index": "island composed to the right, open water at left",
    "ip-sports": "pitch sweeping across the right, darker stands at left",
    "ip-political": "crowd filling the right and centre, darker ground at left",
    "sig-royal-entry": "strong symmetry along the pathway, subject right of centre",
    "weddings-vaidik": "fire altar centred, space around it",
    "vaidik-pure": "centred composition, large areas of negative space",
    # The colonnade's whole point is its vanishing point — do not offset it.
    "cinematic-beat1-threshold": "strong symmetrical perspective, vanishing point centred, figure small and central",
    "cinematic-beat4-revelation": "doorway centred, the lit figure right of centre, the foreground back turned to camera at left",
    # Pathway cards are the one hero-sized slot whose copy sits at the bottom, so
    # they take a centred/card-like composition rather than the left-hand gap.
    # They still receive SCRIM_BASE, so the calm base is not repeated here.
    "pathways-vaidik": "tight centred macro detail",
    "pathways-destination": "horizon high in frame, open water and open sky",
    "pathways-concepts": "overhead centred flat-lay arrangement",
}

# Cards are the one placement whose copy sits at the BOTTOM, not the left — the
# 3:4 / 3:4.2 `.dcard__inner` and `.sig-card` stacks are bottom-anchored over the
# scrim. So a card wants the subject high and the base quiet, rather than the
# hero's left-hand gap.
#
# DO NOT describe that quiet base as space "for overlaid card copy" (or "for
# text", "for a title", "for a caption"). FLUX reads the noun and renders it:
# naming copy produces a block of garbled pseudo-lettering across the lower
# third, which looks like a fake poster and reads as a real venue name. The
# HOUSE layer's "no text, no watermark, no logo, no lettering" does NOT protect
# against this — an explicit request in the frame layer outranks a generic
# negative. Describe the *visual* property instead: empty, plain, uncluttered.
# The CSS overlays the real copy regardless; the image only has to leave room.
CARD_FRAME = (
    "main subject filling the upper two thirds, the lower third kept calm, "
    "empty and uncluttered — plain surface, shadow or negative space, with no "
    "lettering, no signage and nothing written anywhere in the frame"
)

# Positive-framed exclusions. The client's brief specifies a "Negative:" block
# per image, but FLUX is a rectified-flow model and exposes no negative_prompt,
# so negated phrases are unreliable — and in a positive prompt they can summon
# what they name. These describe the DESIRED restraint instead.
EXCLUDE = (
    "specific observed detail rather than generic stock imagery, restrained "
    "real-world staging, natural unposed detail, minimal decoration, "
    "uncluttered frame, simple surroundings"
)

# "Restrained floral styling" only makes sense where decor is genuinely in
# frame. On a car on a black stage or a floodlit pitch it is noise, and worse,
# it can drag florals into a shot that should have none. Keyed off the subject
# text rather than a hand-maintained slot list so it cannot silently fall out
# of sync when a prompt is rewritten.
FLORAL_HINTS = (
    "flower", "floral", "garland", "marigold", "rose", "roses", "mandap",
    "rangoli", "decor", "centre table", "offerings", "petal",
)
FLORAL_EXCLUDE = "restrained floral styling"

# Per-slot additions where the brief flags a specific risk, again phrased as
# what should be present rather than what should be absent.
EXCLUDE_EXTRA = {
    "sig-shiva-entry": "abstract elemental symbolism rather than depicted deities, plain staging",
    "dest-bali": "authentic Balinese and Vaidik materials, no beach-party setting",
    "dest-switzerland": "a real, geologically plausible alpine peak",
    "ip-automotive": "an unbranded vehicle form, plain studio surroundings",
    "ip-political": "anonymous distant figures, civic staging without party insignia",
    "ip-devotional": "respectful documentary observation, no invented iconography",
    "production-digital-content": "a tidy studio, no social-media branding",
    "vaidik-dining": "pure vegetarian food, no meat, seafood or alcohol anywhere in frame",
}

# ── Generation size per aspect ───────────────────────────────────────────────
# Native generation at the target aspect beats centre-cropping a square.
#
# Workers AI snaps both dimensions DOWN to a multiple of 16 before rendering, so
# a request for 900x1200 comes back as 896x1200 — which is no longer 3:4, and
# crop_resize then shaves another 5px off the long edge chasing the aspect.
# The sizes below are already multiples of 16 and already exact ratios, so the
# crop is a no-op and the resize lands precisely on the manifest's target.
# 16:9 is the one case with no in-between: the only exact-ratio options either
# side of 1600 are 1536x864 and 1792x1008, so we accept a 1593x896 result.
GEN_SIZE = {
    (16, 9): (1600, 900),  # -> 1593x896 (see note above)
    (4, 5): (960, 1200),   # -> exact 900x1125
    (3, 4): (960, 1280),   # -> exact 900x1200
}
CARD_SIZE = (960, 1280)
HERO_CINEMATIC_SIZE = (2048, 1152)  # -> exact 1920x1080 for the full-bleed hero

# Slots that fill the viewport edge to edge and so are generated at 1080p rather
# than the standard 1600px hero width.
FULL_BLEED_SLOTS = {
    "hero-cinematic",
    "cinematic-beat1-threshold",
    "cinematic-beat2-invocation",
    "cinematic-beat3-anticipation",
    "cinematic-beat4-revelation",
}

# ── Prompts ──────────────────────────────────────────────────────────────────
# Each prompt states the *idea* the page carries, in the page's own vocabulary —
# not the category it belongs to. Read against src/data/*.ts and src/pages/*.
# A destination hero is not "a palace"; it is the ritual Third Eye actually
# stages there. Where the copy gives a concrete object or gesture, the prompt
# uses that object.
PROMPTS = {
    # ── Homepage ────────────────────────────────────────────────────────────
    # "You dream it. We bring it to life—with trust." The hero is cropped
    # `50% 74%`, so the subject must sit low and the top third stay empty.
    "hero-cinematic":
        "A vast empty ceremonial courtyard at night, a long stone pathway lined with hundreds "
        "of small oil lamps receding toward a distant illuminated carved sandstone archway, low "
        "mist across the ground, deep indigo sky filling the upper half of the frame as empty "
        "darkness, subject low in frame",

    # ── Destinations — each is the ritual Third Eye stages there ────────────
    # Maldives: "the mandapa faces open water so Agni meets horizon"
    "dest-maldives":
        "A barefoot Vaidik wedding mandap of plain white draping and marigold garland standing "
        "on a wooden deck at the edge of a turquoise lagoon at sunrise, a brass fire vessel at "
        "its centre, water still to the horizon, long soft reflections",

    # Rajasthan: "lakeside pheras at dusk", "shehnai in sandstone corridors"
    "dest-rajasthan":
        "A lakeside Rajput palace in Udaipur at golden hour, intricate jharokha balconies and "
        "carved sandstone pavilions lit warm from within, mirrored in still lake water, a small "
        "boat crossing, a vibrant turquoise sky above the Aravalli hills",

    # Switzerland: the Agni-Him concept — "the homa kund glowing at the foot of glaciers"
    "dest-switzerland":
        "A fire ritual on a low wooden platform at the edge of a still alpine lake in the Swiss "
        "Alps, a brass homa fire burning with a warm orange glow, snow-capped peaks and the "
        "Matterhorn reflected perfectly in the water, crisp winter air, fire and ice meeting",

    # Kyoto: "precision as devotion", "meaning lives in restraint", "dawn
    # ceremonies before the crowds". Keeps the iconic torii form but strips the
    # crowd and the saturation — mist, dawn, one gate, empty. The portrait card
    # carries the moss garden, so the pair reads as hero + detail rather than
    # two versions of the same postcard.
    "dest-kyoto":
        "A traditional Kyoto temple garden at soft dawn, vermilion torii gates and moss-covered "
        "stone lanterns beside a raked gravel path scattered with fallen cherry blossom petals, "
        "subtle mist between ancient cedar trunks, contemplative and precise",

    # Italy: "pheras at golden hour, satvik tables under pergolas"
    "dest-italy":
        "A long stone table under a vine pergola on a Tuscan estate at golden hour, linen, brass "
        "vessels and low white flowers, warm light raking across the stone, cypress and hills "
        "receding into haze, empty chairs",

    # Bali: "temple-adjacent settings where Balinese blessings precede Vaidik sankalp"
    "dest-bali":
        "A Balinese temple courtyard gate at dawn, split stone candi bentar and a tiered meru "
        "pagoda, frangipani and woven offerings on wet stone, incense smoke drifting, soft "
        "tropical light",

    # Cruises: "deck mandapas under open sky; Agni permitted at sea"
    "dest-cruises":
        "A ship's open aft deck at dusk prepared for a ceremony, a simply draped mandap and a "
        "brass fire vessel set against an open ocean horizon, warm deck lighting, a long calm "
        "wake behind",

    # ── Signature entries — from their six-part sequences ───────────────────
    # Shiva: "Smoke spreads across the pathway. Blue + gold lighting cuts through
    # the haze. Silhouette appears." + trishul carriers, Rudraksha, damru.
    "sig-shiva-entry":
        "A dark ceremonial pathway filled with low rolling smoke, hard beams of deep blue and "
        "molten gold light cutting through the haze from behind, a trishul trident standing "
        "upright in the mist, wet reflective stone underfoot, the moment before an entrance",

    # Royal: "Warm golden lights slowly illuminate the pathway", "long floral +
    # candle-lit walkway. Symmetry, balance, perfection", chhatra, shehnai.
    "sig-royal-entry":
        "A long symmetrical candle-lit palace walkway at dusk, hundreds of small flames in brass "
        "holders lining both sides, garlands of white flowers, carved sandstone arches receding "
        "into warm golden haze, a chhatra parasol on a pole at the far end",

    # Floral: "Floral arches, pastel drapes, soft flowing textures", phoolon ki
    # baarish, daylight garden venues — the one deliberately warm, open frame.
    "sig-floral-entry":
        "A garden pathway under a canopy of pastel floral arches in late golden light, soft "
        "flowing drapes and hanging blooms, rose and jasmine petals falling through warm sun, "
        "joyful but restrained",

    # Celestial: "Mist spreads across the floor. Light beams cut through like dawn
    # rays", shankh, temple bells, elevated platform, cool dawn tones.
    # First pass read as an ambiguous dark block on a table; the ritual objects
    # are now named concretely and placed in the foreground.
    "sig-celestial-entry":
        "Low mist covering the floor of a dark Indian temple hall, pale blue-white shafts of "
        "light descending through it from high above, a large conch shell and a pair of brass "
        "temple bells resting on a carved stone step in the immediate foreground, cool dawn "
        "tones with the faintest warm glow",

    # ── Weddings ────────────────────────────────────────────────────────────
    # "Not coordination. Composition — of ritual, place, emotion and precision."
    "weddings-index":
        "A Vaidik wedding mandap composed with precision in a courtyard at night, four carved "
        "pillars draped in white and marigold, a square fire altar at the centre, brass vessels "
        "and rose petals arranged in ordered rows on the floor, warm uplighting, dark sky above",

    # "Where Marriage is not an Event… but a Sacred Sanskar." Agni as the centre.
    "weddings-vaidik":
        "A square havan kund fire altar at the centre of a dark ceremonial space, bright orange "
        "flames rising from stacked wood in a copper-lined brick vessel, brass vessels, ghee and "
        "grain arranged precisely around it, firelight the only light source, warm light spilling "
        "across the stone floor",

    # "We don't move your wedding — we translate it into a new landscape."
    "weddings-destination":
        "A minimal white and blush draped mandap on a clifftop at sunset above the sea, tropical "
        "palms silhouetted, long fabric moving in the wind, warm low sun on the horizon, wide "
        "open sky",

    # "Locations are common. Concepts create emotion." Reads as concept, not venue.
    "weddings-concepts":
        "A long banquet table set beneath open sky at night, a canopy of hanging florals and "
        "hundreds of small candles above it, the table running to a vanishing point, deep blue "
        "twilight, luxurious and atmospheric",

    # "An entry is not a walk. It is the first sentence of the story your guests
    # will retell." — the baraat, seen from behind, torch-lit.
    "weddings-experiences":
        "An Indian wedding baraat procession moving away from the camera through a torch-lit "
        "palace courtyard at dusk, silhouetted figures in turbans with drums, motion blur, "
        "sparks rising from torches, warm firelight against deep blue, seen from behind",

    # ── Vaidik ──────────────────────────────────────────────────────────────
    # PURE: "No Alcohol · No Non-Veg · Pure Satvik", "every element supports
    # clarity, calmness and sacredness". The section itself renders a mandala.
    "vaidik-pure":
        "A sacred satvik still life arranged on dark stone: a brass kalash crowned with fresh "
        "mango leaves, an arrangement of white lotus and deep saffron marigold garlands, a "
        "silver bowl of sandalwood paste and a strand of rudraksha beads laid precisely beside "
        "them, warm candlelight catching the polished metal, luminous and utterly still",

    # Dining: "Tamra Patra" hand-hammered copper, banana leaf, "Crafted with
    # Intention. Served with Tradition."
    "vaidik-dining":
        "An elaborate satvik thali served on a fresh banana leaf, small hand-hammered copper "
        "bowls of colourful vegetable preparations in vivid red, green and golden yellow, "
        "garnished with fresh flowers, steam rising gently, on a dark wooden table, warm "
        "natural light from the side, precise and refined, no onion or garlic",

    # ── About ───────────────────────────────────────────────────────────────
    # "Not built on events. Built on vision."
    "about-index":
        "A grand historic theatre auditorium seen from the stage, rows of empty seats rising "
        "into warm darkness, gilded tiers catching low golden light, a single follow spot "
        "burning, vast and expectant",

    # Founder is a trained classical dancer — 1000+ stage performances.
    "about-dance":
        "An Indian classical dancer mid-turn seen from behind, Bharatanatyam costume with a "
        "pleated fan and temple jewellery, one hard spotlight against black, motion blur in the "
        "fabric, only the back and costume visible",

    # "From struggle to stage. From stage to scale. From scale to purpose."
    # Bareilly streets to Delhi stages — the figure is deliberately small.
    "about-story":
        "A lone performer silhouetted far downstage under a single hard spotlight, a vast dark "
        "empty stage and fly tower around them, haze catching the beam, the figure small in the "
        "frame, seen from behind",

    # "Meaning over decoration. Emotion over performance." One quiet flame.
    "about-philosophy":
        "A single clay diya with a small steady flame on dark weathered stone, the flame the "
        "only light in the frame, glowing brightly and throwing warm light across the stone, "
        "one quiet point of meaning, extreme minimalism",

    # "Not built on events. Built on purpose."
    "about-vision":
        "Layered Himalayan ridges at first light seen from a high pass, peaks receding into blue "
        "haze in bands, the nearest ridge catching the first gold, immense distance and silence",

    # "Director · Choreographer · Designer · Visionary" — at work, from behind.
    # The first pass returned a lit, front-facing man: a fabricated portrait of a
    # real person, which is exactly what this slot must never be. The mirror wall
    # is now doing the work — every figure in frame faces away.
    "about-founder":
        "A rehearsal studio at night photographed from the back of the room, the far wall a "
        "mirrored wall reflecting a line of dancers who are all turned away from the camera, a "
        "director's chair and a lit laptop on a table in the immediate foreground, warm "
        "practical lights, atmospheric haze, backs of heads only",

    # ── Destinations section ────────────────────────────────────────────────
    # "Every destination is an experience system — landscape, culture, concept
    # and ritual, composed together." One island legible as one composition.
    # First pass came back bright and saturated, out of step with the rest of
    # the set; pushed toward dawn haze and muted colour.
    "destinations-index":
        "Aerial view of a private island at first light, a ring of pale lagoon around dense "
        "green jungle, a single long jetty leading to a thatched pavilion, low mist over the "
        "trees, vivid turquoise water and saturated green, soft atmospheric haze, the whole island legible as "
        "one composition",

    # "India is not one destination — it is an architecture of worlds." The ghats
    # carry the spiritual/vaidik register, which is the brand's core.
    "destinations-india":
        "The Varanasi ghats at dawn seen from the river, tiers of stone steps and temple spires "
        "in warm mist, a few small boats, oil lamps floating on the water, soft golden haze, "
        "vast and layered",

    # ── Event IP — each states its own line ─────────────────────────────────
    # "Owned. Designed. Delivered." A built environment, not a rented stage.
    "ip-index":
        "A vast custom-built event stage at night, a distinctive sculptural set piece lit from "
        "within, sweeping beams and haze, rigging above, silhouetted audience below, ambitious "
        "and architectural",

    # "designs not just stalls but entire exhibition worlds — flow, pacing,
    # dwell and discovery"
    "ip-exhibitions":
        "A modern exhibition hall with a sequence of illuminated arched pavilions and sleek "
        "display booths receding into depth, visitors only as distant silhouettes, warm ambient "
        "lighting with accent spotlights, polished floor reflecting the colour",

    # "Launch environments built with mechanical precision — vehicles presented
    # as protagonists."
    "ip-automotive":
        "A single luxury car on a dark stage under a low horizontal blade of light, wet black "
        "floor mirroring it, dramatic rim light tracing the bodywork, vivid reflected colour, sculptural "
        "and cinematic, no badges",

    # "Ceremonies engineered for gravity — staging, script, reveal rhythm."
    "ip-awards":
        "A grand auditorium with a single golden lit podium on a vast stage, a polished awards "
        "statuette on a plinth beside it, a huge glowing backdrop behind, rows of seating rising "
        "into warm darkness, one dramatic overhead beam, gravity and anticipation",

    # "products staged with the respect of museum curation"
    "ip-products":
        "Handcrafted Indian objects on individual lit plinths in a gallery, each isolated by a "
        "narrow museum spotlight, brass, textile and ceramic glowing against a deep warm "
        "background, immaculate and reverent",

    # "League formats owned end to end — fixture design, venue experience,
    # broadcast readiness."
    "ip-sports":
        "A floodlit stadium at night from a high camera position, the pitch brilliant green "
        "under banks of floodlights, a dense crowd filling the stands as a dark mass of "
        "silhouetted figures, players small and in motion on the pitch, crisp white line "
        "markings, dramatic scale and clarity",

    # "Runways directed like cinema — walk choreography drawn from Third Eye's
    # performance roots."
    "ip-fashion":
        "A luminous white runway receding through a dark hall, silhouetted seated guests on both "
        "sides, a single model far down the runway in silhouette mid-stride wearing avant-garde "
        "Indian couture with a sculptural silhouette, dramatic spotlights and haze",

    # "crowd architecture, security coordination, zero-error stages"
    "ip-political":
        "A vast open ground at dusk seen from high above, an immense orderly crowd filling it, "
        "tall sound towers and crowd barriers arranged in precise geometric rows, a lit stage "
        "and barricade lines far in the distance, disciplined geometry and scale",

    # "sound, seating and sightlines designed around devotion rather than spectacle"
    "ip-devotional":
        "A riverside aarti at night seen from across the water, tiers of brass oil lamps raised "
        "in glowing arcs, temple spires behind, drifting smoke, warm firelight on dark water, "
        "devotees only as distant silhouettes",

    # "stage, light, artist logistics and crowd energy managed as one instrument"
    "ip-concerts":
        "A massive concert seen from within the crowd at night, silhouetted arms raised "
        "throughout, a brilliant stage far ahead with beams cutting the haze, pyrotechnics "
        "bursting above it, total environment",

    # ── Production ──────────────────────────────────────────────────────────
    # "Behind every frame. Structured. Managed. Delivered by Third Eye."
    "production-index":
        "A film set at night seen from behind the camera position, a dolly track, lighting rigs "
        "and a lit set in the distance, crew as backlit silhouettes, haze and warm practicals, "
        "structured and deliberate",

    # "Location coordination, Crew management, Equipment logistics, Schedule execution"
    "production-feature-films":
        "A large night exterior film set, a heavy cinema camera on a crane, a director's monitor "
        "glowing at the video village, banks of HMI lights on stands, a lit facade in the "
        "background, crew silhouettes and cable runs, ambitious scale",

    # "Small crews, sharp turnarounds." First pass framed the operator's head
    # large in shot; this frames the equipment instead and pushes the head out.
    "production-short-films":
        "Close detail of a shoulder-mounted cinema camera rig on an intimate studio set, warm "
        "natural window light raking across it, the operator's hands and forearm gripping it, "
        "the head out of frame, shallow depth of field, framing the equipment rather than the "
        "person",

    # "Reality does not reschedule. We adjust." / "Real environments"
    "production-documentaries":
        "A documentary camera on a tripod standing in a remote open landscape at golden hour, a "
        "lone figure far in the distance out of focus, long shadows, wind in the grass, patient "
        "and observational",

    # "Content pipelines that keep publishing honest." Volume, consistency, efficiency.
    "production-digital-content":
        "A recording studio at night, a condenser microphone and headphones in the "
        "foreground, acoustic panelling and warm desk lamps behind, a brightly lit screen "
        "glowing with colour, precise and alive",

    # "The brand's voice, protected frame by frame."
    "production-branded-content":
        "A product film set, a lit tabletop holding a single object under a softbox, a "
        "director's monitor glowing with a framed shot beside it, a cinema camera on a tripod "
        "just out of focus in the foreground, warm accent light, controlled and deliberate",

    # "One day. Every department on time."
    "production-ad-shoots":
        "An advertising shoot set with a seamless backdrop, large softboxes and flags on stands, "
        "a lit tabletop and a product on a rotating platform, gaffer tape and cable runs, "
        "precision studio lighting, purposeful equipment",

    # ── Contact ─────────────────────────────────────────────────────────────
    # "Let yours have meaning." / "Every celebration has a beginning."
    "contact":
        "An elegant table setting at night in a dark room, brass candlesticks with lit candles, "
        "crystal glassware, a low arrangement of deep red roses, warm bokeh behind, the "
        "beginning of a celebration",

    # ── Cinematic scroll hero journey ───────────────────────────────────────
    # A four-beat narrative arc: threshold -> invocation -> anticipation ->
    # revelation. The client brief writes these with people facing camera; the
    # narrative survives intact without fabricating faces by putting the figure
    # in back view (beat 1) and in backlight (beat 4), which is also the more
    # cinematic choice. Beat 3 has no figure at all — it is the only still life.
    "cinematic-beat1-threshold":
        "A grand palace corridor with a long symmetrical colonnade of carved sandstone pillars "
        "receding to a vanishing point, warm golden light spilling through ornate jharokha "
        "windows, a single figure in a deep burgundy raw silk sherwani with intricate gold zari "
        "work and a pearl-encrusted safa walking away from the camera toward the light, seen "
        "entirely from behind, dramatic chiaroscuro",

    "cinematic-beat2-invocation":
        "A majestic Indian wedding mandap at dusk, four sacred pillars carved with intricate "
        "motifs and draped in rich crimson and gold silk, cascading marigold garlands, rows of "
        "traditional percussionists in ivory and gold raw silk arranged symmetrically around it "
        "and readable only as silhouettes, warm firelight from brass diyas, a deep orange and "
        "violet evening sky",

    "cinematic-beat3-anticipation":
        "An intricate bridal ensemble displayed on a plain wooden dress form: a deep crimson "
        "Banarasi silk lehenga with gold zari embroidery, kundan jewellery, kaleere hanging at "
        "the wrists, a red chunri veil, scattered rose petals and a brass mirror beside it, "
        "warm candlelight, still life, macro detail",

    "cinematic-beat4-revelation":
        "A bride in a vibrant red and gold Banarasi silk lehenga with heavy kundan jewellery "
        "standing in a doorway framed by marigold garlands, her figure rim-lit and largely in "
        "silhouette against warm golden backlight, a groom in a burgundy sherwani seen from "
        "behind in the foreground, marigold petals suspended in the air, the reveal",

    # ── About — team ────────────────────────────────────────────────────────
    # Faces are composed out: the group is read from behind and over the
    # shoulder, which is also how this photograph is actually taken.
    "about-team-vision":
        "A team gathered around a large drafting table covered with venue blueprints and "
        "lighting plots, seen from behind and over their shoulders as they lean over the plans, "
        "a palace wedding design spread across the table, warm overhead lighting, collaborative "
        "and focused",

    # ── Homepage pathway cards ──────────────────────────────────────────────
    # The brief's three compositions, kept, with one rewrite: its destination
    # prompt asked for a "surreal travel fantasy aesthetic" compositing alpine
    # peaks with a lake palace. That contradicts the brand's real-world editorial
    # staging rule — the whole set is built on photographs that could have been
    # taken. Rewritten as a real twilight lake palace, which carries the same
    # "somewhere extraordinary" idea without the fantasy composite.
    "pathways-vaidik":
        "A close macro view of sacred ritual offerings, pure ghee dripping from a carved wooden "
        "ladle into a small sacred flame, surrounded by fresh marigold garlands and rose petals, "
        "brass ritual vessels, warm firelight catching every detail",

    "pathways-destination":
        "A lakeside palace at twilight seen from a stone jetty, warm lantern-lit pavilions "
        "reflected in still dark water, a wide starry sky above, somewhere extraordinary and "
        "completely real",

    "pathways-concepts":
        "An elegant overhead flat-lay of traditional Indian wedding elements arranged on rich "
        "jewel-toned silk: intricate gold jewellery, kaleere, a red chunri, decorative brass "
        "pieces and scattered rose petals, soft directional light",
}

# ── Portrait cards ───────────────────────────────────────────────────────────
# Not a crop of the wide hero — a genuinely portrait-composed frame of the same
# subject. Cropping 3:4 out of a 16:9 source throws away 62% of the image and
# upscales what is left; composing for the card gives a real photograph.
CARD_PROMPTS = {
    "dest-maldives":
        "A single overwater villa on stilts above a turquoise Maldives lagoon at dusk, warm lit "
        "interior, still water, a wooden ladder descending into it",
    "dest-rajasthan":
        "An ornate carved sandstone jharokha window of a Rajasthani palace at golden hour, "
        "intricate lattice work, warm light raking across the stone, lake "
        "glimpsed below",
    "dest-switzerland":
        "A brass homa fire burning on snow with the Matterhorn rising above it at dawn, "
        "alpenglow on the summit, fire and ice in one frame",
    "dest-kyoto":
        "A Kyoto moss garden at dawn, raked gravel and a single set stone, a stone lantern and "
        "wet moss, mist between cedar trunks",
    "dest-italy":
        "A tall cypress against a misty Tuscan hillside at golden hour, a stone pergola edge and "
        "warm honeyed wall in the foreground",
    "dest-bali":
        "A tiered Balinese meru pagoda in silhouette against a burning sunset sky, "
        "frangipani and woven offerings on wet stone below",
    "dest-cruises":
        "The bow of a luxury cruise liner cutting through a calm dusk ocean, warm deck lights "
        "above, long-exposure water, open horizon",
    "sig-shiva-entry":
        "Thick smoke and converging blue and gold light beams on a dark stage, a trishul trident "
        "standing upright in the mist, wet reflective stone",
    # First pass produced a European baroque corridor with chandeliers — wrong
    # continent for a Rajput wedding. Anchored explicitly to Indian architecture.
    "sig-royal-entry":
        "An ornate carved sandstone Rajput palace archway with a scalloped cusped arch and "
        "jharokha lattice screen, opening onto a candle-lit corridor lined with brass oil lamps, "
        "strong symmetrical composition, warm golden light on the stone, Indian heritage "
        "architecture",
    "sig-floral-entry":
        "A cascade of marigold and rose garlands hanging in warm golden light, petals falling "
        "through the beam, luminous against a richly coloured backdrop",
    "sig-celestial-entry":
        "Pale light shafts descending through low mist onto dark temple steps, a conch shell and "
        "brass bell in the foreground, cool dawn tones",
}


# ── Workers AI plumbing ──────────────────────────────────────────────────────
def load_token() -> str:
    if not os.path.exists(WRANGLER_CFG):
        sys.exit(f"wrangler config not found at {WRANGLER_CFG} — run `npx wrangler login`")
    with open(WRANGLER_CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    tok = cfg.get("oauth_token")
    if not tok:
        sys.exit("no oauth_token in wrangler config — run `npx wrangler login`")
    return tok


# wrangler's OAuth access token lives about an hour and is paired with a
# long-lived refresh token. Running any wrangler command rewrites the config
# with a fresh access token, so on a 401 we shell out and re-read rather than
# failing the whole batch — which matters because a full run takes ~13 minutes
# and the token can expire mid-flight.
_TOKEN = None
_TOKEN_LOCK = threading.Lock()


def current_token(force_refresh: bool = False) -> str:
    global _TOKEN
    with _TOKEN_LOCK:
        if force_refresh or _TOKEN is None:
            if force_refresh:
                print("  · refreshing Cloudflare OAuth token via wrangler…")
                subprocess.run(
                    ["npx", "wrangler", "whoami"],
                    capture_output=True,
                    timeout=180,
                    cwd=os.path.dirname(HERE),
                )
            _TOKEN = load_token()
        return _TOKEN


def multipart(fields: dict) -> tuple[bytes, str]:
    boundary = "----thirdEye" + uuid.uuid4().hex
    chunks = [
        f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, v in fields.items()
    ]
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def compose_prompt(slot: str, subject: str, is_card: bool = False) -> str:
    """Assemble the final prompt from its independent layers.

    Order matters: the model weights the opening of a prompt most heavily, so
    the concrete subject comes first and the shared look comes last, with optics
    and colour in between.

    Kept as separate layers rather than one long string so any single axis can be
    re-aimed without touching the others — swap a lens, move the subject, restage
    the palette — which is how the client's shot list iterates and why it is
    worth preserving that structure here.
    """
    # A card is the portrait sibling of a hero, so it reads the hero's colour and
    # exclusion entries rather than carrying duplicates of its own.
    base_slot = slot[5:] if slot.startswith("card-") else slot
    parts = [subject.strip()]

    # 1 — optics and composition
    if is_card:
        # Cards stay on 50mm regardless of their hero's focal length: a 3:4 crop
        # out of a 24mm wide angle carries visible perspective distortion, which
        # is exactly what a portrait crop should avoid.
        parts.append("50mm cinematic lens")
        parts.append(CARD_FRAME)
    else:
        parts.append(LENS.get(base_slot, DEFAULT_LENS))
        parts.append(FRAME.get(base_slot, DEFAULT_FRAME))
        parts.append(SCRIM_BASE)

    # 2 — the dominant hue story for this slot
    parts.append(COLOR.get(base_slot, DEFAULT_COLOR))

    # 3 — restraint, then the shared look, then the face policy
    excl = [EXCLUDE]
    if any(h in subject.lower() for h in FLORAL_HINTS):
        excl.append(FLORAL_EXCLUDE)
    if base_slot in EXCLUDE_EXTRA:
        excl.append(EXCLUDE_EXTRA[base_slot])
    parts += [", ".join(excl), HOUSE.strip(", "), NO_FACES.strip(", ")]
    return ", ".join(p for p in parts if p)


def generate(prompt: str, width: int, height: int) -> bytes:
    """Call Workers AI and return raw JPEG bytes. Retries transient failures."""
    body, ctype = multipart({"prompt": prompt, "width": str(width), "height": str(height)})
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
    last = None
    refreshed = False
    for attempt in range(RETRIES):
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Authorization": f"Bearer {current_token()}", "Content-Type": ctype},
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.loads(resp.read())
            b64 = (payload.get("result") or {}).get("image")
            if not b64:
                raise RuntimeError(f"no image in response: {str(payload)[:200]}")
            return base64.b64decode(b64)
        except urllib.error.HTTPError as exc:
            detail = exc.read()[:300].decode(errors="replace")
            last = f"HTTP {exc.code}: {detail}"
            # Expired access token — refresh once and try again immediately.
            if exc.code == 401 and not refreshed:
                refreshed = True
                current_token(force_refresh=True)
                continue
            # Daily free-tier exhaustion — retrying now is pointless, the
            # allowance resets at 00:00 UTC.
            if "neurons" in detail.lower() or "daily" in detail.lower():
                raise RuntimeError("QUOTA: " + detail)
            # 4xx other than 429 will not fix themselves
            if exc.code not in (429, 500, 502, 503, 504):
                raise RuntimeError(last)
        except Exception as exc:  # timeouts, transient network
            last = f"{type(exc).__name__}: {exc}"
        if attempt < RETRIES - 1:
            time.sleep(4 * (attempt + 1))
    raise RuntimeError(last)


def job_list(only, cards_only, extras=False):
    """(slot, prompt, width, height, out_path) for everything to generate."""
    jobs = []
    # Slots backed by a real photograph (scripts/place_supplied.py). Never
    # generated — see the `supplied` guard in the manifest loop below.
    supplied = {e["slot"] for e in MANIFEST if e.get("supplied")}
    if not cards_only:
        for entry in MANIFEST:
            slot = entry["slot"]
            if only and slot not in only:
                continue
            # `opt_in` slots belong to sections that do not exist yet, and they
            # are the most expensive in the set. Skipped unless explicitly asked
            # for, so a default run cannot spend the budget on orphaned files.
            if entry.get("opt_in") and not extras and not only:
                continue
            # `supplied` slots are real photographs placed by
            # scripts/place_supplied.py. A model must never overwrite a real
            # person's likeness, so these are skipped even under --force and
            # even under --extras. Only naming the slot in --only can reach
            # them, which makes the override deliberate rather than accidental.
            if entry.get("supplied") and slot not in (only or []):
                continue
            w, h = GEN_SIZE.get(entry["aspect"], (1536, 864))
            if slot in FULL_BLEED_SLOTS:
                w, h = HERO_CINEMATIC_SIZE
            jobs.append(
                (slot, compose_prompt(slot, PROMPTS[slot]), w, h, os.path.join(OUT, f"{slot}.jpg"))
            )
    for slot, prompt in CARD_PROMPTS.items():
        card_slot = f"card-{slot}"
        # Cards are only pulled in when named explicitly (`--only card-dest-kyoto`)
        # or via --cards. Generating them alongside a hero by default silently
        # doubles the Neuron cost of a targeted rerun.
        if only and card_slot not in only:
            continue
        # Only the cards actually backed by supplied imagery are skipped — NOT
        # every card whose hero happens to be supplied. CARD_DERIVATIONS keys a
        # card by its hero's slot, so conflating the two would silently freeze
        # the seven destination cards, which are still the previous generation.
        if slot in SUPPLIED_CARDS and card_slot not in (only or []):
            continue
        w, h = CARD_SIZE
        jobs.append(
            (
                card_slot,
                compose_prompt(card_slot, prompt, is_card=True),
                w,
                h,
                os.path.join(OUT, f"card-{slot}.jpg"),
            )
        )
    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None, help="slot ids to generate")
    ap.add_argument("--cards", action="store_true", help="only the portrait cards")
    ap.add_argument("--extras", action="store_true", help="include opt-in slots (unbuilt sections)")
    ap.add_argument("--force", action="store_true", help="regenerate existing files")
    args = ap.parse_args()

    current_token()  # fail fast if wrangler is not authenticated
    jobs = job_list(args.only, args.cards, args.extras)
    todo = [j for j in jobs if args.force or not os.path.exists(j[4]) or os.path.getsize(j[4]) < 10_000]

    skipped = len(jobs) - len(todo)
    print(f"{len(jobs)} slots · {skipped} already present · {len(todo)} to generate")
    if not todo:
        return

    est = sum(max(1, round(w * h / 262144)) for _, _, w, h, _ in todo) * 26.05
    print(f"estimated {est:,.0f} Neurons (~{est/10000*100:.0f}% of the daily free allowance)\n")

    done = failed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(generate, prompt, w, h): (slot, path)
            for slot, prompt, w, h, path in todo
        }
        for fut in as_completed(futures):
            slot, path = futures[fut]
            try:
                data = fut.result()
                with open(path, "wb") as fh:
                    fh.write(data)
                done += 1
                print(f"  [{done + failed:>2}/{len(todo)}] ok   {slot:<32} {len(data)//1024:>4} KB")
            except Exception as exc:
                failed += 1
                print(f"  [{done + failed:>2}/{len(todo)}] FAIL {slot:<32} {exc}")

    print(f"\ndone: {done} written, {failed} failed → {OUT}")
    if failed:
        print("re-run the same command to retry only the failures (it is resumable)")


if __name__ == "__main__":
    main()
