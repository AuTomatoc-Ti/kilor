# Kilor Dictionary App

A searchable, filterable dictionary SPA for the Kilor constructed language. Built with React 19 + Vite, powered by a SQLite database via [sql.js](https://sqljs.org/).

## Two Ways to Use It

### Option A — Open the Pre-built HTML (Quickest)

After running the export command:

```bash
python kilor.py export --format html
open data/dictionary.html
```

The export command runs `npm run build` (Vite), inlines all JS/CSS, base64-encodes `kilor.db` and the SQLite WebAssembly runtime, and produces a **single self-contained HTML file** at `data/dictionary.html`. No server needed — it works from `file://`.

### Option B — Dev Server (for Editing the UI)

```bash
# 1. Install dependencies (once)
npm install

# 2. Start the Vite dev server
npm run dev
```

Opens at `http://localhost:3000`. Hot-reloads edits to `src/`. The dev server reads `public/kilor.db` (a symlink to `data/kilor.db` — always the live lexicon).

### Option C — Build Standalone HTML Manually

```bash
npm run build                          # Outputs to kilor/dictionary/dist/
python kilor.py export --format html   # Inlines dist + DB into data/dictionary.html
```

## Project Layout

```
kilor/dictionary/
├── index.html          # Vite entry point
├── vite.config.js      # Vite configuration (React plugin, port 3000)
├── public/
│   ├── kilor.db        # → symlink to ../../data/kilor.db (dev server only)
│   └── sql-wasm.wasm   # SQLite WebAssembly runtime
└── src/
    ├── main.jsx        # React root
    ├── App.jsx         # Main app: state, filtering, layout
    ├── App.css         # All styles
    ├── db.js           # SQLite layer — init, query, enrich entries
    └── components/
        ├── Header.jsx
        ├── Toolbar.jsx
        ├── Legend.jsx
        ├── TableView.jsx
        └── CardView.jsx
```

## How Data Flows

```
data/kilor.db  (SSOT)
    │
    ├─▶ public/kilor.db  (symlink, dev server)
    │        │
    │        ▼
    │   db.js → initSqlJs() → queryWords()
    │
    └─▶ export.py → base64-encode → data/dictionary.html  (production)
             │
             ▼
        Self-contained HTML with embedded DB + wasm
```

## Search & Filtering

The dictionary supports:

- **Text search** — matches word form, gloss, or examples
- **Section filter** — A–J semantic domains
- **Type filter** — roots, compounds, function words
- **Mask filter** — NVAD derivation mask (N, NA, VAD, etc.)
- **Sort** — by form, gloss, section, mask, syllable count, prefix, or type
- **Table/Card view** toggle
- **Component chip click** — clicking a compound component searches for that root