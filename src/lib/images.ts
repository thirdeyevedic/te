/**
 * srcset — one place that turns a source image into a responsive candidate
 * list, so plain <img> tags (which cannot use the ExperienceImage component)
 * still get the width variants that scripts/make-responsive.py generates.
 *
 * The manifest is keyed by public path; a source with no entry (SVG, the
 * founder portrait) simply returns undefined and the caller falls back to a
 * plain src. Every candidate is checked on disk at build time, so a stale
 * manifest can never emit a 404.
 */
import { existsSync } from "node:fs";
import { join } from "node:path";
import srcsetManifest from "../data/srcset-manifest.json";

interface ManifestEntry {
  w: number;
  h: number;
  variants: number[];
}

const manifest = srcsetManifest as Record<string, ManifestEntry | undefined>;

export function buildSrcset(src?: string): string | undefined {
  if (!src) return undefined;
  const entry = manifest[src];
  if (!entry) return undefined;

  const candidates: string[] = [];
  for (const vw of entry.variants ?? []) {
    const candidate = src.replace(/\.jpg$/i, `@${vw}.jpg`);
    if (existsSync(join(process.cwd(), "public", candidate))) {
      candidates.push(`${candidate} ${vw}w`);
    }
  }
  candidates.push(`${src} ${entry.w}w`);

  return candidates.length > 1 ? candidates.join(", ") : undefined;
}
