# Images Asset Checklist — Third Eye Events

This checklist tracks all [CONTENT REQUIRED] imagery referenced in the Google Docs briefs and codebase.

## Homepage
- [ ] `/images/hero-cinematic.jpg` — Hero background. High-quality cinematic premium visual, spiritual + luxury wedding aesthetic. Replaces current placeholder. `src/pages/index.astro` heroImage.

## Opening Sequence
- [ ] No image asset required. Uses ॐ typography.

## Vaidik Wedding
- [ ] `/images/vaidik/pure-hero.jpg` — PURE hero background / atmospheric visual for Vaidik section
- [ ] `/images/vaidik/satvik-dining-copper.jpg` — Satvik dining photography: copper serveware
- [ ] `/images/vaidik/satvik-dining-banana-leaf.jpg` — Satvik dining photography: banana leaf dining
- [ ] `/images/vaidik/satvik-dining-seasonal.jpg` — Satvik dining photography: seasonal produce
- [ ] `/images/vaidik/mandap-natural.jpg` — Mandap natural elements for PURE section

## Signature Entries
- [ ] `/images/signature/shiva-entry-hero.jpg` — Shiva Entry hero visual
- [ ] `/images/signature/royal-entry-hero.jpg` — Royal Entry hero visual
- [ ] `/images/signature/floral-entry-hero.jpg` — Floral Entry hero visual
- [ ] `/images/signature/celestial-entry-hero.jpg` — Celestial Entry hero visual
- [ ] `/images/signature/shiva-entry-sequence/*.jpg` — Step-by-step cinematic frames for Shiva Entry detail page
- [ ] `/images/signature/royal-entry-sequence/*.jpg`
- [ ] `/images/signature/floral-entry-sequence/*.jpg`
- [ ] `/images/signature/celestial-entry-sequence/*.jpg`

## About
- [ ] `/images/about/founder-portrait-gautam-gs.jpg` — Founder portrait, high-res, cinematic
- [ ] `/images/about/archival-dance.jpg` — Archival performance imagery
- [ ] `/images/about/archival-mumbai.jpg` — Mumbai years imagery
- [ ] `/images/about/team-vision.jpg` — Brand evolution visual

## Destinations
General pattern: `/images/destinations/{slug}/hero.jpg` and `/images/destinations/{slug}/venues/{venue}.jpg`

- [ ] Maldives: Soneva Fushi, One&Only Reethi Rah, Taj Exotica, Conrad Rangali, Joali
- [ ] Rajasthan: Udaipur, Jaisalmer, Jaipur, Ranthambore, Jodhpur
- [ ] Switzerland: Zermatt, Interlaken, St. Moritz, Lauterbrunnen, Glacier Express
- [ ] Kyoto: Fushimi Inari, Arashiyama, Kinkaku-ji, Gion, Philosopher's Path
- [ ] Italy: Lake Como, Tuscany, Amalfi Coast, Rome, Venice
- [ ] Bali: Uluwatu, Ubud, Besakih, Nusa Dua, Seminyak
- [ ] Cruise: Anchor, Royal Caribbean, Norwegian, Celebrity, Silversea

India master list:
- Royal Heritage: Udaipur, Jaipur, Jodhpur, Jaisalmer, Pushkar, Bikaner, Neemrana, Alwar, Orchha, Gwalior, Khajuraho, Mandu
- Beach & Coastal: Goa, Kerala, Andaman
- Hills & Mountains: Shimla, Manali, Dharamshala, Kasauli, Mussoorie, Rishikesh, Nainital, Auli, Srinagar, Gulmarg, Pahalgam
- Nature & Forest: Shillong, Cherrapunji, Gangtok, Kaziranga, Tawang, Coorg, Chikmagalur, Hampi, Mysore
- Spiritual/Vaidik: Varanasi, Haridwar, Vrindavan, Ayodhya, Ujjain, Tirupati
- Metro Luxury: Delhi, Mumbai, Bangalore, Hyderabad, Chennai, Pune
- Desert & Offbeat: Rann of Kutch, Osian, Thar Desert

## Event IP
- [ ] `/images/ip/exhibitions-hero.jpg`
- [ ] `/images/ip/automotive-hero.jpg`
- [ ] `/images/ip/awards-hero.jpg`
- [ ] `/images/ip/best-products-hero.jpg`
- [ ] `/images/ip/sports-hero.jpg`
- [ ] `/images/ip/fashion-hero.jpg`
- [ ] `/images/ip/political-hero.jpg`
- [ ] `/images/ip/devotional-hero.jpg`
- [ ] `/images/ip/concerts-hero.jpg`

## Production
- [ ] `/images/production/feature-films.jpg`
- [ ] `/images/production/short-films.jpg`
- [ ] `/images/production/documentaries.jpg`
- [ ] `/images/production/youtube-digital.jpg`
- [ ] `/images/production/branded-content.jpg`
- [ ] `/images/production/ad-shoots.jpg`

## General
- [ ] `/images/og.jpg` — Open Graph default. Exists.
- [ ] `/favicon.svg` — Exists.

### Notes
- All images should be high-resolution, consistent color grading: warm gold/ivory palette with spiritual luxury tone.
- Use `src=undefined` fallback via ExperienceImage component for graceful degradation.
- Add alt text for accessibility.
