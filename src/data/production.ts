/**
 * PRODUCTION FACILITATION — Behind every frame.
 * Third Eye acts as execution partner and network enabler,
 * not a direct film studio. [POSITIONING PER SOURCE]
 */

export interface ProductionService {
  id: string;
  name: string;
  capabilities: string[];
  note: string;
}

export const productionServices: ProductionService[] = [
  {
    id: "feature-films",
    name: "Feature Films",
    capabilities: ["Location coordination", "Crew management", "Equipment logistics", "Schedule execution"],
    note: "Long-form complexity handled on the ground.",
  },
  {
    id: "short-films",
    name: "Short Films",
    capabilities: ["Fast production cycles", "Workflow optimization"],
    note: "Small crews, sharp turnarounds.",
  },
  {
    id: "documentaries",
    name: "Documentaries",
    capabilities: ["Adaptability", "Coordination", "Real environments"],
    note: "Reality does not reschedule. We adjust.",
  },
  {
    id: "digital-content",
    name: "YouTube / Digital",
    capabilities: ["Volume", "Consistency", "Efficiency"],
    note: "Content pipelines that keep publishing honest.",
  },
  {
    id: "branded-content",
    name: "Branded Content",
    capabilities: ["Brand alignment", "Quality control"],
    note: "The brand's voice, protected frame by frame.",
  },
  {
    id: "ad-shoots",
    name: "Ad Shoots",
    capabilities: ["Speed", "Precision", "Deadline discipline"],
    note: "One day. Every department on time.",
  },
];

/** Execution network graph — the infrastructure behind facilitation */
export const productionNetwork: { label: string }[] = [
  { label: "Directors" },
  { label: "DOPs" },
  { label: "Production Teams" },
  { label: "Equipment Partners" },
  { label: "Location Network" },
  { label: "Vendors" },
  { label: "On-Ground Execution" },
];

