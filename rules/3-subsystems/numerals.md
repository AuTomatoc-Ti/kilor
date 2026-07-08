# Kilor Numerals, Measure Words & Ordinals

**Module:** Numeral System, Quantification & Ranking
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.0.0
**Depends on:**

---

## I. Core Numerals (0–13)

The first 14 numerals are irregular. Every numeral above 13 is constructed compositionally.

| Value | Form | Syllables | Phonology |
|:---|:---|:---|:---|
| 0 | `aniu` | 2 | V+CV — `a` / `niu` |
| 1 | `mo` | 1 | CV — `m` + `o` |
| 2 | `do` | 1 | CV — `d` + `o` |
| 3 | `ro` | 1 | CV — `r` + `o` |
| 4 | `foi` | 1 | CV — `f` + `oi` |
| 5 | `tai` | 1 | CV — `t` + `ai` |
| 6 | `slo` | 1 | CV — `sl` + `o` |
| 7 | `lai` | 1 | CV — `l` + `ai` |
| 8 | `auk` | 1 | VC — `au` + `k` |
| 9 | `wy` | 1 | CV — `w` + `y` |
| 10 | `gau` | 1 | CV — `g` + `au` |
| 11 | `mai` | 1 | CV — `m` + `ai` |
| 12 | `doi` | 1 | CV — `d` + `oi` |
| 13 | `rai` | 1 | CV — `r` + `ai` |

---

## II. Scale Markers

Scale markers are closed-class numeral roots denoting powers of 10.

| Value | Form | Syllables |
|:---|:---|:---|
| 10¹ (ten) | `gau` | 1 |
| 10² (hundred) | `cu` | 1 |
| 10³ (thousand) | `kas` | 1 |
| 10⁶ (million) | `hus` | 1 |
| 10⁹ (billion) | `tus` | 1 |
| 10¹² (trillion) | `rakas` | 2 |

### A. `-s` Exemption

`kas`, `hus`, `tus`, and `rakas` end in `-s` but are **exempt** from the open-root `-s` constraint (`0-foundation/grammar-syntax.md` §IV-C). All numerals form a **closed class** — they never receive derivational morphology. They join `res`, `nar`, `iu`, `na`, `te`, `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, and `kus` in the closed-class exemption list.

### B. `sl` Positional Exemption

`slo` (6) uses the start-only onset `sl`. Within **mono-word numeral compounds**, `sl` is exempt from the word-initial-only restriction (`0-foundation/phonology.md` §III-C) — it may appear in any position. Numeral compounds form a closed, predictable subsystem; e.g., `gauslokas` (16,000) with `sl` word-medially is legal.

---

## III. Construction Rules

### A. Multiplicative Compounding (Tens, Hundreds, Thousands, etc.)

A numeral expressing N × S is formed by fusing the multiplier with the scale marker into a **mono-word compound**:

```
MULTIPLIER + SCALE → mono-word
```

| Form | Parse | Value |
|:---|:---|:---|
| `dogau` | 2 × 10 | 20 |
| `rogau` | 3 × 10 | 30 |
| `foigau` | 4 × 10 | 40 |
| `taigau` | 5 × 10 | 50 |
| `slogau` | 6 × 10 | 60 |
| `laigau` | 7 × 10 | 70 |
| `aukgau` | 8 × 10 | 80 |
| `wygau` | 9 × 10 | 90 |
| `docu` | 2 × 100 | 200 |
| `rokas` | 3 × 1,000 | 3,000 |
| `wykas` | 9 × 1,000 | 9,000 |
| `dogaukas` | 20 × 1,000 | 20,000 |
| `slohus` | 6 × 1,000,000 | 6,000,000 |

> **Note:** `mo-` (1) as multiplier is **optional**. Both `gau` and `mogau` mean 10. Both `cu` and `mocu` mean 100. The bare scale marker is the unmarked form; `mo-` is used for explicitness or rhythmic balance. The same optionality applies at every order of magnitude: `kas` ≡ `mokas` (1,000), `hus` ≡ `mohus` (1,000,000), etc.

### B. Additive Concatenation (Place-Value Assembly)

Multi-digit numbers are expressed by listing components from **largest to smallest** as a **multi-word vocab**:

```
LARGEST — NEXT — ... — SMALLEST (multi-word)
```

| Form | Parse | Value |
|:---|:---|:---|
| `gau mo` | 10 + 1 | 11 |
| `gau tai` | 10 + 5 | 15 |
| `gau lai` | 10 + 7 | 17 |
| `gau wy` | 10 + 9 | 19 |
| `dogau` | 20 | 20 |
| `dogau mo` | 20 + 1 | 21 |
| `rogau lai` | 30 + 7 | 37 |
| `wygau wy` | 90 + 9 | 99 |
| `cu mo` | 100 + 1 | 101 |
| `cu do` | 100 + 2 | 102 |
| `cu ro` | 100 + 3 | 103 |
| `cu gau` | 100 + 10 | 110 |
| `cu mai` | 100 + 11 | 111 |
| `cu doi` | 100 + 12 | 112 |
| `cu rai` | 100 + 13 | 113 |
| `cu mogau foi` | 100 + (1×10) + 4 | 114 |
| `cu dogau` | 100 + 20 | 120 |
| `cu dogau mo` | 100 + 20 + 1 | 121 |
| `docu` | 200 | 200 |
| `docu slogau foi` | 200 + 60 + 4 | 264 |
| `wycu wygau wy` | 900 + 90 + 9 | 999 |
| `kas` | 1,000 | 1,000 |
| `kas docu rogau foi` | 1,000 + 200 + 30 + 4 | 1,234 |
| `gaukas` | 10,000 | 10,000 |
| `doikas` | 12,000 | 12,000 |
| `doikas rocu foigau tai` | 12,000 + 300 + 40 + 5 | 12,345 |
| `cukas` | 100,000 | 100,000 |
| `cudogaurokas` | (100+20+3)×1,000 | 123,000 |
| `cudogaurokas foicu taigau slo` | 123,000 + 400 + 50 + 6 | 123,456 |
| `hus` | 1,000,000 | 1,000,000 |
| `gauhus` | 10,000,000 | 10,000,000 |
| `cuhus` | 100,000,000 | 100,000,000 |
| `tus` | 10⁹ | 1,000,000,000 |
| `gautus` | 10¹⁰ | 10,000,000,000 |
| `cutus` | 10¹¹ | 100,000,000,000 |
| `rakas` | 10¹² | 1,000,000,000,000 |

Components within a place-value slot that exceed a single scale marker use further multiplicative compounding:

> `cudogaurokas` = `cu` (100) + `dogau` (20) + `ro` (3) fused with `kas` → (100+20+3) × 1,000 = 123,000

### C. Zero (0) — `aniu`

`aniu` means zero. It is used:

- As a standalone number: `aniu` = zero
- In place-value gaps: not used — gaps are handled implicitly by component ordering (largest→smallest). `cu mo` (100+1) = 101, with no zero component between hundred and one.

When zero is explicit for clarity (e.g., arithmetic), `aniu` stands alone:

> `aniu res` = "It is zero."

---

## IV. Tone

Numerals follow **standard tone rules per word**, based on each word's syllable count independently:

| Syllables | Tone Rule |
|:---|:---|
| 1-syllable | Flat mid-tone (toneless) |
| 2-syllable | H→L (noun pattern) |
| 3+ syllable | H→M→L (last-3 domain) |

Multi-word numeral expressions are stitched **modularly**: each word carries its own independent contour per `0-foundation/tone-prosody.md` §IV-D. There is no free variation — tone is deterministic.

> **1-syllable:** `mo`, `gau`, `kas`, `cu` → flat mid-tone
> **2-syllable:** `dogau`, `rakas`, `aniu` → H→L (the `j`/`v` tone marker is used in dictionary citation forms per the standard noun pattern; in practice, numerals follow the closed-class pronoun convention where tone markers may be omitted in spelling — see §VIII)
> **3+ syllable:** `cudogaurokas` → H→M→L across last 3 syllables

---

## V. Ordinals — `dir`

The ordinal particle **`dir`** follows the numeral to form ordinal expressions (first, second, third, etc.).

| Form | Meaning |
|:---|:---|
| `mo dir` | first |
| `do dir` | second |
| `ro dir` | third |
| `gau dir` | tenth |
| `cu mo dir` | one hundred and first |

`dir` is a **function word** — 1-syllable, toneless (flat mid-tone), closed-class.

---

## VI. Noun Phrase Quantification

### A. NP Order

Within a noun phrase, numerals and measure words follow the noun:

```
NOUN — (MEASURE) — NUM — (ORD)
```

| Slot | Required | Description |
|:---|:---|:---|
| `NOUN` | Yes | The thing being counted |
| `MEASURE` | No | A measure word (container, unit, portion) — a regular noun root |
| `NUM` | Yes | Numeral |
| `ORD` | No | Ordinal particle `dir` |

### B. Measure Words

A **measure word** is a regular noun root used to specify a container, unit, portion, or grouping. Kilor has **no taxonomic classifiers** (no equivalent to Chinese 隻/本/個). The 7-colour ontology already classifies nouns by cognitive frame; a separate classifier system would be redundant.

When no measure word is used, the numeral directly quantifies the noun:

| Pattern | Kilor | English |
|:---|:---|:---|
| `NOUN NUM` | `lira ro` | three waters |
| `NOUN MEASURE NUM` | `lira pei ro` | three cups of water |
| `NOUN NUM ORD` | `lira ro dir` | the third water |
| `NOUN MEASURE NUM ORD` | `lira pei ro dir` | the third cup of water |

### C. Colour Prefix Interaction

Quantified nouns are **indefinite** — the colour prefix is omitted per `1-nominals/nouns-colour-prefix.md` §IV-B:

> ✅ `lira ro` = three waters (generic)
> ❌ `i-lira ro` = three the-waters (contradiction: quantified nouns are indefinite by nature)

A colour prefix may be retained when the quantification is part of a larger definite noun phrase (e.g., "the three cups of water that I drank" — the noun phrase as a whole is definite). In that case, the prefix attaches to the main noun, not the measure word:

> `i-lira pei ro dir` = the third cup of water (specific, identifiable water)

---

## VII. Numerals Are Not Nouns

Numerals do not take case suffixes (Accusative or Genitive). They are a closed class — they occupy the modifier slot in the NP and are never the syntactic head.

Measure words, being regular noun roots, **may** take case suffixes when the NP as a whole receives case marking, following the suffix-distribution rule for multi-word vocabs (`0-foundation/grammar-syntax.md` §IV-B).

---

## VIII. Orthographic Convention

Numerals are a closed class. In everyday writing, tone markers (`j`/`v`) may be omitted from multi-syllable numerals following the same convention as pronouns (`1-nominals/pronouns.md` §IV-A) — the closed class and unambiguous numerical context make tone markers redundant in practice.

Dictionary citation forms include tone markers for completeness (e.g., `dovgau`, `rakas`), but canonical example sentences may omit them.

---

## IX. Summary Table

| Category | Items |
|:---|:---|
| **Core numerals (0–13)** | `aniu`, `mo`, `do`, `ro`, `foi`, `tai`, `slo`, `lai`, `auk`, `wy`, `gau`, `mai`, `doi`, `rai` |
| **Scale markers** | `gau`(10¹), `cu`(10²), `kas`(10³), `hus`(10⁶), `tus`(10⁹), `rakas`(10¹²) |
| **Multiplicative rule** | Multiplier + Scale → mono-word compound |
| **Additive rule** | Largest → smallest, multi-word vocab |
| **`mo-` optionality** | `mo` as multiplier is always optional |
| **Ordinal** | Particle `dir` after numeral |
| **NP order** | `NOUN — (MEASURE) — NUM — (ORD)` |
| **`-s` exemption** | `kas`, `hus`, `tus`, `rakas` exempt (numerals = closed class) |
| **`sl` exemption** | `sl` permitted word-medially in numeral compounds |
| **Tone** | Deterministic per-word, modular stitching |
| **Case** | Numerals do not take case suffixes |

---

*End of Numeral Specification.*