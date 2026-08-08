# Kilor Derivational Prefixes

**Module:** Derivational Prefixes
**Status:** Canonical
**Last updated:** 2026-08-09
**Version:** 1.0.0
**Depends on:** `0-foundation/grammar-syntax.md` (§III Restored Consonant Rule), `0-foundation/tone-prosody.md` (Last-3 Domain §IV-A), `0-foundation/phonology.md` (§IV positional consonant classes), `1-nominals/nouns-colour-prefix.md`, `3-subsystems/derivational-suffixes.md`

**Companion file:** `3-subsystems/derivational-suffixes.md` — suffix derivations following the same morphological pattern.
**Interacts with:** `1-nominals/nouns-colour-prefix.md` (prefix ordering), `0-foundation/tone-prosody.md` (tone on fused words)

---

Kilor derivation also uses derivational prefixes — 1–2 syllable abstract heads that fuse directly to the beginning of the root as a single word. The resulting word is a single tone domain.

Prefixes follow the same historical pattern as suffixes: they descend from full content roots, coexist with them as independent words, and appear in a shortened combining form when fused. When the prefixed root begins with a vowel, the elided consonant is restored from the full root — the mirror of the Restored Consonant Rule for suffixes (`0-foundation/grammar-syntax.md` §III).

For multi-word compounding (content-root heads, mono/multi decision rules), see `3-subsystems/compounding.md`.

---

## I. Prefix Inventory

| # | Prefix | Full Root | Domain | Base | Output | Colour | Meaning |
|---|---|---|---|---|---|---|---|
| 1 | `pi-` / `pih-` | `pih` | Temporal Pre- | N | N, A | `o-` | pre-/before (in time) |
| 2 | `pa-` / `pah-` | `pah` | Temporal Post- | N | N, A | `o-` | post-/after (in time) |
| 3 | `sefta-` / `seftah-` | `seftah` | Meta- | any root | N, A | `o-` | meta- / beyond |

All prefixes descend from full content roots (shown in the "Full Root" column) and still coexist with them as independent words. The prefix form is the shortened combining form — the same historical process as derivational suffixes.

### A. Temporal Pre- — `pi-` / `pih-` (noun base)

| Form | Root | Meaning (N) | Meaning (A) |
|---|---|---|---|
| `pi-fora` | `fora` (fire) | pre-fire — the time before fire | pre-fire — occurring before fire |
| `pih-aug` → `pihaug` | `aug` (start) | pre-start — the moment before beginning | pre-start — occurring before the start |

`pi-` frames a noun temporally before the event or period it names. Descends from `pih` ("before / prior").

- **Noun base → N:** "the time/period before X."
- **Noun base → A:** "occurring/existing before X."

### B. Temporal Post- — `pa-` / `pah-` (noun base)

| Form | Root | Meaning (N) | Meaning (A) |
|---|---|---|---|
| `pa-fora` | `fora` (fire) | post-fire — the time after fire | post-fire — occurring after fire |
| `pah-eli` → `paheli` | `eli` (life) | post-life — afterlife | post-life — occurring after life |

`pa-` frames a noun temporally after the event or period it names. Descends from `pah` ("after / subsequent").

- **Noun base → N:** "the time/period after X."
- **Noun base → A:** "occurring/existing after X."

### C. Meta- — `sefta-` / `seftah-` (any root base)

| Form | Root | Meaning (N) | Meaning (A) |
|---|---|---|---|
| `sefta-gor` | `gor` (goodness) | meta-goodness — the study/nature of goodness itself | beyond goodness — transcending goodness |
| `seftah-ema` → `seftahema` | `ema` (truth) | meta-truth — the epistemology of truth | beyond truth — transcending truth |

`sefta-` frames a root in two distinct semantic flavours. Descends from `seftah` ("beyond / meta, transcendent").

- **Any base → N:** "the abstraction/study of X; X-as-such." Names the concept as a field or subject of inquiry.
- **Any base → A:** "beyond/transcending X." Describes something as surpassing the base concept.

The N and A senses are distinguished by tone (3+ syllable) or the `-s` suffix (1–2 syllable) per `0-foundation/tone-prosody.md`.
---

## II. Restored Consonant Rule

When the prefix attaches to a **vowel-initial root**, the prefix's elided consonant is restored from the full root — the mirror of the suffix Restored Consonant Rule (`0-foundation/grammar-syntax.md` §III).

| Prefix | Full Root | Before consonant-initial root | Before vowel-initial root |
|---|---|---|---|
| `pi-` / `pih-` | `pih` | `pi-fora` | `pih-aug` → `pihaug` |
| `pa-` / `pah-` | `pah` | `pa-fora` | `pah-eli` → `paheli` |
| `sefta-` / `seftah-` | `seftah` | `sefta-gor` | `seftah-ema` → `seftahema` |

Consonant-initial roots fuse cleanly with the shortened prefix form — no restoration needed.

---

## III. Syntax & Wordhood

### A. Mono-Word Fusion

Prefix-derived words are single orthographic words with one tone domain per `0-foundation/tone-prosody.md`:

- 1–2 syllable words: toneless (flat mid)
- 3+ syllable words: receive tone markers (`j`/`v`) on the last three syllables

Colour prefixes attach to the fused word as a whole: `o-pi-fora` (the pre-fire), `o-pa-fora` (the post-fire). Case suffixes attach to the end of the fused word: `pi-forani` (pre-fire-ACC), `pa-forasi` (post-fire-GEN).

#### Fusion constraint: one prefix per word

At most one derivational prefix can fuse to the bare root. Prefix and suffix may co-occur on the same root: `pi-takamae` = "pre-eater" (one who existed before the act of eating). When an additional derivational head is needed, it appears as a separate word following head-last semantics — see `3-subsystems/compounding.md` §II.

#### Start-only consonant restriction

Per `0-foundation/phonology.md` §IV-C, start-only consonants (`kl`, `tl`, `bl`, `ml`, `kr`, `br`, `gr`, `fr`, `pr`, `sr`) can only appear at absolute word-initial position. A root beginning with a start-only consonant cannot receive a prefix (which would place the consonant in medial position). Such combinations must use the multi-word form: `pi srato` = "pre-house" (not `*pisrato`). See `3-subsystems/compounding.md` §II for multi-word rules.

### B. Tone & Category

All three prefixes produce `pos_mask = NA`. Both N and A forms are always available; the speaker selects the appropriate form:

| Syllable count | N form | A form |
|---|---|---|
| 1–2 | Bare root | Root + `-s` |
| 3+ | Tonal N: `j` on 1st of last-3 | Tonal A: `j` on 2nd of last-3 |

Since `pos_mask` has two letters (NA), Tone Omission (`tone-prosody.md` §IV-G) does not apply — tone markers are mandatory for 3+ syllable forms.

### C. Derived Stem + Head

When a head attaches to a word that already carries a derivational prefix (a derived stem), the head appears as a separate word. Head-last semantics apply: the rightmost element is the head; everything left modifies it.

---

## IV. Interaction with the Colour Prefix System

All three prefixes take fixed colour prefix `o-` (abstract). The order is:

> colour prefix → derivational prefix → root

| Form | Gloss |
|---|---|
| `o-pi-fora` | the pre-fire |
| `o-pa-fora` | the post-fire |
| `o-sefta-gor` | the meta-goodness |
| `o-pihaug` | the pre-start |
| `o-paheli` | the afterlife |

Colour prefix is inherited from the derivational prefix (always `o-`), not from the base noun. This is a fixed semantic-class prefix rule — parallel to `derivational-suffixes.md` §IV-A (Agent → `a-`, Instrument → `e-`, etc.).

---

## V. Formal Register

Prefix-derived words have no distinct formal register variant. The full-root form of the source word (`pih`, `pah`, `seftah`) is used as a standalone content word, not as a derivational prefix.

---

## VI. Productivity & Editorial Policy

All three prefixes are **fully productive**. The same store/don't-store decision checklist applies as for suffixes — see `rules/4-meta/word-creation-pipeline.md` §VIII.

| Form | Store? | Why |
|---|---|---|
| `pi-fora` (pre-fire) | ❌ | Transparent temporal prefix. Computable from `pi-` + `fora`. |
| `paheli` (post-life / afterlife) | 🤔 | Culturally anchored concept — may merit entry as a named category. |
| `seftahema` (meta-truth / epistemology) | 🤔 | Names a philosophical field — culturally significant. |

---

## VII. Cross-References

- **Suffix system:** `3-subsystems/derivational-suffixes.md`
- **Multi-word compounding:** `3-subsystems/compounding.md`
- **Restored Consonant Rule:** `0-foundation/grammar-syntax.md` §III
- **Tone rules:** `0-foundation/tone-prosody.md`
- **Colour prefix ontology:** `1-nominals/nouns-colour-prefix.md`
- **Phonotactic rules:** `0-foundation/phonology.md`
- **Editorial storage policy:** `rules/4-meta/word-creation-pipeline.md` §VIII

---

*End of Derivational Prefixes Specification.*