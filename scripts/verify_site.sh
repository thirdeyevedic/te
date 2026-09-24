#!/usr/bin/env bash
# verify_site.sh — screenshot key pages with headless Chrome for a visual
# context check. Usage: verify_site.sh <base_url> <out_dir>
#
# Forces prefers-reduced-motion (so IntersectionObserver .reveal elements are
# visible), settles lazy images with --virtual-time-budget, and captures the
# full page at 1440 wide.
set -euo pipefail

BASE="${1:-http://localhost:4322}"
OUT="${2:-/tmp/imgwork/shots}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$OUT"

PAGES=(
  "/"
  "/weddings/"
  "/weddings/vedic/"
  "/weddings/concepts/"
  "/weddings/destination/"
  "/weddings/experiences/"
  "/destinations/"
  "/destinations/india/"
  "/destinations/maldives/"
  "/destinations/switzerland/"
  "/destinations/kyoto/"
  "/destinations/italy/"
  "/destinations/bali/"
  "/destinations/cruises/"
  "/ip-events/"
  "/ip-events/automotive/"
  "/ip-events/awards/"
  "/ip-events/products/"
  "/ip-events/sports/"
  "/ip-events/fashion/"
  "/ip-events/political/"
  "/ip-events/devotional/"
  "/ip-events/concerts/"
  "/ip-events/exhibitions/"
  "/production/"
  "/production/feature-films/"
  "/production/digital-content/"
  "/production/branded-content/"
  "/production/ad-shoots/"
  "/about/"
  "/about/story/"
  "/about/philosophy/"
  "/about/vision/"
  "/about/founder/"
  "/contact/"
)

for p in "${PAGES[@]}"; do
  name="$(echo "$p" | tr '/ ' '__')"
  out="$OUT/${name}.png"
  echo "→ $BASE$p"
  "$CHROME" \
    --headless=new \
    --no-sandbox \
    --disable-gpu \
    --force-prefers-reduced-motion \
    --virtual-time-budget=12000 \
    --hide-scrollbars \
    --window-size=1440,5600 \
    --screenshot="$out" \
    "$BASE$p" 2>/dev/null || echo "  ! failed: $p"
done

echo "saved screenshots to $OUT"
