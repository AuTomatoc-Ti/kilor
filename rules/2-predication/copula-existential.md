# Kilor Copula, Existential & Possession

**Module:** Predication, Existence & Having
**Status:** Canonical
**Last updated:** 2026-07-23
**Version:** 1.4.0
**Depends on:** `2-predication/negation.md`, `2-predication/interrogative.md`, `0-foundation/grammar-syntax.md`

---

Kilor has two relational verbs:

| Verb | Function | Chinese Parallel |
|---|---|---|
| **`res`** | Copula — identity, attribution (X **is** Y) | 是 |
| **`ero`** | Existential & Possession (**there is**, **have**) | 有 |

`res` and `ero` are closed-class, toneless function words. See `0-foundation/grammar-syntax.md` §IV-C.

`ero` unifies existence and possession — "fire exists" and "I have fire" are the same grammatical operation. Possession is existence brought into one's sphere.

---

## I. Word Order

Both verbs follow standard **SOV** word order:

```
Subject — Complement — Verb
```

### A. Predicate Adjective

> `a-fora wem res.` — "The fire is warm."
> `fora wem res.` — "Fire is warm." (generic)

### B. Predicate Nominal

> `ki maeha res.` — "I am a person."
> `si a-fora res.` — "It is the fire."

### C. Existential

> `fora ero.` — "There is fire." / "Fire exists."
> `maeha ero.` — "There is a person."

### D. Existential + Location

When `ero` combines with a spatial postposition (see `3-subsystems/spatials.md`), the spatial PP occupies its standard slot between the subject and the verb per the clause template (`0-foundation/grammar-syntax.md` §I-E). No new particles or special word order is required.

**Structure:** `SUBJ [spatial-ne] ero`

| Kilor | Meaning |
|:---|:---|
| `e-buk slato-si rapne ero.` | "There is a book on the table." |
| `lira pei-si ikne ero.` | "There is water in the cup." |
| `maeha slato-si haune ero.` | "There is a person behind the house." |
| `fora slato-si paune ero.` | "There is fire in front of the house." |

Negation follows the standard pattern (§II-B):
> `e-buk slato-si rapne ero nar.` — "There is no book on the table."
> `lira pei-si ikne ero nar.` — "There is no water in the cup."

Interrogatives follow standard wh-fronting (§III-B):
> `slato-si rapne ewei ero?` — "What is on the table?"
> `slato-si ikne ewei ero iu?` — "Is there anything in the house?"

Possession (subject has entity) and existential-location (entity is at a location) use the same `ero` verb. The presence of a spatial PP with no possessor subject defaults to the existential-location reading.

#### E. Possession

> `ki fora ero.` — "I have fire."
> `si lira ero.` — "He/she has water."

---

## II. Negation

### A. Copula Negation

`nar` follows the copula:
> `fora wem res nar.` — "Fire is not warm."
> `ki maeha res nar.` — "I am not a person."

### B. Existential Negation

> `fora ero nar.` — "There is no fire."

### C. Possession Negation

> `ki fora ero nar.` — "I do not have fire."

### D. Constituent Negation

`nar` placed before the verb negates only the preceding constituent (see `2-predication/negation.md` §II-B):

> `ki nar fora ero.` — "Not I have fire." (someone else does)
> `ki fora nar ero.` — "I not-fire have." (I have something else)

---

## III. Interrogatives

### A. Yes/No Questions

Sentence-final `iu` (see `2-predication/interrogative.md` §IV):

> `fora wem res iu?` — "Is fire warm?"
> `fora ero iu?` — "Is there fire?"
> `ki fora ero iu?` — "Do I have fire?"

### B. Wh-Questions

Question words fronted as usual:

> `ewei wem res iu?` — "What is warm?"
> `iwei fora ero?` — "Where is there fire?"
> `aewei fora ero?` — "Who has fire?"

---

## IV. Case Marking

### A. Copula — Both Arguments Nominative

Neither argument is an object. Both subject and complement are unmarked (NOM):
> ✅ `ki maeha res.`
> ❌ `ki maehani res.` (ACC invalid with copula)

### B. Existential & Possession — Standard Case Rules

> `ki forani ero.` — Accusative optional in SOV speech, mandatory in formal/non-SOV.

---

## V. Zero-Copula in Ambient & Weather Statements

The copula **may** be omitted for ambient conditions (weather, temperature, light level):

> `wem.` = `wem res.` — "It's warm."
> `my.` = `my res.` — "It's dark."

This is the **only** context where zero-copula is permitted. Predicate nominals and possession always require their verbs.

---

## VI. Summary Table

| Pattern | Structure | Example | Meaning |
|---|---|---|---|
| Predicate Adjective | SUBJ ADJ `res` | `fora wem res` | Fire is warm |
| Predicate Nominal | SUBJ NOUN `res` | `ki maeha res` | I am a person |
| Existential | NOUN `ero` | `fora ero` | There is fire |
| Existential + Location | SUBJ SPATIAL `ero` | `e-buk slato-si rapne ero` | There is a book on the table |
| Possession | PSR PSD `ero` | `ki fora ero` | I have fire |
| Negated copula | SUBJ COMP `res nar` | `fora wem res nar` | Fire is not warm |
| Negated existential | NOUN `ero nar` | `fora ero nar` | There is no fire |
| Negated possession | PSR PSD `ero nar` | `ki fora ero nar` | I don't have fire |
| Y/N copula | SUBJ COMP `res iu` | `fora wem res iu` | Is fire warm? |
| Y/N existential | NOUN `ero iu` | `fora ero iu` | Is there fire? |
| Zero-copula (ambient) | ADJ | `wem` | It's warm |

---

*End of Copula, Existential & Possession Specification.*