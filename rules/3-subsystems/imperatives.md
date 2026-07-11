# Kilor Imperatives — Commands, Suggestions, Prohibitions & Vocatives

**Module:** Imperative Mood, Suggestion, Prohibition, Vocative
**Status:** Canonical
**Last updated:** 2026-07-11
**Version:** 1.0.0
**Depends on:** `0-foundation/grammar-syntax.md`, `2-predication/negation.md`, `3-subsystems/colour-emotion.md`

---

## I. Core Philosophy

Kilor expresses commands and related speech acts through a **bare-verb base** plus optional **register particles**. There is no morphological imperative — no conjugation, no tone change. The 4-level register system covers the full pragmatic spectrum from casual command to polite request to authoritative prohibition.

All imperative particles are **toneless, 1-syllable closed-class function words** exempt from the `-s` constraint (see `0-foundation/grammar-syntax.md` §IV-C).

---

## II. Imperative Register System

| Register | Particle | Position | Example | Tone |
|---|---|---|---|---|
| **Casual command** | (bare verb) | — | `Taka!` | Neutral |
| **Casual negative** | `nar` | Post-verbal | `Taka nar!` | Neutral |
| **Suggestion** | `sor` | Sentence-final | `Taka sor.` | Soft, inviting (like Cantonese 啦) |
| **Negative suggestion** | `nar sor` | Post-verbal + sentence-final | `Taka nar sor.` | Soft dissuasion |
| **Polite request** | `chom` | Pre-verbal | `Chom taka.` | Respectful (like Cantonese 請) |
| **Strong prohibition** | `maug` | Pre-verbal | `Maug taka!` | Authoritative (like Cantonese 咪) |

---

## III. Register Details

### A. Casual Command — Bare Verb

The unmarked imperative uses the **bare verb** with no particle:

> `Kau!` — "Come!"
> `Taka!` — "Eat!"
> `Sopa!` — "Look!"

The subject (second person) is implied and omitted.

### B. Negative Command — Verb + `nar`

Following Kilor's standard postpositive negation rule (see `2-predication/negation.md` §II-A), `nar` follows the verb:

> `Taka nar!` — "Don't eat!"
> `Kau nar!` — "Don't come!"

This is consistent with the general negation pattern — `nar` always follows what it negates. No special exception is needed for imperatives.

### C. Suggestion — `sor` (Sentence-Final)

`sor` softens a command into an invitation or suggestion. It is placed **sentence-finally**, after the verb (and after `nar` if negative):

> `Taka sor.` — "Let's eat." / "Why not eat?"
> `Kau sor.` — "Come, won't you?"
> `Taka nar sor.` — "(I suggest) don't eat." / "Maybe don't eat."

`sor` is comparable to Cantonese 啦 (laa1) or Mandarin 吧 (ba) — it signals that the speaker is making a suggestion rather than giving an order.

### D. Polite Request — `chom` (Pre-Verbal)

`chom` elevates the register to a **polite request**. It is placed **before the verb**:

> `Chom taka.` — "Please eat."
> `Chom minau.` — "Please stand/stay."
> `Chom kau.` — "Please come."

`chom` is comparable to Cantonese 請 (cing2) or English "please."

### E. Strong Prohibition — `maug` (Pre-Verbal)

`maug` is a **dedicated prohibitive particle** distinct from general negation `nar`. It conveys strong, authoritative prohibition. It is placed **before the verb**:

> `Maug taka!` — "Do not eat!" (strong)
> `Maug kau!` — "Do not come!" (strong)

`maug` differs from `nar`:
- `Taka nar!` = neutral "don't eat" (informational negation)
- `Maug taka!` = "don't you eat!" (prohibition with speaker authority)

`maug` is comparable to Cantonese 咪 (mai5) — a specialized prohibitive distinct from general negation.

---

## IV. Imperative with Emotional Particles

Emotional particles (see `3-subsystems/colour-emotion.md`) may co-occur with imperatives. The emotional particle precedes the verb in the clause-initial `[Emo]` slot:

> `i Taka nar!` — "Don't eat!" (said with sadness)
> `o Chom kau.` — "Please come." (said with reverence)

---

## V. Vocative — `hei` ("hello / hey")

### A. Basic Usage

`hei` serves as a **vocative interjection** for calling attention, greeting, or hailing someone:

> `Hei!` — "Hello!" / "Hey!"
> `Hei, song!` — "Hey, friend!"

### B. Colour Prefix on Vocative

A colour prefix may optionally be attached to `hei` to convey the speaker's emotional stance toward the person addressed. This follows the 異體字 principle (see `1-nominals/nouns-colour-prefix.md` §VI):

| Form | Colour | Emotional Nuance |
|---|---|---|
| `a-hei` | Red (passion/anger) | Calling with passion or intensity |
| `e-hei` | Orange (longing) | Calling with yearning |
| `i-hei` | Blue (sadness) | Calling with melancholy |
| `o-hei` | Yellow (reverence) | Calling with respect, formal greeting |
| `u-hei` | Green (joy) | Calling with warmth, cheerful greeting |
| `y-hei` | White (wonder) | Calling with curiosity or surprise |
| `ae-hei` | Brown (earthly/dismissive) | Calling down on someone, looking down |

> `ae-hei, ti!` — "Hey, you!" (dismissive, condescending — literally "brown-hello, you")

### C. Vocative Position

Vocatives may appear:
- **Clause-initially:** `Hei, song! ki kau.` — "Hey friend, I'm coming."
- **Standalone:** `Hei!` — "Hello!"

When combined with a colour prefix, the vocative does not affect the colour prefix system of the rest of the clause.

---

## VI. Interaction with Other Systems

### A. Interrogatives

`iu` does not combine with imperatives. To form a polite request-as-question, use a standard yes/no question with `chom`:

> `ti chom kau iu?` — "Will you please come?"

### B. Aspect Particles

Aspect particles (`gin`, `ger`, `gou`) may appear in imperatives (see `3-subsystems/aspect.md`):

> `Taka ger!` — "Eat (have eaten)!" (urging completion)

---

## VII. Summary Table

| Particle | Meaning | Position | Register Level |
|---|---|---|---|
| (bare verb) | command | — | Casual |
| `nar` | negative command | Post-verbal | Casual |
| `sor` | suggestion | Sentence-final | Soft |
| `chom` | polite request | Pre-verbal | Polite |
| `maug` | strong prohibition | Pre-verbal | Authoritative |
| `hei` | hello / hey (vocative) | Clause-initial / standalone | Neutral (colour prefix for nuance) |

---

*End of Imperatives Specification.*