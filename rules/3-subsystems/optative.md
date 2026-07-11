# Kilor Optative — Wishes, Hopes & Desires

**Module:** Optative, Desiderative & Benedictive Mood
**Status:** Canonical
**Last updated:** 2026-07-11
**Version:** 1.0.0
**Depends on:** `0-foundation/grammar-syntax.md`, `0-foundation/tone-prosody.md`, `3-subsystems/colour-emotion.md`, `3-subsystems/imperatives.md`

---

## I. Core Philosophy

Kilor uses a single content root `halise` ("hope, wish") to express three related irrealis-desire moods: optative (impersonal wish about world-state), desiderative (personal hope about events), and benedictive (blessing directed at another). Colour-emotion particles provide finer emotional control (see `3-subsystems/colour-emotion.md`), and the morphological form of `halise` disambiguates noun-use from verb-use.

`halise` is an **open-class content root** (3 syllables), not a closed-class particle. It follows the standard tone patterns for 3+ syllable words (see `0-foundation/tone-prosody.md` §II-A).

---

## II. Morphological Forms

| Category | Form | Last-3 Pattern | Meaning |
|:---|:---|:---|:---|
| **Noun** | `hajlise` | H(j)→M→L | hope (the feeling) |
| **Verb** | `havlise` | L(v)→H→M | to hope, to wish |
| **Adjective** | `halijse` | M→H(j)→H | hopeful |
| **Adverb** | `halivse` | M→L(v)→M | hopefully |

---

## III. Syntax

### A. Verb Form (`havlise`) — Primary Usage

`havlise` is a verb that takes a complement clause. It occupies the verb slot in the SOV template. Three structural patterns disambiguate the mood:

#### 1. Desiderative — Subject + `havlise` + `kus` + clause

When the speaker is an explicit subject, the reading is desiderative ("I hope that…"):

| Kilor | Meaning |
|:---|:---|
| `ki havlise kus ti kau` | "I hope that you come" |
| `si havlise kus hupli hup nar` | "He hopes that rain does not fall" |

#### 2. Optative — Impersonal `havlise` (no subject)

When `havlise` appears without a subject, the reading is an impersonal wish about the world-state:

| Kilor | Meaning |
|:---|:---|
| `havlise hupli hup` | "May rain fall" / "I wish it would rain" |
| `havlise fora fora nar` | "May the fire not burn" |

In the optative, the wished-for clause follows `havlise` directly without `kus`. This parallels the bare juxtaposition pattern for reported speech (see `2-predication/subordination.md` §VIII).

#### 3. Benedictive — `havlise` + 2nd/3rd person target

When the target of the wish is explicitly stated (2nd or 3rd person), the reading is benedictive:

| Kilor | Meaning |
|:---|:---|
| `havlise ti gor roi ero` | "May you have a good day" |
| `havlise si losto res` | "May he/she be happy" |

### B. Noun Form (`hajlise`) — The Feeling of Hope

When used as a noun, `hajlise` takes a colour prefix like any other noun:

| Kilor | Meaning |
|:---|:---|
| `ki e-hajlise ero` | "I have a warm hope" (SOV: I yellow-hope have) |
| `a-hajlise ralis res` | "A burning hope is great" (Red-hope is big) |

---

## IV. Interaction with Emotional Particles

Emotional particles (see `3-subsystems/colour-emotion.md`) layer additional nuance onto optative expressions. The emotional particle appears at the clause level or pre-verbally, not attached to `havlise` itself:

| Kilor | Meaning |
|:---|:---|
| `e, ki havlise kus ti kau` | "(With joy,) I hope that you come" |
| `i, havlise si kau` | "(With sadness,) may he come" |
| `u, havlise ti gor roi` | "(With calm,) may you have a good day" |

When `havlise` carries a colour-emotion reading, the emotional particle selects the dominant emotional lens. The core semantics of `halise` (irrealis desire) remain — the particle does not replace the meaning but colours the flavour of the wish.

---

## V. Hortative ("Let's") — Cross-Reference

Kilor handles hortative ("let's eat!") through the suggestion particle `sor` (see `3-subsystems/imperatives.md` §III), not through `halise`. `sor` is sentence-final and implies joint action:

> `ki taka sor` — "Let's eat!" (lit. "We eat, I suggest")

---

## VI. Summary Table

| Mood | Construction | Example |
|:---|:---|:---|
| **Desiderative** | Subject + `havlise` + `kus` + clause | `ki havlise kus ti kau` |
| **Optative** | `havlise` + clause (no subject) | `havlise hupli hup` |
| **Benedictive** | `havlise` + 2nd/3rd person + `ero` | `havlise ti gor roi ero` |
| **Hortative** | `sor` (sentence-final) | `ki taka sor` |

---

*End of Optative Specification.*