"""REST API server for the Kilor dictionary.

Provides read-only HTTP access to the lexicon database for AI agents,
the dictionary frontend, and external tools.

Run: python -m uvicorn kilor.api:app --port 8765
Or:  python kilor.py serve
"""

import random
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .db import get_db, fts_search
from .schema import SECTION_LABELS, DERIVATION_MASK_LABELS

# ── FastAPI app ──────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: verify database is accessible."""
    conn = get_db()
    conn.close()
    yield

app = FastAPI(
    title="Kilor Dictionary API",
    description="Read-only REST API for the Kilor constructed language lexicon.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Prefix info (SSOT: rules/0-foundation/philosophy.md) ─────────────────────

PREFIX_INFO = {
    "a-":  {"class": "Alive / Energy",     "emotion": "Anger",   "color": "#ef4444"},
    "e-":  {"class": "Crafted / Tool",     "emotion": "Joy",     "color": "#f59e0b"},
    "i-":  {"class": "Fluid / Vast",       "emotion": "Sadness", "color": "#3b82f6"},
    "o-":  {"class": "Abstract / Void",    "emotion": "Surprise","color": "#f5f5f5"},
    "u-":  {"class": "Organic / Growth",   "emotion": "Calm",    "color": "#22c55e"},
    "y-":  {"class": "Dense / Mass",       "emotion": "Fear",    "color": "#6b7280"},
    "ae-": {"class": "Earth / Boundary",   "emotion": "Disgust", "color": "#a16207"},
}

# ── Data helpers ─────────────────────────────────────────────────────────────

def _get_conn():
    """Get a fresh DB connection per request (read-only)."""
    from .db import get_db_path
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def _word_to_dict(conn, row) -> dict:
    """Convert a words row to the full dictionary entry dict."""
    wid = row["id"]

    # Meanings
    meanings = [
        m["gloss"]
        for m in conn.execute(
            "SELECT gloss FROM meanings WHERE word_id = ? ORDER BY sort_order",
            (wid,),
        ).fetchall()
    ]

    # Inflections
    inflections = {}
    for ir in conn.execute(
        "SELECT form_type, form FROM inflections WHERE word_id = ?", (wid,),
    ).fetchall():
        inflections[ir["form_type"]] = ir["form"]

    # Compound components
    components = []
    if row["is_compound"]:
        comps = conn.execute(
            """SELECT w2.form, w2.id, cc.position
               FROM compound_components cc
               JOIN words w2 ON cc.component_id = w2.id
               WHERE cc.compound_id = ? ORDER BY cc.position""",
            (wid,),
        ).fetchall()
        components = [{"form": c["form"], "id": c["id"]} for c in comps]

    # Compound meta
    meta = conn.execute(
        "SELECT pattern, rule_ref FROM compound_meta WHERE compound_id = ?",
        (wid,),
    ).fetchone()

    # Examples
    examples = []
    for ex in conn.execute(
        "SELECT kilor_text, english_text, source FROM examples WHERE word_id = ?",
        (wid,),
    ).fetchall():
        examples.append({
            "kilor": ex["kilor_text"],
            "english": ex["english_text"],
            "source": ex["source"],
        })

    # Grammar ref
    grammar_ref = row["grammar_ref"] if "grammar_ref" in row.keys() else None
    if grammar_ref is None and row["is_function_word"]:
        # Try to derive from compound_meta for function words
        m = conn.execute(
            "SELECT rule_ref FROM compound_meta WHERE compound_id = ?",
            (wid,),
        ).fetchone()
        grammar_ref = m["rule_ref"] if m else None
    elif grammar_ref is None and meta and meta["rule_ref"]:
        grammar_ref = meta["rule_ref"]

    prefix = row["consensus_prefix"] or "o-"
    prefix_info = PREFIX_INFO.get(prefix, None)

    return {
        "id": wid,
        "form": row["form"],
        "syl_count": row["syl_count"],
        "meanings": meanings,
        "derivation_mask": row["derivation_mask"],
        "section": row["section"],
        "section_label": SECTION_LABELS.get(row["section"], "Other"),
        "is_root": bool(row["is_root"]),
        "is_compound": bool(row["is_compound"]),
        "compound_type": row["compound_type"],
        "is_function_word": bool(row["is_function_word"]),
        "consensus_prefix": prefix,
        "prefix_info": prefix_info,
        "inflections": inflections,
        "components": components,
        "pattern": meta["pattern"] if meta else None,
        "rule_ref": meta["rule_ref"] if meta else None,
        "grammar_ref": grammar_ref,
        "examples": examples,
        "notes": row["notes"] or "",
        "phase": row["phase"] if "phase" in row.keys() else None,
        "tags": row["tags"] if "tags" in row.keys() else None,
    }


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/api/words")
def get_words(
    q: Optional[str] = Query(None, description="Search query (substring match across form, meanings, examples)"),
    section: Optional[str] = Query(None, description="Filter by section (A-J)"),
    derivation_mask: Optional[str] = Query(None, description="Filter by derivation mask (N, V, A, D, NV, NA, NVAD, ...)"),
    phase: Optional[int] = Query(None, description="Filter by learning phase (1-6)"),
    tags: Optional[str] = Query(None, description="Filter by semantic tag (comma-separated)"),
    limit: int = Query(200, ge=1, le=5000, description="Max entries to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """List words with optional filters."""
    conn = _get_conn()
    try:
        query = "SELECT * FROM words WHERE 1=1"
        params = []

        if section:
            query += " AND section = ?"
            params.append(section)
        if derivation_mask:
            query += " AND derivation_mask = ?"
            params.append(derivation_mask)
        if phase and "phase" in _get_columns(conn, "words"):
            query += " AND phase = ?"
            params.append(phase)
        if tags and "tags" in _get_columns(conn, "words"):
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            for tag in tag_list:
                query += " AND tags LIKE ?"
                params.append(f"%{tag}%")

        query += " ORDER BY form LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = conn.execute(query, params).fetchall()

        entries = []
        for row in rows:
            entry = _word_to_dict(conn, row)
            # Apply text search filter if q provided (client-side for simplicity)
            if q:
                searchable = " ".join([
                    entry["form"],
                    *entry["meanings"],
                    *[c["form"] for c in entry["components"]],
                    *[ex["kilor"] + " " + ex["english"] for ex in entry["examples"]],
                    entry.get("pattern") or "",
                    entry.get("notes") or "",
                ]).lower()
                if q.lower() not in searchable:
                    continue
            entries.append(entry)

        return {
            "total": len(entries),
            "limit": limit,
            "offset": offset,
            "entries": entries,
        }
    finally:
        conn.close()


@app.get("/api/words/{word_id}")
def get_word(word_id: int):
    """Get a single word by ID with full detail."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
        if not row:
            from fastapi.responses import JSONResponse
            return JSONResponse({"error": f"Word {word_id} not found"}, status_code=404)

        return _word_to_dict(conn, row)
    finally:
        conn.close()


@app.get("/api/search")
def search_words(
    q: str = Query(..., description="Search query (FTS5 full-text search)"),
    limit: int = Query(50, ge=1, le=500, description="Max results"),
):
    """Full-text search via FTS5 index with relevance ranking."""
    conn = _get_conn()
    try:
        word_ids = fts_search(q, limit=limit)
        entries = []
        for wid in word_ids:
            row = conn.execute("SELECT * FROM words WHERE id = ?", (wid,)).fetchone()
            if row:
                entries.append(_word_to_dict(conn, row))

        return {
            "query": q,
            "total": len(entries),
            "entries": entries,
        }
    finally:
        conn.close()


@app.get("/api/status")
def get_status():
    """Lexicon statistics and roadmap progress."""
    conn = _get_conn()
    try:
        total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        roots = conn.execute(
            "SELECT COUNT(*) FROM words WHERE is_root = 1 AND is_function_word = 0"
        ).fetchone()[0]
        func = conn.execute(
            "SELECT COUNT(*) FROM words WHERE is_function_word = 1"
        ).fetchone()[0]
        compounds = conn.execute(
            "SELECT COUNT(*) FROM words WHERE is_compound = 1"
        ).fetchone()[0]
        mono = conn.execute(
            "SELECT COUNT(*) FROM words WHERE compound_type = 'mono'"
        ).fetchone()[0]
        multi = conn.execute(
            "SELECT COUNT(*) FROM words WHERE compound_type = 'multi'"
        ).fetchone()[0]

        # Derived forms (inflections beyond the root)
        # Derived words: each inflection row for a content root counts as a distinct surface word
        # (e.g. maeha-noun + maeha-verb + maehas-adj + maehas-adv = 4 words from 1 root)
        derived = conn.execute(
            """SELECT COUNT(*) FROM inflections
               WHERE word_id IN (SELECT id FROM words
                                 WHERE is_root = 1 AND is_function_word = 0)"""
        ).fetchone()[0]

        # Category breakdown
        cats = [
            {"derivation_mask": r["derivation_mask"], "count": r["cnt"]}
            for r in conn.execute(
                "SELECT derivation_mask, COUNT(*) as cnt FROM words GROUP BY derivation_mask ORDER BY cnt DESC"
            ).fetchall()
        ]

        # Section breakdown
        secs = [
            {
                "section": r["section"],
                "label": SECTION_LABELS.get(r["section"], "Unknown"),
                "count": r["cnt"],
            }
            for r in conn.execute(
                "SELECT section, COUNT(*) as cnt FROM words WHERE section != '' GROUP BY section ORDER BY section"
            ).fetchall()
        ]

        # Syllable breakdown
        syls = [
            {"syl_count": r["syl_count"], "count": r["cnt"]}
            for r in conn.execute(
                "SELECT syl_count, COUNT(*) as cnt FROM words GROUP BY syl_count ORDER BY syl_count"
            ).fetchall()
        ]

        # Roadmap progress (tracking roots + total words)
        content_total = roots
        # Total surface words = derived + compounds + function words (root entries themselves are not surface words)
        total_words = derived + compounds + func

        roadmap_targets = [
            {"phase": 1, "label": "Phase 1 — Basic Daily",          "root_target": 500,  "word_target": 1750},
            {"phase": 2, "label": "Phase 2 — Elementary",           "root_target": 1000, "word_target": 3500},
            {"phase": 3, "label": "Phase 3 — Intermediate",         "root_target": 3000, "word_target": 10500},
            {"phase": 4, "label": "Phase 4 — Advanced",             "root_target": 4500, "word_target": 15750},
            {"phase": 5, "label": "Phase 5 — Proficient",           "root_target": 6000, "word_target": 21000},
            {"phase": 6, "label": "Phase 6 — Near-Native / Literary","root_target": 8600, "word_target": 30100},
        ]

        for t in roadmap_targets:
            t["roots_progress"] = round(content_total / t["root_target"] * 100, 1)
            t["words_progress"] = round(total_words / t["word_target"] * 100, 1)

        return {
            "exported_at": datetime.now().strftime("%Y-%m-%d"),
            "counts": {
                "content_roots": roots,
                "function_words": func,
                "compounds_mono": mono,
                "compounds_multi": multi,
                "compounds_total": compounds,
                "derived_forms": derived,
                "total_words": total_words,
            },
            "by_derivation_mask": cats,
            "by_section": secs,
            "by_syllable_count": syls,
            "roadmap": roadmap_targets,
            "prefix_info": PREFIX_INFO,
        }
    finally:
        conn.close()


@app.get("/api/word-of-day")
def word_of_day():
    """Return a random word entry."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM words WHERE is_root = 1 AND is_function_word = 0 ORDER BY RANDOM() LIMIT 1"
        ).fetchone()
        if not row:
            row = conn.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1").fetchone()
        if not row:
            from fastapi.responses import JSONResponse
            return JSONResponse({"error": "No words in database"}, status_code=404)

        return _word_to_dict(conn, row)
    finally:
        conn.close()


@app.get("/api/prefix-info")
def get_prefix_info():
    """Return the colour prefix ontology lookup table."""
    return {"prefix_info": PREFIX_INFO}


# ── Utility ──────────────────────────────────────────────────────────────────

def _get_columns(conn, table: str) -> list:
    """Get column names for a table."""
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [r["name"] for r in rows]