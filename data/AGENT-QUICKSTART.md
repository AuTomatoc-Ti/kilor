# AI Agent Quick-Start Guide

**Purpose:** Fast decision-making for common Kilor lexicon tasks.  
**For detailed specs:** See `data/AI-GUIDE.md`, `rules/4-meta/word-creation-pipeline.md`, `data/SCHEMA.md`  
**Last updated:** 2026-07-24

---

## Decision Tree: What Are You Trying To Do?

```
Adding to lexicon?
├─ Word from wordlist/ → `python kilor.py next` → fill today.md → `python kilor.py add`
├─ Ad-hoc new root → Use Python API (Method B in AI-GUIDE.md)
├─ Compound word → Use Python API (Method B in AI-GUIDE.md §2)
├─ Add meaning to existing word → `python kilor.py edit <form> --add-meaning "gloss"`
├─ Fix typo → `python kilor.py edit <form> --fix-typo "newform"`
├─ Add example → `python kilor.py edit <form> --add-example "kilor" "english"`
└─ Query/search → `python kilor.py suggest <word>` or REST API `python kilor.py serve`
```

---

## Critical Rules (Violating These = Invalid Data)

### Phonotactics
- **No `j` or `v`** in bare roots (reserved for tone markers on 3+ syllable words)
- **Max 5 syllables** per root
- **1–2 syllable roots cannot end in `-s`** (unless whitelisted: `gus`, `fos`, `aus`, `ous`, `les`, `mangus`, `kas`, `hus`, `tus`, `rakas`, `fidak`)
- **Function words and compounds are exempt** from the `-s` constraint

### Derivation Mask
- **Valid characters:** `N`, `V`, `A`, `D` (case-insensitive)
- **D requires A:** Adverb (`D`) must co-occur with Adjective (`A`)
- **Common masks:** `N` (noun), `V` (verb), `A` (adj), `NA` (noun/adj), `NV` (noun/verb), `NVAD` (all four)

### Colour Prefix ( consensus_prefix )
- **Default:** `o-` (Abstract/Void) — but **verify with 7-Question Filter** before accepting
- **7 prefixes:** `a-` (Alive), `e-` (Crafted), `i-` (Fluid), `o-` (Abstract), `u-` (Organic), `y-` (Dense), `ae-` (Earth)
- **See:** `rules/1-nominals/nouns-colour-prefix.md` §V for the filter

### Section (1–8)
| Code | Domain | Examples |
|------|--------|----------|
| 1 | Concrete | stone, water, fire, house |
| 2 | Living | dog, tree, heart, body |
| 3 | Action | run, eat, sleep, cut |
| 4 | Quality | big, red, happy, smooth |
| 5 | Mental | think, dream, fear, know |
| 6 | Relational | mother, north, above, with |
| 7 | Abstract | law, time, beauty, system |
| 8 | Grammar | pronouns, particles, numerals |

**Tiebreak rule:** When in doubt, choose the **lowest number** (most concrete).

---

## Common Workflows

### 1. Add a New Root (CLI Method)

```bash
# Step 1: Generate template
python kilor.py next --count 10

# Step 2: Edit today.md — fill in Kilor Root, Section, Derivation Mask
# Example entry:
# ### volcano (nature)
# | Kilor Root | foragilan |
# | Section (1-8) | 1 |
# | Derivation Mask | N |
# | Consensus Prefix | o- |

# Step 3: Validate and insert
python kilor.py add --file today.md
```

**What `add.py` does automatically:**
- Validates phonotactics (no `j`/`v`, max 5 syllables, `-s` constraint)
- Checks for duplicates
- Counts syllables
- Generates inflections **based on derivation mask** (not all 4 forms!)
- Inserts into `words`, `meanings`, `inflections` tables
- Rebuilds FTS search index

### 2. Add a New Root (Python API Method)

```python
from kilor.db import get_db, rebuild_fts
from kilor.phonology import validate_content_root, count_syllables

conn = get_db()

form = "newroot"
gloss = "example meaning"
category = "n"  # n, v, a, nv, na, av
section = "1"   # 1-8
mask = "N"      # NVAD mask

# Validate
valid, err = validate_content_root(form, is_func=False, is_compound=False)
if not valid:
    print(f"Invalid: {err}")
    exit(1)

# Insert
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       derivation_mask, section, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 1, 0, NULL, ?, ?, 'o-', 0, '')
""", (form, count_syllables(form), mask, section))
word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# Meaning
conn.execute(
    "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, 'en', 0)",
    (word_id, gloss)
)

# Conditional inflections (only those in mask)
for ft in ['noun']:  # mask = 'N'
    conn.execute(
        "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
        (word_id, ft, form)
    )

conn.commit()
rebuild_fts(conn)
conn.close()
```

### 3. Add a Compound Word

```python
from kilor.db import get_db, rebuild_fts
from kilor.phonology import count_syllables

conn = get_db()

compound_form = "foragilan"  # Single fused form
gloss = "volcano"
components = ["fora", "gilan"]  # Must already exist in DB
pattern = "nominal-compound"  # See rules/3-subsystems/derivational-compounding.md

# Verify components exist
component_ids = []
for cform in components:
    row = conn.execute("SELECT id FROM words WHERE form = ?", (cform,)).fetchone()
    if not row:
        print(f"Error: component '{cform}' not found")
        exit(1)
    component_ids.append(row["id"])

# Insert compound
syl_total = sum(count_syllables(c) for c in components)
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       derivation_mask, section, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 0, 1, 'mono', 'N', '1', 'o-', 0, ?)
""", (compound_form, syl_total, f"compound: {' + '.join(components)}"))
compound_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# Meaning
conn.execute(
    "INSERT INTO meanings (compound_id, gloss, language, sort_order) VALUES (?, ?, 'en', 0)",
    (compound_id, gloss)
)

# Link components
for pos, cid in enumerate(component_ids):
    conn.execute(
        "INSERT INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
        (compound_id, cid, pos)
    )

# Pattern metadata
conn.execute(
    "INSERT INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, ?)",
    (compound_id, pattern, "rules/3-subsystems/derivational-compounding.md §II")
)

conn.commit()
rebuild_fts(conn)
conn.close()
```

### 4. Edit an Existing Word

```bash
# Add a second meaning (polysemy)
python kilor.py edit fora --add-meaning "fireplace"

# Fix a typo in the form
python kilor.py edit foragilan --fix-typo "foragilan"

# Change colour prefix
python kilor.py edit fora --set-prefix "a-"

# Change derivation mask (regenerates inflections)
python kilor.py edit fora --set-mask "nv"

# Add usage example
python kilor.py edit fora --add-example "a-fora res taka" "The fire is hot"

# Remove example (by ID from examples table)
python kilor.py edit fora --remove-example 42
```

### 5. Search the Lexicon

```bash
# Suggest related roots for a concept
python kilor.py suggest "volcano"

# Start REST API server
python kilor.py serve --port 8765

# Query via curl
curl "http://localhost:8765/api/search?q=volcano"
curl "http://localhost:8765/api/words?section=1&limit=50"
```

---

## Validation Checklist

Before inserting any word, verify:

- [ ] **Form is not empty**
- [ ] **No `j` or `v`** in bare root (unless 3+ syllable tone markers)
- [ ] **At least one vowel** (a, e, i, o, u, y, ae)
- [ ] **Max 5 syllables** (use `count_syllables(form)`)
- [ ] **1–2 syllable roots don't end in `-s`** (unless whitelisted)
- [ ] **No duplicate form** in database
- [ ] **Derivation mask** contains only `N`, `V`, `A`, `D`
- [ ] **If mask has `D`, it must also have `A`**
- [ ] **If compound:** all component roots exist in DB
- [ ] **Section** is 1–8 (use tiebreak rule: lowest number when unsure)
- [ ] **Colour prefix** verified with 7-Question Filter (or default `o-` with note)

**Run validation after changes:**
```bash
python kilor.py check   # Validates all entries
python kilor.py status  # Shows statistics
```

---

## Database Schema (SSOT: `data/kilor.db`)

### Core Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `words` | Every lexical entry | `form`, `syl_count`, `derivation_mask`, `section`, `consensus_prefix` |
| `meanings` | English glosses | `word_id`, `gloss`, `sort_order` |
| `inflections` | Derived forms | `word_id`, `form_type` (noun/verb/adj/adv), `form` |
| `compound_components` | Construction links | `compound_id`, `component_id`, `position` |
| `compound_meta` | Pattern metadata | `compound_id`, `pattern`, `rule_ref` |
| `examples` | Usage sentences | `word_id`, `kilor_text`, `english_text`, `source` |

### Important Indexes
```sql
SELECT * FROM words WHERE form = ?;           -- idx_words_form
SELECT * FROM words WHERE section = ?;        -- idx_words_section
SELECT * FROM words WHERE derivation_mask = ?; -- idx_words_derivation_mask
```

### Common Queries

```python
# Full word lookup with meanings
conn.execute("""
    SELECT w.*, GROUP_CONCAT(m.gloss, ' / ') as meanings
    FROM words w
    LEFT JOIN meanings m ON w.id = m.word_id
    WHERE w.form = ?
    GROUP BY w.id
""", (form,))

# All roots with inflections
conn.execute("""
    SELECT w.form, m.gloss, i.form_type, i.form
    FROM words w
    JOIN meanings m ON w.id = m.word_id
    LEFT JOIN inflections i ON w.id = i.word_id
    WHERE w.is_root = 1 AND w.is_function_word = 0
    ORDER BY w.form, i.form_type
""")

# Compound decomposition
conn.execute("""
    SELECT w.form, cc.position, w2.form as component, cm.pattern
    FROM words w
    JOIN compound_components cc ON w.id = cc.compound_id
    JOIN words w2 ON cc.component_id = w2.id
    LEFT JOIN compound_meta cm ON w.id = cm.compound_id
    WHERE w.is_compound = 1
    ORDER BY w.form, cc.position
""")
```

---

## Troubleshooting

### "duplicate — already exists"
The form is already in the database. Check if you meant to add a meaning instead:
```bash
python kilor.py edit <form> --add-meaning "new gloss"
```

### "has only 1 inflected form(s)"
Content roots need at least 2 inflections (noun + verb minimum). Check the derivation mask.

### "syl_count mismatch"
The stored syllable count doesn't match `count_syllables()`. Fix with:
```bash
python kilor.py edit <form> --fix-typo <form>  # Recomputes syl_count
```

### FTS search returns stale results
Run `python kilor.py export --format dictionary` to rebuild FTS index.

---

## Quick Reference

### CLI Commands
```bash
python kilor.py next [--count N]      # Generate today.md template
python kilor.py add --file today.md   # Insert entries from today.md
python kilor.py check                 # Validate all entries
python kilor.py status                # Show statistics
python kilor.py export --format html  # Generate dictionary
python kilor.py suggest <word>        # Find related roots
python kilor.py edit <form> [opts]    # Edit existing word
python kilor.py serve [--port N]      # Start REST API
python kilor.py sync                  # Sync public DB
```

### File Locations
- **Database (SSOT):** `data/kilor.db`
- **AI Guide (detailed):** `data/AI-GUIDE.md`
- **Schema reference:** `data/SCHEMA.md`
- **Word creation pipeline:** `rules/4-meta/word-creation-pipeline.md`
- **Today's template:** `today.md` (auto-generated)
- **Wordlists:** `wordlist/*.txt`

### Key Imports
```python
from kilor.db import get_db, rebuild_fts, fts_search
from kilor.phonology import validate_content_root, count_syllables, get_case_forms
from kilor.schema import SECTION_LABELS, DERIVATION_MASK_LABELS
```

---

## When You Need More Detail

| Topic | Reference |
|-------|-----------|
| Full word creation workflow (4 phases) | `rules/4-meta/word-creation-pipeline.md` |
| Python API examples (roots, compounds, examples) | `data/AI-GUIDE.md` §1-3 |
| Phonotactic rules (positional consonants, schwa) | `rules/0-foundation/phonology.md` |
| Tone system (`j`/`v` placement) | `rules/0-foundation/tone-prosody.md` |
| Colour prefix 7-Question Filter | `rules/1-nominals/nouns-colour-prefix.md` §V |
| Compound patterns (agentive, instrument, etc.) | `rules/3-subsystems/derivational-compounding.md` |
| Case forms (ACC/GEN suffixes) | `rules/1-nominals/cases.md` §II |
| Database schema (tables, columns, FKs) | `data/SCHEMA.md` |
| REST API endpoints | `kilor/api.py` |

---

*This is a quick reference. For complete specifications, see the linked documents.*

</parameter>
<task_progress>
- [x] Analyze current workspace structure and AI interaction patterns
- [x] Review existing AI guides and conventions
- [x] Identify pain points and inefficiencies
- [x] Propose concrete improvements
- [x] Implement critical fixes (add.py, suggest.py, edit command)
- [x] Create AGENT-QUICKSTART.md
- [ ] Enhance check.py validation
- [ ] Fix schema documentation drift
- [ ] Test all changes
</task_progress>
</write_to_file>