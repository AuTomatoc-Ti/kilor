# Kilor — Open Design Questions

**Status:** Active — pre-Phase-1 root pipeline
**Created:** 2026-07-04
**Last Updated:** 2026-07-06

---

All resolved items have moved to their respective rule files (pronouns → `rules/foundation/pronouns.md`, articles → `rules/foundation/nouns-colour-prefix.md`, interrogative → `rules/foundation/interrogative.md`, negation → `rules/foundation/negation.md`, copula/existential → `rules/foundation/copula-existential.md`, numerals → `rules/num.md`, subordination & relativization → `rules/foundation/subordination.md`, oblique particles → `rules/foundation/cases.md` §V).

The remaining open questions below are the ones that must be resolved — or at minimum, have a firm design decision — before the mass root creation pipeline can begin in earnest. See `roadmap.md` §Grammar Gaps for priority mapping.

---

## Blocking — Must Design Before Phase 1 Root Creation

These items directly affect how roots are coined, what grammatical categories exist, and how sentences are structured. They must be resolved before the mass root creation pipeline begins.

---

### 1. ✅ Subordinate Clauses & Relativization — RESOLVED (2026-07-07)

**Moved to:** `rules/foundation/subordination.md`

**Decisions:**
- Relative clauses: postnominal, with declining relativizer `kus` (subject `kus`, object `kus-ni`, possessor `kus-si`); stackable
- Complement clauses: `kus` doubles as complementizer (same as English "that"); clause may take ACC case
- Adverbial subordination: dedicated particles `tu` (when/while), `li` (if), `aiga` (because), `hoskar` (although)
- All subordination particles are closed-class, toneless, exempt from `-s` constraint

---

### 2. ✅ Dative & Instrumental Particle Expansion — RESOLVED (2026-07-07)

**Moved to:** `rules/foundation/cases.md` §V

**Decisions:**
- `su` removed; split into `mer` (comitative: with/together) and `sy` (instrumental: by/with/using)
- Additional oblique particles: `ar` (ablative: from), `tilpe` (locative-relational: between)
- Conjunctions: `ei` (and), `po` (or), `amer` (but)
- Subordinators: `tu` (when/while), `li` (if), `aiga` (because), `hoskar` (although) — see `subordination.md`
- `te` (dative: to/for) retained unchanged

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

*End of Open Design Questions.*