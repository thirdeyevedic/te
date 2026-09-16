#!/usr/bin/env python3
"""
apply_images — turn the selected candidates into finished, web-ready assets.

Run:  python scripts/apply_images.py

Reads /tmp/imgwork/picks.json (written by source_images.py) plus an optional
/tmp/imgwork/overrides.json of the form {"slot-id": 3} to override a pick.
Crops each selection to the slot's aspect ratio, resizes to its target width and
writes an optimised progressive JPEG under public/. Also emits
public/images/CREDITS.md and a review montage of every finished asset.
"""

import json
import os
import sys

import image_lib as il
from image_manifest import CARD_ASPECT, CARD_DERIVATIONS, CARD_WIDTH, MANIFEST

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
PICKS = os.path.join(il.WORK, "picks.json")
OVERRIDES = os.path.join(il.WORK, "overrides.json")
# Slots whose subject sits low or high in frame need the crop biased.
FOCUS = {
    "hero-cinematic": 0.5,
    "vaidik-dining": 0.5,
    "about-dance": 0.4,
    "founder-portrait": 0.4,
}


def load(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return default


def load_picks():
    """Merge every picks file, so a sharded sourcing run needs no extra step."""
    merged = {}
    import glob

    for path in sorted(glob.glob(os.path.join(il.WORK, "picks*.json"))):
        try:
            merged.update(load(path, {}))
        except Exception as exc:  # noqa: BLE001
            print(f"  ! could not read {path}: {exc}")
    return merged


def main():
    picks = load_picks()
    overrides = load(OVERRIDES, {})
    if not picks:
        sys.exit("no picks files — run source_images.py first")

    by_slot = {s["slot"]: s for s in MANIFEST}
    written, credits, failures = [], [], []

    # A photograph must not appear twice on the site. Flickr's tag feed in
    # particular surfaces the same popular shot for related queries, and the
    # first pass put one model's portrait on both the weddings index and the
    # experiences page. The first slot to claim an image keeps it; later slots
    # fall through to their next-best candidate.
    claimed = {}

    def choose(entry, want_idx, slot_id):
        cands = entry.get("candidates") or []
        ordered = [c for c in cands if c["idx"] == want_idx] + [c for c in cands if c["idx"] != want_idx]
        for c in ordered:
            url = c.get("url")
            if url and url not in claimed:
                claimed[url] = slot_id
                return c
        return ordered[0] if ordered else None

    for slot_id, slot in by_slot.items():
        entry = picks.get(slot_id)
        if not entry or not entry.get("candidates"):
            failures.append(f"{slot_id}: no candidates")
            continue

        idx = overrides.get(slot_id, entry["pick"])
        chosen = choose(entry, idx, slot_id)
        if chosen is None:
            failures.append(f"{slot_id}: pick {idx} missing")
            continue

        try:
            with il.Image.open(chosen["file"]) as src:
                src.load()
                aspect = slot["aspect"][0] / slot["aspect"][1]
                focus = FOCUS.get(slot_id, 0.5)
                out = il.crop_resize(src, aspect, slot["width"], focus=focus)
                dest = os.path.join(PUBLIC, slot["out"])
                size = il.save_jpeg(out, dest, quality=82)
                if out.width < slot["width"]:
                    failures.append(
                        f"{slot_id}: {out.width}px wide, below target {slot['width']}px "
                        "(source too small)"
                    )
                written.append((slot_id, slot["out"], out.width, out.height, size))
                credits.append(
                    {
                        "out": slot["out"],
                        "title": chosen.get("title") or "—",
                        "creator": chosen.get("creator") or "—",
                        "license": chosen.get("license") or "—",
                        "landing": chosen.get("landing") or chosen.get("url") or "",
                        "source": chosen.get("provider"),
                    }
                )
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{slot_id}: {exc}")

    # Portrait card crops derived from the same source photograph as the hero.
    for slot_id, out_rel in CARD_DERIVATIONS:
        entry = picks.get(slot_id)
        if not entry or not entry.get("candidates"):
            failures.append(f"{slot_id} (card): no candidates")
            continue
        chosen = next(
            (c for c in entry["candidates"] if claimed.get(c.get("url")) == slot_id), None
        )
        if chosen is None:
            continue
        try:
            with il.Image.open(chosen["file"]) as src:
                src.load()
                aspect = CARD_ASPECT[0] / CARD_ASPECT[1]
                out = il.crop_resize(src, aspect, CARD_WIDTH, focus=0.45)
                dest = os.path.join(PUBLIC, out_rel)
                size = il.save_jpeg(out, dest, quality=80)
                written.append((slot_id + ":card", out_rel, out.width, out.height, size))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{slot_id} (card): {exc}")

    write_credits(credits)
    write_social_card()

    print(f"wrote {len(written)} assets")
    for slot_id, rel, w, h, size in written:
        print(f"  {w:>4}x{h:<4} {size // 1024:>4} KB  {rel}")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  -", f)

    build_montage(written)


def write_social_card():
    """Open Graph card, derived from the homepage hero so previews match the site."""
    src = os.path.join(PUBLIC, "images", "hero-cinematic.jpg")
    if not os.path.exists(src):
        print("skip og.jpg — homepage hero not written yet")
        return
    with il.Image.open(src) as im:
        im.load()
        card = il.crop_resize(im, 1200 / 630, 1200, focus=0.5)
        dest = os.path.join(PUBLIC, "images", "og.jpg")
        size = il.save_jpeg(card, dest, quality=84)
        print(f"wrote {dest} ({size // 1024} KB)")


def write_credits(credits):
    lines = [
        "# Image Credits — Third Eye Events",
        "",
        "All imagery on this site is sourced from openly licensed collections "
        "(Wikimedia Commons, Rawpixel, StockSnap, Flickr) under licences that "
        "permit commercial use and derivative works — CC0, public domain, "
        "CC BY or CC BY-SA. Images have been cropped and resized for layout.",
        "",
        "| Asset | Title | Creator | Licence | Source |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in sorted(credits, key=lambda x: x["out"]):
        landing = c["landing"] or ""
        src = f"[link]({landing})" if landing else (c["source"] or "—")
        title = str(c["title"]).replace("|", "/")[:70]
        creator = str(c["creator"]).replace("|", "/")[:50]
        lines.append(f"| `{c['out']}` | {title} | {creator} | {c['license']} | {src} |")
    lines += [
        "",
        "> If a specific asset should be replaced with commissioned photography, "
        "swap the file in place — every page references these paths directly.",
        "",
    ]
    path = os.path.join(PUBLIC, "images", "CREDITS.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {path}")


def build_montage(written, cols=6, cell=300):
    """One contact sheet of every finished asset, for a final visual pass."""
    items = [(os.path.join(PUBLIC, rel), slot_id) for slot_id, rel, *_ in written]
    paths = [p for p, _ in items]
    labels = [s for _, s in items]
    out = os.path.join(il.SHEETS, "FINAL-all-assets.jpg")
    il.contact_sheet(paths, labels, out, cols=cols, cell=cell, title="FINAL ASSETS")
    print(f"wrote {out}")
    # Split into readable chunks too.
    chunk = cols * 3
    for i in range(0, len(paths), chunk):
        part = paths[i : i + chunk]
        part_labels = labels[i : i + chunk]
        il.contact_sheet(
            part,
            part_labels,
            os.path.join(il.SHEETS, f"FINAL-part{i // chunk + 1}.jpg"),
            cols=cols,
            cell=340,
            title=f"FINAL ASSETS — part {i // chunk + 1}",
        )


if __name__ == "__main__":
    main()
