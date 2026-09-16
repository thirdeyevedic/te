#!/usr/bin/env python3
"""
image_manifest — every photographic slot on the site, with the art-direction
brief used to source it.

CONTEXT-GROUNDED REWRITE
------------------------
Every slot now carries a `context` field: the exact page headline / statement /
section copy the image sits beside. The `ov` / `commons` / `flickr` queries are
derived from THAT copy, not from a generic subject word. This is the fix for the
earlier "images not related to the page" problem — see scripts/IMAGE_RULESET.md.

Each slot carries the brief in three forms, because the three sources answer
different kinds of question:

  ov      — one Openverse query. Openverse fronts curated stock collections
            (Rawpixel, StockSnap) that are strong on concepts: decor, dining,
            stages, studios. Rate-limited, so exactly one query per slot.
  commons — Wikimedia Commons queries. Strong on real places, landmarks,
            architecture, landscape, temples, ceremonies. We also pull the
            "Quality images" subset of each query (see source_images.py), so the
            pick leans toward professionally shot, high-res photography.
  flickr  — a Flickr tag, for extra community photography on the same subject.
            The Flickr public feed returns the 20 most *recent* tagged photos, so
            it is the weakest source and kept only as enrichment.

Every source is restricted to CC0 / public-domain / CC-BY / CC-BY-SA — i.e.
commercially usable with attribution. Attribution is written to
public/images/CREDITS.md.

Note on queries: Wikimedia Commons is a keyword index, not a visual search, so
short generic words collide badly ("stage" returns bicycle-race stages, "film"
returns wildlife). Queries here are deliberately two-to-four concrete nouns taken
from the page copy.
"""

MANIFEST = [
    # ── Homepage ────────────────────────────────────────────────────────────
    dict(
        slot="hero-cinematic",
        supplied=True,  # SUPPLIED — real photograph, see sig-shiva-entry
        # Home hero — brand promise "You dream it. We bring it to life — with
        # trust." The single image that must read as *luxury events* at a glance,
        # without naming one specific ceremony. Grand illuminated heritage
        # architecture says "event production at scale" better than any other
        # keyless source photographs anything.
        context="Home hero — 'You dream it. We bring it to life — with trust.' Must read as luxury events at a glance.",
        places=True,
        out="images/hero-cinematic.jpg",
        aspect=(16, 9),
        width=1920,
        ov="illuminated indian palace architecture night heritage luxury",
        commons=[
            "Udaipur City Palace night illuminated",
            "Rajasthan palace courtyard arches",
            "Indian heritage palace facade evening",
        ],
        flickr=["indianpalace", "udaipur", "rajasthanpalace"],
    ),
    # ── Destinations (7 heroes — all *place* slots) ────────────────────────
    dict(
        slot="dest-maldives",
        places=True,
        context="Maldives — 'Ocean silence. Sky infinity.' Turquoise lagoons, private overwater islands.",
        out="images/destinations/maldives/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="maldives overwater villa turquoise lagoon resort",
        commons=[
            "Maldives overwater bungalow resort",
            "Maldives aerial turquoise lagoon",
            "Maldives beach palm island sunset",
        ],
        flickr="maldives",
    ),
    dict(
        slot="dest-rajasthan",
        places=True,
        context="Rajasthan — 'Where royal memory is still alive.' Lake palaces, golden dunes, forts.",
        out="images/destinations/rajasthan/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="udaipur city palace lake palace rajasthan heritage",
        commons=[
            "Udaipur Lake Palace monsoon",
            "Jaipur Amber Fort Rajasthan",
            "Jodhpur Mehrangarh Fort blue",
        ],
        flickr="rajasthan",
    ),
    dict(
        slot="dest-switzerland",
        places=True,
        context="Switzerland — 'Fire meets ice. Vows meet silence.' Glaciated peaks, Matterhorn.",
        out="images/destinations/switzerland/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="matterhorn zermatt alpine snow peak switzerland",
        commons=[
            "Matterhorn Zermatt Switzerland",
            "Swiss Alps glacier mountain",
            "Zermatt village Matterhorn snow",
        ],
        flickr="swissalps",
    ),
    dict(
        slot="dest-kyoto",
        places=True,
        context="Kyoto — 'Precision as devotion.' Vermilion torii gates, bamboo, temples.",
        out="images/destinations/kyoto/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="fushimi inari torii gates kyoto japan",
        commons=[
            "Fushimi Inari torii gates Kyoto",
            "Arashiyama bamboo grove Kyoto",
            "Kyoto temple garden Japan",
        ],
        flickr="kyoto",
    ),
    dict(
        slot="dest-italy",
        places=True,
        context="Italy — 'La dolce vita, sacred.' Lake villas, cypress, Amalfi cliffs.",
        out="images/destinations/italy/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="lake como italy villa cypress mountains",
        commons=[
            "Lake Como villa Bellagio",
            "Tuscany cypress hills landscape",
            "Amalfi coast cliff village",
        ],
        flickr="lakecomo",
    ),
    dict(
        slot="dest-bali",
        places=True,
        context="Bali — 'Island of the gods.' Cliff temples, rice terraces.",
        out="images/destinations/bali/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="bali uluwatu temple cliff sunset indonesia",
        commons=[
            "Pura Uluwatu Bali cliff temple",
            "Bali Tegallalang rice terrace",
            "Balinese temple gate Indonesia",
        ],
        flickr="bali",
    ),
    dict(
        slot="dest-cruises",
        places=True,
        context="Cruises — 'A world that moves with you.' Ocean horizons, luxury liner.",
        out="images/destinations/cruises/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="luxury cruise ship ocean sunset horizon",
        commons=[
            "cruise ship at sea sunset",
            "cruise liner ocean horizon",
            "cruise ship deck ocean",
        ],
        flickr="cruiseship",
    ),
    # ── Signature entries (4 — driven by their descriptors) ─────────────────
    dict(
        slot="sig-shiva-entry",
        # SUPPLIED — a real photograph placed by scripts/place_supplied.py.
        # `supplied=True` keeps cf_generate.py off it: a generation run must not
        # overwrite a frame the client chose. Drop the flag to make it
        # generatable again.
        supplied=True,
        context="Shiva Entry — 'A powerful beginning, where energy takes form.' Smoke, beats, blue+gold light, damru, trishul.",
        out="images/signature/shiva-entry-hero.jpg",
        aspect=(16, 9),
        width=1600,
        # The descriptor wants energy and form, not a calm portrait. A Nataraja
        # (dancing Shiva) bronze captures raw spiritual intensity and is far
        # better documented on Commons than any stock groom.
        ov="nataraja dancing shiva bronze statue",
        commons=["Nataraja bronze Shiva dancing", "Shiva statue temple India", "Shiva lingam temple smoke"],
        flickr=["nataraja", "shivastatue", "hindutemple"],
    ),
    dict(
        slot="sig-royal-entry",
        supplied=True,  # SUPPLIED — see sig-shiva-entry
        context="Royal Entry — 'Walk the path of kings.' Golden pathway, florals, shehnai, palace.",
        out="images/signature/royal-entry-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="indian palace corridor golden arches heritage interior",
        commons=[
            "Udaipur City Palace corridor",
            "Rajasthan palace courtyard arches",
            "Jaipur palace jharokha facade",
        ],
        flickr=["udaipur", "palaceindia", "rajasthanpalace"],
    ),
    dict(
        slot="sig-floral-entry",
        supplied=True,  # SUPPLIED — see sig-shiva-entry
        context="Floral Entry — 'love celebrated like a festival.' Petals, phoolon ki baarish, dancers.",
        out="images/signature/floral-entry-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="marigold flower petals wedding decoration india",
        commons=[
            "marigold garland flower decoration",
            "flower petals wedding decoration india",
            "floral canopy wedding india",
        ],
        flickr=["marigold", "flowergarland", "indianweddingdecor"],
    ),
    dict(
        slot="sig-celestial-entry",
        supplied=True,  # SUPPLIED — see sig-shiva-entry
        context="Celestial Entry — 'a descent from the divine.' Mist, light beams, shankh, temple bells, diya.",
        out="images/signature/celestial-entry-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="oil lamps diya row temple night glow india",
        commons=[
            "diya oil lamps row temple",
            "temple lamps night India",
            "oil lamps festival diwali",
        ],
        flickr=["diya", "templelamps", "oilamp"],
    ),
    # ── Weddings section (5) ────────────────────────────────────────────────
    dict(
        slot="weddings-index",
        context="Weddings hub — 'Where celebration becomes experience. Not coordination. Composition.'",
        out="images/weddings/index-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="indian wedding ceremony couple ritual hindu",
        commons=["Indian wedding ceremony", "Hindu wedding ritual mandap", "Indian bride groom wedding"],
        flickr="indianwedding",
    ),
    dict(
        slot="weddings-vaidik",
        context="Vaidik — 'Marriage is not an Event… but a Sacred Sanskar.' PURE: no alcohol, no non-veg, Satvik.",
        out="images/weddings/vaidik-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="homa havan sacred fire ritual hindu ceremony",
        commons=["Havan kund fire ritual", "Hindu homa fire ceremony", "vedic fire ritual wedding"],
        flickr=["havan", "homa", "vaidik"],
    ),
    dict(
        slot="weddings-destination",
        context="Destination weddings — 'From dream destinations to divine celebrations. We translate it into a new landscape.'",
        out="images/weddings/destination-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="beach wedding mandap ceremony tropical ocean",
        commons=["beach wedding ceremony setup", "destination wedding beach mandap", "outdoor wedding decoration"],
        flickr="beachwedding",
    ),
    dict(
        slot="weddings-concepts",
        context="Wedding concepts — 'Locations are common. Concepts create emotion.'",
        out="images/weddings/concepts-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="indian wedding mandap decoration flowers luxury",
        commons=["wedding mandap decorated flowers", "luxury wedding mandap decor", "marriage hall floral decoration"],
        flickr=["mandap", "weddingmandap"],
    ),
    dict(
        slot="weddings-experiences",
        context="Signature experiences — 'Moments that define the wedding before it begins.' (Baraat / groom's entry procession). Must read as a wedding procession, NOT a concert.",
        out="images/weddings/experiences-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="indian wedding baraat groom on white horse with dancers and dhol band procession street celebration turban sherwani",
        commons=[
            "Indian baraat groom white horse turban procession",
            "Indian wedding groom on horse with family dancing",
            "Punjabi wedding baraat dhol procession groom",
        ],
        flickr=["baraat", "indianweddingb", "groomhorse"],
    ),
    # ── Vaidik (2) ──────────────────────────────────────────────────────────
    dict(
        slot="vaidik-pure",
        supplied=True,  # SUPPLIED — real photograph, see sig-shiva-entry
        context="Vaidik PURE — 'No Alcohol · No Non-Veg · Pure Satvik.' The philosophy of purity (NOT a feast — that is vaidik-dining).",
        out="images/vaidik/pure-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="lotus flower water white purity minimal",
        commons=["white lotus flower water", "indian ritual pure offerings", "tulsi plant puja"],
        flickr=["lotus", "puja", "satvik"],
    ),
    dict(
        slot="vaidik-dining",
        supplied=True,  # SUPPLIED — real photograph, see sig-shiva-entry
        context="Satvik dining — 'Crafted with Intention. Served with Tradition.' Tamra Patra copper, banana leaf, Jain Satvik.",
        out="images/vaidik/satvik-dining-copper.jpg",
        aspect=(16, 9),
        width=1600,
        ov="indian thali vegetarian meal copper banana leaf",
        commons=["Indian thali vegetarian copper", "banana leaf meal south india", "satvik thali vegetarian"],
        flickr=["indianfood", "thali", "satvikfood"],
    ),
    # The dining section shows three frames, not one — the two below join
    # `vaidik-dining` above. Registered so the paths exist and are protected from
    # generation; the page composes them as a set.
    dict(
        slot="vaidik-dining-banana-leaf",
        supplied=True,
        context="Satvik dining — Banana Leaf. 'The South Indian purity format — meals served on fresh banana leaves.'",
        out="images/vaidik/satvik-dining-banana-leaf.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="vaidik-dining-seasonal",
        supplied=True,
        context="Satvik dining — Modern Satvik. 'Contemporary plating with the same discipline — seasonal ingredients.'",
        out="images/vaidik/satvik-dining-seasonal.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    # ── About (6) ───────────────────────────────────────────────────────────
    dict(
        slot="about-index",
        context="About — 'Not built on events. Built on vision. From struggle to stage. From stage to scale. From scale to purpose.'",
        out="images/about/hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="grand theatre auditorium interior stage",
        commons=["opera house auditorium interior", "theatre stage interior", "concert hall auditorium"],
        flickr="operahouse",
    ),
    dict(
        slot="about-dance",
        context="Archival — founder Gautam GS is a trained dancer/choreographer. Indian classical dance heritage.",
        out="images/about/archival-dance.jpg",
        aspect=(4, 5),
        width=900,
        ov="indian classical dancer performance bharatanatyam costume",
        commons=["Bharatanatyam dancer performance", "Indian classical dance recital", "Kathak dancer performance"],
        flickr=["bharatanatyam", "indianclassicaldance", "kathak"],
    ),
    dict(
        slot="about-story",
        context="Founder's story — 'From struggle to stage…' A journey from dancer to entrepreneur. Stage/spotlight, not a decorative pattern.",
        out="images/about/story-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="theatre stage spotlight performer silhouette",
        commons=["theatre stage spotlight", "spotlight stage performer", "empty theatre stage curtains"],
        flickr=["theatrestage", "spotlight", "stage"],
    ),
    dict(
        slot="about-philosophy",
        context="Philosophy — 'Meaning over decoration. Emotion over performance.' A single calm flame (meaning), explicitly NOT busy decoration.",
        out="images/about/philosophy-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="single oil lamp diya flame dark calm minimal",
        commons=["single diya oil lamp flame", "oil lamp dark background", "meditative lamp flame"],
        flickr=["diya", "oilamp", "meditation"],
    ),
    dict(
        slot="about-vision",
        context="Vision — 'Not built on events. Built on purpose.' A far horizon / summit.",
        out="images/about/vision-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="himalaya mountain range sunrise summit",
        commons=["Himalaya mountains sunrise", "snow peaks mountain range dawn", "mountain summit clouds"],
        flickr=["himalayas", "mountainrange"],
    ),
    dict(
        slot="about-founder",
        # SUPPLIED — the real photograph of Gautam GS, placed by
        # scripts/place_supplied.py. This is the one slot the pipeline must never
        # invent: generating a portrait of a real, named person would fabricate a
        # likeness. `supplied=True` makes cf_generate.py skip it even under
        # --force. The brief's companion slot `archival-mumbai` (a fabricated
        # 1990s photo of the founder) remains unregistered for the same reason.
        supplied=True,
        context="Founder Gautam GS — Director · Choreographer · Designer · Visionary. A working creative lead (rehearsal/direction), not just equipment.",
        out="images/about/founder-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="dance rehearsal studio choreographer instructing dancers",
        commons=["dance rehearsal studio", "choreographer teaching dancers", "theatre director rehearsal"],
        flickr=["dancerehearsal", "choreography", "rehearsal"],
    ),
    # ── Destinations section (2) ────────────────────────────────────────────
    dict(
        slot="destinations-index",
        places=True,
        context="Destinations hub — 'Different worlds. One standard.' Experience systems composed of landscape, culture, concept, ritual.",
        out="images/destinations/index-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="tropical island aerial turquoise lagoon paradise",
        commons=["tropical island aerial lagoon", "overwater resort aerial", "private island beach aerial"],
        flickr=["aerialisland", "tropicalisland"],
    ),
    dict(
        slot="destinations-india",
        places=True,
        context="India destinations — 'One country. Seven worlds.' Royal heritage, desert, forests, coasts, mountains, spiritual, metro.",
        out="images/destinations/india-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="taj mahal agra india sunrise monument",
        commons=["Taj Mahal Agra sunrise", "India palace heritage", "Varanasi ghats Ganges"],
        flickr="tajmahal",
    ),
    # ── Event IP (11 — each states its own line) ───────────────────────────
    dict(
        slot="ip-index",
        context="Event IP hub — 'An ecosystem of signature experiences. Owned. Designed. Delivered by Third Eye.' → a produced spectacle, not a random crowd.",
        out="images/ip/index-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="grand event stage production spectacular lights",
        commons=["concert stage production lights", "spectacular stage show lights", "event production stage"],
        flickr=["stageshow", "eventsproduction", "productionshow"],
    ),
    dict(
        slot="ip-exhibitions",
        context="Exhibitions — 'Industry platforms where Third Eye designs entire exhibition worlds.'",
        out="images/ip/exhibitions-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="museum exhibition gallery interior display",
        commons=["museum exhibition gallery", "art exhibition stand design", "exhibition booth design"],
        flickr=["exhibitiongallery", "museumexhibition"],
    ),
    dict(
        slot="ip-automotive",
        context="Automotive & Mobility — 'Vehicles presented as protagonists.'",
        out="images/ip/automotive-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="luxury sports car showroom studio lighting",
        commons=["auto show car exhibition", "luxury car showroom", "motor show supercar"],
        flickr="autoshow",
    ),
    dict(
        slot="ip-awards",
        context="Awards & Gala — 'Ceremonies engineered for gravity.'",
        out="images/ip/awards-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="awards ceremony stage trophy gala presentation",
        commons=["award ceremony stage", "gala awards stage", "red carpet awards"],
        flickr=["awards", "gala", "awardceremony"],
    ),
    dict(
        slot="ip-products",
        context="Best Products of India — 'products staged with the respect of museum curation' / 'Celebrating Indian excellence.'",
        out="images/ip/best-products-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="premium product display exhibition showcase",
        commons=["product launch display stand", "exhibition product showcase", "retail display premium"],
        flickr=["productdisplay", "shopdisplay"],
    ),
    dict(
        slot="ip-sports",
        context="Sports Leagues — 'League formats owned end to end' / 'Competition meets community.'",
        out="images/ip/sports-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="stadium floodlights night sport arena",
        commons=["stadium floodlights night", "sports arena crowd", "cricket stadium floodlights"],
        flickr="stadium",
    ),
    dict(
        slot="ip-fashion",
        context="Fashion & Modeling — 'Runways and model platforms directed like cinema' / 'Movement as image-making.'",
        out="images/ip/fashion-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="fashion week runway model catwalk",
        commons=["fashion week runway", "catwalk fashion model", "fashion show runway lights"],
        flickr=["fashionweek", "catwalk", "runway"],
    ),
    dict(
        slot="ip-political",
        context="Political & Public — 'Large-scale public gatherings… crowd architecture, security coordination' / 'Scale management meets protocol discipline.'",
        out="images/ip/political-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="large public gathering crowd india rally",
        commons=["political rally crowd india", "public meeting gathering", "election campaign rally"],
        flickr=["politicalrally", "publicgathering"],
    ),
    dict(
        slot="ip-devotional",
        places=True,
        context="Devotional & Spiritual — 'Sacred gatherings produced with reverence' / 'Devotion over spectacle.'",
        out="images/ip/devotional-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="temple aarti ceremony lamps devotees india",
        commons=["Ganga aarti Varanasi ceremony", "temple aarti ceremony lamps", "devotional lamps india"],
        flickr=["aarti", "temple", "devotion"],
    ),
    dict(
        slot="ip-concerts",
        context="Concerts & Live — 'Live entertainment as total environment' / 'Total environment. Total energy.'",
        out="images/ip/concerts-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="concert stage lights crowd silhouette night music",
        commons=["concert stage lights crowd", "live music performance stage", "music concert crowd night"],
        flickr=["concert", "livemusic"],
    ),
    # ── Production (8) ──────────────────────────────────────────────────────
    dict(
        slot="production-index",
        context="Production — 'Behind every frame. Structured. Managed. Delivered by Third Eye.'",
        out="images/production/index-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="film set cinema camera crew production equipment",
        commons=["film crew camera production", "movie set equipment", "cinema production set"],
        flickr=["filmset", "filmmaking", "cinematography"],
    ),
    dict(
        slot="production-feature-films",
        context="Feature Films — 'Long-form complexity handled on the ground.' → a MOVIE set (NOT wildlife 'film').",
        out="images/production/feature-films.jpg",
        aspect=(16, 9),
        width=1600,
        ov="movie set director clapperboard cinema crew",
        commons=["movie set clapperboard", "film director clapperboard", "motion picture set crew camera"],
        flickr=["movieset", "clapperboard", "cinematography"],
    ),
    dict(
        slot="production-short-films",
        context="Short Films — 'Small crews. Sharp turnarounds.'",
        out="images/production/short-films.jpg",
        aspect=(16, 9),
        width=1600,
        ov="camera operator filming videographer shoulder rig",
        commons=["cameraman filming shoulder rig", "video camera operator", "independent film shooting"],
        flickr=["videographer", "filmmaking", "camera"],
    ),
    dict(
        slot="production-documentaries",
        context="Documentaries — 'Reality does not reschedule. We adjust.'",
        out="images/production/documentaries.jpg",
        aspect=(16, 9),
        width=1600,
        ov="documentary filming interview camera tripod outdoors",
        commons=["documentary interview filming", "candid documentary camera", "field documentary filming"],
        flickr=["documentary", "filmmaking", "interview"],
    ),
    dict(
        slot="production-digital-content",
        context="Digital Content — 'Content pipelines that keep publishing honest.' → a recording/podcast studio (NOT a football match).",
        out="images/production/youtube-digital.jpg",
        aspect=(16, 9),
        width=1600,
        ov="recording studio microphone podcast desk",
        commons=["recording studio microphone", "podcast studio desk", "video production studio"],
        flickr=["podcaststudio", "recordingstudio", "videostudio"],
    ),
    dict(
        slot="production-branded-content",
        context="Branded Content — 'The brand's voice, protected frame by frame.' → brand / content studio.",
        out="images/production/branded-content.jpg",
        aspect=(16, 9),
        width=1600,
        ov="video content studio creator filming brand",
        commons=["content studio filming", "social media video production", "brand video shoot"],
        flickr=["contentstudio", "videoproduction", "brandcontent"],
    ),
    dict(
        slot="production-ad-shoots",
        context="Ad Shoots — 'One day. Every department on time.'",
        out="images/production/ad-shoots.jpg",
        aspect=(16, 9),
        width=1600,
        ov="film set lighting softbox studio equipment rig",
        commons=["studio lighting softbox", "advertising photo shoot set", "film set lighting rig"],
        flickr=["studiolighting", "advertising", "filmset"],
    ),
    # ── Contact (1) ─────────────────────────────────────────────────────────
    dict(
        slot="contact",
        context="Contact — 'Every celebration has a beginning.' → an elegant celebration table setting (the start of a celebration), not generic dining.",
        out="images/contact-hero.jpg",
        aspect=(16, 9),
        width=1600,
        ov="elegant celebration table setting flowers evening luxury",
        commons=["luxury wedding table setting", "elegant banquet table flowers", "celebration dinner table setting"],
        flickr=["tablesetting", "banquet", "eventdecor"],
    ),

    # ── Cinematic scroll hero journey (NEW — section not yet built) ─────────
    # These four belong to a scroll-driven hero sequence described in the client
    # brief (threshold -> invocation -> anticipation -> revelation).
    #
    # IMPORTANT: no such section exists yet. src/components/OpeningSequence.astro
    # is text-only (ॐ + a Sanskrit mantra) and nothing in src/ references
    # images/cinematic/. The slots are registered so the images can be produced
    # the moment the section is written — until then they are unreferenced files.
    # Full-bleed, so they take the 1920 cinematic size (see cf_generate.py).
    #
    # Marked `opt_in` because nothing references them yet and they are the most
    # expensive slots in the set (9 billing tiles each). They are skipped by a
    # default run; generate with `--extras` or `--only <slot>`.
    dict(
        slot="cinematic-beat1-threshold",
        opt_in=True,
        context="Scroll hero beat 1 — crossing the threshold. Dark corridor to lit hall.",
        out="images/cinematic/cinematic-beat1-threshold.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="cinematic-beat2-invocation",
        opt_in=True,
        context="Scroll hero beat 2 — the mandap, the drums, the invocation.",
        out="images/cinematic/cinematic-beat2-invocation.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="cinematic-beat3-anticipation",
        opt_in=True,
        context="Scroll hero beat 3 — the bridal ensemble laid out, still life.",
        out="images/cinematic/cinematic-beat3-anticipation.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="cinematic-beat4-revelation",
        opt_in=True,
        context="Scroll hero beat 4 — the reveal, backlit in the doorway.",
        out="images/cinematic/cinematic-beat4-revelation.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),

    # ── About — additional archival / team slots (NEW) ──────────────────────
    # 4:5 to match its sibling `about-dance` (images/about/archival-dance.jpg),
    # which is the only other portrait-aspect archival slot.
    #
    # NOTE: the brief also asks for `archival-mumbai.jpg` — a 1990s photograph of
    # the founder as a young background dancer on a Mumbai film set. That slot is
    # deliberately NOT registered: it asks the model to fabricate a historical
    # photograph of a real, named person. A real photograph or nothing.
    dict(
        slot="about-team-vision",
        context="About — the team around a drafting table. 'Not built on events. Built on vision.'",
        out="images/about/team-vision.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),

    # ── Homepage pathway cards (NEW) ────────────────────────────────────────
    # The brief asks for `public/images/pathways/*.jpg`, which does not exist.
    # The homepage pathway cards (src/pages/index.astro section 04) currently
    # read `images/weddings/{vaidik,destination,concepts}-hero.jpg` — 16:9 heroes
    # squeezed into a card of roughly 1.15:1, throwing away about a third of the
    # frame. The brief's instinct is right, and it is the same argument already
    # used for the portrait cards: compose FOR the card instead of cropping a hero.
    #
    # Registered at the brief's paths, but `opt_in` — switching the cards over is
    # a three-line change in index.astro that has not been made yet. Generate with
    # `--only pathways-vaidik` (etc.) once it has.
    dict(
        slot="pathways-vaidik",
        opt_in=True,
        context="Homepage pathway card 01 — Vaidik. 'Sacred. Pure. Conscious.'",
        out="images/pathways/vaidik.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="pathways-destination",
        opt_in=True,
        context="Homepage pathway card 02 — Destination. 'Different locations. Different worlds.'",
        out="images/pathways/destination.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
    dict(
        slot="pathways-concepts",
        opt_in=True,
        context="Homepage pathway card 03 — Concepts. 'Experiences designed around meaning.'",
        out="images/pathways/concepts.jpg",
        aspect=(16, 9),
        width=1600,
        ov="", commons=[], flickr=[],
    ),
]

# ── Supplied photography ────────────────────────────────────────────────────
# Slots backed by a real photograph rather than a generation. `cf_generate.py`
# skips any slot carrying `supplied=True`, even under --force and --extras, so a
# generation run can never overwrite a frame the client chose — or, for the
# founder, a real person's likeness.
#
# Applied centrally so the complete list is visible in one place. A few slots
# also carry an inline flag next to their brief, where the reason is specific
# enough to be worth stating at the point of use.
#
#   scripts/place_client_set.py  — the 32-image client set (image-to-slot map)
#   scripts/place_supplied.py    — founder, Signature Entry cards, earlier frames
SUPPLIED_SLOTS = {
    # Homepage
    "hero-cinematic",
    # Signature Entries
    "sig-shiva-entry", "sig-royal-entry", "sig-floral-entry", "sig-celestial-entry",
    # Destinations
    "dest-maldives", "dest-rajasthan", "dest-switzerland", "dest-kyoto",
    "dest-italy", "dest-bali", "dest-cruises",
    # Event IP
    "ip-automotive", "ip-awards", "ip-products", "ip-concerts", "ip-devotional",
    "ip-exhibitions", "ip-fashion", "ip-political", "ip-sports",
    # Production
    "production-feature-films", "production-short-films", "production-documentaries",
    "production-digital-content", "production-branded-content", "production-ad-shoots",
    # Vaidik + founder
    "vaidik-pure", "vaidik-dining", "vaidik-dining-banana-leaf",
    "vaidik-dining-seasonal", "about-founder",
    # Weddings
    "weddings-experiences",
}

for _entry in MANIFEST:
    if _entry["slot"] in SUPPLIED_SLOTS:
        _entry["supplied"] = True

# Portrait cards backed by supplied imagery.
#
# This is a SEPARATE set from SUPPLIED_SLOTS on purpose. CARD_DERIVATIONS keys
# each card by the slot of its wide hero, so "the hero is supplied" does not by
# itself mean "the card is supplied". Only the four Signature Entry cards are:
# two were placed from supplied portraits, two were derived from supplied
# heroes. The seven destination cards are still the previous generation and
# remain regenerable, so they can be brought back in line with the new heroes.
SUPPLIED_CARDS = {
    "sig-shiva-entry",
    "sig-royal-entry",
    "sig-floral-entry",
    "sig-celestial-entry",
}

# Portrait cards re-cropped from the same source as the wide hero.
CARD_DERIVATIONS = [
    ("dest-maldives", "images/destinations/maldives/card.jpg"),
    ("dest-rajasthan", "images/destinations/rajasthan/card.jpg"),
    ("dest-switzerland", "images/destinations/switzerland/card.jpg"),
    ("dest-kyoto", "images/destinations/kyoto/card.jpg"),
    ("dest-italy", "images/destinations/italy/card.jpg"),
    ("dest-bali", "images/destinations/bali/card.jpg"),
    ("dest-cruises", "images/destinations/cruises/card.jpg"),
    ("sig-shiva-entry", "images/signature/shiva-entry-card.jpg"),
    ("sig-royal-entry", "images/signature/royal-entry-card.jpg"),
    ("sig-floral-entry", "images/signature/floral-entry-card.jpg"),
    ("sig-celestial-entry", "images/signature/celestial-entry-card.jpg"),
]

CARD_ASPECT = (3, 4)
CARD_WIDTH = 900
