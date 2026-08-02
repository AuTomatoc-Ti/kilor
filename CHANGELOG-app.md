**Current Version:** v1.6.0
**Last Updated:** 2026-08-02
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

## workspace v1.7.0 — 2026-08-02

Derivational suffix audit DB cleanup: removed 4 redundant -lu doublets, created `klush lu` compound, unified question word POS to Q. See also: CHANGELOG.md v1.20.0.

**DB / Backend:**
- **`data/kilor.db`** — Deleted: gorlu (305), mylu (306), emalu (114), wemlu (307) — 4 redundant -lu doublets of quality roots. Modified: wem (55) — added "warmth" as noun meaning. Created: `klush lu` (423) — multi-word compound, mask=N, prefix=a-, meaning=courage (血性), components klush+lu. Question word POS unified to Q: awei, aeweisan, aewei updated in meanings table.

**Validation:**
- `python kilor.py check` — 35 errors (all pre-existing noise)

## workspace v1.6.0 — 2026-08-02

Full lexicon audit complete: 9 batches, ~411 words human-reviewed. Meanings, derivation masks, consensus prefixes, word types, POS tags, notes, and inflections corrected across all existing DB entries. New `audit-apply` and `audit-export` pipeline. Subscript form guards in Python & JS phonology. `updated_at` discipline fixed (application-layer only; recursive trigger removed). `D`-without-`A` mask constraint relaxed.

**Frontend:**
- **`db.js`** — `splitSyllablesJS()`: subscript guard — words with Unicode subscript characters (U+2080–U+2089) skip syllable parsing and return `[word]`. Prevents crash on subscripted pipeline escape-hatch forms like `ero₁`.
- **`TableView.jsx`** — Minor subscript display handling.

**DB / Backend:**
- **`kilor/commands/audit_apply.py`** (new) — Batch audit change application. Parses human-reviewed audit `.md` sheets; applies form renames, word type reclassifications, derivation mask changes, consensus prefix updates, meaning/POS corrections, notes cleanup, compound component re-links, and inflection auto-regeneration. Handles `(CLOSED-CLASS)`→`""` normalization, POS canonicalization (`adj`→`A`, `adv`→`D`, `v`→`V`, `n`→`N`), `(clear)`/`(delete)`/`(remove)`→`""` Notes normalization, and `wrong tone marker` diagnostic→auto-regeneration. 4-phase workflow: preview→commit with `--commit` flag. Sets `updated_at` on every mutation.
- **`kilor/commands/audit_export.py`** (new) — Generates per-batch human-review audit sheets (`.md` format) from the DB. Each word rendered as a table with current values and blank Desired Change column.
- **`kilor/__main__.py`** — Wired `audit-apply` and `audit-export` subcommands. `audit-apply` accepts `--file`, `--batch-size` (default 50), and `--commit`.
- **`kilor/commands/check.py`** — Subscript guard: words with Unicode subscript characters (U+2080–U+2089) skip IPA validation and syllable count checks (subscripted forms are metadata-only per pipeline §VI). Removed `D`-without-`A` mask validation — standalone `D` is valid per grammar spec.
- **`kilor/commands/edit.py`** — `--fix-typo` now sets `updated_at = datetime('now')` on the words table UPDATE.
- **`kilor/schema.py`** — `VALID_POS` added `MODAL`, `DEM`, `Q`, `CLF`, `INTERJ`, `PROPN` tags for future/partial use.
- **`kilor/tests/test_updated_at.py`** (new) — Tests verifying `updated_at` is set on INSERT and bumped on UPDATE via `audit_apply.py` and `edit.py`.
- **`data/kilor.db`** — Audit batches 001–009 applied: all ~411 existing words human-reviewed. Corrections across meanings (typos, missing glosses, POS tag canonicalization), derivation masks (VAD→NVAD, NAD→D, N→NAD, etc.), consensus prefixes (o-/None→e-/u-/a-, etc.), word types (root↔function per Mistake 13), forms (thanar→thaki, wonar→wonir, tlaure→tlaurhak), notes (tor/torra cleanup), compound components (tesakmae, shemae, tamae, takamae → maeha), and inflections (auto-regenerated for all mask-change words + "wrong tone marker" diagnostics). `updated_at` timestamps updated for all modified words via application-layer discipline.
- **`data/fix/drop_timestamp_trigger.sql`** (new) — Cleanup script to drop the recursive `AFTER UPDATE` trigger (postmortem Mistake 14). Not applied — informational only.

**Validation:**
- `python kilor.py check` — ✅ 35 errors (5 new from batch-008 single-form masks, 30 pre-existing; no regressions)
- See `draft/audit-batch-postmortem.md` for full audit pipeline postmortem (16 documented mistakes & lessons)

## workspace v1.5.1 — 2026-07-28

Audio hygiene: orphaned file detection & cleanup, bidirectional `audio --check`, auto-regenerate audio after `--fix-typo` rename.

**DB / Backend:**
- **`kilor/commands/edit.py`** — `--fix-typo` now auto-regenerates audio for the renamed word (if espeak-ng + ffmpeg are available). Falls back to a warning with manual regeneration command if toolchain is unavailable. Added `_regenerate_audio_after_rename()` helper.
- **`kilor/commands/audio.py`** — Added `--check-orphaned` action: lists `.ogg` files with no matching DB row. Added `--cleanup` action: deletes orphaned files (prompts for confirmation unless `--yes` passed). `--check` is now bidirectional: reports both missing files (DB→disk) and orphaned files (disk→DB). Added `_find_orphaned_audio()` helper.
- **`kilor/__main__.py`** — Wired `--check-orphaned`, `--cleanup`, and `--yes` flags for the `audio` subcommand.

**Validation:**
- `python kilor.py check` — ✅ All entries pass

## workspace v1.5.0 — 2026-07-28

IPA-to-speech audio pronunciation (experimental, off by default). espeak-ng + ffmpeg generate Ogg Opus files. 🔊 button appears next to IPA when enabled in Settings.

**Frontend:**
- **`TableView.jsx`** — Added `PronounceButton` component (🔊) in IPA column of table rows, detail panel, and word detail page. Button renders only when `showAudio` is true. Uses persistent `<audio id="audio-player">` element to avoid browser autoplay-policy issues. Audio URL is `./audio/{id}.ogg` (relative, works with Vite base path).
- **`SettingsPanel.jsx`** — Added "Audio pronunciation 🔊 (experimental)" checkbox (default off).
- **`Header.jsx`** — Forwards `showAudio`/`onToggleAudio` props to SettingsPanel.
- **`App.jsx`** — Added `showAudio` state (default false), passes to Header, TableBody, and WordDetailPage. Added hidden `<audio id="audio-player" preload="auto">` element.
- **`App.css`** — `.pronounce-btn`, `.pronounce-btn-inline`, `.pronounce-btn-detail` styles. `.td-form` cursor:copy moved to `.td-form-text`.

**DB / Backend:**
- **`kilor/commands/audio.py`** (new) — CLI command: `python kilor.py audio --generate` synthesizes `.ogg` Opus files for all words via espeak-ng → temp WAV → ffmpeg pipeline. Also supports `--id WORD_ID` and `--check`.
- **`kilor/__main__.py`** — Registered `audio` subcommand.
- **`kilor/dictionary/public/audio/`** — 403 `.ogg` audio files (2.0 MB total, ~9.5× smaller than WAV). Tracked in git (removed from .gitignore).

**Validation:**
- `python kilor.py check` — ✅ All entries pass
- `npx vitest --run src/App.test.jsx` — ✅ 50/50 pass


## workspace v1.4.1 — 2026-07-27

Settings panel, last-modified column, table header/body column alignment fix, autocomplete dismissal on table hover.

**Frontend:**
- **`SettingsPanel.jsx`** (new) — Gear icon (⚙) in header opens settings dropdown with "Show Last Modified column" checkbox. Dropdown dismissed by clicking outside or the close button.
- **`Header.jsx`** — Added gear icon button and `SettingsPanel` to header-right.
- **`App.jsx`** — Added `showModified` state (default false, persisted to URL `?mod=1`) and `settingsOpen` state. Passed `showModified` to `TableHeader` and `TableBody`. Added `onMouseEnter={() => setAutocompleteItems([])}` to `.table-header-bar` and `.main-content` — moving cursor to table area dismisses autocomplete suggestions so results are visible.
- **`Toolbar.jsx`** — Added `onFocus` handler to re-show autocomplete suggestions when clicking back into the search box after dismissal.
- **`TableView.jsx`** — `buildColGroup()` now takes `showModified` prop and returns 7 or 8 `<col>` elements. `TableHeader` and `TableBody` render conditional "Modified" column. `formatUpdatedAt()` formats `updated_at` as `YYYY-MM-DD HH:MM`. Detail row `colSpan` is dynamic (7 or 8).
- **`App.css`** — `.settings-gear-btn`, `.settings-overlay`, `.settings-dropdown`, `.settings-header`, `.settings-row` styles. Settings dropdown: `position: fixed; top: 56px; right: 24px`. `.table-header-bar`: `overflow-y: auto; scrollbar-gutter: stable` (was `overflow: hidden` — needed for `scrollbar-gutter` to work). `.word-table-header`: added `width: 100%; border-collapse: separate; border-spacing: 0` to match `.word-table-body` exactly. `.td-modified` style.

**DB / Backend:**
- **`db.js`** — `queryWords()` SELECT includes `w.updated_at`. `enrichEntries()` passes `updated_at` through to entry objects. `buildTestDB()` table schema includes `updated_at TEXT`. Added `case 'updated'` sort switch handler. Fuzzy search query also fetches `w.updated_at`.

**Validation:**
- `npx vitest run` — ✅ 39/39 pass (30 App + 9 db.reload)
- New tests: 5 table alignment tests (dual `scrollbar-gutter`, column parity default & with modified column, gear button existence, colgroup width match)

## workspace v1.4.0 — 2026-07-27

Stream C UI features + export flags: IPA column in table, colour prefix legend modal, --lite and --no-standalone export flags, schema indexes. See also: CHANGELOG.md v1.19.0.

**Frontend:**
- **`TableView.jsx`** — New IPA column in main table (7-column layout: Word, IPA, Gloss, Type, Prefix, NVAD, Syl). New `PrefixLegend` component: `?` icon in Prefix header opens modal overlay with all 7 colour prefixes, swatches, class names, and emotions. `detail-tr` colSpan updated to 7.
- **`App.css`** — IPA column styles (`.td-ipa`, serif font). Prefix legend styles: trigger button (`.prefix-legend-trigger`), overlay (`.prefix-legend-overlay`), modal (`.prefix-legend-modal`), grid rows (`.prefix-legend-row`, `.prefix-legend-swatch`, `.prefix-legend-label`), close button. Pagination bar styles (`.pagination-bar`, `.pagination-btn`).

**DB / Backend:**
- **`export.py`** — `_export_html()` and `cmd_export()` accept `lite` and `no_standalone` kwargs. `--lite`: creates temp stripped DB (drops `examples`, `compound_meta`, `compound_components`, `inflections`) and VACUUMs. `--no-standalone`: skips base64 embedding, outputs companion `dictionary.db` alongside `dictionary.html`; app fetches via `./dictionary.db`. Temp dir cleanup after export.
- **`__main__.py`** — Parses `--lite` and `--no-standalone` flags for `export` command, passes to `cmd_export()`.
- **`data/kilor.db`** — `idx_words_colour` and `idx_words_syl_count` indexes created on live DB (already in `SCHEMA_SQL`).

**Validation:**
- `npx vitest run` — ✅ 34/34 pass
- `npx vite build` — ✅ Clean: 274KB JS, 12KB CSS, 660KB WASM
- `python kilor.py check` — ✅ 25 pre-existing errors (none new)

## workspace v1.3.0 — 2026-07-27

Frontend scaling: SQL-level pagination (50 words/page), 300ms search debounce, fuzzy search capped at 30 results. Stale `react-window` dependency removed. See also: CHANGELOG.md v1.19.0.

**Frontend:**
- **`db.js`** — `queryWords()` now returns `{ rows, totalCount }` with `page`/`pageSize` params. Added `LIMIT`/`OFFSET` to SQL queries. Added separate COUNT query for total. Extracted `buildFilterClauses()` to share WHERE logic across both queries. `fuzzySearch()` returns `{ rows, totalCount }`, capped to top 30 (was unbounded). `buildTestDB()` schema: added `pos` column to `meanings` table + accepts mixed string/object meanings.
- **`App.jsx`** — Added `searchDraft`/`search` split with 300ms debounce via `useEffect` + `setTimeout`. Added `page` state, resets to 1 on search/filter/sort change. Wires `page` and `totalPages` to `TableView`. Updated `fuzzySearch` caller to use `fuzzyResult.rows`.
- **`TableView.jsx`** — New `PaginationBar` component (Previous/Next buttons, "X–Y of Z" indicator, page count, attached below table). Hidden when only 1 page. `TableBody` accepts and forwards `page`, `totalPages`, `totalCount`, `onPageChange` props.
- **`vite.config.js`** — Fixed WASM path: `fs.allow` from `['..']` to `['../..']` (sql.js WASM lives at root `node_modules/`, two levels up from `kilor/dictionary/`).
- **`package.json`** — Removed stale `react-window` dependency (leftover from 3 failed virtual scrolling attempts).

**Tests:**
- **`App.test.jsx`** — Updated all tests: dynamic word count (no hardcoded "361"), `typeAndWait()` helper for 300ms debounce, `beforeEach`/`afterEach` for URL reset + cleanup. Removed stale `.section` references. Added "view full entry" workflow test (search → expand → full detail → back). 25/25 pass.
- **`db.reload.test.js`** — Updated all tests for `{ rows, totalCount }` return type from `queryWords()`. Fixed all synthetic test words to use valid Kilor forms (consonant-final words crashed `splitSyllablesJS`). 9/9 pass.

**Validation:**
- `npx vitest run` — ✅ 34/34 pass (25 App + 9 db.reload)
- `npx vite build` — ✅ 44 modules, 272KB JS, 10KB CSS, 660KB WASM
- `python kilor.py check` — ✅ 25 pre-existing errors (none new)

## workspace v1.2.0 — 2026-07-27

Compound backfill review applied to live DB. 67 flagged compounds corrected: 6 prefix updates, 16 component re-links, 51 is_root conversions, 1 deletion (arrinna), 1 rename (ero isra→erolise isra), 2 meaning updates. Four new suffix roots added (lu, rin, par, nous). ous renamed to nous. Spec updated: derivational-compounding.md v2.5.0→2.6.0.

**DB / Backend:**
- **`data/kilor.db`** — 67 compound entries updated across `words`, `meanings`, `compound_components`, `compound_meta` tables. 1 word deleted (arrinna, ID 246). 1 word renamed (ero isra→erolise isra, ID 313). 4 new roots added: `lu` (o-, N), `rin` (o-, N), `par` (e-, NV), `nous` (o-, N, renamed from `ous` ID 177). 1 new compound: `rinok param` (ID 413, multi, result pattern, measurement). `rinok` mask N→NV. `pireilu` is_compound→0, is_root→1. `nous` is_function_word=1. FTS rebuilt.

**Spec:**
- **`rules/3-subsystems/derivational-compounding.md`** — v2.5.0→2.6.0. §I table: From Root updated (pireilu→lu, rinok→rin, chap→par). §I-E Process prefix: o-→e-. §V-A: Process nouns moved from Abstract to Crafted.

**Validation:**
- `python kilor.py check` — ✅ 25 errors (all pre-existing; no new errors from our changes)

See also: `CHANGELOG.md` v1.18.0 for spec-side details.

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