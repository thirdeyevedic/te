/**
 * WEDDING CONCEPTS — "Wedding Worlds"
 * Locations are common. Concepts create emotion.
 *
 * Semantic families group concepts by the emotion they carry.
 * Meanings below are literal translations of the supplied concept names.
 */

export interface ConceptFamily {
  id: string;
  family: string;
  essence: string;
  concepts: { name: string; meaning: string }[];
}

export const conceptFamilies: ConceptFamily[] = [
  {
    id: "royal",
    family: "Royal",
    essence: "Heritage lived at grand scale — lineage, court and crown.",
    concepts: [
      { name: "Rajsi Vivaah", meaning: "A royal wedding — grandeur rooted in heritage." },
      { name: "Veer Vivaah", meaning: "The warrior’s union — courage honoured." },
      { name: "Darbar Vivaah", meaning: "A wedding held as a royal court assembly." },
      { name: "Vansh Vivaah", meaning: "The lineage wedding — two families, one future." },
      { name: "Shahi Noor Vivaah", meaning: "The radiance of royalty." },
    ],
  },
  {
    id: "nature",
    family: "Nature",
    essence: "The earth itself as witness, mandap and blessing.",
    concepts: [
      { name: "Prakriti Vivaah", meaning: "Union within nature — the wild as witness." },
      { name: "Van Vivaah", meaning: "The forest wedding." },
      { name: "Vanam Vivaah", meaning: "Amid groves — green, living sanctuary." },
      { name: "Vanprastha Vivaah", meaning: "The forest-stage wedding — retreat into stillness." },
      { name: "Sahaj Vivaah", meaning: "Effortless naturalness — simplicity as luxury." },
    ],
  },
  {
    id: "elemental",
    family: "Elemental",
    essence: "Fire, water, snow, air — the panch tatva as sacrament.",
    concepts: [
      { name: "Agni Tatva Vivaah", meaning: "Marriage witnessed by the element of fire." },
      { name: "Agni Sanskar Vivaah", meaning: "The sacred rite centred on Agni." },
      { name: "Agni-Him Vivaah", meaning: "Fire and snow — opposing elements in one union." },
      { name: "Panch Tatva Vivaah", meaning: "The five elements as wedding witnesses." },
      { name: "Agni & Jal Vivaah", meaning: "Fire and water — union of opposites." },
    ],
  },
  {
    id: "cosmic",
    family: "Cosmic",
    essence: "Vows written against stars, silence and infinity.",
    concepts: [
      { name: "Nakshatra Vivaah", meaning: "Under the constellations — cosmic timing." },
      { name: "Sakshi Vivaah", meaning: "The witness wedding — presence above spectacle." },
      { name: "Chaitanya Vivaah", meaning: "Union in pure consciousness." },
      { name: "Anant Sakshi Vivaah", meaning: "Witnessed by the infinite." },
    ],
  },
  {
    id: "spiritual",
    family: "Spiritual",
    essence: "The Vaidik core — mantra, silence and inner stillness.",
    concepts: [
      { name: "Kashi Vivaah", meaning: "Union in the eternal city." },
      { name: "Ved Vivaah", meaning: "Marriage conducted wholly in Vaidik tradition." },
      { name: "Ashram Vivaah", meaning: "A wedding in the discipline of the hermitage." },
      { name: "Shuddh Sanskar Vivaah", meaning: "The pure rite — satvik in every detail." },
      { name: "Shanti Vivaah", meaning: "Peace as the foundation of union." },
      { name: "Maun Vivaah", meaning: "The vow of quiet — minimal words, deep meaning." },
      { name: "Chintan Vivaah", meaning: "Contemplation woven into ceremony." },
    ],
  },
  {
    id: "journey",
    family: "Journey",
    essence: "Marriage framed as movement — pilgrimage, passage, becoming.",
    concepts: [
      { name: "Vivaah Yatra", meaning: "The wedding journey itself." },
      { name: "Jeevan Yatra Vivaah", meaning: "Marriage as the beginning of life’s journey." },
      { name: "Marg Darshan Vivaah", meaning: "Guidance of the path — blessings for the road ahead." },
      { name: "Anveshan Vivaah", meaning: "The seeking wedding — discovery as ritual." },
      { name: "Mukt Vivaah", meaning: "Free from convention — liberation in form." },
    ],
  },
];
