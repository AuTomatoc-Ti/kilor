"""Database connection, schema, and FTS5 search setup."""

import os
import sqlite3
from . import schema as s

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "kilor.db")


def get_db_path():
    return DB_PATH


def get_db():
    """Get a database connection, creating schema + FTS if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    conn.executescript(s.SCHEMA_SQL)
    conn.commit()
    _ensure_fts(conn)
    return conn


def _ensure_fts(conn):
    """Create FTS5 virtual table if it doesn't exist, seed it if empty."""
    # Create FTS5 table
    conn.executescript(s.FTS_SQL)
    conn.commit()

    # Seed FTS if empty
    count = conn.execute("SELECT COUNT(*) FROM words_fts").fetchone()[0]
    if count == 0:
        _rebuild_fts(conn)


def _rebuild_fts(conn):
    """Populate FTS from current words + meanings + examples.
    Drops and recreates the virtual table since contentless FTS doesn't support DELETE."""
    from . import schema as s

    conn.execute("DROP TABLE IF EXISTS words_fts")
    conn.execute("DROP TRIGGER IF EXISTS words_fts_insert")
    conn.execute("DROP TRIGGER IF EXISTS words_fts_delete")
    conn.execute("DROP TRIGGER IF EXISTS words_fts_update")
    conn.executescript(s.FTS_SQL)

    rows = conn.execute("""
        SELECT w.id, w.form, 
               GROUP_CONCAT(m.gloss, ' | ') as glosses,
               GROUP_CONCAT(e.kilor_text, ' | ') as kilor_examples,
               GROUP_CONCAT(e.english_text, ' | ') as english_examples
        FROM words w
        LEFT JOIN meanings m ON w.id = m.word_id
        LEFT JOIN examples e ON w.id = e.word_id
        GROUP BY w.id
    """).fetchall()
    for r in rows:
        conn.execute(
            "INSERT INTO words_fts(rowid, form, gloss, kilor_examples, english_examples) VALUES (?, ?, ?, ?, ?)",
            (r["id"], r["form"], r["glosses"] or "", r["kilor_examples"] or "", r["english_examples"] or ""),
        )
    conn.commit()


def rebuild_fts(conn=None):
    """Public: rebuild FTS index from scratch."""
    close_after = conn is None
    if conn is None:
        conn = get_db()
    _rebuild_fts(conn)
    if close_after:
        conn.close()


def fts_search(query, limit=50):
    """Search the FTS index. Returns list of word_ids ranked by relevance."""
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT rowid, rank FROM words_fts WHERE words_fts MATCH ? ORDER BY rank LIMIT ?",
            (query, limit),
        ).fetchall()
        return [r["rowid"] for r in rows]
    finally:
        conn.close()