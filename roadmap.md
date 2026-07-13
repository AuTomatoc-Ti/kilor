# Kilor Development Roadmap

**Status:** Grammar complete — Phase 1 root creation underway
**Last Updated:** 2026-07-13

---

## Target

| Goal | Roots | Derived (×2.5) | Compounds (×1) | Total Words | English Equivalent |
|---|---|---|---|---|---|
| **Fluent non-native** (>10k) | 3,000 | 7,500 | 3,000 | 10,500 | B2/C1 speaker |
| **Complete** (>20k) | 6,000 | 15,000 | 6,000 | 21,000 | University-educated adult |
| **Upper aspirational** (>30k) | 8,600 | 21,500 | 8,600 | 30,100 | Shakespeare-range active vocabulary |

**Primary target: 6,000 roots → 21,000 words.** Aspirational ceiling: 8,600 roots.

### Multiplier Explanation

Steady-state targets (mature lexicon, Phase 3+):

- **×2.5 derived:** Average of 2.5 productive surface forms per root (N/V pairs produce 4 forms; noun-only ~2 forms; verb-only ~2 forms; quality-only ~1.5 forms).
- **×1 compounds:** Roughly one lexicalised compound per root, each manually coined and defined. Modeled on Mandarin (~50–70% of vocabulary is compounds), conservatively estimated.
- **Total multiplier: ×3.5**

Current Phase 1 baseline (241 roots, 2026-07-13):

| Metric | Roadmap (steady-state) | Current | Notes |
|---|---|---|---|
| Derived multiplier | ×2.5 | **×2.06** | 30% N-only roots drag average; more verbs/qualities in remaining Phase 1 targets will improve this |
| Compound ratio | ×1.0/root | **×0.30/root** | Expected early-stage effect — compound space grows combinatorially with root count |
| Total multiplier | ×3.5 | **×2.59** | Excluding function words: ×2.36 |

The current under-estimation is **temporal**, not structural. As more action verbs (VAD) and qualities (AD) enter the lexicon, the derived multiplier will rise. Compound density naturally increases as root count grows — compounds are coined from existing roots, so the ratio accelerates through Phase 2–3.

### English Benchmarks

| Tier | Count | What It Is |
|---|---|---|
| OED total entries | ~170,000 | Includes obsolete, dialectal, all inflected forms |
| College-educated passive | ~30,000–40,000 | Words recognised but not actively used |
| **Active vocabulary (target)** | **~20,000–30,000** | Words actually used in speech/writing |
| Core daily 90%+ coverage | ~5,000 | Words that cover most everyday conversation |

Kilor targets **active vocabulary**. 6,000 roots → 21,000 words matches a university-educated English speaker's active vocabulary.

---

## Grammar Foundation

All core grammar is designed and codified. No blocking design questions remain. See `question.md` for a summary.

| Domain | File |
|---|---|
| Sound system | `rules/foundation/phonology.md` |
| Tone & prosody | `rules/foundation/tone-prosody.md` |
| 3-case system (NOM/ACC/GEN) | `rules/foundation/cases.md` |
| Word order, compounding, derivations | `rules/foundation/grammar-syntax.md` |
| 7-colour prefix system | `rules/foundation/nouns-colour-prefix.md` |
| Pronoun inventory | `rules/foundation/pronouns.md` |
| Interrogative | `rules/foundation/interrogative.md` |
| Negation | `rules/foundation/negation.md` |
| Copula & existential | `rules/foundation/copula-existential.md` |
| Subordination & relativization | `rules/foundation/subordination.md` |
| Numeral system | `rules/num.md` |

---

## Lexicon Phased Expansion

Each phase produces both **roots** and **compound words**. Compounds are not automatically generated — each must be manually coined with a defined meaning, usage notes, and (for nouns) a 共識 colour prefix. Wordlist reference files in `wordlist/` provide English-meaning targets organized by semantic category.

---

### Phase 1: A1 — Beginner (→ ~500 roots, → ~1,750 words)

**Comparable to:** ~3-year-old child vocabulary. CEFR A1 — basic survival phrases and familiar everyday expressions.

| Category | What's Covered |
|---|---|
| **Body parts** | head, foot, leg, arm, face, nose, tongue, skin, bone, heart, ear, mouth, eye, hand |
| **Family & people** | mother, father, child, sibling, brother, sister, son, daughter, man, woman, baby, chief, friend, enemy |
| **Daily actions** | sit, sleep, run, swim, fly, fall, cut, hit, push, pull, carry, open, close, wash, wear, buy, sell, walk, work, play, sing, dance, write, read |
| **Food & drink** | bread, meat, fruit, vegetable, salt, sugar, milk, egg, rice, soup, oil, wine, beer |
| **Clothing & home** | shirt, shoe, hat, dress, cloth; door, wall, roof, window, room, bed, chair, table, cup, plate, pot, basket, box, bag, key, lock, fire, light |
| **Basic qualities** | beautiful, ugly, strong, weak, soft, hard, wet, dry, heavy, light, full, empty, clean, dirty, sweet, bitter, sour, sharp, blunt, round, flat, thick, thin, deep, shallow; plus: true/false, same/different, ready/tired, hungry/thirsty, sick/healthy, alive/dead, free/busy, safe/dangerous, easy/difficult, possible/impossible, important, rich/poor, young |
| **Nature & weather** | rain, snow, ice, cloud, thunder, wind, storm, river, lake, sea, ocean, forest, field, sand, island, wave, water, stone, earth, sky, sun, moon, star, tree, flower |
| **Animals** | dog, cat, horse, cow, sheep, pig, snake, insect |
| **Directions & position** | up, down, left, right, front, back, inside, outside, near, far, above, below, beside, between, north, south, east, west |
| **Tools & transport** | boat, cart, rope, hammer, needle, knife, stick, wheel, bridge |
| **Social** | help, thank, greet, promise, gift, war, peace, law, rule, teach, learn, study, question, answer, story, joke, game, music, song, dance |

---

### Phase 2: A2 — Elementary (→ ~1,000 roots, → ~3,500 words)

**Comparable to:** Tourist-level functional language. CEFR A2 — can describe in simple terms aspects of immediate environment and routine needs.

Fills gaps discovered during Phase 1 sentence-building. Expands action verbs, adds more specific qualities, and introduces cultural terms tied to the 7 dual-concepts. Learners can handle simple, direct exchanges on familiar topics.

---

### Phase 3: B1/B2 — Intermediate (→ ~3,000 roots, → ~10,500 words)

**Comparable to:** B1 (Threshold) — can deal with most situations likely to arise while travelling; B2 (Vantage) — can produce clear, detailed text on a wide range of subjects.

Systematic semantic grids across body systems, emotion nuance, social roles, and nature taxonomy. Begins domain-specific vocabulary for basic math, basic physics, and basic law. Learners can interact with a degree of fluency and spontaneity.

**Milestone: crosses 10,000 total words.**

---

### Phase 4: C1 — Advanced (→ ~4,500 roots, → ~15,750 words)

**Comparable to:** Strong professional writing. CEFR C1 — can use language flexibly and effectively for social, academic, and professional purposes.

Full professional and academic vocabulary:

| Domain | Topics |
|---|---|
| **Physics** | force, mass, energy, wave, field, particle, velocity |
| **Biology** | organ systems, species categories, cell, gene, growth stages |
| **Mathematics** | plus, minus, multiply, divide, angle, shape names, set, function |
| **Medicine** | disease, heal, wound, fever, poison, cure |
| **Law & governance** | judge, contract, right, duty, crime, punish, inherit |
| **Technology** | machine, engine, wire, signal, compute (mostly compounds) |

---

### Phase 5: C2 — Proficient (→ ~6,000 roots, → ~21,000 words)

**Comparable to:** University-educated native speaker. CEFR C2 — can express spontaneously, very fluently and precisely, differentiating finer shades of meaning.

Literature and poetry vocabulary: aesthetic terms, rhetorical devices, emotion nuance. Dialectal, archaic, and poetic variants. Comprehensive domain coverage. Can summarise information from different spoken and written sources and reconstruct arguments coherently.

**Milestone: crosses 20,000 total words. Primary target reached.**

---

### Phase 6: Near-Native / Literary (→ ~8,600 roots, → ~30,100 words)

**Comparable to:** Shakespeare-range active vocabulary. Beyond formal CEFR scales — the vocabulary range of a highly literate native speaker with command of rare, archaic, and domain-specific terminology.

Edge cases, rare concepts, highly specific terminology. Historical and archaic roots. Comparable to the active vocabulary of a major literary figure.

**Milestone: crosses 30,000 total words.**

---

## Root Estimate Matrix

| Phase | Level | Roots | Derived (×2.5) | Compounds (×1) | Total Words | English Equivalent |
|---|---|---|---|---|---|---|
| Phase 1 | A1 Beginner | ~500 | ~1,250 | ~500 | ~1,750 | Child (~3 yr) |
| Phase 2 | A2 Elementary | ~1,000 | ~2,500 | ~1,000 | ~3,500 | Tourist-level |
| Phase 3 | B1/B2 Intermediate | ~3,000 | ~7,500 | ~3,000 | ~10,500 | Fluent daily life + simple professional |
| Phase 4 | C1 Advanced | ~4,500 | ~11,250 | ~4,500 | ~15,750 | Professional writing |
| Phase 5 | C2 Proficient | ~6,000 | ~15,000 | ~6,000 | ~21,000 | University-educated native |
| Phase 6 | Literary | ~8,600 | ~21,500 | ~8,600 | ~30,100 | Shakespeare-range |

**Note:** Compounds must be manually coined and defined. Each compound is a dictionary entry with its own meaning, usage, and (for nouns) 共識 prefix.

---

## Process Infrastructure

| Tool / Asset | Purpose |
|---|---|
| `lexicon.csv` | Root database — structured format for search, dedup, collision checking |
| `kilor.py` | Constraint validator — checks new roots against phonotactics |
| `wordlist/` | English-meaning targets organized by semantic category |
| Compound dictionary | (Future) Separate inventory of all defined compounds with meanings and 共識 prefixes |
| Compounding style guide | (Future) Rules for idiomatic vs compositional compounds |
| Etymology convention | (Future) Kilor-internal etymologies for consistency |

---

*End of Roadmap.*