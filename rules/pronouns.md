# Kilor Pronouns — The Closed-Class Pronominal System

**Module:** Pronoun Inventory & Declension
**Status:** Canonical

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

The plural forms are derived from the singular roots via the **infix `-l-`** inserted before the case ending. This `-l-` plural infix is **pronoun-only** — regular nouns have no plural marking (see `grammar-syntax.md` §VII).

> **Rule:** `ki` + `-l-` → `kil` (we). This is a closed-class morphological process that does not extend to nouns.

---

## III. Declension — Reduced Case Endings

Pronouns use **reduced case endings** instead of the standard `-ni`/`-na` (Accusative) and `-si`/`-sa` (Genitive):

| Case | Standard Suffix | Pronoun Suffix | Example (1st Sg) |
|:---|:---|:---|:---|
| **Nominative** | *(unmarked)* | *(unmarked)* | `ki` (I) |
| **Accusative** | `-ni` / `-na` | **`-n`** | `kin` (me) |
| **Genitive** | `-si` / `-sa` | **`-s`** | `kis` (my / mine) |

### A. Invariant Form — No Vowel Harmony

Pronoun case endings are **invariant**. They do not participate in vowel harmony (the Echo Rule). The endings `-n` and `-s` are always used regardless of vowel class. This is a closed-class exception to `cases.md` §II.

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

Pronouns follow the standard Kilor tone rules (see `tone-prosody.md`):

| Syllable Count | Tone Pattern | Example |
|:---|:---|:---|
| **1-syllable** (ki, kin, kis, etc.) | **Toneless** — flat mid-tone | `ki` (flat mid) |
| **2-syllable** (kilin, tilis, etc.) | **Noun pattern** — H(`j`)→L | `kijlin`, `tijlis` |

### A. Rationale

1. **1-syllable pronouns are toneless** — this follows the general rule that all 1-syllable words in Kilor carry no tone markers (see `tone-prosody.md` §II-C).

2. **2-syllable inflected forms** (kilin, tilis, etc.) follow the standard 2-syl noun pattern H(`j`)→L, as they are multi-syllabic and benefit from a clear tonal contour.

3. The tone marker `j` is placed on the **first syllable** of 2-syllable forms: `kijlin`, `tijlis`, `sijlin`, `nijlin`, `tijlis`, `sijlis`, `nijlis`.

---

## V. Usage Notes

### A. Possession

Possession by pronoun follows the same rule as regular nouns (see `cases.md` §IV): the Genitive-marked pronoun may appear before or after the possessed noun.

> **Example:** `kis aelumi` (my light) ≡ `aelumi kis` (the light of mine)

### B. Accusative Optionality

The Accusative forms (`kin`, `tin`, etc.) follow the same two-tier rule as regular nouns (see `cases.md` §III):
- **Optional** in everyday SOV speech
- **Mandatory** in formal writing and non-SOV word order

### C. The `-s` Homograph

The Genitive ending `-s` is identical in form to the derivational modifier suffix `-s` (see `tone-prosody.md` §III). This creates a theoretical homograph (e.g., `kis` = "my" or "ki-like"). In practice, context and syntactic position disambiguate:
- `kis` before/after a noun → Genitive pronoun (my)
- `kis` modifying a verb or as a predicate → adjective derived from hypothetical root `ki`

This ambiguity is accepted as a natural feature of the language.

---

## VI. Summary of Irregularities

| Rule | Standard | Pronoun Exception |
|:---|:---|:---|
| Accusative suffix | `-ni` / `-na` | `-n` (invariant) |
| Genitive suffix | `-si` / `-sa` | `-s` (invariant) |
| Vowel harmony | Required | Exempt (invariant endings) |
| Plural marking | None | `-l-` infix (pronoun-only) |

---

*End of Pronouns Specification.*