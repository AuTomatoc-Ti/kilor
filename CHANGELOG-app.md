**Current Version:** v1.0.0
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