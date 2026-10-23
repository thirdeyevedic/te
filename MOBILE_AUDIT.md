# Mobile audit — all 76 routes

Checked against the live site (https://thirdeyeevents.com) on 23 October 2026, at 360×800, 390×844, 768×1024 and 1440×900.

## Verdict

**76 / 76 routes pass.** 304 route × viewport combinations, 0 failures, 0 warnings.

Traffic is mostly mobile, so the pass also weighed every page at 390×844 with the HTTP cache disabled and every image forced to load — the number a phone actually pays. Four pages were shipping desktop-weight assets; all four are fixed and re-measured.

## What "pass" means

| # | Check | Result |
|---|---|---|
| 1 | No horizontal overflow outside a real scroll container | 0 findings |
| 2 | `<meta name=viewport>` is `width=device-width, initial-scale=1` | 76/76 |
| 3 | No console errors, page errors or ≥400 responses | 76/76 |
| 4 | Burger opens the overlay, locks scroll (`html.is-menu-open`), Escape closes and unlocks | 76/76 |
| 5 | Controls ≥44×44; inline links ≥24 tall | 76/76 |
| 6 | No text below 11px; body copy ≥16px | 76/76 |
| 7 | `srcset`/`sizes` on sampled routes | pass |
| 8 | Carousel: mandatory snap, first card on the gutter, card ≤ viewport | pass |
| 9 | Signature Entry dialog: opens, 44px close, Escape closes, scroll restored | pass |
| 10 | Route expectations (`/admin/` login form, `/404/` title) | pass |

Plus the DOM audit at every viewport: hidden-but-painted text, duplicate ids, images without alt, unnamed controls, focusable content inside `aria-hidden`.

## Fixed in this pass

| Where | Problem | Before | After |
|---|---|---|---|
| All 76 routes | `logo.png` is 820×403 / 198KB, served into a 102×50 slot | 198KB | 22.6KB (2× file) |
| /weddings/experiences/ | Carousel card used a bare `<img>`: 1365px hero for a 271px card | 1117KB | 457KB |
| / | Opening sequence set three 1593px photos as CSS backgrounds for ~156px cards | 1491KB | 377KB |
| All 76 routes | Image ladder was 480/768/1200, so a 390pt phone at DPR 2 (780px) skipped to 1200 or to the untuned original | 41.0MB total | 28.6MB total |

Page weight across all 76 routes, 390×844, cache disabled: **41.0MB → 28.6MB (−30%)** for the ladder fix alone (same build, same method), on top of the three asset fixes above. The per-page table below is measured on the live site.

## Per-page results

`Screens` = page height in 844px viewports. `Images` = every image on the page, forced to load, at 390×844.

### Home

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/` | 15.2 | 2386KB | Cinematic opening (skippable) + 3 hero cards |

### About

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/about/` | 10.1 | 228KB | About subpage |
| `/about/founder/` | 7.6 | 66KB | About subpage |
| `/about/philosophy/` | 4.4 | 69KB | About subpage |
| `/about/story/` | 4.9 | 176KB | About subpage |
| `/about/vision/` | 4.4 | 66KB | About subpage |

### Destinations

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/destinations/` | 5.9 | 1371KB | 7 destination cards |
| `/destinations/bali/` | 7.1 | 850KB | Country page |
| `/destinations/bali/besakih/` | 6.6 | 400KB | Venue template (×30) |
| `/destinations/bali/nusa-dua/` | 6.4 | 400KB | Venue template (×30) |
| `/destinations/bali/seminyak/` | 6.5 | 400KB | Venue template (×30) |
| `/destinations/bali/ubud/` | 6.4 | 400KB | Venue template (×30) |
| `/destinations/bali/uluwatu/` | 6.5 | 400KB | Venue template (×30) |
| `/destinations/cruises/` | 7.2 | 829KB | Country page |
| `/destinations/cruises/anchor-cruise/` | 6.5 | 316KB | Venue template (×30) |
| `/destinations/cruises/celebrity/` | 6.4 | 316KB | Venue template (×30) |
| `/destinations/cruises/norwegian/` | 6.4 | 316KB | Venue template (×30) |
| `/destinations/cruises/royal-caribbean/` | 6.5 | 316KB | Venue template (×30) |
| `/destinations/cruises/silversea/` | 6.5 | 316KB | Venue template (×30) |
| `/destinations/india/` | 5.7 | 109KB | Seven-world taxonomy (intentional) |
| `/destinations/italy/` | 7.0 | 825KB | Country page |
| `/destinations/italy/amalfi-coast/` | 6.6 | 417KB | Venue template (×30) |
| `/destinations/italy/lake-como/` | 6.5 | 417KB | Venue template (×30) |
| `/destinations/italy/rome/` | 6.5 | 417KB | Venue template (×30) |
| `/destinations/italy/tuscany/` | 6.5 | 417KB | Venue template (×30) |
| `/destinations/italy/venice/` | 6.3 | 417KB | Venue template (×30) |
| `/destinations/kyoto/` | 7.3 | 780KB | Country page |
| `/destinations/kyoto/arashiyama/` | 6.6 | 506KB | Venue template (×30) |
| `/destinations/kyoto/fushimi-inari/` | 6.6 | 506KB | Venue template (×30) |
| `/destinations/kyoto/gion/` | 6.6 | 506KB | Venue template (×30) |
| `/destinations/kyoto/kinkaku-ji/` | 6.6 | 506KB | Venue template (×30) |
| `/destinations/kyoto/philosopher-s-path/` | 6.5 | 506KB | Venue template (×30) |
| `/destinations/maldives/` | 7.3 | 848KB | Country page |
| `/destinations/maldives/conrad-rangali/` | 6.5 | 375KB | Venue template (×30) |
| `/destinations/maldives/joali/` | 6.5 | 375KB | Venue template (×30) |
| `/destinations/maldives/reethi-rah/` | 6.6 | 375KB | Venue template (×30) |
| `/destinations/maldives/soneva-fushi/` | 6.5 | 375KB | Venue template (×30) |
| `/destinations/maldives/taj-exotica/` | 6.4 | 375KB | Venue template (×30) |
| `/destinations/switzerland/` | 7.1 | 866KB | Country page |
| `/destinations/switzerland/glacier-express/` | 6.4 | 371KB | Venue template (×30) |
| `/destinations/switzerland/interlaken/` | 6.5 | 371KB | Venue template (×30) |
| `/destinations/switzerland/lauterbrunnen/` | 6.1 | 371KB | Venue template (×30) |
| `/destinations/switzerland/st-moritz/` | 6.6 | 371KB | Venue template (×30) |
| `/destinations/switzerland/zermatt/` | 6.2 | 371KB | Venue template (×30) |

### IP Events

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/ip-events/` | 12.6 | 941KB | IP category page |
| `/ip-events/automotive/` | 4.3 | 92KB | IP category page |
| `/ip-events/awards/` | 4.2 | 83KB | IP category page |
| `/ip-events/concerts/` | 4.3 | 124KB | IP category page |
| `/ip-events/devotional/` | 4.2 | 130KB | IP category page |
| `/ip-events/exhibitions/` | 4.3 | 153KB | IP category page |
| `/ip-events/fashion/` | 4.2 | 88KB | IP category page |
| `/ip-events/political/` | 4.2 | 130KB | IP category page |
| `/ip-events/products/` | 4.3 | 128KB | IP category page |
| `/ip-events/sports/` | 4.2 | 145KB | IP category page |

### Production

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/production/` | 8.2 | 685KB | Production service page |
| `/production/ad-shoots/` | 4.6 | 126KB | Production service page |
| `/production/branded-content/` | 4.5 | 117KB | Production service page |
| `/production/digital-content/` | 4.6 | 101KB | Production service page |
| `/production/documentaries/` | 4.6 | 130KB | Production service page |
| `/production/feature-films/` | 5.8 | 140KB | Production service page |
| `/production/short-films/` | 4.4 | 120KB | Production service page |

### Weddings

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/weddings/` | 4.6 | 382KB |  |
| `/weddings/concepts/` | 8.6 | 133KB |  |
| `/weddings/destination/` | 5.7 | 1365KB |  |
| `/weddings/experiences/` | 4.7 | 402KB |  |
| `/weddings/experiences/celestial-entry/` | 7.9 | 109KB | Signature Entry detail |
| `/weddings/experiences/floral-entry/` | 7.8 | 319KB | Signature Entry detail |
| `/weddings/experiences/royal-entry/` | 7.5 | 361KB | Signature Entry detail |
| `/weddings/experiences/shiva-entry/` | 7.6 | 246KB | Signature Entry detail |
| `/weddings/vedic/` | 8.8 | 488KB |  |

### Contact, legal, utility

| Route | Screens | Images | Notes |
|---|---|---|---|
| `/admin/` | 1.0 | 0KB | Bare layout, no nav — needs a session |
| `/contact/` | 3.8 | 74KB | Enquiry form, single column |
| `/privacy/` | 3.9 | 69KB |  |
| `/sitemap/` | 5.6 | 24KB | Text-only index of every route |
| `/terms/` | 4.2 | 69KB |  |
| `/404.html` | 2.3 | 24KB | Solid nav by design |

## Open items

1. **Remaining weight is encoding, not selection.** Every route now picks the right variant, but the variants keep 4:4:4 chroma at q82 — `/destinations/` is still 1.4MB for seven cards. Switching the *variants* to 4:2:0 would roughly halve that; it was chosen deliberately to protect saturated colour (saffron, marigold), so it needs a visual check before I touch it.
2. **11px microcopy.** Eyebrows, meta labels and card captions render at exactly 11px — the probe's floor. 12px reads better on a phone in daylight, but it moves every label on the site, so it is a design decision.
3. **Body copy over photographs.** `/weddings/vedic/` centres a paragraph on a dark image at low contrast; the country and venue heroes do the same. Legible at night, thin in sunlight. A stronger scrim would fix it.
4. **`/admin/`** is the only route the desktop audit cannot reach without a session. It passes the mobile probe structurally.
