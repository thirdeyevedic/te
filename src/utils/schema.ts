/**
 * Schema builders — shared structured-data fragments
 */

export interface Crumb {
  label: string;
  href?: string;
}

export function buildBreadcrumbs(crumbs: Crumb[], base = "https://thirdeyeevents.com") {
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
