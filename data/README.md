# Kilor Data Files

Machine-readable lexical data for Kilor. The **SQLite database (`kilor.db`)** is the single source of truth (SSOT) for the lexicon.

## Quick Start

```bash
python kilor.py check          # Validate the database
python kilor.py status         # Show lexicon statistics
python kilor.py export --format html    # Generate searchable dictionary
```

## File Inventory

| File | Purpose | Updated by |
|---|---|---|
| `kilor.db` | **Lexicon database (SSOT)** — all words, meanings, inflections, compound metadata, examples, full-text search | `kilor.py add`, `kilor.py migrate` |
| `dictionary.html` | **Searchable dictionary SPA** — open in a browser, search by word/meaning/example, filter by type/category | `kilor.py export --format html` |
| `dictionary-data.json` | Complete dataset consumed by the dictionary SPA | `kilor.py export --format dictionary` or `--format html` |
| `lexicon_export.csv` | CSV export of all entries | `kilor.py export --format csv` |
| `compounds_export.json` | JSON export of compound words | `kilor.py export --format json` |
| `AI-GUIDE.md` | **AI agent guide** — how to add roots, compounds, and examples programmatically or via CLI | Manual |
| `SCHEMA.md` | Human-readable schema reference (tables, columns, relationships, common queries) | Manual (mirrors `kilor.db`) |
| `schema.json` | Machine-parseable schema definition | Manual (mirrors `kilor.db`) |
| `archive/` | **Archived legacy files** (`lexicon.csv`, `compounds.json`) — kept for historical reference only. Do not edit or rely on these. | N/A |
## For AI Agents

### Getting Started
- **`data/AI-GUIDE.md`** — step-by-step guide for adding roots, compounds, and examples. Start here.
- **`data/SCHEMA.md`** — table definitions, relationships, and common queries
- **`data/schema.json`** — machine-parseable schema (tables, columns, types, FKs, indexes)

### Full-Text Search
The database includes an FTS5 index for fast text search across form, gloss, and examples. Query via SQL:
```sql
SELECT rowid FROM words_fts WHERE words_fts MATCH 'volcano' ORDER BY rank;
```
Or use `kilor/db.py`:
```python
from kilor.db import fts_search
word_ids = fts_search('volcano')
```

### Querying the Database
```python
from kilor.db import get_db
conn = get_db()
# See data/SCHEMA.md for common query patterns
```

## Data Flow

```
data/archive/lexicon.csv + compounds.json  (legacy / archived)
        │
        ▼
  kilor.py migrate ──→ kilor.db (SSOT) ←── kilor.py add
        │                       │
        │              kilor.py export
        │                       │
        │         ┌─────────────┼─────────────┐
        │         ▼             ▼             ▼
        │   dictionary-    lexicon_     compounds_
        │   data.json +    export.csv   export.json
        │   dictionary.html
        │
  kilor.py check ──→ validation report
  kilor.py status ──→ statistics dashboard
```

## SSOT Rules

### `kilor.db` is the SSOT for:
- Word form, syllable count, category
- Meanings (English glosses)
- Inflected forms (noun, verb, adjective, adverb)
- Consensus colour prefix, function word status
- Root vs. compound classification
- Compound component links, pattern, and rule references
- Usage examples

### `archive/lexicon.csv` and `archive/compounds.json` (legacy):
- Moved to `data/archive/` for historical reference
- **Not** the SSOT — do not add new entries to these files
- If you need to rebuild `kilor.db` from scratch, run `python kilor.py migrate` (it reads from `data/archive/`)
## Updating the Lexicon

- **Adding a new word:** `python kilor.py add --file today.md`
- **Validating:** `python kilor.py check`
- **Viewing statistics:** `python kilor.py status`
- **Exporting:** `python kilor.py export --format csv|json|html|dictionary`
- **FTS query from Python:** `from kilor.db import fts_search`
- **Browsing:** open `data/dictionary.html` in a browser

## Migration from Legacy Files

If you ever need to rebuild `kilor.db` from scratch (the archived legacy files in `data/archive/`):

```bash
rm data/kilor.db        # Delete existing database
python kilor.py migrate # Rebuild from legacy CSV + JSON in data/archive/
python kilor.py export --format html  # Regenerate dictionary
```
---

*Last updated: 2026-07-19*
