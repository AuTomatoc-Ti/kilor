# Kilor Derivational Compounding

**Module:** Derivation via Light-Noun Compounding
**Status:** Canonical
**Last updated:** 2026-07-12
**Version:** 1.1.0
**Depends on:** `0-foundation/grammar-syntax.md` (compounding §IV, clause template §I-E), `0-foundation/tone-prosody.md`, `1-nominals/nouns-colour-prefix.md`

---

Kilor derives agent, instrument, property, measure, process, result, location, and doctrine nouns through **multi-word compounding** with light noun heads. No dedicated derivational suffixes — the existing compounding infrastructure (§IV of grammar-syntax.md) handles all derivations.

Each head is a full root in `lexicon.csv` that also appears in a shortened combining form in compounds.

---

## I. Head Inventory

| # | Domain | Full Root | Comb. Form | Category | Section | Meaning |
|---|---|---|---|---|---|---|
| 1 | Agent | `maeha` | `mae` | n | B | person / human |
| 2 | Instrument | `tek` | `tek` | n | C | tool |
| 3 | Property | `pireilu` | `lu` | n | I | property / quality |
| 4 | Measure | `rinok` | `rin` | n | I | measure / measurement |
| 5 | Process | `chap` | `par` | n | I | act / deed |
| 6 | Result | `param` | `param` | n | I | result |
| 7 | Location | `poska` | `pos` | n | G | place / location |
| 8 | Doctrine | `lokisra` | `isra` | n | I | doctrine / system of thought |
| 9 | Capability | `afaloi` | `afaloi` | nv | H | ability / able to |
| 10 | Without/Lack | `narau` | `nara` | n | I | without / lack |

All heads are open-class content roots — they carry colour prefixes and accept `-s` derivation per standard rules.

---

## II. Compounding Patterns

### A. Agent — `verb + mae(ha)`

| Form | Meaning |
|---|---|
| `taka mae` | eater (one who eats) |
| `taka maeha` | eater (formal, with full root) |
| `tesak mae` | creator / maker |
| `fei mae` | flyer |

Agent compounds use the verb's bare root (no `-s`). The agent noun may take a colour prefix: `a-taka mae` = "the eater" (living agent).

### B. Instrument — `verb + tek`

| Form | Meaning |
|---|---|
| `kup tek` | cutter (cutting tool) |
| `tesak tek` | creation tool |

### C. Property — `adjective-root + lu`

| Form | Meaning |
|---|---|
| `ema lu` | truth (true-ness) |
| `gor lu` | goodness |
| `my lu` | darkness |
| `wem lu` | warmth |

The adjective root appears bare (no `-s`), since the compound head `lu` signals the nominalisation. Existing entries formed with this pattern (e.g., `emlu`) are lexicalised mono-word compounds and coexist with the productive multi-word form.

### D. Measure — `adjective-root + rin`

| Form | Meaning |
|---|---|
| `shuk rin` | speed (fast-degree) |
| `rali rin` | size (big-degree) |
| `kop rin` | coldness (cold-degree, measurable) |

`rin` nominalises a scalar quality as a measurable degree. Contrasts with `lu`, which nominalises an inherent property.

### E. Process — `verb + par`

| Form | Meaning |
|---|---|
| `tesak par` | creation (act of creating) |
| `thy par` | thought (act of thinking) |

### F. Result — `verb + param`

| Form | Meaning |
|---|---|
| `tesak param` | creation (thing created) |

### G. Location — `noun + pos`

| Form | Meaning |
|---|---|
| `wem pos` | warm-place (greenhouse) |
| `bau pos` | bread-place (bakery) |
| `hamin pos` | food-place (kitchen/dining hall) |

### H. Doctrine — `noun + isra`

| Form | Meaning |
|---|---|
| `ero isra` | existentialism (existence-doctrine) |
| `eli isra` | vitalism (life-doctrine) |

### I. Capability — `afaloi + verb`

| Form | Meaning |
|---|---|
| `afaloi taka` | edible (able-to-eat) |
| `afaloi taki` | drinkable |
| `afaloi tesak` | creatable / makeable |

`afaloi` precedes the verb (modifier position). This pattern is distinct from the periphrastic `sew + verb` ("can X" as a verb phrase) — `afaloi taka` is a nominal/adjectival compound ("edible"), while `sew taka` is a predicate ("can eat").

### J. Without/Lack — `narau + noun` / `noun + nara`

| Form | Meaning |
|---|---|
| `narau lira` | without water (prepositional) |
| `lira nara` | waterless (derivational) |

Two syntactic patterns with the same root:
- **Preposed `narau`:** prepositional usage — `narau lira` = "without water"
- **Postposed `nara`:** derivational compounding — `lira nara` = "waterless"

The combining form `nara` follows the standard head-last compounding pattern.

---

## III. Syntax & Wordhood

### A. Multi-Word Compounds

All derivational compounds are **multi-word vocabs** (two orthographic words with a space). Each word is processed independently per Modular Stitching (`0-foundation/tone-prosody.md` §IV-D).

- 1–2 syllable heads: toneless (flat mid)
- 3+ syllable heads: follow their own Last-3 Domain

Colour prefixes attach to the **head noun**, not the modifier: `a-taka mae` (the eater), `e-kup tek` (the cutting tool).

### B. Case Suffix Distribution

When a derivational compound receives a case suffix, the suffix attaches **only to the head (last word)** per `0-foundation/grammar-syntax.md` §IV-B:

> `kup tekni` — cutter (ACC)
> `taka maesi` — eater's (GEN)

---

## IV. Combining Form vs. Full Root

The combining form and full root are interchangeable. The combining form is preferred in everyday speech; the full root is used in formal registers or for disambiguation.

| Everyday | Formal | Meaning |
|---|---|---|
| `taka mae` | `taka maeha` | eater |
| `wem pos` | `wem poska` | warm-place |

---

## V. Interaction with the Colour Prefix System

Derivational compounds inherit the colour prefix of their **semantic class**, not their modifier:

- Agent nouns: `a-` (living beings)
- Instrument nouns: `e-` (crafted tools)
- Property/Measure/Process/Result nouns: `o-` (abstract)
- Location nouns: `ae-` (physical boundaries/earth)
- Doctrine nouns: `o-` (abstract system)
- Capability compounds: `o-` (abstract)
- Without/Lack compounds: `o-` (abstract)

---

## VI. No Productive -hood/-ship Derivation

Kilor does not have a dedicated compounding head for relational states (English -hood, -ship). Concepts like "childhood," "friendship," and "freedom" are coined ad-hoc using existing compounds (e.g., `pag maeha tlow` = child-time, `song losga` = friend-bond) or dedicated roots.

---

*End of Derivational Compounding Specification.*