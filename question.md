# Kilor — Design Questions

**Last Updated:** 2026-07-23

---

## Audit: What's Already Covered (All Resolved)

### Foundation
- [x] Philosophy & 7 dual-concepts
- [x] Phonemic inventory, syllables, phonotactics, schwa epenthesis
- [x] Tone system (`j`/`v` on 3+ syllable; 1–2 syllable toneless)
- [x] SOV word order, full clause template, modifier placement, oblique PP order
- [x] NP-internal word order: `[Demo] — [Poss GEN] — [Adj] — [Noun] — [Num/Quant] — [Rel]`
- [x] Contrastive suffix rule
- [x] Compounding (mono-word vs multi-word vocab)
- [x] `-s` derivational suffix (adj/adv from bare roots)
- [x] No plural marking (except pronoun `-l-`)
- [x] No possessive suffixes (Genitive `-si`/`-sa` only)
- [x] Pronoun declension (ACC `-n`, GEN `-s`)
- [x] Demonstratives: `thin`/`tha` dual-citizenship (place noun, determiner, pronoun)
- [x] Zero-subject clauses for weather/ambient
- [x] Modal verb syntax: bare serial, modal between manner adv and verb
- [x] Intensifiers on adverbs: `wes`/`meres` precede manner adverbs identically to adjectives

### Nominals
- [x] Colour prefix ontology (7 colours → ontological classes), definiteness, 異體字 emotional override
- [x] Personal pronouns
- [x] Case suffixes (`-ni`/`-na` ACC, `-si`/`-sa` GEN) & oblique particles (`sy`, `mer`, `tilpe`, `ar`, `te`)
- [x] Passive voice via `sy`
- [x] Genitive chains (single vs. nested possessors)
- [x] Demonstratives (`thin`/`tha`)
- [x] Discourse deixis: `thin`/`tha` as propositional anaphora (see `1-nominals/demonstratives.md` §III-C)
- [x] Oblique relativization via pied-piping: `[OBLIQUE_PHRASE] kus [clause with gap]` (see `2-predication/subordination.md` §I-E)

### Predication
- [x] Coordination `ei` (and), `po` (exclusive or), `pem` (inclusive or), `pona` (XNOR), `pemna` (NOR), `amer` (but)
- [x] Conditionals: `li` (if), `bam` (then) — covers realis, hypothetical, and counterfactual via context (Chinese 如果…便/就 model)
- [x] Copula `res` & existential/possession `ero`
- [x] Existential + location: `ero` + spatial postposition per clause template (see `2-predication/copula-existential.md` §I-D)
- [x] Predicate adjective syntax: `res` + adjective form
- [x] Negation: `nar` (uniform postpositive — negates immediately preceding constituent), `na` (negative answer)
- [x] Negation scope with modals: `nar` after modal negates modal ("don't have to"); `nar` after verb negates verb ("must not")
- [x] Negation of non-verbal predicates: `ki res a-maeha nar.` / `fora res gus nar.`
- [x] Interrogatives: 8 question words (aewei, aeweisan, awei, ewei, iwei, owei, uwei, ywei), Y/N `iu`
- [x] Indirect questions (embedded interrogatives): `kus` + wh-fronting + `iu` (see `2-predication/subordination.md` §II-D)
- [x] Subordination: `kus` (relativizer/complementizer), `tu` (when), `tilpi` (before), `tilpa` (after), `shoun` (since), `mitok` (until), `aiga` (because), `hoskar` (although), `arfi` (even), `fidak` (in order to)
- [x] Reported speech: `kus` (optional) or bare juxtaposition
- [x] Reflexive `shen`, reciprocal `meshen`
- [x] Causatives: `min` (let), `mingo` (make/force)
- [x] Focus/emphasis: covered by OSV, `arfi`, `shen`, `nar` contrast (no new grammar needed)

### Subsystems
- [x] Aspect: `gin` (progressive), `ger` (perfective), `gou` (experiential)
- [x] Emotional particles
- [x] Comparatives & superlatives: `tor`, `les`, `torra`, `wetor`, `mangus`
- [x] Derivational compounding (light-noun heads: `lu`, `rin`, `par`, `param`, `tek`, `isra`, `nara`, `tow`)
- [x] Imperatives: bare verb, `sor` (suggestion), `chom` (polite request), `maug` (prohibition), `hei` (vocative)
- [x] Numerals: core 1–10, powers-of-ten, measure words, ordinals (`dir`)
- [x] Optative, desiderative, benedictive: `halise`
- [x] Temporals: day/week/month/year scale, `-saka` frequency paradigm, temporal compounds
- [x] Spatial postpositions: 12 forms via `-ne` suffix (`ikne`, `oukne`, `umne`, `rapne`, `haune`, `paune`, `hinne`, `tene`, `orane`, `meipone`, `orakne`, `inoune`); plus `tilpe` (between, standalone closed-class)
- [x] Directional / motion-path: spatial postpositions + motion verb = direction

---

## Nice-to-Have (Lower Priority — Deferred)

All items below are correctly deferred. Kilor's grammar is sufficient for Phases 1–2 (A1–A2, ~1,000 roots, ~3,500 words). Each would add nuance or naturalness but is not blocking for basic communication.

| # | Area | Phase | Explanation |
|---|---|---|---|
| 10 | Serial verb / converb constructions | 4+ | Multiple verbs chained without subordinators ("go buy eat"). Common in SOV languages; adds naturalness but not required. Many languages (English, Russian) lack this entirely. |
| 11 | Ability vs. permission distinction (`sew` vs `afaloi`) | 3 | `sew` currently covers both "can (ability)" and "may (permission)." Fine-grained distinction needs dedicated lexicon entries or a new particle. Sufficient for basic conversation. |
| 12 | Evidentiality | 5+ | Grammatical marking of information source (witnessed, hearsay, inferred). Optional in most languages — only a few families (e.g., Quechua, Turkish) require it. |
| 13 | Honorifics beyond `chom` | 4+ | Full honorific register (humble forms, elevated forms, kinship politeness). `chom` handles polite requests; a full system requires heavy cultural design work. |
| 14 | Middle voice / anticausative | 4 | Distinguishing "the door opened" (by itself) from "I opened the door" (causative). Currently both use the same bare verb; passive `sy` works for agent demotion. |
| 15 | Reduplication | 4+ | Plurality, intensity, or aspect via repetition ("big-big" = "very big"). Common in Austronesian and Sino-Tibetan but absent in most Indo-European languages. |
| 16 | Tag questions | 3 | "..., right?" / "..., isn't it?" — conversational confirmation. Can be approximated with sentence-final `iu` but a dedicated short form would improve natural dialogue. |
| 17 | Topic marking | 3+ | Dedicated topic particle (cf. Japanese `wa`, Korean `eun/neun`). Currently covered by OSV fronting + `arfi` emphasis. Full topic-comment structure is a Phase 3 feature. |

**When to revisit:** After Phase 2 (A2, ~1,000 roots). At that point, the lexicon will have enough content to test which of these gaps actually cause friction in real communication.

---

*All critical and important grammar gaps resolved as of 2026-07-23. 6 gaps from the 2026-07-22 audit closed (indirect questions, negation-modal scope, before/after/since/until, existential+location, intensifiers on adverbs, discourse deixis). Kilor is ready for lexicon expansion through Phase 2.*