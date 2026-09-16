/**
 * IP EVENTS — An ecosystem of signature experiences.
 * Owned, designed and delivered by Third Eye. Repeatable, brandable, scalable.
 */

export interface IPEventCategory {
  id: string;
  name: string;
  description: string;
  focus: string;
  potentialFormat: string;
  audience: string;
  scalability: string;
  /** Wide hero imagery — public/ URL */
  heroImage?: string;
}

export const ipEvents: IPEventCategory[] = [
  {
    id: "exhibitions",
    heroImage: "/images/ip/exhibitions-hero.jpg",
    name: "Exhibitions & Expos",
    description:
      "Industry platforms where Third Eye designs not just stalls but entire exhibition worlds — flow, pacing, dwell and discovery.",
    focus: "Industry convening · brand visibility",
    potentialFormat: "Annual trade expos · curated showcases",
    audience: "Trade visitors · brands · media",
    scalability: "City → national circuit",
  },
  {
    id: "automotive",
    heroImage: "/images/ip/automotive-hero.jpg",
    name: "Automotive & Mobility",
    description:
      "Launch environments and motoring spectacles built with mechanical precision — vehicles presented as protagonists.",
    focus: "Product drama · engineering storytelling",
    potentialFormat: "Launch nights · track experiences · concours formats",
    audience: "Brands · enthusiasts · press",
    scalability: "Single marque → multi-brand festival",
  },
  {
    id: "awards",
    heroImage: "/images/ip/awards-hero.jpg",
    name: "Awards & Gala",
    description:
      "Ceremonies engineered for gravity — staging, script, reveal rhythm and the discipline a credible stage demands.",
    focus: "Recognition · prestige production",
    potentialFormat: "Industry awards · annual galas",
    audience: "Industry leadership · invitees",
    scalability: "Property licensing · sector editions",
  },
  {
    id: "products",
    heroImage: "/images/ip/best-products-hero.jpg",
    name: "Best Products of India",
    description:
      "A platform format celebrating Indian excellence — products staged with the respect of museum curation.",
    focus: "Discovery · national pride",
    potentialFormat: "Curated showcase IP · travelling edition",
    audience: "Consumers · retailers · makers",
    scalability: "Vertical editions per product class",
  },
  {
    id: "sports",
    heroImage: "/images/ip/sports-hero.jpg",
    name: "Sports Leagues & Tournaments",
    description:
      "League formats owned end to end — fixture design, venue experience, broadcast readiness and season arc.",
    focus: "Competition · community building",
    potentialFormat: "City leagues · corporate tournaments · seasonal cups",
    audience: "Players · fans · sponsors",
    scalability: "Sport → city franchise model",
  },
  {
    id: "fashion",
    heroImage: "/images/ip/fashion-hero.jpg",
    name: "Fashion & Modeling",
    description:
      "Runways and model platforms directed like cinema — walk choreography drawn from Third Eye's performance roots.",
    focus: "Movement · image-making",
    potentialFormat: "Season shows · talent platforms",
    audience: "Designers · brands · talent scouts",
    scalability: "Roster development · city editions",
  },
  {
    id: "political",
    heroImage: "/images/ip/political-hero.jpg",
    name: "Political & Public",
    description:
      "Large-scale public gatherings executed with protocol discipline — crowd architecture, security coordination, zero-error stages.",
    focus: "Scale management · protocol",
    potentialFormat: "Public rallies · civic ceremonies",
    audience: "Public institutions · parties · citizens",
    scalability: "Constituency → state scale",
  },
  {
    id: "devotional",
    heroImage: "/images/ip/devotional-hero.jpg",
    name: "Devotional & Spiritual",
    description:
      "Sacred gatherings produced with reverence — sound, seating and sightlines designed around devotion rather than spectacle.",
    focus: "Reverence · mass participation",
    potentialFormat: "Satsangs · katha · spiritual festivals",
    audience: "Devotees · spiritual organisations",
    scalability: "Temple circuits · touring formats",
  },
  {
    id: "concerts",
    heroImage: "/images/ip/concerts-hero.jpg",
    name: "Concerts & Live Entertainment",
    description:
      "Live entertainment as total environment — stage, light, artist logistics and crowd energy managed as one instrument.",
    focus: "Performance · atmosphere",
    potentialFormat: "Ticketed concerts · festival stages",
    audience: "General public · sponsors",
    scalability: "Touring properties · headline festivals",
  },
];
