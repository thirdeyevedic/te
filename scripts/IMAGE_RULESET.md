# Image Placement Ruleset — Third Eye Events

**Why this exists.** Earlier image sourcing used short, subject-only queries
("film", "wedding") that were not read against the page copy. Wikimedia Commons
is a keyword index, not a visual search, so generic words returned off-topic or
low-quality results (a frog for Feature Films, a football team for YouTube
Content, a Western model in borrowed styling for an Indian wedding). This ruleset
fixes that by making every query derive from the *actual words on the page* and
by holding a single quality bar across all 56 assets.

---

## The 4-step method (mandatory, in order)

For **every** slot, before any query is written:

1. **Analyze the page.** Read the page's hero title, statement, and the section
   copy the image sits beside. Capture the *one idea* the image must carry.
2. **Analyze the image requirement.** Is it a *place* (a real destination/venue),
   a *ritual* (a ceremony moment), a *craft* (production/staging), or a
   *concept* (an abstract brand idea)? Place and ritual slots want real nouns
   Commons photographs well; concept slots want concrete, depictable nouns, not
   adjectives.
3. **Write the prompt from the copy.** Each `commons` query is 2–4 concrete
   nouns taken from the page copy. Each `ov` query is the editorial/concept
   phrasing. Each `flickr` tag is the community synonym.
4. **Generate / source, then verify.** Source candidates, then confirm the
   picked asset against the page copy in a headless-Chrome screenshot. If it
   does not match the idea in step 1, override the pick.

---

## Brand & quality bar

- **Licence-clean only.** CC0 / public domain / CC BY / CC BY-SA. Attribution
  written to `public/images/CREDITS.md`.
- **Commons-led.** Wikimedia Commons is the strongest source for real places,
  ceremonies, architecture and craft, and is effectively unlimited. Openverse
  fronts curated stock (good for editorial concepts) but rate-limits hard.
  Flickr's public tag feed returns the 20 most *recent* tagged photos and is the
  weakest — kept only as enrichment, never the deciding source.
- **Quality bias.** For every slot we now also pull the Commons
  `Quality images` subset of the same query, so the pick leans toward
  professionally shot, high-resolution photography — essential for a luxury
  brand. Larger, correctly-proportioned candidates win; undersized files are
  demoted (they would ship soft at hero size).
- **No off-topic, no costume.** Reject Western models in "borrowed" Indian
  styling, wildlife that collided with a generic word, and sports/stock that
  matched a loosely-related term. The contact sheet (`/tmp/imgwork/sheets/`) and
  the final montage (`FINAL-all-assets.jpg`) are the audit trail.
- **One photograph, one site.** A frame must not appear twice (cross-slot
  de-dup in `apply_images.py`).

---

## Per-section requirements (copy → image meaning)

### Homepage
- **hero-cinematic** — Copy: *"You dream it. We bring it to life — with trust."*
  Must read as luxury events at a glance. → Illuminated Indian palace / heritage
  architecture at night (grand, not a specific ceremony).

### Destinations (7 heroes + 7 cards, all *place* slots)
Each hero is the destination's defining landscape, taken from its tagline:
- **Maldives** — *"Ocean silence. Sky infinity."* → overwater villas, turquoise lagoon.
- **Rajasthan** — *"Where royal memory is still alive."* → lake palaces, forts, golden dunes.
- **Switzerland** — *"Fire meets ice. Vows meet silence."* → Matterhorn / glaciated peaks.
- **Kyoto** — *"Precision as devotion."* → vermilion torii gates, bamboo.
- **Italy** — *"La dolce vita, sacred."* → lake villas, cypress, Amalfi cliffs.
- **Bali** — *"Island of the gods."* → cliff temples, rice terraces.
- **Cruises** — *"A world that moves with you."* → ocean liner on the horizon.

### Signature Entries (4, driven by their descriptors)
- **Shiva Entry** — *"A powerful beginning, where energy takes form."* Smoke,
  beats, blue+gold light, damru, trishul. → Nataraja / Shiva sculpture, energetic.
- **Royal Entry** — *"Walk the path of kings."* Golden pathway, florals, shehnai,
  palace. → palace corridor / courtyard arches.
- **Floral Entry** — *"love celebrated like a festival."* Petals, *phoolon ki
  baarish*, dancers. → marigold garlands / petal decoration.
- **Celestial Entry** — *"a descent from the divine."* Mist, light beams, shankh,
  temple bells, diya. → rows of oil lamps / temple light at night.

### Weddings (5)
- **index** — *"Where celebration becomes experience. Not coordination.
  Composition."* → a lived Indian wedding ceremony.
- **vaidik** — *"Marriage is not an Event… but a Sacred Sanskar."* PURE: no
  alcohol, no non-veg, Satvik. → homa / havan sacred fire.
- **destination** — *"From dream destinations to divine celebrations."* → beach /
  destination wedding setup.
- **concepts** — *"Locations are common. Concepts create emotion."* → decorated
  mandap / floral concept.
- **experiences** — *"Moments that define the wedding before it begins."* → baraat
  / entry procession.

### Vaidik (2)
- **pure** — *"No Alcohol · No Non-Veg · Pure Satvik."* → purity: lotus / clean
  ritual offering (not a feast — that is `dining`).
- **dining** — *"Crafted with Intention. Served with Tradition."* Tamra Patra
  copper, banana leaf, Jain Satvik. → satvik thali, copper / banana leaf.

### About (6)
- **index** — *"From struggle to stage. From stage to scale. From scale to
  purpose."* → grand auditorium / stage.
- **dance** — founder Gautam GS is a trained dancer/choreographer. → Indian
  classical dance performance.
- **story** — *"From struggle to stage…"* → stage / spotlight (journey), not a
  decorative pattern.
- **philosophy** — *"Meaning over decoration. Emotion over performance."* → a
  single calm lamp / flame (meaning), explicitly NOT busy decoration.
- **vision** — *"Built on purpose."* → far horizon / mountain summit.
- **founder** — *Director · Choreographer · Designer · Visionary.* → a working
  creative lead (rehearsal / direction), not just equipment.

### Event IP (11)
Each hero states its own line — the image must show that format owned end to end:
- **index** — *"An ecosystem of signature experiences. Owned. Designed.
  Delivered."* → a produced spectacle / staged show (not a random crowd).
- **exhibitions** — *"entire exhibition worlds."* → exhibition gallery / stand.
- **automotive** — *"Vehicles presented as protagonists."* → car on display.
- **awards** — *"Ceremonies engineered for gravity."* → awards stage / trophy.
- **products** — *"products staged with the respect of museum curation."* →
  premium product showcase.
- **sports** — *"League formats owned end to end."* → stadium / arena.
- **fashion** — *"Runways and model platforms directed like cinema."* → runway.
- **political** — *"crowd architecture, security coordination."* → large public
  gathering.
- **devotional** — *"Sacred gatherings produced with reverence."* → aarti /
  temple devotion.
- **concerts** — *"Live entertainment as total environment."* → concert stage.

### Production (8)
- **index** — *"Behind every frame."* → film set / crew.
- **feature-films** — *"Long-form complexity handled on the ground."* → movie
  set with clapperboard (NOT wildlife "film").
- **short-films** — *"Small crews. Sharp turnarounds."* → camera operator.
- **documentaries** — *"Reality does not reschedule. We adjust."* → field
  interview / documentary camera.
- **digital-content** — *"Content pipelines that keep publishing honest."* →
  recording / podcast studio (NOT a football match).
- **branded-content** — *"The brand's voice, protected frame by frame."* → brand
  / content studio.
- **ad-shoots** — *"One day. Every department on time."* → studio lighting rig.

### Contact (1)
- **contact** — *"Every celebration has a beginning."* → an elegant celebration
  table setting (the start of a celebration), not generic dining.

---

## Verification gate

After sourcing, every key page is screenshotted with headless Chrome
(`--force-prefers-reduced-motion`, `--virtual-time-budget=12000`,
`--window-size=1440,5600`). Each hero/card is checked against its requirement
above. Any mismatch is fixed via `overrides.json` (`{"slot-id": candidate_index}`)
and `apply_images.py` is re-run. The site is built only after the gate passes.
