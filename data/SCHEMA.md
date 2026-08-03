# Kilor Database Schema

**Machine-readable version:** `data/schema.json`

## Tables

### `words` — every lexical entry (SSOT)

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT | Unique word identifier |
| `form` | TEXT | NOT NULL, UNIQUE | Word as written (e.g. `foragilan`, `latif mae`) |
| `syl_count` | INTEGER | NOT NULL | Syllable count |
| `is_root` | BOOLEAN | DEFAULT 0 | True for bare roots |
| `is_compound` | BOOLEAN | DEFAULT 0 | True for compounds |
| `compound_type` | TEXT | `mono` or `multi`; NULL for roots | Compound classification |
| `derivation_mask` | TEXT | | DEPRECATED — NVAD mask (superseded by pos_mask) |
| `pos_mask` | TEXT | DEFAULT '' | POS aggregate for inflection generation (e.g. `NV`, `AD`, `""` = grammar particle) |
| `consensus_prefix` | TEXT | | Default colour prefix (e.g. `o-`); NULL or empty for words without prefix |
| `is_function_word` | BOOLEAN | DEFAULT 0 | DEPRECATED — derived from pos_mask at query time |
| `notes` | TEXT | | Free-text notes |
| `ipa` | TEXT | DEFAULT '' | Auto-computed IPA transcription (e.g. `/ˈfɔ.rɑ/`) |
| `syllables` | TEXT | DEFAULT '' | Auto-computed syllable division (e.g. `fo.ra`) |
| `status` | TEXT | DEFAULT 'active' CHECK(status IN ('draft','active','deprecated','superseded')) | Word lifecycle status |
| `superseded_by` | INTEGER | FK → `words.id` | Replacement word if deprecated/superseded |
| `source_wordlist` | TEXT | DEFAULT '' | Source wordlist file (e.g. `phase1-core300`) |
| `source_line` | INTEGER | DEFAULT 0 | Line number in source wordlist |
| `created_at` | TEXT | DEFAULT (datetime('now')) | Creation timestamp |
| `updated_at` | TEXT | DEFAULT (datetime('now')) | Last update timestamp |

Indexes: `idx_words_form` (form), `idx_words_colour` (consensus_prefix), `idx_words_syl_count` (syl_count), `idx_words_pos_mask` (pos_mask)

### `meanings` — glosses per word

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT | Row identifier |
| `word_id` | INTEGER | FK → `words.id` ON DELETE CASCADE | Owning word |
| `gloss` | TEXT | NOT NULL | English gloss |
| `language` | TEXT | DEFAULT 'en' | Language code |
| `sort_order` | INTEGER | DEFAULT 0 | Display order for multiple glosses |

Index: `idx_meanings_word_id` (word_id)

### `inflections` — inflected forms

| Column | Type | Constraints | Description |
|---|---|---|---|
| `word_id` | INTEGER | FK → `words.id` ON DELETE CASCADE | Owning word |
| `form_type` | TEXT | NOT NULL | `noun`, `verb`, `adjective`, `adverb` |
| `form` | TEXT | NOT NULL | Tone-marked inflected form |

PK: `(word_id, form_type)`

### `compound_components` — construction links

| Column | Type | Constraints | Description |
|---|---|---|---|
| `compound_id` | INTEGER | FK → `words.id` ON DELETE CASCADE | The compound word |
| `component_id` | INTEGER | FK → `words.id` ON DELETE CASCADE | Source root word |
| `position` | INTEGER | NOT NULL | Order in compound (0-based) |

PK: `(compound_id, position)`  
Index: `idx_compound_components_component_id` (component_id)

### `compound_meta` — pattern and rule references

| Column | Type | Constraints | Description |
|---|---|---|---|
| `compound_id` | INTEGER | PK, FK → `words.id` ON DELETE CASCADE | The compound word |
| `pattern` | TEXT | NOT NULL | Derivational/compounding pattern name |
| `rule_ref` | TEXT | | Grammar spec reference (e.g. `rules/3-subsystems/temporals.md §I-A`) |

### `examples` — usage examples

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, AUTOINCREMENT | Row identifier |
| `word_id` | INTEGER | FK → `words.id` ON DELETE CASCADE | Referenced word |
| `kilor_text` | TEXT | NOT NULL | Kilor example sentence |
| `english_text` | TEXT | NOT NULL | English translation |
| `source` | TEXT | DEFAULT 'canonical' | `canonical` or `corpus` |

## Relationship Map

```
words (1) ────< meanings (N)
words (1) ────< inflections (N)
words (1) ────< examples (N)
words (1) ────< compound_meta (0..1)
words.compound (1) ──< compound_components.compound_id (N)
words.root      (1) ──< compound_components.component_id (N)
```

## Common Queries

### Full word lookup
```sql
SELECT w.*, GROUP_CONCAT(m.gloss, ' / ') as meanings
FROM words w
LEFT JOIN meanings m ON w.id = m.word_id
WHERE w.form = ?
GROUP BY w.id;
```

### All roots with inflections
```sql
SELECT w.form, m.gloss, i.form_type, i.form
FROM words w
JOIN meanings m ON w.id = m.word_id
LEFT JOIN inflections i ON w.id = i.word_id
WHERE w.is_root = 1 AND w.is_function_word = 0
ORDER BY w.form, i.form_type;
```

### Compound decomposition
```sql
SELECT w.form, cc.position, w2.form as component, cm.pattern, cm.rule_ref
FROM words w
JOIN compound_components cc ON w.id = cc.compound_id
JOIN words w2 ON cc.component_id = w2.id
LEFT JOIN compound_meta cm ON w.id = cm.compound_id
WHERE w.is_compound = 1
ORDER BY w.form, cc.position;