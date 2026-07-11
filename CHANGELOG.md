# Changelog

Each entry is a workspace version bump (`rules/README.md`). Only changed files listed.

Format: `**file** vX.Y.Z — what changed`

---

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