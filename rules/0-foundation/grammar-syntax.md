# Kilor Grammar & Syntax

**Module:** Word Order, Harmony, Compounding, Plural Strategy
**Status:** Canonical
**Last updated:** 2026-07-12
**Version:** 2.2.0
**Depends on:** `0-foundation/phonology.md`, `0-foundation/tone-prosody.md`, `1-nominals/demonstratives.md`, `3-subsystems/spatials.md`

---

## I. Word Order

### A. Default: SOV

Kilor's **default, unmarked** word order is **Subject–Object–Verb (SOV)**. This is the natural order for everyday speech and standard prose.

> **Note:** SOV is a **pedagogical baseline** — the simplest model for explaining Kilor's core syntax. Real sentences may include additional elements (prepositions, numerals, temporal words, question words, etc.) that create more complex structures. The SOV model describes the relative order of the three core arguments; other elements are placed according to their own rules (see `2-predication/interrogative.md` for question word fronting, `1-nominals/cases.md` §V for dative/instrumental particles).

> **Example:** `a-fora hawuni taka.`
> (the-fire animal-ACC eat.)
> SUBJ [NOM] — OBJ [ACC] — VERB
> "The fire eats the animal."

### A2. Zero-Subject Clauses (Impersonal)

For weather and ambient conditions, the subject may be **omitted entirely**. The bare content word (noun or quality root) stands alone as a complete clause:

> `hupli.` — "It's raining." (bare noun = "Rain.")
> `kop.` — "It's cold." (bare quality root)
> `my.` — "It's dark." (bare quality root)
> `foshu.` — "It's a blizzard." (bare noun)

Negation follows the standard pattern (§I-E, `2-predication/negation.md`):

> `kop nar.` — "It's not cold."
> `hupli nar.` — "It's not raining."

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

> **Example:** `forasi lumi` (fire's light) ≡ `lumi forasi` (light of fire)

For **nested possession** (multiple Genitive-marked nouns chained together), Kilor uses a **fixed recursive order**: each possessor must **precede** what it owns. The outermost possessor comes first, followed by each successively nested pair. See `1-nominals/cases.md` §IV for the full rule.

> **Nested example:** `kis forasi lumi` = "my fire's light" — `kis` owns `forasi`, which owns `lumi`
>
> Free order (`lumi forasi kis`) is not valid for nested possession.

### D. Passive Voice

Kilor expresses passive voice (agent demotion or deletion) using the instrumental particle **`sy`** as a valency-reducing marker. See `1-nominals/cases.md` §V-E for the full specification with all three usage patterns (instrumental, passive agent-deleted, passive agent-expressed).

In brief:

| Pattern | Example |
|:---|:---|
| `Patient sy verb` | `hawu sy taka.` — "The animal was eaten." |
| `Patient sy agent verb` | `hawu sy a-fora taka.` — "The animal was eaten by the fire." |

The patient is promoted to NOM (unmarked). The agent (if expressed) follows `sy` with no case suffix. The verb carries no morphological change — valency reduction is signalled entirely by `sy`.

> **Note:** OSV word order (§I-B) can topicalise the object but cannot delete the agent. Passive `sy` is the only mechanism for structurally omitting the agent from the clause.

### E. Modifier Placement & Oblique PP Order

#### NP-Internal Word Order

Within the noun phrase, modifiers follow a fixed order relative to the head noun:

```
[Demo] — [Poss GEN] — [Adj] — [(Colour-)Noun] — [Num/Quant] — [Rel Clause]
```

| Slot | Position | Example | Notes |
|---|---|---|---|
| Demonstrative | Pre-nominal (leftmost) | `thin` | `thin`/`tha`; replaces colour prefix unless 異體字 override (see `1-nominals/demonstratives.md`) |
| Possessor (GEN) | Pre-nominal | `kis` | Pronoun GEN or noun + `-si`/`-sa` |
| Adjective | Pre-nominal | `ralis` | Noun/quality root + `-s` |
| Head Noun | Centre | `bau` | May carry colour prefix or be bare |
| Numeral / Quantifier | Post-nominal | `ro`, `esa`, `roli` | See `3-subsystems/numerals.md` §VI |
| Relative Clause | Post-nominal (rightmost) | `kus ...` | See `2-predication/subordination.md` §II |

All slots are optional except the head noun. NP-internal order is **rigid** (no poetic reordering within the NP).

> **Full NP example:** `thin kis ralis bau ro kus ki taka ger`
> "these three big breads of mine that I ate"
>
> thin — kis — ralis — bau — ro — [kus ki taka ger]
> this — my — big — bread — three — that I ate

#### Adjectives

Adjectives (noun + `-s` or quality roots used attributively) **precede** the noun:

> `ralis a-maeha` — "big person" (lit. "big the-person")

Intensity adverbs (`wes`, `meres`) precede the adjective:

> `wes ralis a-maeha` — "very big person"

#### Oblique PPs — Fixed Order

When multiple oblique prepositional phrases appear, they follow the **fixed order**:

```
Object [ACC] — [Numeral] — [sy Instrumental] — [mer Comitative] — [spatial-ne / tilpe] — [ar Ablative] — [te Dative] — [Adverb] — Verb
```

> `bauni ro sy y-maliu mer kis song slato-si ikne te ti shuks sounar` — "quickly give three breads to you with an iron knife with my friend inside the house"

The object (with optional ACC case suffix) and any numeral come first. When multiple obliques co-occur, the fixed order is `sy` (Instrumental) > `mer` (Comitative) > spatial postpositions / `tilpe` (Locative-relational & Spatial) > `ar` (Ablative) > `te` (Dative). Manner adverbs (`-s` derived from quality roots or verbs) **precede the verb**. For the full spatial postposition inventory (`ikne`, `oukne`, `umne`, `rapne`, `haune`, `paune`, `hinne`, `tene`, `orane`, `meipone`, `tilpe`), see `3-subsystems/spatials.md`.

#### Modal Verbs

Root modal verbs (`mug` "want", `som` "need", `sew` "can", `hostak` "must", `shunle` "should") form a **bare serial construction** with the main verb. The modal directly precedes the main verb — no complementizer is used. The object stays before the modal+verb complex:

> `ki bau mug taka.` — "I want to eat bread." (lit. "I bread want eat.")
> `ki fei sew.` — "I can fly."
> `ki bau som taka.` — "I need to eat bread."

Modals can **stack**:

> `ki fei mug sew.` — "I want to be able to fly."

The modal sits between the manner adverb and the verb:

> `ki bau mug shuks taka.` — "I want to quickly eat bread."

Epistemic modals (`hostakes` "certainly", `sewanes` "might", `bamares` "would have") are pre-verbal adverbs and already occupy the `[Manner Adv]` slot.

#### Full Clause Template (SOV)

```
[Emo]  [Temporal]  [Intensity Adv]  [NPSUBJ]  [NPOBJ]  [Numeral]  [sy Instr]  [mer Com]  [spatial-ne / tilpe]  [ar Abl]  [te Dat]  [Manner Adv]  [Modal]  [Emo]  [Verb]  [nar]
```

Where NPSUBJ and NPOBJ expand to:

```
NPSUBJ: [Demo]  [Poss GEN]  [Adj]  [(Colour-)Noun]  [Rel Clause]
NPOBJ:  [Demo]  [Poss GEN]  [Adj]  [(Colour-)Noun]  [Rel Clause]  [Num/Quant (on OBJ side preceding Numeral slot)]
```

All slots are optional except the subject and main verb. `[Emo]` is an optional emotional particle (see `3-subsystems/colour-emotion.md` §IV). The clause-initial `[Emo]` sets the emotional frame for the entire clause; the pre-verbal `[Emo]` scopes over the verb only. `[Modal]` is an optional root modal verb (`mug`, `som`, `sew`, `hostak`, `shunle`); epistemic modals (`hostakes`, `sewanes`, `bamares`) occupy the `[Manner Adv]` slot.

#### Maximal Example Sentence

```
piroi  wes  ralis  a-maeha  kus kin avrgonna  bauni ro  sy y-maliu  mer kis song  slato-si ikne  te ti  shuks  sounar  nar.

ei  imaroi  bau  sy a-fora  taka.

amer  ki  mangus kil  torra  ralis.
```

**Translation:** "Yesterday the very big person who loves me did not quickly give three breads to you with an iron knife with my friend inside the house. And today the bread was eaten by the fire. But I am the biggest among us."

For details on the subsystems referenced above:
- `3-subsystems/temporals.md` — temporal expression (clause-initial slot)
- `3-subsystems/colour-emotion.md` — emotional particles (clause-initial and pre-verbal slots)
- `3-subsystems/spatials.md` — spatial postpositions (`-ne` suffix, `tilpe` = between)
- `3-subsystems/comparatives.md` — comparatives & superlatives
- `2-predication/subordination.md` — subordination & relative clauses
- `2-predication/negation.md` — clausal negation (`nar`)
- `1-nominals/demonstratives.md` — demonstratives (`thin`/`tha`)

---

## II. Contrastive Suffix Rule

Suffixes use the vowel class **opposite** to the root's last-syllable nucleus. This creates a pleasant front↔back alternation at the root-suffix boundary.

| Last-Syllable Vowel Class | Suffix Class | Vowels |
|:---|:---|:---|
| **Front / Bright** | Uses Back suffix | e, i, y, ae, ei, eu, iu → `-na` (ACC), `-sa` (GEN) |
| **Back / Deep** | Uses Front suffix | a, o, u, ai, au, oi, ou → `-ni` (ACC), `-si` (GEN) |

> **Example (last vowel `a` = back → front suffix):** `fora` (fire, noun) + Accusative → `forani` (uses `-ni`, not `-na`)
> **Example (last vowel `i` = front → back suffix):** `lumi` (light, noun) + Accusative → `lumina` (uses `-na`, not `-ni`)

### Proclitic Exemption

The **colour prefix** is an external proclitic. It sits outside the phonological boundary of the root and **does not** trigger or participate in the Contrastive Suffix Rule. Only the root's last-syllable nucleus determines suffix vowel class.

> **Example:** `a-forasi` — the prefix `a` is Front, but the root's last vowel `a` is Back, so the Genitive suffix uses front `-si`.

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

> **Example:** `lumi` (light) + `sola` (star) → `lumi sola` (star-light, multi-word vocab)

### B. Word-Unit Processing

Kilor distinguishes two forms of compounding:

1. **Mono-word compounds** — roots fused into a single orthographic word. These are treated as a single word: for 3+ syllable compounds, the Last-3 Domain Rule applies across the entire word (see `0-foundation/tone-prosody.md` §IV-A). 1–2 syllable mono-word compounds are toneless.

   > **Phonotactic constraint:** Start-only onsets (`sh`, `ch`, `th`, `sl`, `kl`, `tl`, `bl`, `ml`; see `0-foundation/phonology.md` §III-C) and ending-only consonants (`ng`, `x`; see `0-foundation/phonology.md` §III-B) are restricted to word-peripheral positions. A root beginning with a start-only onset or ending with an ending-only consonant may **not** appear as a non-initial or non-final element in a mono-word compound — such combinations must use multi-word vocabs instead. Only roots composed entirely of core consonants (see `0-foundation/phonology.md` §III-A) may appear in any position within a mono-word compound.

2. **Multi-word vocabs** — two or more words written with spaces that together form one semantic concept (e.g., `solas lumi`). Each word is processed independently via Modular Stitching (see `0-foundation/tone-prosody.md` §IV-D).

   > **Case suffix distribution:** When a multi-word vocab receives a case suffix (Accusative or Genitive), the suffix attaches **only to the last word** of the vocab. The earlier words remain unmarked. The colour prefix (if present) attaches orthographically to the first word and does not affect suffix placement. See `1-nominals/cases.md` §III–IV for case usage rules.

### C. Root Constraints

- All roots must obey the CV/CVC/VC/V syllable templates
- No `j` or `v` may appear in any root of 1–2 syllables (toneless). `j` and `v` appear only as tone markers on 3+ syllable words
- No consonant clusters
- No 1- or 2-syllable root may end in `s` natively — `-s` is reserved as the modifier derivational suffix
- 3+ syllable roots **may** end in `s` natively (e.g., `marokas`), pronounced as English plural `-s` (`/s/` or `/z/`). This is permitted because the `-s` derivational suffix does not apply to 3+ syllable words — tone pattern alone distinguishes categories at that length, so there is no ambiguity.
- Pronoun genitive forms (`kis`, `tis`, `sis`, `nis` and their plurals) are **inflected**, not roots, and are exempt from the `-s` constraint
- Closed-class function words (`res`, `ero`, `nar`, `iu`, `na`, `te`, `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `pem`, `pona`, `pemna`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus`, `tor`, `les`, `torra`, `wetor`, `mangus`, `sor`, `chom`, `maug`, `gin`, `ger`, `gou`, `bam`, `fidak`, `arfi`) are **exempt** from the `-s` constraint. Numerals (`mo`, `do`, `ro`, `foi`, `tai`, `slo`, `lai`, `auk`, `wy`, `gau`, `mai`, `doi`, `rai`, `aniu`, `cu`, `kas`, `hus`, `tus`, `rakas`) are a **closed class** and are also exempt. This is the **single source of truth** for the closed-class particle inventory — all other files reference this list. The `-s` restriction applies only to open-class content roots (Nouns, Verbs, Adjectives, Adverbs) that participate in the derivational `-s` system. Function words and numerals are a fixed inventory and never receive derivational morphology.

Note: `hei` (vocative, `3-subsystems/imperatives.md`) and `shen` (reflexive, `2-predication/subordination.md` §VII) are open-class content roots, subject to `-s` derivation and not in the closed-class exemption list.

---

## V. The `-s` Derivational Suffix

### A. Category Derivation

The suffix `-s` creates modifiers from base roots. It applies to **1 and 2 syllable** words only. 3+ syllable words distinguish all 4 categories through tone pattern alone (see `0-foundation/tone-prosody.md`).

For 1–2 syllable words:

| Derivation | Result | Applies To |
|:---|:---|:---|
| Root + `-s` | Adjective & Adverb | All 1 & 2 syllable roots |

The bare root serves as both noun and verb. Adding `-s` creates the modifier form, which serves as both adjective and adverb. Position disambiguates: adjectives precede nouns (§I-E), adverbs precede verbs (§I-E).

> **1-syllable examples:** `fei` (bare root: fly/verbal noun) → `feis` (modifier: flying/flyingly). `shuk` (quality root: fast) → `shuks` (adv: quickly).
> **2-syllable example:** `fora` (bare root: fire/burn) → `foras` (modifier: fiery/burningly).
> **Quality root:** `gor` (adj: good) → `gors` (adv: well).

> **Note:** "Quality roots" are roots whose lexical category in `lexicon.csv` is `a` (adjective). These roots describe attributes (e.g., big, small, warm, cold, fast, good) and derive manner adverbs via `-s`. The `a` category label is a lexicon-internal convention, not a grammatical term visible in speech.

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