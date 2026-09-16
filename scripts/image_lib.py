#!/usr/bin/env python3
"""
image_lib — shared helpers for sourcing, reviewing and processing site imagery.

Primary source is the Wikimedia Commons API (keyless, high-resolution, reliable).
Openverse is used opportunistically as enrichment for stock photography and is
skipped silently when it rate-limits.

Only licences that permit commercial use *and* derivative works are accepted:
public domain, CC0, CC BY, CC BY-SA. Anything marked NC (non-commercial) or
ND (no derivatives) is rejected, since we crop every image to fit the layout.
Attribution for the images we keep is written to public/images/CREDITS.md.
"""

import hashlib
import io
import json
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

WORK = "/tmp/imgwork"
CACHE = os.path.join(WORK, "cache")
CAND = os.path.join(WORK, "candidates")
SHEETS = os.path.join(WORK, "sheets")

for _d in (WORK, CACHE, CAND, SHEETS):
    os.makedirs(_d, exist_ok=True)

UA = "ThirdEyeEventsAssetBot/1.0 (asset sourcing; hello@thirdeyeevents.com)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# Licences that forbid commercial use or derivatives are unusable for a
# commercial site whose layout crops every image.
LICENCE_BLOCK = re.compile(r"(\bNC\b|NonCommercial|Non-Commercial|\bND\b|NoDeriv|No Deriv)", re.I)


def _get(url, timeout=50, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:  # noqa: BLE001 - network flake handling
            last = exc
            time.sleep(1.0 + attempt)
    raise last


def _api_get(url, timeout=25, tries=2):
    """A metadata query. Bounded tighter than an image download: a stalled API
    host must not cost a slot more than a minute or so in total."""
    return _get(url, timeout=timeout, tries=tries)


# ── Wikimedia Commons ──────────────────────────────────────────────────────

def _commons_search(query, limit, thumb_width):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo|categories",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": str(thumb_width),
        "cllimit": "max",
        "format": "json",
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    try:
        raw = _api_get(url)
    except Exception:  # noqa: BLE001
        return []
    try:
        pages = json.loads(raw).get("query", {}).get("pages", {})
    except Exception:  # noqa: BLE001
        return []

    out = []
    for page in pages.values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        if info.get("mime") not in ("image/jpeg", "image/png"):
            continue
        w, h = info.get("width") or 0, info.get("height") or 0
        if w < 1000 or h < 600:
            continue
        licence = (meta.get("LicenseShortName", {}).get("value") or "").strip()
        terms = meta.get("UsageTerms", {}).get("value") or ""
        if LICENCE_BLOCK.search(f"{licence} {terms}"):
            continue
        artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value") or "").strip()
        cats = " ".join(c.get("title", "") for c in (page.get("categories") or []))
        # Commons' own peer review — the sharpest, best-composed files on the site.
        quality = bool(re.search(r"Quality images|Featured pictures", cats))
        out.append(
            {
                "source": "commons",
                "url": info.get("thumburl") or info.get("url"),
                "origin": info.get("url"),
                "width": w,
                "height": h,
                "license": licence or "see source",
                "creator": artist[:80],
                "title": page.get("title", "").replace("File:", ""),
                "foreign_landing_url": info.get("descriptionurl"),
                "query": query,
                "quality": quality,
            }
        )
    return out


def search_commons(query, limit=30, thumb_width=1920):
    """Cached, but an empty result is never persisted — it may be a transient miss."""
    key = f"commons::{query}::{limit}::{thumb_width}"
    path = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest() + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if data:
            return data
    data = _commons_search(query, limit, thumb_width)
    if data:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    return data


# ── Openverse (opportunistic enrichment) ───────────────────────────────────

# Openverse allows only a handful of anonymous requests per minute. Space the
# calls out, back off on 429 — and once it is clearly refusing us, stop asking
# so a full run is not held up by retries that will not succeed.
_OV_LOCK = threading.Lock()
_OV_LAST = [0.0]
_OV_MIN_INTERVAL = 14.0
_OV_STRIKES = [0]
_OV_DOWN = [False]


def _openverse_search(query, page_size, source):
    if _OV_DOWN[0]:
        return []

    params = {
        "q": query,
        "license": "cc0,pdm,by,by-sa",
        "page_size": str(page_size),
        "mature": "false",
    }
    if source:
        params["source"] = source
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params)

    for attempt in range(3):
        with _OV_LOCK:
            wait = _OV_MIN_INTERVAL - (time.time() - _OV_LAST[0])
            if wait > 0:
                time.sleep(wait)
            _OV_LAST[0] = time.time()
        try:
            raw = _get(url, timeout=25, tries=1)
        except Exception as exc:  # noqa: BLE001
            if "429" in str(exc):
                _OV_STRIKES[0] += 1
                if _OV_STRIKES[0] >= 3:
                    _OV_DOWN[0] = True
                    print("      [openverse] rate-limited — disabling for this run")
                    return []
                time.sleep(20)
                continue
            return []
        try:
            data = json.loads(raw)
        except Exception:  # noqa: BLE001 - Cloudflare interstitial, not JSON
            _OV_STRIKES[0] += 1
            if _OV_STRIKES[0] >= 3:
                _OV_DOWN[0] = True
                return []
            time.sleep(8)
            continue
        _OV_STRIKES[0] = 0
        return data.get("results", [])
    return []


def search_openverse(query, page_size=24, source=None):
    """Cached, but never caches a failure — a 429 must not look like 'no results'."""
    key = f"openverse::{query}::{page_size}::{source}"
    path = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest() + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if data:
            return data
    data = _openverse_search(query, page_size, source)
    if data:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    return data


# ── Flickr public feed (keyless community photography) ─────────────────────

def _flickr_feed(tag):
    url = (
        "https://www.flickr.com/services/feeds/photos_public.gne"
        f"?tags={urllib.parse.quote(tag)}&tagmode=all&format=json&nojsoncallback=1"
    )
    try:
        raw = _api_get(url, timeout=20)
        items = json.loads(raw).get("items", [])
    except Exception:  # noqa: BLE001
        return []

    out = []
    for it in items:
        media = (it.get("media") or {}).get("m")
        if not media:
            continue
        # The feed hands us the 240px rendition. Flickr's larger renditions are
        # named by a single suffix letter, but not every photo has every size —
        # _b (1024px) is missing on many, so _c (800px) and _z (640px) are
        # offered as fallbacks rather than letting the candidate fail outright.
        big = re.sub(r"_[a-z]\.jpg$", "_b.jpg", media)
        fallbacks = [
            re.sub(r"_[a-z]\.jpg$", f"_{s}.jpg", media) for s in ("c", "z")
        ]
        out.append(
            {
                "source": "flickr",
                "url": big,
                "origin": big,
                "fallbacks": fallbacks,
                "width": 1024,
                "height": 768,
                "license": "CC (see Flickr page)",
                "creator": (it.get("author") or "").replace("nobody@flickr.com (", "").rstrip(")"),
                "title": it.get("title"),
                "foreign_landing_url": it.get("link"),
                "query": tag,
            }
        )
    return out


def search_flickr(tag):
    """Cached, but an empty result is never persisted — it may be a transient miss."""
    key = f"flickr::{tag}"
    path = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest() + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if data:
            return data
    data = _flickr_feed(tag)
    if data:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    return data


# ── Ranking ────────────────────────────────────────────────────────────────

SOURCE_RANK = {"rawpixel": 0, "stocksnap": 1, "commons": 2, "flickr": 3}


def aspect_penalty(cand, aspect):
    w, h = cand.get("width") or 0, cand.get("height") or 0
    if not w or not h:
        return 9.0
    return abs((w / h) - aspect) / max(aspect, 0.4)


def interleave(groups):
    """Round-robin merge of several ranked result lists.

    Each search engine already orders its own results by relevance, so mixing
    them round-robin keeps that judgement instead of replacing it with a
    heuristic of ours.
    """
    merged = []
    depth = max((len(g) for g in groups), default=0)
    for i in range(depth):
        for g in groups:
            if i < len(g):
                merged.append(g[i])
    return merged


MAX_BYTES = 14 * 1024 * 1024


def download(cand, out_dir, idx, want_width=1600):
    """Download one candidate. Returns (path, w, h) or None.

    The cache file is named after the candidate's own URL rather than its
    position, so that re-running a slot with a different ordering reuses the
    bytes already on disk instead of re-fetching — and never hands back a file
    that belongs to a different image.
    """
    key = hashlib.sha1((cand.get("url") or f"{idx}").encode()).hexdigest()[:16]
    path = os.path.join(out_dir, f"{key}.img")
    if os.path.exists(path):
        try:
            with Image.open(path) as im:
                return path, im.width, im.height
        except Exception:  # noqa: BLE001
            os.remove(path)

    urls = []
    # The API already handed us a valid 1920px thumbnail — trust it first.
    if cand.get("url"):
        urls.append(cand["url"])
    # Sources that advertise alternates (Flickr's rendition sizes) get a try too.
    urls.extend(cand.get("fallbacks") or [])

    if cand.get("source") == "commons" and cand.get("origin"):
        m = re.match(
            r"https://upload\.wikimedia\.org/wikipedia/commons/([0-9a-f])/([0-9a-f]{2})/(.+)$",
            cand["origin"],
        )
        if m:
            a, ab, name = m.groups()
            for w in (1920, 1280, 1024, 800):
                if w >= min(want_width, cand.get("width") or w):
                    continue
                urls.append(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/"
                    f"{a}/{ab}/{urllib.parse.quote(name)}/{w}px-{urllib.parse.quote(name)}"
                )
        # Originals can be 15 MB+; only take one when it is modest.
        if (cand.get("width") or 0) <= 2600:
            urls.append(cand["origin"])

    seen = set()
    # At most three attempts per candidate. Each can burn its timeout, so an
    # unbounded list turns one bad host into minutes of a slot's budget.
    for url in [u for u in urls if u and not (u in seen or seen.add(u))][:3]:
        try:
            # Rendition probes fail fast and often; one attempt each, and a
            # short timeout — a single stalled host must not hold the whole
            # slot back, since we are downloading several candidates at once.
            raw = _get(url, timeout=25, tries=1)
            if len(raw) > MAX_BYTES:
                continue
            with Image.open(io.BytesIO(raw)) as im:
                if im.width < 640:
                    continue
                im = im.convert("RGB")
                im.save(path, "JPEG", quality=92)
                return path, im.width, im.height
        except Exception:  # noqa: BLE001
            continue
    return None


def download_many(jobs, workers=5):
    """jobs: list of (cand, out_dir, idx, want_width). Returns list in order."""
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda a: download(*a), jobs))


# ── Review sheets ──────────────────────────────────────────────────────────

def _font(size=15):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(p, size)
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default()


def contact_sheet(paths, labels, out_path, cols=4, cell=400, title=None):
    rows = max(1, (len(paths) + cols - 1) // cols)
    pad, cap = 10, 30
    head = 42 if title else 0
    W = cols * (cell + pad) + pad
    H = head + rows * (cell + cap + pad) + pad
    sheet = Image.new("RGB", (W, H), (16, 16, 16))
    draw = ImageDraw.Draw(sheet)
    font, tfont = _font(15), _font(24)
    if title:
        draw.text((pad + 4, 10), title, fill=(232, 205, 130), font=tfont)
    for i, (p, label) in enumerate(zip(paths, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = head + pad + r * (cell + cap + pad)
        draw.rectangle([x, y, x + cell, y + cell], fill=(34, 34, 34))
        try:
            with Image.open(p) as im:
                im = im.convert("RGB")
                im.thumbnail((cell, cell))
                sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        except Exception:  # noqa: BLE001
            pass
        draw.text((x + 4, y + cell + 6), label, fill=(230, 200, 120), font=font)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sheet.save(out_path, "JPEG", quality=88)
    return out_path


# ── Processing ─────────────────────────────────────────────────────────────

def crop_resize(im, aspect, width, focus=0.5):
    """Centre-crop to aspect (w/h) with a focus bias, then resize to `width`."""
    im = im.convert("RGB")
    w, h = im.size
    if w / h > aspect:
        new_w = int(round(h * aspect))
        left = int((w - new_w) * focus)
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(round(w / aspect))
        top = int((h - new_h) * focus)
        im = im.crop((0, top, w, top + new_h))
    if im.width > width:
        im = im.resize((width, int(round(width / aspect))), Image.LANCZOS)
    return im


def save_jpeg(im, path, quality=80):
    """Write a JPEG tuned to preserve saturated colour.

    `subsampling=0` means 4:4:4 — chroma stored at full resolution. Pillow's
    default for any quality below 95 is 4:2:0, which stores colour at a QUARTER
    of the luminance resolution. That is the wrong trade for this site: the
    palette is built on marigold, vermilion, saffron, emerald and turquoise, and
    4:2:0 blunts precisely those saturated reds and oranges while bleeding colour
    across high-contrast edges. 4:4:4 costs roughly 10-15% more bytes and is the
    single most effective setting for keeping vibrant colour intact on screen.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(
        path, "JPEG", quality=quality, subsampling=0, optimize=True, progressive=True
    )
    return os.path.getsize(path)
