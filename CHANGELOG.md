# Changelog

**Current Version:** v2.9.1
**Last Updated:** 2026-08-11
**Format:** `**file** vX.Y.Z — what changed`

> **App/frontend/database changes** are tracked in `CHANGELOG-app.md`. This file covers rules/grammar/spec and meta changes only.
> For cross-cutting changes (e.g., DB schema + frontend query), see both files with cross-references.

## Template (for next entry):

## workspace v{VERSION} — {DATE}

{One-line summary}

**Category:**
- **`file.md`** vX.Y.Z→X.Y.Z — What changed

**Validation:**
- `python kilor.py check` — ✅ All N entries pass


## workspace v2.9.1 — 2026-08-11

22 new words across 2 batches (batch 2: 11, batch 3: 11). New word families: `im-` temporal triad, `kl-` military, `sys-` politeness, `ok-` core/hub/capital. 3 new spatial `-ne` postpositions added. 5 new compound entries including derivational prefix/suffix patterns.

**Spec:**
- **`3-subsystems/spatials.md`** v1.1.1→1.2.0 — Added `fapne` (on the left), `hapne` (on the right), `bopne` (below) to spatial postposition inventory (§III).

**Validation:**
- `python kilor.py check` — ✅ 12 pre-existing errors, 0 new




## workspace v2.9.0 — 2026-08-09

10 new words added: 9 roots + 1 rename (sola -> auri).

New near-minimal-pair judgment guidance + derivational prefix collision check in the pre-pipeline brainstorm guide. Learned from the Aug 2026 batch (aufe–argoi): `srata`/`srato` (rotate/house, distance 1) was tolerable because domains differ; `kon` was changed to `kona` because it collides with the `kon-` (anti-) prefix.

**Spec:**
- **`4-meta/pre-pipeline-brainstorm.md`** v1.1.0→1.2.0 — New §VI-E "Near-Minimal-Pair Judgment" with decision rule (same domain+POS → redesign; different domain or POS → tolerate) and checklist. Added derivational prefix collision check to §VIII item 3.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new

## workspace v2.8.0 — 2026-08-09

Adopted a JSON array `Meaning` format in `today.md` to eliminate comma-splitting of glosses into redundant meaning rows. One sense per array item (`{"gloss","pos"}`); near-synonyms are grouped into a single item's gloss; legacy per-PoS fields remain supported.

**Spec:**
- **`4-meta/word-creation-pipeline.md`** v2.5.0→2.6.0 — Content-word `today.md` template + parser behaviour now use a JSON array `Meaning` field (`[{"gloss","pos"}, ...]`). Glosses are no longer comma-split; near-synonyms group into one item; legacy `Meaning (N)` etc. kept as fallback. Compound template reference updated.
- **`4-meta/pre-pipeline-brainstorm.md`** v1.0.0→1.1.0 — Rewrote today.md pitfall §VII-A (comma-splitting) into "Meaning Representation — JSON Array (no comma-splitting)".

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new

See also: CHANGELOG-app.md v2.10.0.

## workspace v2.7.0 — 2026-08-09

New pre-pipeline brainstorm guide + pipeline Phase 0. Documented the structured discussion workflow for resolving meaning/POS, root vs compound, and colour prefix from bare brainstorm entries (`{form}, {meaning}`) before filling in `today.md`.

**Spec:**
- **`4-meta/pre-pipeline-brainstorm.md`** — New file v1.0.0. Phase 0 discussion guide covering: user input format (`{form}, {meaning}`), POS decision heuristics (NVAD/NAD/NV/N patterns, tool N→V test, quality A/D rules), colour prefix patterns (7-Question Filter + family consistency override), root vs compound decision flowchart (Rule 5 upgrade, deferral rules), today.md pitfalls (comma-splitting → fragmented glosses, missing `Derivation Mask` → NULL prefix, descriptive phrase fragments), and a 6-step per-word checklist.
- **`4-meta/word-creation-pipeline.md`** v2.4.4→2.5.0 — Added Phase 0: Pre-Pipeline Brainstorm Discussion section; added companion file reference to `pre-pipeline-brainstorm.md` in header; renamed "4-Phase Pipeline" → "5-Phase Pipeline".

**Validation:**
- `python kilor.py check` — ✅ 8 pre-existing errors, 0 new


## workspace v2.6.0 — 2026-08-09

Three new derivational affixes: `ai-`/`aig-` (Re-/Again, prefix #6), `kon-` (Anti-/Opposing, prefix #7), `-rolif` (Over-/Excess, suffix #15). First POS-preserving affixes (V→V, N→N for `ai-`; A→A, N→N/A for `kon-`; V→V, A→A, N→N for `-rolif`). First V-output prefix (`ai-`, pos_mask=VN). Prefix count: 5→7; suffix count: 14→15.

**Spec:**
- **`3-subsystems/derivational-prefixes.md`** v1.1.0→1.2.0 — Added §I-F (`ai-`/`aig-`: Re-/Again, V/N→V/N, pos_mask=VN, `o-`, restored `g` before vowels) and §I-G (`kon-`: Anti-/Opposing, N/A→N/A, pos_mask=NA, `o-`, consonant-final). Updated inventory table (5→7), Restored Consonant Rule table (added `ai-` row + `kon-` note), §III-B Tone & Category (added VN pattern with tonal V forms), §IV-A Fixed Prefix (added `ai-` and `kon-` to `o-` list), §V formal register, §VI productivity (5→7).
- **`3-subsystems/derivational-suffixes.md`** v1.2.0→1.3.0 — Added §I-O (`-rolif`: Over-/Excess, V/A/N→V/A/N, POS-preserving, pos_mask=NAV, `o-`, from `rolifor`). Updated inventory table (14→15), §IV-A colour prefix table (added Over-/Excess → `o-`).
- **`4-meta/word-creation-pipeline.md`** v2.4.3→2.4.4 — Added Over-/Excess, Re-/Again, Anti- rows to colour prefix suggestion table (§V-A).
- **`README.md`** v2.3.4→2.3.5, **`.clinerules/kilor.md`** — Updated prefix count 5→7, suffix count 14→15.

**Lexicon:**
- Two new source roots: `aigan` (repetition/repeated/to repeat/repeatedly, NAVD, `o-`), `konta` (opposition/opposing/to oppose, NAV, `o-`). Existing root `rolifor` (excess/overdo/excessive/excessively, NVAD, `o-`) used for `-rolif` suffix. See also: CHANGELOG-app.md v2.7.0.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.5.0 — 2026-08-09

Two new derivational suffixes added: `-ik`/`-mik` (Study of, -ology) and `-is`/`-mlis` (Method to). Suffix count: 12 → 14. First suffix with start-only consonant restored form requiring multi-word escape (`mlis`).

**Spec:**
- **`3-subsystems/derivational-suffixes.md`** v1.1.1→1.2.0 — Added §I-M (`-ik`/`-mik`: study of, N→N, `o-`, restored `m`) and §I-N (`-is`/`-mlis`: method to, V→N, `e-`, restored `ml` blocked → multi-word for vowel-final roots). Updated inventory table (12→14), Restored Consonant Constraint table (added `-ik` and `-is` rows + `mlis` phonotactic block explanation), §IV-A Fixed Semantic-Class Prefix table (added Study of → `o-`, Method to → `e-`).
- **`0-foundation/tone-prosody.md`** v2.2.0→2.2.1 — Added `mlis` to grandfathered `-es` allomorph list (4→5 roots); added example row (`mlises` = methodical).
- **`4-meta/word-creation-pipeline.md`** v2.4.2→2.4.3 — Added Study of and Method to rows to colour prefix suggestion table (§V-A).
- **`README.md`** v2.3.3→2.3.4 — Updated suffix count 12→14.
- **`.clinerules/kilor.md`** — Updated suffix count 12→14.

**Implementation:**
- **`kilor/phonology.py`** — Added `mlis` to `S_FINAL_WHITELIST`.

**Lexicon:**
- Two new source roots: `mik` (study, N, `o-`), `mlis` (method, N, `e-`, whitelisted -s final). See also: CHANGELOG-app.md v2.6.0.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.4.0 — 2026-08-09

Two new derivational prefixes added: `doi-`/`doir-` (diminutive) and `mes-` (augmentative). Prefix count: 3 → 5. First prefix with inherit-from-base colour (`doi-`). First consonant-final prefix with no restoration needed (`mes-`).

**Spec:**
- **`3-subsystems/derivational-prefixes.md`** v1.0.0→1.1.0 — Added §I-D (`doi-`/`doir-`: diminutive, N→N, colour inherit from base, pos_mask=N) and §I-E (`mes-`: augmentative, N/A→N/A, fixed `y-`, numeric ×10¹²). Updated inventory table, Restored Consonant Rule table (added `doi-`/`doir-` row; noted `mes-` is consonant-final, no restoration needed). Updated §III-B (Tone & Category) for two pos_mask patterns (NA vs. N, Tone Omission for `doi-`). Updated §IV (Colour Prefix) split into §IV-A Fixed Prefix and §IV-B Inherit from Base. Updated §V (formal register root list) and §VI (productivity: 3→5).
- **`4-meta/word-creation-pipeline.md`** v2.4.1→2.4.2 — Added augmentative and diminutive rows to colour prefix suggestion table (§V-A).
- **`README.md`** v2.3.2→2.3.3 — Updated prefix count 3→5.
- **`.clinerules/kilor.md`** — Updated prefix count 3→5.

**Lexicon:**
- Two new source roots: `doir` (little/small/young/cute, N+A, `u-`), `meson` (trillion / huge/giant, NUM+A+N, `y-`). See also: CHANGELOG-app.md v2.5.0.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.3.0 — 2026-08-09

Three derivational prefixes added (`pi-`/`pih-`, `pa-`/`pah-`, `sefta-`/`seftah-`) plus their three source roots created in the lexicon. Prefixes follow the same morphological pattern as suffixes (shortened combining forms, Restored Consonant Rule mirror).

**Spec:**
- **`3-subsystems/derivational-prefixes.md`** v1.0.0 — New file: 3 derivational prefixes (§I A–C): `pi-`/`pih-` (temporal pre-, N→N/A), `pa-`/`pah-` (temporal post-, N→N/A), `sefta-`/`seftah-` (meta-, any→N/A). Restored Consonant Rule (§II): `h` restored before vowel-initial roots (`pihaug`, `paheli`, `seftahema`). Wordhood & tone (§III): fused single word, pos_mask=NA, co-occurrence with suffixes, start-only consonant restriction. Colour prefix `o-` (§IV). Fully productive (§VI).
- **`3-subsystems/derivational-suffixes.md`** v1.1.0→1.1.1 — Added `See also` cross-reference to prefixes file.
- **`3-subsystems/compounding.md`** v1.0.0 — Updated Depends on and companion file reference to include prefixes file; suffix count 9→12.
- **`4-meta/word-creation-pipeline.md`** v2.4.0→2.4.1 — Added `derivational-prefixes.md` to Depends on; added prefix row to colour prefix suggestion table (§V-A); updated cross-references.
- **`README.md`** v2.3.1→2.3.2 — Added prefixes to directory structure, dependency table, index. Updated suffix count 9→12.
- **`.clinerules/kilor.md`** — Added prefixes to directory structure.

**Lexicon:**
- Three new source roots: `pih` (before/prior, ADP+A, `o-`), `pah` (after/subsequent, ADP+A, `o-`), `seftah` (beyond/meta, ADP+A, `o-`). See also: CHANGELOG-app.md v2.4.0.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.2.0 — 2026-08-07

Three new derivational suffixes added: `-wes` (Collective), `-rem` (Retrospective), `-rum` (Prospective). Suffix count: 9 → 12.

**Spec:**
- **`3-subsystems/derivational-suffixes.md`** v1.0.0→1.1.0 — Added §I-J (`-wes`: things/stuff of X, N/V → N), §I-K (`-rem`: former X / that which once was, N→N / V→A / A→A), §I-L (`-rum`: neo-X / that which is yet to be, N→N / V→A / A→A). `-rem` and `-rum` are broad-domain and fully productive (unlike semi-productive `-lise`). §II-A/§II-B updated with new suffix references and phonotactic block examples. §IV-A extended: `-wes` (V-base → `e-` crafted); note added for `-rem`/`-rum` V/A → A (no colour prefix). §IV-B inherit table extended with N-base rows for all three. §I-F `-lise` description updated (no longer sole broad-domain suffix).

**Validation:**
- Docs-only — no DB/lexicon change; `python kilor.py check` unaffected.


## workspace v2.1.0 — 2026-08-07

Colour prefix evolution history documented: full diachronic chain (colour = DET → ontological classifier + renewal → emotional layer) added to the two colour-prefix/emotion specs, plus a new guide on the poetic fossil-colour device. Docs-only — no DB or lexicon changes.

**Spec:**
- **`1-nominals/nouns-colour-prefix.md`** v1.3.0→1.4.0 — New §I-A "Historical Origin — Colour, DET, and Renewal": colour term originally doubled as a determiner (origin of the name *colour prefix*); the colour sense erodes to an ontological classifier (with definiteness) while the literal hue is renewed into dedicated colour words (e.g. `awin`); the poetic/archaic resurrection of the fossil colour sense is cross-referenced to the new guide.
- **`3-subsystems/colour-emotion.md`** v2.5.0→2.6.0 — §I rewritten from "One Form, Two Roles" to "One Etymology, Multiple Layers": expanded 4-stage history (colour=DET → colour→ontology+renewal → poets add emotion as clause-head / pre-verbal register-adverb / 異體字 override → 7-emotion crystallization); cross-ref added to the new guide.

**Guide:**
- **`guide/colour-prefix-poetics.md`** — New file: the fossil-colour device (double-voicing, the `a-` vs `awin` renewal tension, and its contrast with 異體字 emotion).
- **`guide/emotional-register-translation.md`** — New file: translating/conveying colour emotional particles in target languages (pole → contextual realization; the under-translation / legitimate-rendering / over-translation 超譯 test, with a worked `u'sym maeha winar` example).
- **`guide/README.md`** v1.1.0→1.3.0 — Registered `colour-prefix-poetics.md` and `emotional-register-translation.md` (file table + "When to Read" mapping); added the previously-unlisted `phonesthemes.md` row.

**Validation:**
- Docs-only — no DB/lexicon change; `python kilor.py check` unaffected.

## workspace v2.0.0 — 2026-08-06

Phonology MAJOR revision: 14 vowels re-audited, 16 non-core consonants restructured into 2 Start-Only families (lateral-release + approximant-release), sl→sr renamed, r changed from trill /r/ to English approximant /ɹ/ for European texture, IPA tables fully rewritten. DB migration applied: 4 sl-words renamed, 405 IPA fields recomputed.

**Spec:**
- **`0-foundation/phonology.md`** v1.3.0→2.0.0 — Full rewrite.
  - Vowels: a /ɑ/→/a/, e /ɛ/→/e/, iu /ju/→/i̯u/; fixed o, eu, ae English examples.
  - Core consonants: r /r/→/ɹ/, g /g/→/ɡ/.
  - Start-Only restructured from 13 (lateral-release + trill-release with tie bars) to 10 (2 families: lateral-release /Cˡ/: kl/tl/bl/ml; approximant-release /Cɹ/: kr/br/gr/fr/pr/sr).
  - sl renamed to sr (/sɹ/), moved from lateral-release to approximant-release.
  - New core consonant: `qy` /j/ (voiced palatal approximant), multi-char core consonant. Consonant count: 34→33.
  - All tie bars removed.
  - Sound description/example audit: `c` example expanded (pizza + tsu + Zeit), `iu` example removed (no accurate English match), all ASCII fields cleared of IPA-only glyph `ɡ`.
- **`guide/phonology-texture.md`** — New file: aesthetic/texture/tone-type reference for all 31 phonemes, with design principles for word creation. Later updated with real DB-verified examples for every phoneme.
- **`guide/README.md`** v1.0.0→1.1.0 — Added phonology-texture.md entry.
- **`draft/phonology-ipa-audit.md`** — Full audit log with rationale for all 14 structural changes + type-by-type consonant review.

**Tooling:**
- **`kilor/phonology.py`** — IPA lookup tables updated to v2.0.0 mappings. `to_ipa()` now handles multi-word compounds (space-separated IPA blocks). START_ONLYS set updated (sl→sr). `_MULTICHAR_CORE = {"qy"}` for multi-char core consonant support. `split_syllables`, `syllable_positions`, `_syllable_to_ipa` all support multi-char core consonants in onset and coda positions.

**DB:**
- sl→sr rename: 4 words (slato, slo, slosaka, slote → srato, sro, srosaka, srote).
- Full IPA recomputation: 405 of 406 words updated to new phonology.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors (nous, austar components, etc.), 0 new


## workspace v1.26.0 — 2026-08-06

`-es` allomorph for s-final roots: four grandfathered 1-syllable roots ending in `s` (`fos`, `gus`, `meus`, `rius`) now take epenthetic `-es` instead of `-s` for adjective/adverb derivation, avoiding illegal `-ss` geminate. Also extended §IV-G single-category omission to 1–2 syllable words (both bare root and `-s`/`-es` forms acceptable when mask has only one NVAD letter).

**Spec:**
- **`tone-prosody.md`** v2.1.0→2.2.0 — §II-B: Added `-es` allomorph exception table. Epenthetic schwa follows existing phonology.md §V-F strategy. New roots may not end in `s`. §IV-G: Extended single-category omission scope from "3+ syllables" to "any syllable count." 1–2 syllable single-mask words now produce `[bare, inflected]` tuple (both forms optional, e.g. `meus` mask=`A`: both `meus` and `meuses`).

**Validation:**
- `python kilor.py check` — ✅ 7 pre-existing errors, 0 new

> App/DB changes tracked in `CHANGELOG-app.md` v2.2.0.

## workspace v1.25.1 — 2026-08-05

Phonestheme observation guide: documented recurring sub-morphemic patterns (water `li-`, time `roi`/`tar`/`saka`, etc.) vs. productive compound roots. No spec or DB changes.

**Guide:**
- **`guide/phonesthemes.md`** v1.0.0 — New file: 11 semantic-domain observations (water, ice, sky, mountain, fire, time, good, light, room, person/agent, ordained occurrence). Distinguishes productive roots (e.g. `fos`, `auron`, `gilan`) from sub-morphemic echoes (e.g. `li-` in *shili/wonli*, `roi` in *piroi/paroi*). Cross-linguistic parallels included.

## workspace v1.25.0 — 2026-08-05

Split `derivational-compounding.md` (572 lines) into two files: `derivational-suffixes.md` (~225 lines) and `compounding.md` (~305 lines). No content deleted — all rules, examples, and tables preserved with cross-references between companion files.

**Spec:**
- **`derivational-suffixes.md`** v1.0.0 — New file: 9 derivational suffixes (§I A–I), suffix syntax & wordhood (§II A–C), formal register (§III), colour prefix rules for suffixes (§IV A–B). Cross-references to `compounding.md` for multi-word triggers and compound head prefix rules.
- **`compounding.md`** v1.0.0 — New file: 7 multi-word compounding heads (§I A–G), multi-word compound syntax (§II), mono/multi decision rules (§III: Rules 1–7, flowchart, non-colour prefixes, modifier tone, quick reference), compound colour prefix rules (§IV). Cross-references to `derivational-suffixes.md` for suffix rules.
- **`derivational-compounding.md`** — **Deleted** (content migrated to the two new files).

**Cross-references updated (5 files):**
- **`grammar-syntax.md`** — Depends on updated, §III and §VI refs updated.
- **`pronouns.md`** — Depends on updated, 3 internal refs updated.
- **`word-creation-pipeline.md`** — Depends on updated, 6 internal refs updated.
- **`rules/README.md`** — Directory structure, quick-ref table, dependency table: 2 entries replace 1.
- **`.clinerules/kilor.md`** — File structure diagram updated.

**Validation:**
- `python kilor.py check` — ✅ 7 errors, 12 warnings (all pre-existing, 0 new)

## workspace v1.24.0 — 2026-08-05

Mono vs. multi compound formation rules codified: 7-rule priority system, non-colour prefix specification, modifier tone in multi-word compounds.

**Spec:**
- **`derivational-compounding.md`** v2.8.0→3.0.0 — Added §III-C: mono/multi decision rules for content-root compounds (Rules 1–7, flowchart, definitions), non-colour prefix specification (§III-C.3), modifier tone in multi-word compounds via Modular Stitching (§III-C.4), quick reference table (§III-C.5). §II heads now carry an upgrade note (optional mono fusion). Updated Depends on for tone-prosody.md §IV-D.

**Validation:**
- `python kilor.py check` — ✅ All entries pass

## workspace v1.23.0 — 2026-08-04

`amo`/`aiga` swapped (because ↔ again), `fru` gloss edit (flowery→floral), `argonnamae` + `argonnamae lise` added.

**Spec:**
- **`grammar-syntax.md`** v2.4.0→2.4.1 — Closed-class SSOT: `aiga` → `amo`. PATCH bump.
- **`subordination.md`** — Causal subordinator table + example sentence: `aiga` → `amo`.
- **`README.md`** — Particles quick-reference: `aiga` → `amo`.
- **`temporals.md`** — Iterative temporal table: `amo` → `aiga`.

**Validation:**
- `python kilor.py check` — ✅ 0 new errors

> **DB changes** tracked in `CHANGELOG-app.md` v2.0.4.

## workspace v1.22.0 — 2026-08-04

`-lise` suffix redefined: from "numinous life-condition" to "holistic ordained occurrence." Root `lise` redefined. All 14 compounds audited — 13 revised, 1 removed (`song lise`).

**Spec:**
- **`derivational-compounding.md`** v2.7.2→2.8.0 — §I table row 6: Domain "Life-condition" → "Ordained occurrence", Meaning column updated. §I-F rewritten: `-lise` now broad-domain ("holistic ordained occurrence"), root `lise` gloss changed to "assigned state; divine season; appointed time; providential ordering; sacred rhythm." Example table: all 13 compounds with revised glosses. Etymology note added (originated in `maelise`). MINOR bump.

**Validation:**
- `python kilor.py check` — ✅

> **DB changes** tracked in `CHANGELOG-app.md` v2.0.3.

## workspace v1.21.0 — 2026-08-03

POS mask system: replaced derivation_mask (NVAD) with auto-computed pos_mask in word creation pipeline.

**Spec:**
- **`word-creation-pipeline.md`** v2.3.0→2.4.0 — §I: replaced row e (Derivation mask, manual) with e (POS tags per meaning, manual) + e₂ (pos_mask, auto-computed from meanings via compute_pos_mask()). MODAL→V, PROPN→N, closed-class tags contribute nothing. A and D are independent (D-only pos_mask valid). §II: Phase 1 step 5 changed from "Derivation mask" to "Per-meaning POS tags". Phase 2 validation: replaced derivation mask character check with POS-in-VALID_POS check; added pos_mask auto-computation step. §III: Content Word template removed Derivation Mask row. Function Word template: is_function_word→pos_mask auto-compute. §IV-B: complete rewrite — POS tag validation + compute_pos_mask() mapping table, D-must-co-occur-with-A removed, mixed content+grammar words documented. §V-D: new inflection generation table from pos_mask via POS_TO_INFLECTION, including pos_mask derivation matrix. §IX: removed resolved gaps 1,2,5 (conditional inflection, hardcoded prefix, tone markers). Added "Resolved (v2.4.0)" section.

**Data:**
- **`data/SCHEMA.md`** — Documented pos_mask column; deprecated derivation_mask and is_function_word.

**Validation:**
- `python kilor.py check` — ✅ 5 pre-existing errors, 0 new

> **POS mask system migration** tracked in `CHANGELOG-app.md` v2.0.0.
> **Grammar badge sync, tonal inflection, compound fixes** tracked in `CHANGELOG-app.md` v2.0.2.
> **UI/UX overhaul** tracked in `CHANGELOG-app.md` v2.0.1.


## workspace v1.20.1 — 2026-08-03

20 missing consensus_prefix assigned to nouns; no spec changes.

**Data:**
- **`data/kilor.db`** — 20 nouns assigned colour prefix: asdo (o-), aultake (ae-), gor (o-), gus (a-), hostak (o-), kau (o-), kop (o-), meki (o-), mekri (o-), mug (u-), naram (o-), niba (u-), noba (u-), pusar (o-), retanik (u-), roli (o-), rolifor (o-), taka (u-), taki (u-), tle (o-).

**Validation:**
- `python kilor.py check` — 0 prefix-mask errors, 12 prefix-mask warnings (pre-existing stale prefixes on non-nouns); 35 total errors (all pre-existing noise)

> **Tooling changes** tracked in `CHANGELOG-app.md` v1.8.0.

## workspace v1.20.0 — 2026-08-02

Derivational suffix red-team audit: removed redundant -lu doublets, re-scoped -lu to concrete nouns, added -ia quality-root caveat, renamed nara→naras.

**Spec:**
- **`derivational-compounding.md`** v2.6.0→2.7.2 — Red-team audit of all 9 suffixes against NVAD collision risk. `-lu` redefined: concrete noun → abstract property (quality roots already nominalise — removed gorlu, mylu, emalu, wemlu). Added quality-root caveat to `-ia`. New canonical example: `klush lu` (courage, 血性). Renamed derivational compound form nara→naras to match existing `lira naras`. Added `-lu` row to §V-B base-dependent prefix table.

**Validation:**
- `python kilor.py check` — 35 validation errors (all pre-existing noise unrelated to this changeset)

> **DB changes** tracked in `CHANGELOG-app.md` v1.7.0.

## workspace v1.19.0 — 2026-07-27

Red-team audit: Streams B & C complete. Frontend scaling (SQL pagination, search debounce, fuzzy cap), UI features (IPA column, colour prefix legend), export flags (--lite, --no-standalone), schema indexes, documentation Quick Wins. See also: CHANGELOG-app.md v1.3.0. See `draft/red-team/STATUS.md` for full audit status.

**Spec:**
- **`word-creation-pipeline.md`** v2.2.0→2.3.0 — §I field table: added rows j (IPA), k (syllables string), l (status). Bumped version + date.

**Guide:**
- **`data/AGENT-QUICKSTART.md`** — Updated "What add.py does automatically" section with ipa/syllables/status columns. Added new auto-computed fields table. Bumped date.

**Meta:**
- **`draft/red-team/STATUS.md`** — Updated: Stream B/C marked complete, all non-human tasks done, cross-reference map updated.

**Validation:**
- `python kilor.py check` — ✅ 25 errors (all pre-existing; no new errors)

## workspace v1.18.0 — 2026-07-27

Compound backfill review: 67 flagged compounds corrected. Derivational suffix table updated — combining forms (`lu`, `rin`, `par`) replace legacy full-root references (`pireilu`, `rinok`, `chap`). Process prefix changed from `o-` to `e-`. Four suffix roots added to DB (`lu`, `rin`, `par`, `nous`). `ous` renamed to `nous`. `arrinna` deleted.

**Spec:**
- **`derivational-compounding.md`** v2.5.0→2.6.0 — §I suffix table: From Root column updated (rows 3–5: `pireilu`→`lu`, `rinok`→`rin`, `chap`→`par`). §I-E Process prefix: `o-` → `e-`. §V-A table: Process nouns moved from Abstract (`o-`) to Crafted (`e-`).

**Validation:**
- `python kilor.py check` — ✅ 25 errors (all pre-existing; no new errors from spec change)

See also: `CHANGELOG-app.md` v1.2.0 for corresponding DB changes.

## workspace v1.17.0 — 2026-07-26

Three new phonological/orthographic rules: Restored Consonant Rule for vowel-initial suffixes,
Tone Omission for single-category words, and orthographic split (hyphen vs apostrophe)
for colour prefix connectors.

**Spec:**
- **`grammar-syntax.md`** v2.3.0→2.4.0 — §III replaced: Diphthong Merge → Restored Consonant Rule. Vowel-final roots + vowel-initial suffixes (`-ius`/`-eus`/`-ia`) restore the suffix's elided first consonant (`r`/`m`/`n` from `rius`/`meus`/`nia`).
- **`derivational-compounding.md`** v2.4.1→2.5.0 — Updated examples (`foraia`→`forania`, `foraius`→`forarius`). New §III-A sub-rule: Restored Consonant Constraint for vowel-initial suffixes.
- **`tone-prosody.md`** v2.0.3→2.1.0 — New §IV-G: Tone Omission for Single-Category Words. 3+ syllable words with single-letter derivation mask may omit `j`/`v` tone markers. Applies to names, terminology, and any mask=`n`/`v`/`a`/`d` words.
- **`nouns-colour-prefix.md`** v1.2.0→1.3.0 — §II-A rewritten: two-connector system (hyphen `-` for foregrounded/共識, apostrophe `'` for emotional 異體字 and proper nouns). §IV-C proper noun apostrophe convention (`e'austareus`). §VI 異體字 examples updated.
- **`colour-emotion.md`** v2.4.0→2.5.0 — §IV-F clause-initial fusion rewritten with apostrophe fused form (`a'maeha`) and bare-noun casual variant (`a maeha`). §VII table and §VIII examples updated.
- **`numerals.md`** v1.1.0→1.1.1 — `i-lira` → `i'lira` (apostrophe for emotional override on indefinite nouns).
- **`demonstratives.md`** v1.1.0→1.1.1 — Emotional override examples (`thin e'bau`, `thin a'bau`, etc.) → apostrophe.
- **`imperatives.md`** v1.1.0→1.1.1 — Vocative `hei` colour forms (`e'hei`, `i'hei`, etc.) → apostrophe.
- **`word-creation-pipeline.md`** v2.1.0→2.2.0 — New §VIII: Editorial Policy — When to Store Derived & Compound Words. Decision checklist (6 questions), per-type policy table, cross-language parallels (Chinese 朋友們, English baker), concrete examples, and `notes`-field rationale recording convention.
- **`guide/emotional-register-usage.md`** — All 異體字 examples updated to apostrophe connector.

**Validation:**
- `python kilor.py check` — ✅ All N entries pass

## workspace v1.16.0 — 2026-07-26

Added `pos` column to `meanings` table with 15-value PoS taxonomy (N/V/A/D + PRON/NUM/CCONJ/SCONJ/ADP/PART/MODAL/DEM/Q/CLF/INTERJ/PROPN). Redesigned `today.md` templates to two-tier system (content word per-PoS fields, function word `POS` field). `edit --add-meaning` accepts `--pos` flag.

**Spec:**
- **`word-creation-pipeline.md`** v2.0.0→2.1.0 — §III templates redesigned: Content Word template (per-PoS `Meaning (N)`, `Meaning (V)`, etc.), Function Word template (`POS` field + single `Meaning`), Compound extension. §D polysemy updated with `--pos` flag. Added `kilor/schema.py` to depends-on list.
- **`schema.py`** (new metadata) — `VALID_POS` frozenset and `POS_LABELS` dict now the SSOT for valid PoS tag values used by `add.py`, `edit.py`, and frontend.

**Infrastructure:**
- **`add.py`** — New `_parse_field()` parses both template formats. Comma-separated senses → multiple meanings rows. Function words set `is_function_word=1` and skip inflection generation.
- **`edit.py`** — `--add-meaning` accepts optional `--pos N|V|A|D|...`. `sort_order` scoped within same pos.
- **`__main__.py`** — Wired `--pos` flag for CLI edit command.

**Cross-reference:** `CHANGELOG-app.md` v1.1.0 for DB migration and frontend changes.

## workspace v1.14.0 — 2026-07-25

Replaced `-l(i)-` pronoun plural infix with `-lo` fused suffix (from root `lote` "group/multitude/collective"). Extended collective marking to human nouns via multi-word `lote` (head-final compounding, Chinese 們 style). Pronoun-only closed-class fusion; human nouns use separate `lote` word; numerals and `lote` never co-occur.

**Spec:**
- **`pronouns.md`** v1.0.1→2.0.0 — Replaced `-l(i)-` infix with `-lo` suffix. New declension: `kilo/kilon/kilos` etc. Added §VI human noun collectives + `lote` etymology.
- **`grammar-syntax.md`** v2.2.6→2.3.0 — §VI rewritten from "No Plural Marking" to "Collective -lo / lote". Updated pronoun examples (lines 171, 254, 339).
- **`derivational-compounding.md`** v2.3.0→2.4.0 — Added `lote` as §II-#13 multi-word compounding head. Added §II-G subsection with full specification.
- **`spatials.md`** v1.1.1→1.1.2 — Updated pronoun genitive forms.
- **`subordination.md`** v2.5.0→2.6.0 — Updated reflexive/reciprocal pronoun examples.
- **`comparatives.md`** v1.1.1→1.1.2 — Updated example sentence.
- **`README.md`** v2.3.1→2.3.2 — Updated pronoun table in summary.
- **`guide/emotional-register-usage.md`** — Updated `sil`→`silo`.

**Code:**
- **`phonology.py`** — Updated `_PRONOUN_ACC_GEN` dict (`kilo/kilon/kilos` etc.).
- **`db.js`** — Updated `_PRONOUN_ACC_GEN` object in dictionary frontend case-form generator.

**DB:**
- Added 1 new root: `lote` (section A, gloss "group / multitude / collective", mask N, prefix a-).
- Deleted 12 old pronoun forms (`kil/til/sil/nil` + ACC/GEN variants).
- Inserted 12 new pronoun forms (`kilo/tilo/silo/nilo` + ACC/GEN variants).
- Rebuilt DB schema (fixed FK references from broken section removal migration).

**Clarification (2026-07-26):** Bare human roots that have no prior derivational suffix and no phonotactic block now fuse `-lo` directly (e.g., `maehalo`, `mamaelo`, `famaelo`), not just multi-word `lote`. The three blockers (one-suffix-per-word, phonotactic block, semantic concreteness) are conditions, not absolutes — when none apply, fusion is the preferred form.

**Validation:**
- `python kilor.py check` — ✅ All entries pass (near-collision warnings only)

## workspace v1.13.0 — 2026-07-25

Removed section classification (1–8) from the lexicon. Section was a semantic-domain label that required human judgment during word creation but provided minimal value — the colour prefix system already provides ontological classification. Removed from DB writes/reads, API, dictionary UI, and all documentation. Polysemy merge/split test now uses only prefix + mask.

**Meta:**
- **`word-creation-pipeline.md`** v1.1.0→2.0.0 — Removed field `c` (Section) from field table, Phase 1 steps, and both templates. Updated polysemy compatibility test to use only prefix + mask. MAJOR bump (structural change).
- **`section-taxonomy.md`** — Deleted (82 lines, no remaining consumers).
- **`rules/README.md`** v2.3.1→2.3.2 — Removed `section-taxonomy.md` from directory structure and dependency table. PATCH bump.

**DB:**
- **`kilor/schema.py`** — Removed `SECTION_LABELS` dict and `idx_words_section` index.
- **`kilor/commands/add.py`** — Removed `SECTION_MAP` dict and `section` from INSERT.
- **`kilor/commands/migrate.py`** — Removed `section` from INSERT statements.
- **`kilor/commands/status.py`** — Removed "By Section" output section.
- **`kilor/commands/export.py`** — Removed `section` from CSV export, dictionary data export, and inline HTML fallback (section filter dropdown + grouped rendering).
- **`kilor/api.py`** — Removed `section` from `_word_to_dict()`, `?section=` query param, and `by_section` from `/api/status`.
- **`kilor/tests/test_api_syllables.py`** — Removed `section` from test schema.

**Dictionary:**
- **`kilor/dictionary/src/db.js`** — Removed `section` from SELECT columns, filter logic, sort cases, and `enrichEntry()`.
- **`kilor/dictionary/src/components/FilterPanel.jsx`** — Removed "Section" column and `SECTION_OPTIONS`.
- **`kilor/dictionary/src/components/TableView.jsx`** — Removed "§" column from table header/body and "Section" from `DetailPanel`.
- **`kilor/dictionary/src/App.jsx`** — Removed `filterSections` state and prop passing.
- **`kilor/dictionary/src/App.test.jsx`** — Removed section filter test.

**Docs:**
- **`data/AI-GUIDE.md`** — Removed §5 (Section Map) and `section` from code examples.
- **`data/AGENT-QUICKSTART.md`** — Removed section table, tiebreak rule, `section` from code examples, validation checklist, schema table, and `?section=` curl example.
- **`data/SCHEMA.md`** — Removed `section` column from `words` table and `idx_words_section` from indexes.
- **`data/schema.json`** — Removed `section` column, `idx_words_section` index, and `section_labels` top-level key.
- **`data/README.md`** — Removed "filter by section" from dictionary description and "section" from SSOT list.

**Validation:**
- `python kilor.py check` — ✅ All N entries pass

## workspace v1.12.0 — 2026-07-25

Added abundative suffix `-ia`/`nia` ("full of X") as fully productive noun-derived suffix, and `posia` as new multi-word compounding head ("land/realm of X"). Restructured colour prefix rules (§V) into two tiers: fixed semantic-class (for verb/adj derivations) and base-inheritance (for noun-derived suffixes).

**Subsystems:**
- **`derivational-compounding.md`** v2.2.0→2.3.0 — Added suffix 9 (`-ia` from `nia`, Abundative) to Table I. Added §I-I (Abundative) with examples, base-prefix inheritance, phonotactic-block multi-word form `nia`, and contrast with `-ius`. Added `posia` to Table II as compounding head #12. Added §II-F (Realm/Land). Restructured §V into §V-A (fixed semantic-class) and §V-B (base-dependent — inherit from noun). Updated phonotactic constraint to include `-ia`. Fixed all examples to use existing DB roots (`fora` for fire, `fos` for ice, `auron` for sky).

**DB:**
- **`data/kilor.db`** — 2 new entries: `nia` (abundance, fullness; o-; section 7) and `posia` (land, realm, domain; ae-; section 6). Both are content roots. `posia` prefix corrected post-insert via `edit --set-prefix ae-`.

**Draft:**
- **`draft/future-suffix-ideas.md`** — Recorded adoption of `-ia`/`nia` (abundative) and `posia` (realm/land). Struck `riel` as superseded by `posia`. Updated productive suffix list and prefix inheritance notes.

**Validation:**
- `python kilor.py check` — ✅ All 390 entries pass (1 near-collision: ema vs nia)

## workspace v1.11.0 — 2026-07-25

Added two new derivational suffixes: `-ius` (similative: -like/-ish) and `-eus` (relational: type of / from / belongs to). Both are fully productive 1-syllable suffixes inheriting the base noun's colour prefix. Nine new lexicon entries including source roots `rius` and `meus`, compound `austar` (dusk sky), and six suffix-derived examples.

**Subsystems:**
- **`derivational-compounding.md`** v2.1.0→2.2.0 — Added suffixes 7–8 to Table I (`-ius` from `rius`, `-eus` from `meus`). Added §I-G (Similative) and §I-H (Relational) with examples, base-prefix inheritance rule, and phonotactic-block multi-word variants. Added "Base-dependent — Inherits from base" row to §V colour prefix table. Updated phonotactic constraint wording to include all suffixes. Noted person/place name usage.
- **`rules/README.md`** v2.3.0→2.3.1 — Added `-ius` and `-eus` to Case Suffixes & Tone Markers quick reference.

**DB Migration:**
- **`data/kilor.db`** — 9 new entries: 3 roots (`rius`, `meus`, `austar`) + 6 suffix-derived compounds (`auronius`, `auroneus`, `song rius`, `song meus`, `austarius`, `austareus`). Prefixes: `o-` for `rius`, `ae-` for `meus`, `i-` for sky-derived, `a-` for friend-derived. Multi-word forms for `song` compounds due to phonotactic block (`ng`).

**Code:**
- **`kilor/phonology.py`** — Whitelisted `rius` and `meus` in `S_FINAL_WHITELIST` (1-syllable -s final roots).
- **`kilor/commands/add.py`** — Added `is_compound` detection for multi-word forms to prevent false -s validation errors.

**Draft:**
- **`draft/today.md`** — 2026-07-25 batch (9 entries).
- **`draft/future-suffix-ideas.md`** — New: captured deferred suffix/compounding directions (poetic naming heads, design principles, explored-and-rejected avenues, cross-linguistic inspirations).

**Validation:**
- `python kilor.py check` — ✅ All 388 entries pass (12 pre-existing validation artifacts from pipeline gaps; no new blocking errors).

---

[Historical entries below - DO NOT READ when writing new entry]

Derivational morphology restructure: 14 multi-word compounds migrated to mono-word suffixes; `-lise` redefined as semi-productive numinous life-condition; positional consonant constraints and one-fuse-per-word rule formalised.

**DB Migration:**
- **`data/kilor.db`** — 14 multi-word derivational compounds converted to mono-word suffix forms: 6 agent (`latif mae`→`latifmae`, `miso mae`→`misomae`, `miso maeha`→`misomaeha`, `tesak mae`→`tesakmae`, `taka mae`→`takamae`, `fei mae`→`feimae`), 2 instrument (`kup tek`→`kuptek`, `tesak tek`→`tesaktek`), 3 property (`gor lu`→`gorlu`, `my lu`→`mylu`, `wem lu`→`wemlu`), 2 measure (`shuk rin`→`shukrin`, `rali rin`→`ralirin`), 1 process (`tesak par`→`tesakpar`). `compound_type` multi→mono, `compound_meta.pattern` updated, `syl_count` recomputed, FTS rebuilt. 7 multi-word compounds unchanged (`bau pos`, `hamin pos`, `ero isra`, `afaloi taka`, `narau lira`, `lira nara`, `gilan fora`).

**Subsystems:**
- **`derivational-compounding.md`** v1.1.0→2.1.0 — Major restructure (2.0.0): renamed to Derivational Morphology; split into §I Derivational Suffixes (6 mono-word: `-mae`, `-tek`, `-lu`, `-rin`, `-par`, `-lise`) and §II Multi-Word Compounding Heads (5: `param`, `pos`, `isra`, `afaloi`, `nara`); §III split into suffix rules (colour prefix on fused word, case on end) and multi-word rules (colour prefix on head, case on head). §IV formal register retained (agent `-maeha`). Update (2.1.0): `-lise` redefined from "fate/destiny (closed set)" to "numinous life-condition (semi-productive)"; §III-A added fusion constraint (one suffix per word) and phonotactic constraint (end-only/edge-only consonant roots block fusion → multi-word); §III-B added three multi-word triggers (phonotactic block, derived stem + head, multi-syllable/concrete heads); §VI deleted (`-lise` now fills the -hood/-ship gap); `phonology.md` added to Depends on.

**Draft:**
- **`draft/lise-concepts.md`** — New: eligibility guide for `-lise` suffixation. Eligible categories: life arcs, existential states, commitments/bonds, fortunes/arcs, spiritual conditions, love/desire. Borderline cases noted (happiness, sadness, health, wisdom, courage, faith). Explicit NOT-eligible table with correct suffix cross-references.

**Validation:**
- `python kilor.py check` — ✅ All 379 entries pass (346 roots, 100 function words, 85 compounds). Positional consonant check: 0 violations.

---

## workspace v1.9.0 — 2026-07-24

Grammar gap resolution (5 issues closed): oblique relativization, aspect slot in clause template, `hei` classification, spatial postposition counts, roadmap stale paths.

**Predication:**
- **`subordination.md`** v2.4.0→2.5.0 — §I-E: New section — Oblique relativization via pied-piping. All 6 oblique types (`sy`, `mer`, `te`, `ar`, spatial `-ne`, `tilpe`) relativized by moving the entire oblique phrase before `kus`. Spatial landmarks retain GEN case. MINOR bump.

**Foundation:**
- **`grammar-syntax.md`** v2.2.4→2.2.6 — §I-E: Added `[Aspect]` slot between `[Verb]` and `[nar]` in full clause template (matching `aspect.md` §I). §IV-C: Reclassified `hei` as open-class content noun (mask `n` only; no `-s` derivation; colour prefixes follow 異體字 override). PATCH bumps (2).

**Meta:**
- **`question.md`** — Added `[x] Oblique relativization via pied-piping` to Predication checklist. Fixed spatial postposition count: "13 forms via `-ne` suffix (…tilpe)" → "12 forms via `-ne` suffix (…inoune); plus `tilpe` (standalone closed-class)".
- **`rules/README.md`** — Added `orakne` (across) and `inoune` (through/via) to Spatial Postpositions quick-reference table (was missing 2 of 12 entries).
- **`roadmap.md`** — Updated `Last Updated:` to 2026-07-24. Grammar Foundation table: replaced all 11 stale `rules/foundation/` paths with correct layer-qualified paths; added 9 missing domains (demonstratives, conditionals, clause combining, aspect, comparatives, imperatives, spatials, temporals, emotional particles).

---

## workspace v1.8.0 — 2026-07-23

Grammar gap resolution (6 gaps closed): indirect questions, negation-modal scope, temporal subordinators, existential+location, intensifiers on adverbs, discourse deixis. Plus 2 bug fixes (modal word order, copula-existential section labels). Total: 7 spec files modified, 2 new DB entries.

**Predication:**
- **`subordination.md`** v2.2.2→2.4.0 — §II-D: New section — Indirect questions (embedded interrogatives): wh-complements via `kus` + fronting, Y/N complements via `kus`...`iu`, alternative complements via disjunction particles, bare wh-word complements, system interactions. §III-B: Added 4 temporal subordinators — `tilpi` (before), `tilpa` (after), `shoun` (since), `mitok` (until) — with examples. MINOR bumps (2).
- **`negation.md`** v1.0.2→1.1.0 — §II-B: Replaced two-tier scope rule with **uniform postpositive rule**: `nar` always negates the immediately preceding constituent. §II-C: New section — Scope with modals — `nar` after modal negates modal ("don't have to"), `nar` after verb negates verb ("must not"). §II-D (was §II-C): Updated `iu` interaction to use uniform rule. MINOR bump.
- **`copula-existential.md`** v1.3.0→1.4.0 — §I-D: New section — Existential + location: `ero` with spatial postpositions per existing clause template. Added summary table row. Fixed section labels (I-D/I-E). MINOR bump.
- **`interrogative.md`** v1.3.0→1.3.1 — §I: Added cross-reference to `subordination.md` §II-D for embedded interrogatives. PATCH bump.

**Foundation:**
- **`grammar-syntax.md`** v2.2.1→2.2.4 — §I-E: Fixed modal word order bugs (`ki fei sew` → `ki sew fei`, `ki fei mug sew` → `ki mug sew fei`, `ki orse fei sew` → `ki orse sew fei`). §I-E Adjectives: Added intensifier-on-adverb example (`wes shuks taka`). §IV-C: Added `tilpi`, `tilpa`, `shoun`, `mitok` to closed-class particle inventory (SSOT). PATCH bumps (3).

**Nominals:**
- **`demonstratives.md`** v1.0.1→1.1.0 — §III-C: New section — Propositional anaphora: `thin`/`tha` as discourse deixis referring to clauses/facts. Clarified no `kus` redundancy. Also fixed pronoun-example word order (`thin res gor` → `thin gor res`, `tha res bono` → `tha bono res`). MINOR bump.

**Lexicon:**
- **`data/kilor.db`** — Added `shoun` (since, temporal, section 8 function word, 1-syl) and `mitok` (until, section 8 function word, 2-syl).

**Meta:**
- **`question.md`** — Added 6 resolved gaps to audit checklist. Expanded 7 deferred items with explanations (what each is, why deferred, when to revisit).
- **`rules/README.md`** — Added `interrogative.md` row to dependency table. Added `tilpi`, `tilpa`, `shoun`, `mitok` to closed-class particles quick-reference table. Bumped version to 2.3.0.

**Validation:**
- `python kilor.py check` — ✅ All 379 entries pass (346 roots, 100 function words, 85 compounds).

---

## workspace v1.7.1 — 2026-07-13

Additive adverb `orse` ("also/too/as well").

**Foundation:**
- **`grammar-syntax.md`** v2.2.0→2.2.1 — Added `orse` to closed-class particle inventory (§IV-C). Added §VIII: Additive adverb `orse` — pre-verbal `[Manner Adv]` slot, three scope positions (subject/object/verb), negation and stacking rules.

**Lexicon:**
- **`data/kilor.db`** — Added `orse` (function word, 2-syl, gloss: "also, too, as well").

**Validation:**
- `python kilor.py check` — ✅ All 318 entries pass (262 content roots, 57 function words, 73 compounds).

---

## workspace v1.7.0 — 2026-07-12

Lexicon expansion: added 73 roots from draft plus full core numeral system (0–13, scale markers, ordinal). Created `data/` directory and `compounds.json` as SSOT for compound construction metadata (73 entries: 52 mono-word + 21 multi-word). Data flow documented in `data/README.md`: `lexicon.csv` + `compounds.json` → `kilor.py dict` → dictionary output. Whitelisted `kas`/`hus`/`tus`/`rakas` as closed-class numeral `-s` exceptions.

**New:**
- **`data/` directory** — Organized lexicon data into `data/lexicon.csv`, `data/compounds.json`, `data/README.md`. Moved from project root.
- **`data/compounds.json`** — Compound dictionary (SSOT for construction metadata). 73 entries: 52 mono-word + 21 multi-word. All entries carry `meaning` (lexical cache for mono-word compounds also in lexicon.csv; sole source for multi-word compounds). All mono-word entries now have `meaning` field for self-contained dictionary lookup.
- **`data/README.md`** — Field reference for both CSV and JSON, SSOT rules, data flow diagram, update instructions.

**Lexicon:**
- **`lexicon.csv`** — Added 73 new entries:
  - **Draft roots (37):** `ma` (mom), `mamae` (mother), `fa` (dad), `famae` (father), `lorrak` (language), `wug` (dog), `mau` (cat), `onla` (leaves), `walunla` (forest), `rori` (sunrise), `aura` (celestial object), `auron` (sky), `aurok` (cosmic/space, compound: auron+rok), `auronte` (dome/canopy, compound: auron+tek), `thung` (swim), `latif` (heal/save), `argonnia` (grace/grateful, 4-syl), `miso` (music), `bop` (bottom/down), `hap` (right), `fap` (left), `arrin` (distance), `arrinna` (distant), `hak` (half), `hakdo` (1/4), `hakfoi` (1/8), `hakauk` (1/6), `dok` (double), `dokdo` (4×), `dokfoi` (8×), `dokauk` (16×), `dise` (head/facing), `diserin` (direction), `nordi` (north), `sirdi` (south), `aerdi` (east), `bordi` (west)
  - **Core numerals 0–13 (14):** `aniu` (zero), `mo` (1), `do` (2), `ro` (3), `foi` (4), `tai` (5), `slo` (6), `lai` (7), `auk` (8), `wy` (9), `gau` (10), `mai` (11), `doi` (12), `rai` (13) — closed-class
  - **Scale markers (5):** `cu` (100), `kas` (1,000), `hus` (10⁶), `tus` (10⁹), `rakas` (10¹²) — closed-class
  - **Ordinal (1):** `dir` — closed-class function word
  - **Temporal compounds (10):** `piroi` (yesterday), `paroi` (tomorrow), `imaroi` (today), `pimaroi` (day before yesterday), `pamaroi` (day after tomorrow), `pima` (earlier), `pama` (later), `esaka` (always), `slosaka` (sometimes), `nasaka` (never) — from `temporals.md` §I
  - **Nature compounds (4):** `foragilan` (volcano), `lirahup` (waterfall), `roralumi` (sunlight), `yrelumi` (moonlight)
  - **Place compounds (2):** `theprusome` (bedroom), `haminrusome` (dining room)
  - **Direction family renamed (4):** `nordis`→`nordi`, `sirdis`→`sirdi`, `aerdis`→`aerdi`, `bordis`→`bordi` (comply with 1–2 syllable `-s` constraint)

**Tooling:**
- **`kilor.py`** — Added `kas`, `hus`, `tus`, `rakas` to `S_FINAL_WHITELIST` (closed-class scale markers per `numerals.md` §II-A).

**Validation:**
- `python kilor.py check` — ✅ All 296 entries pass (246 content roots, 50 function words).

---

## workspace v1.6.0 — 2026-07-12

Grammar completeness audit (second round): resolved 9 grammar gaps — demonstratives, NP-internal word order, spatial postpositions, modal verb syntax, directional/motion-path, focus/emphasis, impersonal constructions, predicate adjective syntax, negation of non-verbal predicates. Added 2 new rule files, 10 new lexicon roots.

**New:**
- **`rules/1-nominals/demonstratives.md`** v1.0.0 — Demonstratives `thin`/`tha` as dual-citizenship words: place nouns, demonstrative determiners (pre-colour-prefix, replace colour prefix unless 異體字 override), demonstrative pronouns.
- **`rules/3-subsystems/spatials.md`** v1.1.0 — 13 spatial postpositions via invariable `-ne` suffix. `tilpe` redefined as "between" (was "at/on/in/near"). Landmark takes GEN case.

**Foundation:**
- **`grammar-syntax.md`** 2.0.2→2.2.0 — §I-A2: New section — zero-subject impersonal clauses. §I-E: Added NP-internal word order table `[Demo]—[Poss]—[Adj]—[Noun]—[Num/Quant]—[Rel]`. §I-E: Added modal verb syntax (bare serial, modal between manner adv and verb). §I-E: Updated clause template with `[Modal]` slot. `tilpe` redefined as "between" throughout. Oblique PP order updated to `sy > mer > spatial-ne/tilpe > ar > te`. Added `demonstratives.md` and `spatials.md` to Depends on.

**Nominals:**
- **`cases.md`** 1.3.2→1.4.0 — `tilpe` redefined as "between". Oblique PP order updated to include spatial postpositions. Added `spatials.md` to Depends on.

**Subsystems:**
- **`spatials.md`** 1.0.0→1.1.0 — Added `orak` (across) and `inou` (through/via) roots. MINOR bump.

**Lexicon:**
- **`lexicon.csv`** — `tilpe` meaning changed from "at/on/in/near" to "between". `thin`/`tha` notes updated for demonstrative dual-citizenship. `rap` notes updated for spatial root. `te` notes updated for dual-use (dative particle + spatial root). Added 10 new spatial roots (Category G): `ik` (in), `ouk` (out), `um` (under), `hau` (back), `pau` (front), `hin` (side), `ora` (along), `meipo` (around), `orak` (across), `inou` (through/via).

**Meta:**
- **`rules/README.md`** 2.1.0→2.2.0 — Added spatial postpositions quick-reference table, demonstratives entry in closed-class particles, updated directory structure (demonstratives.md, spatials.md), updated dependency table (3 new entries). `tilpe` description changed from "Locative-relational" to "Between".
- **`rules/4-meta/lexicon-roadmap.md`** 1.0.1→1.0.2 — Updated `tilpe` description. Added spatial postpositions reference.
- **`question.md`** — All 9 gaps documented as resolved. Audit checklist merged into single comprehensive list. Deferred items noted.

**Validation:**
- `python kilor.py check` — ✅ All 223 entries pass (193 content roots, 30 function words).

---

## workspace v1.5.0 — 2026-07-12

Grammar gap resolution: quantifier inventory, derivational compounding system (10 heads), epistemic modals.

**New:**
- **`rules/3-subsystems/derivational-compounding.md`** v1.1.0 — 10 derivational heads via light-noun compounding: agent (mae), instrument (tek), property (lu), measure (rin), process (par), result (param), location (pos), doctrine (isra), capability (afaloi), without/lack (narau/nara).
- **`rules/3-subsystems/derivational-compounding.md`** v1.0.0→v1.1.0 — Added patterns I–J (capability, without/lack). MINOR bump.

**Lexicon:**
- **`lexicon.csv`** — Added 16 entries:
  - **Quantifiers (5):** `eski` (each), `amin` (any), `naram` (none, compound: nar + amin), `meki` (most), `mekri` (few)
  - **Derivational heads (7):** `tek` (tool), `pireilu` (property), `rinok` (measure), `chap` (act), `param` (result), `lokisra` (doctrine), `isra` (idea)
  - **Epistemic modals (3):** `hostakes` (certainly/must have), `sewanes` (might/perhaps), `bamares` (would have)
  - **Without/lack (1):** `narau` (without/lack, combining form `nara`)
  - Modified: `emlu` note updated to `compound: em + lu`

**Meta:**
- **`rules/README.md`** v2.0.0→2.1.0 — Added `derivational-compounding.md` to directory structure, dependency table. Bumped date/version.

**Validation:**
- `python kilor.py check` — ✅ All 213 entries pass (183 content roots, 30 function words).


## workspace v1.4.0 — 2026-07-11

Documentation reorganization for agent-optimized readability. No content deleted — everything moved to `guide/` with cross-references, or duplicate boilerplate deduplicated. New `guide/` directory for usage guides. Cleaned 14 spec files (~13% line reduction). Updated `.clinerules/kilor.md` with agent-optimized conventions.

**New:**
- **`guide/README.md`** v1.0.0 — Index for usage guides; SSOT exemption, lighter header format
- **`guide/emotional-register-usage.md`** v1.0.0 — Extracted from `colour-emotion.md`: rhetorical devices (反諷, 輕描淡寫, 不協調, 假裝), multi-colour artistic layering (重彩), full example gallery, historical evolution narrative, blended emotions table

**Foundation:**
- **`tone-prosody.md`** v2.0.1→2.0.2 — Removed §V summary table (duplicate of §II). PATCH bump.

**Nominals:**
- **`cases.md`** v1.3.1→1.3.2 — §V-B/C/D: Replaced duplicate conjunction/subordinator/comparative particle tables with cross-references to SSOT files. PATCH bump.
- **`nouns-colour-prefix.md`** v1.1.1 (unchanged version) — §IV-B: Trimmed emotional-colouring sub-block from 10 lines to one sentence + cross-ref.

**Predication:**
- **`clause-combining.md`** v1.0.0→1.1.0 — Removed §I boilerplate, §VII summary table. MINOR bump.
- **`conditionals.md`** v1.0.0→1.1.0 — Removed §I boilerplate, §VI summary table. `**Interacts with:**` header added replacing §III prose. MINOR bump.
- **`copula-existential.md`** v1.2.1→1.3.0 — Removed duplicate §II property tables (tone info SSOT elsewhere). MINOR bump.
- **`interrogative.md`** v1.2.0→1.3.0 — Removed §I/§II-A tone boilerplate, §V summary table. MINOR bump.
- **`negation.md`** v1.0.1→1.0.2 — Removed tone note (SSOT). Added `grammar-syntax.md` to Depends on. PATCH bump.
- **`subordination.md`** v2.1.0→2.2.0 — Removed §I prose, §V interaction section (→ `**Interacts with:**` header), merged §VI summary into body. MINOR bump.

**Subsystems:**
- **`aspect.md`** v1.0.0→1.1.0 — Removed §I boilerplate, §IV interaction prose (→ `**Interacts with:**` header), §VI summary. MINOR bump.
- **`colour-emotion.md`** v2.3.0→2.4.0 — Major cleanup: §I compressed to 8 lines; §VIII (duplicate of §VII) removed; §IX example gallery moved to guide; §X rhetorical devices moved to guide; §XI artistic layering moved to guide; toneless/closed-class repetition removed from §VI-B. 523→198 lines. MINOR bump.
- **`comparatives.md`** v1.1.0→1.1.1 — Removed closed-class boilerplate. PATCH bump.
- **`imperatives.md`** v1.0.0→1.1.0 — Removed §I boilerplate, §VI interaction prose (→ `**Interacts with:**` header), §VII summary table. MINOR bump.
- **`optative.md`** v1.0.0→1.1.0 — Removed §I prose, §VI summary table. MINOR bump.

**Meta:**
- **`rules/README.md`** v1.3.0→2.0.0 — Restructured: collapsed verbose reference index into agent-friendly Quick Reference (all particles, prefixes, pronouns, question words in consolidated tables). Added `guide/` to directory structure. Added agent-optimized conventions section. MAJOR bump (structural reorganization).
- **`.clinerules/kilor.md`** — Added §9 (Usage Guides — `guide/` directory) and §10 (Agent-Optimized Conventions: closed-class SSOT, file size cap, `Interacts with` header, no summary tables in short files, tables over prose). Updated directory structure diagram to include all current files.

**Validation:**
- `python kilor.py check` — ✅ All 197 entries pass.

---

## workspace v1.3.0 — 2026-07-11

Grammar completeness audit: resolved 12 missing grammatical systems. Added 3 new rule files, 20 new lexicon entries, 1 new phonology section. Major update to subordination.md (reported speech, purpose clauses, bare serialisation, concessive/conditional/purpose particles).

**Foundation:**
- **`grammar-syntax.md`** v2.0.1→2.0.2 — §IV-C: Added 3 new closed-class particles (`bam`, `fidak`, `arfi`). Bumped version and date.
- **`phonology.md`** v1.1.0→1.2.0 — §IV-F: New section — Schwa epenthesis rule for loanword adaptation. Insert `e` between consonant clusters.

**Predication:**
- **New: `conditionals.md`** v1.0.0 — Conditional & consequential clauses: `li` (if), `bam` (then/consequential 便/就). Two patterns: `li X, bam Y` and `Y li X`. `bam` as standalone consequential connector. Interaction with negation, emotional particles, aspect.
- **`subordination.md`** v2.0.0→2.1.0 — §IV: Added `fidak` (purpose subordinator) and `arfi` (concessive intensifier) to subordinator inventory. §VI: Updated summary table with new particles. §VIII: New section — Reported speech (two strategies: `kus` + bare juxtaposition; pronoun resolution; direct quote). §IX: New section — Purpose clauses (bare serial verb default; explicit `fidak` particle). §X: New section — `kus` vs. bare serialisation decision table.

**Subsystems:**
- **New: `optative.md`** v1.0.0 — Optative, desiderative & benedictive mood via `halise` (3-syllable content root with full tone paradigm: `hajlise`/`havlise`/`halijse`/`halivse`). Three structural patterns for disambiguation. Interaction with emotional particles. Hortative cross-reference to `sor` in `imperatives.md`.

**Lexicon:**
- **`lexicon.csv`** — Added 20 entries: 3 closed-class particles (`bam`, `fidak`, `arfi`), 13 previously-uncatalogued closed-class particles (`mer`, `sy`, `ar`, `tilpe`, `ei`, `po`, `amer`, `tu`, `li`, `aiga`, `hoskar`, `kus`), 1 open-class optative root (`halise`, 3-syl, `hajlise`/`havlise`/`halijse`/`halivse`), 2 causative verbs (`min` = let, `mingo` = make/force 使/令).

**Meta:**
- **`README.md`** v1.2.0→1.3.0 — Added new files to reference index (conditionals, concessives, causatives, optative, purpose, reported speech, temporal clauses, bare serialisation), directory structure, and dependency table. Added `conditionals.md` and `optative.md` to dependency table.
- **`question.md`** — Updated: all 12 gaps from grammar completeness audit recorded as resolved. Old causatives deferred item resolved. Only topic marking remains deferred.

---

## workspace v1.2.0 — 2026-07-11

Grammar expansion: coordination, imperatives, aspect, complement clauses, reflexives/reciprocals. Added 4 new rule files, 13 new lexicon entries. Major update to subordination.md (complement clause syntax, reflexives/reciprocals).

**Foundation:**
- **`grammar-syntax.md`** v2.0.1→2.0.2 — §IV-C: Added 13 new closed-class particles (`pem`, `pona`, `pemna`, `sor`, `chom`, `maug`, `gin`, `ger`, `gou`). Noted `hei` and `shen` as open-class content roots not in closed-class exemption list.

**Nominals:**
- **`cases.md`** v1.3.1→1.3.2 — §V-B: Added `pem` (inclusive or), `pona` (xnor), `pemna` (nor) to conjunction table. Added cross-reference to `2-predication/clause-combining.md`.

**Predication:**
- **`subordination.md`** v1.0.2→2.0.0 — §III: Complement clause syntax changed to head-final pattern (`SUBJ MAIN-VERB kus [embedded clause]`). Added `kus` with non-clausal complements. Added §VII: Reflexives (`shen`) & reciprocals (`meshen`). Updated disambiguation table and negation example. Added dependency on `3-subsystems/aspect.md`.
- **New: `clause-combining.md`** v1.0.0 — Coordination & conjunction: `ei` (and), `po` (exclusive or), `pem` (inclusive or), `pona` (xnor), `pemna` (nor), `amer` (but). NP coordination, clause coordination, shared argument gapping, negation interaction, disjunction in questions.

**Subsystems:**
- **New: `imperatives.md`** v1.0.0 — 4-level imperative register system: bare verb (casual), `nar` post-verbal (negative), `sor` sentence-final (suggestion), `chom` pre-verbal (polite), `maug` pre-verbal (strong prohibition). Vocative `hei` with optional colour prefix for emotional nuance.
- **New: `aspect.md`** v1.0.0 — Optional post-verbal aspect particles: `gin` (progressive), `ger` (perfective), `gou` (experiential). Interaction with negation, temporal words, imperatives. Explicitly optional — bare verb always grammatical.

**Lexicon:**
- **`lexicon.csv`** — Added 13 entries: `pem` (inclusive or), `pona` (xnor), `pemna` (nor), `sor` (suggestion), `chom` (polite request), `maug` (strong prohibition), `gin` (progressive), `ger` (perfective), `gou` (experiential), `hei` (vocative, open-class), `shen` (reflexive, open-class), `meshen` (reciprocal, open-class).

**Meta:**
- **`README.md`** v1.1.6→1.2.0 — Added new files to reference index, directory structure, and dependency table.

**Deferred (recorded in question.md):**
- Topic marking, causatives.

---

## workspace v1.1.8 — 2026-07-11

Added 16 new lexicon entries (time roots, modals, greetings). Removed 1 entry (`rima` → `mug`). Whitelisted `aus`/`ous` as `-s`-final exceptions.

**Lexicon:**
- **`lexicon.csv`** — Removed `rima` (want/desire, replaced by `mug`). Added 16 entries: `aus` (start-of), `oug` (end), `ous` (end-of), `taroinous` (weekend, compound: taroi + ous), `faure` (5min), `tlaure` (30min), `afaloi` (ability / able to, nv), `sew` (can, v), `hostak` (must, v), `mug` (want, v), `som` (need, v), `shunle` (should, v), `chorogor` (good morning, compound: cho + roi + gor), `sarrogor` (good afternoon, compound: sar + roi + gor), `targor` (good evening, compound: tar + gor), `rokgor` (good night, compound: rok + gor).

**Tooling:**
- **`kilor.py`** — Added `'aus'`, `'ous'` to `S_FINAL_WHITELIST`.

---

## workspace v1.1.7 — 2026-07-10

Added 33 new lexicon entries (weather, time, temperature, fos-family compounds). Modified 2 existing entries. White-listed `gus`/`fos` as `-s`-final exceptions.

**Lexicon:**
- **`lexicon.csv`** — `liwat` meaning changed from "river" to "lake". Added 33 entries: `hu` (wind), `hupli` (rain), `shili` (river), `blusa` (wave), `wonli` (sea), `wonar` (ocean), `liforli` (flood), `aron` (season), `apar` (spring), `gustar` (summer), `choumar` (autumn), `fossar` (winter), `maur` (second), `faur` (minute), `tlaur` (hour), `taroi` (week), `gauroi` (ten-day), `yra` (month), `ron` (year), `gauron` (decade), `curon` (century), `gus` (hot), `fem` (cool), `fos` (ice/freeze), `fosli` (snow), `foske` (frost), `foshu` (blizzard, compound), `fosgilan` (glacier, compound), `fosblon` (avalanche, compound), `foskaera` (frozen soil, compound), `blon` (collapse), `hup` (fall), `rolifor` (excess).

**Tooling:**
- **`kilor.py`** — added `S_FINAL_WHITELIST = {'gus', 'fos'}` to `validate_content_root()`. These 1-syllable roots end in `-s` but are exceptions (noun/adj share the bare root form; the `-s` is part of the root not the derivational suffix).

---

## workspace v1.1.6 — 2026-07-10

Orthographic normalization: removed hyphens between root and case suffix (e.g., `bau-ni` → `bauni`), and fixed incorrect ACC allomorph.

**Foundation:**
- **`grammar-syntax.md`** v2.0.0→2.0.1 — §I-A: `hawu-ni`→`hawuni`. §I-E: `bau-ni`→`bauni` (2 occurrences). §II: `a-fora-si`→`a-forasi` (canonical orthography, no hyphen between root and suffix).

**Nominals:**
- **`cases.md`** v1.3.0→1.3.1 — §III-C, §V-E: `bau-ni`→`bauni` (2 occurrences).

**Predication:**
- **`copula-existential.md`** v1.2.0→1.2.1 — §VI-A: `maehana`→`maehani`. `maeha` last vowel `a` (Back) requires front ACC `-ni`, even in the invalid example.

**Subsystems:**
- **`colour-emotion.md`** v2.2.3→2.2.4 — §IV-B, §IV-C: `bau-ni`→`bauni` (3 occurrences).

---

## workspace v1.1.5 — 2026-07-10

Re-audit: 2 errors fixed in tone-prosody.md.

**Foundation:**
- **`tone-prosody.md`** v2.0.0→2.0.1 — §IV-B: Fixed `forasa` → `forasi`. `fora` last vowel `a` (Back) requires front Genitive `-si` per Contrastive Suffix Rule. §IV-D: Fixed `dinovgak` label "adj" → "adv". `v` on syllable 2 is the adverb pattern (M→L→M); the adjective pattern would use `j` on syllable 2 (`dinojgak`).

---

## workspace v1.1.4 — 2026-07-10

Rigorous cross-file audit: 1 conflict resolved + 1 example error fixed.

**Lexicon:**
- **`lexicon.csv`** — `dinogak` consensus_prefix changed from `u-` (Green) to `ae-` (Brown). Wood aligns with Brown/Earth per the 7-Question Filter in `nouns-colour-prefix.md` §V.

**Subsystems:**
- **`colour-emotion.md`** v2.2.2→2.2.3 — §IV-D: Fixed `a-solani` (star) → `ae-rusomena` (room) in two example glosses. `sola` means "star"; the intended word was "room" (`rusome`, consensus `ae-`).

---

## workspace v1.1.3 — 2026-07-10

Rigorous cross-file audit: 1 conflict + 5 example errors fixed across 5 files.

**Meta:**
- **`lexicon-roadmap.md`** v1.0.0→1.0.1 — §I-B: Updated 2-syllable tone patterns from old H(j)→L / L(v)→H to Toneless (missed in v1.1.0 architecture change). §II-A, §II-B: Replaced `j`-marked 2-syllable example words (`lujmi`, `sojla`, `aujli`) with legal toneless forms (`lumi`, `sola`, `auli`).

**Nominals:**
- **`nouns-colour-prefix.md`** v1.1.0→1.1.1 — §IV-B: Fixed `i-ro` (Blue-sadness water) → `i-lira` (ro=3, not water).

**Subsystems:**
- **`colour-emotion.md`** v2.2.1→2.2.2 — §VIII-A: Same `i-ro` → `i-lira` fix. §IV-A, §IV-D, §IX: Normalized double-hyphen case forms (`a-fora-ni` → `a-forani`, `a-maeha-ni` → `a-maehani`, `lira-ni` → `lirani`, `a-sola-ni` → `a-solani`) to match standard prefix-hyphen-root-suffix pattern in `cases.md`.

**Predication:**
- **`subordination.md`** v1.0.1→1.0.2 — §IV-C: Fixed `ki slato te kau` → `ki te slato kau` (dative `te` must precede its NP per oblique PP fixed order in `grammar-syntax.md` §I-E).

---

## workspace v1.1.2 — 2026-07-10

Tone marker placement fix: `j`/`v` must sit between nucleus and coda, not between coda and next syllable onset.

**Lexicon:**
- **`lexicon.csv`** — `aultake` noun form: `auljtake` → `aujltake`. Correct placement for syllable `aul` (V=diphthong `au`, C=`l`): `j` goes after nucleus `au` before coda `l` → `aujltake`. The old spelling `auljtake` placed `j` after the coda, which is phonotactically incorrect.

**Important phonotactic rule confirmed:**
For 3+ syllable words with `j`/`v` tone markers on a CVC syllable: the marker goes immediately after the vowel nucleus, **before** any coda consonant. Examples:
- `aul` (VC) + H = `auj` — not `aulj`
- `ar` (VC) + H = `ajr` — not `arj` (this was already correct in `ajrgonna`)
- `sin` (CVC) + H = `sijn` — correct in `ilsijnkoi`
- `din` (CVC) + H = `dijn` — correct in `dijnogak`

---

## workspace v1.1.1 — 2026-07-10

Rigorous cross-file audit follow-up: 4 grammar/lexicon errors fixed in example sentences and verb tone marker.

**Subsystems:**
- **`colour-emotion.md`** v2.2.0→2.2.1 — §IV-A: Fixed GEN `-si` → ACC `-ni` on `a-fora` in "entered the fire" example. §IV-A, §IX: Fixed passive sentence — `ae, ki bau-ni sy a-fora taka` (active with `ki` subject) → `ae, bau sy a-fora taka` (correct passive: patient NOM unmarked). §IV-B: Fixed `po` ("or") → `te` ("to" dative) in "come to the person" example. §IV-B, §IX, §X-B: Fixed `aultake` → `auvltake` (3-syllable verb tone: `v` on 1st of last-3, not 2nd). §IV-F: Fixed fusion table `aultake` → `auvltake`.
- **`lexicon.csv`** — Fixed `aultavke` → `auvltake` in verb column (tone marker `v` was on wrong syllable).

---

## workspace v1.1.0 — 2026-07-10

Major architectural change: 1–2 syllable words are now fully toneless. Bare root serves as both noun/verb; -s form serves as both adj/adv. Disambiguation via syntactic position, colour prefixes, and context. 3+ syllable tone system unchanged.

Also fixed 11 non-existent words in example sentences, 3 tone/category errors, 1 grammar rule violation (zero-copula), and added 8 new lexicon entries.

**Foundation:**
- **`tone-prosody.md`** v1.0.3→2.0.0 — §II-A: 3+ syllable tone system unchanged. §II-B: 2-syllable tone distinction removed — all 1–2 syllable words are now toneless (bare root = noun/verb, +-s = adj/adv). §III: -s redefined as single modifier marker. §IV-B: Tone Lock Rule simplified for 1–2 syllable words. §V: Summary table updated.
- **`grammar-syntax.md`** v1.3.0→2.0.0 — All example sentences: stripped `j`/`v` from 1–2 syllable words. §II: Contrastive Suffix Rule examples updated. §IV-C: Updated root constraint wording for toneless 1–2 syllables. §V-A: -s derivation reframed for single modifier role (root+s = adj/adv). §V-A: `fei` example updated (bare root = noun and verb).
- **`phonology.md`** v1.0.0→1.1.0 — §I: Narrowed `j`/`v` reserved scope to 3+ syllable words.
- **`philosophy.md`** v1.0.1→1.1.0 — §IV: Updated tonal metaphor description for toneless 1–2 syllable words. Footnote [^1] rewritten.

**Nominals:**
- **`nouns-colour-prefix.md`** v1.0.2→1.1.0 — §III: Multi-word vocab examples stripped of `j`/`v`. §IV-B: Emotional colouring examples updated.
- **`cases.md`** v1.2.0→1.3.0 — All examples: stripped `j`/`v`. §V-E: Fixed `cut` → `kup` (now in lexicon). §VI: Tone Lock Rule updated for 1–2 syllable toneless words.
- **`pronouns.md`** v1.0.0→1.0.1 — §III-A, §IV: Updated tone description (pronouns are toneless 1–2 syllable, consistent with new rule). §V-A: `lujmi` → `lumi`.

**Predication:**
- **`copula-existential.md`** v1.1.0→1.2.0 — All examples: stripped `j`/`v`. §II-B: `ero` reclassified as toneless (2-syllable closed-class). Summary table updated.
- **`negation.md`** v1.0.0→1.0.1 — All examples: `tavka` → `taka`, `fojra` → `fora`.
- **`interrogative.md`** v1.1.0→1.2.0 — §II-A, §II-D: Removed `aeweijsan` tone exception (now toneless, consistent with 1–2 syllable rule). `aeweisan` spelling (no `j`). All examples stripped of `j`/`v`.
- **`subordination.md`** v1.0.0→1.0.1 — All examples: stripped `j`/`v` from 1–2 syllable words. §IV-C: `lojsto` → `losto`, `lijra` → `lira`, `kojra` → `kora`.

**Subsystems:**
- **`colour-emotion.md`** v2.1.0→2.2.0 — Fixed 9 non-existent words in examples: `aulvtavka` → `aultake`, `sojlan`/`soujlan` → `thep`, `mekan` → `rilda`, `fen` → `taki`, `shuki` → `tle`, `dorito` → `hik`, `kilorsa` → `berat`, `aulvsojpa` → removed, `ro-ni` → `lira-ni`. Fixed zero-copula violations (`lojsto res`, `hik res`). Fixed noun/verb tone confusion (now moot with toneless 1–2 syllables). All examples stripped of `j`/`v`.
- **`comparatives.md`** v1.0.1→1.1.0 — §VI: `mevres` → `meres` (toneless). `pejres` → `peres`. Examples stripped of `j`/`v`. `rajlis` → `ralis`.
- **`numerals.md`** v1.0.1→1.1.0 — §IV: Tone section rewritten — 1–2 syllable numerals are toneless (consistent with new rule). 3+ syllable numeral compounds follow noun H→M→L. §VIII: Orthographic convention updated. Removed `dovgau` reference.
- **`temporals.md`** v1.0.0→1.0.1 — §I-A, §I-C, §I-D: Added tone notes — 2-syllable compounds toneless, 3-syllable compounds follow noun Last-3 Domain.

**Lexicon:**
- **`lexicon.csv`** — All `j`/`v` tone markers stripped from 1–2 syllable entries across all columns (noun/verb/adj/adv now identical for short words). Added 8 new entries: `fei` (fly), `thep` (sleep), `tle` (wait), `hik` (sad), `kup` (cut), `taki` (drink), `auli` (comet). Updated `rilda` notes: verb use = "speak/say". Updated `mere`/`pere` entries for toneless `meres`/`peres`.

**Meta:**
- **`README.md`** v1.0.1→1.1.0 — Version and date bump.

---

## workspace v1.0.2 — 2026-07-09

Systematic consistency audit — resolved 10 issues across 3 rounds.

**Foundation:**
- **`tone-prosody.md`** v1.0.0→1.0.3 — §III-A: Added Adj/Quality root + -s → Manner Adverb derivation; §II-B/C: Updated per-syllable tables for Quality root; §V: Summary table includes Quality root as adverb source
- **`grammar-syntax.md`** v1.1.0→1.3.0 — §I-E: Oblique PP order and clause template updated to `sy > mer > tilpe > ar > te`; §IV-C: Added `ero` to closed-class inventory (SSOT)
- **`phonology.md`** v1.0.0 — (unchanged)

**Nominals:**
- **`nouns-colour-prefix.md`** v1.0.1→1.0.2 — §II-A: Added question-word hyphenation exception (`awei` not `a-wei`)
- **`cases.md`** v1.0.0→1.2.0 — §III-C: Lexical-vs-syntactic distinction for case suffix placement on multi-word vocabs vs quantified NPs; §V-A: Oblique table reordered to `sy > mer > tilpe > ar > te`
- **`pronouns.md`** v1.0.0 — (unchanged)

**Predication:**
- **`copula-existential.md`** v1.0.0→1.1.0 — §II-B: `ero` reclassified from open-class to closed-class
- **`interrogative.md`** v1.0.0→1.1.0 — §II-B: Question-word hyphenation exemption; §II-A/V: Removed all hyphenated forms (`a-wei` → `a + wei` construction)
- **`negation.md`** v1.0.0 — (unchanged)
- **`subordination.md`** v1.0.0 — (unchanged)

**Subsystems:**
- **`numerals.md`** v1.0.0→1.0.1 — §II-A: Removed duplicated closed-class list; replaced with cross-reference to SSOT
- **`comparatives.md`** v1.0.0→1.0.1 — §VI: Fixed `mere`/`mejre` as separate roots (no implied V→N derivation)
- **`colour-emotion.md`** v2.1.0 — (unchanged)
- **`temporals.md`** v1.0.0 — (unchanged)

**Meta:**
- **`README.md`** v1.0.1→1.0.2 — Dependency table: Updated grammar-syntax.md and numerals.md entries for cross-reference change

---

## workspace v1.0.1 — 2026-07-09

- **`colour-emotion.md`** v2.1.0 — Rewrite (v2.0.0): 7 basic emotions replace abstract registers; removed particle compounding; dual-pole retained; added historical evolution §I, coverage §III, emoji-role §V. Additions (v2.1.0): §IV-F clause-initial fusion (casual shorthand); §X rhetorical uses (修辭: irony, understatement, dissonance, feigned emotion)
- **`nouns-colour-prefix.md`** v1.0.1 — Fix outdated emotion labels (passion→anger, longing→sadness); add `colour-emotion.md` to Depends on
- **`philosophy.md`** v1.0.1 — Add historical bridge note linking dual-concepts to modern emotion mapping
- **`README.md`** v1.0.1 — Update dependency table for `colour-emotion.md`

---

## workspace v1.0.0 — 2026-07-09

Initial specification. All 16 rule files at v1.0.0.