# Kilor Data Files

Machine-readable lexical data for Kilor. These files are the single source of truth (SSOT) for the lexicon. Human-readable dictionary output is generated via `python kilor.py dict` (future command).

## Files

| File | Purpose | Format |
|------|---------|--------|
| `lexicon.csv` | **Root database** — bare roots, syllables, meanings, categories, inflected forms, colour prefixes. Validated by `kilor.py check`. | CSV |
| `compounds.json` | **Compound dictionary** — mono-word and multi-word compounds, construction metadata, meanings, patterns, rule references. | JSON |

## Data Flow

```
┌──────────────────┐    ┌─────────────────────┐
│ data/lexicon.csv │    │ data/compounds.json │
│ (roots — SSOT)   │    │ (compounds — SSOT)  │
└────────┬─────────┘    └──────────┬──────────┘
         │                         │
         └───────────┬─────────────┘
                     ▼
            ┌─────────────────┐
            │  kilor.py dict  │  ← future command
            └────────┬────────┘
                     ▼
         ┌───────────────────────┐
         │  dictionary output    │
         │  (.html / .md / .pdf) │
         └───────────────────────┘
```

## SSOT Rules

### `lexicon.csv` is the SSOT for:
- Bare root form and syllable count
- Meaning (English gloss)
- Category (n, v, a, nv, na, av)
- Section (A–J)
- Inflected forms (noun, verb, adjective, adverb columns)
- Consensus colour prefix
- Function word status

### `compounds.json` is the SSOT for:
- Construction (which roots form this compound)
- Pattern (agentive, instrumental, property, temporal-day, etc.)
- Rule reference (`rule_ref` — pointer to the grammar spec file)
- Entry type (`mono` = single orthographic word; `multi` = multi-word vocab)

### Meaning in `compounds.json`

All compounds carry a `meaning` field. For mono-word compounds also in `lexicon.csv`, this is a **lexical cache** — the canonical meaning lives in `lexicon.csv`. For multi-word compounds (which have no `lexicon.csv` entry), `compounds.json` is the sole location for the meaning.

The `in_lexicon` boolean tracks whether a compound also exists as a validated root entry.

## `lexicon.csv` Field Reference

| Column | Description | Example |
|--------|-------------|---------|
| `bare_root` | Root form (no spaces, no tone markers for 1–2 syl) | `fora` |
| `syl` | Syllable count | `2` |
| `meaning` | English gloss | `fire` |
| `category` | n, v, a, nv, na, av | `nv` |
| `section` | A–J semantic domain | `A` |
| `noun` | Noun form (with tone markers for 3+ syl) | `fora` |
| `verb` | Verb form | `fora` |
| `adjective` | Adjective form (+ `-s` for 1–2 syl) | `foras` |
| `adverb` | Adverb form | `foras` |
| `consensus_prefix` | Default colour prefix | `a-` |
| `is_function_word` | `true` for closed-class; `false` for content roots | `false` |
| `notes` | Etymology, compound construction, cross-references | `compound: fora + gilan` |

## `compounds.json` Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| `type` | `mono` (single word) or `multi` (multi-word vocab) | `mono` |
| `meaning` | English gloss | `volcano` |
| `construction` | Array of source roots | `["fora", "gilan"]` |
| `pattern` | Derivational or compounding pattern name | `nominal-compound` |
| `rule_ref` | Grammar spec reference (optional) | `rules/3-subsystems/temporals.md §I-A` |
| `in_lexicon` | Whether an entry exists in `lexicon.csv` | `true` |

## Updating These Files

- **Adding a new root:** add a row to `lexicon.csv`, run `python kilor.py check`
- **Adding a new mono-word compound:** add to both `lexicon.csv` (as a root) and `compounds.json` (construction metadata + meaning cache)
- **Adding a new multi-word compound:** add only to `compounds.json` with `in_lexicon: false`
- **Changing a meaning:** update `lexicon.csv` (SSOT for roots); if the entry also exists in `compounds.json`, update the cached meaning there too

---

*Last updated: 2026-07-12*