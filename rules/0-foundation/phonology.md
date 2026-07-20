# Kilor Phonology — The Sound System

**Module:** Phonemic Inventory & Syllable Structure
**Status:** Canonical
**Last updated:** 2026-07-21
**Version:** 1.3.0
**Depends on:**

---

## I. Crucial Constraint: `j` and `v` Reserved

The letters **`j`** and **`v`** are **exclusively reserved for Tone Notation** on 3+ syllable words (see `0-foundation/tone-prosody.md`). They never serve as consonants or vowels in the segmental phonetic inventory. No root, suffix, or colour prefix may contain `j` or `v` as a segmental phoneme. 1–2 syllable words are toneless and never carry `j` or `v`.

When `j` or `v` appears in the orthography of a 3+ syllable word (e.g., `lunjlagak`, `rujsome`), it is a floating tone marker — an extra-segmental annotation overlaid on the vowel of its anchor syllable, not a consonant or vowel in the syllable structure. See `0-foundation/tone-prosody.md` §I and `0-foundation/phonology.md` §IV-A for the syllable-level treatment.

---

## II. ASCII Transcription Convention

Kilor has its own native script. The ASCII transcription is a romanisation — it represents Kilor sounds using only letters available on an English keyboard. This document uses the ASCII transcription exclusively.

**Single letters, multi-character typing.** Several Kilor phonemes require two (or three) ASCII characters to write because no single English letter corresponds to the sound. These multi-character sequences represent **a single Kilor letter** — one glyph in the native script, one articulatory gesture, one phoneme. They are **not** sequences of separate consonants. Examples:

| ASCII | Kilor letter type | IPA | Native script |
|---|---|---|---|
| `sh` | one letter | /ʃ/ | one glyph |
| `ch` | one letter | /tʃ/ | one glyph |
| `th` | one letter | /θ/ | one glyph |
| `ng` | one letter | /ŋ/ | one glyph |
| `rk` | one letter | /ɾk/ (coarticulated) | one glyph |
| `sl`, `kl`, `tl`, `bl`, `ml` | one letter each | lateral-release coarticulations | one glyph each |
| `kr`, `br`, `gr`, `fr`, `pr` | one letter each | trill-release coarticulations | one glyph each |

When a reader sees `pesha` in the ASCII transcription, it represents the Kilor letters: **p, e, s, h, a** — five separate letters. The sequence `sh` in mid-word position is never the single Kilor letter for /ʃ/; it is two distinct letters (`s` immediately followed by `h`). See §III-E for the formal disambiguation rule.

---

## III. Vowel Inventory

### A. The 7 Monophthongs (Single Vowels)

Pure, ungliding vowel sounds.

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **a** | /ɑ/ | ah | f**a**ther |
| **e** | /ɛ/ | eh | b**e**d |
| **i** | /i/ | ee | mach**i**ne |
| **o** | /ɔ/ | aw | l**o**t / th**ough**t |
| **u** | /u/ | oo | fl**u**te |
| **y** | /y/ | ü | German *über* |
| **ae** | /æ/ | short a | c**a**t / **ai**r |

### B. The 7 Permitted Diphthongs

Two vowels that merge into a **single syllable nucleus**. These are the **only** allowed vowel glides.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **ai** | /aɪ/ | eye | m**y** / b**uy** |
| **au** | /aʊ/ | ow | c**ow** / h**ow** |
| **ei** | /eɪ/ | ay | d**ay** / s**ay** |
| **eu** | /eʊ/ | ew | m**ew** / f**ew** |
| **iu** | /ju/ | you | **you** / **use** |
| **oi** | /ɔɪ/ | oy | b**oy** / t**oy** |
| **ou** | /oʊ/ | oh | g**o** / sn**ow** |

---

## IV. Consonant Inventory

Kilor consonants belong to one of four positional classes. A consonant's class determines where it may appear in a word.

### A. Core Consonants (Appear Anywhere)

15 consonants that may appear word-initially, word-medially, or word-finally. Grouped by articulatory mechanics.

**Labial** (lips / lip-teeth):

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **p** | /p/ | Voiceless bilabial plosive | s**p**in |
| **b** | /b/ | Voiced bilabial plosive | **b**oy |
| **m** | /m/ | Bilabial nasal | **m**oon |
| **f** | /f/ | Voiceless labiodental fricative | **f**ish |
| **w** | /w/ | Voiced labio-velar approximant | **w**e |

**Coronal** (tongue tip / blade):

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **t** | /t/ | Voiceless alveolar plosive | s**t**op |
| **d** | /d/ | Voiced alveolar plosive | **d**og |
| **n** | /n/ | Alveolar nasal | **n**o |
| **s** | /s/ | Voiceless alveolar fricative | **s**ee |
| **l** | /l/ | Alveolar lateral approximant | **l**ight |
| **r** | /r/ | Alveolar trill | Spanish pe**rr**o |
| **c** | /ts/ | Voiceless alveolar affricate | pi**zz**a |

**Dorsal & Glottal** (velar / glottis):

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **k** | /k/ | Voiceless velar plosive | s**k**y |
| **g** | /g/ | Voiced velar plosive | **g**o |
| **h** | /h/ | Voiceless glottal fricative | **h**at |

### B. Edge-Only Consonants

3 single-letter consonants that may appear at either word edge — word-initially (as syllable onset) or word-finally (as syllable coda) — but **never word-medially**. These are single Kilor letters, each representing one phoneme.

**Fricative/Affricate:**

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **sh** | /ʃ/ | Voiceless postalveolar fricative | **sh**ip |
| **ch** | /tʃ/ | Voiceless postalveolar affricate | **ch**urch |
| **th** | /θ/ | Voiceless dental fricative | **th**in |

> **Mid-word appearance:** The sequences `sh`, `ch`, `th` appearing mid-word are always two separate core consonants (`s`+`h`, `c`+`h`, `t`+`h`), never the single edge-only letter. See §IV-E.

### C. Start-Only Consonants

13 single-letter consonants that may appear **only at the absolute beginning of a word** (word-initial position). No vowel may precede them. Each is one continuous articulatory gesture — a single phoneme, one Kilor letter.

**Lateral-release onsets:** The tongue tip presses to the roof, and air releases over the sides into the vowel.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **sl** | /s͜l/ | `s` released laterally | whi**stl**e (without the 't') |
| **kl** | /k͜l/ | `k` released laterally | **cl**ick |
| **tl** | /t͜l/ | `t` released laterally | bo**ttl**e |
| **bl** | /b͜l/ | `b` released laterally | bub**bl**e |
| **ml** | /m͜l/ | `m` released laterally | ha**ml**et (compressed) |

**Trill-release onsets:** The consonant releases directly into an alveolar trill as one continuous motion.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **kr** | /k͡r/ | `k` released into trill | **cr**y (coarticulated) |
| **br** | /b͡r/ | `b` released into trill | **br**ight (coarticulated) |
| **gr** | /ɡ͡r/ | `g` released into trill | **gr**een (coarticulated) |
| **fr** | /f͡r/ | `f` released into trill | **fr**ee (coarticulated) |
| **pr** | /p͡r/ | `p` released into trill | **pr**oud (coarticulated) |

> **Compounding restriction:** These start-only consonants are restricted to **absolute word-initial** position. A root beginning with a start-only consonant may not appear as the second or later element in a mono-word compound (where it would become word-medial). Such combinations must use multi-word compounds instead. Roots beginning with a core consonant (see §IV-A) may appear in any position within a compound.

> **Mid-word appearance:** The sequences `sl`, `kl`, `tl`, `bl`, `ml`, `kr`, `br`, `gr`, `fr`, `pr` appearing mid-word are always two separate core consonants, never the single start-only letter. See §IV-E.

### D. End-Only Consonants

3 single-letter consonants that may appear **only at the absolute end of a word** (word-final position). No vowel may follow them. Each is one phoneme — one Kilor letter.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **ng** | /ŋ/ | Velar nasal | si**ng** |
| **x** | /x/ | Voiceless uvular/velar fricative | Scottish Lo**ch** |
| **rk** | /ɾk/ | Rhotic-velar coarticulated coda | a**rk**, da**rk** |

> **Mid-word appearance:** The sequences `ng` and `rk` appearing mid-word are always two separate core consonants (`n`+`g`, `r`+`k`), never the single end-only letter. See §IV-E.

### E. Mid-Word Disambiguation Rule

When a multi-character ASCII sequence (e.g., `sh`, `ng`, `kr`, `rk`, `sl` …) appears **inside** a word — not at the absolute start or end — it is always parsed as two separate core consonants, never as the single Kilor letter. The single letter only exists at word edges.

**Examples:**

| Word | Kilor Letters | Syllables | Explanation |
|:---|:---|:---|:---|
| `shu` | (sh), u | shu | Single `sh` letter at word start ✓ |
| `ash` | a, (sh) | ash | Single `sh` letter at word end ✓ |
| `pesha` | p, e, s, h, a | pes·ha | Mid-word: separate `s` + `h` letters |
| `meshen` | m, e, s, h, e, n | mes·hen | Mid-word: separate `s` + `h` letters |
| `mingo` | m, i, n, g, o | min·go | Mid-word: separate `n` + `g` letters |
| `mangus` | m, a, n, g, u, s | man·gus | Mid-word: separate `n` + `g` letters |
| `akri` | a, k, r, i | ak·ri | Mid-word: separate `k` + `r` letters |
| `darka` | d, a, r, k, a | dar·ka | Mid-word: separate `r` + `k` letters |

### F. Positional Class Summary

| Class | Count | Appears | Examples |
|:---|:---|:---|:---|
| Core (§IV-A) | 15 | Anywhere (initial, medial, final) | `p, b, m, f, w, t, d, n, s, l, r, c, k, g, h` |
| Edge-Only (§IV-B) | 3 | Absolute word-initial or word-final only | `sh, ch, th` |
| Start-Only (§IV-C) | 13 | Absolute word-initial only | `sl, kl, tl, bl, ml, kr, br, gr, fr, pr` |
| End-Only (§IV-D) | 3 | Absolute word-final only | `ng, x, rk` |

> **Total consonants:** 34 (15 core + 3 edge-only + 13 start-only + 3 end-only)

> **No `j` or `v` permitted** as consonants — these are reserved for tone markers (§I).

---

## V. Syllable Structure

### A. Extra-Segmental Tone Markers

The letters **`j`** and **`v`** are exclusively tone markers. They are **extra-segmental annotations** — they carry no segmental phonetic value (no inherent sound) and float outside the syllable structure. A syllable like `auj` is parsed as **V** (nucleus `au`) with a floating H tone marker, **not** as a V+C sequence.

### B. The 4 Permitted Templates

**Consonant clusters are strictly forbidden.** Every syllable must conform to exactly one of these four shapes:

| Template | Pattern | Examples |
|:---|:---|:---|
| **CV** | Consonant + Vowel | *ka, mi, sou* |
| **CVC** | Consonant + Vowel + Consonant | *kan, mil, sok* |
| **VC** | Vowel + Consonant | *ak, il, ok* |
| **V** | Standalone Vowel/Diphthong | *a, o, ae, ai* |

The single C in the templates above may be a core consonant, an edge-only consonant (at word edges), a start-only consonant (only in onset position at word start), or an end-only consonant (only in coda position at word end). Multi-character representations (`sh`, `ng`, `kr`, etc.) occupy a single C slot — they are not consonant clusters.

### C. The V Template Rule

The **V** template (a standalone vowel or diphthong) is primarily permitted at:

1. The **beginning of words** (e.g., *a-ki-la*)
2. As **standalone grammatical particles** (e.g., colour prefixes like `a-`, `e-`)
3. As a **hiatus** between a colour prefix and the root (e.g., `a-ajkora`: V + V, creating a brief vowel hiatus; an optional glottal catch may be inserted in careful speech)

> **Note:** A diphthong (e.g., `au`) counts as a single **V** nucleus within a syllable.

### D. Hard Constraints

- ❌ No consonant clusters (no CCV, CVCC, etc.) — multi-character letters such as `sh`, `kr`, `ng` are single C slots, not clusters
- ❌ No `j` or `v` as consonants
- ❌ Start-only consonants only at absolute word-initial position; no vowel before them
- ❌ End-only consonants only at absolute word-final position; no vowel after them
- ❌ Edge-only consonants only at absolute word edges (initial or final); not word-medially
- ❌ Mid-word multi-character sequences are always separate core consonants
- ❌ No diphthong outside the 7 permitted glides
- ✅ Every syllable is clearly delineated and stands on its own

### E. Extrasyllabic Appendix: `-s`

The derivational modifier suffix `-s` (see `0-foundation/tone-prosody.md`) is a **toneless extrasyllabic appendix** — pronounced like English plural `-s` (`/s/` or `/z/`). It:

- Does **not** add a syllable
- Does **not** create a consonant cluster (it is an appendix, not part of the syllable nucleus/coda)
- Does **not** carry `j` or `v`
- Does **not** affect the last-3 domain or syllable count for tone purposes

### F. Schwa Epenthesis for Loanwords

When a loanword contains a consonant cluster (CC, CCC, etc.) that violates Kilor's strict no-cluster phonotactic constraint, an epenthetic schwa `e` /ə/ is inserted between the consonants to break the cluster. This rule applies systematically to all imported words:

- **Between adjacent consonants:** Insert `e` between any C₁C₂ sequence
- **Word-final clusters:** Insert `e` before the final consonant if a cluster would result
- **Multiple clusters:** Apply to each cluster independently

> **Example:** English "star" /stɑr/ → `setar` (e inserted between s-t)
> **Example:** English "spring" /sprɪŋ/ → `sepurin` (e between s-p, e between p-r, -ing→-in)
> **Example:** English "left" /left/ → `lefet` (e between f-t)

The inserted `e` is a full vowel nucleus forming its own syllable, pronounced as schwa /ə/. It carries no tone (flat mid) and does not count toward the last-3 tone domain for 3+ syllable adapted loanwords — tone markers are assigned to the adapted form following standard tone rules.

#### Loanword Exception Pipeline for Positional Rules

For loanwords and foreign terminology, positional restrictions (start-only, end-only, edge-only) may be relaxed when native Kilor phonology cannot accommodate the word. Apply these steps in order:

1. **Native mapping:** Map each sound to the closest Kilor phoneme, respecting all positional classes. For example, a word requiring /kr/ mid-word maps each to separate core consonants (`k` + `r`).

2. **Positional override:** If the native mapping produces a sound that cannot be represented with core consonants alone in the required position (e.g., /ʃ/ needed mid-word), break the positional restriction — use the single edge-only letter (`sh`) mid-word. This is rare and explicitly marked as a loanword.

3. **Schwa Epenthesis:** If consonant clusters remain that cannot be broken by positional overrides, insert epenthetic `e` as described above.

Loanwords that break positional rules must be flagged in the lexicon (e.g., `notes` field: `loanword: positional override`).

---

*End of Phonology Specification.*