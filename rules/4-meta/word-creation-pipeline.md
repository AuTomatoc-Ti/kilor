# Kilor Word Creation Pipeline

**Module:** Word creation workflow & field-level automation rules
**Status:** Canonical
**Last updated:** 2026-08-23
**Version:** 2.7.0
**Depends on:** `0-foundation/phonology.md`, `0-foundation/tone-prosody.md`, `1-nominals/nouns-colour-prefix.md`, `1-nominals/cases.md`, `3-subsystems/derivational-suffixes.md`, `3-subsystems/derivational-prefixes.md`, `3-subsystems/compounding.md`, `data/SCHEMA.md`, `kilor/schema.py`

**Companion file:** `4-meta/pre-pipeline-brainstorm.md` — Phase 0 discussion guide for resolving meaning/POS, root vs compound, and colour prefix from bare brainstorm entries before filling in `today.md`. Read this first when starting from brainstorm input.

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
| d | **Colour prefix** (共識 default) | `#` | completely human confirms | 7-Question Filter (`nouns-colour-prefix.md` §V) + compound head rules (`compounding.md` §IV, `derivational-suffixes.md` §IV) |
| e | **POS tags per meaning** | `#` | Human | Each meaning line carries a POS tag (`N`, `V`, `A`, `D` for content words; closed-class tags from `VALID_POS` for function words per §III-B). Multiple PoS senses → use separate `Meaning (N)`, `Meaning (V)`, etc. fields. |
| e₂ | **`pos_mask`** (aggregate NVAD) | `*` | AI auto-computes | `compute_pos_mask(meanings)` — derives NVAD from per-meaning POS tags. Maps MODAL→V, PROPN→N; closed-class tags (PRON, NUM, PART, etc.) contribute nothing. Empty (`""`) for grammar-only words. |
| f | **Syllable count** | `*` | AI auto-computes | `count_syllables(form)` |
| g | **Syllable division** | `*?` | AI auto-computes → human reviews edge cases | `split_syllables(form)`; compound-boundary ambiguity flagged |
| h | **Inflections** | `*` | AI auto-generates from `pos_mask` | Uses `POS_TO_INFLECTION` mapping (N→noun, V→verb, A→adjective, D→adverb, MODAL→verb, PROPN→noun); closed-class→none. Applies tone markers for 3+ syllable words. A and D are independent (no forced co-occurrence). |
| i | **Acc/gen forms** | `*` | AI auto-computes → stores in DB | `get_case_forms(form, mask)`; Contrastive Suffix Rule |
| H | **Sentences** (examples) | `?` | Optional: LLM drafts via `--with-examples` flag; human accepts/rejects/edits in Phase 3 | 1–3 example sentences per word; must follow grammar, tone, and lexicon constraints (§V-F). Also insertable later via `edit` command |
| j | **IPA transcription** | `*` | AI auto-computes | `to_ipa(form)` — stored in `words.ipa` column; used for pronunciation display in dictionary app |
| k | **Syllables** (stored string) | `*` | AI auto-computes | `split_syllables(form)` — stored in `words.syllables` column (e.g. `fo.ra`); IPA and division are independent computations |
| l | **Status** (word lifecycle) | `*?` | AI auto-sets → human can override | `draft` (default for new), `active`, `deprecated`, `superseded` — stored in `words.status`; `superseded_by` FK set via `edit` command |

---

## II. The 5-Phase Pipeline

### Phase 0: Pre-Pipeline Brainstorm Discussion

When starting from bare brainstorm entries (`{form}, {meaning}`), run through `4-meta/pre-pipeline-brainstorm.md` to resolve:

1. **Meaning & POS expansion** — what NVAD senses extend from the brief meaning
2. **Root vs compound** — bare root, or compound of existing roots; defer if components missing
3. **Colour prefix** — 7-Question Filter + family consistency check

Discuss **one word at a time** with the human. Only proceed to Phase 1 after all three dimensions are locked.

### Phase 1: Human Design (all creative work in one sitting)

The human fills in the creative fields in `today.md`:

1. **Meaning** — from `wordlist/` or ad-hoc
2. **Kilor form** — invent the root or compose the compound
3. **Type** — `root`, `compound-mono`, or `compound-multi`
4. **If compound:** component roots (by form) + pattern name
5. **Per-meaning POS tags** — fill `Meaning (N)`, `Meaning (V)`, `Meaning (A)`, `Meaning (D)` fields corresponding to the word's grammatical roles. For function words, use the `POS` field with a closed-class tag (PRON, NUM, PART, MODAL, etc.).
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
| POS tags per meaning are in `VALID_POS` set (`kilor/schema.py`) | — |
| If compound: all component roots exist in DB | — |
| If a voiceless-plosive-final root (`p`/`t`/`k`) takes a vowel-initial suffix, the fused form must voice the root-final stop (`p→b`, `t→d`, `k→g`) | `phonology.md` §VI |

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
| `pos_mask` | `compute_pos_mask(meanings)` — aggregate NVAD from per-meaning POS tags |
| Inflections (from `pos_mask`) | `POS_TO_INFLECTION` mapping; tone markers for 3+ syllable words |
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
| `words` | 1 row per entry (includes auto-computed `pos_mask`) |
| `meanings` | 1+ rows (multiple glosses for polysemy, each with `pos` tag) |
| `inflections` | Conditional: 1 row per applicable form type (`noun`, `verb`, `adjective`, `adverb`), generated from `pos_mask` |
| `compound_components` | If compound: 2+ rows linking to component roots |
| `compound_meta` | If compound: 1 row with pattern + rule_ref |
| `examples` | If `--with-examples`: 1–3 rows with `source = 'canonical'` (only human-accepted sentences are stored) |

Output: `Added 'a-fora' (fire, n). Total entries: 42.`

---

## III. today.md Template Specification

Two templates exist: **Content Word** and **Function Word / Closed-Class**.

### A. Content Word Template

For open-class roots and compounds. Meanings are split by word class — each PoS gets its own meaning field. Multiple senses within the same PoS are comma-separated.

```markdown
### {english} ({domain})

| Field | Value |
|---|---|
| Kilor Form |  |
| Type | root / compound-mono / compound-multi |
| Consensus Prefix |  |
| Meaning | [{gloss, pos}, ...] |
| Notes |  |
```

**Human fills:** Kilor Form, Type, the `Meaning` array. Each array item is **one distinct sense** tagged with an explicit `pos` (N/V/A/D). Group near-synonyms into a **single item's `gloss`** rather than splitting them (e.g. `{"gloss": "to lance, pierce", "pos": "V"}`).  
**Parser behaviour:** The `Meaning` field is parsed as a JSON array of `{"gloss": ..., "pos": ...}` objects. Each item becomes one `meanings` row with that `pos` and ascending `sort_order` (scoped per `pos`). **Glosses are NOT comma-split** — a comma inside a `gloss` is preserved as part of that single sense. `pos` must be in `VALID_POS`. The legacy per-PoS fields (`Meaning (N)`, etc.) remain supported for backward compatibility. `pos_mask` is auto-computed by `compute_pos_mask()` from the aggregate POS tags.  
**AI fills during Phase 2:** Consensus Prefix (auto-suggest).  
**AI computes:** `pos_mask`, Syllable Count, Syllable Division, Inflections, ACC/GEN — these are not displayed in the template; they appear in the Phase 2 summary report and are stored directly in DB.

### B. Function Word / Closed-Class Template

For function words, pronouns, numerals, modals, and other closed-class items. Uses a single `POS` field.

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

**Parser behaviour:** `POS` is stored as `pos` on each `meanings` row. `pos_mask` auto-computes to `""` for closed-class-only words. `derivation_mask` (deprecated) is set to `""` for backwards compatibility.

### C. Compound Template (Content Word Extension)

Add the following fields to the Content Word template above:

```markdown
| Components | root1-form + root2-form |
| Pattern | Agent / Instrument / Property / Measure / Process / Result / Location / Doctrine / Capability / Without |
| Rule Ref | rules/3-subsystems/compounding.md §I-{section} |
```

**Human fills:** Kilor Form, `Meaning` array, Type, Components, Pattern, Rule Ref.  
**AI validates:** Component roots exist in DB.  
**AI auto-suggests:** Consensus Prefix (from compound head rules, `compounding.md` §IV and `derivational-suffixes.md` §IV).

### D. Polysemy (Adding a Meaning to an Existing Word)

Use the `edit` command with a `--pos` flag:

```
python kilor.py edit existing-form --add-meaning "new gloss" --pos N
```

Inserts a new `meanings` row with the specified `pos` and incremented `sort_order` (scoped within the same `pos`). `pos_mask` is auto-recomputed after insertion.

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

### A₂. Boundary Plosive Voicing Validation

See `0-foundation/phonology.md` §VI. Blocking errors when a **voiceless core plosive-final** root (`p`/`t`/`k`) fuses with a **vowel-initial** derivational suffix:

- The fused form **must** voice the root-final stop to its voiced counterpart (`p→b`, `t→d`, `k→g`) in the intervocalic position. Storing the unvoiced spelling (e.g. `*kopik` for root `kop` + `-ik`) is a blocking error.
- The neutralisation policy (voiced form may collide with an existing root) is **non-blocking** — accept it; record the homograph in `notes` if it arises.
- Non-triggering cases (consonant-initial suffixes, case suffixes, `-s`, multi-word forms) are unaffected and require no mutation.

> **Existing exemplar:** `lorrak` (root, k-final) + `-ik` → `lorragik` (linguistics), stored voiced.

### B. POS Tag & pos_mask Validation

POS tags are validated per-meaning during template parsing: each must be in `VALID_POS` (`kilor/schema.py`). Tags not in the valid set produce a blocking error.

`pos_mask` is auto-computed by `compute_pos_mask()` — no manual validation needed. The function maps:

| Input POS tag | Contributes to pos_mask |
|---|---|
| `N`, `V`, `A`, `D` | Direct mapping |
| `MODAL` | `V` (modals surface in verb form) |
| `PROPN` | `N` (proper names take noun form) |
| `PRON`, `NUM`, `DET`, `CCONJ`, `SCONJ`, `ADP`, `PART`, `DEM`, `Q`, `CLF`, `INTERJ` | Nothing (closed-class) |

A and D are independent — no forced co-occurrence. `D`-only pos_mask is valid. A word with only closed-class meanings gets `pos_mask = ""` (grammar particle — no inflections). A word can have both content and grammar meanings (e.g. `aniu`: zero/NUM + not/D → pos_mask = `"D"`; `is_grammar` = true because NUM is a grammar tag).

### C. Compound Validation

- All component forms must exist in `words` table (by `form`)
- Components must be roots (`is_root = 1`) — a compound cannot itself be a component
- Start-only consonants (§IV-C of `phonology.md`) must not appear word-medially in mono-compounds — such combinations require multi-word compounds

---

## V. Auto-Computation Rules (Detailed)

### A. Colour Prefix Suggestion — 7-Question Filter

Run the ordered checklist from `nouns-colour-prefix.md` §V. The **first question that strongly resonates** dictates the suggestion.

For **compounds**, the prefix follows the semantic class of the head noun (`compounding.md` §IV):

| Compound Type | Suggested Prefix |
|---|---|
| Agent (`mae`) | `a-` (living) |
| Instrument (`tek`) | `e-` (crafted) |
| Property (`lu`), Measure (`rin`), Process (`par`), Result (`param`) | `o-` (abstract) |
| Location (`pos`) | `ae-` (earth/boundary) |
| Doctrine (`isra`), Capability (`afaloi`), Without (`nara`) | `o-` (abstract) |
| Study of (`-ik`) | `o-` (abstract) |
| Method to (`-is`) | `e-` (crafted) |
| Over-/Excess (`-rolif`) | `o-` (abstract) |
| Temporal Pre- (`pi-`), Temporal Post- (`pa-`), Meta- (`sefta-`) | `o-` (abstract) |
| Augmentative (`mes-`) | `y-` (dense/mass) |
| Diminutive (`doi-`) | Inherit from base (§IV-B of `derivational-prefixes.md`) |
| Re-/Again (`ai-`), Anti-/Negative/Reversive (`kon-`) | `o-` (abstract) |

### B. Syllable Count

`count_syllables(form)` — counts vowel nuclei. Handles diphthongs and `ae` as single nuclei. Tone markers (`j`, `v`) and hyphen are stripped before counting.

### C. Syllable Division

`split_syllables(form)` — greedy Maximal Onset Principle parse. For mono-compounds, `detect_syllable_ambiguities()` flags `ae`/diphthong/vowel-hiatus at morpheme boundaries for human review.

### D. Inflection Generation (from `pos_mask`)

Inflections are generated from the `pos_mask` aggregate via `POS_TO_INFLECTION` (`kilor/schema.py`):

| pos_mask letter | `form_type` | 1–2 syllable surface | 3+ syllable surface |
|---|---|---|---|
| `N` | `noun` | bare root | tonal N (`j` on 1st of last-3) |
| `V` | `verb` | bare root | tonal V (`v` on 1st of last-3) |
| `A` | `adjective` | root + `-s` | tonal A (`j` on 2nd of last-3) |
| `D` | `adverb` | root + `-s` | tonal D (`v` on 2nd of last-3) |

**pos_mask derivation from meanings:**

| Meanings have POS tags... | `pos_mask` result | Inflections |
|---|---|---|
| Only `N`, `V`, `A`, `D` tags | Aggregate NVAD (e.g. `"NV"`, `"AD"`, `"NAVD"`) | 1 row per letter |
| Mixed content + grammar (e.g. `NUM` + `D`) | Content letters only (grammar tags ignored) | Per content letters |
| Only closed-class tags (e.g. `PART`, `PRON`, `ADP`) | `""` | **None** |
| No meanings | `""` | **None** |

For **3+ syllable roots**, tone markers (`j`, `v`) are applied to all inflected forms per `tone-prosody.md` before storage. Multi-word compounds: tone markers on the last word only.

### E. Acc/Gen Forms

`get_case_forms(form, derivation_mask)` — applies the Contrastive Suffix Rule (`cases.md` §II):

- Grammar particles (`pos_mask == ""`): exempt → `(None, None)`
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
| Use the word in its default colour prefix and most common grammatical role per its `pos_mask` | — |
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
- They can share the same `consensus_prefix` and `pos_mask`

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

> **Can both meanings coexist under one `consensus_prefix` and one `pos_mask`?**

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

Priority-ordered list of pipeline features not yet implemented:

| Priority | Gap | Impact |
|---|---|---|
| 3 | **Compound support** — `add.py` treats every entry as a bare root | Cannot insert compounds through the pipeline |
| 4 | **Edit mode** — no `edit` command exists | Cannot fix typos, add meanings, or update prefixes without raw SQL |
| — | **Near-collision detection** — no Levenshtein-distance flagging | Duplicate-like roots may be inserted without warning |
| — | **`--with-examples` flag** — LLM sentence generation not yet wired into `add.py` Phase 2 | Example sentences can only be added post-creation via raw SQL or a future `edit` command |

**Resolved (v2.4.0):**
- ~~Priority 1: Conditional inflection generation~~ — Fixed: `pos_mask`-based generation via `POS_TO_INFLECTION` mapping; `add.py` + `edit.py` both regenerate from mask.
- ~~Priority 2: Hardcoded consensus_prefix~~ — Fixed: `add.py` validates prefix against NVAD mask rules; missing N-prefix is a blocking error.
- ~~Priority 5: Tone markers on inflections~~ — Fixed: `compute_tonal_inflections()` in `phonology.py` computes and stores tonal forms for 3+ syllable words (both in `inflections` table and `search_text`).

---

## X. Cross-References

- **Phonotactic rules:** `0-foundation/phonology.md`
- **Tone application:** `0-foundation/tone-prosody.md`
- **7-Question Filter & colour prefix ontology:** `1-nominals/nouns-colour-prefix.md` §V
- **Compound head prefix rules:** `3-subsystems/compounding.md` §IV, `3-subsystems/derivational-suffixes.md` §IV, and `3-subsystems/derivational-prefixes.md` §IV
- **Case suffix rules (Contrastive Suffix Rule):** `1-nominals/cases.md` §II
- **DB schema reference:** `data/SCHEMA.md`
- **POS tag set & pos_mask computation:** `kilor/schema.py`
- **Validation implementation:** `kilor/phonology.py`
- **CLI commands:** `.clinerules/kilor.md` §Available CLI commands

---

*End of Word Creation Pipeline Specification.*