# Kilor Compounding

**Module:** Multi-Word Compounding & Mono/Multi Decision Rules
**Status:** Canonical
**Last updated:** 2026-08-13
**Version:** 1.1.0
**Depends on:** `0-foundation/grammar-syntax.md` (compounding §IV, clause template §I-E), `0-foundation/tone-prosody.md` (Modular Stitching §IV-D, Last-3 Domain §IV-A), `0-foundation/phonology.md` (§IV positional consonant classes), `1-nominals/nouns-colour-prefix.md`, `3-subsystems/derivational-suffixes.md`, `3-subsystems/derivational-prefixes.md`

**Companion file:** `3-subsystems/derivational-suffixes.md` — 12 derivational suffixes (-mae, -tek, -lu, -rin, -par, -lise, -ius, -eus, -ia, -wes, -rem, -rum), suffix syntax, formal register, colour prefix rules for suffixes. See also `3-subsystems/derivational-prefixes.md` — 3 derivational prefixes (`pi-`, `pa-`, `sefta-`).

---

Kilor compounding combines content roots into complex concepts. Two forms coexist:

1. **Multi-word compounds** — two or more words written with spaces; each word processed independently via Modular Stitching
2. **Mono-word compounds** — fused into a single orthographic word with one tone domain

For derivational suffixes (fusion of 1-syllable abstract heads), see `3-subsystems/derivational-suffixes.md`.

---

## I. Multi-Word Compounding Heads

Heads that are 2+ syllables or semantically concrete remain as separate words in productive two-word compounds.

| # | Head | Full Root | Domain | Category | Meaning |
|---|---|---|---|---|---|
| 1 | `param` | `param` | Result | n | result / thing made |
| 2 | `pos` | `poska` | Location | n | place |
| 3 | `isra` | `lokisra` | Doctrine | n | doctrine / system |
| 4 | `afaloi` | `afaloi` | Capability | nv | ability / able to |
| 5 | `naras` / `narau` | `narau` | Without/Lack | n | without / -less |
| 6 | `posia` | `posia` | Realm/Land | n | land of / realm of |
| 7 | `lote` | `lote` | Collective | n | group / multitude (human nouns only; see §I-G) |

All heads are open-class content roots — they carry colour prefixes and accept `-s` derivation per standard rules.

> **Upgrade note:** §I heads default to multi-word but may optionally fuse into a mono-word compound when the compound is a lexically entrenched cultural concept, the fused form is ≤ 5 syllables, and no phonotactic block applies. See §III Rule 5 for the full upgrade criteria. When fused, the resulting word follows Last-3 Domain tone rules (`0-foundation/tone-prosody.md` §IV-A).

### A. Result — `verb + param`

| Form | Meaning |
|---|---|
| `tesak param` | creation (thing created) |

Takes colour prefix `o-` (abstract).

### B. Location — `noun + pos`

| Form | Meaning |
|---|---|
| `wem pos` | warm-place (greenhouse) |
| `bau pos` | bread-place (bakery) |
| `hamin pos` | food-place (kitchen/dining hall) |

Takes colour prefix `ae-` (physical boundaries/earth).

### C. Doctrine — `noun + isra`

| Form | Meaning |
|---|---|
| `ero isra` | existentialism (existence-doctrine) |
| `eli isra` | vitalism (life-doctrine) |

Takes colour prefix `o-` (abstract system).

### D. Capability — `afaloi + verb`

| Form | Meaning |
|---|---|
| `afaloi taka` | edible (able-to-eat) |
| `afaloi taki` | drinkable |
| `afaloi tesak` | creatable / makeable |

`afaloi` precedes the verb (modifier position). This pattern is distinct from the periphrastic `sew + verb` ("can X" as a verb phrase) — `afaloi taka` is a nominal/adjectival compound ("edible"), while `sew taka` is a predicate ("can eat"). Takes colour prefix `o-` (abstract).

### E. Without/Lack — `narau + noun` / `noun + naras`

| Form | Meaning |
|---|---|
| `narau lira` | without water (prepositional) |
| `lira naras` | waterless (derivational) |

Two syntactic patterns with the same root:
- **Preposed `narau`:** prepositional usage — `narau lira` = "without water"
- **Postposed `naras`:** derivational compounding — `lira naras` = "waterless"

The postposed form `naras` follows the standard head-last compounding pattern. Takes colour prefix `o-` (abstract).

### F. Realm/Land — `noun + posia`

| Form | Meaning |
|---|---|
| `fos posia` | land of ice |
| `fora posia` | fire-realm / land of fire |

`posia` is a content root meaning "land, realm, domain" — the elevated counterpart to everyday `pos` ("place"). While `pos` forms practical location compounds (bakery, greenhouse), `posia` forms names for countries, regions, mythical realms, and poetic toponyms.

Takes colour prefix `ae-` (physical boundaries/earth): `ae-fos posia` = "the land of ice."

### G. Collective — `noun + -lo` / `noun + lote`

| Form | Meaning | Rule |
|---|---|---|
| `maehalo` | people (collective, unspecified number) | Bare root, clean fuse |
| `mamaelo` | mothers (collective) | Bare root, clean fuse (reduplicative, not agent-derived) |
| `famae` → `famaelo` | fathers (collective) | Bare root, clean fuse |
| `song lote` | friends (collective) | End-only `ng` blocks fusion (§II) |
| `takamae lote` | eaters (collective) | Derived stem — `-mae` already consumed the one-suffix slot |
| `kirolote` | paragraph (a group of text) | Non-human — full `lote`, head-class prefix |

`lote` is a content root meaning "group, multitude, collective." It forms collectives
with two surface forms, split by whether the base is a human noun undergoing **clean**
fusion:

- **Fused `-lo` — HUMAN NOUNS ONLY, clean fusion only.** When the human noun is a bare
  root with no prior derivational suffix AND no phonotactic block (end-only/edge-only
  consonant at the root boundary). The shortened combining form `-lo` fuses directly:
  `maehalo`, `mamaelo`, `famaelo`. The fused `-lo` is the grammatically special,
  human-collective marker.
- **Full `lote` — everything else.** Used for:
  - **Human nouns where clean fusion is blocked:** one-suffix-per-word constraint
    (`derivational-suffixes.md` §II-A, e.g. `takamae` with `-mae`), or a phonotactic
    block (§II, e.g. `song` with `ng`).
  - **Non-human / any other term** (extended usage): `kirolote` = "group of text" →
    paragraph, `theslote` = "group of equipment", etc. Here `lote` is the ordinary
    full word "group", and the whole reads as a general "group of X".

Pronouns are a **closed class** that always fuses `-lo`: `kilo`, `tilo`, `silo`, `nilo`. See `1-nominals/pronouns.md` for the full pronoun paradigm.

**Numeral constraint:** `-lo` / `lote` never co-occurs with numerals. Use either `a-song ro` (three friends) or `song lote` (friends, collective, unspecified number), never `*song lote ro`. This mirrors the Chinese 們/number mutual-exclusion pattern.

**Colour prefix:**
- Human `-lo` / human `lote`: takes `a-` (living beings/human): `a-maehalo` = "the people," `a-mamaelo` = "the mothers."
- Non-human `lote`: takes the **head/referential class prefix** (the class of the thing being grouped): `kirolote` (text matter) → `o-` (abstract), matching `kiro`.

---

## II. Multi-Word Compound Syntax

Multi-word compounds are two orthographic words with a space. Each word is processed independently per Modular Stitching (`0-foundation/tone-prosody.md` §IV-D):

- 1–2 syllable heads: toneless (flat mid)
- 3+ syllable heads: follow their own Last-3 Domain

Colour prefixes attach to the **head noun** (the last word): `ae-bau pos` (the bakery). Case suffixes attach only to the head: `bau posni` — bakery (ACC).

Three situations produce multi-word forms:

### 1. Phonotactic block

When a root ends in an end-only or edge-only consonant, fusion is blocked (see `derivational-suffixes.md` §II-A). The head appears as a separate word:

| Form | Meaning | Rule |
|---|---|---|
| `klush lu` | courage | `klush` ends in edge-only `sh` |
| `song lise` | fated friend | `song` ends in end-only `ng` |

### 2. Derived stem + head

When a head attaches to a word that already carries a derivational suffix (a derived stem), the head appears as a separate word. Head-last semantics apply: the rightmost element is the head; everything left modifies it.

| Form | Structure | Meaning |
|---|---|---|
| `argonnalise mae` | `[[argonna]-lise] mae` | person characterized by fated love |
| `takamae lise` | `[[taka]-mae] lise` | the lived condition of being an eater |

### 3. Multi-syllable / semantically concrete heads

Heads in §I always appear as separate words by default — see §III for the optional mono upgrade path.

---

## III. Content-Root Compounding: Mono vs. Multi Decision Rules

When two **ordinary content roots** are combined — neither a derivational suffix (`derivational-suffixes.md` §I) nor a §I defined head — or when a §I head is a candidate for optional upgrade, the following priority-ordered rules determine whether the compound is written as a mono-word (fused, one tone domain) or a multi-word compound (separated, each word independent per Modular Stitching).

### 0. Definitions

| Term | Definition | Example |
|:---|:---|:---|
| **Derivational suffix** | `derivational-suffixes.md` §I suffixes + collective `-lo` | `-mae`, `-lise`, `-lo` |
| **Defined head** | §I content-root heads | `pos`, `posia`, `lote` |
| **Ordinary content root** | Any root not in the above two categories | `fora`, `gilan`, `bau`, `wem` |
| **Non-colour prefix** | Word-internal derivational prefix (lexical, not grammatical proclitic) | `pi-`, `pa-`, `rem-`, `rum-`, `sef-` |
| **Phonotactic block** | An edge-only (`sh`,`ch`,`th`), end-only (`ng`,`x`,`rk`), or start-only consonant at a morpheme boundary in a non-peripheral position — see `0-foundation/phonology.md` §IV | `song` + `lise` → blocked by `ng` |

### 1. Priority-Ordered Rules

**Rule 1** ⚠️ *Non-overridable* — **Derivational suffixes → mono**

All derivational suffixes and the collective suffix `-lo` **must** fuse with their base root into a single word, unless blocked by Rule 2. See `derivational-suffixes.md` §II.

```
takamae  ✅     gorlise  ✅     auronius  ✅     maehalo  ✅
```

**Exception:** The one-suffix-per-word constraint — if a derived stem already carries a suffix, the second derivational head must appear as a separate word: `takamae lote` (not `*takamaelote`).

---

**Rule 2** ⚠️ *Non-overridable* — **Phonotactic block → multi**

When the morpheme boundary would place an edge-only, end-only, or start-only consonant in a non-peripheral position, fusion is **forbidden**. The head must appear as a separate word, using its full-root form when applicable.

| Blocked fusion | Valid form | Reason |
|:---|:---|:---|
| `*songlise` | `song lise` | End-only `ng` at word-medial position |
| `*klushlu` | `klush lu` | Edge-only `sh` at word-medial position |
| `*songius` | `song rius` | End-only `ng` + full-root form `rius` |
| `*auromlar` | `auro mlar` | Start-only `ml` at word-medial position |

---

**Rule 3** — **Default: ordinary content-root compounds → multi**

All new compounds formed from two ordinary content roots default to multi-word.

```
fora gilan       won lira       gilan fora
sym rilse        bau pos        gilan fora
```

---

**Rule 4** — **Default: §I defined heads → multi**

§I content-root heads default to multi-word, but may be overridden by Rule 5.

```
tesak param      bau pos        ero isra
afaloi taka      lira naras     fos posia
```

---

**Rule 5** — *Optional upgrade* — **Lexicalisation + length + no block → mono**

A compound that defaults to multi (Rule 3 or Rule 4) may be upgraded to mono when **all three** conditions are met:

| Condition | Criterion |
|:---|:---|
| **A. Semantic lexicalisation** | The compound denotes a stable cultural concept with its own dictionary entry, not an ad-hoc descriptive combination |
| **B. Fused length ≤ 5 syllables** | `syllables(base) + syllables(head) ≤ 5` |
| **C. No phonotactic block** | The morpheme boundary does not violate Rule 2 |

**Exception:** Highly lexicalised proper nouns (place names, personal names, technical terms) may exceed the 5-syllable limit.

| Compound | Lexicalised? | Syllables | Blocked? | Verdict |
|:---|:---|:---|:---|:---|
| `fora` + `gilan` = volcano | ✅ | 4 ✅ | None ✅ | **mono:** `foragilan` |
| `gilan` + `fora` = wildfire on mountain | ❌ | 4 | None | **multi:** `gilan fora` |
| `sym` + `rilse` = myth | ✅ | 3 ✅ | None ✅ | **mono:** `symrilse` |
| `wem` + `pos` = greenhouse | ✅ | 2 ✅ | None ✅ | **mono:** `wempos` |
| `bau` + `pos` = bakery | ❌ | 2 | None | **multi:** `bau pos` |
| `messa` + `posia` = great-land | ✅ | 5 ✅ | None ✅ | **mono:** `messaposia` |
| `taix` + `sik` = disaster | ✅ | 3 | `x` ❌ | **multi:** `taix sik` |

---

**Rule 6** — **Word order = semantics (head-final)**

The modifier precedes the head. The last element is the semantic head (the thing being defined). This rule is **orthogonal** to mono/multi — it applies identically to both forms.

| Order | Meaning | Head |
|:---|:---|:---|
| `fora gilan` / `foragilan` | volcano (mountain of the fire-type) | `gilan` (mountain) |
| `gilan fora` / `gilanfora` | wildfire (fire on the mountain) | `fora` (fire) |

---

**Rule 7** — **Mono and multi forms may coexist**

A lexicalised compound may have both forms. The mono form is the fused, dictionary-entry version; the multi form is the analytic version usable in poetry, pedagogy, or formal register.

```
foragilan   = volcano (fused, dictionary entry)
fora gilan  = volcano (analytic, poetic/pedagogical)
```

### 2. Decision Flowchart

```
Two-component combination
│
├─ One is a derivational suffix (derivational-suffixes.md §I)?
│   ├─ Yes → Rule 1: Check phonotactic block
│   │        ├─ No block → mono
│   │        └─ Blocked → multi (Rule 2)
│   └─ No ↓
│
├─ Phonotactic block at boundary?
│   ├─ Yes → Rule 2: forced multi
│   └─ No ↓
│
├─ One is a non-colour prefix?
│   ├─ Yes → mono (forced fusion), counts toward tone domain
│   └─ No ↓
│
├─ §I head or ordinary content roots?
│   ├─ Default: Rule 3/4 → multi
│   └─ Optional upgrade: Rule 5 → mono (lexicalised + ≤5syl + no block)
│
└─ Word order (modifier-before-head) decided before mono/multi → Rule 6
```

### 3. Non-Colour Prefixes

Prefixes such as `pi-`, `pa-`, `rem-`, `rum-`, `sef-` are **word-internal derivational prefixes** (lexical, creating new dictionary entries), distinct from colour prefixes (grammatical proclitics).

| Property | Colour prefix `a-` | Non-colour prefix `pa-` |
|:---|:---|:---|
| Nature | External proclitic (grammatical) | Word-internal prefix (lexical) |
| Counts toward syllable count? | ❌ | ✅ |
| Counts toward tone domain? | ❌ | ✅ |
| Space before root? | ❌ Hyphenated (`a-fora`) | ❌ Fused (`pares`) |
| Replacing prefix creates new word? | ❌ (same word, different ontological class) | ✅ (new dictionary entry) |

Non-colour prefixes always fuse — they cannot form multi-word compounds. The fused word follows standard tone rules: 1–2 syllable forms are toneless; 3+ syllable forms receive Last-3 Domain tone markers.

```
pires   = pi + res   (2 syl, toneless)
pafora  = pa + fora  (3 syl → Last-3 Domain)
remres  = rem + res  (2 syl, toneless)
```

### 4. Modifier Tone in Multi-Word Compounds

Per Modular Stitching (`0-foundation/tone-prosody.md` §IV-D), each word in a multi-word compound is processed independently. The modifier retains its own part-of-speech form and tone contour — it does **not** adopt the head's category.

| Modifier syllables | Modifier form | Example |
|:---|:---|:---|
| 1–2 syl | Root + `-s` (toneless) | `ralis bau` (big bread) |
| 3+ syl | Adjective tone pattern (`j` on 2nd of last-3) | `rujsome lunlavgak` |

Each word's tone domain is sealed — no cross-word tone sandhi occurs.

### 5. Quick Reference

| Situation | Action | Rule |
|:---|:---|:---|
| Unsure | Multi (with space) — always safe | 3/4 |
| Derivational suffix (`-mae`, `-lise`...) | Mono, unless phonotactically blocked — see `derivational-suffixes.md` | 1 |
| Phonotactic block (`ng`,`sh`,`x`... at boundary) | Forced multi | 2 |
| Lexicalised concept + ≤5 syl + no block | Optional mono | 5 |
| Descriptive / ad-hoc combination | Multi | 3/4 |
| Proper noun (place/person name) >5 syl | Exception: mono allowed | 5 exception |
| Non-colour prefix (`pa-`, `pi-`) | Mono (forced), counts toward tone domain | §3 |
| Word order (modifier-before-head) | Last element is head, independent of mono/multi | 6 |
| Multi-word modifier tone | Retains own POS tone, Modular Stitching | §4 |

---

## IV. Interaction with the Colour Prefix System

Multi-word heads (`pos`, `posia`, `param`, `isra`, etc.) carry their own prefix as head nouns; the compound's prefix comes from the head (`ae-bau pos` = "the bakery", `ae-fos posia` = "the land of ice"), not from the modifier. This is standard head-last compounding (§II), distinct from the base-inheritance rule for fused suffixes (see `derivational-suffixes.md` §IV-B).

| Semantic Class | Prefix | Applies to |
|---|---|---|
| Abstract | `o-` | Result (`param`), Doctrine (`isra`), Capability (`afaloi`), Without/Lack (`naras`) |
| Physical boundaries/earth | `ae-` | Location nouns (`pos`, `posia`) |

---

*End of Compounding Specification.*