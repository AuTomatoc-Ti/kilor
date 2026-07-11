# Kilor — Design Questions

**Status:** All resolved
**Last Updated:** 2026-07-11

All major grammatical design questions have been resolved. Decisions codified in their respective rule files.

---

## Resolved (2026-07-11 — Grammar Completeness Audit)

| # | Question | Resolution | Codified In |
|---|---|---|---|
| 1 | Conditionals (if…then) | `li` = if, `bam` = then/consequential (便/就); two patterns: `li X, bam Y` and `Y li X` | `rules/2-predication/conditionals.md` |
| 2 | Purpose clauses | Bare verb serialisation (Chinese-style) default; `fidak` = optional explicit "in order to" | `rules/2-predication/subordination.md` §IX |
| 3 | Reason/cause clauses | `aiga` — already documented | `rules/2-predication/subordination.md` §IV |
| 4 | Reported speech | `kus` (optional) or bare juxtaposition (optional); pronoun perspective retained | `rules/2-predication/subordination.md` §VIII |
| 5 | Causatives | `min` = let (permissive), `mingo` = make/force (使/令), `tesak` = make/create (造) | `lexicon.csv` |
| 6 | Concessive clauses | `hoskar` = although (existing), `arfi` = even | `rules/2-predication/subordination.md` §IV |
| 7 | Temporal adverbial clauses | Temporal noun + clause: `tilpi ki kau` = before I came; `tu` for "when" | `rules/2-predication/subordination.md` §IV, `rules/3-subsystems/temporals.md` |
| 8 | Optative / desiderative / benedictive | `halise` (3 syllables, full tone paradigm) for all three; `sor` covers hortative "let's"; emotional particles add nuance | `rules/3-subsystems/optative.md` |
| 9 | Noun → adverb derivation | `-s` applies: e.g., `roks` = at night (nightly) | `rules/0-foundation/grammar-syntax.md` §V |
| 10 | `kus` vs. bare serialisation | Decision table codified; `kus` required for relatives & cognition complements, optional for reported speech, prohibited for purpose & causatives | `rules/2-predication/subordination.md` §X |
| 11 | Schwa epenthesis | Formalised for loanword adaptation; `e` inserted between consonant clusters | `rules/0-foundation/phonology.md` §IV-F |
| 12 | Polite/formal register | Intentional omission — colour-emotion system + `chom` sufficient | N/A (design decision) |
| 13 | Missing closed-class particles in CSV | Added all missing particles: `mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `bam`, `aiga`, `hoskar`, `arfi`, `fidak`, `kus` | `lexicon.csv` |

---

## Older Resolved

| # | Question | Resolution | Codified In |
|---|---|---|---|
| 14 | Subordinate clauses & relativization | Postnominal `kus` relativizer + adverbial particles | `rules/2-predication/subordination.md` |
| 15 | Dative & instrumental particles | `su` split into `mer` (comitative) and `sy` (instrumental) | `rules/1-nominals/cases.md` §V |
| 16 | Temporal word inventory | Day scale compounds with `roi`, frequency `-saka` paradigm, bare temporal roots | `rules/0-foundation/grammar-syntax.md` §VI |
| 17 | Comparatives & superlatives | Analytic particle system: `tor`, `les`, `torra`, `wetor`, `mangus` | `rules/3-subsystems/comparatives.md` |
| 18 | `ae` prefix ambiguity | Mandatory hyphen rule — hyphen never omitted between prefix and root | `rules/1-nominals/nouns-colour-prefix.md` §II-A |
| 19 | Passive voice | `sy` extended as unified passive + instrumental particle (Chinese 被 model) | `rules/1-nominals/cases.md` §V-E, `rules/0-foundation/grammar-syntax.md` §I-D |

---

## Deferred

| # | Question | Status | Notes |
|---|---|---|---|
| 20 | Topic marking | Deferred | No topic marker for now. Revisit if needed during sentence-building. |

---

*All blocking design questions resolved. Lexicon expansion can begin.*