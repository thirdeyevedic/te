/**
 * Schema builders — shared structured-data fragments
 */

import { SITE_URL, CONTACT_EMAIL, SITE_NAME } from "../data/site";

export interface Crumb {
  label: string;
  href?: string;
}

export function buildBreadcrumbs(crumbs: Crumb[], base = SITE_URL) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: c.label,
      ...(c.href ? { item: `${base}${c.href}` } : {}),
    })),
  };
}

/**
 * ProfessionalService node — the business entity behind the Organization.
 * Google uses this for the knowledge panel / rich results; keep every claim
 * verifiable (no invented phone numbers or street addresses).
 */
export function buildLocalBusiness(site = SITE_URL) {
  return {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": `${site}#localbusiness`,
    name: SITE_NAME,
    description:
      "Third Eye Events is a multi-domain experience and execution powerhouse — Vedic luxury weddings, destination weddings, signature experiences, owned IP Events, production facilitation and cultural events.",
    url: site,
    email: CONTACT_EMAIL,
    image: `${site}/images/og.jpg`,
    logo: `${site}/images/logo.png`,
    priceRange: "₹₹₹",
    currenciesAccepted: "INR",
    paymentAccepted: "Bank Transfer, UPI, Card",
    areaServed: [
      { "@type": "Country", name: "India" },
      { "@type": "Place", name: "Worldwide (destination events)" },
    ],
    knowsLanguage: ["en-IN", "hi"],
    parentOrganization: { "@id": `${site}#organization` },
    hasOfferCatalog: {
      "@type": "OfferCatalog",
      name: "Event services",
      itemListElement: [
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Vedic luxury weddings" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Destination weddings" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Signature experiences" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "IP Events" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Production facilitation" } },
        { "@type": "Offer", itemOffered: { "@type": "Service", name: "Cultural events" } },
      ],
    },
  };
}
