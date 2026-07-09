# Kilor Pronouns — The Closed-Class Pronominal System

**Module:** Pronoun Inventory & Declension
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.0.0
**Depends on:** `1-nominals/cases.md`, `0-foundation/grammar-syntax.md` §VI, `0-foundation/tone-prosody.md`

---

## I. Core Philosophy

Pronouns in Kilor form a **closed-class irregular paradigm**. They follow the same 3-case system as regular nouns (Nominative unmarked, Accusative, Genitive) but use **reduced case endings** that are exceptions to the standard suffix inventory.

This irregularity is intentional — natural languages nearly always have irregular pronoun paradigms (English *I/me/my*, Japanese *watashi/watashi no*), and Kilor embraces this as a naturalistic feature.

---

## II. Pronoun Roots

### A. Person System

Kilor distinguishes **1st, 2nd, and 3rd person**, with a **living vs. non-living** split in the 3rd person. There is no inclusive/exclusive distinction, no dual/trial number, and no formality levels.

| Person | Singular | Plural | Description |
|:---|:---|:---|:---|
| **1st** | `ki` | `kil` | I / we |
| **2nd** | `ti` | `til` | you (singular) / you (plural) |
| **3rd Living** | `si` | `sil` | he, she, living thing / they (living) |
| **3rd Non-Living** | `ni` | `nil` | it, dead thing, abstract / they (non-living) |

### B. Plural Formation

Pronouns form plurals with the **plural marker `-l(i)-`**. This is a **pronoun-only** closed-class process — regular nouns have no plural marking (see `0-foundation/grammar-syntax.md` §VI).

The marker surfaces in two forms depending on what follows:

- **`-l`** when word-final (Nominative, no case suffix): `ki` → `kil` (we)
- **`-li-`** when a consonant-initial case suffix follows (Accusative `-n`, Genitive `-s`): `ki` → `kilin` (us), `ki` → `kilis` (our)

The epenthetic `-i-` in the `-li-` form prevents forbidden consonant clusters (`-ln-`, `-ls-`) while keeping the root and ending phonotactically legal.

> **Rule:** This is a closed-class morphological process that does not extend to nouns.

---

## III. Declension — Reduced Case Endings

Pronouns use **reduced case endings** instead of the standard `-ni`/`-na` (Accusative) and `-si`/`-sa` (Genitive):

| Case | Standard Suffix | Pronoun Suffix | Example (1st Sg) |
|:---|:---|:---|:---|
| **Nominative** | *(unmarked)* | *(unmarked)* | `ki` (I) |
| **Accusative** | `-ni` / `-na` | **`-n`** | `kin` (me) |
| **Genitive** | `-si` / `-sa` | **`-s`** | `kis` (my / mine) |

### A. Invariant Form — No Contrastive Suffix Rule

Pronoun case endings are **invariant**. They do not participate in the Contrastive Suffix Rule. The endings `-n` and `-s` are always used regardless of vowel class. This is a closed-class exception to `1-nominals/cases.md` §II.

Unlike regular case suffixes (`-ni`/`-na`, `-si`/`-sa`), which are extrasyllabic for tone purposes (see `0-foundation/tone-prosody.md` §IV-B), the reduced pronoun endings are **fully syllabified**: `-n` and `-s` become the coda of the preceding syllable (e.g., `ki-lin`, `ki-lis` = CVC). They participate in the word's tone contour rather than sitting outside it as flat-mid appendices.

### B. Full Declension Table

| Person | NOM | ACC | GEN |
|:---|:---|:---|:---|
| **1st Sg** | ki | kin | kis |
| **2nd Sg** | ti | tin | tis |
| **3rd Living Sg** | si | sin | sis |
| **3rd Non-Living Sg** | ni | nin | nis |
| **1st Pl** | kil | kilin | kilis |
| **2nd Pl** | til | tilin | tilis |
| **3rd Living Pl** | sil | silin | silis |
| **3rd Non-Living Pl** | nil | nilin | nilis |

---

## IV. Tone

Pronouns follow the standard Kilor tone rules in pronunciation only (see `0-foundation/tone-prosody.md`):

| Syllable Count | Spelled Form | Pronounced Tone |
|:---|:---|:---|
| **1-syllable** (ki, kin, kis, etc.) | `ki` | Flat mid-tone |
| **2-syllable** (kilin, tilis, etc.) | `kilin` | H→L (noun pattern) |

### A. Simplified Spelling Convention

Pronouns are a closed class — every form is unambiguously nominal. Therefore, **tone markers (`j`/`v`) are omitted from pronoun spelling** even when multi-syllable forms carry non-flat tone contours in speech. This simplifies the written form without creating ambiguity.

> **Pronunciation:** 2-syllable inflected forms (`kilin`, `tilis`, `silin`, `nilin`, `silis`, `nilis`) are pronounced with H→L contour. 1-syllable forms are flat mid.

---

## V. Usage Notes

### A. Possession

Possession by pronoun follows the same rule as regular nouns (see `1-nominals/cases.md` §IV): the Genitive-marked pronoun may appear before or after the possessed noun.

> **Example:** `kis lujmi` (my light) ≡ `lujmi kis` (light of mine)

### B. Accusative Optionality

The Accusative forms (`kin`, `tin`, etc.) follow the same two-tier rule as regular nouns (see `1-nominals/cases.md` §III):
- **Optional** in everyday SOV speech
- **Mandatory** in formal writing and non-SOV word order

### C. The `-s` on Pronouns — Genitive Only

The derivational modifier suffix `-s` (see `0-foundation/tone-prosody.md` §III) attaches only to noun and verb roots to form adjectives and adverbs. Pronouns are a **closed class** — they never receive derivational morphology.

The `-s` on a pronoun form (e.g., `kis`, `tis`, `sis`, `nis`, and their plural counterparts) is always and exclusively the **Genitive case ending**. There is no ambiguity.

---

## VI. Summary of Irregularities

| Rule | Standard | Pronoun Exception |
|:---|:---|:---|
| Accusative suffix | `-ni` / `-na` | `-n` (invariant) |
| Genitive suffix | `-si` / `-sa` | `-s` (invariant) |
| Contrastive Suffix Rule | Required | Exempt (invariant endings) |
| Plural marking | None | `-l(i)-` marker (pronoun-only, surfaces as `-l` word-finally, `-li-` before a consonant-initial suffix) |

---

*End of Pronouns Specification.*