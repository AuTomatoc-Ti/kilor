# Kilor Copula, Existential & Possession

**Module:** Predication, Existence & Having
**Status:** Canonical
**Last updated:** 2026-08-19
**Version:** 1.5.0
**Depends on:** `2-predication/negation.md`, `2-predication/interrogative.md`, `0-foundation/grammar-syntax.md`

---

Kilor has two relational verbs:

| Verb | Function | Chinese Parallel |
|---|---|---|
| **`res`** | Copula — identity, attribution (X **is** Y) | 是 |
| **`os`** | Existential & Possession (**there is**, **have**) | 有 |

`res` and `os` are closed-class, toneless function words. See `0-foundation/grammar-syntax.md` §IV-C.

`os` unifies existence and possession — "fire exists" and "I have fire" are the same grammatical operation. Possession is existence brought into one's sphere.

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

> `fora os.` — "There is fire." / "Fire exists."
> `maeha os.` — "There is a person."

### D. Existential + Location

When `os` combines with a spatial postposition (see `3-subsystems/spatials.md`), the spatial PP occupies its standard slot between the subject and the verb per the clause template (`0-foundation/grammar-syntax.md` §I-E). No new particles or special word order is required.

**Structure:** `SUBJ [spatial-ne] os`

| Kilor | Meaning |
|:---|:---|
| `e-buk slato-si rapne os.` | "There is a book on the table." |
| `lira pei-si ikne os.` | "There is water in the cup." |
| `maeha slato-si haune os.` | "There is a person behind the house." |
| `fora slato-si paune os.` | "There is fire in front of the house." |

Negation follows the standard pattern (§II-B):
> `e-buk slato-si rapne os nar.` — "There is no book on the table."
> `lira pei-si ikne os nar.` — "There is no water in the cup."

Interrogatives follow standard wh-fronting (§III-B):
> `slato-si rapne ewei os?` — "What is on the table?"
> `slato-si ikne ewei os iu?` — "Is there anything in the house?"

Possession (subject has entity) and existential-location (entity is at a location) use the same `os` verb. The presence of a spatial PP with no possessor subject defaults to the existential-location reading.

#### E. Possession

> `ki fora os.` — "I have fire."
> `si lira os.` — "He/she has water."

---

## II. Negation

### A. Copula Negation

`nar` follows the copula:
> `fora wem res nar.` — "Fire is not warm."
> `ki maeha res nar.` — "I am not a person."

### B. Existential Negation

> `fora os nar.` — "There is no fire."

### C. Possession Negation

> `ki fora os nar.` — "I do not have fire."

### D. Constituent Negation

`nar` placed before the verb negates only the preceding constituent (see `2-predication/negation.md` §II-B):

> `ki nar fora os.` — "Not I have fire." (someone else does)
> `ki fora nar os.` — "I not-fire have." (I have something else)

---

## III. Interrogatives

### A. Yes/No Questions

Sentence-final `iu` (see `2-predication/interrogative.md` §IV):

> `fora wem res iu?` — "Is fire warm?"
> `fora os iu?` — "Is there fire?"
> `ki fora os iu?` — "Do I have fire?"

### B. Wh-Questions

Question words fronted as usual:

> `ewei wem res iu?` — "What is warm?"
> `iwei fora os?` — "Where is there fire?"
> `aewei fora os?` — "Who has fire?"

---

## IV. Case Marking

### A. Copula — Both Arguments Nominative

Neither argument is an object. Both subject and complement are unmarked (NOM):
> ✅ `ki maeha res.`
> ❌ `ki maehani res.` (ACC invalid with copula)

### B. Existential & Possession — Standard Case Rules

> `ki forani os.` — Accusative optional in SOV speech, mandatory in formal/non-SOV.

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
| Existential | NOUN `os` | `fora os` | There is fire |
| Existential + Location | SUBJ SPATIAL `os` | `e-buk slato-si rapne os` | There is a book on the table |
| Possession | PSR PSD `os` | `ki fora os` | I have fire |
| Negated copula | SUBJ COMP `res nar` | `fora wem res nar` | Fire is not warm |
| Negated existential | NOUN `os nar` | `fora os nar` | There is no fire |
| Negated possession | PSR PSD `os nar` | `ki fora os nar` | I don't have fire |
| Y/N copula | SUBJ COMP `res iu` | `fora wem res iu` | Is fire warm? |
| Y/N existential | NOUN `os iu` | `fora os iu` | Is there fire? |
| Zero-copula (ambient) | ADJ | `wem` | It's warm |

---

*End of Copula, Existential & Possession Specification.*