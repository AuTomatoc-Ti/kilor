"""Export lexicon to CSV, JSON, HTML dictionary, or dictionary data."""

import csv
import json
import os
import re
import subprocess
from datetime import datetime

from ..db import get_db, rebuild_fts
from ..phonology import get_case_forms
from ..schema import SECTION_LABELS

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _export_csv(conn):
    """Export to legacy CSV format."""
    words = conn.execute(
        """SELECT w.*, GROUP_CONCAT(m.gloss, ' / ') as meanings_concat
           FROM words w LEFT JOIN meanings m ON w.id = m.word_id
           GROUP BY w.id ORDER BY w.id"""
    ).fetchall()

    output_path = os.path.join(SCRIPT_DIR, "data", "lexicon_export.csv")
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "form", "syl_count", "meaning", "derivation_mask", "section",
            "noun", "verb", "adjective", "adverb",
            "consensus_prefix", "is_function_word", "is_compound",
            "compound_type", "notes",
        ])
        for w in words:
            infls = {}
            for row in conn.execute(
                "SELECT form_type, form FROM inflections WHERE word_id = ?", (w["id"],)
            ).fetchall():
                infls[row["form_type"]] = row["form"]

            writer.writerow([
                w["form"], w["syl_count"],
                w["meanings_concat"] or "",
                w["derivation_mask"], w["section"],
                infls.get("noun", ""), infls.get("verb", ""),
                infls.get("adjective", ""), infls.get("adverb", ""),
                w["consensus_prefix"] or "o-",
                "true" if w["is_function_word"] else "false",
                "true" if w["is_compound"] else "false",
                w["compound_type"] or "",
                w["notes"] or "",
            ])

    print(f"Exported to {output_path}")


def _export_json(conn):
    """Export compounds to JSON."""
    compounds_export = {}
    compound_words = conn.execute(
        """SELECT w.*, cm.pattern, cm.rule_ref
           FROM words w LEFT JOIN compound_meta cm ON w.id = cm.compound_id
           WHERE w.is_compound = 1 ORDER BY w.id"""
    ).fetchall()

    for cw in compound_words:
        comps = conn.execute(
            """SELECT w2.form FROM compound_components cc
               JOIN words w2 ON cc.component_id = w2.id
               WHERE cc.compound_id = ? ORDER BY cc.position""",
            (cw["id"],),
        ).fetchall()

        meanings = conn.execute(
            "SELECT gloss FROM meanings WHERE word_id = ? ORDER BY sort_order",
            (cw["id"],),
        ).fetchall()
        meaning_str = " / ".join(m["gloss"] for m in meanings)

        compounds_export[cw["form"]] = {
            "type": cw["compound_type"],
            "meaning": meaning_str,
            "construction": [c["form"] for c in comps],
            "pattern": cw["pattern"] or "",
            "in_lexicon": cw["compound_type"] == "mono",
        }
        if cw["rule_ref"]:
            compounds_export[cw["form"]]["rule_ref"] = cw["rule_ref"]

    output = {
        "_last_updated": datetime.now().strftime("%Y-%m-%d"),
        "_total": len(compounds_export),
        "compounds": compounds_export,
    }

    output_path = os.path.join(SCRIPT_DIR, "data", "compounds_export.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Exported to {output_path}")


def _export_html(conn):
    """Export a self-contained searchable dictionary SPA.

    Generates dictionary-data.json, runs Vite build, and inlines
    all assets + data so the dictionary works from file: URLs.
    """
    # Build React app with Vite
    dict_dir = os.path.join(SCRIPT_DIR, "kilor", "dictionary")
    dist_dir = os.path.join(dict_dir, "dist")
    print("Building React app with Vite...")
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("WARNING: npm run build failed — falling back to legacy template.")
        print("stderr:", result.stderr[:500])
        html_content = _get_inline_html()
    else:
        static_html_path = os.path.join(dist_dir, "index.html")
        if os.path.exists(static_html_path):
            with open(static_html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            # Inline assets from the dist directory
            assets_dir = os.path.join(dist_dir, "assets")
            html_content = _inline_assets(html_content, assets_dir)
        else:
            print("WARNING: Vite dist/index.html not found — using fallback.")
            html_content = _get_inline_html()

    # Base64-encode kilor.db and sql-wasm.wasm for truly self-contained HTML
    import base64
    db_path = os.path.join(SCRIPT_DIR, "data", "kilor.db")
    with open(db_path, "rb") as bf:
        db_b64 = base64.b64encode(bf.read()).decode("ascii")
    print(f"Encoded kilor.db: {len(db_b64)} base64 chars")

    wasm_path = os.path.join(dict_dir, "public", "sql-wasm.wasm")
    with open(wasm_path, "rb") as wf:
        wasm_b64 = base64.b64encode(wf.read()).decode("ascii")
    print(f"Encoded wasm: {len(wasm_b64)} base64 chars")

    inline = (
        '<script>window.__SQL_WASM_B64__="' + wasm_b64 + '";'
        'window.__KILOR_DB_B64__="' + db_b64 + '";</script>'
    )
    html_content = html_content.replace("<!-- DATA_PLACEHOLDER -->", inline)

    # Write self-contained output
    html_path = os.path.join(SCRIPT_DIR, "data", "dictionary.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Exported self-contained dictionary to {html_path}")


def _inline_assets(html, assets_dir):
    """Inline CSS and JS assets referenced in HTML. Returns modified HTML."""
    # Inline CSS: find <link rel="stylesheet" ... href="/assets/name.css">
    css_pattern = re.compile(
        r'<link\s+rel="stylesheet"\s+crossorigin\s+href="([^"]+)"\s*/?>'
    )
    for m in css_pattern.finditer(html):
        url = m.group(1)
        filename = os.path.basename(url)
        css_path = os.path.join(assets_dir, filename)
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            html = html.replace(m.group(0), '<style>\n' + css_content + '\n</style>')

    # Inline JS: find <script type="module" crossorigin src="/assets/name.js"></script>
    js_pattern = re.compile(
        r'<script\s+type="module"\s+crossorigin\s+src="([^"]+)"\s*></script>'
    )
    for m in js_pattern.finditer(html):
        url = m.group(1)
        filename = os.path.basename(url)
        js_path = os.path.join(assets_dir, filename)
        if os.path.exists(js_path):
            with open(js_path, "r", encoding="utf-8") as f:
                js_content = f.read()
            html = html.replace(m.group(0), '<script type="module">\n' + js_content + '\n</script>')

    return html


def _get_inline_html():
    """Return the SPA HTML template (embedded fallback)."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kilor Dictionary</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: #f8f9fa; color: #1a1a2e; }
header { background: #1a1a2e; color: #fff; padding: 20px 24px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,.15); }
header h1 { font-size: 1.5rem; margin-bottom: 8px; }
header p { font-size: .85rem; opacity: .7; }
.toolbar { display: flex; gap: 10px; flex-wrap: wrap; padding: 16px 24px; background: #fff; border-bottom: 1px solid #e0e0e0; position: sticky; top: 80px; z-index: 99; align-items: center; }
#search { flex: 1; min-width: 220px; padding: 10px 14px; border: 1px solid #ccc; border-radius: 6px; font-size: 1rem; outline: none; }
#search:focus { border-color: #4a6cf7; box-shadow: 0 0 0 3px rgba(74,108,247,.15); }
.toolbar select { padding: 10px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: .9rem; outline: none; background: #fff; cursor: pointer; }
.toolbar select:focus { border-color: #4a6cf7; }
#result-count { font-size: .85rem; color: #666; white-space: nowrap; margin-left: 8px; }
.container { max-width: 960px; margin: 0 auto; padding: 20px 24px; }
.section-header { font-size: 1.25rem; font-weight: 700; color: #4a6cf7; margin: 32px 0 12px; padding-bottom: 6px; border-bottom: 2px solid #e0e0e0; display: flex; align-items: baseline; gap: 10px; }
.section-header .count { font-size: .85rem; color: #888; font-weight: 400; }
.entry { background: #fff; border-radius: 8px; margin: 8px 0; box-shadow: 0 1px 4px rgba(0,0,0,.06); overflow: hidden; transition: box-shadow .15s; }
.entry:hover { box-shadow: 0 2px 8px rgba(0,0,0,.1); }
.entry-header { display: flex; align-items: baseline; padding: 14px 18px; cursor: pointer; user-select: none; gap: 12px; flex-wrap: wrap; }
.entry-header:hover { background: #f4f6ff; }
.word { font-size: 1.25rem; font-weight: 700; color: #1a1a2e; }
.meanings { font-size: 1rem; color: #555; }
.meta-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-left: auto; }
.tag { font-size: .75rem; padding: 3px 8px; border-radius: 12px; font-weight: 500; }
.tag-mask { background: #e8f0fe; color: #1a56db; }
.tag-compound { background: #fef3c7; color: #92400e; }
.tag-function { background: #fce7f3; color: #be185d; }
.tag-root { background: #e0e7ff; color: #3730a3; }
.entry-body { display: none; padding: 0 18px 16px; border-top: 1px solid #f0f0f0; }
.entry.open .entry-body { display: block; }
.entry.open .entry-header { background: #f4f6ff; }
.detail-row { margin: 10px 0; font-size: .9rem; }
.detail-row strong { color: #555; min-width: 110px; display: inline-block; }
.infl-list { display: inline-flex; gap: 12px; flex-wrap: wrap; }
.infl-item { background: #f0f0f0; padding: 2px 10px; border-radius: 4px; font-size: .85rem; }
.infl-type { color: #888; font-size: .75rem; }
.component-list { display: inline-flex; gap: 8px; flex-wrap: wrap; }
.component-item { background: #fff7ed; padding: 2px 10px; border-radius: 4px; font-size: .85rem; color: #9a3412; }
.example-block { margin: 8px 0; padding: 10px 14px; background: #f8f9fa; border-left: 3px solid #4a6cf7; border-radius: 4px; font-size: .88rem; }
.example-block .kilor-text { font-weight: 600; color: #1a1a2e; }
.example-block .english-text { color: #666; margin-left: 8px; }
.example-block .source-tag { font-size: .7rem; color: #aaa; margin-left: 8px; }
.pattern-ref { display: inline-flex; gap: 8px; flex-wrap: wrap; }
.pattern-ref span { font-size: .8rem; background: #ede9fe; color: #5b21b6; padding: 2px 10px; border-radius: 4px; }
.no-results { text-align: center; padding: 60px 20px; color: #888; }
.no-results .icon { font-size: 2.5rem; margin-bottom: 12px; }
@media (max-width: 600px) {
  header { padding: 14px 16px; }
  .toolbar { padding: 12px 16px; flex-direction: column; }
  #search { min-width: unset; width: 100%; }
  .toolbar select { width: 100%; }
  .container { padding: 12px 16px; }
  .entry-header { flex-direction: column; gap: 6px; }
  .meta-tags { margin-left: 0; }
}
</style>
</head>
<body>
<header>
  <h1>Kilor Dictionary</h1>
  <p id="header-info">Loading...</p>
</header>

<div class="toolbar">
  <input type="text" id="search" placeholder="Search words, meanings, examples..." autofocus>
  <select id="filter-section">
    <option value="">All sections</option>
    <option value="1">1 — Concrete</option>
    <option value="2">2 — Living</option>
    <option value="3">3 — Action</option>
    <option value="4">4 — Quality</option>
    <option value="5">5 — Mental</option>
    <option value="6">6 — Relational</option>
    <option value="7">7 — Abstract</option>
    <option value="8">8 — Grammar</option>
  </select>
  <select id="filter-type">
    <option value="">All types</option>
    <option value="root">Roots</option>
    <option value="compound">Compounds</option>
    <option value="function">Function words</option>
  </select>
  <select id="filter-mask">
    <option value="">All masks</option>
    <option value="N">N — Noun</option>
    <option value="V">V — Verb</option>
    <option value="A">A — Adjective</option>
    <option value="D">D — Adverb</option>
    <option value="NAD">NAD — Noun/Adj/Adv</option>
    <option value="NV">NV — Noun/Verb</option>
    <option value="NA">NA — Noun/Adj</option>
    <option value="NVA">NVA — Noun/Verb/Adj</option>
    <option value="NVAD">NVAD — All</option>
    <option value="VAD">VAD — Verb/Adj/Adv</option>
    <option value="AD">AD — Adj/Adv</option>
    <option value="EMPTY">(closed-class)</option>
  </select>
  <span id="result-count"></span>
</div>

<div class="container" id="entry-container">
  <div class="no-results"><div class="icon">📖</div><p>Loading dictionary data...</p></div>
</div>

<!-- DATA_PLACEHOLDER -->

<script>
let allEntries = [];
let currentView = 'table';
let sortCol = 'form';
let sortDir = 'asc';

function loadDictionary() {
  try {
    var data = window.__DICT_DATA__;
    if (!data) {
      document.getElementById('entry-container').innerHTML = '<div class="no-results"><div class="icon">⚠️</div><p>No data found. Run: <code>python kilor.py export --format html</code></p></div>';
      return;
    }
    allEntries = data.entries;
    document.getElementById('header-info').textContent = data.meta.total_words + ' words · exported ' + data.meta.exported_at;
    render();
  } catch (err) {
    document.getElementById('entry-container').innerHTML = '<div class="no-results"><div class="icon">⚠️</div><p>Error: ' + err.message + '</p></div>';
  }
}

function getFilteredEntries() {
  const st = document.getElementById('search').value.toLowerCase().trim();
  const sf = document.getElementById('filter-section').value;
  const tf = document.getElementById('filter-type').value;
  const cf = document.getElementById('filter-mask').value;
  return allEntries.filter(e => {
    if (sf && e.section !== sf) return false;
    if (tf === 'root' && !e.is_root) return false;
    if (tf === 'compound' && !e.is_compound) return false;
    if (tf === 'function' && !e.is_function_word) return false;
    if (cf === 'EMPTY' && e.derivation_mask) return false;
    if (cf && cf !== 'EMPTY' && e.derivation_mask !== cf) return false;
    if (st) {
      const s = [e.form, ...e.meanings, ...e.components, ...e.examples.map(ex => ex.kilor + ' ' + ex.english), e.pattern || '', e.notes || ''].join(' ').toLowerCase();
      if (!s.includes(st)) return false;
    }
    return true;
  });
}
function render() {
  const filtered = getFilteredEntries();
  const container = document.getElementById('entry-container');
  document.getElementById('result-count').textContent = filtered.length === allEntries.length ? allEntries.length + ' words' : filtered.length + ' of ' + allEntries.length + ' words';
  if (filtered.length === 0) { container.innerHTML = '<div class="no-results"><div class="icon">🔍</div><p>No words match your search.</p></div>'; return; }
  const searchActive = !!document.getElementById('search').value.trim();
  const sectionActive = !!document.getElementById('filter-section').value;
  if (searchActive && !sectionActive) { container.innerHTML = filtered.map(e => entryHTML(e)).join(''); return; }
  const grouped = {};
  const sectionOrder = ['1','2','3','4','5','6','7','8'];
  for (const sec of sectionOrder) grouped[sec] = [];
  for (const e of filtered) { const sec = e.section || '7'; if (!grouped[sec]) grouped[sec] = []; grouped[sec].push(e); }
  let html = '';
  for (const sec of sectionOrder) {
    if (!grouped[sec] || grouped[sec].length === 0) continue;
    const secLabel = grouped[sec][0].section_label || 'Other';
    html += '<div class="section-header">' + sec + ' — ' + secLabel + '<span class="count">' + grouped[sec].length + '</span></div>';
    html += grouped[sec].map(e => entryHTML(e)).join('');
  }
  container.innerHTML = html;
}
function entryHTML(e) {
  const tags = [];
  tags.push('<span class="tag tag-mask">' + (e.derivation_mask || 'closed-class') + '</span>');
  if (e.is_function_word) tags.push('<span class="tag tag-function">function</span>');
  else if (e.is_compound) tags.push('<span class="tag tag-compound">' + e.compound_type + '-compound</span>');
  else if (e.is_root) tags.push('<span class="tag tag-root">root</span>');
  let detail = '';
  const inflKeys = Object.keys(e.inflections);
  if (inflKeys.length > 0) {
    detail += '<div class="detail-row"><strong>Inflections:</strong><span class="infl-list">';
    for (const [type, form] of Object.entries(e.inflections)) detail += '<span class="infl-item"><span class="infl-type">' + type + '</span> ' + esc(form) + '</span>';
    detail += '</span></div>';
  }
  if (e.components.length > 0) {
    detail += '<div class="detail-row"><strong>Components:</strong><span class="component-list">';
    for (const comp of e.components) detail += '<span class="component-item">' + esc(comp) + '</span>';
    detail += '</span></div>';
  }
  if (e.pattern || e.rule_ref) {
    detail += '<div class="detail-row"><strong>Pattern:</strong><span class="pattern-ref">';
    if (e.pattern) detail += '<span>' + esc(e.pattern) + '</span>';
    if (e.rule_ref) detail += '<span>' + esc(e.rule_ref) + '</span>';
    detail += '</span></div>';
  }
  if (e.case_forms && Object.keys(e.case_forms).length > 0) {
    detail += '<div class="detail-row"><strong>Case Forms:</strong><span class="infl-list">';
    if (e.case_forms.acc) detail += '<span class="infl-item" style="background:#e8f5e9">' + esc(e.case_forms.acc) + ' <span class="infl-type">(ACC)</span></span>';
    if (e.case_forms.gen) detail += '<span class="infl-item" style="background:#e3f2fd">' + esc(e.case_forms.gen) + ' <span class="infl-type">(GEN)</span></span>';
    detail += '</span></div>';
  }
  if (e.consensus_prefix && e.consensus_prefix !== 'o-') detail += '<div class="detail-row"><strong>Prefix:</strong> ' + esc(e.consensus_prefix) + '</div>';
  detail += '<div class="detail-row"><strong>Syllables:</strong> ' + e.syl_count + '</div>';
  if (e.notes) detail += '<div class="detail-row"><strong>Notes:</strong> ' + esc(e.notes) + '</div>';
  if (e.examples.length > 0) {
    detail += '<div style="margin-top:10px;"><strong style="color:#555;">Examples:</strong></div>';
    for (const ex of e.examples) detail += '<div class="example-block"><span class="kilor-text">' + esc(ex.kilor) + '</span><span class="english-text">— ' + esc(ex.english) + '</span><span class="source-tag">' + ex.source + '</span></div>';
  }
  return '<div class="entry" data-id="' + e.id + '"><div class="entry-header" onclick="this.parentElement.classList.toggle(\'open\')"><span class="word">' + esc(e.form) + '</span><span class="meanings">— ' + e.meanings.map(m => esc(m)).join(' / ') + '</span><span class="meta-tags">' + tags.join('') + '</span></div><div class="entry-body">' + detail + '</div></div>';
}
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
document.getElementById('search').addEventListener('input', render);
document.getElementById('filter-section').addEventListener('change', render);
document.getElementById('filter-type').addEventListener('change', render);
document.getElementById('filter-mask').addEventListener('change', render);
loadDictionary();
</script>
</body>
</html>"""


def _export_dictionary_data(conn):
    """Export complete dictionary data as JSON for the searchable SPA."""
    words = conn.execute("SELECT * FROM words ORDER BY form").fetchall()

    entries = []
    for w in words:
        meanings = [
            m["gloss"]
            for m in conn.execute(
                "SELECT gloss FROM meanings WHERE word_id = ? ORDER BY sort_order",
                (w["id"],),
            ).fetchall()
        ]

        inflections = {}
        for row in conn.execute(
            "SELECT form_type, form FROM inflections WHERE word_id = ?", (w["id"],)
        ).fetchall():
            inflections[row["form_type"]] = row["form"]

        components = []
        if w["is_compound"]:
            comps = conn.execute(
                """SELECT w2.form, w2.id, cc.position
                   FROM compound_components cc
                   JOIN words w2 ON cc.component_id = w2.id
                   WHERE cc.compound_id = ? ORDER BY cc.position""",
                (w["id"],),
            ).fetchall()
            components = [{"form": c["form"], "id": c["id"]} for c in comps]

        meta = conn.execute(
            "SELECT pattern, rule_ref FROM compound_meta WHERE compound_id = ?",
            (w["id"],),
        ).fetchone()

        examples = []
        for row in conn.execute(
            "SELECT kilor_text, english_text, source FROM examples WHERE word_id = ?",
            (w["id"],),
        ).fetchall():
            examples.append({
                "kilor": row["kilor_text"],
                "english": row["english_text"],
                "source": row["source"],
            })

        # Compute case forms (ACC/GEN) on the fly
        case_forms = {}
        acc, gen = get_case_forms(
            w["form"],
            derivation_mask=w["derivation_mask"] or None,
            is_function_word=bool(w["is_function_word"]),
            compound_type=w["compound_type"],
        )
        if acc is not None:
            case_forms["acc"] = acc
        if gen is not None:
            case_forms["gen"] = gen

        entry = {
            "id": w["id"],
            "form": w["form"],
            "syl_count": w["syl_count"],
            "meanings": meanings,
            "derivation_mask": w["derivation_mask"],
            "section": w["section"],
            "section_label": SECTION_LABELS.get(w["section"], "Other"),
            "is_root": bool(w["is_root"]),
            "is_compound": bool(w["is_compound"]),
            "compound_type": w["compound_type"],
            "is_function_word": bool(w["is_function_word"]),
            "consensus_prefix": w["consensus_prefix"] or "o-",
            "inflections": inflections,
            "components": components,
            "pattern": meta["pattern"] if meta else None,
            "rule_ref": meta["rule_ref"] if meta else None,
            "case_forms": case_forms,
            "examples": examples,
            "notes": w["notes"] or "",
        }
        entries.append(entry)

    output = {
        "meta": {
            "exported_at": datetime.now().strftime("%Y-%m-%d"),
            "version": "2.0.0",
            "total_words": len(entries),
        },
        "entries": entries,
    }

    output_path = os.path.join(SCRIPT_DIR, "data", "dictionary-data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(entries)} entries to {output_path}")


def cmd_export(fmt="json"):
    """Export the lexicon to the specified format."""
    conn = get_db()
    rebuild_fts(conn)

    if fmt == "csv":
        _export_csv(conn)
    elif fmt == "json":
        _export_json(conn)
    elif fmt == "html":
        _export_html(conn)
    elif fmt == "dictionary":
        _export_dictionary_data(conn)
    else:
        print(f"Unknown format: {fmt}. Use csv, json, html, or dictionary.")

    conn.close()