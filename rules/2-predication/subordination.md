# Kilor Subordination — Clause Embedding & Relativization

**Module:** Relative Clauses, Complement Clauses, Adverbial Clauses
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.0.0
**Depends on:**
**Created:** 2026-07-07

---

## I. Core Philosophy

Kilor uses a minimal set of closed-class particles to embed clauses within clauses. The relativizer `kus` serves double duty — introducing both relative clauses ("the fire that burns") and complement clauses ("I know that you came") — mirroring English "that". Adverbial clauses (when, because, if) use dedicated subordinator particles.

All subordination particles are **toneless, closed-class, 1–2 syllable function words** exempt from the `-s` constraint (see `0-foundation/grammar-syntax.md` §IV-C).

---

## II. The Relativizer `kus`

### A. Form

`kus` is a **declining relative pronoun** — it takes the same case suffixes as any noun to indicate the grammatical role of the head noun within the relative clause.

| Gap Role | Form | Suffix |
|:---|:---|:---|
| **Subject** | `kus` | unmarked (NOM) |
| **Object** | `kus-ni` | ACC (Front suffix; `u` = Back → `-ni`) |
| **Possessor** | `kus-si` | GEN (Front suffix; `u` = Back → `-si`) |

The contrastive vowel rule applies: `kus` ends in `u` (Back vowel), so it takes Front suffixes `-ni` (ACC) and `-si` (GEN).

### B. Relative Clauses — Postnominal

Relative clauses follow the head noun. The relativizer `kus` marks the start of the relative clause. Word order inside the relative clause remains SOV.

**Structure:** `HEAD-NOUN kus(-CASE) [ ... clause ... ]`

| Kilor | Gloss | Meaning |
|:---|:---|:---|
| `fojra kus dinu fovra` | fire REL tree burn | "the fire that burns the tree" |
| `dinu kus-ni fojra fovra` | tree REL-ACC fire burn | "the tree that fire burns" |
| `maeha kus-si slato fovra` | person REL-GEN house burn | "the person whose house burns" |

> **Subject gap:** `kus` unmarked — the head noun (`fojra`) is the subject of `fovra` (the fire does the burning).
>
> **Object gap:** `kus-ni` (ACC) — the head noun (`dinu`) is the object of `fovra` (the tree is what gets burned).
>
> **Possessor gap:** `kus-si` (GEN) — the head noun (`maeha`) owns something inside the relative clause (`slato`).

### C. Stacking (Nested Relative Clauses)

Relative clauses may be nested. Each level uses its own `kus`:

| Kilor | Meaning |
|:---|:---|
| `fojra kus dinu kus-ni ki wivnar fovra wem res` | "The fire that burns the tree that I saw is hot" |

Parse: `fojra [kus dinu [kus-ni ki wivnar] fovra] wem res`
- Outer clause: `fojra` modified by `[kus dinu ... fovra]` — "fire that burns the tree"
- Inner clause: `dinu` modified by `[kus-ni ki wivnar]` — "tree that I saw"

### D. Relativizer vs Complementizer — Disambiguation

`kus` serves two functions. Disambiguation is structural:

| Function | Structure | Example |
|:---|:---|:---|
| **Relative** | Head noun immediately precedes `kus` | `fojra kus [dinu fovra]` — "fire that burns tree" |
| **Complement** | No head noun; `kus` starts a clause in object position | `ki kus [fojra dinu fovra] asdo` — "I know that fire burns tree" |

---

## III. Complement Clauses

### A. Structure

A complement clause is an embedded sentence that functions as the object of a verb (e.g., "know", "want", "think", "see"). `kus` introduces the clause, which sits in the object slot before the main verb. The entire clause may take ACC case marking.

**Structure:** `SUBJ kus [embedded clause](-ACC) MAIN-VERB`

| Kilor | Gloss | Meaning |
|:---|:---|:---|
| `ki kus ti kau asdo` | I REL you come know | "I know that you come/came" |
| `ki kus lir tavka-ni rima` | I REL fish eat-ACC want | "I want to eat fish" |
| `si kus fojra dinu fovra wivnar` | 3L REL fire tree burn see | "He/she sees that fire burns the tree" |

### B. ACC Case on Complement Clauses

The ACC suffix `-ni`/`-na` may optionally attach to the last word of the complement clause to mark it as the object. This follows the same rule as multi-word vocabs (`1-nominals/cases.md` §III-C).

In SOV order with unambiguous position, ACC marking is optional (same optionality as regular objects). In formal writing or non-SOV order, it is mandatory.

> **Example (formal):** `ki kus lir tavka-ni asdo` — "I know that fish eats" (ACC marks the clause as object)

### C. No Tense in Embedded Clauses

Kilor has no grammatical tense. Time reference in embedded clauses is inferred from context, temporal words, or the main clause's temporal frame. See `3-subsystems/temporals.md`.

---

## IV. Adverbial Clauses

### A. Structure

Adverbial clauses modify the main action — specifying when, why, under what condition, or despite what. A subordinator particle introduces the clause. The clause may appear before or after the main clause.

**Structure:** `SUBORDINATOR [clause], MAIN-CLAUSE` or `MAIN-CLAUSE, SUBORDINATOR [clause]`

### B. Subordinator Inventory

| Particle | Meaning | Type |
|:---|:---|:---|
| `tu` | when / while | Temporal |
| `li` | if | Conditional |
| `aiga` | because | Causal |
| `hoskar` | although | Concessive |

### C. Examples

| Kilor | Meaning |
|:---|:---|
| `tu ti kau, ki losto res` | "When you come, I am happy" |
| `li ti lir tavka, ki lira sounar` | "If you eat fish, I give water" |
| `aiga fojra fovra, kora wem res` | "Because fire burns, the stone is hot" |
| `hoskar roch my res, ki slato te kau` | "Although the night is dark, I come to the house" |

### D. Position Flexibility

Adverbial clauses may precede or follow the main clause. Clause-initial position establishes the frame first (preferred for clarity in formal prose). Clause-final position is common in casual speech.

| Position | Example |
|:---|:---|
| **Clause-first** | `tu ti kau, ki losto res` — "When you come, I am happy" |
| **Clause-last** | `ki losto res, tu ti kau` — "I am happy, when you come" |

---

## V. Interaction with Other Systems

### A. Question Word Fronting

When a relative or complement clause contains a question word, that question word is fronted to the start of the **embedded clause**, not the matrix clause. See `2-predication/interrogative.md` §III.

### B. Negation

Negation particles (`nar`, `na`) scope over the clause they appear in. See `2-predication/negation.md`.

> **Example:** `ki kus nar ti kau asdo` — "I know that you did NOT come" (negation scopes inside the complement clause)

### C. Case Marking in Embedded Clauses

Case suffixes inside embedded clauses follow the same rules as matrix clauses: optional in SOV order, mandatory in formal writing and non-SOV order.

---

## VI. Summary Table

| Particle | Function | Section |
|:---|:---|:---|
| `kus` | Relativizer ("that/which/who") | §II |
| `kus` | Complementizer ("that" — I know that...) | §III |
| `tu` | Temporal subordinator ("when/while") | §IV |
| `li` | Conditional subordinator ("if") | §IV |
| `aiga` | Causal subordinator ("because") | §IV |
| `hoskar` | Concessive subordinator ("although") | §IV |

---

*End of Subordination Specification.*