#!/usr/bin/env python3
"""
place_firefly.py — post-process Adobe Firefly downloads into the site.

Reads scripts/kling_prompts.py (slot -> prompt/out/aspect/width), finds each
slot's downloaded file in /tmp/firefly/<slot>.*, then center-crops to the exact
manifest aspect ratio and resizes to the manifest width, writing a progressive
JPEG into public/<out>.

Also regenerates public/images/og.jpg (1200x630 from hero-cinematic) and
rewrites public/images/CREDITS.md to mark every asset as Adobe Firefly
(AI-generated, commercially-safe licence).

Run from the repo root:  /usr/bin/python3 scripts/place_firefly.py
"""
import os, sys, glob, datetime, io

REPO = "/Users/macbookair/te"
PUB = os.path.join(REPO, "public")
SRC_DIR = "/tmp/firefly"
sys.path.insert(0, os.path.join(REPO, "scripts"))
from kling_prompts import ALL  # noqa: E402

from PIL import Image  # noqa: E402

TODAY = datetime.date.today().isoformat()


def find_src(slot):
    hits = sorted(glob.glob(os.path.join(SRC_DIR, slot + ".*")))
    # prefer common raster formats
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        for h in hits:
            if h.lower().endswith(ext):
                return h
    return hits[0] if hits else None


def process(src, out_rel, aspect, width):
    img = Image.open(src).convert("RGB")
    tw, th = aspect
    target = tw / th
    w, h = img.size
    cur = w / h
    if cur > target:
        # too wide -> crop width
        nw = int(h * target)
        nx = (w - nw) // 2
        img = img.crop((nx, 0, nx + nw, h))
    elif cur < target:
        # too tall -> crop height
        nh = int(w / target)
        ny = (h - nh) // 2
        img = img.crop((0, ny, w, ny + nh))
    out_h = int(round(width / target))
    img = img.resize((width, out_h), Image.LANCZOS)
    out_path = os.path.join(PUB, out_rel)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "JPEG", quality=88, progressive=True, optimize=True)
    return out_path, img.size


def main():
    done, skipped = [], []
    for s in ALL:
        slot = s["slot"]
        src = find_src(slot)
        if not src:
            print(f"SKIP  {slot:24s} (no download in {SRC_DIR})")
            skipped.append(slot)
            continue
        out_path, size = process(src, s["out"], s["aspect"], s["width"])
        print(f"OK    {slot:24s} {size[0]}x{size[1]}  -> {s['out']}")
        done.append(slot)

    # og.jpg from hero-cinematic
    hero_src = find_src("hero-cinematic")
    if hero_src:
        img = Image.open(hero_src).convert("RGB")
        tw, th = 1200, 630
        target = tw / th
        w, h = img.size
        if w / h > target:
            nw = int(h * target); nx = (w - nw) // 2
            img = img.crop((nx, 0, nx + nw, h))
        else:
            nh = int(w / target); ny = (h - nh) // 2
            img = img.crop((0, ny, w, ny + nh))
        img = img.resize((tw, th), Image.LANCZOS)
        og = os.path.join(PUB, "images", "og.jpg")
        img.save(og, "JPEG", quality=88, progressive=True, optimize=True)
        print(f"OK    og.jpg 1200x630")

    # CREDITS.md
    lines = ["# Image Credits — Third Eye Events", "",
             f"All imagery below was generated with **Adobe Firefly** "
             f"(AI-generated, commercially-safe licence) on {TODAY}.",
             "No third-party photography or stock licences are used.", ""]
    for s in ALL:
        if s["slot"] in done:
            lines.append(f"- `{s['out']}` — Adobe Firefly (text-to-image), "
                         f"{s['aspect'][0]}:{s['aspect'][1]}, generated {TODAY}.")
    if skipped:
        lines += ["", "## Not yet generated (pending)", ""]
        for slot in skipped:
            lines.append(f"- `{slot}` — pending Firefly generation.")
    credits = os.path.join(PUB, "images", "CREDITS.md")
    with open(credits, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nWrote {credits}")
    print(f"Placed {len(done)} images; {len(skipped)} pending.")

    # montage of done assets for quick local review (optional)
    try:
        from PIL import ImageDraw
        thumbs = []
        for s in ALL:
            if s["slot"] in done:
                p = os.path.join(PUB, s["out"])
                try:
                    t = Image.open(p).convert("RGB").resize((240, 160))
                    thumbs.append(t)
                except Exception:
                    pass
        if thumbs:
            cols = 8
            rows = (len(thumbs) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * 240, rows * 160), (20, 20, 20))
            for i, t in enumerate(thumbs):
                r, c = divmod(i, cols)
                sheet.paste(t, (c * 240, r * 160))
            sheet.save("/tmp/firefly/SHEET-done.jpg", "JPEG", quality=80)
            print(f"Wrote /tmp/firefly/SHEET-done.jpg ({len(thumbs)} thumbs)")
    except Exception as e:
        print(f"(montage skipped: {e})")


if __name__ == "__main__":
    main()
