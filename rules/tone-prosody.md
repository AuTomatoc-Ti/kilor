# Kilor Tone & Prosody — System F (Revised)

**Module:** The Unified Prosody Engine
**Status:** Canonical (v3.0 — 1-Syllable Toneless Standard)

---

## I. Core Philosophy

In Kilor, tone signals **word category**, not part of speech in isolation. Patterns use two dedicated graphemes:

- **`j`** — High (H) tone
- **`v`** — Low (L) tone

These letters are **exclusively reserved** for tone notation and never appear as consonants or vowels.

`j` and `v` are **extra-segmental tone annotations** — they carry no inherent segmental sound and float outside the syllable structure. They are purely tonal markers that overlay onto the vowel nucleus of their anchor syllable. A syllable like `auj` is a V nucleus (`au`) with a floating H tone, not a V+C sequence. See `phonology.md` §IV-A for the syllable-level treatment.

Tone is **immutable** in speech — a word's category is fixed at creation, and its tonal contour cannot be shifted for poetic or oratorical effect. Shifting the `j`/`v` marker would change the word's category, breaking intelligibility.

In song and metered poetry, a separate performance convention applies — see §IV-F (Musical Tone Override).

---

## II. The 4 Category Patterns

Kilor distinguishes **Noun, Verb, Adjective, and Adverb** through pitch contour for words of 2+ syllables. For 1-syllable words, all categories are **toneless** — category is distinguished by distinct roots and the `-s` derivational suffix.

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

### B. 2-Syllable Words

Only Noun and Verb carry distinct tone patterns. Adjective and Adverb are derived from them via `-s`.

| Category | Pattern | Suffix | Derived From |
|---|---|---|---|
| **Noun** | H(`j`) → L | — | — |
| **Verb** | L(`v`) → H | — | — |
| **Adjective** | H(`j`) → L | `-s` | Noun form + `-s` |
| **Adverb** | L(`v`) → H | `-s` | Verb form + `-s` |

> **Example:** `aujli` (noun, H→L) → `aujlis` (adj). `auvli` (verb, L→H) → `auvlis` (adv).

**Constraint:** No 1- or 2-syllable root may end in `s` natively. This preserves `-s` as an unambiguous modifier marker.

---

### C. 1-Syllable Words — Toneless

All 1-syllable words in Kilor are **toneless** — pronounced with flat mid-tone. No 1-syllable word carries a `j` or `v` tone marker.

| Category | Form | Tone |
|---|---|---|
| **Noun** | Distinct root | Toneless (flat mid) |
| **Verb** | Distinct root | Toneless (flat mid) |
| **Adjective** | Noun root + `-s` | Toneless (flat mid) |
| **Adverb** | Verb root + `-s` | Toneless (flat mid) |

> **Example:** `fei` (verb, toneless) → `feis` (adverb, toneless). Noun and verb are independent roots — the noun for "fly" is a different word entirely.

**Category distinction** for 1-syllable words is handled by:
1. **Distinct roots** — nouns and verbs are different words, not distinguished by tone
2. **The `-s` suffix** — marks adjective (noun + `-s`) and adverb (verb + `-s`)
3. **Word order and colour prefixes** — provide additional disambiguation

---

## III. The `-s` Derivational Suffix

### A. Function

| Derivation | Result |
|---|---|
| Noun + `-s` | Adjective |
| Verb + `-s` | Adverb |

`s` applies only to **1 and 2 syllable** words. 3+ syllable words use tone pattern alone to distinguish all 4 categories.

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

When a **case suffix** (Accusative `-ni`/`-na`, Genitive `-si`/`-sa`) is attached, the tone marker (`j` or `v`) **never migrates**. It remains locked to its original syllable. Case suffixes are pronounced flat Mid and do **not** count toward the last-3 domain.

> **Crucial:** Case suffixes are **extrasyllabic for tone purposes** — they do not count toward the syllable count for the Last-3 Domain Rule. A 2-syllable root + case suffix remains a **2-syllable word** tonally, retaining its original H→L or L→H contour. The case suffix is simply appended as a flat Mid appendix. This means a 2-syl root + case suffix (e.g., `aujlisa`) has a **different** tonal pattern from a bare 3-syllable root (which would follow the Last-3 Domain: H→M→L for nouns).

> **Example:** `aujli` (noun, 2-syl, H→L) + Genitive `-sa` → `aujlisa` — `j` stays on `au`; `-sa` is flat Mid. The word is tonally 2 syllables (H→L) with a flat appendix, not a 3-syllable H→M→L noun.

### C. Colour Prefix Exemption

The **colour prefix** is an external proclitic. It is pronounced flat Mid and does **not** count toward the syllable count for the last-3 domain. Only the root's syllables are counted.

> **Example:** `a-` (red prefix, flat Mid) + `lujmi sojla` (2-syl noun + 2-syl noun, multi-word vocab) = `a-lujmi sojla`
> The colour prefix `a-` is flat Mid and attaches to the first word. Each word retains its own tonal contour: H→L → H→L.

### D. Modular Stitching (Multi-Word Vocabs)

When a semantic concept is expressed as **multiple orthographic words** (a multi-word vocab with spaces), each word retains its own last-3 domain. The tonal contours are **stitched sequentially** across the word sequence, not recalculated as if the phrase were a single word.

This contrasts with mono-word compounds written as a single word — those use the Last-3 Domain Rule (§IV-A) recalculated across the entire word.

> **Example:** `aujli lujmi` (2-syl noun + 2-syl noun, two-word vocab)
> **Melody:** H→L → H→L. Each word's internal contour is preserved.
> **Contrast:** If these were fused into a single word, the Last-3 Domain Rule would recalculate the contour across the entire compound (e.g., a 4-syllable noun → M→H→M→L).

### E. No Cross-Word Tone Sandhi

Identical contours may abut across word boundaries. Kilor permits this — musicality comes from rhythmic phrasing and syntactic structure, not forced phonetic alteration.

### F. Musical Tone Override

In song and metered poetry, the melody or rhythmic metre of the composition may override lexical tone contours. When a word is set to music, its tonal pattern can be flattened or reshaped to follow the musical line.

This is consistent with how tonal languages (Mandarin, Cantonese, Thai, Vietnamese) function in song — lexical tone is subordinated to melody when the two conflict. In Kilor, when tones are neutralised by music, word category is recovered from:

1. **Syntactic position** — word order and case suffixes (which remain mandatory in poetic registers) disambiguate role
2. **The `-s` derivational suffix** — audible even when tones are flattened, preserving the noun/adjective and verb/adverb distinction for 1–2 syllable words
3. **Colour prefixes** — ontological class provides additional semantic grounding

This is not a grammatical rule but a **performance convention**. No morphological changes, prefixes, or alternative spellings are required — the poet or composer simply prioritises the composition's melodic contour over lexical tone, and the grammar's existing redundancy carries the disambiguation burden.

---

## V. Summary Table

| Syl | Noun | Verb | Adjective | Adverb |
|---|---|---|---|---|
| **1** | Toneless | Toneless | Noun+`s`, Toneless | Verb+`s`, Toneless |
| **2** | H(`j`)→L | L(`v`)→H | Noun+`s` | Verb+`s` |
| **3** | H(`j`)→M→L | L(`v`)→H→M | M→H(`j`)→H | M→L(`v`)→M |
| **4+** | ...M→**H(j)→M→L** | ...M→**L(v)→H→M** | ...M→**M→H(j)→H** | ...M→**M→L(v)→M** |

> **Footnote — Case suffixes:** Case suffixes (Accusative `-ni`/`-na`, Genitive `-si`/`-sa`) are extrasyllabic for tone purposes. They do not count toward the syllable count and do not affect the Last-3 Domain. A 2-syl root + case suffix remains tonally a 2-syl word (H→L or L→H) with a flat Mid appendix. See §IV-B.

---

*End of Tone & Prosody Specification (v3.0).*