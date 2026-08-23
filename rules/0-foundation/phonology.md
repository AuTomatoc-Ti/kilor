# Kilor Phonology — The Sound System

**Module:** Phonemic Inventory & Syllable Structure
**Status:** Canonical
**Last updated:** 2026-08-23
**Version:** 2.3.0
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
| `rk` | one letter | /ɹk/ | one glyph |
| `kl`, `tl`, `bl`, `ml` | one letter each | lateral-release | one glyph each |
| `kr`, `br`, `gr`, `fr`, `pr`, `sr` | one letter each | approximant-release | one glyph each |
| `qy` | one letter | /j/ | one glyph |

When a reader sees `pesha` in the ASCII transcription, it represents the Kilor letters: **p, e, s, h, a** — five separate letters. The sequence `sh` in mid-word position is never the single Kilor letter for /ʃ/; it is two distinct letters (`s` immediately followed by `h`). See §III-E for the formal disambiguation rule.

---

## III. Vowel Inventory

### A. The 7 Monophthongs (Single Vowels)

Pure, ungliding vowel sounds.

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **a** | /a/ | ah (central-low) | Spanish c**a**sa, Japanese **あ** |
| **e** | /e/ | mid-high eh | Spanish qu**e**, French ét**é** |
| **i** | /i/ | ee | mach**i**ne |
| **o** | /ɔ/ | aw | th**ough**t, d**aw**n, s**aw** |
| **u** | /u/ | oo | fl**u**te |
| **y** | /y/ | ü | German *über* |
| **ae** | /æ/ | short a | c**a**t, b**a**t |

### B. The 7 Permitted Diphthongs

Two vowels that merge into a **single syllable nucleus**. These are the **only** allowed vowel glides.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **ai** | /aɪ/ | eye | m**y** / b**uy** |
| **au** | /aʊ/ | ow | c**ow** / h**ow** |
| **ei** | /eɪ/ | ay | d**ay** / s**ay** |
| **eu** | /eʊ/ | eh-oo | Spanish n**eu**tro |
| **iu** | /i̯u/ | ee-oo glide | — |
| **oi** | /ɔɪ/ | oy | b**oy** / t**oy** |
| **ou** | /oʊ/ | oh | g**o** / sn**ow** |

---

## IV. Consonant Inventory

Kilor consonants belong to one of four positional classes. A consonant's class determines where it may appear in a word.

### A. Core Consonants (Appear Anywhere)

16 consonants that may appear word-initially, word-medially, or word-finally. Grouped by articulatory mechanics.

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
| **r** | /ɹ/ | Voiced alveolar approximant | **r**ed |
| **c** | /ts/ | Voiceless alveolar affricate (alveolar counterpart of `ch`) | pi**zz**a, Japanese **ts**u (つ), German **Z**eit |

**Dorsal & Glottal** (velar / glottis):

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **k** | /k/ | Voiceless velar plosive | s**k**y |
| **g** | /ɡ/ | Voiced velar plosive | **g**o |
| **h** | /h/ | Voiceless glottal fricative | **h**at |

**Palatal** (hard palate):

| Letter | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **qy** | /j/ | Voiced palatal approximant | **y**es, Japanese **y**a (や), Mandarin **y**ě (也) |

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

10 single-letter consonants that may appear **only at the absolute beginning of a word** (word-initial position). No vowel may precede them. Each is one continuous articulatory gesture — a single phoneme, one Kilor letter.

They fall into two families:

**Lateral-release:** The plosive releases with air escaping over the sides of the tongue. The tongue tip touches the alveolar ridge (as for /l/) during the release, giving a distinctive "spreading" sensation.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **kl** | /kˡ/ | `k` with lateral release | like `k` + brief `l` touch |
| **tl** | /tˡ/ | `t` with lateral release | like `t` + brief `l` touch |
| **bl** | /bˡ/ | `b` with lateral release | like `b` + brief `l` touch |
| **ml** | /mˡ/ | `m` with lateral release | like `m` + brief `l` touch |

**Approximant-release:** The consonant releases into a smooth, flowing English-style r-sound (/ɹ/), giving each one a European-language texture.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **kr** | /kɹ/ | `k` released into approximant r | **cr**y |
| **br** | /bɹ/ | `b` released into approximant r | **br**ight |
| **gr** | /ɡɹ/ | `g` released into approximant r | **gr**een |
| **fr** | /fɹ/ | `f` released into approximant r | **fr**ee |
| **pr** | /pɹ/ | `p` released into approximant r | **pr**oud |
| **sr** | /sɹ/ | `s` released into approximant r | S**ri** Lanka |

> **Compounding restriction:** These start-only consonants are restricted to **absolute word-initial** position. A root beginning with a start-only consonant may not appear as the second or later element in a mono-word compound (where it would become word-medial). Such combinations must use multi-word compounds instead. **Exception — Rule 2b boundary vowel-repair (general):** *any* positionally-restricted consonant (start-only, end-only, or edge-only) may appear word-medially at a compound boundary when a vowel adjoins it immediately on the side its positional class forbids — start-only/edge-only onset ← the modifier-final vowel before it; end-only/edge-only coda → the head-initial vowel after it. See `3-subsystems/compounding.md` §III Rule 2b. Roots beginning with a core consonant (see §IV-A) may appear in any position within a compound.

> **Mid-word appearance:** The sequences `kl`, `tl`, `bl`, `ml`, `kr`, `br`, `gr`, `fr`, `pr`, `sr` appearing mid-word are always two separate core consonants, never the single start-only letter. `qy` appearing mid-word is two separate core consonants (`q` + `y`), never the single Kilor letter. See §IV-E.

### D. End-Only Consonants

3 single-letter consonants that may appear **only at the absolute end of a word** (word-final position). No vowel may follow them. Each is one phoneme — one Kilor letter.

| Letters | IPA | Sound Description | English Example |
|:---|:---|:---|:---|
| **ng** | /ŋ/ | Velar nasal | si**ng** |
| **x** | /x/ | Voiceless uvular/velar fricative | Scottish Lo**ch** |
| **rk** | /ɹk/ | Approximant-velar coda | a**rk**, da**rk** |

> **Mid-word appearance:** The sequences `ng` and `rk` appearing mid-word are always two separate core consonants (`n`+`g`, `r`+`k`), never the single end-only letter. See §IV-E.

### E. Mid-Word Disambiguation Rule

When a multi-character ASCII sequence (e.g., `sh`, `ng`, `kr`, `rk`, `kl` …) appears **inside** a word — not at the absolute start or end — it is always parsed as two separate core consonants, never as the single Kilor letter. The single letter only exists at word edges.

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
| Core (§IV-A) | 16 | Anywhere (initial, medial, final) | `p, b, m, f, w, t, d, n, s, l, r, c, k, g, h, qy` |
| Edge-Only (§IV-B) | 3 | Absolute word-initial or word-final only | `sh, ch, th` |
| Start-Only (§IV-C) | 10 | Absolute word-initial only | `kl, tl, bl, ml, kr, br, gr, fr, pr, sr` |
| End-Only (§IV-D) | 3 | Absolute word-final only | `ng, x, rk` |

> **Total consonants:** 32 (16 core + 3 edge-only + 10 start-only + 3 end-only)

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

## VI. Boundary Plosive Voicing (Morphophonology)

A **boundary repair** rule complementary to the Restored Consonant Rule (`0-foundation/grammar-syntax.md` §III): where that rule handles a **vowel-final** root meeting a vowel-initial suffix, this rule handles a root ending in a **voiceless plosive** meeting a vowel-initial suffix.

### A. The Rule

When a word ending in a voiceless core plosive — `p`, `t`, or `k` (with no vowel between it and the suffix) — fuses with a **vowel-initial derivational suffix**, the root-final stop is resyllabified into the **onset** of the suffix's first syllable. It now stands **between two vowels** (`V_C_V`). In that intervocalic position the stop **voices** to its voiced counterpart:

| Root-final stop | Voiced counterpart | Archetype (root + suffix → derived) |
|:---|:---|:---|
| `p` → `b` | `kop` + `-ius` | `kopius` → `kobius` |
| `t` → `d` | `rat` + `-ia` | `ratia` → `radia` |
| `k` → `g` | `lanak` + `-ik` | `lanagik` → `lanagik` |

> The suffix is vowel-initial; the root-final stop is pulled into the suffix's first syllable (`V_C_V`), where it voices. Hypothetical `kop` + `-ius` → `kobius`, `rat` + `-ia` → `radia`, `lanak` + `-ik` → `lanagik`.

### B. Triggering Environment — Only Vowel-Initial Suffixes

Voicing fires **only** when the attached derivational suffix begins with a vowel: the existing vowel-initial suffixes `-ius`, `-eus`, `-ia`, `-ik`, `-is` — and, by definition, **any future vowel-initial suffix**. This is a broad, future-proof rule: nothing needs updating when a new vowel-initial suffix is added; it is captured automatically by the "vowel-initial" definition.

### C. Non-Triggering Environments

The rule explicitly does **not** fire in any of these:

- **Consonant-initial suffixes** (`-mae`, `-tek`, `-lu`, `-rin`, `-par`, `-wes`, `-rem`, `-rum`, `-tesy`, …) — the root-final stop stays in coda position, so no intervocalic environment arises.
- **Case suffixes** (`-ni`/`-na`, `-si`/`-sa`) — all consonant-initial; the stop remains word-final or in coda, never intervocalic.
- **The `-s` derivational appendix** — attaches directly (extrasyllabic; §V-E), no resyllabification, no voicing.
- **Multi-word compounds / derived head + head** (space-separated independent words) — the root-final stop stays word-final; no fusion, no voicing.

### D. Existing Instantiation

The rule is not new in fact — the lexicon already contains a word built by it:

> `lorrak` (root, final `k`) + `-ik` (study-of) → **`lorragik`** (linguistics, "study of language").
> The root-final `k` resyllabifies into the onset of the suffix's first syllable (…`-g-`…), voices `k→g`, and is stored as `lorragik` (`lor·rak` → `lor·rag·ik`), as already present in the DB.

### E. Neutralisation Policy

Voicing may merge a derived form with an existing word (e.g., a root-final-`g` word and its voiceless counterpart's derivation become homographs): **accept it** and rely on syntactic/contextual disambiguation — the same policy already applied to homographs arising from the Restored Consonant Rule (`0-foundation/grammar-syntax.md` §III; `3-subsystems/derivational-suffixes.md` §II-A). No prohibition rule is added. Avoiding a collision is a lexical choice during word creation, not a phonological constraint.

### F. Interaction with Other Boundary Rules

The three boundary-side effects are orthogonal and compose:

| Rule | Handles | File |
|:---|:---|:---|
| Contrastive Suffix Vowel | Vowel-class of suffix chosen by last-syllable nucleus | `0-foundation/grammar-syntax.md` §II |
| Restored Consonant | Vowel-final root + vowel-initial suffix | `0-foundation/grammar-syntax.md` §III |
| Boundary Plosive Voicing | Voiceless-plosive-final root + vowel-initial suffix | this §VI |

All three concern the comfortable seam at a morph boundary; none conflicts with the others.

---

## VII. Geminate Collapse (Morphophonology)

A boundary repair rule for mono-word fusion. Where §VI handles final voiceless stops and the Restored Consonant Rule handles vowel-vowel hiatus, this rule removes the identical-consonant overlap at a fusion boundary.

### A. The Rule

When two identical core consonants abut at the morpheme boundary of a mono-word compound or fused derivation — the first belongs to the final syllable of the first root (coda), the second to the initial consonant of the second element (onset) — the geminate collapses to a single consonant:

| Boundary | Collapsed surface |
|:---|:---|
| `...l` + `l...` | `...l...` |
| `...h` + `h...` | `...h...` |
| `...k` + `k...` | `...k...` |
| `...n` + `n...` | `...n...` |
| any identical core consonant | single instance |

### B. Triggering Environment

Collapse applies at the fusion seam of a mono-word compound or fused derivation, when both ends of the boundary are the same consonant (true geminate). The result is stored as a single orthographic letter.

### C. Non-Triggering Environments

The rule does not fire:

- Inside a bare root — underlying geminates remain legal and are never collapsed. argonna, torra, messa, lorrak, lerra, ekke, sarrok are valid native roots.
- Where the two consonants differ — no collapse.
- Multi-word compounds (space-separated) — no fusion seam.

### D. Relationship to Other Rules

Geminate collapse is a surface-simplification at the seam. It does not block or replace Rule 2/2b (positional restriction); both keep Kilor cluster-free — 2b re-syllabifies restricted consonants, collapse deletes the redundant identical twin.

### E. Existing Instantiation

The rule is already present in the lexicon:

> halise (hal + lise) — ll → l
> milise (mil + lise) — ll → l
> neihait (neih + hait) — hh → h
> shukau (shuk + kau) — kk → k

---

## VIII. V-V Glide Repair (qy)

A boundary repair for mono-word fusion: a seam that would join two vowels (front root ends in a vowel, back root begins with a vowel).

### A. The Rule

When a mono-compound seam would join two vowels (V-V), insert the glide consonant `qy` (= /j/, a multi-char core consonant) as the onset of the following vowel, turning the hiatus into a smooth V-qy-V link:

| Seam | Raw | Repaired |
|:---|:---|:---|
| esa + asdo | esaasdo | esaqyasdo |
| roli + asdaito | roliasdaito | roliqyasdaito |

### B. Triggering Environment

Repair fires at the fusion seam of a mono-word compound when the first component ends in a vowel and the second begins with a vowel. The glide `qy` takes onset of the following vowel, so the seam reads as two clean syllables.

### C. Relationship to Other Rules

| Rule | Handles | File |
|:---|:---|:---|
| Restored Consonant | Vowel-final root + vowel-initial derivational suffix | 0-foundation/grammar-syntax.md §III |
| Boundary Plosive Voicing | p/t/k-final root + vowel-initial suffix | this §VI |
| Geminate Collapse | Identical-consonant boundary | this §VII |
| V-V Glide Repair | Front-vowel + back-vowel seam (mono) | this §VIII |

Where the Restored Consonant rule fixes V-V at the suffix seam by restoring an elided consonant, this rule fixes V-V at a content-compound seam by inserting `qy`. The two are complementary.

### D. Non-Triggering

External-boundary hiatus (colour prefix or emotional particle before a vowel-initial word, e.g. a-ajkora) is phonotactically legal and is NOT repaired by this rule (an optional-glottal-catch context). Multi-word compounds keep their space and do not fuse, so no repair applies.

### E. Existing Instantiation

The lexicon previously stored two V-V seams with inconsistent repair consonants (esalasdokira using -l-, rolinasdaito using -n-). Both are re-spelled with the standard `qy` glide: `esaqyasdokira`, `roliqyasdaito`. This also exposed and fixed a syllable-count bug in count_syllables, which had treated the y of the multi-char core consonant qy as a vowel in these forms.

---

*End of Phonology Specification.*


