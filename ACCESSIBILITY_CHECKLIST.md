# Accessibility Checklist — Third Eye Events

Last reviewed: 2026-08-22

## Perceivable

### Images
- [x] All content images have descriptive alt text
- [x] Decorative images use `alt=""` and are inside `aria-hidden` containers
- [ ] Hero / Signature / Destination images supplied — currently using ExperienceImage fallback
- [ ] Alt text is meaningful, not just "image" or empty for content images

### Text and contrast
- [ ] Color contrast meets WCAG AA for body text and interactive elements
- [ ] Text scaling up to 200% does not break layout
- [x] `prefers-reduced-motion` disables opening sequence

### Multimedia
- [ ] Opening sequence has Skip Intro button and Escape key support
- [ ] Opening sequence respects `prefers-reduced-motion`
- [ ] Captions/transcripts provided for any video/audio added later

## Operable

### Keyboard
- [x] Skip link present: `Skip to content`
- [x] All interactive elements focusable and visible
- [x] Opening sequence skippable via button and Escape
- [ ] Tab order follows visual order

### Navigation
- [x] Consistent site navigation across pages
- [x] Breadcrumb trail available on inner pages via PageHero
- [ ] Focus states styled visibly

## Understandable

### Readability
- [x] Language set to `lang="en-IN"`
- [x] Heading hierarchy logical — single H1 per page
- [ ] Content avoids jargon without explanation

### Predictability
- [x] Links open in same tab unless external
- [x] Form has honeypot and validation feedback

## Robust

### Semantics
- [x] Semantic HTML: `<main>`, `<section>`, `<nav>`, `<footer>`
- [x] ARIA landmarks via BaseLayout
- [x] JSON-LD structured data present

### Compatibility
- [x] Build passes with no Astro errors
- [x] No user-visible `[CONTENT REQUIRED]` placeholders

## Content to supply for full compliance
- Hero cinematic image `public/images/hero-cinematic.jpg`
- Founder portrait and archival imagery
- Satvik dining photography
- Signature Entries hero images with descriptive alt
- Destination hero images with descriptive alt

## Notes
Run `npm run build` after changes to verify no SSR errors.
Update this checklist after each content drop.
