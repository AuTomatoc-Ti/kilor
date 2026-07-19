# Kilor Subordination — Clause Embedding & Relativization

**Module:** Relative Clauses, Complement Clauses, Adverbial Clauses, Reported Speech, Purpose Clauses, Bare Serialisation
**Status:** Canonical
**Last updated:** 2026-07-19
**Version:** 2.2.2
**Depends on:** `0-foundation/grammar-syntax.md`, `2-predication/interrogative.md`, `2-predication/negation.md`, `1-nominals/cases.md`, `3-subsystems/aspect.md`, `3-subsystems/optative.md`
**Interacts with:** `2-predication/conditionals.md` (li, bam cross-reference), `2-predication/clause-combining.md` (ei vs bare juxtaposition)

---

All subordination particles are closed-class, toneless function words. See `0-foundation/grammar-syntax.md` §IV-C.

## I. The Relativizer `kus`

### A. Form

`kus` is a **declining relative pronoun** — it takes case suffixes to indicate the head noun's role within the relative clause.

| Gap Role | Form | Suffix |
|:---|:---|:---|
| **Subject** | `kus` | unmarked (NOM) |
| **Object** | `kusni` | ACC (`u` = Back → `-ni`) |
| **Possessor** | `kussi` | GEN (`u` = Back → `-si`) |

### B. Relative Clauses — Postnominal

Relative clauses follow the head noun. Word order inside remains SOV.

**Structure:** `HEAD-NOUN kus(-CASE) [ ... clause ... ]`

| Kilor | Gloss | Meaning |
|:---|:---|:---|
| `fora kus lunla fora` | fire REL tree burn | "the fire that burns the tree" |
| `lunla kusni fora fora` | tree REL-ACC fire burn | "the tree that fire burns" |
| `maeha kussi slato fora` | person REL-GEN house burn | "the person whose house burns" |

### C. Stacking (Nested Relative Clauses)

Each level uses its own `kus`:
> `fora kus lunla kusni ki winar fora wem res` — "The fire that burns the tree that I saw is warm"

### D. Relativizer vs Complementizer — Disambiguation

| Function | Structure | Example |
|:---|:---|:---|
| **Relative** | Head noun immediately precedes `kus` | `fora kus [lunla fora]` — "fire that burns tree" |
| **Complement** | No head noun; main verb precedes `kus` | `ki asdo kus [fora lunla fora]` — "I know that fire burns tree" |

---

## II. Complement Clauses

### A. Structure

**Head-final pattern:** `SUBJ MAIN-VERB kus [embedded SOV clause]`

| Kilor | Meaning |
|:---|:---|
| `ki asdo kus ti kau.` | "I know that you came." |
| `ki thy kus fora lunla fora.` | "I think that fire burns the tree." |
| `si winar kus ki bau taka.` | "He/she sees that I eat bread." |

### B. `kus` with Non-Clausal Complements

Optional with simple noun objects:
> `ki wamy kus mysa.` — "I fear the darkness." (optional `kus`)
> `ki myna wamy.` — "I fear the darkness." (standard SOV with ACC)

### C. No Tense in Embedded Clauses

Kilor has no grammatical tense. Time reference is inferred from context or temporal words. Aspect particles (`gin`, `ger`, `gou`) may appear in complement clauses independently of the main clause. See `3-subsystems/aspect.md` and `3-subsystems/temporals.md`.

---

## III. Adverbial Clauses

### A. Structure

`SUBORDINATOR [clause], MAIN-CLAUSE` or `MAIN-CLAUSE, SUBORDINATOR [clause]`

### B. Subordinator Inventory

| Particle | Meaning | Type |
|:---|:---|:---|
| `tu` | when / while | Temporal |
| `li` | if | Conditional (see `conditionals.md`) |
| `aiga` | because | Causal |
| `hoskar` | although | Concessive |
| `fidak` | in order to | Purpose |
| `arfi` | even | Concessive intensifier |

### C. Examples

| Kilor | Meaning |
|:---|:---|
| `tu ti kau, ki losto res` | "When you come, I am happy" |
| `li ti lir taka, ki lira sounar` | "If you eat fish, I give water" |
| `aiga fora fora, kora wem res` | "Because fire burns, the stone is warm" |
| `hoskar rok my res, ki te slato kau` | "Although the night is dark, I come to the house" |

### D. Interaction with Other Systems

- **Question words:** Fronted within the embedded clause, not the matrix clause. See `2-predication/interrogative.md` §III.
- **Negation:** `nar` scopes over the clause it appears in.
- **Case marking:** Same rules as matrix clauses (optional in SOV, mandatory in non-SOV).

---

## IV. Reflexives & Reciprocals

### A. Reflexive — `shen` ("self")

`she` is a toneless, 1-syllable open-class root (not closed-class — it receives `-s` derivation).

| Kilor | Meaning |
|:---|:---|
| `ki shen` | myself |
| `ti shen` | yourself |
| `si shen` | himself / herself |
| `kil shen` | ourselves |
| `til shen` | yourselves |
| `sil shen` | themselves |

The reflexive occupies the object slot and may take ACC case:
> `ki ki shenna winar.` — "I see myself." (`e` = Front → Back `-na`)

Emphatic use ("I myself"):
> `ki shen ki bau taka.` — "I myself ate bread."

### B. Reciprocal — `meshen` ("each other")

Placed **pre-verbally** as an adverb:
> `sil meshen avrgonna.` — "They love each other."
> `kil meshen winar.` — "We see each other."

`meshen` can take `-s` via standard derivation (`meshens`), though the bare root form is standard for the reciprocal function.

### C. Case Interaction

Reflexive `shen` takes standard case suffixes per the Contrastive Suffix Rule (`e` = Front → Back: `-na` ACC, `-sa` GEN). Reciprocal `meshen` as a pre-verbal adverb does not take case marking.

---

## V. Reported Speech

### A. Two Acceptable Strategies

| Strategy | Structure | Example |
|:---|:---|:---|
| **With `kus`** | Verb-of-saying + `kus` + reported clause | `si rilda kus hamin gor res` |
| **Bare juxtaposition** | Verb-of-saying + reported clause | `si rilda hamin gor res` |

### B. Pronoun Resolution

Pronouns retain the speaker's perspective (Chinese model). No pronoun shift:
> `si rilda kus ki hik res` — "He said that I am sad" (ki = current speaker)
> `si rilda kus si hik res` — "He said that he (himself) is sad"

### C. Direct Quote

Bare juxtaposition with no `kus`:
> `si rilda: "ki hik res"` — "He said: 'I am sad'"

Colon and quotation marks are orthographic conventions; in speech, intonation and pause mark the boundary.

---

## VI. Purpose Clauses

### A. Bare Serial Verb — Default

Two verb phrases juxtaposed; the second is interpreted as the purpose:
> `ki kau hamin taka` — "I come (to) eat food"

No subordinator needed. Word order is fixed: purpose clause follows main verb.

### B. Explicit Purpose Particle — `fidak`

`fidak` ("in order to") provides optional explicit marking:
> `ki kau fidak hamin taka` — "I come in order to eat food"

`fidak` may appear clause-initially:
> `fidak hamin taka, ki te selo kau` — "In order to eat food, I go to the road"

---

## VII. `kus` vs. Bare Serialisation — Decision Table

| Context | Strategy | Example |
|:---|:---|:---|
| **Relative clause** | `kus` **required** | `maeha kus hamin taka` — "the person who ate the food" |
| **Complement clause** (cognition) | `kus` **required** | `ki asdo kus ti kau` — "I know that you came" |
| **Reported speech** | `kus` **optional** | `rilda kus X` or `rilda X` |
| **Purpose clause** | **No `kus`** — bare serial (default); `fidak` optional | `kau hamin taka` |
| **Causative** (make/let) | **No `kus`** — bare verb complement | `ki min ti taka` |
| **Sequential actions** | `ei` (coordinator) or bare juxtaposition | `ti bau taka ei thep` |

---

*End of Subordination Specification.*