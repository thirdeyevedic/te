#!/usr/bin/env python3
"""
Generate the 56 Third Eye Events images via the Gemini (Google AI Studio) image API.

Why this exists:
  - Firefly browser-automation was blocked (agent-browser uses a temp profile +
    mock keychain + forced headless, so it can never read the user's real Chrome
    session; real-Chrome CDP is refused on the default profile).
  - Kling connector has 0 credits.
  - Gemini image models (e.g. gemini-2.5-flash-image / gemini-3-pro-image) are
    excellent at prompt-faithful photoreal generation and have a free tier at
    aistudio.google.com. We call the REST API directly with the user's key.

Outputs: one file per slot at /tmp/firefly/<slot>.<ext>
  (place_firefly.py then crops/resizes/places them into public/images/**).

Usage:
  GEMINI_API_KEY=... python3 scripts/gemini_generate.py --limit 1     # PoC
  GEMINI_API_KEY=... python3 scripts/gemini_generate.py               # all 56
  GEMINI_API_KEY=... GEMINI_MODEL=gemini-3-pro-image python3 scripts/gemini_generate.py

Env:
  GEMINI_API_KEY   (required) API key from https://aistudio.google.com/apikey
  GEMINI_MODEL     (optional) model id, default gemini-2.5-flash-image
"""
import os
import sys
import json
import time
import base64
import argparse
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kling_prompts as KP   # noqa: E402

OUTDIR = "/tmp/firefly"
PROGRESS = os.path.join(OUTDIR, "progress.json")
MAX_RETRIES = 6


def aspect_str(slot_obj):
    a = getattr(slot_obj, "aspect", None)
    if a:
        return f"{a[0]}:{a[1]}"
    return "16:9"


def call_api(prompt, aspect, api_key, model):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
           f":generateContent?key={api_key}")
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "aspectRatio": aspect},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def extract_image(resp):
    try:
        parts = resp["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("No candidates in response: " + json.dumps(resp)[:500])
    for part in parts:
        if isinstance(part, dict) and "inlineData" in part:
            mime = part["inlineData"].get("mimeType", "image/png")
            b64 = part["inlineData"]["data"]
            ext = "png" if "png" in mime else "jpg"
            return base64.b64decode(b64), ext
    raise RuntimeError("No inline image data in response: " + json.dumps(resp)[:500])


def generate_one(slot, api_key, model, quiet=False):
    prompt = slot.prompt
    aspect = aspect_str(slot)
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = call_api(prompt, aspect, api_key, model)
            raw, ext = extract_image(resp)
            out = os.path.join(OUTDIR, f"{slot.slot}.{ext}")
            with open(out, "wb") as f:
                f.write(raw)
            if not quiet:
                print(f"  ok  {slot.slot} ({len(raw)} bytes, .{ext})")
            return out
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            last_err = f"HTTP {e.code}: {body[:300]}"
            # 429 / 5xx -> backoff; 400 with aspectRatio -> retry without it
            if e.code == 400 and "aspectRatio" in body:
                # one-shot fallback: drop aspectRatio
                try:
                    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
                           f":generateContent?key={api_key}")
                    body2 = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"responseModalities": ["IMAGE"]},
                    }
                    req = urllib.request.Request(
                        url, data=json.dumps(body2).encode(),
                        headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=180) as r:
                        resp = json.loads(r.read().decode())
                    raw, ext = extract_image(resp)
                    out = os.path.join(OUTDIR, f"{slot.slot}.{ext}")
                    with open(out, "wb") as f:
                        f.write(raw)
                    if not quiet:
                        print(f"  ok  {slot.slot} (no-aspect fallback, {len(raw)} bytes)")
                    return out
                except Exception as e2:
                    last_err = f"fallback failed: {e2}"
            if e.code in (429, 500, 502, 503, 504):
                wait = min(2 ** attempt * 3, 60)
                if not quiet:
                    print(f"  retry {slot.slot} in {wait}s ({last_err})")
                time.sleep(wait)
                continue
            raise RuntimeError(last_err)
        except Exception as e:  # network/timeout/parse
            last_err = str(e)
            wait = min(2 ** attempt * 3, 60)
            if not quiet:
                print(f"  retry {slot.slot} in {wait}s ({last_err})")
            time.sleep(wait)
    raise RuntimeError(f"{slot.slot} failed after {MAX_RETRIES} tries: {last_err}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="generate only first N slots (PoC)")
    ap.add_argument("--slots", nargs="*", help="generate only these slot names")
    ap.add_argument("--sleep", type=float, default=1.5, help="delay between calls (s)")
    ap.add_argument("--no-sleep", action="store_true")
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:  # fallback: read from a temp file the user creates themselves
        keyfile = "/tmp/gemini_key.txt"
        if os.path.exists(keyfile):
            with open(keyfile) as f:
                api_key = f.read().strip()
    if not api_key:
        sys.exit("ERROR: set GEMINI_API_KEY, or put the key (no newline) in /tmp/gemini_key.txt.")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-image")

    os.makedirs(OUTDIR, exist_ok=True)
    progress = {}
    if os.path.exists(PROGRESS):
        try:
            progress = json.load(open(PROGRESS))
        except Exception:
            progress = {}

    slots = KP.ALL
    if args.slots:
        slots = [s for s in slots if s.slot in args.slots]
    if args.limit:
        slots = slots[: args.limit]

    done = [s for s in slots if progress.get(s.slot, {}).get("ok")]
    todo = [s for s in slots if s.slot not in {d.slot for d in done}]
    print(f"Model: {model}")
    print(f"Total slots: {len(slots)} | already done: {len(done)} | to do: {len(todo)}")

    for i, slot in enumerate(todo, 1):
        if not args.no_sleep and i > 1:
            time.sleep(args.sleep)
        print(f"[{i}/{len(todo)}] {slot.slot}")
        try:
            out = generate_one(slot, api_key, model)
            progress[slot.slot] = {"ok": True, "file": out}
        except Exception as e:
            progress[slot.slot] = {"ok": False, "error": str(e)[:300]}
            print(f"  FAILED {slot.slot}: {e}")
            # persist partial progress, but keep going for the rest
        json.dump(progress, open(PROGRESS, "w"), indent=2)

    ok = sum(1 for v in progress.values() if v.get("ok"))
    print(f"\nDONE. {ok} successful images in {OUTDIR}.")


if __name__ == "__main__":
    main()
