# Kilor Temporal Expression

**Module:** Temporal Expression
**Status:** Canonical
**Last updated:** 2026-07-11
**Version:** 1.1.0
**Depends on:** `0-foundation/grammar-syntax.md` (clause template, §I-E), `3-subsystems/aspect.md`

---

Kilor has **no grammatical tense**. There are no verb conjugations for past, present, or future.

Time is expressed through **context and temporal words** (yesterday, tomorrow, now, later, before, etc.). These time words are critically important in the language and **must be placed clause-initially** (before the subject) to establish the temporal frame.

Optional aspect particles (`gin`, `ger`, `gou`; see `3-subsystems/aspect.md`) provide additional temporal precision when needed but are never required.

> **Example:** *piroi ki kau* (yesterday I come) = I came yesterday
> *paroi ki kau* (tomorrow I come) = I will come tomorrow

---

## I. Temporal Word Inventory

### A. Day Scale (mono-word compounds with `roi` "day")

| Word | Syl | Meaning | Construction |
|---|---|---|---|
| `pimaroi` | 3 | day before yesterday | `pi` + `ma` + `roi` |
| `piroi` | 2 | yesterday | `pi` + `roi` |
| `imaroi` | 3 | today | `ima` + `roi` |
| `paroi` | 2 | tomorrow | `pa` + `roi` |
| `pamaroi` | 3 | day after tomorrow | `pa` + `ma` + `roi` |

> **Combining forms:** `pi` ← `tilpi` (before), `pa` ← `tilpa` (after), `ma` (bound infix: one step removed). `roi` = day. `ima` = now.
>
> **Tone:** 2-syllable compounds (`piroi`, `paroi`) are toneless (flat mid-tone). 3-syllable compounds (`pimaroi`, `imaroi`, `pamaroi`) follow the noun Last-3 Domain pattern (H→M→L) — tone markers are used in dictionary citation forms but may be omitted in everyday writing per the closed-class orthographic convention.

### B. Distance Scale (free-standing adverbs)

| Word | Meaning | Construction |
|---|---|---|
| `pima` | earlier / further back | `pi` + `ma` |
| `pama` | later / further ahead | `pa` + `ma` |

> **`pima` and `pama`** have two context-disambiguated meanings:
> 1. **Specific:** exactly two steps away (one thing between it and `ima`)
> 2. **Open-range:** anything ≥ two steps away

### C. Frequency Words (`-saka` paradigm from `sakar` "occurrence")

| Word | Syl | Meaning | Construction |
|---|---|---|---|
| `esaka` | 3 | always | `esa` (all) + `sakar` |
| `slosaka` | 3 | sometimes | `slo(te)` (some) + `sakar` |
| `nasaka` | 3 | never | `na` (negation) + `sakar` |

> **Tone:** 3-syllable frequency words follow the noun Last-3 Domain pattern in citation form. Tone markers may be omitted in everyday writing.

### D. Bare Temporal Roots

| Root | Syl | Meaning | Notes |
|---|---|---|---|
| `shu` | 1 | soon | Simplified from `shuk` + `tlow` |
| `sar` | 1 | late | Simplified from `pusar` + `tlow` |
| `cho` | 1 | early | Bare root, `ch` onset (start-only) |
| `aiga` | 2 | again | Bare root |
| `fou` | 1 | during | Related to `founai` (duration) |

> **Tone:** All bare temporal roots (1–2 syllables) are toneless (flat mid-tone), consistent with the 1–2 syllable toneless rule (`0-foundation/tone-prosody.md` §II-B).

---

## II. Syntax

Temporal words occupy the **clause-initial slot** in the full clause template (see `0-foundation/grammar-syntax.md` §I-E):

```
[Temporal]  [Intensity Adv]  [Adj]  [Subject-NOM]  ...  [Verb]  [nar]
```

> **Example:** `piroi ki kau.` — "I came yesterday." (yesterday I come)

---

*End of Temporal Expression Specification.*