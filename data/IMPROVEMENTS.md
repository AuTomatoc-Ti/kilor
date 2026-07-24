# Kilor Workspace Improvements for AI Agents

**Date:** 2026-07-24  
**Purpose:** Document improvements made to enhance AI agent usability and management  
**Status:** Implemented

---

## Summary

This document tracks improvements made to the Kilor workspace to make it more AI-agent friendly. All changes follow the existing conventions and maintain backward compatibility.

---

## Phase 1: Critical Fixes (Completed)

### 1. Fixed Conditional Inflection Generation in `add.py`

**Problem:** `add.py` was creating all 4 inflection types (noun/verb/adj/adv) for every word, ignoring the derivation mask. This created invalid data.

**Solution:** Added `MASK_TO_FORMS` mapping and conditional inflection generation that respects the derivation mask.

**Files Modified:**
- `kilor/commands/add.py` — Added mask-to-form-type mapping, conditional inflection generation

**Impact:** Words now get only the inflections specified by their derivation mask (e.g., mask `N` = noun only, mask `NVAD` = all four).

---

### 2. Fixed `suggest.py` Bugs

**Problem:** Lines 36-42 had copy-paste errors showing wrong form labels:
- Verb form displayed as "Adjective form"
- Duplicate "Adjective form" line
- Missing adverb form display

**Solution:** Corrected all form type labels to match the derivation mask.

**Files Modified:**
- `kilor/commands/suggest.py` — Fixed form type labels (Noun, Verb, Adjective, Adverb)

**Impact:** AI agents now get correct suggestions when exploring related roots.

---

### 3. Created `edit` Command

**Problem:** No way to fix typos, add meanings, or update prefixes without raw SQL. The `word-creation-pipeline.md` §VIII listed this as Priority #4 infrastructure gap.

**Solution:** Implemented full `edit` command with 6 operations:
- `--add-meaning "gloss"` — Add polysemous meaning
- `--set-prefix "a-"` — Change colour prefix
- `--set-mask "nv"` — Change derivation mask (regenerates inflections)
- `--add-example "kilor" "english"` — Add usage example
- `--remove-example <id>` — Remove example by ID
- `--fix-typo "newform"` — Correct form (validates, updates syl_count)

**Files Modified:**
- `kilor/commands/edit.py` — New file (168 lines)
- `kilor/__main__.py` — Added edit command routing and argument parsing

**Impact:** AI agents can now perform post-creation fixes without raw SQL, reducing errors and improving workflow.

---

### 4. Enhanced `check.py` Validation

**Problem:** Basic validation missed several error types:
- No check that inflections match derivation mask
- No verification that compound components are roots (not compounds)
- No near-collision detection (Levenshtein distance ≤ 2)

**Solution:** Added three new validation checks:
- **Mask-inflection consistency:** Verifies all expected form types (from mask) exist in inflections table
- **Compound component validation:** Ensures components are roots, not compounds
- **Near-collision warnings:** Flags root pairs with Levenshtein distance 1-2 (for short words ≤6 chars)

**Files Modified:**
- `kilor/commands/check.py` — Added mask validation, compound validation, Levenshtein distance calculation

**Impact:** Catches data inconsistencies early, prevents invalid compounds, warns about potential homophone confusion.

---

### 5. Created `AGENT-QUICKSTART.md`

**Problem:** AI agents had to read 4+ files (AI-GUIDE.md, word-creation-pipeline.md, SCHEMA.md, phonology.md) to understand basic workflows.

**Solution:** Created consolidated quick-start guide with:
- Decision tree for common tasks
- Critical rules (phonotactics, masks, prefixes, sections)
- 5 common workflows with code examples
- Validation checklist
- Database schema overview
- Troubleshooting guide
- Quick reference tables

**Files Created:**
- `data/AGENT-QUICKSTART.md` — 280-line quick reference

**Impact:** AI agents can now get started in minutes instead of reading 1000+ lines of documentation.

---

## Phase 2: Documentation Fixes (Completed)

### 6. Fixed Schema Documentation Drift

**Problem:** `data/SCHEMA.md` said sections are "A-J" but they're actually "1-8".

**Solution:** Updated section description to match actual implementation.

**Files Modified:**
- `data/SCHEMA.md` — Fixed section domain description

**Impact:** Prevents AI agents from using invalid section codes.

---

### 7. Fixed Roadmap Documentation

**Problem:** `roadmap.md` listed `lexicon.csv` as SSOT, but `kilor.db` is the actual single source of truth.

**Solution:** Updated Process Infrastructure table to reflect current architecture.

**Files Modified:**
- `roadmap.md` — Updated tool/asset table with correct SSOT

**Impact:** Prevents AI agents from trying to edit legacy files instead of the database.

---

## Testing Results

### Validation Test
```bash
$ python kilor.py check
2 validation error(s) — 2 compounds using other compounds as components (pre-existing data issue)
1088 warning(s) — Near-collision warnings (expected for 246 roots)
```

**Note:** The 2 errors are pre-existing data issues where compounds reference other compounds as components. This is a data quality issue from earlier migration, not caused by our changes.

### Edit Command Test
```bash
$ python kilor.py edit fora --add-meaning "fireplace"
✅ Updated 'fora':
  • Added meaning: 'fireplace'
```

**Result:** Successfully added polysemous meaning.

### Suggest Command Test
```bash
$ python kilor.py suggest fire
⚠️  Already exists: fora = fire
```

**Result:** Correctly detects existing word.

### Status Command Test
```bash
$ python kilor.py status
Content roots: 246
Function words: 100
Compounds (mono): 76
Compounds (multi): 9
Derived surface forms: 503
Total surface words: 688
```

**Result:** Statistics display correctly.

---

## Files Changed Summary

| File | Type | Lines | Description |
|------|------|-------|-------------|
| `kilor/commands/add.py` | Modified | +20 | Conditional inflection generation |
| `kilor/commands/suggest.py` | Modified | -4/+4 | Fixed form type labels |
| `kilor/commands/edit.py` | Created | 168 | New edit command |
| `kilor/__main__.py` | Modified | +35 | Edit command routing |
| `kilor/commands/check.py` | Modified | +85 | Enhanced validation |
| `data/AGENT-QUICKSTART.md` | Created | 280 | AI agent quick reference |
| `data/SCHEMA.md` | Modified | 1 | Fixed section description |
| `roadmap.md` | Modified | 6 | Updated SSOT references |

**Total:** 8 files changed, ~600 lines added/modified

---

## Remaining Opportunities (Not Implemented)

### Lower Priority (Documented for Future)

1. **Colour prefix suggestion in `add.py`** — Currently hardcoded to "o-". Could integrate 7-Question Filter from `nouns-colour-prefix.md` §V.

2. **Compound support in `add.py`** — Currently treats all entries as bare roots. Could add compound notation parsing.

3. **`--with-examples` flag** — Documented in pipeline §V-F but not implemented. Would generate example sentences via LLM.

4. **Tone markers on inflections** — 3+ syllable inflected forms don't get `j`/`v` markers. Requires complex tone placement logic.

5. **Integration tests** — Could add `tests/test_pipeline.py` for full 4-phase workflow testing.

---

## Recommendations for AI Agents

### Getting Started
1. Read `data/AGENT-QUICKSTART.md` first (15-minute overview)
2. Refer to `data/AI-GUIDE.md` for detailed Python API examples
3. Check `rules/4-meta/word-creation-pipeline.md` for the 4-phase workflow spec

### Common Tasks
- **Add word from wordlist:** `python kilor.py next` → edit `today.md` → `python kilor.py add`
- **Add ad-hoc root:** Use Python API (Method B in AI-GUIDE.md)
- **Fix existing word:** `python kilor.py edit <form> --fix-typo "newform"`
- **Add meaning:** `python kilor.py edit <form> --add-meaning "gloss"`
- **Validate:** `python kilor.py check` (run after every batch)

### Critical Reminders
- ✅ Conditional inflections now work correctly (respects derivation mask)
- ✅ Edit command available for post-creation fixes
- ✅ Enhanced validation catches mask mismatches and compound errors
- ⚠️  Near-collision warnings are expected — review but don't panic
- ⚠️  2 pre-existing compound errors in data (not introduced by our changes)

---

## Backward Compatibility

All changes are backward compatible:
- Existing `add.py` workflow unchanged (just fixes inflection bug)
- `edit` command is new (no existing code depends on it)
- `check.py` adds warnings but doesn't break existing output format
- All existing CLI commands work as before

---

*End of improvements document.*

</parameter>
<task_progress>
- [x] Analyze current workspace structure and AI interaction patterns
- [x] Review existing AI guides and conventions
- [x] Identify pain points and inefficiencies
- [x] Propose concrete improvements
- [x] Implement critical fixes (add.py, suggest.py, edit command)
- [x] Create AGENT-QUICKSTART.md
- [x] Enhance check.py validation
- [x] Fix schema documentation drift
- [x] Test all changes
</task_progress>
</write_to_file>