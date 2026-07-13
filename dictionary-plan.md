# Kilor Dictionary — Gap Analysis & Improvement Plan

**Status:** Planning
**Last updated:** 2026-07-13
**Target:** Local offline dictionary → eventual online deployment

---

## Overview

The existing dictionary (`data/dictionary.html` + `data/dictionary-data.json`) is a functional SPA with search and filtering across 317 words (241 content roots, 55 function words, 73 compounds). This document identifies what's missing to make it a complete, learner-friendly dictionary of Kilor.

**Design goals of Kilor this dictionary must serve:**
- Beautiful to hear, suited for music and poetry
- Intuitive and easy to learn and pronounce for beginners
- Typable on an English keyboard

**Deployment strategy:** Local-first. Polish the offline dictionary completely, then deploy to a static host (GitHub Pages) as the final step.

---

## Architecture: Frontend + Optional API Layer

### Current State

The dictionary consists of a single static HTML file (`data/dictionary.html`) that fetches a pre-generated JSON blob (`dictionary-data.json`). This is simple and offline-capable, but limits query capabilities and requires re-export after every database change.

### Proposed: Add Optional REST API

Split into two access paths — the static SPA remains the zero-dependency fallback; a new lightweight API server provides richer query access for AI agents and future frontend upgrades.

```
kilor/db.py                          ← Data access layer (SSOT, already exists)
    │
    ├── kilor/commands/export.py     ← Static export (HTML + JSON, already exists)
    │       └── data/dictionary.html ← Human: offline-capable SPA (no server needed)
    │
    └── kilor/api.py                 ← NEW: Lightweight REST API server
            ├── GET /api/words?q=&section=&category=&phase=&tags=
            ├── GET /api/words/{id}
            ├── GET /api/search?q=   (FTS5, returns ranked results)
            ├── GET /api/status      (lexicon stats, roadmap progress)
            └── GET /api/word-of-day
                │
                ├── AI agent (curl, MCP tool, any HTTP client)
                ├── Human browser (optional: SPA calls API for richer features)
                └── External tools (flashcard generators, corpus tools, etc.)
```

### Design Principles

1. **The API is optional, not mandatory.** The static `dictionary.html` still works by fetching `dictionary-data.json` — no server needed. The API is an *additional* access path. Preserves local-first, offline-capable design.

2. **Both share `kilor/db.py`.** No query logic duplication. The export command and the API server both call the same functions.

3. **AI agents get a clean HTTP interface.** Instead of needing Python + the `kilor` package, any agent can query via `curl` or any HTTP client. Trivially wrappable as an MCP tool later.

4. **The frontend can optionally upgrade.** The SPA can try fetching from the API first (for autocomplete, fuzzy search, real-time stats) and fall back to the static JSON if the API isn't running. Feature detection, not hard dependency.

### What the API Enables That Static JSON Cannot

| Capability | Static JSON | API |
|---|---|---|
| Full-text search (FTS5 ranked) | Client-side substring match | Server-side FTS5 with relevance ranking |
| Autocomplete (typeahead) | Precomputed prefix index (large JSON) | `GET /api/search?q=vol&limit=5` (fast) |
| Fuzzy/typo-tolerant search | Expensive client-side Levenshtein | Server-side with SQLite FTS5 prefix queries |
| Real-time data (no export step) | Stale until re-exported | Always queries live `kilor.db` |
| Word-of-day / random word | Precomputed | Dynamic query |
| Cross-reference resolution | Limited (static data) | JOIN queries across tables |
| Programmatic access by AI agents | Parse JSON or call CLI | Single `curl` call, structured JSON response |

### Implementation

- **Framework:** FastAPI (Python, auto-docs at `/docs`, async)
- **New file:** `kilor/api.py` (~100–150 lines of thin HTTP wrappers over `kilor/db.py`)
- **Dependencies:** `fastapi`, `uvicorn` (2 packages, standard Python ecosystem)
- **Run with:** `python -m uvicorn kilor.api:app --port 8765` or `python kilor.py serve`
- **Zero schema changes.** All query logic already exists in `kilor/db.py`.

### API Endpoints

| Method | Path | Parameters | Returns |
|---|---|---|---|
| GET | `/api/words` | `q`, `section`, `category`, `phase`, `tags`, `limit`, `offset` | Paginated word list with meanings, inflections, examples |
| GET | `/api/words/{id}` | — | Single word with full detail (components, meta, examples) |
| GET | `/api/search` | `q` (required), `limit` | FTS5-ranked search results |
| GET | `/api/status` | — | Lexicon statistics + roadmap progress (roots + total words) |
| GET | `/api/word-of-day` | — | Random word entry |

### Frontend API Integration Strategy (Deferred)

When the SPA is upgraded to optionally use the API:

```javascript
const API_BASE = 'http://localhost:8765';

async function fetchDictionary() {
  try {
    // Try API first
    const resp = await fetch(`${API_BASE}/api/words?limit=5000`, { signal: AbortSignal.timeout(2000) });
    if (resp.ok) return await resp.json();
  } catch {}
  // Fall back to static JSON
  const resp = await fetch('dictionary-data.json');
  return await resp.json();
}
```

### What to Avoid

- **Don't build a Node/Express backend.** Python is the project's language; adding a second runtime is unnecessary complexity.
- **Don't make the SPA require the API.** Offline-first is a feature, not a limitation.
- **Don't add write endpoints.** The API is read-only. Word creation remains via `kilor.py add` or direct SQLite access.
- **Don't add auth, users, or persistence layers.** Read-only, local-network-only is sufficient.

---

## Priority Tiers

| Tier | Definition |
|---|---|
| **P0 — Critical** | Blocks core dictionary functionality; no pronunciation data, no examples, no cross-links |
| **P1 — Important** | Significantly improves learner experience; colour philosophy, browse mode, inflection rules |
| **P2 — Polish** | Nice-to-have; PWA, autocomplete, section population |

---

## P0 — Critical Gaps

### 1. No Pronunciation Data

The dictionary shows syllable count but nothing about *how a word sounds*. For a language designed for beauty of sound, this is the #1 content gap.

**What's needed:**

| Field | Source | Display |
|---|---|---|
| IPA transcription | New DB column `ipa` on `words` table | Per-word, manual input |
| Syllable breakdown | Computable from `form` via `kilor/phonology.py` | Visual separator (e.g., `fo·ra·gi·lan`) |
| Tone visualization | `j` (high) and `v` (low) markers already in orthography | CSS: bold/colored tone markers |

**Schema change:**

```sql
ALTER TABLE words ADD COLUMN ipa TEXT;
```

**Display example:**

```
foragilan  [fo.ra.ˈɡi.lan]  — volcano
  syllables: fo·ra·gi·lan
  tones: j = high (marked in blue)
```

**Implementation notes:**
- `kilor/phonology.py` already has `count_syllables()`. Add a `split_syllables(form: str) -> list[str]` function.
- Update `kilor.py export --format html` and `kilor.py export --format dictionary` to include `ipa` in output.
- Update `data/dictionary.html` to render IPA field and syllable breakdown.

### 2. Sparse Example Sentences

Most entries have empty `examples` arrays. For a learner dictionary, every content word needs at least one canonical example showing usage. This is per-word content work.

**Target:** Every Phase 1 word (body parts, family, food, daily actions, etc.) should have at least 1 example sentence.

**Implementation notes:**
- The `examples` table and dictionary display code already exist.
- Use `kilor.py add` workflow or direct SQL INSERT (see `data/AI-GUIDE.md` §3).
- Prioritize: function words, compounds, multi-category words (e.g., `nv`, `na`, `av`).

### 3. No Entry Cross-Linking

**Compound → component roots:** Shown as plain text (`sori`, `leman`), not clickable links. Fix: render components as anchor links that filter/scroll to the component's entry.

**Function words → grammar spec:** Entries like `res`, `kus`, `pona` have no link to their defining spec file. Add a `grammar_ref` field or reuse `compound_meta.rule_ref` pattern.

**Colour prefix → philosophy:** `consensus_prefix: "o-"` displayed with zero context. Should show ontological class name and link to `philosophy.md`.

**Implementation notes:**
- Compound component links: change `entryHTML()` in `dictionary.html` to render component names as `<a>` tags with `onclick` handlers that search/filter to that word.
- Grammar cross-references: add `rule_ref` column to `words` table (or reuse notes field convention).
- Prefix context: static mapping from prefix code to label + colour in the dictionary JS.

### 4. Roadmap Progress Tracks Roots Only, Not Total Words

Current `kilor.py status` shows progress against root counts:

```
Phase 1 — Basic Daily: 314/500 = 62.8%
```

But the roadmap's real target is **total words** (roots + derived N/V/Adj/Adv + compounds):

| Phase | Root Target | Total Word Target |
|---|---|---|
| Phase 1 | 500 | ~1,750 |
| Phase 2 | 1,000 | ~3,500 |
| Phase 3 | 3,000 | ~10,500 |
| Phase 4 | 4,500 | ~15,750 |
| Phase 5 | 6,000 | ~21,000 |
| Phase 6 | 8,600 | ~30,100 |

**Revised display should be:**

```
Phase 1 — Basic Daily:
  Roots:    241 /   500 = 48.2%
  Words:    317 / 1,750 = 18.1%   (roots + derived + compounds)
```

**Implementation notes:**
- Modify `kilor/commands/status.py` to compute total surface forms.
- Derived forms = number of distinct inflection entries across content roots.
- Total words = roots + derived + compounds.
- Update `roadmap.md` to clarify tracking metric (track both roots and total words).

---

## P1 — Important Gaps

### 5. No Colour Philosophy Integration in Entries

`consensus_prefix` is displayed as a raw string (`o-`). Should show:

```
Prefix: o- (Abstract / Void — Surprise)   🟣
```

**Implementation notes:**
- Static mapping in dictionary JS or embedded in export data:
  ```javascript
  const prefixInfo = {
    "a-": { class: "Alive / Energy", emotion: "Anger", color: "#ef4444" },
    "e-": { class: "Crafted / Tool", emotion: "Joy", color: "#f59e0b" },
    "i-": { class: "Fluid / Vast", emotion: "Sadness", color: "#3b82f6" },
    "o-": { class: "Abstract / Void", emotion: "Surprise", color: "#8b5cf6" },
    "u-": { class: "Organic / Growth", emotion: "Calm", color: "#22c55e" },
    "y-": { class: "Dense / Mass", emotion: "Fear", color: "#6b7280" },
    "ae-":{ class: "Earth / Boundary", emotion: "Disgust", color: "#a16207" },
  };
  ```
- Add prefix info to `dictionary-data.json` export (include in entry or as a top-level lookup table).
- Link to `rules/0-foundation/philosophy.md` for full context.

### 6. No Learning Browse Mode

The dictionary is a flat, search-driven list. Missing:
- Browse by **Phase** (Phase 1 = body parts, family, food, daily actions, etc.)
- Browse by **semantic subcategory** (aligned with `wordlist/` groupings)
- **Related words** (same-category, synonyms, antonyms)

**Implementation notes:**
- Add a `phase` column to `words` table (INTEGER, 1–6) or derive from wordlist membership.
- Add a `tags` column for semantic subcategories (e.g., `body-part`, `food`, `kinship`).
- Add a browse panel to the dictionary UI: collapsible category tree or tab bar.
- The `wordlist/` directory already organizes English targets by category — align with this.

**Schema changes:**

```sql
ALTER TABLE words ADD COLUMN phase INTEGER;
ALTER TABLE words ADD COLUMN tags TEXT;  -- JSON array or comma-separated
```

### 7. No Inflection Rule Explanation

Inflected forms are shown (e.g., `aerdis` for adjective/adverb) but there's zero explanation of *why* `-s` is there. A learner sees the form but doesn't learn the rule.

**Fix:** In the entry detail view, next to each inflection form, show a brief rule note:

```
Inflections:
  noun      aerdi
  verb      aerdi
  adjective aerdis    (root + derivational -s)
  adverb    aerdis    (root + derivational -s)
```

**Implementation notes:**
- Display-only change in `data/dictionary.html` `entryHTML()` function.
- For 1–2 syllable content roots: show `(root + -s)` on adj/adv rows.
- For 3+ syllable roots with tone: show `(root + j/v tone marker + -s)`.

---

## P2 — Polish Gaps

### 8. Underpopulated Sections

| Section | Domain | Count | Status |
|---|---|---|---|
| A | Worlds & Elements | 41 | OK |
| B | Living Things | 16 | Light |
| C | Physical Objects | 16 | Light |
| D | Actions & Motion | 20 | Light |
| E | Qualities & States | 22 | OK |
| F | Mind & Emotion | 8 | **Underpopulated** |
| G | Time & Space | 66 | Good |
| H | Social & Relational | 26 | OK |
| I | Abstract | 70 | Good |
| J | Sensation | 2 | **Nearly empty** |
| - | Unassigned | 30 | **Needs triage** |

**Action:** Prioritize Phase 1 wordlist items that fall under sections F and J. Triage the 30 unassigned entries.

### 9. Search Enhancements

- No autocomplete / suggestion dropdown as user types
- No fuzzy search (typo tolerance for English glosses)
- No search by Kilor prefix/rhyme

**Implementation notes:**
- Autocomplete: debounced input → filter first N matches → dropdown below search bar.
- Fuzzy search: use a simple Levenshtein distance or FTS5 with prefix queries.
- Prefix/rhyme search: regex on `form` field, or add a dedicated filter.

### 10. PWA / Offline Support

The dictionary is a single HTML + JSON pair — making it installable as a PWA is low effort.

**Implementation notes:**
- Add a `manifest.json` with app name, icon, theme color.
- Add a service worker that caches `dictionary.html` and `dictionary-data.json`.
- Register the service worker in the HTML.
- **Defer** until content is richer (more entries, examples, IPA).

---

## Schema Changes Needed

Summary of all proposed database changes:

| Change | Table | Column | Type | Purpose |
|---|---|---|---|---|
| ADD | `words` | `ipa` | TEXT | IPA pronunciation |
| ADD | `words` | `phase` | INTEGER | Learning phase (1–6) |
| ADD | `words` | `tags` | TEXT | Semantic subcategory tags |
| ADD | `words` | `grammar_ref` | TEXT | Link to grammar spec file |

---

## Export Changes Needed

The `kilor.py export --format html` and `--format dictionary` commands need updates:

1. Include `ipa`, `phase`, `tags`, `grammar_ref` in the JSON output.
2. Include `prefix_info` lookup table at top level of JSON (or per-entry prefix context).
3. Include syllable breakdown (computed).
4. Include tone-highlighted form (computed).

---

## Dictionary HTML Changes Needed

1. **Pronunciation display:** IPA field, syllable breakdown with visual separator, tone marker highlighting.
2. **Cross-linking:** Compound components as clickable links; function words link to grammar spec.
3. **Prefix context:** Show ontological class + emotion + colour swatch for `consensus_prefix`.
4. **Inflection rules:** Show brief rule note next to each inflection form.
5. **Browse mode:** Phase/category browse panel (collapsible tree or tabs).
6. **Autocomplete:** Search bar suggestions dropdown.

---

## Implementation Order

```
Phase A — Foundations (engineering, low effort)
  ├── Build API server (kilor/api.py) — FastAPI REST endpoints over kilor/db.py
  ├── 4. Roadmap progress: track total words, not just roots (in status.py + API /api/status)
  ├── 5. Colour prefix contextual display
  ├── 7. Inflection rule explanation
  └── 3. Entry cross-linking (compound → components)

Phase B — Content foundation (content work, high effort)
  ├── 1a. Add IPA transcription to existing entries
  ├── 1b. Syllable breakdown display
  ├── 1c. Tone visualization
  └── 2. Example sentences for Phase 1 words

Phase C — Learner experience (engineering, medium effort)
  ├── 6. Learning browse mode
  └── 9. Search enhancements (autocomplete, fuzzy)

Phase D — Section population (content work)
  └── 8. Populate sections F, J; triage unassigned entries

Phase E — Future
  ├── Audio generation / TTS (deferred)
  └── 10. PWA offline support (deferred)
```

---

## Related Files

| File | Relevance |
|---|---|
| `data/dictionary.html` | Dictionary SPA — all display changes go here |
| `data/dictionary-data.json` | Exported data consumed by SPA |
| `kilor/api.py` | **NEW** — REST API server (FastAPI) for AI agent & frontend access |
| `kilor/commands/export.py` | Export command — generates dictionary JSON + HTML |
| `kilor/commands/status.py` | Status command — roadmap progress display |
| `kilor/phonology.py` | Phonology utilities — syllable splitting, tone detection |
| `kilor/db.py` | Database access — FTS rebuild, queries (shared by export + API) |
| `data/AI-GUIDE.md` | AI agent guide for adding entries |
| `data/SCHEMA.md` | Database schema reference |
| `roadmap.md` | Phase targets and wordlist categories |
| `rules/0-foundation/philosophy.md` | SSOT for 7 dual-concepts (prefix meanings) |
| `wordlist/` | English target words organized by semantic category |

---

*End of plan.*