# Kilor Grammar & Syntax

**Module:** Word Order, Harmony, Compounding, Temporal & Plural Strategy
**Status:** Canonical

---

## I. Word Order

### A. Default: SOV

Kilor's **default, unmarked** word order is **Subject–Object–Verb (SOV)**. This is the natural order for everyday speech and standard prose.

> **Example:** `a-kojra aelujmina tavka.`
> (The fire the light burns.)
> SUBJ [NOM] — OBJ [ACC] — VERB

### B. Poetic & Formal Reordering

Because case suffixes explicitly mark syntactic roles (see `cases.md`), Kilor is **non-configurational** — writers and poets may reorder elements for rhythm, emphasis, or aesthetic beauty. Common poetic inversions include:

| Order | Pattern | Effect |
|:---|:---|:---|
| **SOV** | Subject—Object—Verb | Default, unmarked |
| **OSV** | Object—Subject—Verb | Emphasises the object/victim |
| **VSO** | Verb—Subject—Object | Leads with the action for dramatic effect |

> **Rule:** When word order deviates from SOV, all non-Nominative case suffixes become **mandatory** (even the Accusative, which is otherwise optional in speech). This ensures the syntactic roles remain unambiguous.

### C. Genitive Chains

The Genitive possessor may precede or follow the possessed noun. Both orders are intelligible because the `-si`/`-sa` suffix marks the possessor unambiguously.

> **Example:** `a-kojrasa aelujmi` (the fire's light) ≡ `aelujmi a-kojrasa` (the light of the fire)

---

## II. Vowel Harmony — The Echo Rule

Suffixes must assimilate to the vowel class of the root word's nucleus.

| Class | Vowels |
|:---|:---|
| **Back / Deep** | a, o, u, au, ou |
| **Front / Bright** | e, i, y, ae, ai, ei, eu, iu, oi |

**Rule:** A root containing a Back vowel dictates that all subsequent agglutinative suffixes must use Back vowel variants, and vice versa.

> **Example (Back root):** `kojra` (fire, contains `o`, noun H→L) + Accusative → `kojrana` (uses `-na`, not `-ni`)
> **Example (Back root):** `lujmi` (light, contains `u`, noun H→L) + Accusative → `lujmina` (uses `-na`, not `-ni` — `u` is a back vowel)

### Proclitic Exemption

The **colour prefix** is an external proclitic. It sits outside the phonological boundary of the root and **does not** trigger or participate in the Echo Rule. Only the root's nucleus determines suffix vowel class.

> **Example:** `a-kojra-sa` — the prefix `a` is Front, but the root `o` is Back, so the Genitive suffix uses `-sa` (Back).

---

## III. Diphthong Merge — The Collision Rule

When a root terminating in a vowel interfaces with a vowel-initial suffix, they must fuse into one of the 7 official diphthongs.

| Root Ending | Suffix Start | Merge | Official Diphthong |
|:---|:---|:---|:---|
| -a | i- | a + i | **ai** |
| -a | u- | a + u | **au** |
| -e | i- | e + i | **ei** |
| -e | u- | e + u | **eu** |
| -i | u- | i + u | **iu** |
| -o | i- | o + i | **oi** |
| -o | u- | o + u | **ou** |

> **Note:** All currently defined suffixes (`-ni`/`-na`, `-si`/`-sa`, `-s`) begin with consonants, so the Diphthong Merge has no active application with the current suffix inventory. This rule is reserved for future vowel-initial affixes.
>
> The derivational suffix `-s` is an extrasyllabic appendix that attaches directly without merging: a root ending in a vowel (e.g., `korai`) simply takes `-s` with no diphthongisation → `korai-s`.

---

## IV. Compounding

### A. Lexical Compounding

Vocabulary is expanded through **lexical compounding**: roots of 1 to 5 syllables are combined to form complex concepts.

> **Example:** `lujmi` (light, H→L) + `sojla` (star, H→L) → `lujmisojla` (moon)

### B. Word-Unit Processing

A compound word is **not** treated as a single monolithic block for tone calculation. It is processed as a sequence of independent **Word-Units (Morphemes)**. Tone contours are stitched together via the Modular Stitching Rule (see `tone-prosody.md`), not recalculated for the compound's total syllable count.

### C. Root Constraints

- All roots must obey the CV/CVC/VC/V syllable templates
- No `j` or `v` may appear in any root
- No consonant clusters
- No 1- or 2-syllable root may end in `s` natively — `-s` is reserved as the modifier derivational suffix

---

## V. The `-s` Derivational Suffix

### A. Category Derivation

The suffix `-s` creates modifiers from base roots. It applies to **1 and 2 syllable** words only. 3+ syllable words distinguish all 4 categories through tone pattern alone (see `tone-prosody.md`).

| Derivation | Result | Applies To |
|:---|:---|:---|
| Noun + `-s` | Adjective | 1 & 2 syllable nouns |
| Verb + `-s` | Adverb | 1 & 2 syllable verbs |

> **1-syllable example:** `fei` (verb, toneless) → `feis` (adverb, toneless)
> **2-syllable example:** `aujli` (noun, H→L) → `aujlis` (adjective, H→L)

### B. Phonological Nature

`s` is a **toneless extrasyllabic appendix** — pronounced like English plural `-s` (`/s/` or `/z/`). It does not add a syllable, does not carry `j` or `v`, and does not affect the last-3 tone domain.

### C. Suffix Order

When multiple suffixes co-occur on the same root, the order is:

**root → case suffix → `-s`**

> **Example:** `aujli` (noun) + Accusative `-na` + `-s` → `aujlina-s`

---

## VI. Temporal Expression — No Tense

Kilor has **no grammatical tense**. There are no verb conjugations for past, present, or future, and no aspect particles (e.g., no equivalent to Cantonese 咗).

Time is expressed purely through **context and temporal words** (yesterday, tomorrow, now, later, before, etc.). These time words are critically important in the language and should be placed early in the clause to establish the temporal frame.

> **Example (conceptual):** *yesterday I eat apple* (= I ate an apple yesterday)
> *tomorrow I eat apple* (= I will eat an apple tomorrow)

---

## VII. Plural Strategy — No Plural Marking

Kilor has **no plural marking** — neither suffixes, nor prefixes, nor tonal changes indicate plurality. This follows the Chinese approach: number is inferred from **context, quantifiers, and numerals**.

To express quantity explicitly, use numeral + classifier constructions or quantifier words (many, few, all, some, three, etc.).

> **Example (conceptual):** *three apple* (= three apples)
> *many bird* (= many birds)
> *apple* (could be one or more, depending on context)

### Pronoun Exception

The **only exception** to the no-plural-marking rule is the pronoun system. Pronouns use a dedicated **`-l-` plural infix** to distinguish singular from plural:

| | Singular | Plural |
|---|---------|--------|
| 1st | ki | kil |
| 2nd | ti | til |
| 3rd Living | si | sil |
| 3rd Non-Living | ni | nil |

This is a closed-class morphological process that applies **only** to pronouns. See `pronouns.md` §II-B for full details.
---

## VIII. No Possessive Suffixes

Kilor has **no dedicated agglutinative possessive suffix**. Possession is expressed exclusively through the **Genitive case** suffix (`-si`/`-sa`). See `cases.md` for full details.

---

*End of Grammar & Syntax Specification.*