# Kilor Grammar & Syntax

**Module:** Word Order, Harmony, Compounding, Temporal & Plural Strategy
**Status:** Canonical

---

## I. Word Order

### A. Default: SOV

Kilor's **default, unmarked** word order is **Subject–Object–Verb (SOV)**. This is the natural order for everyday speech and standard prose.

> **Note:** SOV is a **pedagogical baseline** — the simplest model for explaining Kilor's core syntax. Real sentences may include additional elements (prepositions, numerals, temporal words, question words, etc.) that create more complex structures. The SOV model describes the relative order of the three core arguments; other elements are placed according to their own rules (see `interrogative.md` for question word fronting, `cases.md` §V for dative/instrumental particles).

> **Example:** `a-fojra hawu-ni tavka.`
> (the-fire animal-ACC eat.)
> SUBJ [NOM] — OBJ [ACC] — VERB
> "The fire eats the animal."

### B. Poetic & Formal Reordering

Because case suffixes explicitly mark syntactic roles (see `cases.md`), Kilor is **non-configurational** — writers and poets may reorder elements for rhythm, emphasis, or aesthetic beauty. Common poetic inversions include:

| Order | Pattern | Effect |
|:---|:---|:---|
| **SOV** | Subject—Object—Verb | Default, unmarked |
| **OSV** | Object—Subject—Verb | Emphasises the object/victim |
| **VSO** | Verb—Subject—Object | Leads with the action for dramatic effect |

> **Rule:** When word order deviates from SOV, all non-Nominative case suffixes become **mandatory** (even the Accusative, which is otherwise optional in speech). This ensures the syntactic roles remain unambiguous.
>
> **Exception:** Question words are **exempt** from this rule — they are always fronted (see `interrogative.md` §III) and carry no case suffixes regardless of word order (see `interrogative.md` §II-C).

### C. Genitive Chains

For a **single possessor**, the Genitive-marked noun may precede or follow the possessed noun:

> **Example:** `fojrasi lujmi` (fire's light) ≡ `lujmi fojrasi` (light of fire)

For **nested possession** (multiple Genitive-marked nouns chained together), Kilor uses a **fixed recursive order**: each possessor must **precede** what it owns. The outermost possessor comes first, followed by each successively nested pair. See `cases.md` §IV for the full rule.

> **Nested example:** `kis fojrasi lujmi` = "my fire's light" — `kis` owns `fojrasi`, which owns `lujmi`
> 
> Free order (`lujmi fojrasi kis`) is not valid for nested possession.

### D. Passive Voice

Kilor expresses passive voice (agent demotion or deletion) using the instrumental particle **`sy`** as a valency-reducing marker. See `cases.md` §V-E for the full specification with all three usage patterns (instrumental, passive agent-deleted, passive agent-expressed).

In brief:

| Pattern | Example |
|:---|:---|
| `Patient sy verb` | `hawu sy tavka.` — "The animal was eaten." |
| `Patient sy agent verb` | `hawu sy a-fojra tavka.` — "The animal was eaten by the fire." |

The patient is promoted to NOM (unmarked). The agent (if expressed) follows `sy` with no case suffix. The verb carries no morphological change — valency reduction is signalled entirely by `sy`.

> **Note:** OSV word order (§I-B) can topicalise the object but cannot delete the agent. Passive `sy` is the only mechanism for structurally omitting the agent from the clause.

---

## II. Contrastive Suffix Rule

Suffixes use the vowel class **opposite** to the root's last-syllable nucleus. This creates a pleasant front↔back alternation at the root-suffix boundary.

| Last-Syllable Vowel Class | Suffix Class | Vowels |
|:---|:---|:---|
| **Front / Bright** | Uses Back suffix | e, i, y, ae, ei, eu, iu → `-na` (ACC), `-sa` (GEN) |
| **Back / Deep** | Uses Front suffix | a, o, u, ai, au, oi, ou → `-ni` (ACC), `-si` (GEN) |

> **Example (last vowel `a` = back → front suffix):** `fojra` (fire, noun H→L) + Accusative → `fojrani` (uses `-ni`, not `-na`)
> **Example (last vowel `i` = front → back suffix):** `lujmi` (light, noun H→L) + Accusative → `lujmina` (uses `-na`, not `-ni`)

### Proclitic Exemption

The **colour prefix** is an external proclitic. It sits outside the phonological boundary of the root and **does not** trigger or participate in the Contrastive Suffix Rule. Only the root's last-syllable nucleus determines suffix vowel class.

> **Example:** `a-fojra-si` — the prefix `a` is Front, but the root's last vowel `a` is Back, so the Genitive suffix uses front `-si`.

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
> The derivational suffix `-s` is an extrasyllabic appendix that attaches directly without merging: a root ending in a vowel (e.g., `kora`) simply takes `-s` with no diphthongisation → `kora-s`.

---

## IV. Compounding

### A. Lexical Compounding

Vocabulary is expanded through **lexical compounding**: roots of 1 to 5 syllables are combined to form complex concepts.

> **Example:** `lujmi` (light, H→L) + `sojla` (star, H→L) → `lujmi sojla` (moon, multi-word vocab)

### B. Word-Unit Processing

Kilor distinguishes two forms of compounding for tone purposes:

1. **Mono-word compounds** — roots fused into a single orthographic word. These are treated as a single word for tone: the Last-3 Domain Rule applies across the entire word (see `tone-prosody.md` §IV-A).

   > **Phonotactic constraint:** Start-only onsets (`sh`, `ch`, `th`, `sl`, `kl`, `tl`, `bl`, `ml`; see `phonology.md` §III-C) and ending-only consonants (`ng`, `x`; see `phonology.md` §III-B) are restricted to word-peripheral positions. A root beginning with a start-only onset or ending with an ending-only consonant may **not** appear as a non-initial or non-final element in a mono-word compound — such combinations must use multi-word vocabs instead. Only roots composed entirely of core consonants (see `phonology.md` §III-A) may appear in any position within a mono-word compound.

2. **Multi-word vocabs** — two or more words written with spaces that together form one semantic concept (e.g., `sojlas lujmi`). Each word retains its own tonal contour independently via Modular Stitching (see `tone-prosody.md` §IV-D). The contours are stitched sequentially, not recalculated across word boundaries.

   > **Case suffix distribution:** When a multi-word vocab receives a case suffix (Accusative or Genitive), the suffix attaches **only to the last word** of the vocab. The earlier words remain unmarked. The colour prefix (if present) attaches orthographically to the first word and does not affect suffix placement. See `cases.md` §III–IV for case usage rules.

### C. Root Constraints

- All roots must obey the CV/CVC/VC/V syllable templates
- No `j` or `v` may appear in any root
- No consonant clusters
- No 1- or 2-syllable root may end in `s` natively — `-s` is reserved as the modifier derivational suffix
- 3+ syllable roots **may** end in `s` natively (e.g., `marokas`), pronounced as English plural `-s` (`/s/` or `/z/`). This is permitted because the `-s` derivational suffix does not apply to 3+ syllable words — tone pattern alone distinguishes categories at that length, so there is no ambiguity.
- Pronoun genitive forms (`kis`, `tis`, `sis`, `nis` and their plurals) are **inflected**, not roots, and are exempt from the `-s` constraint
- Closed-class function words (`res`, `nar`, `iu`, `na`, `te`, `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus`, `tor`, `les`, `torra`, `wetor`, `mangus`) are **exempt** from the `-s` constraint. The `-s` restriction applies only to open-class content roots (Nouns, Verbs, Adjectives, Adverbs) that participate in the derivational `-s` system. Function words are a fixed inventory and never receive derivational morphology.

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

---

## VI. Temporal Expression — No Tense

Kilor has **no grammatical tense**. There are no verb conjugations for past, present, or future, and no aspect particles (e.g., no equivalent to Cantonese 咗).

Time is expressed purely through **context and temporal words** (yesterday, tomorrow, now, later, before, etc.). These time words are critically important in the language and **must be placed clause-initially** (before the subject) to establish the temporal frame.

> **Example:** *piroi ki kau* (yesterday I come) = I came yesterday
> *paroi ki kau* (tomorrow I come) = I will come tomorrow

### A. Temporal Word Inventory

#### Day Scale (mono-word compounds with `roi` "day")

| Word | Syl | Meaning | Construction |
|---|---|---|---|
| `pimaroi` | 3 | day before yesterday | `pi` + `ma` + `roi` |
| `piroi` | 2 | yesterday | `pi` + `roi` |
| `imaroi` | 3 | today | `ima` + `roi` |
| `paroi` | 2 | tomorrow | `pa` + `roi` |
| `pamaroi` | 3 | day after tomorrow | `pa` + `ma` + `roi` |

> **Combining forms:** `pi` ← `tilpi` (before), `pa` ← `tilpa` (after), `ma` (bound infix: one step removed). `roi` = day. `ima` = now.

#### Distance Scale (free-standing adverbs)

| Word | Meaning | Construction |
|---|---|---|
| `pima` | earlier / further back | `pi` + `ma` |
| `pama` | later / further ahead | `pa` + `ma` |

> **`pima` and `pama`** have two context-disambiguated meanings:
> 1. **Specific:** exactly two steps away (one thing between it and `ima`)
> 2. **Open-range:** anything ≥ two steps away

#### Frequency Words (`-saka` paradigm from `sakar` "occurrence")

| Word | Syl | Meaning | Construction |
|---|---|---|---|
| `esaka` | 3 | always | `esa` (all) + `sakar` |
| `slosaka` | 3 | sometimes | `slo(te)` (some) + `sakar` |
| `nasaka` | 3 | never | `na` (negation) + `sakar` |

#### Bare Temporal Roots

| Root | Syl | Meaning | Notes |
|---|---|---|---|
| `shu` | 1 | soon | Simplified from `shuk` + `tlow` |
| `sar` | 1 | late | Simplified from `pusar` + `tlow` |
| `cho` | 1 | early | Bare root, `ch` onset (start-only) |
| `amo` | 2 | again | Bare root |
| `fou` | 1 | during | Related to `founai` (duration) |

---

## VII. Plural Strategy — No Plural Marking

Kilor has **no plural marking** — neither suffixes, nor prefixes, nor tonal changes indicate plurality. This follows the Chinese approach: number is inferred from **context, quantifiers, and numerals**.

To express quantity explicitly, use **numeral + optional measure word + noun** constructions (see `num.md` §VI) or quantifier words (many, few, all, some, three, etc.).

> **Example (conceptual):** *lira ro* (= three waters / three [units of] water)
> *lira pei ro* (= three cups of water)
> *lira* (could be one or more, depending on context)

### Pronoun Exception

The **only exception** to the no-plural-marking rule is the pronoun system. Pronouns use a dedicated **`-l(i)-` plural marker** to distinguish singular from plural:

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

## IX. Comparatives & Superlatives

Kilor uses analytic particles to express comparison. No dedicated comparative/superlative morphology exists — comparison is handled through a small inventory of closed-class particles that pattern like the oblique preposition system (see `cases.md` §V).

### A. Comparative Particle Inventory

| Particle | Meaning | Role |
|---|---|---|
| `tor` | than | Marks the standard of comparison |
| `les` | as | Marks the equative standard |
| `torra` | most | Marks the superlative |
| `wetor` | much more than | Intensified comparative (fused from `wes` + `tor`) |
| `mangus` | among / among all | Restricts superlative scope |

These particles are **closed-class**: 1–2 syllables, toneless, no `j`/`v`, exempt from the `-s` constraint. They are added to the exemption list in §IV-C and the oblique particle inventory in `cases.md` §V.

### B. Comparative of Inequality

The comparative frame:

```
Subject  tor  Standard  (Degree)  Quality
```

> **Example:** `ki tor ti rali.`
> (I than you big)
> "I am bigger than you."

Degree words optionally intensify or diminish the comparison. These slot between the `tor`-phrase and the quality:

- `wes` (very, adverb derived from `we` + `-s`): `ki tor ti wes rali` — "I am much bigger than you"
- `meres` (a bit, adverb derived from `mere` + `-s`): `ki tor ti meres rali` — "I am a little bigger than you"
- `wetor` (much more than, fused particle): `ki wetor ti rali` — "I am much bigger than you"

The standard may be fronted for emphasis (OSV-like reordering), with the ACC case suffix marking the object:

> **Example:** `ti-n tor ki rali.`
> (you-ACC than I big)
> "Compared to you, I am bigger."

### C. Equative ("as X as Y")

The equative frame uses `les` in the same syntactic position as `tor`:

```
Subject  les  Standard  (Degree)  Quality
```

> **Example:** `ki les ti rali.`
> (I as you big)
> "I am as big as you."

**Negation:** Negation of the comparison uses `nar` **after** the particle (`les nar`, `tor nar`) to scope over the comparison itself, not over the subject:

> **Example:** `ki les nar ti rali.`
> (I as NEG you big)
> "I am not as big as you."

> **Example:** `ki tor nar ti rali.`
> (I than NEG you big)
> "I am not bigger than you."

### D. Superlative

The superlative particle `torra` precedes the quality:

```
Subject  torra  Quality
```

> **Example:** `ki torra rali.`
> (I most big)
> "I am the biggest."

To restrict the scope, use `mangus` (among). `mangus` may appear with or without `torra`:

> **Example (with explicit superlative):** `ki mangus torra rali.`
> (I among most big)
> "I am the biggest among (them/all)."

> **Example (implicit superlative):** `ki mangus rali.`
> (I among big)
> "I am the biggest among (them)."

`mangus` may take an explicit reference group as its object:

> **Example:** `ki mangus kil rali.`
> (I among us big)
> "I am the biggest among us."

### E. Word Order

The comparative phrase (`tor`/`les` + Standard + Degree) sits **between the subject and the quality**. In a full SOV clause with a copula:

```
Subject  tor/les  Standard  Degree  Quality  (res)  Object  Verb
```

In attributive position, the quality may link via the copula `res`. The copula may be omitted in casual speech when the quality directly follows the comparative frame — the comparative particle itself signals the predicative relationship.

### F. Supporting Content Roots

| Root | Syl | Category | Meaning | Derived Forms |
|---|---|---|---|---|
| `rap` | 2 | Noun | top / peak | `rajp` (n, H→L) → `rajps` (adj) "topmost" |
| `we` | 1 | Verb | to intensify | `wes` (adv) "very" |
| `mere` | 2 | Verb | to be slight (intensity) | `mejre` (n), `mevres` (adv) "a bit" |
| `pere` | 2 | Noun | small amount | `pejre` (n) → `pejres` (adj) "little (amount)" |

> **Distinction:** `mere` (intensity: "a bit") and `pere` (amount: "little") are distinct roots. Kilor separates intensity modification from quantity modification. Compare:
> - `meres rali` = "a bit big" (intensity — slightly big)
> - `peres hamin` = "little food" (amount — small quantity of food)

---

*End of Grammar & Syntax Specification.*
