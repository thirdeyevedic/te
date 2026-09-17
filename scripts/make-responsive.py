#!/usr/bin/env python3
"""
make-responsive.py — generate responsive width-variants of every site image.

The site serves hero/card imagery from /public as plain <img src="/images/...">
strings (see src/components/ExperienceImage.astro). Astro's astro:assets
optimisation only applies to imported metadata, not /public paths, so phones
were downloading the full 1600px hero. This script closes that gap at the asset
layer: for each source JPEG it emits downscaled siblings

    <stem>@480.jpg  <stem>@768.jpg  <stem>@1200.jpg

and writes src/data/srcset-manifest.json, which ExperienceImage consumes to
build a `srcset` (the original stays the largest entry). Variants keep the
site's 4:4:4 chroma (subsampling=0) so saturated colour survives downscaling.

Run:  python3 scripts/make-responsive.py
Outputs land next to the originals (public/images/**) + the manifest in src/data.
Resumable: a variant is skipped when it already exists and is newer than its
source, so re-running after a regeneration only tops up what changed.

NOTE: this needs Pillow. In this project the managed venv has it:
  /Users/macbookair/.workbuddy-ai/binaries/python/envs/default/bin/python scripts/make-responsive.py
On a clean Cloudflare build image Pillow may be absent — that is fine, the
committed variants + manifest are used as-is (wire `prebuild` with `|| true`).
"""
import json
import os
import sys
import time

try:
    from PIL import Image
except ImportError:
    # Pillow not installed (e.g. a clean Cloudflare build image). The committed
    # variants + manifest are used as-is, so exit cleanly rather than failing
    # the build. Run the script locally (managed venv has Pillow) to regenerate.
    print("make-responsive: Pillow not available — skipping (using committed variants)")
    sys.exit(0)

# Reuse the site's vibrancy-tuned JPEG writer (4:4:4, progressive).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_lib import save_jpeg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
MANIFEST = os.path.join(ROOT, "src", "data", "srcset-manifest.json")

# Widths to emit as variants (the original's natural width is the largest
# srcset entry, so we only generate strictly-smaller widths).
VARIANT_WIDTHS = [480, 768, 1200]
HERO_QUALITY = 82  # variants are small; 82 keeps them crisp without bloat


def public_path(fs_path: str) -> str:
    rel = os.path.relpath(fs_path, PUBLIC)
    return "/" + rel.replace(os.sep, "/")


def main() -> None:
    sources = []
    for dirpath, _dirs, files in os.walk(os.path.join(PUBLIC, "images")):
        for fn in files:
            if fn.lower().endswith(".jpg"):
                sources.append(os.path.join(dirpath, fn))
    sources.sort()

    manifest: dict[str, dict] = {}
    made = 0
    skipped = 0
    failed = 0

    for src in sources:
        try:
            with Image.open(src) as im:
                w, h = im.size
                im.load()
            stem, ext = os.path.splitext(src)
            variants: list[int] = []
            for vw in VARIANT_WIDTHS:
                if vw >= w:
                    continue
                vh = max(1, round(h * vw / w))
                out = f"{stem}@{vw}{ext}"
                fresh = not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src)
                if fresh:
                    with Image.open(src) as base:
                        resized = base.resize((vw, vh), Image.LANCZOS)
                        save_jpeg(resized, out, quality=HERO_QUALITY)
                    made += 1
                else:
                    skipped += 1
                variants.append(vw)
            manifest[public_path(src)] = {"w": w, "h": h, "variants": variants}
        except Exception as exc:  # noqa: BLE001 — one bad file must not abort the run
            failed += 1
            print(f"  ! failed {src}: {exc}", file=sys.stderr)

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with_variants = sum(1 for v in manifest.values() if v["variants"])
    print(f"make-responsive: {len(sources)} sources, {with_variants} with variants, "
          f"{made} variants generated, {skipped} up-to-date, {failed} failed")
    print(f"manifest -> {os.path.relpath(MANIFEST, ROOT)}")


if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"done in {time.time() - t0:.1f}s")
