# Kilor Word Creation Pipeline

**Module:** Word creation workflow & field-level automation rules
**Status:** Canonical
**Last updated:** 2026-07-27
**Version:** 2.3.0
**Depends on:** `0-foundation/phonology.md`, `0-foundation/tone-prosody.md`, `1-nominals/nouns-colour-prefix.md`, `1-nominals/cases.md`, `3-subsystems/derivational-compounding.md`, `data/SCHEMA.md`, `kilor/schema.py`

---

## I. Field Table — What Gets Created

Every word entry consists of these fields. The **Verdict** column encodes who handles each:

| `#` | All human/LLM judgment required |
| `*` | Fully automatable (non-LLM code) |
| `*/#` | Auto-compute first, then human/LLM confirms or overrides |
| `*?` | Auto-compute, but flag ambiguous edge cases for human review |
| `?` | Skippable on creation; added later via edit command |

| # | Field | Verdict | Who | Automation Detail |
|---|---|---|---|---|
| a | **Word form** (Kilor root/compound) | `*/#` | Human designs → AI validates | Phonotactic check + duplicate check + near-collision flag |
| b | **Meaning** (English gloss) | `#` | Human | From wordlist (`wordlist/`) or ad-hoc |
| c | **Type** (root / compound / derivation) | `#` | Human | If compound: specify component roots + pattern name |
| d | **Colour prefix** (共識 default) | `#` | completely human confirms | 7-Question Filter (`nouns-colour-prefix.md` §V) + compound head rules (`derivational-compounding.md` §V) |
| e | **Derivation mask** (NVAD) | `#` | Human | `n`, `v`, `a`, `d`, `nv`, `na`, `av`, `nva`, `nav`, `nvd`, `avd`, `nvad` |
| f | **Syllable count** | `*` | AI auto-computes | `count_syllables(form)` |
| g | **Syllable division** | `*?` | AI auto-computes → human reviews edge cases | `split_syllables(form)`; compound-boundary ambiguity flagged |
| h | **Inflections** | `*` | AI auto-generates (conditional on mask) | Only generates applicable form types; applies tone markers for 3+ syllable words |
| i | **Acc/gen forms** | `*` | AI auto-computes → stores in DB | `get_case_forms(form, mask)`; Contrastive Suffix Rule |
| H | **Sentences** (examples) | `?` | Optional: LLM drafts via `--with-examples` flag; human accepts/rejects/edits in Phase 3 | 1–3 example sentences per word; must follow grammar, tone, and lexicon constraints (§V-F). Also insertable later via `edit` command |
| j | **IPA transcription** | `*` | AI auto-computes | `to_ipa(form)` — stored in `words.ipa` column; used for pronunciation display in dictionary app |
| k | **Syllables** (stored string) | `*` | AI auto-computes | `split_syllables(form)` — stored in `words.syllables` column (e.g. `fo.ra`); IPA and division are independent computations |
| l | **Status** (word lifecycle) | `*?` | AI auto-sets → human can override | `draft` (default for new), `active`, `deprecated`, `superseded` — stored in `words.status`; `superseded_by` FK set via `edit` command |

---

## II. The 4-Phase Pipeline

### Phase 1: Human Design (all creative work in one sitting)

The human fills in the creative fields in `today.md`:

1. **Meaning** — from `wordlist/` or ad-hoc
2. **Kilor form** — invent the root or compose the compound
3. **Type** — `root`, `compound-mono`, or `compound-multi`
4. **If compound:** component roots (by form) + pattern name
5. **Derivation mask** — `n`, `v`, `a`, `nv`, etc.
6. **Colour prefix suggestion**


### Phase 2: AI Validation + Computation (one CLI command)

```
python kilor.py add today.md --dry-run
```

Runs all automated checks and computations. Outputs a summary report. If errors exist, the command stops and reports them without inserting anything.

**Validation checks (blocking errors):**

| Check | Rule Reference |
|---|---|
| Form is not empty | — |
| No `j` or `v` in bare roots | `phonology.md` §I |
| Has at least one vowel nucleus | `phonology.md` §V |
| Max 5 syllables | `phonology.md` validation |
| 1–2 syllable content roots must not end in `-s` (unless whitelisted) | `phonology.md` §V-E |
| No duplicate form in DB | — |
| Derivation mask contains only `N`, `V`, `A`, `D` characters | — |
| If compound: all component roots exist in DB | — |

**Validation warnings (non-blocking flags):**

| Flag | What It Means |
|---|---|
| Near-collision | Form is within Levenshtein distance ≤ 2 of an existing root |
| Compound boundary ambiguity | `ae`, diphthong, or vowel hiatus spans a morpheme boundary (`phonology.py:detect_syllable_ambiguities`) |

**Auto-computations (always run):**

| Computation | Function |
|---|---|
| Syllable count | `count_syllables(form)` |
| Syllable division | `split_syllables(form)` |
| Inflections (conditional) | Only for form types present in derivation mask |
| Acc/gen forms | `get_case_forms(form, mask)` |

**Optional computations (`--with-examples` flag):**

| Computation | Function |
|---|---|
| LLM sentence generation | 1–3 example sentences per word, with English translations. See §V-F for constraints. |

### Phase 3: Human Review (confirm or fix)

Human reviews the Phase 2 summary report:

- **Syllable division (boundary cases)** → confirm or specify alternative parse
- **Near-collision warnings** → decide to proceed or redesign the form
- **Inflections** → sanity-check the generated forms
- **LLM-generated sentences (if `--with-examples`)** → accept, reject, or edit each sentence. Accepted sentences are stored with `source = 'canonical'`.

If changes needed: edit `today.md`, re-run `--dry-run`. Repeat until satisfied.

### Phase 4: DB Insert

```
python kilor.py add today.md
```

Without `--dry-run`, the command inserts all validated entries:

| Table | Rows Inserted |
|---|---|
| `words` | 1 row per entry |
| `meanings` | 1+ rows (multiple glosses for polysemy) |
| `inflections` | Conditional: 1 row per applicable form type (`noun`, `verb`, `adjective`, `adverb`) |
| `compound_components` | If compound: 2+ rows linking to component roots |
| `compound_meta` | If compound: 1 row with pattern + rule_ref |
| `examples` | If `--with-examples`: 1–3 rows with `source = 'canonical'` (only human-accepted sentences are stored) |

Output: `Added 'a-fora' (fire, n). Total entries: 42.`

---

## III. today.md Template Specification

Two templates exist: **Content Word** (derivation_mask = N/V/A/D) and **Function Word** (no mask; single POS tag).

### A. Content Word Template (N/V/A/D)

For open-class roots and compounds. Meanings are split by word class — each PoS in the derivation mask gets its own meaning field. Multiple senses within the same PoS are comma-separated.

```markdown
### {english} ({domain})

| Field | Value |
|---|---|
| Kilor Form |  |
| Type | root / compound-mono / compound-multi |
| Derivation Mask (N/V/A/D) |  |
| Consensus Prefix |  |
| Meaning (N) |  |
| Meaning (V) |  |
| Meaning (A) |  |
| Meaning (D) |  |
| Notes |  |
```

**Human fills:** Kilor Form, Type, Derivation Mask, per-PoS meanings (only lines matching mask letters are required).  
**Parser behaviour:** Only non-empty per-PoS meaning fields are inserted. Each field becomes one `meanings` row with `pos = N|V|A|D`. Comma-separated senses within a field → multiple `meanings` rows with same `pos` and ascending `sort_order`.  
**AI fills during Phase 2:** Consensus Prefix (auto-suggest).  
**AI computes:** Syllable Count, Syllable Division, Inflections, ACC/GEN — these are not displayed in the template; they appear in the Phase 2 summary report and are stored directly in DB.

### B. Function Word / Closed-Class Template

For function words, pronouns, numerals, modals, and other closed-class items. Uses a single `POS` field instead of a derivation mask.

```markdown
### {english} ({domain})

| Field | Value |
|---|---|
| Kilor Form |  |
| Type | function |
| POS |  |
| Consensus Prefix | o- |
| Meaning |  |
| Notes |  |
```

**`POS` values** (from `kilor/schema.py:VALID_POS`):

| Content words | Closed-class |
|---|---|
| `N`, `V`, `A`, `D` | `PRON`, `NUM`, `CCONJ`, `SCONJ`, `ADP`, `PART`, `MODAL`, `DEM`, `Q`, `CLF`, `INTERJ`, `PROPN` |

**Parser behaviour:** `POS` is stored as `pos` on each `meanings` row. `derivation_mask` is set to `""`. `is_function_word` = 1.

### C. Compound Template (Content Word Extension)

Add the following fields to the Content Word template above:

```markdown
| Components | root1-form + root2-form |
| Pattern | Agent / Instrument / Property / Measure / Process / Result / Location / Doctrine / Capability / Without |
| Rule Ref | rules/3-subsystems/derivational-compounding.md §II-{section} |
```

**Human fills:** Kilor Form, per-PoS Meaning, Type, Derivation Mask, Components, Pattern, Rule Ref.  
**AI validates:** Component roots exist in DB.  
**AI auto-suggests:** Consensus Prefix (from compound head rules, `derivational-compounding.md` §V).

### D. Polysemy (Adding a Meaning to an Existing Word)

Use the `edit` command with a `--pos` flag:

```
python kilor.py edit existing-form --add-meaning "new gloss" --pos N
```

Inserts a new `meanings` row with the specified `pos` and incremented `sort_order` (scoped within the same `pos`).

---

## IV. Validation Rules (Detailed)

### A. Phonotactic Validation

See `kilor/phonology.py:validate_content_root()`. Blocking errors:

- Empty form
- Contains `j` or `v` (reserved for tone — `phonology.md` §I)
- No vowel nucleus
- > 5 syllables
- 1–2 syllable content root ends in `-s` and not in `S_FINAL_WHITELIST`

Non-blocking warning:
- Near-collision: form is within Levenshtein distance ≤ 2 of an existing root (threshold configurable)

### B. Derivation Mask Validation

Valid characters: `N`, `V`, `A`, `D` (case-insensitive).  
`D` (adverb) must co-occur with `A` (adjective) — standalone `D` is invalid.  
Must be non-empty.

### C. Compound Validation

- All component forms must exist in `words` table (by `form`)
- Components must be roots (`is_root = 1`) — a compound cannot itself be a component
- Start-only consonants (§IV-C of `phonology.md`) must not appear word-medially in mono-compounds — such combinations require multi-word compounds

---

## V. Auto-Computation Rules (Detailed)

### A. Colour Prefix Suggestion — 7-Question Filter

Run the ordered checklist from `nouns-colour-prefix.md` §V. The **first question that strongly resonates** dictates the suggestion.

For **compounds**, the prefix follows the semantic class of the head noun (`derivational-compounding.md` §V):

| Compound Type | Suggested Prefix |
|---|---|
| Agent (`mae`) | `a-` (living) |
| Instrument (`tek`) | `e-` (crafted) |
| Property (`lu`), Measure (`rin`), Process (`par`), Result (`param`) | `o-` (abstract) |
| Location (`pos`) | `ae-` (earth/boundary) |
| Doctrine (`isra`), Capability (`afaloi`), Without (`nara`) | `o-` (abstract) |

### B. Syllable Count

`count_syllables(form)` — counts vowel nuclei. Handles diphthongs and `ae` as single nuclei. Tone markers (`j`, `v`) and hyphen are stripped before counting.

### C. Syllable Division

`split_syllables(form)` — greedy Maximal Onset Principle parse. For mono-compounds, `detect_syllable_ambiguities()` flags `ae`/diphthong/vowel-hiatus at morpheme boundaries for human review.

### D. Inflection Generation (Conditional)

| Condition | Inflections Generated |
|---|---|
| `is_function_word = 1` | **None** |
| Mask contains `N` | `noun` form: bare root |
| Mask contains `V` | `verb` form: bare root |
| Mask contains `A` | `adjective` form: root + `-s` |
| Mask contains `D` | `adverb` form: root + `-s` |

For **3+ syllable roots**, tone markers (`j`, `v`) are applied to all inflected forms per `tone-prosody.md` before storage.

### E. Acc/Gen Forms

`get_case_forms(form, derivation_mask)` — applies the Contrastive Suffix Rule (`cases.md` §II):

- Function words: exempt → `(None, None)`
- Mask without `N`: exempt → `(None, None)`
- Pronouns: invariant reduced forms (`-n`, `-s`)
- Front vowels (`e`, `i`, `y`, `ae`, `ei`, `eu`, `iu`) → back suffixes `-na` (ACC), `-sa` (GEN)
- Back vowels (`a`, `o`, `u`, `ai`, `au`, `oi`, `ou`) → front suffixes `-ni` (ACC), `-si` (GEN)
- Multi-word compounds: suffix attaches to the last word only
- Colour prefix preserved in output but ignored for vowel selection

Computed forms are stored in the `inflections` table with `form_type` = `accusative` / `genitive`.

### F. LLM Sentence Generation (`--with-examples`)

When the `--with-examples` flag is set, the LLM generates 1–3 example sentences per word. Each sentence must satisfy all of the following constraints:

| Constraint | Rule Reference |
|---|---|
| Follow Kilor clause template (SOV word order, case markings on nouns) | `grammar-syntax.md` §I |
| Use the word's correct colour prefix on nouns (共識 default, or contextually appropriate variant) | `nouns-colour-prefix.md` §IV |
| Apply tone markers (`j`, `v`) to 3+ syllable words | `tone-prosody.md` |
| Use **only** words already present in the lexicon — no inventing new roots | — |
| Keep sentences short (3–8 words) suitable for a learner | — |
| Demonstrate the word's **primary meaning** (first gloss in `meanings`, lowest `sort_order`) | — |
| Use the word in its default colour prefix and most common grammatical role per its `derivation_mask` | — |
| Provide a literal English translation | — |

Sentences are presented in the Phase 2 summary report. During Phase 3 (Human Review), each sentence can be:

- **Accepted** → stored in `examples` with `source = 'canonical'`
- **Rejected** → discarded
- **Edited** → corrected text stored, `source = 'canonical'`

Only human-accepted sentences are committed to the DB in Phase 4. Sentences can also be added post-creation via `python kilor.py edit <form> --add-example "kilor text" "english text"`.

**When to use `--with-examples`:** recommended when the lexicon is sufficiently large (200+ words) that the LLM can compose natural sentences without being forced to overuse the few available roots. Early-stage batches may produce stilted or repetitive sentences.

---

## VI. Polysemy Policy

### Default: Merge (One Word, Multiple Meanings)

When two meanings share the same form and **at least one** of the following holds:
- The meanings are semantically related
- They can share the same `consensus_prefix` and `derivation_mask`

→ Insert one `words` row, multiple `meanings` rows with distinct `sort_order`.

Use the `edit` command to add a second meaning:
```
python kilor.py edit <form> --add-meaning "second gloss"
```

### Escape Hatch: Split (Subscript Convention)

When two meanings are genuinely unrelated AND they cannot share prefix + mask:

→ Create two `words` rows with subscripted forms: `form₁`, `form₂`.

Subscripts are metadata only — they exist to satisfy the UNIQUE constraint on `words.form`. They are not pronounced, not part of the phonology. Dictionary display strips the subscript.

This escape hatch will rarely be used in a constructed language; the lexicon is designed to avoid accidental homophones.

### Compatibility Test

To decide merge vs. split, ask:

> **Can both meanings coexist under one `consensus_prefix` and one `derivation_mask`?**

If yes → Merge. If no → Split.

---

## VII. Post-Creation: Editing Existing Words

Adding meanings, fixing prefixes, or adding examples after creation uses the `edit` command:

```
python kilor.py edit <form> --add-meaning "gloss"
python kilor.py edit <form> --set-prefix "a-"
python kilor.py edit <form> --set-mask "nv"
python kilor.py edit <form> --add-example "kilor text" "english text"
python kilor.py edit <form> --remove-example <example_id>
```

---

## VIII. Editorial Policy — When to Store Derived & Compound Words

Derivational suffixes (`-mae`, `-tek`, `-lu`, `-rin`, `-par`, `-ius`, `-eus`, `-ia`) and compounding heads (`param`, `pos`, `isra`, etc.) are **productive** — a speaker can form new words by rule. Not every rule-produced form deserves a lexicon entry. The question is the same one dictionary editors face in every language: does this word name a recognizable category, or can a speaker compute it from root + rule alone?

### Decision checklist

For any suffix-derived or compound word candidate, ask:

| # | Question | If yes → | If no → |
|---|---|---|---|
| 1 | Is the meaning **non-compositional**? (Semantic drift, idiomatic shift, cultural referent) | ✅ Store | → continue |
| 2 | Is it a **proper noun**? (Personal name, place name) | ✅ Store | → continue |
| 3 | Is it a **`-lise` word**? (Semi-productive — every coinage is intentional) | ✅ Store | → continue |
| 4 | Is it a **closed-class grammatical form**? (Pronoun collective, numeral compound) | ✅ Store | → continue |
| 5 | Does it name a **high-frequency cultural category**? (Profession, institution, common concept) | 🤔 Store | → continue |
| 6 | Is it fully transparent and not culturally anchored? | ❌ Skip | |

### By suffix/head type

| Type | Policy |
|---|---|
| **Roots** | ✅ Always store |
| **Closed-class forms** (pronouns, numerals, etc.) | ✅ Always store |
| **`-lise` words** | ✅ Store all — each coinage is a deliberate act of naming |
| **Productive suffixes** (`-mae`, `-tek`, `-lu`, `-rin`, `-par`, `-ius`, `-eus`, `-ia`) | Check list above. Default: *do not store* unless lexicalized, proper-noun, or high-frequency |
| **Multi-word compounds** (`param`, `pos`, `isra`, etc.) | Same as productive suffixes — skip transparent compounds; store culturally fixed names |
| **`-lo` / `lote` collectives** | ❌ Never store — purely computed, like Chinese 朋友們 |

### Concrete examples

| Form | Store? | Why |
|---|---|---|
| `takamae` (eater) | ❌ | Transparent agent. "Anyone who eats" — not a cultural category. |
| `misomae` (musician) | 🤔 | Names a profession. Culturally anchored — probably merits an entry. |
| `forania` (fiery) | ❌ | Transparent abundative. Computed from `fora` + `-ia`. |
| `maelise` (fate) | ✅ | Semi-productive `-lise` — meaning is existential, not compositional. |
| `auronius` (sky-like) | ❌ | Transparent similative. |
| `auronius` (personal name) | ✅ | Proper noun — culturally assigned, not computed. |
| `fora posia` (Fire Realm) | ✅ | Culturally fixed toponym — not any old "fire-place." |
| `bau pos` (bakery) | ❌ | Transparent location compound. |
| `takamae lote` (eaters, collective) | ❌ | Collective of derived agent — double computation, no special meaning. |
| `maehalo` (people) | ❌ | Purely computed collective — like 人們. |

### Cross-language parallel

| Kilor | Analog | Stored? |
|---|---|---|
| `maehalo` | Chinese 人們 | ❌ Not in dictionary |
| `kilo` | Chinese 我們 | ✅ In dictionary (closed-class pronoun) |
| `takamae` | English `eater` | ❌ Not a common dictionary entry |
| `misomae` | English `musician` | ✅ Profession earns an entry |
| `fora posia` | English `Fire Realm` (mythical) | ✅ Proper name |
| `song lote` | Chinese 朋友們 | ❌ Purely compositional |

### Recording rationale

When storing a word that passes checklist item 1–5, record the reason in the `notes` field:
- `"semantically shifted"` — meaning differs from compositional reading
- `"proper noun"` — personal/place name
- `"professional term"` — culturally anchored category
- `"high-frequency exemplar"` — core vocabulary despite transparency

This is **editorial judgment**, not an algorithmic rule. When in doubt, lean toward **not storing** — transparent derivatives cost the learner nothing to miss, and the DB stays cleaner for genuinely meaningful entries.

---

## IX. Known Infrastructure Gaps

Priority-ordered list of pipeline features not yet implemented (as of 2026-07-22):

| Priority | Gap | Impact |
|---|---|---|
| 1 | **Conditional inflection generation** — currently creates all 4 form types for every word | Invalid data in DB; dictionary app displays inflections that don't exist |
| 2 | **Hardcoded `consensus_prefix = "o-"`** — `add.py` never runs the 7-Question Filter | Wrong default prefixes for most concrete nouns |
| 3 | **Compound support** — `add.py` treats every entry as a bare root | Cannot insert compounds through the pipeline |
| 4 | **Edit mode** — no `edit` command exists | Cannot fix typos, add meanings, or update prefixes without raw SQL |
| 5 | **Tone markers on inflections** — 3+ syllable inflected forms are bare, no `j`/`v` applied | Inflected forms are phonologically incomplete |
| — | **Near-collision detection** — no Levenshtein-distance flagging | Duplicate-like roots may be inserted without warning |
| — | **`--with-examples` flag** — LLM sentence generation not yet wired into `add.py` Phase 2 | Example sentences can only be added post-creation via raw SQL or a future `edit` command |

---

## X. Cross-References

- **Phonotactic rules:** `0-foundation/phonology.md`
- **Tone application:** `0-foundation/tone-prosody.md`
- **7-Question Filter & colour prefix ontology:** `1-nominals/nouns-colour-prefix.md` §V
- **Compound head prefix rules:** `3-subsystems/derivational-compounding.md` §V
- **Case suffix rules (Contrastive Suffix Rule):** `1-nominals/cases.md` §II
- **DB schema reference:** `data/SCHEMA.md`
- **Validation implementation:** `kilor/phonology.py`
- **CLI commands:** `.clinerules/kilor.md` §Available CLI commands

---

*End of Word Creation Pipeline Specification.*