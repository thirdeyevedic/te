#!/usr/bin/env python3
"""
apply_generated — place the Workers AI images into public/ as web-ready assets.

Run:  python scripts/apply_generated.py

Companion to cf_generate.py. Reads the raw generations from /tmp/imgwork/gen/
and writes every slot in image_manifest.py to its final path under public/:
crops to the slot's aspect ratio, resizes to its target width, encodes a
progressive JPEG, derives the social share card from the homepage hero, and
rewrites CREDITS.md with the generation provenance.

Also emits a review montage at /tmp/imgwork/gen-sheets/ so the whole set can be
eyeballed at once before it ships.
"""

import os
import re
import sys
from datetime import date

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import image_lib as il  # noqa: E402
from image_manifest import (  # noqa: E402
    CARD_ASPECT,
    CARD_DERIVATIONS,
    CARD_WIDTH,
    MANIFEST,
    SUPPLIED_CARDS,
)

ROOT = os.path.dirname(HERE)
PUBLIC = os.path.join(ROOT, "public")
GEN = os.path.join(il.WORK, "gen")
SHEETS = os.path.join(il.WORK, "gen-sheets")
os.makedirs(SHEETS, exist_ok=True)

MODEL = "FLUX.2 klein 4B"
PROVIDER = "Cloudflare Workers AI"

# Subject sits low in a few frames; bias the crop rather than centring.
FOCUS = {
    "hero-cinematic": 0.5,
    "vaidik-dining": 0.5,
    "about-dance": 0.42,
    "contact": 0.5,
}


def source(slot: str) -> Image.Image | None:
    """Raw generation for `slot` from the scratch dir, or None if absent.

    NOTE: `GEN` is a *persistent* scratch dir (/tmp/imgwork/gen), not a
    per-run temp dir. It routinely still holds files from an earlier
    generation pass. Callers MUST check the slot's `supplied` flag before
    using this — see the guards in main().
    """
    path = os.path.join(GEN, f"{slot}.jpg")
    if not os.path.exists(path):
        return None
    return Image.open(path).convert("RGB")


def public_source(rel: str) -> Image.Image | None:
    """The already-placed asset at `rel` under public/, or None if absent."""
    path = os.path.join(PUBLIC, rel)
    if not os.path.exists(path):
        return None
    return Image.open(path).convert("RGB")


def main():
    written, missing = [], []
    credit_overrides = {}
    supplied_slots = {e["slot"] for e in MANIFEST if e.get("supplied")}

    # ── Hero / section slots ────────────────────────────────────────────────
    for entry in MANIFEST:
        slot, rel = entry["slot"], entry["out"]
        # Slots backed by real client photography are NEVER written. This guard
        # is load-bearing: GEN persists across runs, so a stale generated file
        # for a supplied slot will still be sitting there, and without this
        # check it silently overwrites the client's photograph — including the
        # founder's real likeness — and then re-credits it as AI-generated.
        # (cf_generate.py has the matching guard; the two must stay in step.)
        if slot in supplied_slots:
            continue
        im = source(slot)
        if im is None:
            missing.append(slot)
            continue
        aspect = entry["aspect"][0] / entry["aspect"][1]
        out = il.crop_resize(im, aspect, entry["width"], focus=FOCUS.get(slot, 0.5))
        dest = os.path.join(PUBLIC, rel)
        # 85 for full-bleed heroes: they are viewed at large size, so ringing and
        # gradient banding are visible at lower settings. Paired with the 4:4:4
        # chroma in image_lib.save_jpeg, which is what keeps the saturated
        # palette from going muddy.
        size = il.save_jpeg(out, dest, quality=85)
        written.append((rel, out.size, size))

    # ── Portrait cards ──────────────────────────────────────────────────────
    # Composed for the card, not cropped from the hero — see cf_generate.py.
    # CARD_DERIVATIONS keys a card by its HERO's slot, so "the hero is supplied"
    # does not imply "the card is supplied". Only SUPPLIED_CARDS — the four
    # Signature cards, which are backed by real photography — are skipped here.
    # Keying this guard on `supplied_slots` instead would freeze all 11 cards.
    for slot, rel in CARD_DERIVATIONS:
        if slot in SUPPLIED_CARDS:
            continue
        im = source(f"card-{slot}")
        if im is None:
            missing.append(f"card-{slot}")
            continue
        aspect = CARD_ASPECT[0] / CARD_ASPECT[1]
        out = il.crop_resize(im, aspect, CARD_WIDTH, focus=0.5)
        dest = os.path.join(PUBLIC, rel)
        size = il.save_jpeg(out, dest, quality=83)
        written.append((rel, out.size, size))

    # ── Social share card, derived from the homepage hero ───────────────────
    # `hero-cinematic` is client-supplied, so derive the share card from the
    # real photograph already in public/ — NOT from GEN, which may hold a stale
    # generation for that slot. Its provenance stays client-supplied.
    hero_entry = next((e for e in MANIFEST if e["slot"] == "hero-cinematic"), None)
    if hero_entry and hero_entry.get("supplied"):
        hero = public_source(hero_entry["out"])
        credit_overrides["images/og.jpg"] = "client-supplied photograph"
    else:
        hero = source("hero-cinematic")
    if hero is not None:
        card = il.crop_resize(hero, 1200 / 630, 1200, focus=0.5)
        dest = os.path.join(PUBLIC, "images/og.jpg")
        size = il.save_jpeg(card, dest, quality=87)
        written.append(("images/og.jpg", card.size, size))

    # ── Report ──────────────────────────────────────────────────────────────
    total = sum(s for _, _, s in written)
    print(f"wrote {len(written)} assets · {total/1024/1024:.1f} MB total\n")
    for rel, dims, size in sorted(written):
        print(f"  {rel:<46} {dims[0]:>4}x{dims[1]:<4} {size//1024:>4} KB")
    if missing:
        print(f"\n  MISSING SOURCE for {len(missing)} slots (run cf_generate.py):")
        for slot in missing:
            print(f"    - {slot}")

    write_credits(written, credit_overrides)
    build_montage(written)
    return 1 if missing else 0


CREDITS_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")


def read_existing_rows(dest):
    """rel -> (dims, provenance) for every row already in CREDITS.md."""
    rows = {}
    if not os.path.exists(dest):
        return rows
    with open(dest, encoding="utf-8") as fh:
        for line in fh:
            m = CREDITS_ROW.match(line.strip())
            if m:
                rows[m.group(1)] = (m.group(2), m.group(3))
    return rows


def write_credits(written, overrides=None):
    """Provenance file. AI generation must be disclosed, not implied as photography.

    Merges, never truncates. A large part of this site is real client-supplied
    photography, including a real person's likeness in the founder slot.
    Rebuilding this file from only the assets one generation run happened to
    write would silently delete that disclosure and re-assert that everything on
    the site is AI-generated — a false provenance claim. So existing rows are
    preserved and only the rows this run actually produced are refreshed.

    `overrides` maps a written rel-path to a provenance string, for assets that
    this run rewrote from real photography rather than generated (e.g. the share
    card, which is cropped from the client-supplied homepage hero).
    """
    overrides = overrides or {}
    dest = os.path.join(PUBLIC, "images/CREDITS.md")

    rows = {}
    for rel, (dims, prov) in read_existing_rows(dest).items():
        if os.path.exists(os.path.join(PUBLIC, rel)):
            rows[rel] = (dims, prov)
    for rel, dims, _ in written:
        prov = overrides.get(rel, "`scripts/cf_generate.py`")
        rows[rel] = (f"{dims[0]}×{dims[1]}", prov)

    supplied = sorted(rel for rel, (_, prov) in rows.items() if "client-supplied" in prov)
    generated = sorted(set(rows) - set(supplied))

    lines = [
        "# Image Credits — Third Eye Events",
        "",
        "This site carries two kinds of imagery, and the table below records which is "
        "which. **Generated** assets were produced with "
        f"{MODEL} via {PROVIDER} from an art-directed prompt written against the page "
        "copy they sit beside (see `scripts/cf_generate.py`). **Client-supplied** assets "
        "are real photographs and are marked as such in the table.",
        "",
        "For the generated assets: no photograph of any real person, client, wedding or "
        "venue is depicted. Prompts deliberately avoid recognisable faces — where people "
        "appear they are silhouetted, seen from behind, or out of focus. They are "
        "illustrative of the *kind* of work Third Eye Events does and should not be "
        "presented as a record of past events.",
        "",
        f"Generated {date.today().isoformat()}.",
        "",
        "| Asset | Dimensions | Prompt source |",
        "| --- | --- | --- |",
    ]
    for rel in sorted(rows):
        dims, prov = rows[rel]
        lines.append(f"| `{rel}` | {dims} | {prov} |")
    lines += [
        "",
        "> Replacing a generated asset with commissioned photography: drop the file in "
        "place at the same path and aspect ratio — every page references these paths "
        "directly — then mark the row `client-supplied photograph` so a later generation "
        "run does not re-claim it.",
        "",
    ]

    if supplied:
        lines += [
            "## Client-supplied photography",
            "",
            f"{len(supplied)} assets on this site are supplied photographs, not AI "
            "generations, and are marked as such in the table above. They were cropped "
            "to the slot aspect, re-encoded as progressive 4:4:4 JPEGs, and written to "
            "the paths the pages reference — `scripts/place_client_set.py` and "
            "`scripts/place_supplied.py` hold the image-to-slot mapping.",
            "",
            "The images remain illustrative of the *kind* of work Third Eye Events does; "
            "if any depicts a real client or event, confirm consent to publish before "
            "launch. The founder slot keeps a real photograph deliberately: an "
            "AI-generated portrait of a real, named person would fabricate a likeness.",
            "",
        ]
        lines += [f"- `{rel}`" for rel in supplied]
        lines += [""]

    with open(dest, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(
        f"\n  credits → {os.path.relpath(dest, ROOT)} "
        f"({len(generated)} generated, {len(supplied)} client-supplied)"
    )


def build_montage(written, cols=6, cell=260):
    """One contact sheet per directory group, for visual review."""
    groups = {}
    for rel, _, _ in written:
        key = os.path.dirname(rel).replace("images/", "") or "root"
        groups.setdefault(key, []).append(rel)

    for key, rels in groups.items():
        rels = sorted(rels)
        rows = (len(rels) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 18)), (18, 18, 18))
        draw = ImageDraw.Draw(sheet)
        for i, rel in enumerate(rels):
            try:
                im = Image.open(os.path.join(PUBLIC, rel)).convert("RGB")
            except Exception:
                continue
            im.thumbnail((cell - 8, cell - 8), Image.LANCZOS)
            x = (i % cols) * cell + (cell - im.width) // 2
            y = (i // cols) * (cell + 18) + 4
            sheet.paste(im, (x, y))
            draw.text(((i % cols) * cell + 4, y + cell - 4), rel.split("/")[-1][:34], fill=(200, 200, 200))
        out = os.path.join(SHEETS, f"{key.replace('/', '-')}.jpg")
        sheet.save(out, "JPEG", quality=80)
        print(f"  sheet → {os.path.relpath(out, il.WORK)}")


if __name__ == "__main__":
    sys.exit(main())
