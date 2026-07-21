# Kilor Language Rules

The authoritative specification of the Kilor constructed language. This directory contains all grammatical, phonological, and philosophical rules.

**Last updated:** 2026-07-12
**Version:** 2.2.0

---

## Start Here — Learning Path

New to Kilor? Read these 5 files in order:

1. `0-foundation/philosophy.md` — The 7 dual-concepts that shape everything
2. `0-foundation/phonology.md` — Sounds, syllables, and pronunciation
3. `0-foundation/tone-prosody.md` — How tone works
4. `0-foundation/grammar-syntax.md` — Word order, clause template, compounding
5. `1-nominals/nouns-colour-prefix.md` — How the 7 colours classify nouns

After these, explore any subsystem that interests you — they all depend on the foundation but not on each other.

For usage guides (examples, rhetoric, artistic patterns), see `guide/`.

---

## Quick Reference — Particles & Forms

### Closed-Class Particles

| Particle | Function | File |
|---|---|---|
| `res` | Copula ("is") | `2-predication/copula-existential.md` |
| `ero` | Existential / Possession ("there is", "have") | `2-predication/copula-existential.md` |
| `nar` | Negation ("not") | `2-predication/negation.md` |
| `iu` | Yes/No question marker; affirmative answer | `2-predication/interrogative.md` |
| `na` | Negative answer ("no") | `2-predication/negation.md` |
| `ei` | And | `2-predication/clause-combining.md` |
| `po` | Or (exclusive) | `2-predication/clause-combining.md` |
| `pem` | Or (inclusive) | `2-predication/clause-combining.md` |
| `pona` | XNOR (both or neither) | `2-predication/clause-combining.md` |
| `pemna` | NOR (neither...nor) | `2-predication/clause-combining.md` |
| `amer` | But | `2-predication/clause-combining.md` |
| `li` | If | `2-predication/conditionals.md` |
| `bam` | Then / consequently | `2-predication/conditionals.md` |
| `tu` | When / while | `2-predication/subordination.md` |
| `aiga` | Because | `2-predication/subordination.md` |
| `hoskar` | Although | `2-predication/subordination.md` |
| `fidak` | In order to | `2-predication/subordination.md` |
| `arfi` | Even | `2-predication/subordination.md` |
| `kus` | Relativizer / complementizer | `2-predication/subordination.md` |
| `thin` / `tha` | Demonstrative ("this"/"that") | `1-nominals/demonstratives.md` |
| `gin` | Progressive aspect | `3-subsystems/aspect.md` |
| `ger` | Perfective aspect | `3-subsystems/aspect.md` |
| `gou` | Experiential aspect | `3-subsystems/aspect.md` |
| `sor` | Suggestion (hortative) | `3-subsystems/imperatives.md` |
| `chom` | Polite request | `3-subsystems/imperatives.md` |
| `maug` | Strong prohibition | `3-subsystems/imperatives.md` |
| `tor` | Than (comparative) | `3-subsystems/comparatives.md` |
| `les` | As (equative) | `3-subsystems/comparatives.md` |
| `torra` | Most (superlative) | `3-subsystems/comparatives.md` |
| `wetor` | Much more than | `3-subsystems/comparatives.md` |
| `mangus` | Among | `3-subsystems/comparatives.md` |
| `dir` | Ordinal marker | `3-subsystems/numerals.md` |

### Oblique Particles

| Particle | Role | File |
|---|---|---|
| `sy` | Instrumental / Passive | `1-nominals/cases.md` |
| `mer` | Comitative ("with") | `1-nominals/cases.md` |
| `tilpe` | Between | `1-nominals/cases.md`, `3-subsystems/spatials.md` |
| `ar` | Ablative ("from") | `1-nominals/cases.md` |
| `te` | Dative ("to/for") & spatial root ("towards") | `1-nominals/cases.md`, `3-subsystems/spatials.md` |

### Spatial Postpositions (`-ne` suffix)

| Form | Meaning | File |
|---|---|---|
| `ikne` | inside | `3-subsystems/spatials.md` |
| `oukne` | outside | `3-subsystems/spatials.md` |
| `umne` | under | `3-subsystems/spatials.md` |
| `rapne` | above | `3-subsystems/spatials.md` |
| `haune` | behind | `3-subsystems/spatials.md` |
| `paune` | in front of | `3-subsystems/spatials.md` |
| `hinne` | beside / near | `3-subsystems/spatials.md` |
| `tene` | towards | `3-subsystems/spatials.md` |
| `orane` | along | `3-subsystems/spatials.md` |
| `meipone` | around | `3-subsystems/spatials.md` |

### Case Suffixes & Tone Markers

| Form | Function | File |
|---|---|---|
| `-ni` / `-na` | Accusative | `1-nominals/cases.md` |
| `-si` / `-sa` | Genitive | `1-nominals/cases.md` |
| `-s` | Derivational suffix (adj/adv) | `0-foundation/tone-prosody.md` |
| `j` | High tone marker | `0-foundation/tone-prosody.md` |
| `v` | Low tone marker | `0-foundation/tone-prosody.md` |

### Colour Prefixes & Emotional Particles

| Form | Ontological Class | Emotion | File |
|---|---|---|---|
| `a-` / `a` | Alive / Energy | Anger | `0-foundation/philosophy.md`, `3-subsystems/colour-emotion.md` |
| `e-` / `e` | Crafted / Tool | Joy | same |
| `i-` / `i` | Fluid / Vast | Sadness | same |
| `o-` / `o` | Abstract / Void | Surprise | same |
| `u-` / `u` | Organic / Growth | Calm | same |
| `y-` / `y` | Dense / Mass | Fear | same |
| `ae-` / `ae` | Earth / Boundary | Disgust | same |

### Question Words

| Form | Meaning |
|---|---|
| `aewei` | Who? |
| `aeweisan` | Whose? |
| `awei` | Which? |
| `ewei` | What? |
| `iwei` | Where? |
| `owei` | When? |
| `uwei` | How? |
| `ywei` | Why? |

See `2-predication/interrogative.md` for full details.

### Pronouns

| | Singular | Plural |
|---|---|---|
| 1st | `ki` | `kil` |
| 2nd | `ti` | `til` |
| 3rd Living | `si` | `sil` |
| 3rd Non-Living | `ni` | `nil` |

See `1-nominals/pronouns.md` for declension (ACC `-n`, GEN `-s`).

---

## Directory Structure

```
rules/
├── README.md                   ← You are here
├── 0-foundation/               ← Prerequisite knowledge (read linearly)
│   ├── philosophy.md           — The 7 dual-concepts (SSOT for colour meanings)
│   ├── phonology.md            — Phoneme inventory, syllables, phonotactics
│   ├── tone-prosody.md         — Tone system, -s derivation
│   └── grammar-syntax.md       — Word order, clause template, closed-class particles (SSOT), compounding, plural
├── 1-nominals/                 ← Noun-related systems
│   ├── nouns-colour-prefix.md  — Colour prefix ontology, definiteness, 異體字 override
│   ├── pronouns.md             — Personal pronouns
│   ├── demonstratives.md       — Demonstratives (thin/tha)
│   └── cases.md                — Case suffixes and oblique particles
├── 2-predication/              ← Verb-related & clause-level systems
│   ├── clause-combining.md     — Coordination, disjunction, adversative
│   ├── conditionals.md         — Conditional & consequential clauses (li, bam)
│   ├── copula-existential.md   — Copula & existential constructions
│   ├── interrogative.md        — Question words
│   ├── negation.md             — Negation
│   └── subordination.md        — Relative clauses, complement clauses, adverbial clauses
├── 3-subsystems/               ← Self-contained modules (depend on foundation)
│   ├── aspect.md               — Optional aspect particles
│   ├── colour-emotion.md       — Emotional particles
│   ├── comparatives.md         — Comparatives & superlatives
│   ├── derivational-compounding.md — Derivational compounding via light-noun heads
│   ├── imperatives.md          — Commands, suggestions, prohibitions, vocative
│   ├── numerals.md             — Numerals, measure words, ordinals
│   ├── optative.md             — Optative, desiderative & benedictive mood
│   ├── spatials.md             — Spatial postpositions (-ne suffix)
│   └── temporals.md            — Temporal expression
└── 4-meta/                     ← Project governance
    ├── lexicon-roadmap.md      — Lexicon development plan
    └── section-taxonomy.md     — Section taxonomy (1-8) SSOT

guide/                          ← Usage guides (examples, style, rhetoric)
├── README.md
└── emotional-register-usage.md
```

---

## Dependency Table

When you change a file, check these dependents:

| If you change… | Also check… |
|---|---|
| `0-foundation/philosophy.md` | `nouns-colour-prefix.md`, `colour-emotion.md`, `interrogative.md` |
| `0-foundation/grammar-syntax.md` | All files — defines clause template, closed-class inventory (SSOT), `-s` derivation |
| `0-foundation/phonology.md` | `tone-prosody.md`, `numerals.md`, `kilor.py` |
| `0-foundation/tone-prosody.md` | `numerals.md`, `pronouns.md`, `colour-emotion.md`, `grammar-syntax.md` |
| `1-nominals/nouns-colour-prefix.md` | `colour-emotion.md`, `grammar-syntax.md`, `demonstratives.md` |
| `1-nominals/cases.md` | `grammar-syntax.md`, `pronouns.md`, `spatials.md` |
| `1-nominals/pronouns.md` | `cases.md`, `grammar-syntax.md` |
| `1-nominals/demonstratives.md` | `grammar-syntax.md`, `nouns-colour-prefix.md` |
| `2-predication/conditionals.md` | `grammar-syntax.md`, `subordination.md` |
| `2-predication/copula-existential.md` | `negation.md`, `interrogative.md` |
| `2-predication/negation.md` | `interrogative.md` |
| `2-predication/clause-combining.md` | `grammar-syntax.md`, `cases.md`, `negation.md` |
| `2-predication/subordination.md` | `grammar-syntax.md`, `cases.md`, `interrogative.md`, `negation.md`, `aspect.md`, `conditionals.md` |
| `3-subsystems/aspect.md` | `grammar-syntax.md`, `temporals.md` |
| `3-subsystems/imperatives.md` | `grammar-syntax.md`, `negation.md`, `colour-emotion.md`, `optative.md` |
| `3-subsystems/optative.md` | `grammar-syntax.md`, `colour-emotion.md`, `imperatives.md` |
| `3-subsystems/numerals.md` | `grammar-syntax.md` |
| `3-subsystems/colour-emotion.md` | `philosophy.md`, `nouns-colour-prefix.md`, `grammar-syntax.md` |
| `3-subsystems/temporals.md` | `grammar-syntax.md` |
| `3-subsystems/comparatives.md` | `grammar-syntax.md`, `copula-existential.md` |
| `3-subsystems/derivational-compounding.md` | `grammar-syntax.md`, `tone-prosody.md`, `nouns-colour-prefix.md` |
| `3-subsystems/spatials.md` | `grammar-syntax.md`, `cases.md` |
| `4-meta/section-taxonomy.md` | `kilor/commands/add.py`, `data/AI-GUIDE.md`, `kilor/schema.py`, `kilor/dictionary/src/components/FilterPanel.jsx`, `kilor/commands/export.py` |

---

## For Automated Tools

When modifying any rule file:
1. Read the dependency table above
2. Check all listed dependents for broken cross-references
3. Search `rules/` for any concept name you changed to find implicit references
4. Update this README if you add, remove, or rename a file
5. Run `python kilor.py check` to verify no constraints are violated

---

## Agent-Optimized Conventions

- **No concept is defined in more than one file** — cross-reference with `See path/to/file.md §Section`.
- **Closed-class particles are toneless and `-s` exempt** — this is SSOT in `grammar-syntax.md` §IV-C; do not repeat in other files.
- **Spec files capped at ~250 lines** — if a file exceeds this, extract usage/examples to `guide/`.
- **Every spec file header includes `Depends on:`** listing prerequisite files.

---

## Versioning Convention

Every rule file carries a header with:
- **Module:** Short name
- **Status:** Canonical / Draft / Deprecated
- **Last updated:** YYYY-MM-DD
- **Version:** Semver (MAJOR.MINOR.PATCH)
- **Depends on:** List of prerequisite files

### Version Bumping

| Change Type | Bump |
|---|---|
| Content addition (new section, new rule) | MINOR (1.1.0) |
| Content correction (typo, clarifying wording) | PATCH (1.1.1) |
| Structural change (reorganization, renamed sections, removed rules) | MAJOR (2.0.0) |

All files start at **1.0.0**. When a file's version changes, review its dependents — they may need a PATCH bump.