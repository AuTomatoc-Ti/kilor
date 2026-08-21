# Kilor Lexicon & Developer Roadmap

**Module:** Word Formation, Constraints & Development Pipeline
**Status:** Canonical
**Last updated:** 2026-08-21
**Version:** 1.0.3
**Depends on:** `3-subsystems/spatials.md`

---

## I. Lexical Architecture

### A. Root Words

All roots in Kilor must satisfy the following constraints:

| Constraint | Rule |
|:---|:---|
| **Syllable count** | Typically 1 to 5 syllables per root (soft guideline; lexicalised forms may exceed) |
| **Syllable templates** | Strictly CV, CVC, VC, or V only |
| **Consonant clusters** | Forbidden — no CCV, CVCC, or any multi-consonant sequences |
| **`j` and `v`** | Must never appear as consonants or vowels |
| **Tone markers** | Only applied externally via `j`/`v`; never baked into the root spelling |

### B. Word Categories & Tone Patterns

Each root belongs to one of **four** categories. For 3+ syllable words, the tone pattern alone distinguishes them. For 1–2 syllable words, the derivational suffix `-s` creates adjective and adverb forms.

| Category | 1-Syl | 2-Syl | 3+ Syl (Last-3 Domain) | `-s` Derivation |
|:---|:---|:---|:---|:---|
| **Noun** | Toneless | Toneless | ...M→H(`j`)→M→L | — |
| **Verb** | Toneless | Toneless | ...M→L(`v`)→H→M | — |
| **Adjective** | Noun + `-s`, Toneless | Noun + `-s` | ...M→M→H(`j`)→H | from Noun |
| **Adverb** | Verb + `-s`, Toneless | Verb + `-s` | ...M→M→L(`v`)→M | from Verb |

> See `0-foundation/tone-prosody.md` for full contour rules, last-3 domain, and `-s` appendix rules.

---

## II. Compounding

### A. Mechanism

Vocabulary is expanded through **lexical compounding** — independent roots are combined to form complex concepts.

> **Example:** `lumi` (light) + `sola` (star) → `lumi sola` (star-light, multi-word vocab)

### B. Tone Processing — Mono-Words vs. Multi-Word Vocabs

Kilor distinguishes two forms of compounding for tone:

1. **Mono-word compounds** — roots fused into a single orthographic word. These are treated as a single word: the Last-3 Domain Rule applies across the entire word (see `0-foundation/tone-prosody.md` §IV-A).

2. **Multi-word vocabs** — two or more words written with spaces that together form one semantic concept (e.g., `lumi sola`, `auli lumi`). Each word retains its own tonal contour independently. The contours are **stitched sequentially** across the word sequence, not recalculated (see `0-foundation/tone-prosody.md` §IV-D).

   > **Example:** `auli lumi` (2-syl noun + 2-syl noun, two-word vocab) → toneless → toneless. Each word retains its own independent processing per `0-foundation/tone-prosody.md` §IV-D.

---

## III. Grammatical Mechanisms — Summary of Absence

Kilor intentionally **does not have** the following. All are handled analytically or contextually:

| Mechanism | How It's Handled Instead |
|:---|:---|
| **Grammatical tense** | Temporal words (yesterday, tomorrow, now); see `3-subsystems/temporals.md` |
| **Plural marking** | Context, quantifiers, numerals (Chinese-style); see `0-foundation/grammar-syntax.md` §VI |
| **Agglutinative possessive suffix** | Genitive case (`-si`/`-sa`); see `1-nominals/cases.md` §IV |
| **Agglutinative plural suffix** | Abolished; no equivalent |
| **Possessive pronouns** | Pronoun root + Genitive suffix |

---

## IV. Development Pipeline & Heuristics

For contributors (human or AI) extending the Kilor lexicon and grammar, follow this sequential pipeline:

### Step 1: Morphological Foundation

Define core roots ensuring:
- Strict compliance with CV/CVC/VC/V syllable templates
- No `j` or `v` in root spelling
- No consonant clusters
- **No 1- or 2-syllable root may end in `s` natively** — `-s` is reserved
- Each root assigned to its category (Noun / Verb / Adjective / Adverb) with corresponding tone pattern (see `0-foundation/tone-prosody.md`)

### Step 2: Lexical Generation

Generate roots across all **four** categories at multiple syllable lengths:
- **5 Noun roots** (1-syl, 2-syl, 3+ syl)
- **5 Verb roots** (1-syl, 2-syl, 3+ syl)
- **5 Adjective roots** (3+ syl — for 1/2 syl, derive via Noun + `-s`)
- **5 Adverb roots** (3+ syl — for 1/2 syl, derive via Verb + `-s`)

Verify that 1- and 2-syllable noun and verb roots combined with `-s` produce valid adjective/adverb forms. Run constraint checks on every root.

### Step 3: Compounding Matrix

Create 5 compound words (e.g., 2-syl + 2-syl combinations, or 3-syl + 2-syl). Include both mono-word compounds and multi-word vocabs. Verify:
- **Mono-word compounds:** Last-3 Domain Rule applies across the entire word (recalculated, not stitched)
- **Multi-word vocabs:** Each word keeps its own last-3 domain, stitched sequentially across word boundaries
- Colour prefixes apply only to noun Word-Units

### Step 4: Syntactic Testing

Construct 5 SOV sentences using the generated lexicon.
- **Target structure:** [ColourPrefix-Noun] [ColourPrefix-Noun-Accusative] [Adverb] [Verb]
- Test SOV (default), OSV, and VSO orders — verify case suffixes disambiguate correctly
- Test `-s` derivation in context: adjective modifying noun, adverb modifying verb

### Step 5: Acoustic Simulation

Read the sentences aloud. Evaluate:
- **Rhythmic smoothness:** No consonant clusters should mean the rhythm feels percussive and fluid
- **Melodic arc:** The stitched contours should feel natural — not monotonous, not chaotic
- **Physical ease:** Adjust root vowel choices if articulation feels overly labored

---

## V. Reserved & Future Work

| Area | Status |
|:---|:---|
| **Article morphology / Demonstratives** (a/an/the, this/that) | **Defined** — expressed through the colour prefix system itself; see `1-nominals/nouns-colour-prefix.md` §IV |
| **Pronoun inventory** | **Defined** — see `1-nominals/pronouns.md` |
| **Numeral & classifier system** | **Defined** — see `3-subsystems/numerals.md` |
| **Temporal word inventory** | **Defined** — see `3-subsystems/temporals.md` |
| **1-syllable noun & verb roots** | Deferred — atomic roots needed as base for `-s` adjective/adverb derivation |
| **2-syllable noun & verb roots** | Deferred — needed as base for `-s` adjective/adverb derivation; must not end in `s` |
| **Dative/Instrumental particle inventory** | **Defined** — see `1-nominals/cases.md` §V: `te` (to/for; also spatial root), `mer` (with), `sy` (by/using), `ar` (from), `tilpe` (between). Spatial postpositions via `-ne` suffix: see `3-subsystems/spatials.md`. Conjunctions: `ei` (and), `po` (or), `amer` (but) |
| **Interrogative structure** | **Defined** — see `2-predication/interrogative.md` |
| **Negation** | **Defined** — see `2-predication/negation.md` |

---

*End of Lexicon & Roadmap Specification.*