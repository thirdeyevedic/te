#!/usr/bin/env node
/**
 * Generate SVG placeholder images for [CONTENT REQUIRED] assets.
 * Run: node scripts/generate-placeholders.mjs
 */
import { writeFileSync, mkdirSync } from "fs";
import { join } from "path";

const PUBLIC = join(import.meta.dirname, "..", "public");

const placeholders = [
  // Homepage
  { path: "images/hero-cinematic.jpg.svg", w: 1920, h: 1080, label: "Hero Cinematic", accent: "#b89b5e" },

  // Vaidik
  { path: "images/vaidik/pure-hero.jpg.svg", w: 1920, h: 800, label: "PURE Hero", accent: "#b89b5e" },
  { path: "images/vaidik/satvik-dining-copper.jpg.svg", w: 800, h: 1000, label: "Tamra Patra", accent: "#a9552b" },
  { path: "images/vaidik/satvik-dining-banana-leaf.jpg.svg", w: 800, h: 1000, label: "Banana Leaf", accent: "#6e5a3e" },
  { path: "images/vaidik/satvik-dining-seasonal.jpg.svg", w: 800, h: 1000, label: "Modern Satvik", accent: "#b89b5e" },

  // Signature entries
  { path: "images/signature/shiva-entry-hero.jpg.svg", w: 800, h: 1100, label: "Shiva Entry", accent: "#4a6fa5" },
  { path: "images/signature/royal-entry-hero.jpg.svg", w: 800, h: 1100, label: "Royal Entry", accent: "#b89b5e" },
  { path: "images/signature/floral-entry-hero.jpg.svg", w: 800, h: 1100, label: "Floral Entry", accent: "#c9bda6" },
  { path: "images/signature/celestial-entry-hero.jpg.svg", w: 800, h: 1100, label: "Celestial Entry", accent: "#8a8fa8" },

  // About
  { path: "images/about/founder-portrait-gautam-gs.jpg.svg", w: 800, h: 1000, label: "Gautam GS", accent: "#b89b5e" },

  // Destinations
  { path: "images/destinations/maldives/hero.jpg.svg", w: 1200, h: 800, label: "Maldives", accent: "#4a8fa8" },
  { path: "images/destinations/rajasthan/hero.jpg.svg", w: 1200, h: 800, label: "Rajasthan", accent: "#c9a84a" },
  { path: "images/destinations/switzerland/hero.jpg.svg", w: 1200, h: 800, label: "Switzerland", accent: "#7a9ab8" },
  { path: "images/destinations/kyoto/hero.jpg.svg", w: 1200, h: 800, label: "Kyoto", accent: "#a85a5a" },
  { path: "images/destinations/italy/hero.jpg.svg", w: 1200, h: 800, label: "Italy", accent: "#8aaa6a" },
  { path: "images/destinations/bali/hero.jpg.svg", w: 1200, h: 800, label: "Bali", accent: "#5a8a6a" },
  { path: "images/destinations/cruises/hero.jpg.svg", w: 1200, h: 800, label: "Cruise", accent: "#4a6a8a" },

  // Event IP
  { path: "images/ip/exhibitions-hero.jpg.svg", w: 1200, h: 800, label: "Exhibitions", accent: "#b89b5e" },
  { path: "images/ip/automotive-hero.jpg.svg", w: 1200, h: 800, label: "Automotive", accent: "#6a6a7a" },
  { path: "images/ip/awards-hero.jpg.svg", w: 1200, h: 800, label: "Awards", accent: "#b89b5e" },
  { path: "images/ip/best-products-hero.jpg.svg", w: 1200, h: 800, label: "Best Products", accent: "#a9552b" },
  { path: "images/ip/sports-hero.jpg.svg", w: 1200, h: 800, label: "Sports", accent: "#4a8a6a" },
  { path: "images/ip/fashion-hero.jpg.svg", w: 1200, h: 800, label: "Fashion", accent: "#a85a7a" },
  { path: "images/ip/political-hero.jpg.svg", w: 1200, h: 800, label: "Political", accent: "#6a5a8a" },
  { path: "images/ip/devotional-hero.jpg.svg", w: 1200, h: 800, label: "Devotional", accent: "#b89b5e" },
  { path: "images/ip/concerts-hero.jpg.svg", w: 1200, h: 800, label: "Concerts", accent: "#a85a5a" },

  // Production
  { path: "images/production/feature-films.jpg.svg", w: 800, h: 600, label: "Feature Films", accent: "#4a6a8a" },
  { path: "images/production/short-films.jpg.svg", w: 800, h: 600, label: "Short Films", accent: "#6a8a4a" },
  { path: "images/production/documentaries.jpg.svg", w: 800, h: 600, label: "Documentaries", accent: "#8a6a4a" },
  { path: "images/production/youtube-digital.jpg.svg", w: 800, h: 600, label: "YouTube / Digital", accent: "#a85a5a" },
  { path: "images/production/branded-content.jpg.svg", w: 800, h: 600, label: "Branded Content", accent: "#b89b5e" },
  { path: "images/production/ad-shoots.jpg.svg", w: 800, h: 600, label: "Ad Shoots", accent: "#5a8a8a" },
];

function generateSVG({ w, h, label, accent }) {
  const fontSize = Math.max(14, Math.min(w, h) * 0.025);
  const subSize = fontSize * 0.65;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#201b15"/>
      <stop offset="52%" stop-color="#12100d"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </linearGradient>
    <radialGradient id="glow1" cx="30%" cy="20%">
      <stop offset="0%" stop-color="${accent}" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="${accent}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="78%" cy="88%">
      <stop offset="0%" stop-color="#a9552b" stop-opacity="0.14"/>
      <stop offset="64%" stop-color="#a9552b" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  <rect width="${w}" height="${h}" fill="url(#glow1)"/>
  <rect width="${w}" height="${h}" fill="url(#glow2)"/>
  <text x="50%" y="48%" text-anchor="middle" fill="${accent}" opacity="0.35" font-family="Georgia,serif" font-size="${fontSize}" letter-spacing="0.15em">${label.toUpperCase()}</text>
  <text x="50%" y="54%" text-anchor="middle" fill="#8a8580" opacity="0.25" font-family="Helvetica Neue,sans-serif" font-size="${subSize}" letter-spacing="0.2em">CONTENT REQUIRED</text>
</svg>`;
}

let count = 0;
for (const p of placeholders) {
  const fullPath = join(PUBLIC, p.path);
  mkdirSync(join(fullPath, ".."), { recursive: true });
  writeFileSync(fullPath, generateSVG(p));
  count++;
  console.log(`  created ${p.path}`);
}

console.log(`\n  ${count} placeholder images generated.`);
