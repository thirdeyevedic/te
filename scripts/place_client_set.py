#!/usr/bin/env python3
"""
place_client_set — place the client's supplied 32-image set into the site.

Run:  python scripts/place_client_set.py

The set was generated on another platform against a written prompt list. That
list names a target path per image, but every path ends in `.jpg.svg` — the
naming of an earlier repo state (git: "Place 33 SVGs as hero images…"). The
current site references plain `.jpg`, so this script maps each prompt onto the
path the pages actually use today.

MAPPING
-------
The supplied files carry opaque ids, so the prompt list's own ids do not
identify them. The mapping below was established by CONTENT — every image was
inspected and matched to the subject its prompt describes (a shiva groom with a
trishul, a palace baraat, a floral arch, a misty descent, and so on). All 32
matched, which is what makes the order trustworthy.

Prompt 07 (`about/founder-portrait-gautam-gs`) has no image in the set. That is
correct and deliberate: an AI-generated portrait of a real, named person would
fabricate a likeness. The founder slot keeps the real photograph supplied
separately (see place_supplied.py). `archival-mumbai` remains unregistered for
the same reason.

NOT COVERED BY THE SET
----------------------
The list covers 33 slots. It does NOT cover: the 11 portrait cards, the 5
weddings-section heroes, the 6 about-section images, contact, the two index
heroes (destinations / event-IP / production), or `vaidik/dining`. Those keep
their existing imagery, so a replaced hero may sit above a card from the
previous set. Regenerate the cards (or supply them) to bring them back in line.

ASPECT
------
Sources are 1376x768 (1.79) against a 16:9 (1.78) slot, so heroes lose under 1%
of the frame. Like the rest of the pipeline this does NOT upscale, so a hero
comes out 1365x768 rather than the nominal 1600 — the same reason the generated
heroes are 1593x896.
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
DL = "/Users/macbookair/Downloads"
BACKUP = os.path.join(il.WORK, "backup-client-set")

HERO = ((16, 9), 1600, 85)

# (prompt no., source filename, output path under public/)
BATCH = [
    (1,  "hC4GF3CNWcdBTFUI.jpg",        "images/signature/shiva-entry-hero.jpg"),
    (2,  "5-MqyWl4yapvwGn6.jpg",        "images/signature/royal-entry-hero.jpg"),
    (3,  "07Y3FbaZNoy4G7GG.jpg",        "images/signature/floral-entry-hero.jpg"),
    (4,  "_8DOW2uERpDv93Na.jpg",        "images/signature/celestial-entry-hero.jpg"),
    (5,  "_2Dw9aIFMk_ivfHH.jpg",        "images/hero-cinematic.jpg"),
    (6,  "ib2-Kb8RsUrWHGAh.jpg",        "images/og.jpg"),
    # 7 = founder portrait — no image supplied, real photograph retained.
    (8,  "58_t6D4-QxDedsRE.jpg",        "images/destinations/bali/hero.jpg"),
    (9,  "7Dub8J9f7IeOe34q.jpg",        "images/destinations/cruises/hero.jpg"),
    (10, "6og35gK24K-6j3O1.jpg",        "images/destinations/italy/hero.jpg"),
    (11, "0CHenZeUHQfEnD7g.jpg",        "images/destinations/kyoto/hero.jpg"),
    (12, "f9AqXcgQcodIODom.jpg",        "images/destinations/maldives/hero.jpg"),
    (13, "4psvjK9n9D8u046A.jpg",        "images/destinations/rajasthan/hero.jpg"),
    (14, "rGB0UmFlqIIUBwmI.jpg",        "images/destinations/switzerland/hero.jpg"),
    (15, "vyg0Xr76Jm0yMgMw.jpg",        "images/ip/automotive-hero.jpg"),
    (16, "DiujBcMtAVTe4F06.jpg",        "images/ip/awards-hero.jpg"),
    (17, "1JdDhdjepmI5KvZO.jpg",        "images/ip/best-products-hero.jpg"),
    (18, "1k_AdsctDEDs2h0l.jpg",        "images/ip/concerts-hero.jpg"),
    (19, "ZB_rQu-XJAsGz0pa.jpg",        "images/ip/devotional-hero.jpg"),
    (20, "vHuPaVdXnqCpCTzj.jpg",        "images/ip/exhibitions-hero.jpg"),
    (21, "U8QHv9ZAn6EPfqz0.jpg",        "images/ip/fashion-hero.jpg"),
    (22, "ZHQ0xve-Ut9kt8Zq.jpg",        "images/ip/political-hero.jpg"),
    (23, "JQLCtW3wiRrVsvny.jpg",        "images/ip/sports-hero.jpg"),
    (24, "JWz-I0434-xrk6DX.jpg",        "images/production/ad-shoots.jpg"),
    (25, "tSqUp30srpJVw0MS.jpg",        "images/production/branded-content.jpg"),
    (26, "n9G4G62ElfUcyTab.jpg",        "images/production/documentaries.jpg"),
    (27, "jLtJXXpGOQCbwv-f.jpg",        "images/production/feature-films.jpg"),
    (28, "AK_ssKRb5tkgkKcb.jpg",        "images/production/short-films.jpg"),
    (29, "rwgZz8dOY_heTGJO.jpg",        "images/production/youtube-digital.jpg"),
    (30, "Qq4lWxDp5dLfvmxL.jpg",        "images/vaidik/pure-hero.jpg"),
    (31, "SoFH04fIVxgH7Aml.jpg",        "images/vaidik/satvik-dining-banana-leaf.jpg"),
    (32, "wb6SspXe-8-BzzJK.jpg",        "images/vaidik/satvik-dining-copper.jpg"),
    (33, "QqJ8UMZxaMPjDlyz.jpg",        "images/vaidik/satvik-dining-seasonal.jpg"),
]

# The social card is a fixed 1.905:1, not 16:9.
ASPECT_OVERRIDE = {"images/og.jpg": ((1200, 630), 1200, 87)}

# The dining trio is landscape on the page, so it keeps the source aspect.
DINING = {
    "images/vaidik/satvik-dining-banana-leaf.jpg",
    "images/vaidik/satvik-dining-copper.jpg",
    "images/vaidik/satvik-dining-seasonal.jpg",
}


def main():
    os.makedirs(BACKUP, exist_ok=True)
    saved = 0
    for _, _, rel in BATCH:
        src = os.path.join(PUBLIC, rel)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(BACKUP, rel.replace("/", "__")))
            saved += 1
    print(f"backed up {saved} existing assets → {BACKUP}\n")

    written, missing = [], []
    for num, name, rel in BATCH:
        src = os.path.join(DL, name)
        if not os.path.exists(src):
            missing.append((num, name, rel))
            continue

        if rel in ASPECT_OVERRIDE:
            aspect, width, quality = ASPECT_OVERRIDE[rel]
        elif rel in DINING:
            aspect, width, quality = (16, 9), 1600, 85
        else:
            aspect, width, quality = HERO

        im = il.Image.open(src).convert("RGB")
        out = il.crop_resize(im, aspect[0] / aspect[1], width, focus=0.5)
        size = il.save_jpeg(out, os.path.join(PUBLIC, rel), quality=quality)
        written.append((num, rel, out.size, size))

    total = sum(s for _, _, _, s in written)
    print(f"wrote {len(written)} assets · {total/1024/1024:.1f} MB total\n")
    for num, rel, dims, size in written:
        print(f"  {num:>2}. {rel:<48} {dims[0]:>4}x{dims[1]:<4} {size//1024:>4} KB")

    if missing:
        print(f"\n  MISSING {len(missing)} source file(s):")
        for num, name, rel in missing:
            print(f"    {num:>2}. {name}  →  {rel}")

    update_credits(written)
    return 1 if missing else 0


def update_credits(written):
    dest = os.path.join(PUBLIC, "images/CREDITS.md")
    if not os.path.exists(dest):
        print("\n  (no CREDITS.md to update)")
        return

    with open(dest, encoding="utf-8") as fh:
        raw = fh.read()

    marker_note = "\n## Client-supplied photography"
    if marker_note in raw:
        raw = raw.split(marker_note)[0].rstrip("\n") + "\n"

    lines = raw.split("\n")
    supplied = {rel: dims for _, rel, dims, _ in written}
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
        "Every asset below is a supplied photograph, not an AI generation, and is "
        "marked as such in the table above. The set was produced on an external "
        "platform against a written prompt list; `scripts/place_client_set.py` holds "
        "the image-to-slot mapping and `scripts/place_supplied.py` covers the founder, "
        "the Signature Entry cards and the earlier supplied frames.\n\n"
        + "\n".join(f"- `{rel}`" for rel in sorted(supplied))
        + "\n\n"
        "They were cropped to the slot aspect, re-encoded as progressive 4:4:4 JPEGs, "
        "and written to the paths the pages reference. The images remain illustrative "
        "of the *kind* of work Third Eye Events does; if any depicts a real client or "
        "event, confirm consent to publish before launch.\n\n"
        "The founder slot is deliberately absent from this set — an AI-generated "
        "portrait of a real, named person would fabricate a likeness, so it keeps the "
        "supplied photograph instead.\n"
        f"\nPlaced {date.today().isoformat()}.\n"
    )
    marker = "\n> Replacing any asset with commissioned photography:"
    text = text.replace(marker, note + marker, 1) if marker in text else text + note

    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"\n  credits → {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
