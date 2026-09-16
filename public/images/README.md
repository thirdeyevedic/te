# Imagery — Third Eye Events

**All imagery on this site is AI-generated.** Nothing here is a placeholder, and
nothing here is a photograph of a real event, venue, couple or person.

## How the assets are organised

```
public/images/
  hero-cinematic.jpg          homepage hero (1920×1080)
  og.jpg                      social share card (1200×630)
  founder-portrait.svg        hand-drawn "third eye" portrait plate (not AI)
  destinations/<slug>/
    hero.jpg                  wide crop, used by the destination page hero
    card.jpg                  portrait crop, used by listing cards
  signature/<entry>-hero.jpg  wide crop for the signature entry page hero
  signature/<entry>-card.jpg  portrait crop for the homepage card
  weddings/                   section heroes (vaidik, destination, concepts…)
  vaidik/                     Vaidik hero + satvik dining
  about/                      about, story, philosophy, vision, founder
  ip/                         one hero per owned event IP
  production/                 one hero per production service
  contact-hero.jpg
  CREDITS.md                  provenance for every asset
```

Venue pages reuse their destination's hero, so 37 venue pages inherit imagery
without 37 more files.

## Why generated, not sourced

The previous set came from Wikimedia Commons — licence-clean and free, but
Commons is a keyword index rather than a visual search. The picks were routinely
off-brand: a Giovanni Boldini oil painting as the founder hero, a 1925 Charlie
Chaplin still for Feature Films, an anti-Putin rally in Moscow for Political &
Public, a Canon lens product shot for Branded Content. See
`scripts/IMAGE_RULESET.md` for the full post-mortem.

Generation replaces that with art direction we control.

## How the set is made

Two scripts, run in order:

```bash
python scripts/cf_generate.py     # 56 prompts -> /tmp/imgwork/gen/
python scripts/apply_generated.py # crop, resize, compress -> public/, credits
```

`cf_generate.py` calls Cloudflare Workers AI directly (`flux-2-klein-4b`) using
the OAuth token `wrangler login` already stored. No API key, no per-image cost —
Workers AI includes 10,000 Neurons/day free, which is roughly 60–75 images.

Each prompt is written from the page copy it sits beside, not from a category
label — read the docstring in `cf_generate.py` for why that distinction is the
whole point. Every prompt shares one house style so 56 separate generations read
as a single commissioned shoot.

Generation is resumable, and `--only <slot> [<slot>…]` regenerates specific
frames:

```bash
python scripts/cf_generate.py --only dest-kyoto            # one hero
python scripts/cf_generate.py --only card-dest-kyoto       # one card
python scripts/cf_generate.py --force --only sig-shiva-entry
```

Contact sheets for visual review land in `/tmp/imgwork/gen-sheets/`.

## Replacing an image

Every page references these paths directly, so a commissioned photograph can be
dropped over any file without touching code — keep the filename and the aspect
ratio and the layout holds.

Wide heroes are 16:9; listing cards are 3:4. Cards are composed for portrait
rather than cropped from the hero, so replacing a destination means replacing
two files.

**If you commission real photography, remove the corresponding row from
`CREDITS.md`.** That file is the disclosure record.

## Disclosure

The images are illustrative of the kind of work Third Eye Events does. They must
not be presented as a record of past events. Prompts deliberately avoid
recognisable faces: where people appear they are silhouetted, seen from behind,
or out of focus. There is no AI-generated portrait of the founder — if a real
founder photograph is needed, it has to be supplied.

## Licensing

Generated output from Workers AI is not subject to the source licences that
governed the Commons set, so no attribution obligations attach. Provenance is
still recorded in `CREDITS.md`.
