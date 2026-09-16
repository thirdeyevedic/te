#!/usr/bin/env python3
"""
place_supplied — place client-supplied photography into the site's image slots.

Run:  python scripts/place_supplied.py

Every entry below is a real photograph, not a generation. Each is cropped to its
slot's aspect, encoded as a progressive JPEG with 4:4:4 chroma
(`image_lib.save_jpeg`) so the saturated palette survives, and written to a path
the pages already reference — so most placements need no change in `src/`.

Why this exists rather than `apply_generated.py`: the manifest's prompts describe
concrete physical details (a trishul, shehnai players, a floral arch, copper
Tamra Patra, mist and light beams). A supplied frame carries those details
literally instead of approximately. The founder slot is stronger still — it must
never be invented, because generating a portrait of a real, named person
fabricates a likeness.

Sourcing and rules
------------------
`src` is an absolute path to the supplied file. Keep the originals where they
are; this script only reads them. Anything placed here is flagged `supplied=True`
in `image_manifest.py` so `cf_generate.py` cannot overwrite it — not even under
`--force`.

Aspect and `focus`
------------------
Like the rest of the pipeline this does NOT upscale (`crop_resize` only ever
shrinks), so a 1376x768 source yields a 1365x768 hero rather than the nominal
1600 — the same reason the generated heroes are 1593x896.

`focus` biases the crop: 0.0 keeps the left/top edge, 1.0 the right/bottom. It
only ever moves the crop along the axis that is actually being trimmed, so it is
a no-op on the untrimmed axis. Values here were chosen by rendering candidate
crops and inspecting them, not guessed.

`box` optionally pre-crops to a region of the source, in fractions
(left, top, right, bottom), BEFORE the aspect crop. `crop_resize` alone cannot
tighten a portrait whose subject sits small in a lot of empty frame, because it
always keeps the full width when it is trimming height.
"""

import os
import shutil
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import image_lib as il  # noqa: E402

ROOT = os.path.dirname(HERE)
PUBLIC = os.path.join(ROOT, "public")
BACKUP = os.path.join(il.WORK, "backup-signature")

DL = "/Users/macbookair/Downloads"
CLIP = "/Users/macbookair/.workbuddy-ai/clipboard-images"

# ── Signature Entries ───────────────────────────────────────────────────────
# Wide hero (16:9) + portrait card (3:4) per entry. The four wedding frames carry
# the people and the moment; where a purpose-composed portrait was supplied it
# replaces the derived card crop.
SIG = [
    dict(
        key="shiva",
        hero=dict(src=f"{DL}/hC4GF3CNWcdBTFUI.jpg", focus=0.5),
        card=dict(src=f"{DL}/img/shiva-entry-hero.png", focus=0.5),
    ),
    dict(
        key="royal",
        hero=dict(src=f"{DL}/5-MqyWl4yapvwGn6.jpg", focus=0.5),
        card=dict(src=f"{DL}/img/royal-entry-hero.png", focus=0.5),
    ),
    dict(
        key="floral",
        hero=dict(src=f"{CLIP}/clipboard-2026-09-15T04-48-09-257Z-7858d574.jpg", focus=0.5),
        # No purpose-composed portrait supplied — derive the card from the hero.
        card=dict(src=f"{CLIP}/clipboard-2026-09-15T04-48-09-257Z-7858d574.jpg", focus=0.58),
    ),
    dict(
        key="celestial",
        hero=dict(src=f"{DL}/_8DOW2uERpDv93Na.jpg", focus=0.5),
        card=dict(src=f"{DL}/_8DOW2uERpDv93Na.jpg", focus=0.70),
    ),
]
SIG_SLUG = {
    "shiva": "shiva-entry",
    "royal": "royal-entry",
    "floral": "floral-entry",
    "celestial": "celestial-entry",
}

# ── Founder ─────────────────────────────────────────────────────────────────
# The one subject the pipeline must never invent.
#   founder-hero.jpg     16:9 — the /about/founder/ page hero
#   founder-portrait.jpg 4:5  — the homepage founder figure (was a placeholder SVG)
FOUNDER = dict(
    src=f"{DL}/GS Gautam.jpg",
    hero=dict(rel="images/about/founder-hero.jpg", aspect=(16, 9), width=1600,
              quality=85, focus=0.40),
    portrait=dict(rel="images/founder-portrait.jpg", aspect=(4, 5), width=800,
                  quality=85, box=(0.16, 0.20, 0.90, 0.93), focus=0.5),
)

# ── Homepage hero + Vaidik dining ───────────────────────────────────────────
# `out` paths that already exist are replacements; `new` marks a slot introduced
# by this batch (it also needs a reference added in src/ — see the page edits).
OTHERS = [
    dict(
        key="hero-cinematic",
        src=f"{DL}/img/hero-cinematic.png",
        rel="images/hero-cinematic.jpg",
        aspect=(16, 9), width=1600, quality=85, focus=0.5,
        note="homepage hero",
    ),
    dict(
        key="vaidik-dining",
        src=f"{DL}/img/satvik-dining-copper.png",
        rel="images/vaidik/dining.jpg",
        aspect=(4, 5), width=900, quality=85, focus=0.5,
        note="Tamra Patra copper — lead dining visual",
    ),
    dict(
        key="vaidik-dining-banana-leaf",
        src=f"{DL}/img/satvik-dining-banana-leaf.png",
        rel="images/vaidik/dining-banana-leaf.jpg",
        aspect=(4, 5), width=900, quality=85, focus=0.5,
        note="Banana Leaf — second dining visual",
    ),
    dict(
        key="vaidik-pure",
        src=f"{DL}/img/pure-bg.png",
        rel="images/vaidik/pure-hero.jpg",
        aspect=(16, 9), width=1600, quality=85, focus=0.5,
        note="PURE section atmosphere",
    ),
]

CARD_ASPECT = (3, 4)
CARD_WIDTH = 900
CARD_QUALITY = 83


def crop_box(im, box):
    """Crop to a box given in source fractions (left, top, right, bottom)."""
    w, h = im.size
    l, t, r, b = box
    return im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def place(src, rel, aspect, width, quality, focus=0.5, box=None):
    """Crop `src` to `aspect`, encode, and write to `rel` under public/."""
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    im = il.Image.open(src).convert("RGB")
    if box:
        im = crop_box(im, box)
    out = il.crop_resize(im, aspect[0] / aspect[1], width, focus=focus)
    dest = os.path.join(PUBLIC, rel)
    size = il.save_jpeg(out, dest, quality=quality)
    return rel, out.size, size


def all_outputs():
    rels = []
    for s in SIG:
        slug = SIG_SLUG[s["key"]]
        rels += [f"images/signature/{slug}-hero.jpg", f"images/signature/{slug}-card.jpg"]
    rels += [FOUNDER["hero"]["rel"], FOUNDER["portrait"]["rel"]]
    rels += [o["rel"] for o in OTHERS]
    rels += ["images/og.jpg"]
    return rels


def backup(rel_paths):
    """Never overwrite an asset without a copy — these are not all in git."""
    os.makedirs(BACKUP, exist_ok=True)
    saved = []
    for rel in rel_paths:
        src = os.path.join(PUBLIC, rel)
        if os.path.exists(src):
            dst = os.path.join(BACKUP, rel.replace("/", "__"))
            shutil.copy2(src, dst)
            saved.append(dst)
    return saved


def main():
    saved = backup(all_outputs())
    print(f"backed up {len(saved)} existing assets → {BACKUP}\n")

    written = []

    # Signature heroes and cards
    for s in SIG:
        slug = SIG_SLUG[s["key"]]
        written.append(
            place(s["hero"]["src"], f"images/signature/{slug}-hero.jpg",
                  (16, 9), 1600, 85, s["hero"]["focus"])
        )
        written.append(
            place(s["card"]["src"], f"images/signature/{slug}-card.jpg",
                  CARD_ASPECT, CARD_WIDTH, CARD_QUALITY, s["card"]["focus"])
        )

    # Founder
    h = FOUNDER["hero"]
    written.append(place(FOUNDER["src"], h["rel"], h["aspect"], h["width"],
                         h["quality"], h["focus"]))
    p = FOUNDER["portrait"]
    written.append(place(FOUNDER["src"], p["rel"], p["aspect"], p["width"],
                         p["quality"], p["focus"], box=p.get("box")))

    # Homepage hero + Vaidik dining/pure
    for o in OTHERS:
        written.append(place(o["src"], o["rel"], o["aspect"], o["width"],
                             o["quality"], o["focus"]))

    # Social share card — derived from the homepage hero, so it must follow it.
    hero_src = next(o["src"] for o in OTHERS if o["key"] == "hero-cinematic")
    im = il.Image.open(hero_src).convert("RGB")
    og = il.crop_resize(im, 1200 / 630, 1200, focus=0.5)
    og_size = il.save_jpeg(og, os.path.join(PUBLIC, "images/og.jpg"), quality=87)
    written.append(("images/og.jpg", og.size, og_size))

    total = sum(s for _, _, s in written)
    print(f"wrote {len(written)} assets · {total/1024/1024:.1f} MB total\n")
    for rel, dims, size in written:
        print(f"  {rel:<48} {dims[0]:>4}x{dims[1]:<4} {size//1024:>4} KB")

    update_credits(written)
    return 0


def update_credits(written):
    """Rewrite the affected rows and disclose the change of provenance.

    The rest of the site is AI-generated and the file must keep saying so. These
    are not, and claiming a generator we did not run would be a false disclosure
    — so they get their own row wording and a note.
    """
    dest = os.path.join(PUBLIC, "images/CREDITS.md")
    if not os.path.exists(dest):
        print("\n  (no CREDITS.md to update)")
        return

    with open(dest, encoding="utf-8") as fh:
        raw = fh.read()

    # Idempotent: drop a note written by an earlier run before writing a fresh one.
    marker_note = "\n## Client-supplied photography"
    if marker_note in raw:
        raw = raw.split(marker_note)[0].rstrip("\n") + "\n"

    lines = raw.split("\n")
    supplied = {rel: dims for rel, dims, _ in written}
    out, matched, last_row = [], set(), -1
    for line in lines:
        row = next((rel for rel in supplied if line.startswith(f"| `{rel}` |")), None)
        if row:
            dims = supplied[row]
            out.append(f"| `{row}` | {dims[0]}×{dims[1]} | client-supplied photograph |")
            matched.add(row)
            last_row = len(out) - 1
        else:
            out.append(line)

    # Slots that replaced a placeholder SVG or are newly introduced have no row.
    new = sorted(set(supplied) - matched)
    if new and last_row >= 0:
        rows = [
            f"| `{rel}` | {supplied[rel][0]}×{supplied[rel][1]} | client-supplied photograph |"
            for rel in new
        ]
        out[last_row + 1 : last_row + 1] = rows

    text = "\n".join(out)
    note = (
        "\n## Client-supplied photography\n\n"
        "The assets listed below are supplied photographs, not AI generations, and are "
        "marked as such in the table above. They cover the four Signature Entries "
        "(Shiva / Royal / Floral / Celestial), the founder, the homepage hero and the "
        "Vaidik dining/pure imagery.\n\n"
        + "\n".join(f"- `{rel}`" for rel in sorted(supplied))
        + "\n\n"
        "They were cropped to the slot aspect, re-encoded as progressive 4:4:4 JPEGs, "
        "and written to the paths the pages reference (`scripts/place_supplied.py`). "
        "The images remain illustrative of the *kind* of work Third Eye Events does; "
        "if any depicts a real client or event, confirm consent to publish before "
        "launch.\n\n"
        "These slots are **not** regenerable: each is flagged `supplied` in "
        "`scripts/image_manifest.py` and skipped by `cf_generate.py`, so a generation "
        "run cannot overwrite a real photograph or a real person's likeness.\n"
        f"\nPlaced {date.today().isoformat()}.\n"
    )
    marker = "\n> Replacing any asset with commissioned photography:"
    text = text.replace(marker, note + marker, 1) if marker in text else text + note

    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\n  credits → {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
