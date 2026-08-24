# Kilor Aspect — Optional Post-Verbal Particles

**Module:** Progressive, Perfective, Experiential Aspect
**Status:** Canonical
**Last updated:** 2026-08-25
**Version:** 1.3.0
**Depends on:** `0-foundation/grammar-syntax.md`, `3-subsystems/temporals.md`
**Interacts with:** `2-predication/negation.md` (nar after aspect), `3-subsystems/imperatives.md` (aspect in commands)

---

Kilor has **no grammatical tense** — time is expressed through temporal words and context (see `3-subsystems/temporals.md`). Aspect is handled by three **optional** post-verbal particles, all closed-class and toneless (see `0-foundation/grammar-syntax.md` §IV-C).

**Aspect particles are entirely optional.** A bare verb defaults to a habitual or simple reading determined by context.

## I. Aspect Particle Inventory

| Particle | Meaning | Example |
|---|---|---|
| `gin` | progressive — "be X-ing" | `ki bau taka gin.` — "I'm eating bread." |
| `ger` | perfective — "have X-ed" | `ki bau taka ger.` — "I've eaten bread." |
| `gou` | experiential — "have X-ed before" | `ki bau taka gou.` — "I've eaten bread before." |
| (bare verb) | habitual / simple | `ki bau taka.` — "I eat bread." |

`gin` ≈ Cantonese 緊 (gan2). `ger` ≈ 咗 (zo2). `gou` ≈ 過 (gwo3).

### Contrast: `ger` vs `gou`

| Particle | Focus | Implication |
|---|---|---|
| `ger` | Action completed; result state relevant now | "I've eaten (so I'm not hungry)" |
| `gou` | Action happened at least once in experience | "I've eaten that before (it's not new to me)" |

---

## II. Aspect Details

### A. Progressive — `gin`

> `ki bau taka gin.` — "I'm eating bread (right now)."
> `piroi ki kau gin.` — "Yesterday I was coming."

### B. Perfective — `ger`

> `si kau ger.` — "He/she has arrived." (and is here now)
> `ki lira taki ger.` — "I've drunk water." (and am no longer thirsty)

### C. Experiential — `gou`

> `si te selo kau gou.` — "He/she has been to the market before."
> `ki yre winar gou.` — "I've seen the moon before."

---

## III. Interaction with Other Systems

### A. Negation

`nar` follows the aspect particle:

> `ki bau taka gin nar.` — "I'm not eating bread."
> `ki kau ger nar.` — "I haven't arrived yet."
> `ki te selo kau gou nar.` — "I've never been to the market."

### B. Temporal Words

Aspect particles combine freely with clause-initial temporal words:

> `piroi ki bau taka ger.` — "Yesterday I had already eaten bread."
> `paroi ki bau taka gin.` — "Tomorrow I'll be eating bread."

### C. Imperatives

> `Taka ger!` — "Eat up!" (urging completion)

### D. Future + Aspect (`rum` modal)

The root-modal `rum` "will; to be about to" (see `0-foundation/grammar-syntax.md` §I-E) marks the general future and stacks with aspect particles post-verbally without combining them:
> `ki bau rum taka gin.` — "I will be eating bread."
> `ki bau rum taka ger.` — "I will have eaten bread."

There is **no aspect stacking** (`ger gin` is avoided for poor euphony); the perfect-progressive set ("have/had/will have been -ing") is expressed via context/time words, not grammatically. See §IV for the full English-tense mapping.

---

## IV. English-Tense Overview (conceptual mapping)

Kilo has **no grammatical tense**; this is a **conceptual mapping** of English tense terms onto Kilo's temporal/contextual + aspect + modal machinery. Aspect is never stacked (`ger gin` is avoided — poor euphony); the perfect-progressive set is not grammatically marked.

| # | English | Kilor | Notes |
|---|---|---|---|
| 1 | Simple present (I eat) | `ki bau taka` | bare verb |
| 2 | Present progressive (am eating) | `ki bau taka gin` | `gin` aspect |
| 3 | Present perfect (have eaten) | `ki bau taka ger` | `ger` aspect |
| 4 | Simple past (ate) | `piroi ki bau taka` | temporal word or context |
| 5 | Past progressive (was eating) | `piroi ki bau taka gin` | |
| 6 | Past perfect (had eaten) | `piroi ki bau taka ger` | |
| 7 | Simple future (will eat) | `ki bau rum taka` | **`rum` modal** |
| 8 | Future progressive (will be eating) | `ki bau rum taka gin` | `rum` + `gin` (separate) |
| 9 | Future perfect (will have eaten) | `ki bau rum taka ger` | `rum` + `ger` (separate) |

**Excluded (perfect-progressive set):** present/past/future perfect progressive ("have/had/will have been -ing") are not grammatically marked — expressed via context, time words, or periphrasis. This matches their low frequency in English and the awkwardness of an aspect stack in Kilo.

---

*End of Aspect Specification.*