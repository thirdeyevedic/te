/**
 * DESTINATIONS — Different destinations. Different worlds.
 * Each destination is an experience, not a pin on a map.
 *
 * Imagery: heroImage is the wide crop used by page heroes; cardImage is the
 * portrait crop used by listing cards. Both are supplied.
 *
 * Venues live in ./venues.ts as the single source of truth — read them with
 * getVenuesByCountry(destination.slug). Do not duplicate venue names or
 * concepts here; a second copy drifts and silently breaks the join.
 */

export interface Destination {
  slug: string;
  name: string;
  region: string;
  country: string;
  tagline: string;
  /** Wide hero imagery — public/ URL or imported asset */
  heroImage?: string;
  /** Wide hero alt text */
  heroAlt?: string;
  /** Portrait crop of the same photograph, used by listing cards */
  cardImage?: string;
  /** Portrait card alt text */
  cardAlt?: string;
  landscape: string;
  culturalContext: string;
  luxuryContext: string;
  thirdEyeInterpretation: string;
  ritualDirection: string;
  experienceDescription: string;
  idealAudience: string;
  bestFor: string[];
  seoTitle: string;
  metaDescription: string;
}

export const destinations: Destination[] = [
  {
    slug: "maldives",
    name: "Maldives",
    region: "Indian Ocean",
    country: "Maldives",
    tagline: "Ocean silence. Sky infinity.",
    heroImage: "/images/destinations/maldives/hero.jpg",
    heroAlt: "A serene overwater mandapa in the Maldives at sunrise, with turquoise waters stretching to a seamless horizon.",
    cardImage: "/images/destinations/maldives/card.jpg",
    cardAlt: "A vertical view of a luxury overwater villa on stilts above a crystal-clear Maldives lagoon.",
    landscape:
      "Low coral islands, turquoise lagoons and sand that dissolves into shallow sea — a horizon with almost no edges.",
    culturalContext:
      "A maritime world of fishermen, monsoon winds and coral — nature governing every rhythm of the day.",
    luxuryContext:
      "Some of the world's most private resort islands, where a single property occupies an entire island.",
    thirdEyeInterpretation:
      "We treat the ocean not as backdrop but as sakshi — witness. The wedding slows to the pace of tide and light.",
    ritualDirection:
      "Ceremonies align to sunrise and sunset; the mandapa faces open water so Agni meets horizon.",
    experienceDescription:
      "Days move between lagoon stillness and celebration; nights are lit by flame and starlight rather than chandeliers.",
    idealAudience:
      "Couples seeking intimate scale, barefoot formality and absolute privacy.",
    bestFor: ["Intimate guest lists", "Sunrise rituals", "Private-island takeovers"],
    seoTitle: "Maldives Destination Weddings | Third Eye Events",
    metaDescription:
      "Vedic destination weddings across Maldives private islands — Soneva Fushi, One&Only Reethi Rah, Taj Exotica, Conrad Rangali and Joali, each designed around a distinct Sanskrit wedding concept.",
  },
  {
    slug: "switzerland",
    name: "Switzerland",
    region: "The Alps",
    country: "Switzerland",
    tagline: "Fire meets ice. Vows meet silence.",
    heroImage: "/images/destinations/switzerland/hero.jpg",
    heroAlt: "A glowing brass homa fire contrasted against the stark white snow of the Swiss Alps, with the Matterhorn peak rising in the distance.",
    cardImage: "/images/destinations/switzerland/card.jpg",
    cardAlt: "A close-up of a sacred fire burning on a snowfield, with towering Alpine peaks in the background.",
    landscape:
      "Glaciated peaks, meadow valleys, waterfalls falling from cliff villages and trains crossing the high snow.",
    culturalContext:
      "Alpine precision and quietness — a culture of order, altitude and understatement.",
    luxuryContext:
      "Car-free mountain resorts, grand hotels and rail journeys engineered like clockwork.",
    thirdEyeInterpretation:
      "Altitude changes people. We use thin air, silence and scale to make vows feel weightier.",
    ritualDirection:
      "Agni against snow — the homa kund glowing at the foot of glaciers, mantra carrying in cold clear air.",
    experienceDescription:
      "Guests arrive by cog railway; ceremonies pause mid-silence as clouds part over four-thousand-metre peaks.",
    idealAudience:
      "Couples drawn to elemental contrast — warmth of ritual inside vast cold landscapes.",
    bestFor: ["Elemental drama", "Alpine privacy", "Rail journeys"],
    seoTitle: "Switzerland Destination Weddings — Zermatt, Interlaken | Third Eye Events",
    metaDescription:
      "Agni-Him weddings beneath the Matterhorn, Panch Tatva ceremonies in Interlaken and vows aboard the Glacier Express — Swiss alpine weddings designed by Third Eye Events.",
  },
  {
    slug: "kyoto",
    name: "Kyoto",
    region: "Kansai",
    country: "Japan",
    tagline: "Precision as devotion.",
    heroImage: "/images/destinations/kyoto/hero.jpg",
    heroAlt: "A meditative Kyoto moss garden at dawn, with raked gravel, a stone lantern, and a soft mist between ancient cedar trees.",
    cardImage: "/images/destinations/kyoto/card.jpg",
    cardAlt: "A vertical composition of a traditional Japanese zen garden with wet moss and grey stone lanterns.",
    landscape:
      "Wooden machiya lanes, vermilion gates climbing forested hills, moss gardens and bamboo moving in wind.",
    culturalContext:
      "A thousand years of imperial refinement — craft, seasonality and ma (negative space) as spiritual practice.",
    luxuryContext:
      "Ryokan hospitality, kaiseki dining and gardens maintained for centuries by hand.",
    thirdEyeInterpretation:
      "Kyoto understands what Vedic tradition understands: meaning lives in restraint. Two disciplines, one language.",
    ritualDirection:
      "Dawn ceremonies before the crowds; purification gestures echoing between Japanese and Vedic practice.",
    experienceDescription:
      "Tea ceremony to tilak, cedar scent to sandalwood — a dialogue of two ancient civilisations around one union.",
    idealAudience:
      "Couples who want cultural depth over spectacle — connoisseurs of detail.",
    bestFor: ["Cultural depth", "Garden ceremonies", "Seasonal beauty"],
    seoTitle: "Kyoto Destination Weddings | Third Eye Events",
    metaDescription:
      "Destination weddings in Kyoto — Fushimi Inari, Arashiyama, Kinkaku-ji, Gion — where Japanese precision meets Vedic ceremony, designed by Third Eye Events.",
  },
  {
    slug: "italy",
    name: "Italy",
    region: "Mediterranean Europe",
    country: "Italy",
    tagline: "La dolce vita, sacred.",
    heroImage: "/images/destinations/italy/hero.jpg",
    heroAlt: "An elegant lakefront villa in Italy at golden hour, with cypress trees and a mirrored reflection in the still water.",
    cardImage: "/images/destinations/italy/card.jpg",
    cardAlt: "A narrow view of a Tuscan hillside with a single cypress tree and a honey-coloured stone wall.",
    landscape:
      "Lake villas mirrored in still water, cypress-lined Tuscan ridges, Amalfi cliffs stacked above the sea.",
    culturalContext:
      "Renaissance artistry and Mediterranean family culture — celebration as an art of living.",
    luxuryContext:
      "Historic villas, Michelin kitchens and centuries-old estates opened for private celebration.",
    thirdEyeInterpretation:
      "We bring the Vedic heart to Italian beauty — pheras at golden hour, satvik tables under pergolas.",
    ritualDirection:
      "Outdoor mandapas framed by cypress and stone; muhurat timed to Tuscan light.",
    experienceDescription:
      "Processions through villa gardens, long-table feasts, opera notes drifting over lake water.",
    idealAudience:
      "Couples blending Indian tradition with European romance.",
    bestFor: ["Villa weddings", "Lakeside pheras", "Multi-day celebrations"],
    seoTitle: "Italy Destination Weddings — Lake Como, Tuscany, Amalfi | Third Eye Events",
    metaDescription:
      "Vedic weddings across Italy — Lake Como villas, Tuscany estates and Amalfi cliffs — where Indian tradition meets Mediterranean beauty. By Third Eye Events.",
  },
  {
    slug: "bali",
    name: "Bali",
    region: "Indonesia",
    country: "Indonesia",
    tagline: "Island of the gods.",
    heroImage: "/images/destinations/bali/hero.jpg",
    heroAlt: "A cliff-top Vedic ceremony in Bali, with cascading frangipani flowers and a burning sunset over the Indian Ocean.",
    cardImage: "/images/destinations/bali/card.jpg",
    cardAlt: "A silhouette of a Balinese meru pagoda against a vivid vermilion and gold sunset sky.",
    landscape:
      "Cliff temples above breaking surf, rice terraces stepped into volcano slopes, mist rising from river gorges.",
    culturalContext:
      "Living Balinese Hinduism — daily offerings, temple dance and ceremony woven into ordinary life.",
    luxuryContext:
      "Cliff-top villas, jungle resorts and beach estates with deeply trained hospitality.",
    thirdEyeInterpretation:
      "Bali already prays. We build your Vedic ceremony inside an island that understands ritual natively.",
    ritualDirection:
      "Temple-adjacent settings where Balinese blessings can precede Vedic sankalp.",
    experienceDescription:
      "Sunset cliff ceremonies, gamelan meeting shehnai, flower baths after pheras.",
    idealAudience:
      "Couples wanting spiritual atmosphere with tropical ease and value.",
    bestFor: ["Cliff ceremonies", "Spiritual resonance", "Tropical luxury"],
    seoTitle: "Bali Destination Weddings — Uluwatu, Ubud | Third Eye Events",
    metaDescription:
      "Destination weddings in Bali — Uluwatu cliffs, Ubud jungle and Besakih temple surroundings — Vedic ceremony within the island of the gods. By Third Eye Events.",
  },
  {
    slug: "cruises",
    name: "Cruise",
    region: "International waters",
    country: "Multiple",
    tagline: "A world that moves with you.",
    heroImage: "/images/destinations/cruises/hero.jpg",
    heroAlt: "A luxury cruise ship deck at dusk, with warm gold ambient lighting and a vast, dark indigo ocean horizon.",
    cardImage: "/images/destinations/cruises/card.jpg",
    cardAlt: "The bow of a white luxury liner cutting through a calm ocean under a magenta twilight sky.",
    landscape:
      "Open ocean horizons, ports changing outside your window, decks that become venues at night.",
    culturalContext:
      "A floating city — hospitality systems refined across thousands of sailings.",
    luxuryContext:
      "From full-ship charters to expedition yachts, entire vessels privatised for celebration.",
    thirdEyeInterpretation:
      "A wedding at sea removes distraction completely. Guests cannot drift away — the world holds everyone together.",
    ritualDirection:
      "Deck mandapas under open sky; Agni permitted at sea with maritime compliance handled end-to-end.",
    experienceDescription:
      "Multi-day itineraries where sangeet, ceremony and reception each land on a different shore or deck.",
    idealAudience:
      "Families wanting an immersive multi-day wedding without hotel logistics.",
    bestFor: ["Multi-day format", "Full privacy", "Built-in entertainment"],
    seoTitle: "Cruise Destination Weddings | Third Eye Events",
    metaDescription:
      "Weddings at sea aboard Royal Caribbean, Norwegian, Celebrity and Silversea — full-ship charters designed and delivered by Third Eye Events.",
  },
];

/** India destination architecture — master categories (source-supported entries slotted) */
export interface IndiaCategory {
  id: string;
  name: string;
  essence: string;
  destinations: string[];
}

export const indiaCategories: IndiaCategory[] = [
  {
    id: "royal-heritage",
    name: "Royal Heritage",
    essence: "Palaces, forts and living court culture.",
    destinations: ["Udaipur", "Jaipur", "Jodhpur"],
  },
  {
    id: "desert-offbeat",
    name: "Desert & Offbeat",
    essence: "Dune camps, salt flats and star-heavy skies.",
    destinations: ["Jaisalmer"],
  },
  {
    id: "nature-forest",
    name: "Nature & Forest",
    essence: "Wilderness retreats where ceremony meets the wild.",
    destinations: ["Ranthambore"],
  },
  {
    id: "beach-coastal",
    name: "Beach & Coastal",
    essence: "Shorelines and seaside heritage.",
    destinations: ["Goa", "Kerala", "Andaman"],
  },
  {
    id: "mountains-hills",
    name: "Mountains & Hills",
    essence: "Altitude, deodar and valley light.",
    destinations: ["Shimla", "Manali", "Dharamshala", "Mussoorie"],
  },
  {
    id: "spiritual-vedic",
    name: "Spiritual / Vedic",
    essence: "Cities and ghats where ritual is daily life.",
    destinations: ["Varanasi", "Haridwar", "Rishikesh"],
  },
  {
    id: "metro-luxury",
    name: "Metro Luxury",
    essence: "Five-star scale inside India's metros.",
    destinations: ["Delhi", "Mumbai", "Bangalore"],
  },
];

export const getDestination = (slug: string) => destinations.find((d) => d.slug === slug);
