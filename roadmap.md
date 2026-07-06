# Kilor Development Roadmap

**Status:** Active
**Last Updated:** 2026-07-06

---

## Target

| Goal | Roots | Derived (×2.5) | Compounds (×1) | Total Words | English Equivalent |
|---|---|---|---|---|---|
| **Fluent non-native** (>10k) | 3,000 | 7,500 | 3,000 | 10,500 | B2/C1 speaker |
| **Complete** (>20k) | 6,000 | 15,000 | 6,000 | 21,000 | University-educated adult |
| **Upper aspirational** (>30k) | 8,600 | 21,500 | 8,600 | 30,100 | Shakespeare-range active vocabulary |

**Primary target: 6,000 roots → 21,000 words.** Aspirational ceiling: 8,600 roots.

### Multiplier Explanation

- **×2.5 derived:** Average of 2.5 productive surface forms per root. Not all roots fill all 4 categories (N/V pair ~10% = 4 forms; noun-only ~45% = ~2 forms; verb-only ~35% = ~2 forms; quality-only ~10% = ~1.5 forms). Weighted average ≈ 2.5.
- **×1 compounds:** Roughly one lexicalised compound per root. Compounds are not automatic — each must be **manually coined and defined**. Compounding is modeled on Mandarin (~50–70% of vocabulary is compounds) but conservatively estimated at 1 compound per root.
- **Total multiplier: ×3.5**

### English Benchmarks

| Tier | Count | What It Is |
|---|---|---|
| OED total entries | ~170,000 | Includes obsolete, dialectal, all inflected forms — no human knows this many |
| College-educated passive | ~30,000–40,000 | Words recognised but not actively used |
| **Active vocabulary (target)** | **~20,000–30,000** | Words actually used in speech/writing |
| Core daily 90%+ coverage | ~5,000 | Words that cover most everyday conversation |

Kilor targets **active vocabulary**, not dictionary total. 6,000 roots → 21,000 words matches a university-educated English speaker's active vocabulary.

---

## Current State

| Asset | Count |
|---|---|
| Bare roots (validated) | 76 |
| Surface word forms (4-category expansion) | ~190 |
| Compounds (defined) | 0 |
| Rule files (foundation) | 13 |
| Progress toward 6,000 target | 1.3% |
| Completed in this session | Phonotactic audit, `fojra` rename, `wino` colour system, copula/existential spec (`res`/`ero`), closed-class `-s` exemption, 4-category expansion table, `roli` added, numeral system (`num.md`), ordinal `dir`, NP quantification order, subordination (`subordination.md`), oblique particle inventory (`mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus`) |

---

## Grammar Gaps (Before Large-Scale Lexicon Work)

| # | Gap | Priority | Why |
|---|---|---|---|
| 1 | ~~Numeral & classifier system~~ | ✅ Resolved | `rules/num.md` — base-10, 0–13 irregular, scale markers (`gau`/`cu`/`kas`/`hus`/`tus`/`rakas`), multiplicative + additive, no taxonomic classifiers, ordinal `dir`, NP order `NOUN — (MEASURE) — NUM — (ORD)` |
| 2 | ~~Subordinate clauses & relativization~~ | ✅ Resolved | `rules/foundation/subordination.md` — postnominal `kus` (relative/complement), `tu`/`li`/`aiga`/`hoskar` (adverbial). Full oblique particle + conjunction inventory in `cases.md` §V |
| 3 | **Temporal word inventory** | 🟡 High | "yesterday", "tomorrow", "always", "never" — needed for tense-free time expression |
| 4 | **Comparatives & superlatives** | 🟡 Medium | "bigger", "biggest", "more beautiful than" |
| 5 | **Passive voice or equivalent** | 🟢 Low | Can be handled by OSV word order + mandatory cases; may not need dedicated grammar |

---

## Lexicon Phased Expansion

Each phase produces both **roots** and **compound words**. Compounds are not automatically generated — each compound must be manually coined with its own meaning, usage notes, and (for nouns) a 共識 colour prefix. A compound is a dictionary entry just like a root.

### Phase 0: Grammar Completion (now → near-term)
- ~~Define numeral system and numerals 0–10, hundred, thousand~~ ✅ Done — see `rules/num.md`
- ~~Design subordination (relative clauses, complement clauses, adverbial clauses)~~ ✅ Done — see `rules/foundation/subordination.md`
- Fill core temporal words (yesterday, tomorrow, always, never, soon, late, early, again)
- **Root target:** 76 → ~80 (+4 temporal roots)
- **Compound target:** ~10 core compounds from existing roots

### Phase 1: Basic Daily (→500 roots, →1,750 words)
- Target: **76 → 500 roots**
- Categories to fill:
  - Body parts (head, foot, leg, arm, face, nose, tongue, skin, bone, heart)
  - Family/people (mother, father, child, sibling, man, woman, baby, chief)
  - Daily actions (sit, sleep, run, swim, fly, fall, cut, hit, push, pull, carry, open, close, wash, wear, buy, sell, work, play, sing, write, read)
  - Food/clothing/shelter (bread, meat, fruit, vegetable, cup, table, chair, bed, shirt, shoe, wall, roof, window)
  - More qualities (beautiful, ugly, strong, weak, wet, dry, heavy, light, full, empty, clean, dirty, sweet, bitter)
  - Nature/weather (rain, snow, ice, cloud, thunder, lake, sea, forest, field, sand)
  - Directions/position (up, down, left, right, front, back, inside, outside, near, far, above, below)
  - Tools/transport (boat, cart, rope, hammer, needle, pot, basket)
  - Social (help, thank, greet, promise, gift, war, peace, law, teach, learn)
- **Compound target:** ~400 compounds manually defined from the expanded root set
- Comparable to: ~3-year-old child vocabulary

### Phase 2: Functional (→1,000 roots, →3,500 words)
- Target: **500 → 1,000 roots**
- Fill gaps discovered during Phase 1 sentence-building
- More action verbs, more specific qualities, cultural terms tied to the 7 dual-concepts
- **Compound target:** ~500 compounds
- Comparable to: tourist-level functional language

### Phase 3: Fluent Non-Native (→3,000 roots, →10,500 words)
- Target: **1,000 → 3,000 roots**
- Major expansion across all domains
- Systematic semantic grids: body systems, emotion nuance, social roles, nature taxonomy
- Start of domain-specific vocabulary (basic math, basic physics, basic law)
- **Compound target:** ~2,000 compounds
- Comparable to: B2/C1 non-native speaker — fluent daily life + simple professional
- **Milestone: crosses 10,000 total words**

### Phase 4: Professional (→4,500 roots, →15,750 words)
- Target: **3,000 → 4,500 roots**
- Full professional/academic vocabulary:
  - Physics (force, mass, energy, wave, field, particle, velocity)
  - Biology (organ systems, species categories, cell, gene, growth stages)
  - Mathematics (plus, minus, multiply, divide, angle, shape names, set, function)
  - Medicine (disease, heal, wound, fever, poison, cure)
  - Law/governance (judge, contract, right, duty, crime, punish, inherit)
  - Technology (machine, engine, wire, signal, compute — mostly compounds)
- **Compound target:** ~3,000 compounds
- Comparable to: strong professional writing across fields

### Phase 5: Complete (→6,000 roots, →21,000 words)
- Target: **4,500 → 6,000 roots**
- Literature and poetry: aesthetic terms, rhetorical devices, emotion nuance
- Dialectal, archaic, and poetic variants
- Comprehensive domain coverage
- **Compound target:** ~4,500 compounds
- Comparable to: university-educated native speaker
- **Milestone: crosses 20,000 total words**

### Phase 6: Upper Aspirational (→8,600 roots, →30,100 words)
- Target: **6,000 → 8,600 roots**
- Edge cases, rare concepts, highly specific terminology
- Historical/archaic roots
- **Compound target:** ~6,000 compounds
- Comparable to: Shakespeare-range active vocabulary
- **Milestone: crosses 30,000 total words**

---

## Root Estimate Matrix

| Scope | Roots | Derived (×2.5) | Compounds (×1) | Total Words | English Equivalent |
|---|---|---|---|---|---|
| Phase 1 — Basic daily | 500 | 1,250 | 500 | 1,750 | Child (~3 yr) |
| Phase 2 — Functional | 1,000 | 2,500 | 1,000 | 3,500 | Tourist-level |
| Phase 3 — Fluent non-native | 3,000 | 7,500 | 3,000 | 10,500 | B2/C1 speaker |
| Phase 4 — Professional | 4,500 | 11,250 | 4,500 | 15,750 | Professional writing |
| Phase 5 — Complete (lower) | 6,000 | 15,000 | 6,000 | 21,000 | University-educated |
| Phase 6 — Complete (upper) | 8,600 | 21,500 | 8,600 | 30,100 | Shakespeare-range |

**Note:** Compounds must be manually coined and defined. They are not automatic. Each compound is a dictionary entry with its own meaning, usage, and (for nouns) 共識 prefix.

---

## Process Infrastructure (Needed Before Phase 3+)

| Need | Description |
|---|---|
| **Root database** | `.csv` or structured format for search, dedup, collision checking |
| **Compound dictionary** | Separate inventory of all defined compounds with meanings and 共識 prefixes |
| **Constraint validator** | Script to check new roots against phonotactics before acceptance |
| **Compounding style guide** | Rules for idiomatic vs compositional compounds; canonical multi-word vocab format |
| **Etymology convention** | Kilor-internal etymologies for consistency across roots and compounds |

---

## Key Design Decisions (from this session)

| Decision | Detail |
|---|---|
| Fire root: `fora` → `fojra` (H→L noun) | `kojra` renamed globally; 50 occurrences in 6 files |
| Colour vocabulary: `wino` | One root meaning "colour/hue"; 7 colours = prefix + `wino` |
| Copula: `res` | 1-syl toneless closed-class verb (是); identity/attribution |
| Existential/Possession: `ero` | 2-syl L→H → `evro` (有); Chinese unified model |
| Closed-class `-s` exemption | `res`, `nar`, `iu`, `na`, `te`, `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus` exempt from `-s` constraint (`grammar-syntax.md` §IV-C) |
| `roli` | 2-syl quality root = "lot / many" |

---

## Files

| File | Purpose |
|---|---|
| `rules/foundation/phonology.md` | Sound system, syllable templates |
| `rules/foundation/tone-prosody.md` | 4-category tone system |
| `rules/foundation/cases.md` | 3-case system (NOM/ACC/GEN) |
| `rules/foundation/grammar-syntax.md` | SOV order, compounding, `-s` derivation, plural/tense strategy |
| `rules/foundation/nouns-colour-prefix.md` | 7-colour prefix system, definiteness, 共識 |
| `rules/foundation/philosophy.md` | 7 dual-concepts mapped to colours |
| `rules/foundation/pronouns.md` | Pronoun inventory & declension |
| `rules/foundation/interrogative.md` | Wh-questions + yes/no (`wei` + `iu`) |
| `rules/foundation/negation.md` | `nar`, `na`, `iu` system |
| `rules/foundation/copula-existential.md` | `res` (是) + `ero` (有) |
| `rules/foundation/lexicon-roadmap.md` | Root constraints, development pipeline |
| `rules/foundation/subordination.md` | Relative clauses, complement clauses, adverbial clauses |
| `rules/lexicon-roots.md` | 76 bare roots with English meanings (manual fill-in template) |
| `rules/lexicon-expanded.md` | 76 roots × 4 categories with tone markers & 共識 prefixes |
| `question.md` | Deferred design questions (stale — several completed) |
| `draft/colour-kilor.txt` | Original philosophy notes for the 7-colour system |

---

*End of Roadmap.*