# Kilor Subordination — Clause Embedding & Relativization

**Module:** Relative Clauses, Complement Clauses, Adverbial Clauses
**Status:** Canonical
**Last updated:** 2026-07-11
**Version:** 2.0.0
**Depends on:** `0-foundation/grammar-syntax.md`, `2-predication/interrogative.md`, `2-predication/negation.md`, `1-nominals/cases.md`, `3-subsystems/aspect.md`

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
| **Object** | `kusni` | ACC (Front suffix; `u` = Back → `-ni`) |
| **Possessor** | `kussi` | GEN (Front suffix; `u` = Back → `-si`) |

The contrastive vowel rule applies: `kus` ends in `u` (Back vowel), so it takes Front suffixes `-ni` (ACC) and `-si` (GEN).

### B. Relative Clauses — Postnominal

Relative clauses follow the head noun. The relativizer `kus` marks the start of the relative clause. Word order inside the relative clause remains SOV.

**Structure:** `HEAD-NOUN kus(-CASE) [ ... clause ... ]`

| Kilor | Gloss | Meaning |
|:---|:---|:---|
| `fora kus dinu fora` | fire REL tree burn | "the fire that burns the tree" |
| `dinu kusni fora fora` | tree REL-ACC fire burn | "the tree that fire burns" |
| `maeha kussi slato fora` | person REL-GEN house burn | "the person whose house burns" |

> **Subject gap:** `kus` unmarked — the head noun (`fora`) is the subject of `fora` (the fire does the burning).
>
> **Object gap:** `kusni` (ACC) — the head noun (`dinu`) is the object of `fora` (the tree is what gets burned).
>
> **Possessor gap:** `kussi` (GEN) — the head noun (`maeha`) owns something inside the relative clause (`slato`).

### C. Stacking (Nested Relative Clauses)

Relative clauses may be nested. Each level uses its own `kus`:

| Kilor | Meaning |
|:---|:---|
| `fora kus dinu kusni ki winar fora wem res` | "The fire that burns the tree that I saw is warm" |

Parse: `fora [kus dinu [kusni ki winar] fora] wem res`
- Outer clause: `fora` modified by `[kus dinu ... fora]` — "fire that burns the tree"
- Inner clause: `dinu` modified by `[kusni ki winar]` — "tree that I saw"

### D. Relativizer vs Complementizer — Disambiguation

`kus` serves two functions. Disambiguation is structural:

| Function | Structure | Example |
|:---|:---|:---|
| **Relative** | Head noun immediately precedes `kus` | `fora kus [dinu fora]` — "fire that burns tree" |
| **Complement** | No head noun; main verb precedes `kus` | `ki asdo kus [fora dinu fora]` — "I know that fire burns tree" |

---

## III. Complement Clauses

### A. Structure

A complement clause is an embedded sentence that functions as the object of a verb (e.g., "know", "want", "think", "see", "fear"). Kilor uses a **head-final** pattern: the main verb comes first, `kus` acts as a bridge, and the embedded clause follows.

**Structure:** `SUBJ MAIN-VERB kus [embedded SOV clause]`

| Kilor | Gloss | Meaning |
|:---|:---|:---|
| `ki asdo kus ti kau.` | I know COMP you come | "I know that you came." |
| `ki thy kus fora dinu fora.` | I think COMP fire tree burn | "I think that fire burns the tree." |
| `si winar kus ki bau taka.` | 3L see COMP I bread eat | "He/she sees that I eat bread." |
| `ki wamy kus mysa.` | I fear COMP darkness-GEN | "I fear the darkness." (noun complement: non-clausal object) |

This head-final pattern preserves the SOV subject-verb adjacency (`ki asdo`) and uses `kus` to bridge from the main verb to the content clause that describes or specifies the verb's complement.

### B. `kus` with Non-Clausal Complements

When the object of a verb like `wamy` (fear) or `thy` (think) is a simple noun rather than a clause, `kus` may still appear:

> `ki wamy kus mysa.` — "I fear the darkness." (the darkness is what I fear)

This is optional — a bare object without `kus` remains the default:

> `ki myna wamy.` — "I fear the darkness." (standard SOV with ACC; `y` = Front → ACC `-na`)

### C. Multi-Verb Complements

For verbs that take a purpose or serial complement (e.g., "go to buy"), see the serial verb construction under §III-D. For purpose clauses using serial verbs, no `kus` is needed.

### D. No Tense in Embedded Clauses

Kilor has no grammatical tense. Time reference in embedded clauses is inferred from context, temporal words, or the main clause's temporal frame. See `3-subsystems/temporals.md`.

Aspect particles (`gin`, `ger`, `gou`; see `3-subsystems/aspect.md`) may appear in complement clauses independently of the main clause's aspect:

> `ki asdo kus ti kau ger.` — "I know that you have arrived."
> `ki winar kus si bau taka gin.` — "I see that he/she is eating bread."

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
| `li ti lir taka, ki lira sounar` | "If you eat fish, I give water" |
| `aiga fora fora, kora wem res` | "Because fire burns, the stone is warm" |
| `hoskar rok my res, ki te slato kau` | "Although the night is dark, I come to the house" |

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

> **Example:** `ki asdo kus ti kau nar.` — "I know that you did NOT come" (negation scopes inside the complement clause)

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


## VII. Reflexives & Reciprocals

### A. Reflexive — `shen` ("self")

`shen` is a reflexive pronoun meaning "self." It follows the personal pronoun to form a reflexive expression:

| Kilor | Meaning |
|:---|:---|
| `ki shen` | myself |
| `ti shen` | yourself |
| `si shen` | himself / herself |
| `kil shen` | ourselves |
| `til shen` | yourselves |
| `sil shen` | themselves |

`shen` is a toneless, 1-syllable open-class root (not closed-class — it receives `-s` derivation).

In usage, the reflexive pronoun occupies the object slot and may take ACC case:

> `ki ki shenna winar.` — "I see myself." (shen + ACC -na; `e` = Front → Back `-na`)

> `ki winar kus ki shen.` — "I see myself." (with kus complementizer: "I see that self")

> `si si shenna argonna.` — "He/she loves himself/herself."

The reflexive may also be used for emphasis ("I myself did it"):

> `ki shen ki bau taka.` — "I myself ate bread." (shen as emphatic, NOM position)

### B. Reciprocal — `meshen` ("each other")

`meshen` means "each other / one another." It is placed **pre-verbally** as an adverb:

> `sil meshen argonna.` — "They love each other."
> `kil meshen winar.` — "We see each other."
> `til meshen sounar.` — "You (pl) give to each other."

`meshen` can take the `-s` suffix for adverbial use (`meshens`), though the bare root form is standard for the reciprocal function.

### C. Interaction with Case

Reflexive `shen` takes standard case suffixes per the Contrastive Suffix Rule (last vowel `e` = Front → Back suffixes `-na` ACC, `-sa` GEN). Reciprocal `meshen` as a pre-verbal adverb does not take case marking.

---

*End of Subordination Specification.*