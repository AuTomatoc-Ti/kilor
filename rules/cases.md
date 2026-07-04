# Kilor Cases — The 3-Case Syntactic Engine

**Module:** Syntactic Role Marking & Poetic Freedom
**Status:** Canonical

---

## I. Core Philosophy

Traditional case languages overwhelm learners with 10+ morphological slots. Kilor simplifies to exactly **3 cases**, mirroring the most intuitive grammatical mapping for learners: **I (Actor) / me (Target) / my (Owner)**.

This minimal system achieves two goals:

1. **Zero Cognitive Friction** — learners only need two suffixes. The subject (Nominative) is unmarked.
2. **Absolute Poetic Freedom** — because every non-subject noun wears an explicit syntactic tag, word order can be shuffled for rhythm, emphasis, and aesthetic beauty without breaking grammar.

---

## II. The 3-Case Paradigm

Case suffixes use simple CV (Consonant-Vowel) forms to maintain rhythmic purity.

| Case | Function | Front/Bright Suffix | Back/Deep Suffix | Phonetic Intuition |
|:---|:---|:---|:---|:---|
| **Nominative** | The Actor / Subject *(Who does it?)* | *(unmarked)* | *(unmarked)* | Zero effort. The default, grounded state. |
| **Accusative** | The Target / Object *(Who receives it?)* | **`-ni`** | **`-na`** | `n` is a nasal resonance — it phonetically flows *toward* a target. |
| **Genitive** | The Owner / Possession *(Whose? / "Of")* | **`-si`** | **`-sa`** | `s` is continuous fricative — it implies a lingering connection. |

### Vowel Harmony Assignment

| Front Root Vowels | Back Root Vowels |
|:---|:---|
| e, i, y, ae, ai, ei, eu, iu, oi | a, o, u, au, ou |

> **Example (Back root):** `kojra` (fire, `o`, noun H→L) + Accusative → `kojrana`
> **Example (Back root):** `lujmi` (light, `u`, noun H→L) + Accusative → `lujmina`
> **Example (Back root):** `kojra` (fire) + Genitive → `kojrasa`
> **Example (Back root):** `lujmi` (light) + Genitive → `lujmisa`

---

## III. Accusative Usage — Optional in Speech

The Accusative suffix (`-ni`/`-na`) has a **two-tier usage rule**:

### A. Optional — Everyday Speech (SOV Order)

When a sentence follows the **default SOV order**, the Accusative may be **dropped** in everyday conversation. The object's position between Subject and Verb already signals its role sufficiently.

> **Conceptual example (SOV speech):** `a-kojra lujmi tavka` — *lujmi* (light) is unambiguously the object by position.

### B. Mandatory — Formal Writing & Non-SOV Order

The Accusative becomes **mandatory** in two contexts:

1. **Formal writing** (even in SOV order) — for precision and clarity
2. **Any non-SOV word order** (OSV, VSO, or other poetic inversions) — because position no longer signals objecthood, the suffix is the sole disambiguator

> **Conceptual example (OSV):** `lujmina a-kojra tavka` — the `-na` on *lujmi* confirms it as the object despite being sentence-initial.

---

## IV. Genitive Usage — Possession

The Genitive (`-si`/`-sa`) is the **only mechanism for expressing possession** in Kilor. There is no separate possessive particle or agglutinative possessive suffix.

### Word Order Flexibility

The Genitive-marked possessor may appear before or after the possessed noun:

> `a-kojrasa aelujmi` (the fire's light) ≡ `aelujmi a-kojrasa` (the light of the fire)

### Absence of Possessive Pronouns

There are no dedicated possessive pronouns (no equivalent to English *my*, *your*, *his*). Possession by pronoun is expressed by attaching the Genitive suffix to the pronoun root.

> **Pronoun exception:** Pronouns use **reduced case endings** — Accusative `-n` and Genitive `-s` — instead of the standard `-ni`/`-na` and `-si`/`-sa`. These endings are invariant (no vowel harmony). See `pronouns.md` §III for the full declension table.
---

## V. Dative & Instrumental — Analytic Particles

Kilor intentionally restricts the case system to 3 slots. Two additional semantic roles are handled analytically:

| Role | Meaning | Particle | Usage |
|:---|:---|:---|:---|
| **Dative** | To / For (recipient) | **`te`** | Placed before the recipient noun |
| **Instrumental** | With / By (means) | **`su`** | Placed before the instrument noun |

These particles are **standalone, single-syllable words** that sit outside the case suffix system. They do not trigger vowel harmony and carry flat mid-tone.

---

## VI. Phonological Integration — The Tone Lock Rule

When a case suffix is attached to a root, the tonal architecture of the root is completely preserved:

- The tone marker (`j` or `v`) **never migrates**
- It remains ontologically locked to its original anchor syllable
- The case suffix itself is pronounced with a **neutral, flat mid-tone**
- The case suffix does **not** count toward the last-3 tone domain (see `tone-prosody.md`)

> **Example:** `aujli` (noun, 2 syllables, H(`j`)→L) + Genitive `-sa` → `aujlisa`
> The `j` stays locked on `au`; `-sa` is flat mid-tone.

### Suffix Order

When the derivational `-s` (modifier marker) co-occurs with a case suffix, the order is:

**root → case suffix → `-s`**

> **Example:** `aujli` (noun) + Accusative `-na` + `-s` → `aujlina-s`
> (Accusative noun form turned into an adjective)

---

*End of Cases Specification.*
