# Kilor Negation — Affirmation & Negation System

**Module:** Yes/No Answers & Clausal Negation
**Status:** Canonical
**Last updated:** 2026-07-23
**Version:** 1.1.0
**Depends on:** `2-predication/interrogative.md`, `0-foundation/grammar-syntax.md`

---

## I. Core Particles

Kilor uses three dedicated particles for affirmation and negation:

| Particle | Meaning | Function |
|:---|:---|:---|
| `iu` | yes | Affirmative answer to a question |
| `na` | no | Negative answer to a question |
| `nar` | not | Negates the preceding word or phrase |

All three are closed-class, toneless function words. See `0-foundation/grammar-syntax.md` §IV-C.

---

## II. Clausal Negation — `nar`

### A. Position

`nar` is placed **immediately after** the word or phrase it negates. It is a **postpositive negator**.

> **Example (negating a noun):** `ki nar` = "not me"
> **Example (negating a verb):** `taka nar` = "not eat"
> **Example (negating a full clause):** `ki fora taka nar` = "I do not eat fire"

### B. Scope — Uniform Postpositive Rule

`nar` always negates the **immediately preceding constituent**. No exceptions.

| Phrase | `nar` follows | Negates | Meaning |
|:---|:---|:---|:---|
| `ki nar fora taka` | `ki` | the subject | "Not I eat fire" (someone else does) |
| `ki fora nar taka` | `fora` | the object | "I not-the-fire eat" (I eat something else) |
| `ki fora taka nar` | `taka` | the verb | "I fire not-eat" = "I do not eat fire" |

When `nar` follows the verb at clause-end, it negates the verb — which naturally produces predicate-level negation since the verb is the clause head. No special "two-tier" rule is needed.

### C. Scope with Modals

Root modals (`hostak`, `sew`, `som`, `mug`, `shunle`) form a `[Modal] [Verb]` complex (see `0-foundation/grammar-syntax.md` §I-E). The uniform postpositive rule cleanly disambiguates negation of the modal vs. negation of the main verb:

| Phrase | `nar` follows | Negates | Meaning |
|:---|:---|:---|:---|
| `ki hostak nar sounar` | `hostak` | the modal | "I not-must give" = "I don't have to give" |
| `ki hostak sounar nar` | `sounar` | the verb | "I must not-give" = "I must not give" |
| `ki sew nar fei` | `sew` | the modal | "I not-can fly" = "I can't fly" |
| `ki sew fei nar` | `fei` | the verb | "I can not-fly" = "I can refrain from flying" |
| `ki mug nar taka` | `mug` | the modal | "I not-want eat" = "I don't want to eat" |
| `ki mug taka nar` | `taka` | the verb | "I want not-eat" = "I want to not eat" |

The same rule applies to stacked modals:

> `ki mug sew nar fei` — `nar` follows `sew` → "I want to not-be-able-to fly"
> `ki mug sew fei nar` — `nar` follows `fei` → "I want to be able to not-fly"

### D. Interaction with `iu`

The sentence-final question particle `iu` sits **outside the clause proper** and does **not** affect `nar`'s scope determination. When `nar` appears immediately before `iu` at the end of a sentence (e.g., `ti fora taka nar iu?`), `nar` negates the preceding verb (`taka`) as usual — the uniform postpositive rule (§II-B) applies identically. See `2-predication/interrogative.md` §IV-B.

### E. Double Negation

**Double negation (`nar nar`) is forbidden in formal language.** Two consecutive `nar` particles are ungrammatical. To express emphasis, use contextual intensifiers or rephrase the sentence.

---

## III. Yes/No Answers

### A. Affirmative Answer

`iu` is used as a standalone affirmative response:

> **Q:** `ti fora taka iu?` (Do you eat fire?)
> **A:** `iu.` (Yes.)

### B. Negative Answer

`na` is used as a standalone negative response:

> **Q:** `ti fora taka iu?` (Do you eat fire?)
> **A:** `na.` (No.)

---

## IV. Interaction with Interrogatives

`iu` also functions as the **yes/no question marker** when placed at the end of a declarative sentence (see `2-predication/interrogative.md` §IV). In this role, it converts a statement into a polar question.

> **Statement:** `ti fora taka.` (You eat fire.)
> **Question:** `ti fora taka iu?` (Do you eat fire?)

---

*End of Negation Specification.*