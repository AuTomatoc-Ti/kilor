# Kilor Tone & Prosody — System F (Revised)

**Module:** The Unified Prosody Engine
**Status:** Canonical (v4.0 — Toneless 1–2 Syllable Standard)
**Last updated:** 2026-08-09
**Version:** 2.2.1
**Depends on:**

---

## I. Core Philosophy

In Kilor, tone signals **word category** for words of 3+ syllables. For 1–2 syllable words, all categories are **toneless** — a bare root serves as both noun and verb, and the `-s` derivational suffix serves as both adjective and adverb. Disambiguation comes from syntactic position, colour prefixes, and context.

Tone patterns use two dedicated graphemes:

- **`j`** — High (H) tone
- **`v`** — Low (L) tone

These letters are **exclusively reserved** for tone notation on 3+ syllable words and never appear as consonants or vowels.

`j` and `v` are **extra-segmental tone annotations** — they carry no inherent segmental sound and float outside the syllable structure. They are purely tonal markers that overlay onto the vowel nucleus of their anchor syllable. A syllable like `auj` is a V nucleus (`au`) with a floating H tone, not a V+C sequence. See `0-foundation/phonology.md` §IV-A for the syllable-level treatment.

Tone is **immutable** in speech — a word's category is fixed at creation, and its tonal contour cannot be shifted for poetic or oratorical effect. Shifting the `j`/`v` marker would change the word's category, breaking intelligibility.

In song and metered poetry, a separate performance convention applies — see §IV-F (Musical Tone Override).

---

## II. The Category System

Kilor distinguishes **Noun, Verb, Adjective, and Adverb** through pitch contour for words of 3+ syllables. For 1–2 syllable words, all categories are **toneless** — the bare root serves as both noun and verb, and the `-s` derivational suffix marks both adjective and adverb.

---

### A. 3+ Syllable Words — Last-3 Domain

Only the **last 3 syllables** carry the tonal contour. All preceding syllables are **flat Mid (M)**. This ensures even rare 6+ syllable compounds adapt cleanly.

| Category | Last-3 Pattern | Marker | Marker Position (in last-3) |
|---|---|---|---|
| **Noun** | H(`j`) → M → L | `j` | 1st of last-3 |
| **Verb** | L(`v`) → H → M | `v` | 1st of last-3 |
| **Adjective** | M → H(`j`) → H | `j` | 2nd of last-3 |
| **Adverb** | M → L(`v`) → M | `v` | 2nd of last-3 |

Every (marker, position) pair is unique — the marker placement alone signals the category unambiguously.

**Extended examples:**

| Syl | Noun | Verb | Adjective | Adverb |
|---|---|---|---|---|
| 3 | H(`j`)→M→L | L(`v`)→H→M | M→H(`j`)→H | M→L(`v`)→M |
| 4 | M→**H(`j`)→M→L** | M→**L(`v`)→H→M** | M→**M→H(`j`)→H** | M→**M→L(`v`)→M** |
| 5 | M→M→**H(`j`)→M→L** | M→M→**L(`v`)→H→M** | M→M→**M→H(`j`)→H** | M→M→**M→L(`v`)→M** |
| 6+ | ...M→**H(`j`)→M→L** | ...M→**L(`v`)→H→M** | ...M→**M→H(`j`)→H** | ...M→**M→L(`v`)→M** |

---

### B. 1–2 Syllable Words — Toneless

All 1–2 syllable words in Kilor are **toneless** — pronounced with flat mid-tone. No `j` or `v` tone marker appears on any 1–2 syllable word.

The **bare root** serves as both noun and verb. The **`-s` suffixed form** serves as both adjective and adverb. Category is disambiguated by:

1. **Syntactic position** — adjectives precede nouns; adverbs precede verbs; nouns occupy argument slots; verbs occupy predicate slots
2. **Colour prefixes** — only nouns carry them; verbs do not
3. **Context** — discourse and semantics resolve remaining ambiguity

| Category | Form | Tone |
|---|---|---|
| **Noun** | Bare root | Toneless (flat mid) |
| **Verb** | Bare root | Toneless (flat mid) |
| **Adjective** | Bare root + `-s` | Toneless (flat mid) |
| **Adverb** | Bare root + `-s` | Toneless (flat mid) |

> **Example:** `fora` (bare root) = "fire" (noun) or "burn" (verb). `foras` (root + `-s`) = "fiery/burning" (adjective) or "burningly" (adverb).
> **Example:** `fei` (bare root) = "fly" (noun) or "fly" (verb). `feis` (root + `-s`) = "flying" (adjective) or "flyingly" (adverb).
> **Example:** `shuk` (bare root) = "fast" (quality root, category `a` in lexicon). `shuks` (root + `-s`) = "quickly" (manner adverb).

**Constraint:** No 1- or 2-syllable root may end in `s` natively. This preserves `-s` as an unambiguous modifier marker.

**Exception — `-es` allomorph:** A small set of grandfathered 1-syllable roots ending in `s` (`fos`, `gus`, `meus`, `rius`, `mlis`) take the epenthetic variant `-es` instead of `-s` for adjective/adverb forms. This follows the general Kilor schwa-epenthesis strategy (see `0-foundation/phonology.md` §V-F): inserting `e` /ə/ breaks the illegal geminate `-ss` that would otherwise result. Examples:

| Root | A/D form (not `*-ss`) | Gloss |
|------|----------------------|-------|
| `fos` | `foses` | icy, frozen |
| `gus` | `guses` | hot, hotly |
| `meus` | `meuses` | -ian, -ese, characteristic of |
| `rius` | `riuses` | similar, kind of |
| `mlis` | `mlises` | methodical, procedural |

The `-es` suffix adds one syllable (as in English bus→buses). New roots should not end in `s` — this exception exists solely for the five grandfathered forms.

---

## III. The `-s` Derivational Suffix

### A. Function

| Derivation | Result |
|---|---|
| Root + `-s` | Adjective (modifies nouns) & Adverb (modifies verbs) |

The `-s` suffix is the **only category marker** for 1–2 syllable words. It distinguishes modifiers (adj/adv) from arguments/predicates (noun/verb). The same `-s` form serves both adjective and adverb roles — position disambiguates: adjectives precede nouns, adverbs precede verbs (see `0-foundation/grammar-syntax.md` §I-E).

`s` applies only to **1–2 syllable** words. 3+ syllable words use tone pattern alone to distinguish all 4 categories.

> **Note:** "Quality roots" are roots whose lexical category in `lexicon.csv` is `a` (adjective). These roots describe attributes (e.g., big, small, warm, cold, fast, good) and derive manner adverbs via `-s`. The `a` category label is a lexicon-internal convention, not a grammatical term visible in speech.

### B. Phonological Nature

`s` is a **toneless extrasyllabic appendix** — pronounced like English plural `-s` (`/s/` or `/z/`). It:

- Does **not** add a syllable
- Does **not** affect the last-3 domain calculation
- Does **not** carry `j` or `v`
- Does **not** count toward syllable count for tone rules

---

## IV. Cross-Cutting Tonal Rules

### A. The Last-3 Domain Rule

For any word of 3+ syllables, **only the last 3 syllables** carry the tonal contour. All preceding syllables are pronounced flat Mid (M).

This ensures long compounds (6+ syllables) are tonally predictable — no recalculating contours across morpheme boundaries.

### B. The Tone Lock Rule

When a **case suffix** (Accusative `-ni`/`-na`, Genitive `-si`/`-sa`) is attached, case suffixes are **extrasyllabic for tone purposes** — they do not count toward the syllable count for the Last-3 Domain Rule.

For 3+ syllable roots: the tone marker (`j` or `v`) **never migrates**. It remains locked to its original syllable. Case suffixes are pronounced flat Mid.

For 1–2 syllable roots: there are no tone markers to lock. Case suffixes are simply appended as flat Mid appendices.

> **Crucial:** A 2-syllable root + case suffix (e.g., `fora` + Genitive `-si` → `forasi`) remains tonally a 2-syllable word (flat mid throughout, with `-si` as a flat appendix), not a 3-syllable word that would follow the Last-3 Domain.
>
> A 3-syllable root + case suffix keeps its Last-3 Domain contour with the suffix as a flat appendix on top.

### C. Colour Prefix Exemption

The **colour prefix** is an external proclitic. It is pronounced flat Mid and does **not** count toward the syllable count for the last-3 domain. Only the root's syllables are counted.

> **Example:** `a-` (red prefix, flat Mid) + `lumi sola` (2-syl noun + 2-syl noun, multi-word vocab) = `a-lumi sola`
> The colour prefix `a-` is flat Mid and attaches to the first word. Each word is toneless (flat mid).

### D. Modular Stitching (Multi-Word Vocabs)

When a semantic concept is expressed as **multiple orthographic words** (a multi-word vocab with spaces), each word is processed independently. The tonal contours are **stitched sequentially** across the word sequence, not recalculated as if the phrase were a single word.

This contrasts with mono-word compounds written as a single word — those use the Last-3 Domain Rule (§IV-A) recalculated across the entire word.

> **Example (toneless):** `lumi sola` (2-syl noun + 2-syl noun, two-word vocab) — each word is toneless (flat mid).
> **Example (3+ syllable):** `rujsome lunlavgak` (3-syl noun + 3-syl adv) — each word carries its own Last-3 contour independently.
> **Contrast:** If words were fused into a single word, the Last-3 Domain Rule would recalculate the contour across the entire compound.

### E. No Cross-Word Tone Sandhi

Identical contours may abut across word boundaries. Kilor permits this — musicality comes from rhythmic phrasing and syntactic structure, not forced phonetic alteration.

### F. Musical Tone Override

In song and metered poetry, the melody or rhythmic metre of the composition may override lexical tone contours. When a word is set to music, its tonal pattern can be flattened or reshaped to follow the musical line.

This is consistent with how tonal languages (Mandarin, Cantonese, Thai, Vietnamese) function in song — lexical tone is subordinated to melody when the two conflict. In Kilor, when tones are neutralised by music, word category is recovered from:

1. **Syntactic position** — word order and case suffixes (which remain mandatory in poetic registers) disambiguate role
2. **The `-s` derivational suffix** — audible even when tones are flattened, preserving the modifier/non-modifier distinction for 1–2 syllable words
3. **Colour prefixes** — ontological class provides additional semantic grounding

This is not a grammatical rule but a **performance convention**. No morphological changes, prefixes, or alternative spellings are required — the poet or composer simply prioritises the composition's melodic contour over lexical tone, and the grammar's existing redundancy carries the disambiguation burden.

### G. Tone Omission for Single-Category Words

Words of **any syllable count** whose **derivation mask has exactly one NVAD letter** (N, V, A, or D only) may **omit** their category marker (tone markers for 3+ syllable words; `-s`/`-es` suffix for 1–2 syllable words). Omission is **optional** but preferred. The bare root serves as the form for that single category.

Motivation: tone markers exist to disambiguate category. A word that can only be one category has no ambiguity to resolve — tone is redundant. The `-s` suffix (for 1–2 syllable words) and colour prefixes already provide partial disambiguation for listeners; syntactic position handles the rest.

| Mask | Example | With tone (allowed) | Without tone (preferred) |
|:---|:---|:---|:---|
| `n` | `austareus` (personal name) | `austajreus` (noun tone: `j` 1st of last-3) | `austareus` |
| `n` | `auronius` (personal name) | `aujronius` | `auronius` |
| `n` | `songeus` (personal name) | `songjeus` | `songeus` |
| `v` | (hypothetical verb-only term) | `takavnak` | `takavnak` or `takanak` |
| `a` | (hypothetical adj-only term) | `raljnikor` | `ralnikor` |
| `d` | (hypothetical adv-only term) | `shukvnali` | `shuknali` |

**Applies to:** words of any syllable count whose derivation mask is a single NVAD letter. For 3+ syllable words, tone markers are optional; for 1–2 syllable words, both bare root and `-s`/`-es` suffixed forms are acceptable (e.g., `meus` mask=`A`: both `meus` and `meuses`).

**Does not apply to:** words with 2+ mask letters (NV, NA, ND, AV, etc.) — these still require their category marker to disambiguate at runtime. Words with an empty mask (closed-class particles) are unaffected.

**Interaction with other rules:** the Colour Prefix Exemption (§IV-C), Tone Lock Rule (§IV-B), and Musical Tone Override (§IV-F) all apply to toneless forms exactly as they would to toned forms — the absence of `j`/`v` changes only the pitch contour of the word itself, not its prosodic relationship to prefixes, suffixes, or surrounding words.

---

---

*End of Tone & Prosody Specification (v4.0).*
