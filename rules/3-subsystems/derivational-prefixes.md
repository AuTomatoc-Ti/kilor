# Kilor Derivational Prefixes

**Module:** Derivational Prefixes
**Status:** Canonical
**Last updated:** 2026-08-09
**Version:** 1.2.0
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
| 4 | `doi-` / `doir-` | `doir` | Diminutive | N | N | inherit | little / young / cute |
| 5 | `mes-` | `meson` | Augmentative | N, A | N, A | `y-` | mega- / giant / ×10¹² |
| 6 | `ai-` / `aig-` | `aigan` | Re-/Again | V, N | V, N | `o-` | re- / again (POS-preserving) |
| 7 | `kon-` | `konta` | Anti- | N, A | N, A | `o-` | anti- / opposing (POS-preserving) |

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
### D. Diminutive — `doi-` / `doir-` (noun base)

| Form | Root | Meaning (N) |
|---|---|---|
| `doi-chel` | `chel` (child) | little child, young one |
| `doir-aug` → `doiraug` | `aug` (start) | little beginning, small start |

`doi-` creates a diminutive noun — a smaller, younger, or cuter version of the base. Descends from `doir` ("little, small, young, cute / little one").

- **Noun base → N:** "little X, small X, young X." pos_mask = `N`.

`doi-` is the only prefix with output `pos_mask = N` (single-category). Tone Omission (`tone-prosody.md` §IV-G) applies for 3+ syllable forms. For 1–2 syllable words, the bare root is the N form.

### E. Augmentative — `mes-` (noun / adjective base)

| Form | Base | Meaning (N) | Meaning (A) |
|---|---|---|---|
| `mes-fora` | `fora` (fire, N) | giant fire, mega-fire | mega-fiery, extremely fiery |
| `mes-gor` | `gor` (goodness, A) | giant goodness | mega-good, extremely good |

`mes-` creates an augmentative — an enormously scaled version of the base. Descends from `meson` ("huge, giant, enormous; trillion / 10¹²").

- **Noun base → N:** "giant X, mega-X."
- **Noun base → A:** "extremely X-ish, mega-X in quality."
- **Adjective base → A:** "extremely X." Intensifies the quality.
- **Numeric base:** ×10¹² multiplier (e.g., `mes-` + measure word = trillion-fold).

pos_mask = `NA`. Both N and A forms distinguished by tone/`-s`.

`mes-` is **consonant-final** (`s`) — it fuses cleanly with any root without needing consonant restoration (see §II).
### F. Re-/Again — `ai-` / `aig-` (verb / noun base)

| Form | Base | Meaning |
|---|---|---|
| `ai-taka` | `taka` (eat, V) | re-eat, eat again |
| `aig-aug` → `aigaug` | `aug` (start, V/N) | re-start, begin again |
| `ai-srato` | `srato` (house, N) | re-house, rebuild |

`ai-` frames a verb or noun iteratively — "do X again, X again." Descends from `aigan` ("repetition; repeated; to repeat; repeatedly"). POS-preserving: V→V, N→N. pos_mask = `VN`.

`ai-` is vowel-final — before vowel-initial roots, the restored consonant `g` surfaces: `ai-` → `aig-` (§II). `aig-aug` → `aigaug`.

### G. Anti-/Opposing — `kon-` (noun / adjective base)

| Form | Base | Meaning (N) | Meaning (A) |
|---|---|---|---|
| `kon-fora` | `fora` (fire, N) | anti-fire, counter-fire | anti-fire, fire-opposing |
| `kon-gor` | `gor` (good, A) | anti-good | opposing goodness |

`kon-` frames a noun or adjective as oppositional — "anti-X, opposing X." Descends from `konta` ("opposition; opposing; to oppose"). POS-preserving: N→N/A, A→A. pos_mask = `NA`.

`kon-` is **consonant-final** (`n`) — it fuses cleanly with any root without needing consonant restoration (§II): `kon-aug` → `konaug`.
---

## II. Restored Consonant Rule

When the prefix attaches to a **vowel-initial root**, the prefix's elided consonant is restored from the full root — the mirror of the suffix Restored Consonant Rule (`0-foundation/grammar-syntax.md` §III).

| Prefix | Full Root | Before consonant-initial root | Before vowel-initial root |
|---|---|---|---|
| `pi-` / `pih-` | `pih` | `pi-fora` | `pih-aug` → `pihaug` |
| `pa-` / `pah-` | `pah` | `pa-fora` | `pah-eli` → `paheli` |
| `sefta-` / `seftah-` | `seftah` | `sefta-gor` | `seftah-ema` → `seftahema` |
| `doi-` / `doir-` | `doir` | `doi-chel` | `doir-aug` → `doiraug` |
| `ai-` / `aig-` | `aigan` | `ai-taka` | `aig-aug` → `aigaug` |

Consonant-initial roots fuse cleanly with the shortened prefix form — no restoration needed.

`mes-` is **consonant-final** (`s`) — it fuses cleanly with both consonant-initial and vowel-initial roots without any restoration: `mes-fora`, `mes-aug` → `mesaug`.

`kon-` is **consonant-final** (`n`) — likewise no restoration needed: `kon-fora`, `kon-aug` → `konaug`.

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

Prefixes produce three `pos_mask` patterns:

| Prefixes | pos_mask | Tone Omission | N form | A form | V form |
|---|---|---|---|---|---|
| `pi-`, `pa-`, `sefta-`, `mes-`, `kon-` | NA | No (2 letters) | Bare / tonal N | Root+`-s` / tonal A | — |
| `ai-` | VN | No (2 letters) | Bare / tonal N | — | Bare / tonal V |
| `doi-` | N | Yes (1 letter) | Bare root | — | — |

For `pos_mask = NA` prefixes, both N and A are available:

| Syllable count | N form | A form |
|---|---|---|
| 1–2 | Bare root | Root + `-s` |
| 3+ | Tonal N: `j` on 1st of last-3 | Tonal A: `j` on 2nd of last-3 |

For `ai-` (`pos_mask = VN`), N and V forms are available:

| Syllable count | N form | V form |
|---|---|---|
| 1–2 | Bare root | Bare root |
| 3+ | Tonal N: `j` on 1st of last-3 | Tonal V: `v` on 1st of last-3 |

Tone Omission does not apply (2 letters) for NA and VN prefixes — tone markers are mandatory for 3+ syllable forms.

For `doi-` (`pos_mask = N`), only the N form exists — Tone Omission applies: tone markers are optional for 3+ syllable forms; the bare root is always valid.

### C. Derived Stem + Head

When a head attaches to a word that already carries a derivational prefix (a derived stem), the head appears as a separate word. Head-last semantics apply: the rightmost element is the head; everything left modifies it.

---

## IV. Interaction with the Colour Prefix System

Derivational prefixes follow one of three colour prefix rules:

### A. Fixed Prefix

`pi-`, `pa-`, `sefta-`, `ai-`, `kon-` take fixed `o-` (abstract). `mes-` takes fixed `y-` (dense/mass). The order is:

> colour prefix → derivational prefix → root

| Form | Gloss |
|---|---|
| `o-pi-fora` | the pre-fire |
| `o-pa-fora` | the post-fire |
| `o-sefta-gor` | the meta-goodness |
| `o-pihaug` | the pre-start |
| `o-paheli` | the afterlife |
| `o-ai-taka` | the re-eating |
| `o-kon-fora` | the anti-fire |
| `y-mes-fora` | the giant fire |
| `y-mes-gor` | the mega-good |

### B. Inherit from Base

`doi-` inherits the colour prefix of the base noun — the diminutive does not change the ontological class:

| Form | Base prefix | Gloss |
|---|---|---|
| `a-doi-chel` | `a-chel` (child) | the little child |
| `y-doi-srato` | `y-srato` (stone) | the little stone |

This is parallel to suffix inherit-from-base rules (`derivational-suffixes.md` §IV-B: `-ius`, `-eus`, `-ia`, `-lu`, `-wes`, `-rem`, `-rum`).

---

## V. Formal Register

Prefix-derived words have no distinct formal register variant. The full-root form of the source word (`pih`, `pah`, `seftah`, `doir`, `meson`, `aigan`, `konta`) is used as a standalone content word, not as a derivational prefix.

---

## VI. Productivity & Editorial Policy

All seven prefixes are **fully productive**. The same store/don't-store decision checklist applies as for suffixes — see `rules/4-meta/word-creation-pipeline.md` §VIII.

| Form | Store? | Why |
|---|---|---|
| `pi-fora` (pre-fire) | ❌ | Transparent temporal prefix. Computable from `pi-` + `fora`. |
| `paheli` (post-life / afterlife) | 🤔 | Culturally anchored concept — may merit entry as a named category. |
| `seftahema` (meta-truth / epistemology) | 🤔 | Names a philosophical field — culturally significant. |
| `doi-chel` (little child) | ❌ | Transparent diminutive. Computable from `doi-` + `chel`. |
| `mes-fora` (giant fire) | ❌ | Transparent augmentative. Computable from `mes-` + `fora`. |

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