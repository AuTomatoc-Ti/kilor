**Current Version:** v1.1.0
**Last Updated:** 2026-07-26
**Format:** `**file** — what changed`

## Template (for next entry):

## workspace v{VERSION} — {DATE}

{One-line summary}

**Frontend:**
- **`file.jsx`** — What changed
- **`file.css`** — What changed

**DB / Backend:**
- **`file.py`** — What changed

**Validation:**
- `python kilor.py check` — ✅ All N entries pass
- `npx vitest --run src/App.test.jsx` — ✅ N/N pass

---

## workspace v1.1.0 — 2026-07-26

Added `pos` column to `meanings` table (15-value PoS taxonomy). Word detail subpage with PoS-grouped meaning display. Pipeline: `add.py` parses new per-PoS `today.md` templates; `edit.py` `--add-meaning` accepts `--pos` flag.

**Frontend:**
- **`TableView.jsx`** — New `GlossWithPos` component: inline PoS tags in table gloss column (N, V, A, D, CONJ, ADP, PART etc.). Click "View full entry →" in accordion opens subpage. New `WordDetailPage` component: full-width dictionary entry with identity card, meanings grouped by PoS sections, inflections, case forms, components, pattern, examples, notes. Two-tier PoS labels: minimal abbreviations in table rows with hover tooltips; full descriptive labels (Noun, Verb, Pronoun, Demonstrative, etc.) in subpage sections.
- **`App.jsx`** — Added `detailId` state (from `?detail=` URL param). Conditional rendering: table body vs `WordDetailPage`. Back button preserves filter state. Import `WordDetailPage` from TableView.
- **`App.css`** — PoS inline tag styles (`.pos-tag-inline`, `.gloss-sep`, `.gloss-more`). Detail subpage layout (`.word-detail-page`, `.detail-identity-card`, `.detail-content-columns`, `.detail-main`, `.detail-sidebar`). PoS section headers (`.pos-section-header`, `.pos-meaning-list`). Responsive sidebar collapse. Back button, "View full entry" link.
- **`db.js`** — `queryWords` now selects `GROUP_CONCAT(m.pos, ' | ') AS poses_concat`. `enrichEntries` zips glosses with poses into `[{gloss, pos}]` arrays.

**DB / Backend:**
- **`data/kilor.db`** — `ALTER TABLE meanings ADD COLUMN pos TEXT DEFAULT ''`. Backfilled 483 meanings across 15 PoS tags (N, V, A, D, PRON, NUM, CCONJ, SCONJ, ADP, PART, MODAL, DEM, Q, CLF, INTERJ, PROPN).
- **`kilor/schema.py`** — `SCHEMA_SQL` includes `pos` column. Added `VALID_POS` frozenset (15 tags + empty for legacy). Added `POS_LABELS` dict mapping tags to display names.
- **`kilor/api.py`** — `_word_to_dict` returns meanings as `{"gloss": "...", "pos": "..."}` objects. Fixed search text aggregation for new format.
- **`kilor/commands/add.py`** — New `_parse_field()` function parses two `today.md` template formats: content word (per-PoS `Meaning (N)`, `Meaning (V)` fields) and function word (`POS` field + single `Meaning`). Inserts `pos` on all meanings rows. Comma-separated senses in per-PoS fields become multiple rows with same `pos`. Function words flag `is_function_word=1` and skip inflection generation. Legacy `| Meaning |` field still supported with empty `pos`.
- **`kilor/commands/edit.py`** — `--add-meaning` accepts optional `--pos` flag. `sort_order` now scoped within same `pos`. Import `VALID_POS` for validation.
- **`kilor/__main__.py`** — Wired `--pos` flag for `edit` command in CLI argument parser.

**Validation:**
- `python kilor.py check` — ✅ 22 errors / 1,224 warnings (all pre-existing)
- Frontend build: ✅ 44 modules, 551ms, no new errors

---

## workspace v1.0.0 — 2026-07-26

Dictionary frontend overhaul: sticky table headers, bidirectional sort, relevance-ranked search, inflection/case form search, fuzzy "Did you mean?" fallback, IPA notation, filter chips, keyboard shortcuts, autocomplete, copy-to-clipboard, URL state persistence. Backend: `search_text` column for precomputed search forms.

**Frontend — Layout:**
- **`kilor/dictionary/src/App.css`** — Grid-based layout (`grid-template-rows: auto auto auto 1fr`) with HTML body overflow lock. Table header row physically separated from scrollable body table. `border-collapse: separate` on body table. Sticky column headers replaced with fixed-position separate table. Fuzzy banner style, filter chips bar, autocomplete dropdown, search match highlighting (`mark.search-highlight`), toast notification, row-keyboard-selected outline.
- **`kilor/dictionary/src/components/TableView.jsx`** — Split into `TableHeader` (exports `TableHeader`, `TableBody`, default `TableView`). Shared `COLGROUP` with `table-layout: fixed` for column alignment. Sort arrows: inactive `↕`, active `▲`/`▼`. `highlightMatch()` for search term highlighting. `DetailPanel` shows inflections in N→V→A→D order, IPA line, single-mask tuple display. Copy-to-clipboard on word click with guard for jsdom environment.
- **`kilor/dictionary/src/components/Toolbar.jsx`** — Added search-wrapper div with autocomplete dropdown (`autocomplete-dropdown` UL). Autocomplete items navigable by arrow keys.
- **`kilor/dictionary/src/App.jsx`** — Added filter chips (FilterChips component), keyboard shortcuts (Esc/↑↓/Enter, gated to search focus), clipboard toast, fuzzy fallback with yellow banner, URL state read/write for shareable searches. Imports `fuzzySearch`, `autocompleteSearch`. `handleSort` refactored from nested-state-updater to flat if/else.
- **`kilor/dictionary/src/main.jsx`** — Unchanged.

**Frontend — Data Layer:**
- **`kilor/dictionary/src/db.js`** — Major additions:
  - `queryWords()`: 4-tier relevance scoring via `CASE WHEN` (form-prefix > form-contains > search_text > gloss). WHERE clause includes `w.search_text` for inflection/case form matching. Search overrides sortCol with relevance ordering.
  - `autocompleteSearch(term)`: top 5 form matches, prefix-priority ordered.
  - `fuzzySearch(term)`: Levenshtein distance ≤1 (≤3 chars) / ≤2 (4–6 chars) / ≤3 (7+ chars). Returns enriched entries with `fuzzyDistance`.
  - `computeInflections(form, syl_count, derivationMask)`: client-side inflection computation from prosody rules — 1–2 syl toneless (N/V=bare, A/D=+s), 3+ syl tone markers (j on 1st of last-3 for N/V, 2nd for A/D; v on 1st for V, 2nd for D). Single-mask words return `[base, tonemarked]` tuples. N→V→A→D order. Replaces stored `inflections` table.
  - `toIPA(word)`: full IPA mapper from `phonology.md` — 7 monophthongs, 7 diphthongs, 34 consonants. Tone markers: j→˥, v→˩.
  - `_syllablePositions(word)`: tone-preserving syllable splitter for inflection anchor calculation.
  - `enrichEntries(rows)`: batch enrichment — 4 queries per result set instead of N×4 (from 40,000 queries at 10k results to 4). Wired to `computeInflections` + `toIPA`.
  - `buildTestDB()`: Added `search_text` column.

**Backend:**
- **`kilor/schema.py`** — Added `search_text TEXT DEFAULT ''` column to `words` table.
- **`kilor/db.py`** — Added `populate_search_text(conn)`: computes all inflection forms (toneless + tonemarked) + case forms (ACC, GEN) per word and stores in `search_text`. Auto-creates column if missing. Called after DB changes.
- **`kilor/commands/add.py`** — Calls `populate_search_text()` after inserting new words.
- **`kilor/commands/edit.py`** — Calls `populate_search_text()` after any edit (mask change, typo fix, prefix, meaning, example).

**DB:**
- **`data/kilor.db`** — `search_text` column populated for all 400 existing entries via `populate_search_text()` migration.
- DB size may have changed due to new column and extended text data.

**Validation:**
- `python kilor.py check` — Not yet verified (please run before finalizing this entry).
- `npx vitest --run src/App.test.jsx` — 15/24 pass. 5 pre-existing `'361'` vs `'400'` count mismatch failures. 4 URL state cross-test contamination (all pass individually).