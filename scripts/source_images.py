#!/usr/bin/env python3
"""
source_images — fetch candidates for every manifest slot and pick a provisional
winner for each.

Run:  python scripts/source_images.py [slot ...]

Candidates land in /tmp/imgwork/candidates/<slot>/, per-slot contact sheets in
/tmp/imgwork/sheets/<slot>.jpg, and provisional picks in /tmp/imgwork/picks.json.
"""

import json
import os
import sys

import image_lib as il
from image_manifest import MANIFEST

N_CANDIDATES = 12
# We download a few more than we keep, because some candidates turn out to be
# undersized or unreadable. Fetching far more than that only costs time — the
# contact sheet is a shortlist to choose from, not an exhaustive survey.
# Bumped from 8/11 so context-grounded re-sourcing has more to choose from and
# higher-quality, larger shots can outrank a mediocre snapshot.
N_DOWNLOAD = 16
# Slots are independent, so the pass can be sharded across processes. Each
# shard writes its own picks file, which apply_images.py merges.
PICKS = os.environ.get("IMG_PICKS") or os.path.join(il.WORK, "picks.json")


def collect(slot):
    """Gather candidates for one manifest slot.

    Each query is kept as its own ordered list rather than being pooled and
    re-sorted. Search engines already rank by relevance, and re-scoring their
    output with a keyword heuristic of ours promoted loose matches over good
    ones — a wedding hero slot once resolved to a portrait of a woman in a
    field. Merging the lists round-robin keeps each engine's own judgement
    while still giving every query a turn at the front.

    The order the sources are merged in is deliberate. Commons leads every
    slot, because across this whole build it was consistently the strongest
    source and every bad result traced back to a badly written query rather
    than to the archive itself.

    The other two are weaker than they look. The Flickr public feed is not a
    search engine — it returns the twenty most *recent* photographs carrying a
    tag, so an "incense" query answered with a child in a pink jacket, and a
    "wedding" query answered with a Western model in borrowed styling. Openverse
    fronts genuinely curated stock, which is exactly right for editorial
    concepts, but it rate-limits anonymous callers hard and often returns
    nothing. Both are kept as enrichment behind Commons, and a slot resolves
    from whichever of the three answers best.
    """
    commons_groups, ov_groups, flickr_groups = [], [], []
    seen = set()

    def add(bucket, cands):
        fresh = []
        for c in cands:
            url = c.get("url")
            if url and url not in seen:
                seen.add(url)
                fresh.append(c)
        if fresh:
            bucket.append(fresh)

    # Commons — real places, ceremonies, architecture, craft. Effectively unlimited.
    for query in slot.get("commons", []):
        add(commons_groups, il.search_commons(query, limit=26, thumb_width=1920))
        # Peer-reviewed "Quality images" are vetted, professionally shot, high-
        # resolution photographs — exactly the production value a luxury brand
        # needs. We now pull them for EVERY slot (interleaved right after the
        # primary query, so they share the front of the relevance queue) rather
        # than only for place slots, because the context-grounded queries in
        # image_manifest.py are concrete enough that the QI subset stays on-topic
        # while raising quality. The apply_images verification gate still catches
        # any loose match.
        add(
            commons_groups,
            il.search_commons(f'{query} incategory:"Quality images"', limit=20, thumb_width=1920),
        )

    # Openverse — curated stock. Often rate-limited; harmless if not. Gated
    # behind NO_OPENVERSE so a full re-run can skip the slow, weak source and
    # still complete (Commons + Flickr carry the relevance).
    if slot.get("ov") and not os.environ.get("NO_OPENVERSE"):
        add(ov_groups, il.search_openverse(slot["ov"], page_size=50))

    # Flickr public feed — extra community photography on the same subject.
    tags = slot.get("flickr") or []
    if isinstance(tags, str):
        tags = [tags]
    for tag in tags:
        add(flickr_groups, il.search_flickr(tag))

    return il.interleave(commons_groups + ov_groups + flickr_groups)


def fetch(slot, force=False):
    slot_id = slot["slot"]
    out_dir = os.path.join(il.CAND, slot_id)
    os.makedirs(out_dir, exist_ok=True)
    meta_path = os.path.join(out_dir, "meta.json")

    if os.path.exists(meta_path) and not force:
        with open(meta_path, encoding="utf-8") as fh:
            return json.load(fh)

    ranked = collect(slot)
    jobs = [(c, out_dir, i, slot["width"]) for i, c in enumerate(ranked[:N_DOWNLOAD])]
    results = il.download_many(jobs, workers=8)

    kept = []
    for cand, got in zip(ranked[: len(jobs)], results):
        if not got or len(kept) >= N_CANDIDATES:
            continue
        path, w, h = got
        kept.append(
            {
                "idx": len(kept),
                "file": path,
                "w": w,
                "h": h,
                "provider": cand.get("source"),
                "license": cand.get("license"),
                "title": cand.get("title"),
                "creator": cand.get("creator"),
                "landing": cand.get("foreign_landing_url"),
                "url": cand.get("url"),
                "query": cand.get("query"),
            }
        )

    if not kept:
        print(f"  !! no candidates for {slot_id}")
        return []

    aspect = slot["aspect"][0] / slot["aspect"][1]
    want_w = slot["width"]

    def pick_key(c):
        # Stable sort: candidates already arrive in relevance order, so a
        # tiebreak that reorders equals would throw that away.
        #
        # Two things disqualify a candidate ahead of relevance. One that is
        # too small cannot be upscaled — the file would ship soft at hero size
        # — and one with the wrong proportions would need a destructive crop.
        # Both are demoted rather than dropped, so a slot still resolves even
        # if nothing ideal was found.
        #
        # Final tiebreak prefers the larger source (more resolution = ships
        # sharper at hero size = higher production value) without ever
        # overriding relevance or aspect, because it only acts when the first
        # three keys tie.
        too_small = (c["w"] or 0) < want_w
        pen = il.aspect_penalty(c, aspect)
        return (too_small, pen > 0.5, pen, -(c["w"] or 0))

    kept.sort(key=pick_key)
    labels = [
        f"{c['idx']:02d} {c['provider']} {c['w']}x{c['h']} {str(c['title'])[:30]}"
        for c in kept
    ]
    il.contact_sheet(
        [c["file"] for c in kept],
        labels,
        os.path.join(il.SHEETS, f"{slot_id}.jpg"),
        title=f"{slot_id}  →  {slot['out']}",
    )

    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(kept, fh, indent=1)
    return kept


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    wanted = set(args)

    shard, shards = 0, 1
    for a in sys.argv[1:]:
        if a.startswith("--shard="):
            shard, shards = (int(x) for x in a.split("=", 1)[1].split("/"))

    picks = {}
    if os.path.exists(PICKS):
        with open(PICKS, encoding="utf-8") as fh:
            picks = json.load(fh)

    for i, slot in enumerate(MANIFEST):
        if wanted and slot["slot"] not in wanted:
            continue
        if i % shards != shard:
            continue
        print(f"→ {slot['slot']}", flush=True)
        kept = fetch(slot, force=force)
        if kept:
            picks[slot["slot"]] = {
                "out": slot["out"],
                "aspect": slot["aspect"],
                "width": slot["width"],
                "candidates": kept,
                "pick": kept[0]["idx"],
            }
            print(
                f"   {len(kept)} candidates · pick {kept[0]['idx']:02d} "
                f"({kept[0]['provider']} {kept[0]['w']}x{kept[0]['h']})",
                flush=True,
            )

    with open(PICKS, "w", encoding="utf-8") as fh:
        json.dump(picks, fh, indent=1)
    print(f"\nwrote {PICKS} ({len(picks)} slots)")


if __name__ == "__main__":
    main()
