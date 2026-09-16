#!/usr/bin/env python3
"""
kling_prompts — the AI-generation brief for every site image.

Each slot carries a fully-crafted Kling text-to-image prompt, grounded in the
page copy from scripts/image_manifest.py (see scripts/IMAGE_RULESET.md). The
prompts are written in the brand's "Cinematic Minimalism" palette:

    gold   #b89b5e  -> "warm gold / amber"
    agni   #a9552b  -> "agni orange / crimson"
    ink    #0a0a0a  -> "deep charcoal / ink shadows"
    ivory  #f5f1e8  -> "ivory / cream highlights"

They are meant for the connected Kling AI connector (text-to-image). The
`out` paths match scripts/image_manifest.py exactly, relative to public/.

Usage (once the Kling MCP tool is available):
    from kling_prompts import SLOTS
    for s in SLOTS:
        # call mcp__kling-ai-plugin__text_to_image(prompt=s["prompt"], ...)
        # then resize/crop to (s["width"], aspect s["aspect"]) with PIL
"""

# Shared style tail — keeps every image in one coherent visual language.
STYLE = (
    "cinematic minimalism, warm gold and amber tones, deep charcoal shadows, "
    "ivory and cream highlights, photorealistic, ultra-detailed, professional "
    "photography, soft volumetric lighting, shallow depth of field, high "
    "resolution, film grain, no text, no watermark, no logo, no signature"
)

# Shared negative prompt.
NEGATIVE = (
    "cartoon, illustration, painting, sketch, 3d render, low resolution, "
    "blurry, deformed, extra limbs, bad anatomy, oversaturated, cluttered, "
    "watermark, text, logo, handwritten, stocky, flat lighting"
)

# slot, out(relative to public/), aspect(w,h), width, prompt
SLOTS = [
    # ── Homepage ──────────────────────────────────────────────────────────
    dict(
        slot="hero-cinematic",
        out="images/hero-cinematic.jpg",
        aspect=(16, 9), width=1920,
        prompt=(
            "Grand illuminated Indian heritage palace courtyard at night, "
            "towering arched marble colonnades draped in warm golden light, a "
            "hint of an elegant celebration beyond, luxurious and serene, "
            "cinematic wide establishing shot, no clear faces, " + STYLE
        ),
    ),
    # ── Destinations (7 heroes) ───────────────────────────────────────────
    dict(
        slot="dest-maldives",
        out="images/destinations/maldives/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Turquoise overwater villa on a private Maldives island at golden "
            "hour, glass-clear lagoon, wooden decks, infinity edge, palm "
            "silhouettes, serene luxury, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="dest-rajasthan",
        out="images/destinations/rajasthan/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Lake Palace glowing at dusk on a calm Indian lake, Rajasthan, "
            "golden fort silhouettes, mirror reflection in water, royal "
            "heritage, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="dest-switzerland",
        out="images/destinations/switzerland/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Matterhorn peak at sunrise above an alpine village, snow and a "
            "fire-lit chalet, crisp blue and warm gold, 'fire meets ice' mood, "
            "cinematic landscape, " + STYLE
        ),
    ),
    dict(
        slot="dest-kyoto",
        out="images/destinations/kyoto/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Vermilion torii gates winding through a misty Kyoto forest at "
            "dawn, precision and devotion, cinematic, rich red and gold, " + STYLE
        ),
    ),
    dict(
        slot="dest-italy",
        out="images/destinations/italy/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Lake Como villa with cypress trees and mountain backdrop at "
            "golden hour, elegant la dolce vita, warm gold and green, "
            "cinematic, " + STYLE
        ),
    ),
    dict(
        slot="dest-bali",
        out="images/destinations/bali/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Cliffside Balinese temple (Pura Uluwatu) at sunset against the "
            "Indian Ocean, island of the gods, warm orange and gold, "
            "cinematic, " + STYLE
        ),
    ),
    dict(
        slot="dest-cruises",
        out="images/destinations/cruises/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Luxury cruise liner sailing into a vast ocean sunset horizon, a "
            "world that moves with you, expansive, warm gold and deep blue, "
            "cinematic, " + STYLE
        ),
    ),
    # ── Signature entries (4) ─────────────────────────────────────────────
    dict(
        slot="sig-shiva-entry",
        out="images/signature/shiva-entry-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Bronze Nataraja (dancing Shiva) statue enveloped in blue and gold "
            "light with drifting sacred smoke, raw spiritual energy, cinematic, "
            "photorealistic sculpture, " + STYLE
        ),
    ),
    dict(
        slot="sig-royal-entry",
        out="images/signature/royal-entry-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Golden palace corridor archway with a marigold floral pathway and "
            "warm shehnai-lit ambience, walk the path of kings, royal luxury, "
            "gold and amber, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="sig-floral-entry",
        out="images/signature/floral-entry-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Cascade of marigold and rose petals falling like rain (phoolon ki "
            "baarish) over an elegant celebration arch, joyous festival, warm "
            "gold and crimson, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="sig-celestial-entry",
        out="images/signature/celestial-entry-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Misty temple interior with beams of light descending, rows of "
            "glowing oil lamps (diya) and a conch shell, descent from the "
            "divine, ethereal, ivory and gold, cinematic, " + STYLE
        ),
    ),
    # ── Weddings (5) ──────────────────────────────────────────────────────
    dict(
        slot="weddings-index",
        out="images/weddings/index-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Elegant Hindu wedding mandap at golden hour, couple silhouette in "
            "ritual, floral drapes, celebration becomes experience, warm gold "
            "and ivory, cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="weddings-vaidik",
        out="images/weddings/vaidik-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Sacred havan kund fire ritual with priests, pure satvik "
            "ceremony, spiritual, warm amber and gold, cinematic, no clear "
            "faces, " + STYLE
        ),
    ),
    dict(
        slot="weddings-destination",
        out="images/weddings/destination-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Beach mandap wedding setup on tropical sand at sunset, ocean "
            "behind, divine celebrations in new landscapes, warm gold and teal, "
            "cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="weddings-concepts",
        out="images/weddings/concepts-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Lavishly decorated wedding mandap with cascading florals and "
            "chandeliers, concepts create emotion, luxury, gold and ivory, "
            "cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="weddings-experiences",
        out="images/weddings/experiences-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Vibrant Indian baraat procession, groom on an ornate horse, dhol "
            "players, festive street celebration, energetic, warm gold and "
            "crimson, cinematic, no clear faces, " + STYLE
        ),
    ),
    # ── Vaidik (2) ────────────────────────────────────────────────────────
    dict(
        slot="vaidik-pure",
        out="images/vaidik/pure-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "A single white lotus floating on still dark water, symbol of "
            "purity (satvik), minimal and serene, ivory and gold light, "
            "cinematic macro, " + STYLE
        ),
    ),
    dict(
        slot="vaidik-dining",
        out="images/vaidik/dining.jpg",
        aspect=(4, 5), width=900,
        prompt=(
            "Traditional Indian satvik thali on banana leaf and copper (tamra "
            "patra), vegetarian purity, top-down, warm gold and earth tones, "
            "cinematic food photography, " + STYLE
        ),
    ),
    # ── About (6) ─────────────────────────────────────────────────────────
    dict(
        slot="about-index",
        out="images/about/hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Grand empty theatre auditorium with sweeping balconies and a "
            "stage under warm house lights, built on vision, gold and "
            "charcoal, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="about-dance",
        out="images/about/archival-dance.jpg",
        aspect=(4, 5), width=900,
        prompt=(
            "Indian classical dancer (Bharatanatyam) mid-pose in a spotlight, "
            "intricate costume, heritage, warm gold and ink, cinematic, no "
            "clear face, " + STYLE
        ),
    ),
    dict(
        slot="about-story",
        out="images/about/story-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Empty theatre stage with a single dramatic spotlight beam through "
            "curtains, from struggle to stage, moody, gold and charcoal, "
            "cinematic, " + STYLE
        ),
    ),
    dict(
        slot="about-philosophy",
        out="images/about/philosophy-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "A single oil lamp (diya) flame in darkness, calm and meaningful, "
            "meaning over decoration, ivory and gold glow, cinematic macro, " + STYLE
        ),
    ),
    dict(
        slot="about-vision",
        out="images/about/vision-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Distant mountain summit above a sea of clouds at sunrise, far "
            "horizon, built on purpose, gold and cool blue, cinematic "
            "landscape, " + STYLE
        ),
    ),
    dict(
        slot="about-founder",
        out="images/about/founder-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Creative director choreographing dancers in a rehearsal studio, "
            "working leadership, warm practical lights, gold and ink, "
            "cinematic, no clear faces, " + STYLE
        ),
    ),
    # ── Destinations section (2) ───────────────────────────────────────────
    dict(
        slot="destinations-index",
        out="images/destinations/index-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Aerial view of a private tropical island with turquoise lagoon "
            "and overwater villas, different worlds one standard, expansive, "
            "gold and teal, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="destinations-india",
        out="images/destinations/india-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Taj Mahal at sunrise with soft mist, symbol of India's heritage, "
            "one country seven worlds, warm gold and ivory, cinematic, " + STYLE
        ),
    ),
    # ── Event IP (11) ─────────────────────────────────────────────────────
    dict(
        slot="ip-index",
        out="images/ip/index-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Spectacular concert stage production with dramatic lighting rigs "
            "and lasers, owned signature experiences, energy, gold and ink, "
            "cinematic, " + STYLE
        ),
    ),
    dict(
        slot="ip-exhibitions",
        out="images/ip/exhibitions-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Immersive museum exhibition gallery with sculptural display stands "
            "and curated lighting, design entire exhibition worlds, refined, "
            "gold and charcoal, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="ip-automotive",
        out="images/ip/automotive-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Luxury sports car on a turntable in a dark studio with rim "
            "lighting, vehicles as protagonists, gold and ink, cinematic "
            "automotive photography, " + STYLE
        ),
    ),
    dict(
        slot="ip-awards",
        out="images/ip/awards-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Elegant awards gala stage with a glowing trophy and ceremonious "
            "lighting, ceremonies engineered for gravity, gold and charcoal, "
            "cinematic, " + STYLE
        ),
    ),
    dict(
        slot="ip-products",
        out="images/ip/best-products-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Premium Indian product displayed like a museum piece on a "
            "pedestal with spotlight, staged with respect of curation, gold "
            "and ivory, cinematic product photography, " + STYLE
        ),
    ),
    dict(
        slot="ip-sports",
        out="images/ip/sports-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Floodlit night stadium with empty pitch and dramatic arena "
            "lighting, competition meets community, gold and ink, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="ip-fashion",
        out="images/ip/fashion-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Fashion runway with a model walking under directional lights, "
            "runways directed like cinema, elegance, gold and charcoal, "
            "cinematic fashion photography, " + STYLE
        ),
    ),
    dict(
        slot="ip-political",
        out="images/ip/political-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Large orderly public gathering in India with staged crowd "
            "architecture and banners, scale management meets protocol, vast, "
            "gold and ink, cinematic aerial, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="ip-devotional",
        out="images/ip/devotional-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Ganga aarti ceremony on Varanasi ghats, rows of burning lamps and "
            "devotees in silhouette, devotion over spectacle, warm gold and "
            "ink, cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="ip-concerts",
        out="images/ip/concerts-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Live music concert stage with crowd silhouettes and immersive "
            "light show, total environment total energy, gold and ink, "
            "cinematic, " + STYLE
        ),
    ),
    # ── Production (8) ─────────────────────────────────────────────────────
    dict(
        slot="production-index",
        out="images/production/index-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Behind-the-scenes film production command center with monitors "
            "and crew, behind every frame, technical, gold and charcoal, "
            "cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="production-feature-films",
        out="images/production/feature-films.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Movie set with a director holding a clapperboard in front of a "
            "camera on a soundstage, long-form complexity, gold and ink, "
            "cinematic, no clear face, " + STYLE
        ),
    ),
    dict(
        slot="production-short-films",
        out="images/production/short-films.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Cameraman with a shoulder rig filming on location, small crew, "
            "sharp turnarounds, gold and charcoal, cinematic, no clear face, " + STYLE
        ),
    ),
    dict(
        slot="production-documentaries",
        out="images/production/documentaries.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Documentary crew filming an interview with a handheld camera and "
            "tripod outdoors, candid, gold and earth, cinematic, no clear "
            "faces, " + STYLE
        ),
    ),
    dict(
        slot="production-digital-content",
        out="images/production/youtube-digital.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Modern recording and podcast studio with microphone, desk and "
            "acoustic panels, content pipelines, warm gold and ink, cinematic, " + STYLE
        ),
    ),
    dict(
        slot="production-branded-content",
        out="images/production/branded-content.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Branded content shoot in a creative studio with camera and "
            "teleprompter, brand's voice protected, gold and charcoal, "
            "cinematic, no clear faces, " + STYLE
        ),
    ),
    dict(
        slot="production-ad-shoots",
        out="images/production/ad-shoots.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Advertising photo shoot set with softbox lighting rig and camera, "
            "every department on time, gold and ink, cinematic, no clear "
            "face, " + STYLE
        ),
    ),
    # ── Contact (1) ────────────────────────────────────────────────────────
    dict(
        slot="contact",
        out="images/contact-hero.jpg",
        aspect=(16, 9), width=1600,
        prompt=(
            "Elegant celebration table setting with fine china, candlelight "
            "and florals at dusk, every celebration has a beginning, warm "
            "gold and ivory, cinematic, " + STYLE
        ),
    ),
]

# ── Portrait cards (3:4, 900px) — tighter crops of the hero subjects ────────
CARDS = [
    dict(slot="dest-maldives", out="images/destinations/maldives/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Overwater villa balcony detail, turquoise lagoon, warm "
                 "golden hour, luxury, portrait crop, gold and teal, "
                 "cinematic, " + STYLE)),
    dict(slot="dest-rajasthan", out="images/destinations/rajasthan/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Lake palace facade detail at dusk, golden arches, "
                 "reflection, portrait crop, gold and amber, cinematic, " + STYLE)),
    dict(slot="dest-switzerland", out="images/destinations/switzerland/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Matterhorn summit against blue sky with snow, portrait "
                 "crop, gold and blue, cinematic, " + STYLE)),
    dict(slot="dest-kyoto", out="images/destinations/kyoto/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Single vermilion torii gate in a misty forest, portrait "
                 "crop, red and gold, cinematic, " + STYLE)),
    dict(slot="dest-italy", out="images/destinations/italy/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Lake Como villa balcony with cypress, portrait crop, gold "
                 "and green, cinematic, " + STYLE)),
    dict(slot="dest-bali", out="images/destinations/bali/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Balinese temple gate (candi bentar) at sunset, portrait "
                 "crop, orange and gold, cinematic, " + STYLE)),
    dict(slot="dest-cruises", out="images/destinations/cruises/card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Cruise ship bow cutting through ocean at sunset, portrait "
                 "crop, gold and blue, cinematic, " + STYLE)),
    dict(slot="sig-shiva-entry", out="images/signature/shiva-entry-card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Bronze Nataraja detail with blue-gold light and sacred "
                 "smoke, portrait crop, cinematic, photorealistic sculpture, " + STYLE)),
    dict(slot="sig-royal-entry", out="images/signature/royal-entry-card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Golden archway with marigold pathway detail, portrait crop, "
                 "gold and amber, cinematic, " + STYLE)),
    dict(slot="sig-floral-entry", out="images/signature/floral-entry-card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Falling marigold petals close-up, portrait crop, gold and "
                 "crimson, cinematic, " + STYLE)),
    dict(slot="sig-celestial-entry",
         out="images/signature/celestial-entry-card.jpg",
         aspect=(3, 4), width=900,
         prompt=("Rows of glowing diya lamps in mist, portrait crop, ivory "
                 "and gold, cinematic, " + STYLE)),
]

ALL = SLOTS + CARDS


def by_slot(slot):
    for s in ALL:
        if s["slot"] == slot:
            return s
    return None


if __name__ == "__main__":
    print(f"Total generation slots: {len(ALL)} "
          f"({len(SLOTS)} heroes + {len(CARDS)} cards)")
    for s in ALL:
        print(f"  {s['slot']:24s} {s['aspect'][0]}:{s['aspect'][1]} "
              f"w={s['width']:4d}  -> {s['out']}")
