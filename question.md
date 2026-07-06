# Kilor — Open Design Questions

**Status:** Active — pre-Phase-1
**Created:** 2026-07-04
**Last Updated:** 2026-07-06

---

Resolved items moved to their respective rule files:

| # | Domain | Resolved In |
|---|--------|-------------|
| 1 | Pronoun inventory | `rules/foundation/pronouns.md` |
| 2 | Article system | `rules/foundation/nouns-colour-prefix.md` §IV (colour prefix encodes definiteness; no separate articles) |
| 4 | Interrogative structure | `rules/foundation/interrogative.md` |
| 5 | Negation | `rules/foundation/negation.md` |
| 8 | Copula & existential | `rules/foundation/copula-existential.md` |
| — | Numeral & classifier system | `rules/num.md` — base-10, 0–13 irregular, scale markers (`gau`/`cu`/`kas`/`hus`/`tus`/`rakas`), multiplicative + additive construction, no taxonomic classifiers (measure words = regular nouns), ordinal `dir`, NP order `NOUN — (MEASURE) — NUM — (ORD)` |

---

## Blocking — Must Design Before Phase 1 Root Creation

These items directly affect how roots are coined, what grammatical categories exist, and how sentences are structured. They must be resolved before the mass root creation pipeline begins.

---

### 1. Subordinate Clauses & Relativization

**Context:** No mechanism exists for embedding clauses (e.g., "the fire that burns", "I know that you came", "when/because/if").

**Roadmap:** 🔴 Critical (`roadmap.md` Grammar Gaps #2)

**Questions:**
- Relative clauses: prenominal (like Japanese), postnominal (like English), or correlative?
- Complement clauses (e.g., "I know that..."): particle, nominalization, or parataxis?
- Adverbial subordination (when, because, if): particles or conjunctions?
- How do embedded clauses interact with SOV word order and case marking?

---

### 2. Dative & Instrumental Particle Expansion

**Context:** `te` (dative: to/for) and `su` (instrumental: with/by) are reserved slots. `cases.md` §V defines them as standalone single-syllable words with flat mid-tone. It is unclear whether additional oblique particles should exist.

**Questions:**
- Will there be additional particles beyond `te` and `su`? (e.g., locative, ablative, comitative, benefactive)
- Or will all other oblique roles be handled by context + the 3-case system?
- If additional particles are added, what are they phonologically?
- Decision affects which oblique roots are needed in the lexicon (e.g., dedicated location roots vs. particle-based location).

---

### 3. Temporal Word Inventory

**Context:** Kilor uses a tense-free time expression strategy (`grammar-syntax.md` §VI). Core temporal words are needed to anchor events in time without grammatical tense.

**Roadmap:** 🟡 High (`roadmap.md` Grammar Gaps #3)

**Questions:**
- Which temporal words are roots vs. compounds? (e.g., "yesterday" = "day" + "before"?)
- Inventory: yesterday, today, tomorrow, always, never, soon, late, early, again, now, then, before, after, during
- How do temporal expressions interact with SOV word order — are they clause-initial adverbials, or can they appear in situ?

---

### 4. Comparatives & Superlatives

**Context:** No mechanism exists for "bigger", "biggest", "more beautiful than", "as big as".

**Roadmap:** 🟡 Medium (`roadmap.md` Grammar Gaps #4)

**Questions:**
- Particle-based (e.g., "X big more than Y" like Chinese 比)?
- Dedicated comparative/superlative suffixes?
- Equative constructions ("as X as Y")?
- Superlative: how to express "the biggest" — particle, word order, or context?

---

## Deferred — Can Resolve During or After Phase 1

These are lower priority. They do not block root creation and can be addressed incrementally.

---

### 5. Phonetic Root Inventory — `ae` as Prefix vs Monophthong

**Context:** `ae` is both a 7-monophthong vowel (/æ/) in `phonology.md` and a colour prefix (`ae-` for Brown). It is also listed in the Front/Bright vowel class for harmony purposes. The two-letter representation is unambiguous in isolation but could create parsing issues at word boundaries.

**Questions:**
- Could `ae` at word start ever be ambiguous between "Brown prefix" vs "word beginning with /æ/"?
- Is this a theoretical concern or worth addressing now?
- Potential resolution: if all roots beginning with /æ/ are prohibited (phonotactic constraint), the ambiguity vanishes. Worth codifying?

---

### 6. Passive Voice or Equivalent

**Context:** No passive construction is defined.

**Roadmap:** 🟢 Low (`roadmap.md` Grammar Gaps #5)

**Questions:**
- Can OSV word order + mandatory case marking handle all passive-like needs?
- Or is a dedicated passive construction needed for agent-demotion (e.g., "the fire was eaten" without specifying by whom)?
- If passive exists, how is it formed — particle, word order, or verbal morphology?

---

## General Design Philosophy (Settled de facto)

These questions were posed when little grammar existed. The completed rule files now answer them implicitly:

| Question | De Facto Answer |
|----------|-----------------|
| **Simplicity vs expressiveness** | 6,000-root target → approaching Esperanto-level expressiveness, not Toki Pona minimalism. Full grammatical toolkit: 3 cases, 7-colour ontology, interrogative, negation, copula/existential, planned subordination |
| **Naturalism vs regularity** | Hybrid: pronouns are a closed-class irregular paradigm (naturalistic); tone system is fully regular; colour prefix is fluid/contextual. Irregularity is intentional where natural languages have it — regularity everywhere else |
| **Priority order of remaining questions** | #1 Subordination → #2 Particles → #3 Temporal words → #4 Comparatives → #5 `ae` → #6 Passive (see Blocking section above) |

---

*End of Open Design Questions.*