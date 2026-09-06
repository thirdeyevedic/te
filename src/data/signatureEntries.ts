/**
 * SIGNATURE ENTRIES — Moments that define the wedding before it begins.
 * These are experience products, never service cards.
 */

export interface SignatureEntry {
  slug: string;
  category: string;
  title: string;
  line: string;
  descriptor: string;
  /** Imagery path when supplied — public/ URL or imported asset */
  heroImage?: string;
  /** Video URL for cinematic playback */
  videoUrl?: string;
  /** Audio URL for sound identity */
  audioUrl?: string;
  sequence: { label: string; description: string }[];
  sound?: string;
  targetAudience: string;
  customizationOptions: string[];
  seoTitle: string;
  metaDescription: string;
}

export const signatureEntries: SignatureEntry[] = [
  {
    slug: "shiva-entry",
    category: "Majestic Power",
    title: "The Shiva Entry",
    line: "A powerful beginning, where energy takes form.",
    descriptor: "The groom doesn’t just arrive — he emerges like Shiva, surrounded by smoke, beats, and raw spiritual intensity.",
    heroImage: "/images/signature/shiva-entry-hero.jpg.svg",
    videoUrl: "/videos/shiva-entry-cinematic.mp4",
    audioUrl: "/audio/shiva-entry-sound-identity.mp3",
    sequence: [
      { label: "Silence Before the Storm", description: "Lights dim. Subtle ambient hum. Guests feel something is about to happen." },
      { label: "The First Beat", description: "A single Damru sound echoes followed by slow, deep percussion building tension." },
      { label: "The Emergence", description: "Smoke spreads across the pathway. Blue + gold lighting cuts through the haze. Silhouette appears." },
      { label: "The Revelation", description: "Groom steps forward slowly. Shiv Tandav-inspired soundscape. Light hits the face — full reveal." },
      { label: "The Ascension Walk", description: "Walk is slow, controlled, powerful. Trishul carriers, Rudraksha aesthetics, minimal entourage." },
      { label: "The Arrival", description: "Music drops into calm. Fire visible ahead. Transition from power to sacred ritual." },
    ],
    sound: "Deep damru pulses that vibrate through the chest · Shiv Tandav-inspired rhythmic builds · sub-bass frequencies designed for physical impact — felt before heard",
    targetAudience: "Couples wanting a bold, spiritually charged entrance — power over pageantry. Ideal for grooms who identify with strength, discipline and presence.",
    customizationOptions: [
      "Intensity level — from controlled emergence to full theatrical reveal",
      "Sound design — live damru performers or curated electronic soundscape",
      "Lighting palette — blue-gold, pure gold, or fire-orange tones",
      "Entourage scale — minimal trishul carriers to full procession",
    ],
    seoTitle: "The Shiva Entry — Majestic Power | Third Eye Events",
    metaDescription:
      "A baraat entry built on stillness, damru and fire — the Shiva Entry by Third Eye Events turns the groom's arrival into cinematic power.",
  },
{
    slug: "royal-entry",
    category: "Grand Heritage",
    title: "The Royal Entry",
    line: "Walk the path of kings before you take your vows.",
    descriptor: "A golden pathway unfolds lined with florals, lights and legacy. Every step echoes royalty, grace and timeless grandeur.",
    heroImage: "/images/signature/royal-entry-hero.jpg.svg",
    videoUrl: "/videos/royal-entry-cinematic.mp4",
    audioUrl: "/audio/royal-entry-sound-identity.mp3",
    sequence: [
      { label: "The Awakening of the Palace", description: "Warm golden lights slowly illuminate the pathway. Soft shehnai begins in background." },
      { label: "The Path of Gold", description: "Long floral + candle-lit walkway revealed. Symmetry, balance, perfection." },
      { label: "The Announcement", description: "Traditional instruments rise — shehnai + nagada, soft controlled. Optional shankh." },
      { label: "The Arrival", description: "Groom enters on horseback / vintage car / walking. Dressed in regal attire with elegant entourage." },
      { label: "The Royal Walk", description: "Slow, confident steps. Optional petal rain, chhatra, live classical performers." },
      { label: "The Throne Moment", description: "Groom reaches mandap/stage with slight elevation. Music softens into ritual." },
    ],
    sound: "Live shehnai flowing through corridors · soft nagada establishing rhythm · occasional shankh marking the arrival — each note placed with ceremonial precision",
    targetAudience: "Couples who want their entrance to feel like a royal procession — heritage, grandeur and ceremonial weight. Perfect for palace and fort venues.",
    customizationOptions: [
      "Arrival mode — horseback, vintage car, elephant, or walking procession",
      "Floral design — marigold heavy, rose-focused, or mixed seasonal",
      "Musical ensemble — solo shehnai, full nagada group, or fusion orchestra",
      "Royal accoutrements — chhatra, petal rain, guard of honour",
    ],
    seoTitle: "The Royal Entry — Grand Heritage | Third Eye Events",
    metaDescription:
      "Palace awakening, golden pathways and royal procession — the Royal Entry by Third Eye Events stages the baraat as living heritage.",
  },
{
    slug: "floral-entry",
    category: "Blissful",
    title: "The Floral Entry",
    line: "A moment where love is celebrated like a festival.",
    descriptor: "Petals fall. Music flows. The air itself feels alive. A joyful, vibrant entry where the bride/groom is welcomed like a celebration of life.",
    heroImage: "/images/signature/floral-entry-hero.jpg.svg",
    videoUrl: "/videos/floral-entry-cinematic.mp4",
    audioUrl: "/audio/floral-entry-sound-identity.mp3",
    sequence: [
      { label: "The Mood Shift", description: "Gentle live music begins — flute / violin / soft vocals. Atmosphere becomes warm, inviting." },
      { label: "The Blooming Path", description: "Floral arches, pastel drapes, soft flowing textures. Everything feels alive and moving." },
      { label: "The First Petals", description: "Light phoolon ki baarish begins. Slow, graceful, almost magical." },
      { label: "The Entrance", description: "Groom enters surrounded by dancers, live musicians, floral carriers. Movement fluid." },
      { label: "The Celebration Walk", description: "Dance, laughter, interaction. Guests become part of entry. Petals intensify." },
      { label: "The Bloom Peak", description: "Final heavy floral shower as they reach mandap. Music swells emotionally." },
      { label: "The Soft Landing", description: "Music transitions into calm melody. Energy settles into ritual." },
    ],
    sound: "Live flute or violin carrying warmth · acoustic vocals floating over light percussion · romantic instrumentals that build gently — sound as a blanket, not a broadcast",
    targetAudience: "Couples seeking joy without intensity — warmth, colour and celebration as a shared experience. Ideal for daylight ceremonies and garden venues.",
    customizationOptions: [
      "Floral palette — pastel, vibrant, or monochrome white",
      "Music format — solo instrumental, live band, or DJ with live vocals",
      "Petal delivery — manual phoolon ki baarish, cannon, or drone release",
      "Dance integration — flash mob, classical, or Bollywood choreography",
    ],
    seoTitle: "The Floral Entry — Blissful | Third Eye Events",
    metaDescription:
      "Petal falls, dancers and a pathway of flowers — the Floral Entry by Third Eye Events makes joy visible.",
  },
{
    slug: "celestial-entry",
    category: "Auspicious",
    title: "The Celestial Entry",
    line: "Not an entry… a descent from the divine.",
    descriptor: "Floating. Elevated. Surreal. A heavenly arrival designed with light, sound and sacred symbolism creating a moment beyond this world.",
    heroImage: "/images/signature/celestial-entry-hero.jpg.svg",
    videoUrl: "/videos/celestial-entry-cinematic.mp4",
    audioUrl: "/audio/celestial-entry-sound-identity.mp3",
    sequence: [
      { label: "The Stillness", description: "Complete silence or soft ambient drone. Lights dim into soft white/blue hues." },
      { label: "The Divine Sound", description: "Shankh echoes gently followed by temple bells and soft Vedic chants/alaap." },
      { label: "The Atmosphere Forms", description: "Mist spreads across the floor. Light beams cut through like dawn rays." },
      { label: "The Appearance", description: "Silhouette becomes visible above or within mist. Platform/pathway softly illuminated." },
      { label: "The Descent", description: "Couple enters slowly, extremely graceful, almost gliding. No sudden actions." },
      { label: "The Divine Walk", description: "Each step synced with music. Lighting follows like aura. Guests silent, absorbed." },
      { label: "The Union Point", description: "Light intensifies briefly. Chant peaks softly. Transition into ritual seamless and sacred." },
    ],
    sound: "Shankh resonance marking sacred space · temple bells creating depth · Vedic chants layered with ambient pads — sound designed to slow time itself",
    targetAudience: "Couples drawn to the divine and surreal — entrance as a spiritual event, not a performance. Best for evening ceremonies and temple-adjacent settings.",
    customizationOptions: [
      "Descent method — elevated platform, staircase, or mist-pathway emergence",
      "Sound layer — live Vedic chants, ambient score, or hybrid sacred-electronic",
      "Atmospheric effects — mist machines, light beams, flower petal rain",
      "Lighting temperature — cool dawn tones, warm firelight, or cosmic blue",
    ],
    seoTitle: "The Celestial Entry — Auspicious | Third Eye Events",
    metaDescription:
      "Shankh, temple bells, mist and descending light — the Celestial Entry by Third Eye Events opens the wedding with auspice.",
  },
];

export const getSignatureEntry = (slug: string) => signatureEntries.find((e) => e.slug === slug);
