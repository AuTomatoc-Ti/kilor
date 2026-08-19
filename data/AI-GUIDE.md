# AI Agent Guide — Updating the Kilor Database

This document teaches an AI agent how to **add new roots, compounds, and examples** to the Kilor lexicon database. Read `data/SCHEMA.md` and `data/schema.json` first for table reference.

---

## 1. Adding a New Root Word

### Method A — CLI (preferred for batch input via today.md)

```bash
python kilor.py next                    # Generate today.md with untranslated words
# → Edit today.md, fill in Kilor Root, Derivation Mask, etc.
python kilor.py add --file today.md     # Validate and insert into kilor.db
```

### Method B — Direct Python (for programmatic/single-word insertion)

```python
from kilor.db import get_db, rebuild_fts
from kilor.phonology import validate_content_root, count_syllables

conn = get_db()

form = "newroot"          # Must follow phonotactics (see §4)
gloss = "example meaning"
mask = "N"                # NVAD mask (N, V, A, D, NV, NA, etc.)
prefix = "o-"             # Default colour prefix

# ── Validate ──
valid, err = validate_content_root(form, is_func=False, is_compound=False)
if not valid:
    print(f"Invalid: {err}")
    # ... handle error ...

# ── Insert word ──
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       derivation_mask, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 1, 0, NULL, ?, ?, 0, '')
""", (form, count_syllables(form), mask, prefix))
word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# ── Insert meaning ──
conn.execute(
    "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, 'en', 0)",
    (word_id, gloss)
)

# ── Insert inflections (conditional on mask) ──
# Only generate forms that the mask allows
mask_upper = (mask or "").upper()
if 'N' in mask_upper:
    conn.execute("INSERT INTO inflections (word_id, form_type, form) VALUES (?, 'noun', ?)", (word_id, form))
if 'V' in mask_upper:
    conn.execute("INSERT INTO inflections (word_id, form_type, form) VALUES (?, 'verb', ?)", (word_id, form))
if 'A' in mask_upper:
    conn.execute("INSERT INTO inflections (word_id, form_type, form) VALUES (?, 'adjective', ?)", (word_id, f"{form}s"))
if 'D' in mask_upper:
    conn.execute("INSERT INTO inflections (word_id, form_type, form) VALUES (?, 'adverb', ?)", (word_id, f"{form}s"))

conn.commit()
rebuild_fts(conn)    # CRITICAL: keep FTS in sync
conn.close()
```

---

## 2. Adding a Compound Word

A compound links two or more existing roots. The roots **must already exist** in the database.

### Method A — CLI (today.md with compound notation)

In today.md, use the Decision column:
```
| Decision (root/compound/derivation) | compound |
| Notes | kom + pon + ent |
```
The notes field documents which roots form the compound. You must then manually link them (see Method B).

### Method B — Direct Python

```python
from kilor.db import get_db, rebuild_fts
from kilor.phonology import count_syllables

conn = get_db()

compound_form = "sori leman"       # Multi-word: space-separated
gloss = "good person"
component_forms = ["sori", "leman"]  # Must already exist in words table
pattern = "nominal-compound"         # See §6 for pattern list
rule_ref = "rules/3-subsystems/derivational-compounding.md"  # Optional

# ── Look up component IDs ──
component_ids = []
for cform in component_forms:
    row = conn.execute("SELECT id, syl_count FROM words WHERE form = ?", (cform,)).fetchone()
    if not row:
        raise ValueError(f"Component '{cform}' not found in database — add it first")
    component_ids.append(row["id"])

syl_total = sum(count_syllables(c) for c in component_forms)

# ── Determine compound type ──
compound_type = "multi" if " " in compound_form else "mono"

# ── Determine mask from pattern ──
mask_map = {
    "agentive": "N", "instrument": "N", "property": "N", "measure": "N",
    "process": "N", "location": "N", "doctrine": "N", "capability": "NA",
    "without": "NA", "epistemic-modal": "NA", "nominal-compound": "N",
}
mask = mask_map.get(pattern, "N")

# ── Insert word ──
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       derivation_mask, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 0, 1, ?, ?, 'o-', 0, ?)
""", (compound_form, syl_total, compound_type, mask,
      f"compound: {' + '.join(component_forms)}"))
compound_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# ── Insert meaning ──
conn.execute(
    "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, 'en', 0)",
    (compound_id, gloss)
)

# ── Link components ──
for pos, cid in enumerate(component_ids):
    conn.execute(
        "INSERT INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
        (compound_id, cid, pos)
    )

# ── Add pattern metadata ──
conn.execute(
    "INSERT INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, ?)",
    (compound_id, pattern, rule_ref)
)

conn.commit()
rebuild_fts(conn)
conn.close()
```

---

## 3. Adding Usage Examples

```python
from kilor.db import get_db, rebuild_fts

conn = get_db()

word_id = 1  # ID of the word
kilor_text = "foragilan res rali"
english_text = "The volcano is big."
source = "canonical"  # "canonical" or "corpus"

conn.execute("""
    INSERT INTO examples (word_id, kilor_text, english_text, source)
    VALUES (?, ?, ?, ?)
""", (word_id, kilor_text, english_text, source))

conn.commit()
rebuild_fts(conn)  # Rebuild so FTS indexes the new example text
conn.close()
```

---

## 4. Phonotactic Constraints (Must Validate Before Insert)

| Rule | Detail |
|---|---|
| No **j** or **v** | These letters are reserved for tone marking |
| Max 5 syllables | Roots exceeding 5 syllables are invalid |
| **-s rule** | 1–2 syllable content roots may NOT end in `s` (reserved for derivational suffix) |
| -s whitelist | `os`, `gus`, `fos`, `aus`, `ous`, `les`, `mangus`, `kas`, `hus`, `tus`, `rakas`, `fidak` — these are exempt |
| Function words | Not subject to -s constraint (`is_func=True` bypasses) |
| Compounds | Not subject to -s constraint (`is_compound=True` bypasses) |

Validation call:
```python
from kilor.phonology import validate_content_root
valid, error = validate_content_root(form, is_func=False, is_compound=False)
```

---

## 5. Compound Pattern Names

Valid values for `compound_meta.pattern`:
```
agentive, instrument, property, measure, process, location,
doctrine, capability, without, epistemic-modal, nominal-compound
```

---

## 6. Verification & Export After Changes

```bash
# Always run after changes:
python kilor.py check                     # Validate all entries
python kilor.py status                    # View statistics
python kilor.py export --format html      # Regenerate dictionary
python kilor.py export --format csv       # Regenerate CSV export
```

Or programmatically:
```python
from kilor.commands.check import cmd_check
cmd_check()
```

---

## 7. Critical Rules

1. **Always rebuild FTS after any INSERT/UPDATE/DELETE** — call `rebuild_fts(conn)` after committing. Without this, the search index will be stale.

2. **Components must exist before creating compounds** — the component roots referenced in `compound_components.component_id` must have valid `words.id` entries.

3. **Run `validate_content_root()` before inserting** — sanitize inputs against phonotactics.

4. **Never delete `words_fts` triggers** — if you need to bulk-insert many words, insert them all first, then call `rebuild_fts()` once at the end.

5. **Database file is `data/kilor.db`** — back it up before destructive operations.

---

*Last updated: 2026-07-25*