# Kilor Grammar & Syntax

**Module:** Word Order, Harmony, Compounding, Plural Strategy
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.1.0
**Depends on:** `0-foundation/phonology.md`, `0-foundation/tone-prosody.md`

---

## I. Word Order

### A. Default: SOV

Kilor's **default, unmarked** word order is **Subject–Object–Verb (SOV)**. This is the natural order for everyday speech and standard prose.

> **Note:** SOV is a **pedagogical baseline** — the simplest model for explaining Kilor's core syntax. Real sentences may include additional elements (prepositions, numerals, temporal words, question words, etc.) that create more complex structures. The SOV model describes the relative order of the three core arguments; other elements are placed according to their own rules (see `2-predication/interrogative.md` for question word fronting, `1-nominals/cases.md` §V for dative/instrumental particles).

> **Example:** `a-fojra hawu-ni tavka.`
> (the-fire animal-ACC eat.)
> SUBJ [NOM] — OBJ [ACC] — VERB
> "The fire eats the animal."

### B. Poetic & Formal Reordering

Because case suffixes explicitly mark syntactic roles (see `1-nominals/cases.md`), Kilor is **non-configurational** — writers and poets may reorder elements for rhythm, emphasis, or aesthetic beauty. Common poetic inversions include:

| Order | Pattern | Effect |
|:---|:---|:---|
| **SOV** | Subject—Object—Verb | Default, unmarked |
| **OSV** | Object—Subject—Verb | Emphasises the object/victim |
| **VSO** | Verb—Subject—Object | Leads with the action for dramatic effect |

> **Rule:** When word order deviates from SOV, all non-Nominative case suffixes become **mandatory** (even the Accusative, which is otherwise optional in speech). This ensures the syntactic roles remain unambiguous.
>
> **Exception:** Question words are **exempt** from this rule — they are always fronted (see `2-predication/interrogative.md` §III) and carry no case suffixes regardless of word order (see `2-predication/interrogative.md` §II-C).

### C. Genitive Chains

For a **single possessor**, the Genitive-marked noun may precede or follow the possessed noun:

> **Example:** `fojrasi lujmi` (fire's light) ≡ `lujmi fojrasi` (light of fire)

For **nested possession** (multiple Genitive-marked nouns chained together), Kilor uses a **fixed recursive order**: each possessor must **precede** what it owns. The outermost possessor comes first, followed by each successively nested pair. See `1-nominals/cases.md` §IV for the full rule.

> **Nested example:** `kis fojrasi lujmi` = "my fire's light" — `kis` owns `fojrasi`, which owns `lujmi`
> 
> Free order (`lujmi fojrasi kis`) is not valid for nested possession.

### D. Passive Voice

Kilor expresses passive voice (agent demotion or deletion) using the instrumental particle **`sy`** as a valency-reducing marker. See `1-nominals/cases.md` §V-E for the full specification with all three usage patterns (instrumental, passive agent-deleted, passive agent-expressed).

In brief:

| Pattern | Example |
|:---|:---|
| `Patient sy verb` | `hawu sy tavka.` — "The animal was eaten." |
| `Patient sy agent verb` | `hawu sy a-fojra tavka.` — "The animal was eaten by the fire." |

The patient is promoted to NOM (unmarked). The agent (if expressed) follows `sy` with no case suffix. The verb carries no morphological change — valency reduction is signalled entirely by `sy`.

> **Note:** OSV word order (§I-B) can topicalise the object but cannot delete the agent. Passive `sy` is the only mechanism for structurally omitting the agent from the clause.

### E. Modifier Placement & Oblique PP Order

#### Adjectives

Adjectives (noun + `-s` or quality roots used attributively) **precede** the noun:

> `rajlis a-maeha` — "big person" (lit. "big the-person")

Intensity adverbs (`wes`, `mevres`) precede the adjective:

> `wes rajlis a-maeha` — "very big person"

#### Oblique PPs — Fixed Order

When multiple oblique prepositional phrases appear, they follow the **fixed order**:

```
Object [ACC] — [Numeral] — [sy Instrumental] — [te Dative] — [Adverb] — Verb
```

> `bau-ni ro sy y-maliu te kis song shuks souvnar` — "quickly give three breads to my friend with an iron knife"

The object (with optional ACC case suffix) and any numeral come first. Instrumental `sy` precedes dative `te`. Manner adverbs (`-s` derived from quality roots or verbs) **precede the verb**.

#### Full Clause Template (SOV)

```
[Emo]  [Temporal]  [Intensity Adv]  [Adj]  [Subject-NOM]  [Relative Clause]  [Object-ACC]  [Numeral]  [sy Instr]  [te Dat]  [Manner Adv]  [Emo]  [Verb]  [nar]
```

All slots are optional except the subject and verb. `[Emo]` is an optional emotional particle (see `3-subsystems/colour-emotion.md` §IV). The clause-initial `[Emo]` sets the emotional frame for the entire clause; the pre-verbal `[Emo]` scopes over the verb only.

#### Maximal Example Sentence

```
piroi  wes  rajlis  a-maeha  kus kin avrgona  bau-ni ro  sy y-maliu  te kis song  shuks  souvnar  nar.

ei  imaroi  bau  sy a-fojra  tavka.

amer  ki  mangus kil  torra  rajlis.
```

**Translation:** "Yesterday the very big person who loves me did not quickly give three breads to my friend with an iron knife. And today the bread was eaten by the fire. But I am the biggest among us."

For details on the subsystems referenced above:
- `3-subsystems/temporals.md` — temporal expression (clause-initial slot)
- `3-subsystems/colour-emotion.md` — emotional particles (clause-initial and pre-verbal slots)
- `3-subsystems/comparatives.md` — comparatives & superlatives
- `2-predication/subordination.md` — subordination & relative clauses
- `2-predication/negation.md` — clausal negation (`nar`)

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

> **Example:** `lujmi` (light, H→L) + `sojla` (star, H→L) → `lujmi sojla` (star-light, multi-word vocab)

### B. Word-Unit Processing

Kilor distinguishes two forms of compounding for tone purposes:

1. **Mono-word compounds** — roots fused into a single orthographic word. These are treated as a single word for tone: the Last-3 Domain Rule applies across the entire word (see `0-foundation/tone-prosody.md` §IV-A).

   > **Phonotactic constraint:** Start-only onsets (`sh`, `ch`, `th`, `sl`, `kl`, `tl`, `bl`, `ml`; see `0-foundation/phonology.md` §III-C) and ending-only consonants (`ng`, `x`; see `0-foundation/phonology.md` §III-B) are restricted to word-peripheral positions. A root beginning with a start-only onset or ending with an ending-only consonant may **not** appear as a non-initial or non-final element in a mono-word compound — such combinations must use multi-word vocabs instead. Only roots composed entirely of core consonants (see `0-foundation/phonology.md` §III-A) may appear in any position within a mono-word compound.

2. **Multi-word vocabs** — two or more words written with spaces that together form one semantic concept (e.g., `sojlas lujmi`). Each word retains its own tonal contour independently via Modular Stitching (see `0-foundation/tone-prosody.md` §IV-D). The contours are stitched sequentially, not recalculated across word boundaries.

   > **Case suffix distribution:** When a multi-word vocab receives a case suffix (Accusative or Genitive), the suffix attaches **only to the last word** of the vocab. The earlier words remain unmarked. The colour prefix (if present) attaches orthographically to the first word and does not affect suffix placement. See `1-nominals/cases.md` §III–IV for case usage rules.

### C. Root Constraints

- All roots must obey the CV/CVC/VC/V syllable templates
- No `j` or `v` may appear in any root
- No consonant clusters
- No 1- or 2-syllable root may end in `s` natively — `-s` is reserved as the modifier derivational suffix
- 3+ syllable roots **may** end in `s` natively (e.g., `marokas`), pronounced as English plural `-s` (`/s/` or `/z/`). This is permitted because the `-s` derivational suffix does not apply to 3+ syllable words — tone pattern alone distinguishes categories at that length, so there is no ambiguity.
- Pronoun genitive forms (`kis`, `tis`, `sis`, `nis` and their plurals) are **inflected**, not roots, and are exempt from the `-s` constraint
- Closed-class function words (`dir`, `res`, `nar`, `iu`, `na`, `te`, `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus`, `tor`, `les`, `torra`, `wetor`, `mangus`) are **exempt** from the `-s` constraint. This is the **single source of truth** for the closed-class particle inventory — all other files reference this list. The `-s` restriction applies only to open-class content roots (Nouns, Verbs, Adjectives, Adverbs) that participate in the derivational `-s` system. Function words are a fixed inventory and never receive derivational morphology.

---

## V. The `-s` Derivational Suffix

### A. Category Derivation

The suffix `-s` creates modifiers from base roots. It applies to **1 and 2 syllable** words only. 3+ syllable words distinguish all 4 categories through tone pattern alone (see `0-foundation/tone-prosody.md`).

| Derivation | Result | Applies To |
|:---|:---|:---|
| Noun + `-s` | Adjective | 1 & 2 syllable nouns |
| Verb + `-s` | Adverb | 1 & 2 syllable verbs |
| Quality root + `-s` | Manner Adverb | 1 & 2 syllable adjective/quality roots (lexicon `category: a`) |

> **1-syllable verb → adverb:** `fei` (verb, toneless) → `feis` (adverb, toneless)
> **2-syllable noun → adjective:** `aujli` (noun, H→L) → `aujlis` (adjective, H→L)
> **1-syllable quality → manner adverb:** `shuk` (adj: fast) → `shuks` (adv: quickly)
> **1-syllable quality → manner adverb:** `gor` (adj: good) → `gors` (adv: well)

> **Note:** "Quality roots" are roots whose lexical category in `lexicon.csv` is `a` (adjective). These roots describe attributes (e.g., big, small, hot, cold, fast, good) and derive manner adverbs via `-s`. The `a` category label is a lexicon-internal convention, not a grammatical term visible in speech.

Manner adverbs derived from quality roots are distinguished from attributive adjectives by **position**: adjectives precede nouns (§I-E), manner adverbs precede verbs (§I-E). The same `-s` form serves both roles — context disambiguates.

### B. Phonological Nature

`s` is a **toneless extrasyllabic appendix** — pronounced like English plural `-s` (`/s/` or `/z/`). It does not add a syllable, does not carry `j` or `v`, and does not affect the last-3 tone domain.

---

## VI. Plural Strategy — No Plural Marking

Kilor has **no plural marking** — neither suffixes, nor prefixes, nor tonal changes indicate plurality. This follows the Chinese approach: number is inferred from **context, quantifiers, and numerals**.

To express quantity explicitly, use **numeral + optional measure word + noun** constructions (see `3-subsystems/numerals.md` §VI) or quantifier words (many, few, all, some, three, etc.).

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

This is a closed-class morphological process that applies **only** to pronouns. See `1-nominals/pronouns.md` §II-B for full details.

---

## VII. No Possessive Suffixes

Kilor has **no dedicated agglutinative possessive suffix**. Possession is expressed exclusively through the **Genitive case** suffix (`-si`/`-sa`). See `1-nominals/cases.md` for full details.

---

*End of Grammar & Syntax Specification.*