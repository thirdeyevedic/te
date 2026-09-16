/**
 * VENUE EXPERIENCES — the named-concept venues.
 * One page per venue that carries its own Vedic concept (§63 information gain).
 * Content derives from supplied concept meanings and country contexts.
 */

export interface VenueExperience {
  slug: string;
  countrySlug: string;
  countryName: string;
  name: string;
  concept: string;
  meaning: string;
  tagline: string;
  whyVenue: string;
  interpretation: string;
  ritualDirection: string;
  experienceDesign: string;
  signatureMoments: string[];
  bestFor: string[];
  seoTitle: string;
  metaDescription: string;
}

export const venueExperiences: VenueExperience[] = [
  {
    slug: "soneva-fushi",
    countrySlug: "maldives",
    countryName: "Maldives",
    name: "Soneva Fushi",
    concept: "Prakriti Vivaah",
    meaning: "Union within nature — the wild as witness.",
    tagline: "The island itself officiates.",
    whyVenue:
      "A private island where jungle meets an empty lagoon — no roads, no shoes, no noise. Nature sets every schedule here.",
    interpretation:
      "We let the wild be witness. Ceremony is woven into forest and shore without ornament — Prakriti needs no decoration.",
    ritualDirection:
      "The mandapa stands between jungle and sea; Agni is lit at the water's edge so sunrise enters the ritual itself.",
    experienceDesign:
      "Barefoot processions on sand paths, meals under canopy, and pheras held to the rhythm of tide rather than clock.",
    signatureMoments: [
      "Sunrise sankalp spoken over the lagoon",
      "Sand-path baraat beneath palm shade",
      "Canopy satvik dinner lit by oil lamps",
      "Night close under an unbroken field of stars",
    ],
    bestFor: ["Intimate guest lists", "Nature-first couples", "Absolute privacy"],
    seoTitle: "Prakriti Vivaah at Soneva Fushi — Maldives | Third Eye Events",
    metaDescription:
      "A Prakriti Vivaah on Soneva Fushi — union within nature on a private Maldivian island, designed and delivered by Third Eye Events.",
  },
  {
    slug: "reethi-rah",
    countrySlug: "maldives",
    countryName: "Maldives",
    name: "One&Only Reethi Rah",
    concept: "Rajsi Vivaah",
    meaning: "A royal wedding — grandeur rooted in heritage.",
    tagline: "Courtly grandeur, translated to open sea.",
    whyVenue:
      "An entire island composed like a palace estate — grand avenues, formal courtyards and generous scale within total privacy.",
    interpretation:
      "Royalty is proportion, not gold. Reethi Rah gives the wedding the scale a court deserves, surrounded by ocean instead of walls.",
    ritualDirection:
      "Processions move along palm avenues toward an oceanfront mandapa; nagada answers across open water.",
    experienceDesign:
      "Grand arrivals, courtyard celebrations and a firelit beach finale — formal, unhurried, magnificent.",
    signatureMoments: [
      "Palm-avenue royal procession at dusk",
      "Courtyard sangeet under lit colonnades",
      "Sunset ceremony on a throne-framed stage",
      "Beachside pheras ringed by flame",
    ],
    bestFor: ["Large celebrations", "Grand entrances", "Island takeovers"],
    seoTitle: "Rajsi Vivaah at One&Only Reethi Rah — Maldives | Third Eye Events",
    metaDescription:
      "A Rajsi Vivaah at One&Only Reethi Rah — royal Maldivian island grandeur designed and delivered by Third Eye Events.",
  },
  {
    slug: "taj-exotica",
    countrySlug: "maldives",
    countryName: "Maldives",
    name: "Taj Exotica Resort & Spa",
    concept: "Parampara Vivaah",
    meaning: "Tradition carried forward without dilution.",
    tagline: "Ritual unchanged. Setting renewed.",
    whyVenue:
      "Indian hospitality language on an emerald lagoon — elders feel at home while the horizon feels brand new.",
    interpretation:
      "Parampara means continuity. Every rite is conducted exactly as it would be at home — only the frame changes.",
    ritualDirection:
      "The complete Vedic sequence is preserved in full, framed by calm lagoon water and open sky.",
    experienceDesign:
      "Familiar rhythms — haldi mornings, seated rituals, elders honoured first — held gently by the sea.",
    signatureMoments: [
      "Haldi by the water's edge",
      "Traditional baraat along the jetty",
      "Elders-first ceremony seating under palms",
      "Lagoon-side vidai at last light",
    ],
    bestFor: ["Multi-generation families", "Orthodox rituals", "First-time travellers"],
    seoTitle: "Parampara Vivaah at Taj Exotica Maldives | Third Eye Events",
    metaDescription:
      "A Parampara Vivaah at Taj Exotica Resort & Spa — tradition carried whole to the Maldives, by Third Eye Events.",
  },
  {
    slug: "conrad-rangali",
    countrySlug: "maldives",
    countryName: "Maldives",
    name: "Conrad Maldives Rangali Island",
    concept: "Nakshatra Vivaah",
    meaning: "Under the constellations — cosmic timing.",
    tagline: "The night itself becomes witness.",
    whyVenue:
      "Two islands joined by a footbridge under minimal light pollution — the Maldivian sky arrives in full.",
    interpretation:
      "Muhurat is read in both shastra and stars. Here the constellations are not metaphor; they are present.",
    ritualDirection:
      "Ceremonies move to night; pheras are held under open sky, timed to celestial alignment.",
    experienceDesign:
      "Candlelight replaces chandeliers; guests look up as often as forward.",
    signatureMoments: [
      "Star-chart invitations drawn to your date",
      "Footbridge procession by candlelight",
      "Midnight mangal pheras under constellations",
      "Telescope terrace for waiting guests",
    ],
    bestFor: ["Astrology-led muhurats", "Night ceremonies", "Romantic scale"],
    seoTitle: "Nakshatra Vivaah at Conrad Rangali Maldives | Third Eye Events",
    metaDescription:
      "A Nakshatra Vivaah at Conrad Maldives Rangali — vows under the constellations, delivered by Third Eye Events.",
  },
  {
    slug: "joali",
    countrySlug: "maldives",
    countryName: "Maldives",
    name: "Joali Maldives",
    concept: "Adhyatmik Aesthetics Vivaah",
    meaning: "Spirituality expressed through artful form.",
    tagline: "Devotion, given beautiful form.",
    whyVenue:
      "An island conceived as a living art collection — sculpture, design and craft at every turn.",
    interpretation:
      "Aesthetics in service of meaning. Form expresses the sacred without ever becoming decoration.",
    ritualDirection:
      "Each rite is framed by commissioned installations — the mandapa itself composed as artwork.",
    experienceDesign:
      "Celebrations move like an exhibition — one curated space after another, each holding its own emotion.",
    signatureMoments: [
      "Artist-commissioned mandapa reveal",
      "Art-walk sangeet through the island",
      "Sculptural floral shagun presentation",
      "Gallery-styled gifting suite",
    ],
    bestFor: ["Design-led couples", "Curated detail", "Contemporary expression"],
    seoTitle: "Adhyatmik Aesthetics Vivaah at Joali Maldives | Third Eye Events",
    metaDescription:
      "An Adhyatmik Aesthetics Vivaah at Joali — spirituality expressed through artful form, by Third Eye Events.",
  },
  {
    slug: "zermatt",
    countrySlug: "switzerland",
    countryName: "Switzerland",
    name: "Zermatt",
    concept: "Agni-Him Vivaah",
    meaning: "Fire × Ice — a rare union of opposing elements.",
    tagline: "A rare union of opposing elements.",
    whyVenue:
      "A car-free alpine village beneath the Matterhorn — fire and snow share a single frame here.",
    interpretation:
      "Two opposites, one union. The homa burns against the snowfield and neither yields — the marriage mirrors the mountain.",
    ritualDirection:
      "The sacred fire is raised beside the snow; warmth of ritual held inside vast cold clarity.",
    experienceDesign:
      "Gondola arrivals, mountain-restaurant venues and heated glass chapels facing four-thousand-metre peaks.",
    signatureMoments: [
      "Gondola ascent procession",
      "Fireside vows facing the glacier",
      "Snowfall during the pheras",
      "Alpine satvik table after the fire",
    ],
    bestFor: ["Elemental contrast", "Mountain drama", "Winter dates"],
    seoTitle: "Agni-Him Vivaah in Zermatt — Fire and Ice Wedding | Third Eye Events",
    metaDescription:
      "An Agni-Him Vivaah beneath the Matterhorn in Zermatt — fire and ice in one union, by Third Eye Events.",
  },
  {
    slug: "interlaken",
    countrySlug: "switzerland",
    countryName: "Switzerland",
    name: "Interlaken",
    concept: "Panch Tatva Vivaah",
    meaning: "The five elements as wedding witnesses.",
    tagline: "Every element, present and accounted for.",
    whyVenue:
      "Between two lakes, beneath twin peaks, with a river running through — Interlaken holds all five elements in one valley.",
    interpretation:
      "Each element is honoured at its own station — the celebration becomes a pilgrimage through earth, water, fire, air and space.",
    ritualDirection:
      "Five stations map onto five events: meadow rites, lakefront blessings, an evening homa, mountain-air celebration and open-sky conclusion.",
    experienceDesign:
      "Guests travel short distances between dramatically different settings — the valley does the staging.",
    signatureMoments: [
      "Earth — meadow mandapa at noon",
      "Water — lakeside blessing at dusk",
      "Fire — evening homa against the peaks",
      "Air & space — terrace sangeet under open sky",
    ],
    bestFor: ["Multi-event weddings", "Elemental symbolism", "Mixed-age guests"],
    seoTitle: "Panch Tatva Vivaah in Interlaken — Five Elements Wedding | Third Eye Events",
    metaDescription:
      "A Panch Tatva Vivaah in Interlaken — the five elements as wedding witnesses, designed by Third Eye Events.",
  },
  {
    slug: "lauterbrunnen",
    countrySlug: "switzerland",
    countryName: "Switzerland",
    name: "Lauterbrunnen",
    concept: "Shanti Vivaah",
    meaning: "Peace as the foundation of union.",
    tagline: "The waterfalls keep the mantra.",
    whyVenue:
      "A valley of seventy-two waterfalls beneath cliff villages — falling water is the constant sound here; nothing else competes.",
    interpretation:
      "Shanti chosen as foundation. Celebration without noise-for-noise — presence over performance.",
    ritualDirection:
      "Quiet ceremonies paced to the waterfalls; acoustic sound only, amplification declined.",
    experienceDesign:
      "Long silences that hold everyone, meadow walks, and vows that need no microphone.",
    signatureMoments: [
      "Waterfall-backdrop pheras",
      "Silent meadow walk before vows",
      "Acoustic shehnai at first light",
      "Candle-lit closing circle",
    ],
    bestFor: ["Quiet luxury", "Elopement-scale", "Restorative celebrations"],
    seoTitle: "Shanti Vivaah in Lauterbrunnen — Waterfall Valley Wedding | Third Eye Events",
    metaDescription:
      "A Shanti Vivaah in Lauterbrunnen — peace as the foundation of union, in the valley of waterfalls. By Third Eye Events.",
  },
  {
    slug: "glacier-express",
    countrySlug: "switzerland",
    countryName: "Switzerland",
    name: "Glacier Express",
    concept: "Jeevan Yatra Vivaah",
    meaning: "Marriage as the beginning of life's journey.",
    tagline: "The journey is the ceremony.",
    whyVenue:
      "Eight hours of panoramic rail through the high Alps — a moving world where movement itself becomes meaning.",
    interpretation:
      "Marriage framed as yatra. The celebration travels carriage by carriage toward its destination — together the entire way.",
    ritualDirection:
      "Chartered carriages host the rites en route; vows are exchanged at the journey's highest point.",
    experienceDesign:
      "Station send-off, rolling lunches, window-seat rituals — logistics choreographed to the timetable.",
    signatureMoments: [
      "Station send-off baraat on the platform",
      "Vintage-wagon seated lunch",
      "Garland exchange against panoramic windows",
      "Arrival-station reception in the mountains",
    ],
bestFor: ["Journey narratives", "Rail romantics", "Compact guest lists"],
    seoTitle: "Jeevan Yatra Vivaah aboard the Glacier Express | Third Eye Events",
    metaDescription:
      "A Jeevan Yatra Vivaah aboard the Glacier Express — marriage as the beginning of the journey, by Third Eye Events.",
  },
  {
    slug: "st-moritz",
    countrySlug: "switzerland",
    countryName: "Switzerland",
    name: "St. Moritz",
    concept: "Shwet Rajsi Vivaah",
    meaning: "White Royal Wedding",
    tagline: "Purity, precision and alpine sophistication.",
    whyVenue:
      "Playground of billionaires and royalty with ultra-luxury hotels like Badrutt's Palace, offering winter elegance at its peak.",
    interpretation:
      "White-themed mandaps reflect purity and clarity, while indoor-outdoor balance provides comfort without sacrificing connection to nature. Royal discipline ensures precision over chaos.",
    ritualDirection:
      "Ceremonies follow precise timing with white floral aesthetics, sacred fire in snow landscapes, and rituals conducted with royal discipline and attention to detail.",
    experienceDesign:
      "Indoor-outdoor flow for guest comfort, white and silver aesthetics, premium hospitality service, and rituals that maintain solemnity despite luxurious surroundings.",
    signatureMoments: [
      "White mandap against alpine backdrop",
      "Sacred fire ceremony in snow landscape",
      "White-themed reception with alpine elegance",
      "Candle-lit vows under starlit sky",
    ],
    bestFor: ["Elite luxury", "Winter weddings", "Royal sophistication"],
    seoTitle: "Shwet Rajsi Vivaah in St. Moritz | Third Eye Events",
    metaDescription:
      "A Shwet Rajsi Vivaah in St. Moritz — white royal wedding in the Swiss Alps, by Third Eye Events.",
  },
  {
    slug: "fushimi-inari",
    countrySlug: "kyoto",
    countryName: "Kyoto",
    name: "Fushimi Inari Shrine",
    concept: "Marg Darshan Vivaah",
    meaning: "The Path-Aligned Wedding",
    tagline: "Two paths become one through torii gates.",
    whyVenue:
      "Thousands of Torii gates forming a spiritual pathway that symbolizes journey, destiny and life transitions.",
    interpretation:
      "The wedding begins with a walk together through the gates — no grand entry, only intentional beginning. Rituals focus on sankalp (commitment) rather than performance.",
    ritualDirection:
      "Couple walks together through the torii gate pathway, performing sankalp at the beginning. Subsequent rituals follow naturally from this aligned starting point.",
    experienceDesign:
      "Quiet, reflective procession through the gates, minimal decoration to honor the spiritual nature of the site, rituals focused on intention and commitment rather than spectacle.",
    signatureMoments: [
      "Joint walk through torii gates",
      "Sankalp spoken at gate threshold",
      "Quiet procession to ceremony site",
      "Minimalist ceremony honoring the path",
    ],
    bestFor: ["Spiritual couples", "Minimalist ceremonies", "Path-focused symbolism"],
    seoTitle: "Marg Darshan Vivaah at Fushimi Inari | Third Eye Events",
    metaDescription:
      "A Marg Darshan Vivaah at Fushimi Inari Shrine — the path-aligned wedding where two journeys become one, by Third Eye Events.",
  },
  {
    slug: "arashiyama",
    countrySlug: "kyoto",
    countryName: "Kyoto",
    name: "Arashiyama Bamboo Forest",
    concept: "Maun Vivaah",
    meaning: "The Silent Sacred Union",
    tagline: "Silence as the foundation of union.",
    whyVenue:
      "Towering bamboo creates natural sound isolation — one of the most peaceful places on Earth.",
    interpretation:
      "No music — only wind passing through bamboo. Mantras chanted softly — not performed loudly. Guests experience inner stillness, not external excitement.",
    ritualDirection:
      "Ceremony conducted in complete silence except for natural elements and soft mantras. Focus on internal experience rather than external performance.",
    experienceDesign:
      "Natural bamboo setting as-is, silent procession, whispered mantras, focus on internal spiritual experience rather than external display. Every element serves inner stillness.",
    signatureMoments: [
      "Silent procession through bamboo grove",
      "Soft mantras whispered in stillness",
      "Natural breeze as only soundtrack",
      "Inner-focused ceremony without external display",
    ],
    bestFor: ["Meditative couples", "Silent ceremonies", "Inner-focused unions"],
    seoTitle: "Maun Vivaah in Arashiyama Bamboo Forest | Third Eye Events",
    metaDescription:
      "A Maun Vivaah in Arashiyama Bamboo Forest — the silent sacred union where inner stillness meets outer beauty, by Third Eye Events.",
  },
  {
    slug: "kinkaku-ji",
    countrySlug: "kyoto",
    countryName: "Kyoto",
    name: "Kinkaku-ji (Golden Pavilion)",
    concept: "Chintan Vivaah",
    meaning: "The Reflective Union",
    tagline: "Union as reflection of self and soul.",
    whyVenue:
      "Golden temple reflecting on still water — symbol of clarity, balance and self-awareness.",
    interpretation:
      "Mandap aligned with reflection angle of water. Rituals emphasizing self-understanding. Marriage framed as mirror of each other's soul.",
    ritualDirection:
      "Mandap positioned to capture golden reflection in water. Rituals include self-reflection elements, clarity-focused practices, and union-as-mirror symbolism throughout.",
    experienceDesign:
      "Water-reflection alignment, minimalist gold-toned decorations, clarity-focused ritual elements, balance and harmony emphasized in every aspect. Setting enables deep self-reflection.",
    signatureMoments: [
      "Mandap aligned with golden reflection",
      "Self-reflection ritual before vows",
      "Balance and harmony ceremony elements",
      "Union witnessed through water reflection",
    ],
    bestFor: ["Reflective couples", "Clarity-seeking unions", "Symbolic ceremonies"],
    seoTitle: "Chintan Vivaah at Kinkaku-ji | Third Eye Events",
    metaDescription:
      "A Chintan Vivaah at Kinkaku-ji — the reflective union where marriage becomes mirror of self and soul, by Third Eye Events.",
  },
  {
    slug: "gion",
    countrySlug: "kyoto",
    countryName: "Kyoto",
    name: "Gion District",
    concept: "Parampara Sangam Vivaah",
    meaning: "Cultural Fusion Wedding",
    tagline: "Two ancient traditions in harmonious alignment.",
    whyVenue:
      "Traditional streets, lanterns, preserved heritage — heart of old Japan culture.",
    interpretation:
      "Fusion of Japanese rituals + Vedic Sanskar. Cultural respect — not mixing, but alignment. Every ritual explained → deeply understood.",
    ritualDirection:
      "Sequential presentation: Japanese ritual element followed by corresponding Vedic element, each explained in depth. Focus on understanding rather than performance.",
    experienceDesign:
      "Sequential cultural presentation with explanations, traditional Japanese setting respected, Vedic rituals performed with clarity, fusion achieved through understanding not blending.",
    signatureMoments: [
      "Japanese ritual element explained",
      "Corresponding Vedic element explained",
      "Sequential cultural presentation",
      "Deep understanding achieved by couple and guests",
    ],
    bestFor: ["Cultural enthusiasts", "Educational ceremonies", "Tradition-respecting couples"],
    seoTitle: "Parampara Sangam Vivaah in Gion District | Third Eye Events",
    metaDescription:
      "A Parampara Sangam Vivaah in Gion District — cultural fusion where Japanese and Vedic traditions align in deep understanding, by Third Eye Events.",
  },
  {
    slug: "philosopher-s-path",
    countrySlug: "kyoto",
    countryName: "Kyoto",
    name: "Philosopher's Path",
    concept: "Sakshi Vivaah",
    meaning: "The Witness Conscious Wedding",
    tagline: "Marriage witnessed by self, soul and journey.",
    whyVenue:
      "Famous contemplative walking path. Cherry blossoms = impermanence and beauty of life.",
    interpretation:
      "Wedding designed as a slow mindful walk. Each ritual = a pause, not a rush. Focus on sat (truth) of life.",
    ritualDirection:
      "Ceremony proceeds as mindful walk with pauses for each ritual. Each element is experienced consciously rather than rushed through. Focus on truth and presence.",
    experienceDesign:
      "Path-based progression, mindful pauses between elements, conscious experience of each ritual, focus on truth and presence rather than speed or spectacle.",
    signatureMoments: [
      "Mindful walk to ceremony start",
      "Conscious pause before each ritual",
      "Truth-focused wedding experience",
      "Journey-as-witness consciousness throughout",
    ],
    bestFor: ["Mindful couples", "Contemplative ceremonies", "Presence-focused unions"],
    seoTitle: "Sakshi Vivaah on Philosopher's Path | Third Eye Events",
    metaDescription:
      "A Sakshi Vivaah on Philosopher's Path — the witness conscious wedding where marriage unfolds with mindfulness and truth, by Third Eye Events.",
  },
  {
    slug: "lake-como",
    countrySlug: "italy",
    countryName: "Italy",
    name: "Lake Como",
    concept: "Vansh Parampara Vivaah",
    meaning: "Legacy Wedding",
    tagline: "Love staged by history itself.",
    whyVenue:
      "World's most elite wedding destination. Historic villas like Balbianello = old money elegance. Preferred by global billionaires and celebrities.",
    interpretation:
      "Mandap facing the lake → flow of lineage and continuity. Rituals designed around family legacy, not just couple. Entry via boat → symbolic arrival into a new life chapter.",
    ritualDirection:
      "Boat entry symbolizing transition, lakeside mandap facing water for lineage continuity, rituals focused on family legacy and multigenerational blessings.",
    experienceDesign:
      "Boat arrival sequence, lakeside mandap setup, legacy-focused ritual elements, multigenerational blessing ceremonies, flow of lineage emphasized throughout.",
    signatureMoments: [
      "Boat arrival at lakeside mandap",
      "Legacy blessing ritual for families",
      "Lakeside pheras facing water continuum",
      "Multigenerational celebration continuation",
    ],
    bestFor: ["Legacy-focused couples", "Multigenerational celebrations", "Historic venue weddings"],
    seoTitle: "Vansh Parampara Vivaah at Lake Como | Third Eye Events",
    metaDescription:
      "A Vansh Parampara Vivaah at Lake Como — legacy wedding where love flows through generations, by Third Eye Events.",
  },
  {
    slug: "tuscany",
    countrySlug: "italy",
    countryName: "Italy",
    name: "Tuscany",
    concept: "Sahaj Vivaah",
    meaning: "Effortless Natural Union",
    tagline: "Effortless union in rolling vineyards.",
    whyVenue:
      "Rolling vineyards + golden sunsets. Rustic yet ultra-premium countryside luxury. Slow, soulful European lifestyle.",
    interpretation:
      "Open-air mandap in vineyards → nature as witness. Long sitting-style satvik feasts (not rushed dining). Rituals done in flow, not schedule pressure.",
    ritualDirection:
      "Natural flow-based timing rather than rigid schedules, outdoor mandap to connect with nature, extended feast times for leisurely enjoyment, pressure-free ritual progression.",
    experienceDesign:
      "Outdoor vineyard setting, natural material decorations, extended feast periods, flow-based timing, connection to agricultural cycles and natural rhythms.",
    signatureMoments: [
      "Outdoor mandap in vineyard setting",
      "Leisurely satvik feast in natural flow",
      "Nature-witnessed ceremony proceedings",
      "Pressure-free ritual experience",
    ],
    bestFor: ["Nature-loving couples", "Relaxed celebrations", "Outdoor venue weddings"],
    seoTitle: "Sahaj Vivaah in Tuscany | Third Eye Events",
    metaDescription:
      "A Sahaj Vivaah in Tuscany — effortless natural union in the Italian countryside, by Third Eye Events.",
  },
  {
    slug: "amalfi-coast",
    countrySlug: "italy",
    countryName: "Italy",
    name: "Amalfi Coast",
    concept: "Samudra Sakshi Vivaah",
    meaning: "Ocean Witness Wedding",
    tagline: "Vows witnessed by ocean and sky.",
    whyVenue:
      "Dramatic cliffs + endless sea views. One of the most visually powerful wedding backdrops. Ultra-romantic, cinematic energy.",
    interpretation:
      "Mandap at cliff edge → infinity below, sky above. Ocean becomes sakshi (witness) to vows. Fire + wind + water → full element activation.",
    ritualDirection:
      "Cliff-edge mandap placement for ocean and sky witness, fire-water-wind elemental balance, ceremonies timed to maximize natural light and sound elements.",
    experienceDesign:
      "Cliff-edge platform with safety measures, ocean-view optimization, elemental balance rituals, natural light and sound utilization, dramatic yet safe setting.",
    signatureMoments: [
      "Cliff-edge mandap with ocean view",
      "Fire-water-wind elemental ceremony",
      "Sky and ocean as dual witnesses",
      "Dramatic yet safe cliff proceedings",
    ],
    bestFor: ["Dramatic ceremony lovers", "Ocean-view weddings", "Elemental balance seekers"],
    seoTitle: "Samudra Sakshi Vivaah on Amalfi Coast | Third Eye Events",
    metaDescription:
      "A Samudra Sakshi Vivaah on Amalfi Coast — ocean witness wedding where vows are held by sea and sky, by Third Eye Events.",
  },
  {
    slug: "rome",
    countrySlug: "italy",
    countryName: "Italy",
    name: "Rome",
    concept: "Sanatan Vivaah",
    meaning: "Eternal Union Beyond Time",
    tagline: "Union that feels beyond time itself.",
    whyVenue:
      "City of ancient empire & civilization. Architecture that has stood for centuries. Symbol of timeless human legacy.",
    interpretation:
      "Vedic rituals performed within ancient Roman structures. Marriage framed as timeless dharmic bond. Sanskar aligned with idea of eternity, not trend.",
    ritualDirection:
      "Ancient Roman structure integration, timeless ritual elements, eternity-focused symbolism, connection to historical continuity rather than contemporary trends.",
    experienceDesign:
      "Historical structure utilization, timeless ritual adaptations, eternity-focused design elements, respect for ancient architecture while performing authentic rituals.",
    signatureMoments: [
      "Rituals in ancient Roman setting",
      "Timeless symbolism throughout ceremony",
      "Eternity-focused vows and blessings",
      "Historical continuity honored in proceedings",
    ],
    bestFor: ["History enthusiasts", "Timeless symbolism seekers", "Ancient venue weddings"],
    seoTitle: "Sanatan Vivaah in Rome | Third Eye Events",
    metaDescription:
      "A Sanatan Vivaah in Rome — eternal union beyond time, where ancient settings host timeless vows, by Third Eye Events.",
  },
  {
    slug: "venice",
    countrySlug: "italy",
    countryName: "Italy",
    name: "Venice",
    concept: "Swapna Vivaah",
    meaning: "Dreamlike Wedding Experience",
    tagline: "Love flows like water in floating city.",
    whyVenue:
      "Floating city — unlike anywhere in the world. Gondolas, canals, historic palaces. Pure romance + fantasy.",
    interpretation:
      "Entry via gondola → symbolic transition into new life. Mandap near water channels → fluidity of life. Soft, slow, immersive rituals.",
    ritualDirection:
      "Gondola entry sequence, water-proximate mandap placement, fluid ritual timing, soft progression through ceremony elements, water symbolism throughout.",
    experienceDesign:
      "Gondola arrival coordination, water-adjacent mandap setup, fluid timing for ceremonies, soft progression through elements, water and transition symbolism emphasized.",
    signatureMoments: [
      "Gondola arrival at water mandap",
      "Fluid ceremony progression",
      "Water transition symbolism",
      "Soft, immersive ritual experience",
    ],
    bestFor: ["Romantic couples", "Water-element weddings", "Dreamlike ceremony seekers"],
    seoTitle: "Swapna Vivaah in Venice | Third Eye Events",
    metaDescription:
      "A Swapna Vivaah in Venice — dreamlike wedding experience where love flows like water in the floating city, by Third Eye Events.",
  },
  {
    slug: "uluwatu",
    countrySlug: "bali",
    countryName: "Bali",
    name: "Uluwatu",
    concept: "Anant Sakshi Vivaah",
    meaning: "Infinity Witness Wedding",
    tagline: "Surrender into the infinite universe.",
    whyVenue:
      "Dramatic cliffs overlooking the Indian Ocean. One of the most iconic sunset points in the world. Powerful natural energy — vast, open, infinite.",
    interpretation:
      "Mandap at cliff edge → no boundary, only infinity. Agni + ocean winds = intense elemental balance. Sunset pheras with Surya descending into the ocean.",
    ritualDirection:
      "Cliff-edge mandap for infinity symbolism, fire-ocean balance rituals, sunset timing for Surya descent, elemental intensity honored in proceedings.",
    experienceDesign:
      "Cliff-edge platform with safety, fire-ocean ritual optimization, sunset timing alignment, elemental balance emphasized, vastness and infinity symbolized throughout.",
    signatureMoments: [
      "Cliff-edge mandap at sunset",
      "Fire-ocean elemental balance ritual",
      "Surya descent witnessed in ocean",
      "Infinity symbolism throughout proceedings",
    ],
    bestFor: ["Infinity-seeking couples", "Cliff ceremony lovers", "Elemental balance seekers"],
    seoTitle: "Anant Sakshi Vivaah at Uluwatu | Third Eye Events",
    metaDescription:
      "An Anant Sakshi Vivaah at Uluwatu — infinity witness wedding where surrender meets the infinite universe, by Third Eye Events.",
  },
  {
    slug: "ubud",
    countrySlug: "bali",
    countryName: "Bali",
    name: "Ubud",
    concept: "Vanam Vivaah",
    meaning: "Forest Sacred Union",
    tagline: "Union in nature's lap.",
    whyVenue:
      "Dense jungle, rivers, rice terraces. Heart of Bali's spiritual and artistic life. Peaceful, introspective, deeply connected to nature.",
    interpretation:
      "Mandap beside river → flow of life energy. Soundscape = water, birds, wind — not speakers. Rituals designed for inner connection, not external show.",
    ritualDirection:
      "Riverside mandap placement for life flow, natural soundscape only (no amplified music), inner-focused ritual design, connection to natural elements and flow.",
    experienceDesign:
      "Riverside setting optimization, natural soundscape preservation, inner-focused ritual design, connection to water-bird-wind elements, peaceful and introspective atmosphere.",
    signatureMoments: [
      "Riverside mandap placement",
      "Natural soundscape ceremony",
      "Inner-focused ritual experience",
      "Connection to water-bird-wind elements",
    ],
    bestFor: ["Spiritual couples", "Nature-connected unions", "Peaceful ceremony seekers"],
    seoTitle: "Vanam Vivaah in Ubud | Third Eye Events",
    metaDescription:
      "A Vanam Vivaah in Ubud — forest sacred union where union happens in nature's lap, by Third Eye Events.",
  },
  {
    slug: "besakih",
    countrySlug: "bali",
    countryName: "Bali",
    name: "Besakih Temple",
    concept: "Shuddh Sanskar Vivaah",
    meaning: "Pure Ritual Wedding",
    tagline: "Ritual purity, uncompromised and complete.",
    whyVenue:
      "Known as Mother Temple of Bali. Deepest connection to Hindu traditions outside India. Located near Mount Agung (sacred energy center).",
    interpretation:
      "Vedic rituals aligned with Balinese Hindu practices. No over-design — only ritual purity. Ceremony guided by both Indian & Balinese priests.",
    ritualDirection:
      "Balinese Hindu vedic ritual alignment, zero ornamentation or over-design, dual-priest guidance (Indian and Balinese), ritual purity as sole focus.",
    experienceDesign:
      "Dual-priest coordination, pure ritual execution, zero decoration or over-design, alignment with both traditions, purity as the sole metric of success.",
    signatureMoments: [
      "Dual-priest ceremony execution",
      "Zero-over-design ritual purity",
      "Balinese-Hindu vedic alignment",
      "Pure ritual completion without ornament",
    ],
    bestFor: ["Purity-focused couples", "Traditional ritual seekers", "Dual-tradition ceremonies"],
    seoTitle: "Shuddh Sanskar Vivaah at Besakih Temple | Third Eye Events",
    metaDescription:
      "A Shuddh Sanskar Vivaah at Besakih Temple — pure ritual wedding where tradition is honored without compromise, by Third Eye Events.",
  },
  {
    slug: "nusa-dua",
    countrySlug: "bali",
    countryName: "Bali",
    name: "Nusa Dua",
    concept: "Shanti Vivaah",
    meaning: "Peaceful Luxury Wedding",
    tagline: "Luxury refined into peace, not extravagance.",
    whyVenue:
      "Home to Bali's most luxurious 5-star resorts. Clean, private beaches + controlled environment. Perfect for high-end global clientele.",
    interpretation:
      "Minimal yet elegant mandap — no visual noise. Calm rituals — slow, precise, meaningful. Luxury refined into peace, not extravagance.",
    ritualDirection:
      "Minimalist mandap design, slow and precise ritual timing, meaningful rather than elaborate proceedings, luxury expressed through peace and composure.",
    experienceDesign:
      "Minimalist aesthetic approach, slow timing for meaningful experiences, precision over extravagance, luxury expressed through peace and calm rather than opulence.",
    signatureMoments: [
      "Minimalist mandap setup",
      "Slow, precise ritual proceedings",
      "Peaceful luxury expression",
      "Calm, composed ceremony experience",
    ],
    bestFor: ["Luxury-seeking couples", "Peaceful ceremony lovers", "High-end clientele"],
    seoTitle: "Shanti Vivaah in Nusa Dua | Third Eye Events",
    metaDescription:
      "A Shanti Vivaah in Nusa Dua — peaceful luxury wedding where opulence gives way to peace, by Third Eye Events.",
  },
  {
    slug: "seminyak",
    countrySlug: "bali",
    countryName: "Bali",
    name: "Seminyak",
    concept: "Utsav Vivaah",
    meaning: "Celebration with Consciousness",
    tagline: "Joyful yet conscious celebration of union.",
    whyVenue:
      "Trendy, vibrant, modern Bali hotspot. Best for young, global, high-energy weddings. Beach clubs + luxury villas.",
    interpretation:
      "Celebration without losing discipline & sanskar. No alcohol → still high energy through music, culture, performance. Structured rituals before celebration.",
    ritualDirection:
      "Structured ritualling before celebration phase, high-energy possible through music-culture-performance sans alcohol, discipline maintained throughout festivities.",
    experienceDesign:
      "Two-phase approach: structured rituals first, celebration second, alcohol-free high energy through cultural elements, discipline maintained throughout.",
    signatureMoments: [
      "Structured pre-celebration rituals",
      "Alcohol-free high-energy celebration",
      "Discipline-maintained festivities",
      "Joyful yet conscious celebration experience",
    ],
    bestFor: ["Young couples", "High-energy celebrations", "Conscious festivity seekers"],
    seoTitle: "Utsav Vivaah in Seminyak | Third Eye Events",
    metaDescription:
      "An Utsav Vivaah in Seminyak — celebration with consciousness where joy meets discipline, by Third Eye Events.",
  },
  {
    slug: "anchor-cruise",
    countrySlug: "cruises",
    countryName: "Cruise",
    name: "Anchor Cruise",
    concept: "Vivaah Yatra",
    meaning: "The Sacred Wedding Journey",
    tagline: "Step-by-step transformation into marriage.",
    whyVenue:
      "India's most premium cruise route. Multi-day immersive celebration. Familiar yet exclusive.",
    interpretation:
      "Day 1: Haldi (purification). Day 2: Mehendi (celebration). Day 3: Vivaah Sanskar under open sky.",
    ritualDirection:
      "Three-phase journey: purification → celebration → sacred ceremony. Each phase builds upon the previous, creating complete transformation.",
    experienceDesign:
      "Sequential three-day programming, phase-appropriate activities and rituals, smooth transitions between experiences, journey narrative maintained throughout.",
    signatureMoments: [
      "Day 1: Haldi purification ceremony",
      "Day 2: Mehendi celebration experience",
      "Day 3: Open sky vivaah sanskar",
      "Complete journey transformation",
    ],
    bestFor: ["Journey-focused couples", "Multi-day celebration lovers", "Sequential experience seekers"],
    seoTitle: "Vivaah Yatra on Anchor Cruise | Third Eye Events",
    metaDescription:
      "A Vivaah Yatra on Anchor Cruise — sacred wedding journey where marriage unfolds step by step, by Third Eye Events.",
  },
  {
    slug: "royal-caribbean",
    countrySlug: "cruises",
    countryName: "Cruise",
    name: "Royal Caribbean",
    concept: "Vishwa Vivaah",
    meaning: "Global Union Wedding",
    tagline: "Global spiritual celebration with Indian roots.",
    whyVenue:
      "World's largest and most luxurious cruise line. International standard facilities. Perfect for global guest list.",
    interpretation:
      "Blend of global luxury + Vedic rituals. Grand scale but spiritually controlled. Sanskar explained for international guests.",
    ritualDirection:
      "Global-local balance in rituals, explanation and translation for international guests, scale maintained with spiritual control, cultural bridging through understanding.",
    experienceDesign:
      "International-standard facilities with Vedic rituals, cultural explanation components, scale-appropriate yet spiritually controlled proceedings, global-local harmony.",
    signatureMoments: [
      "Global luxury setting with Vedic rituals",
      "Cultural explanation for international guests",
      "Spiritually controlled grand scale",
      "Global-local harmony in proceedings",
    ],
    bestFor: ["Global couples", "International guest weddings", "Spiritually controlled scale"],
    seoTitle: "Vishwa Vivaah on Royal Caribbean | Third Eye Events",
    metaDescription:
      "A Vishwa Vivaah on Royal Caribbean — global union wedding where Indian tradition meets global celebration, by Third Eye Events.",
  },
  {
    slug: "norwegian",
    countrySlug: "cruises",
    countryName: "Cruise",
    name: "Norwegian Cruise Line",
    concept: "Mukt Vivaah",
    meaning: "Free-Spirited Wedding",
    tagline: "Free, natural and joyful union.",
    whyVenue:
      "Known for freestyle luxury (no rigid structure). Relaxed yet premium experience.",
    interpretation:
      "Rituals designed with flow, not pressure. No chaos — no over-scheduling. Marriage experienced, not rushed.",
    ritualDirection:
      "Flow-based rather than pressure-based timing, relaxed progression through elements, joyful experience maintained, natural unfolding of union.",
    experienceDesign:
      "Flexible timing and sequencing, relaxed atmosphere maintenance, joy-focused experience design, natural union progression rather than forced progression.",
    signatureMoments: [
      "Relaxed, flowing ceremony progression",
      "Joyful, natural union experience",
      "Pressure-free ritual timing",
      "Free-spirited celebration experience",
    ],
    bestFor: ["Free-spirited couples", "Relaxed ceremony lovers", "Joy-focused unions"],
    seoTitle: "Mukt Vivaah on Norwegian Cruise Line | Third Eye Events",
    metaDescription:
      "A Mukt Vivaah on Norwegian Cruise Line — free-spirited wedding where marriage is experienced joyfully and naturally, by Third Eye Events.",
  },
  {
    slug: "celebrity",
    countrySlug: "cruises",
    countryName: "Cruise",
    name: "Celebrity Cruises",
    concept: "Chaitanya Vivaah",
    meaning: "Conscious Luxury Wedding",
    tagline: "Refined, intelligent and conscious wedding.",
    whyVenue:
      "Sophisticated, design-focused luxury. Less crowd, more class. Premium experience for refined clients.",
    interpretation:
      "Minimal design → maximum meaning. Silence, space, elegance. Rituals deeply explained and felt.",
    ritualDirection:
      "Minimalist aesthetic approach, explanation-focused ritual delivery, spacious and elegant settings, deep understanding and feeling rather than superficial performance.",
    experienceDesign:
      "Minimalist design optimization, ritual explanation and education, spacious elegant environments, deep understanding emphasis over surface-level performance.",
    signatureMoments: [
      "Minimalist elegant setting",
      "Deeply explained ritual experience",
      "Silent and spacious proceedings",
      "Conscious luxury wedding experience",
    ],
    bestFor: ["Refined couples", "Conscious luxury seekers", "Intelligent ceremony appreciators"],
    seoTitle: "Chaitanya Vivaah on Celebrity Cruises | Third Eye Events",
    metaDescription:
      "A Chaitanya Vivaah on Celebrity Cruises — conscious luxury wedding where refinement meets understanding, by Third Eye Events.",
  },
  {
    slug: "silversea",
    countrySlug: "cruises",
    countryName: "Cruise",
    name: "Silversea Expeditions",
    concept: "Anveshan Vivaah",
    meaning: "Exploration Wedding",
    tagline: "Rare, once-in-a-lifetime union beyond boundaries.",
    whyVenue:
      "Ultra-luxury expedition cruises. Rare, exclusive, offbeat destinations. Designed for elite explorers.",
    interpretation:
      "Wedding as a discovery journey. Rituals aligned with unknown, new beginnings. Highly intimate, deeply personal.",
    ritualDirection:
      "Discovery journey framing, ritual alignment with new beginnings, intimacy and personal focus, boundary-transcending symbolism throughout.",
    experienceDesign:
      "Expedition journey optimization, new beginnings ritual alignment, intimacy and personal focus maintenance, exploration and discovery symbolism emphasized.",
    signatureMoments: [
      "Wedding as discovery journey",
      "Rituals aligned with new beginnings",
      "Intimate, deeply personal experience",
      "Boundary-transcending union symbolism",
    ],
    bestFor: ["Explorer couples", "Once-in-a-lifetime seekers", "Boundary-transcending unions"],
    seoTitle: "Anveshan Vivaah on Silversea Expeditions | Third Eye Events",
    metaDescription:
      "An Anveshan Vivaah on Silversea Expeditions — exploration wedding where rare unions happen beyond boundaries, by Third Eye Events.",
  },
];

export const getVenue = (countrySlug: string, slug: string) =>
  venueExperiences.find((v) => v.countrySlug === countrySlug && v.slug === slug);

export const getVenuesByCountry = (countrySlug: string) =>
  venueExperiences.filter((v) => v.countrySlug === countrySlug);
