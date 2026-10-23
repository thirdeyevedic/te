# Mobile vertical spacing — 76 routes, measured

Checked at **390×844** against a local build of `c35bdd0`, then re-measured live on thirdeyeevents.com. The measurement is new: `spacing-probe.mjs` walks text-node and media rects to find where content actually paints, then reports the empty band between consecutive sections. No existing gate measured this, which is why the site passed every check while reading as broken on a phone.

## Verdict

**76 / 76 routes pass.** No empty band exceeds 231px (was 581), no route spends more than 29% of its height on section padding (was 39%), and no route got taller.

Total document height across all 76 routes: **394,198 → 338,817px (−14.0%)**.

## What was wrong

| | Before | After |
|---|---|---|
| `--space-section` @390×844 | 135px (`clamp(7rem, 16vh, 13rem)`) | 80px (`clamp(4.5rem, 20.5vw, 5rem)`) |
| `--space-section-lg` @390×844 | 186px (`clamp(9rem, 22vh, 18rem)`) | 109px (`clamp(6.25rem, 28vw, 7rem)`) |
| Two adjacent sections | 270px apart | 160px |
| CTA band | 372px of padding | 218px |
| Hero → next section | 219px | 128px |

`16vh` of 844 is **above** the 7rem floor, so a tall phone got more air than a short laptop window, and every breakpoint in the codebase is `min-width` — nothing ever subtracted as the viewport narrowed. The mobile branch is now width-driven, so a 390×844 and a 390×700 handset agree.

## Structural space the tokens could not reach

| Route | Was | Now |
|---|---|---|
| `/` (home hero) | `min-height: 100svh` filled the screen exactly — the next section was invisible until you scrolled blind; hard-coded 128/112px inset | `min(100svh, 46rem)`, inset 96/72px |
| `/weddings/experiences/` | 616px between the last card and the next heading: 202px inner padding inside a 135px section, plus 67px track padding, plus 84px from `(pointer: coarse)` | inner padding 0, track 24px, coarse-pointer rule overridden → 208px |
| `/weddings/experiences/` card | 439px tall for a 335px-wide box | 343px (`min-height: 0` neutralises `.sig`'s 405px floor) |
| `/sitemap/` | Only content page with no `PageHero`: opened with 186px of black under an 88px navbar | pays nav clearance + 32px |
| `/404` | `100svh` plus a full `.section-lg` | `min(100svh, 42rem)` |
| 4 one-sentence sections | a full `.section` / `.section-lg` beat | `.section--compact`: 0.75×, or 0.8× of the large token where the line is display-size |
| last `.family`, last `.chain__node` | trailing padding after the final item, stacked on the section's own | dropped on mobile |

## Stacked card heights

Every card is full-width on a phone, so device-height units made them tall for a narrow box. They are now a function of card width.

| Card | Was @390 | Now |
|---|---|---|
| `.world` (`/destinations/`) | 380px (`45vh`) | 304px (`78vw`) |
| `.pathway` (`/`) | 354px (`42vh`) | 265px (`68vw`) |
| `.sig-card` (`/`) | 490px (`3 / 4.2`) | 350px (`1 / 1`) |
| `.path` (`/weddings/`) | 304px (`36vh`) | 242px (`62vw`) |
| `.world__card` (`/weddings/destination/`) | 416px (`3 / 4`) | 359px (`1 / 1.15`) |
| `.cat` (`/destinations/india/`) | 287px (`34vh`) | 234px (`60vw`) |

## Per-page results

`Height` is the full document at 390×844. `Gap` is the largest empty band between two sections' painted content.

### Home

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/` | 10,547px | -18% | 214px | 17% | Cinematic opening (skippable) + 3 hero cards |

### About

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/about/` | 7,620px | -11% | 214px | 16% | About subpage |
| `/about/founder/` | 5,700px | -11% | 223px | 16% | About subpage |
| `/about/philosophy/` | 3,100px | -16% | 223px | 25% | About subpage |
| `/about/story/` | 3,613px | -13% | 219px | 20% | About subpage |
| `/about/vision/` | 3,149px | -15% | 219px | 23% | About subpage |

### Destinations

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/destinations/` | 4,125px | -18% | 192px | 14% | 7 destination cards |
| `/destinations/bali/` | 5,027px | -16% | 192px | 24% | Country page |
| `/destinations/bali/besakih/` | 4,724px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/bali/nusa-dua/` | 4,570px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/bali/seminyak/` | 4,679px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/bali/ubud/` | 4,609px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/bali/uluwatu/` | 4,664px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/cruises/` | 5,112px | -16% | 192px | 24% | Country page |
| `/destinations/cruises/anchor-cruise/` | 4,650px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/cruises/celebrity/` | 4,636px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/cruises/norwegian/` | 4,623px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/cruises/royal-caribbean/` | 4,702px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/cruises/silversea/` | 4,707px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/india/` | 3,978px | -17% | 231px | 14% | Seven-world taxonomy (intentional) |
| `/destinations/italy/` | 4,967px | -16% | 192px | 24% | Country page |
| `/destinations/italy/amalfi-coast/` | 4,756px | -14% | 212px | 23% | Venue template (x30) |
| `/destinations/italy/lake-como/` | 4,716px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/italy/rome/` | 4,672px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/italy/tuscany/` | 4,703px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/italy/venice/` | 4,517px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/kyoto/` | 5,196px | -16% | 192px | 23% | Country page |
| `/destinations/kyoto/arashiyama/` | 4,795px | -14% | 212px | 23% | Venue template (x30) |
| `/destinations/kyoto/fushimi-inari/` | 4,747px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/kyoto/gion/` | 4,762px | -14% | 212px | 23% | Venue template (x30) |
| `/destinations/kyoto/kinkaku-ji/` | 4,739px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/kyoto/philosopher-s-path/` | 4,721px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/maldives/` | 5,193px | -16% | 192px | 23% | Country page |
| `/destinations/maldives/conrad-rangali/` | 4,662px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/maldives/joali/` | 4,660px | -15% | 213px | 24% | Venue template (x30) |
| `/destinations/maldives/reethi-rah/` | 4,747px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/maldives/soneva-fushi/` | 4,693px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/maldives/taj-exotica/` | 4,586px | -15% | 213px | 24% | Venue template (x30) |
| `/destinations/switzerland/` | 5,039px | -16% | 192px | 24% | Country page |
| `/destinations/switzerland/glacier-express/` | 4,604px | -15% | 212px | 24% | Venue template (x30) |
| `/destinations/switzerland/interlaken/` | 4,706px | -15% | 212px | 23% | Venue template (x30) |
| `/destinations/switzerland/lauterbrunnen/` | 4,359px | -16% | 213px | 25% | Venue template (x30) |
| `/destinations/switzerland/st-moritz/` | 4,758px | -14% | 212px | 23% | Venue template (x30) |
| `/destinations/switzerland/zermatt/` | 4,461px | -15% | 212px | 25% | Venue template (x30) |

### IP Events

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/ip-events/` | 10,163px | -4% | 214px | 6% | IP category page |
| `/ip-events/automotive/` | 3,082px | -15% | 219px | 23% | IP category page |
| `/ip-events/awards/` | 3,015px | -15% | 219px | 24% | IP category page |
| `/ip-events/concerts/` | 3,056px | -15% | 219px | 24% | IP category page |
| `/ip-events/devotional/` | 3,031px | -15% | 219px | 24% | IP category page |
| `/ip-events/exhibitions/` | 3,119px | -15% | 219px | 23% | IP category page |
| `/ip-events/fashion/` | 3,031px | -15% | 219px | 24% | IP category page |
| `/ip-events/political/` | 3,015px | -15% | 219px | 24% | IP category page |
| `/ip-events/products/` | 3,056px | -15% | 219px | 24% | IP category page |
| `/ip-events/sports/` | 3,031px | -15% | 219px | 24% | IP category page |

### Production

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/production/` | 6,257px | -10% | 223px | 15% | Production service page |
| `/production/ad-shoots/` | 3,194px | -17% | 219px | 28% | Production service page |
| `/production/branded-content/` | 3,115px | -17% | 219px | 28% | Production service page |
| `/production/digital-content/` | 3,194px | -17% | 219px | 28% | Production service page |
| `/production/documentaries/` | 3,225px | -17% | 219px | 27% | Production service page |
| `/production/feature-films/` | 4,066px | -17% | 219px | 27% | Production service page |
| `/production/short-films/` | 3,083px | -17% | 219px | 29% | Production service page |

### Weddings

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/weddings/` | 3,230px | -17% | 192px | 17% |  |
| `/weddings/concepts/` | 6,811px | -7% | 212px | 8% |  |
| `/weddings/destination/` | 4,198px | -12% | 199px | 17% |  |
| `/weddings/experiences/` | 2,878px | -28% | 208px | 25% |  |
| `/weddings/experiences/celestial-entry/` | 5,876px | -11% | 224px | 18% | Signature Entry detail |
| `/weddings/experiences/floral-entry/` | 5,844px | -12% | 224px | 18% | Signature Entry detail |
| `/weddings/experiences/royal-entry/` | 5,604px | -12% | 224px | 19% | Signature Entry detail |
| `/weddings/experiences/shiva-entry/` | 5,660px | -12% | 224px | 18% | Signature Entry detail |
| `/weddings/vedic/` | 6,487px | -12% | 225px | 19% |  |

### Contact, legal, utility

| Route | Height | Δ | Gap | Padding share | Notes |
|---|---|---|---|---|---|
| `/admin/` | 844px | +0% | 0px | 0% | Bare layout, no nav — needs a session |
| `/contact/` | 2,889px | -9% | 82px | 12% | Enquiry form |
| `/privacy/` | 3,042px | -8% | 82px | 11% |  |
| `/sitemap/` | 4,475px | -5% | 0px | 4% | Only content page with no PageHero |
| `/terms/` | 3,280px | -8% | 82px | 10% |  |
| `/404.html` | 1,672px | -13% | 0px | 13% | 404 template |

## What was deliberately left alone

- **Desktop and tablet.** 1440×900 across all 76 routes shows zero change: `--space-section` 144px, `--space-section-lg` 198px, `.phero` 212/90, `.cta` 198, home hero 900px, and every card box identical. The mobile block stops at 47.99em so a 768px viewport keeps the old rendering; the 767→768px jump (80→164px) is intentional.
- **`--nav-h`.** Fixed-nav clearance, not air — it stays inside every `calc()` and in the 12 `scroll-margin-top` rules that depend on it.
- **Tap targets.** `.btn` padding, `.link-line`, footer links and `.sm-link` are 44px/24px floors the mobile probe enforces; none were touched.
- **`--space-gutter`.** Horizontal grid line and carousel snap origin.

## Remaining, and why

1. **Body copy over photographs** (`/weddings/vedic/` centres a paragraph on a dark image; country and venue heroes do the same) is legible at night and thin in sunlight. A stronger scrim would fix it — a design call, not a spacing one.
2. **11px microcopy** is still exactly the probe's floor. 12px reads better in daylight but moves every label on the site.
3. **Variant encoding** is still q82 4:4:4; `/destinations/` remains ~1.4MB. Dropping the *variants* to 4:2:0 would roughly halve it but needs a visual sign-off on the saffron and marigold.

## Reproducing

```
cd ~/.workbuddy-ai/binaries/node/workspace
node spacing-probe.mjs <baseUrl> /tmp/pages.txt --json out.json      # mobile
node spacing-probe.mjs <baseUrl> /tmp/pages.txt --desktop --json out.json   # desktop invariance
```
Thresholds: `maxGap ≤ 240px`, `padShare ≤ 0.35`, `revealHidden === 0`. Two traps found while building it, both fixed: a 0.8×viewport scroll walk outruns the IntersectionObserver and reports phantom hidden reveals, and reading the walk bound before lazy images finish stops ~2,600px early on the home page.

