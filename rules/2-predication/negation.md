# Kilor Negation — Affirmation & Negation System

**Module:** Yes/No Answers & Clausal Negation
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.0.0
**Depends on:**

---

## I. Core Particles

Kilor uses three dedicated particles for affirmation and negation:

| Particle | Meaning | Function |
|:---|:---|:---|
| `iu` | yes | Affirmative answer to a question |
| `na` | no | Negative answer to a question |
| `nar` | not | Negates the preceding word or phrase |

All three are **1-syllable words** and follow the standard 1-syllable tone rule: **toneless** (flat mid-tone). See `0-foundation/tone-prosody.md` §II-C.

---

## II. Clausal Negation — `nar`

### A. Position

`nar` is placed **immediately after** the word or phrase it negates. It is a **postpositive negator**.

> **Example (negating a noun):** `ki nar` = "not me"
> **Example (negating a verb):** `tavka nar` = "not eat"
> **Example (negating a full clause):** `ki fojra tavka nar` = "I do not eat fire"

### B. Scope

`nar` has a **two-tier scope rule** depending on position:

#### Clause-End Position — Predicate Scope

When `nar` appears at the **end of a clause** (after the verb), it scopes over the **entire predicate** — the whole clause is negated.

> `ki fojra tavka nar` = "I do not eat fire" (entire predicate negated)

#### Non-Final Position — Constituent Scope

In any other position, `nar` negates only the **immediately preceding constituent**:

| Phrase | Meaning |
|:---|:---|
| `ki nar fojra tavka` | "Not I eat fire" (someone else does) |
| `ki fojra nar tavka` | "I not-the-fire eat" (I eat something else) |

### C. Interaction with `iu`

The sentence-final question particle `iu` sits **outside the clause proper** and does **not** affect `nar`'s scope determination. When `nar` appears immediately before `iu` at the end of a sentence (e.g., `ti fojra tavka nar iu?`), `nar` is treated as clause-final — scoping over the entire predicate, not just the preceding verb. See `2-predication/interrogative.md` §IV-B.

### D. Double Negation

**Double negation (`nar nar`) is forbidden in formal language.** Two consecutive `nar` particles are ungrammatical. To express emphasis, use contextual intensifiers or rephrase the sentence.

---

## III. Yes/No Answers

### A. Affirmative Answer

`iu` is used as a standalone affirmative response:

> **Q:** `ti fojra tavka iu?` (Do you eat fire?)
> **A:** `iu.` (Yes.)

### B. Negative Answer

`na` is used as a standalone negative response:

> **Q:** `ti fojra tavka iu?` (Do you eat fire?)
> **A:** `na.` (No.)

---

## IV. Interaction with Interrogatives

`iu` also functions as the **yes/no question marker** when placed at the end of a declarative sentence (see `2-predication/interrogative.md` §IV). In this role, it converts a statement into a polar question.

> **Statement:** `ti fojra tavka.` (You eat fire.)
> **Question:** `ti fojra tavka iu?` (Do you eat fire?)

---

*End of Negation Specification.*