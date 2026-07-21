# AI Agent Guide — Updating the Kilor Database

This document teaches an AI agent how to **add new roots, compounds, and examples** to the Kilor lexicon database. Read `data/SCHEMA.md` and `data/schema.json` first for table reference.

---

## 1. Adding a New Root Word

### Method A — CLI (preferred for batch input via today.md)

```bash
python kilor.py next                    # Generate today.md with untranslated words
# → Edit today.md, fill in Kilor Root, Category, Section, etc.
python kilor.py add --file today.md     # Validate and insert into kilor.db
```

### Method B — Direct Python (for programmatic/single-word insertion)

```python
from kilor.db import get_db, rebuild_fts
from kilor.phonology import validate_content_root, count_syllables

conn = get_db()

form = "newroot"          # Must follow phonotactics (see §4)
gloss = "example meaning"
category = "n"            # n, v, a, nv, na, av
section = "7"             # 1-8 (see §5)
prefix = "o-"             # Default colour prefix

# ── Validate ──
valid, err = validate_content_root(form, is_func=False, is_compound=False)
if not valid:
    print(f"Invalid: {err}")
    # ... handle error ...

# ── Insert word ──
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       category, section, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 1, 0, NULL, ?, ?, ?, 0, '')
""", (form, count_syllables(form), category, section, prefix))
word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

# ── Insert meaning ──
conn.execute(
    "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, 'en', 0)",
    (word_id, gloss)
)

# ── Insert inflections (default: form + -s for adj/adv) ──
for ft in ('noun', 'verb', 'adjective', 'adverb'):
    conn.execute(
        "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
        (word_id, ft, f"{form}s" if ft in ('adjective', 'adverb') else form)
    )

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

# ── Determine category from pattern ──
cat_map = {
    "agentive": "n", "instrument": "n", "property": "n", "measure": "n",
    "process": "n", "location": "n", "doctrine": "n", "capability": "na",
    "without": "na", "epistemic-modal": "na", "nominal-compound": "n",
}
category = cat_map.get(pattern, "n")

# ── Insert word ──
conn.execute("""
    INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                       category, section, consensus_prefix, is_function_word, notes)
    VALUES (?, ?, 0, 1, ?, ?, '7', 'o-', 0, ?)
""", (compound_form, syl_total, compound_type, category,
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
| -s whitelist | `gus`, `fos`, `aus`, `ous`, `les`, `mangus`, `kas`, `hus`, `tus`, `rakas`, `fidak` — these are exempt |
| Function words | Not subject to -s constraint (`is_func=True` bypasses) |
| Compounds | Not subject to -s constraint (`is_compound=True` bypasses) |

Validation call:
```python
from kilor.phonology import validate_content_root
valid, error = validate_content_root(form, is_func=False, is_compound=False)
```

---

## 5. Section Map (1–8)

Section codes follow an ontological taxonomy from concrete to abstract. Each word gets exactly one section.

See `rules/4-meta/section-taxonomy.md` for the SSOT.

| Code | Domain | Boundary Test |
|---|---|---|
| 1 | Concrete | Tangible matter, substances, artifacts, buildings, geographic features |
| 2 | Living | Organisms, body parts, life processes |
| 3 | Action | Events, motions, changes, processes |
| 4 | Quality | Properties, attributes, sensory qualities, conditions |
| 5 | Mental | Internal experience, cognition, emotion, perception, art |
| 6 | Relational | Positioning: spatial, temporal, social, kinship, communication |
| 7 | Abstract | Ideas, concepts, values, systems, spirit, existence |
| 8 | Grammar | Closed-class operators, pronouns, numerals, question words, particles, modals |

### Tiebreak Rule

When a word has polysemous glosses spanning multiple sections, assign the section with **lowest code number** (most concrete):

**1 > 2 > 3 > 4 > 5 > 6 > 7 > 8**

Example: `fos` means both "ice" (1 — Concrete) and "freeze" (3 — Action). Assign section 1 (more concrete).

---
Category codes: `n` (noun), `v` (verb), `a` (adjective), `nv` (noun/verb), `na` (noun/adjective), `av` (adjective/verb)

---

## 6. Compound Pattern Names

Valid values for `compound_meta.pattern`:
```
agentive, instrument, property, measure, process, location,
doctrine, capability, without, epistemic-modal, nominal-compound
```

---

## 7. Verification & Export After Changes

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

## 8. Critical Rules

1. **Always rebuild FTS after any INSERT/UPDATE/DELETE** — call `rebuild_fts(conn)` after committing. Without this, the search index will be stale.

2. **Components must exist before creating compounds** — the component roots referenced in `compound_components.component_id` must have valid `words.id` entries.

3. **Run `validate_content_root()` before inserting** — sanitize inputs against phonotactics.

4. **Never delete `words_fts` triggers** — if you need to bulk-insert many words, insert them all first, then call `rebuild_fts()` once at the end.

5. **Database file is `data/kilor.db`** — back it up before destructive operations.

---

*Last updated: 2026-07-21*