# Kilor Language Rules

The authoritative specification of the Kilor constructed language. This directory contains all grammatical, phonological, and philosophical rules.

**Last updated:** 2026-07-09
**Version:** 1.0.1

---

## Start Here — Learning Path

New to Kilor? Read these 5 files in order:

1. `0-foundation/philosophy.md` — The 7 dual-concepts that shape everything
2. `0-foundation/phonology.md` — Sounds, syllables, and pronunciation
3. `0-foundation/tone-prosody.md` — How tone works
4. `0-foundation/grammar-syntax.md` — Word order, clause template, compounding
5. `1-nominals/nouns-colour-prefix.md` — How the 7 colours classify nouns

After these, explore any subsystem that interests you — they all depend on the foundation but not on each other.

---

## Reference Index

| Concept | File |
|---|---|
| Case suffixes (Nominative, Accusative, Genitive, Instrumental, Dative) | `1-nominals/cases.md` |
| Clause template (full slot layout) | `0-foundation/grammar-syntax.md` §I-E |
| Closed-class particles (full inventory) | `0-foundation/grammar-syntax.md` §IV-C |
| Colour emotional particles (`a`, `e`, `i`, `o`, `u`, `y`, `ae`) | `3-subsystems/colour-emotion.md` |
| Colour noun prefixes (`a-`, `e-`, `i-`, `o-`, `u-`, `y-`, `ae-`) | `1-nominals/nouns-colour-prefix.md` |
| Comparatives & superlatives (`tor`, `les`, `torra`, `wetor`, `mangus`) | `3-subsystems/comparatives.md` |
| Copula & existential (`res`) | `2-predication/copula-existential.md` |
| Dual-concepts (philosophy) | `0-foundation/philosophy.md` |
| Emotional override on nouns (異體字) | `1-nominals/nouns-colour-prefix.md` §VI |
| Interrogatives (question words) | `2-predication/interrogative.md` |
| Lexicon development roadmap | `4-meta/lexicon-roadmap.md` |
| Negation (`nar`) | `2-predication/negation.md` |
| Numerals & measure words | `3-subsystems/numerals.md` |
| Phoneme inventory, syllables, phonotactics | `0-foundation/phonology.md` |
| Plural strategy (none, except pronouns) | `0-foundation/grammar-syntax.md` §VI |
| Pronouns | `1-nominals/pronouns.md` |
| Subordination & relative clauses | `2-predication/subordination.md` |
| Temporal expression (time words) | `3-subsystems/temporals.md` |
| Tone system | `0-foundation/tone-prosody.md` |
| `-s` derivational suffix | `0-foundation/grammar-syntax.md` §V |
| 異體字 (speaker colour override on nouns) | `1-nominals/nouns-colour-prefix.md` §VI |

---

## Directory Structure

```
rules/
├── README.md                   ← You are here
├── 0-foundation/               ← Prerequisite knowledge (read linearly)
│   ├── philosophy.md           — The 7 dual-concepts (SSOT for colour meanings)
│   ├── phonology.md            — Phoneme inventory, syllables, phonotactics
│   ├── tone-prosody.md         — Tone system
│   └── grammar-syntax.md       — Word order, clause template, particles, compounding, -s derivation, plural
├── 1-nominals/                 ← Noun-related systems
│   ├── nouns-colour-prefix.md  — Colour prefix ontology, definiteness, emotional override (異體字)
│   ├── pronouns.md             — Personal pronouns
│   └── cases.md                — Case suffixes and oblique particles
├── 2-predication/              ← Verb-related & clause-level systems
│   ├── copula-existential.md   — Copula & existential constructions
│   ├── negation.md             — Negation
│   ├── interrogative.md        — Question words
│   └── subordination.md        — Relative clauses & subordination
├── 3-subsystems/               ← Self-contained modules (depend on foundation)
│   ├── numerals.md             — Numerals, measure words, ordinals
│   ├── colour-emotion.md       — Emotional particles (sentence-level & verb-level)
│   ├── temporals.md            — Temporal expression
│   └── comparatives.md         — Comparatives & superlatives
└── 4-meta/                     ← Project governance
    └── lexicon-roadmap.md      — Lexicon development plan
```

---

## Maintenance Guide — Dependency Table

When you change a file, check these dependents:

| If you change… | Also check… | Reason |
|---|---|---|
| `0-foundation/philosophy.md` | `1-nominals/nouns-colour-prefix.md`, `3-subsystems/colour-emotion.md`, `2-predication/interrogative.md` | All colour-based systems derive from philosophy dual-concepts |
| `0-foundation/grammar-syntax.md` | All files in `3-subsystems/`, `2-predication/`, `1-nominals/cases.md` | Defines clause template, closed-class particle inventory, `-s` derivation — referenced everywhere |
| `0-foundation/phonology.md` | `0-foundation/tone-prosody.md`, `3-subsystems/numerals.md`, `kilor.py` | Phoneme inventory and phonotactics constrain all word-building; `kilor.py` validates against them |
| `0-foundation/tone-prosody.md` | `3-subsystems/numerals.md`, `1-nominals/pronouns.md`, `3-subsystems/colour-emotion.md`, `0-foundation/grammar-syntax.md` §IV-B | Tone rules apply to numerals, pronouns, emotional particles, and compounding |
| `1-nominals/nouns-colour-prefix.md` | `3-subsystems/colour-emotion.md`, `0-foundation/grammar-syntax.md` | Colour prefix system interacts with emotional particles and NP syntax |
| `1-nominals/cases.md` | `0-foundation/grammar-syntax.md`, `1-nominals/pronouns.md` | Case suffixes interact with word order rules and pronoun inflection |
| `1-nominals/pronouns.md` | `1-nominals/cases.md`, `0-foundation/grammar-syntax.md` §VI | Pronoun declension uses reduced case endings; plural exception to general no-plural rule |
| `2-predication/copula-existential.md` | `2-predication/negation.md`, `2-predication/interrogative.md` | Copula `res` and existential `ero` interact with negation and interrogative particles |
| `2-predication/negation.md` | `2-predication/interrogative.md` | `iu` serves dual role as yes/no marker and affirmative answer; `nar` scoping interacts with `iu` |
| `2-predication/interrogative.md` | `1-nominals/nouns-colour-prefix.md` | Question words use colour prefixes; definiteness rule exemption |
| `2-predication/subordination.md` | `0-foundation/grammar-syntax.md`, `1-nominals/cases.md`, `2-predication/interrogative.md`, `2-predication/negation.md` | `kus` relativizer interacts with case suffixes, question fronting, and negation scoping |
| `3-subsystems/numerals.md` | `0-foundation/grammar-syntax.md` §IV-C, §VI | NP quantification references clause template and closed-class list |
| `3-subsystems/colour-emotion.md` | `0-foundation/philosophy.md` (historical origin), `1-nominals/nouns-colour-prefix.md`, `0-foundation/grammar-syntax.md` §IV-C, §I-E | Emotional particles interact with noun prefixes, clause slots, and closed-class list |
| `3-subsystems/temporals.md` | `0-foundation/grammar-syntax.md` §I-E | Temporal words occupy the clause-initial slot |
| `3-subsystems/comparatives.md` | `0-foundation/grammar-syntax.md` §IV-C, `2-predication/copula-existential.md` | Comparative particles are closed-class; equative uses copula |
| `4-meta/lexicon-roadmap.md` | All files in `rules/` | Lexicon development pipeline — any schema change in rule files may affect word-building workflow |

---

## For Automated Tools

When modifying any rule file:
1. Read the dependency table above
2. Check all listed dependents for broken cross-references
3. Search `rules/` for any concept name you changed to find implicit references
4. Update this README if you add, remove, or rename a file
5. Run `python kilor.py` to verify no constraints are violated

---

## Versioning Convention

Every rule file should carry a header with:
- **Module:** Short name
- **Status:** Canonical / Draft / Deprecated
- **Last updated:** YYYY-MM-DD
- **Version:** Semver (MAJOR.MINOR.PATCH)
- **Depends on:** List of prerequisite files

### Version Bumping

| Change Type | Bump |
|---|---|
| Content addition (new section, new rule, new example) | MINOR (e.g., 1.1.0) |
| Content correction (typo, clarifying wording, bug fix) | PATCH (e.g., 1.1.1) |
| Structural change (reorganization, renamed sections, removed rules) | MAJOR (e.g., 2.0.0) |

All files start at **1.0.0** (canonical baseline). When a file's version changes, review its dependents (see dependency table above) — they may need a PATCH bump if the change affects their content.

### Traceability

Git tags the overall language spec at milestones (e.g., `v1.0.0` = all files at 1.0.0). Individual file versions let you trace which rules changed between releases without diffing the entire repo.
