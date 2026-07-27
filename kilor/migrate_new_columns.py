"""One-shot migration: add ipa, syllables, status, superseded_by, source_wordlist, source_line columns to words table.
Safe to re-run — uses IF NOT EXISTS-style checks.
"""
import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "kilor.db")


def migrate():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # Get existing columns
    existing = {r[1] for r in cur.execute("PRAGMA table_info(words)").fetchall()}

    new_columns = {
        "ipa": "TEXT DEFAULT ''",
        "syllables": "TEXT DEFAULT ''",
        "status": "TEXT DEFAULT 'active'",
        "superseded_by": "INTEGER REFERENCES words(id)",
        "source_wordlist": "TEXT DEFAULT ''",
        "source_line": "INTEGER DEFAULT 0",
    }

    added = []
    for col_name, col_def in new_columns.items():
        if col_name not in existing:
            try:
                cur.execute(f"ALTER TABLE words ADD COLUMN {col_name} {col_def}")
                added.append(col_name)
            except sqlite3.OperationalError as e:
                print(f"  WARNING: could not add column '{col_name}': {e}")
        else:
            print(f"  Column '{col_name}' already exists — skipping")

    # Set status = 'active' for all existing words where status is NULL or empty
    if "status" in existing or "status" in added:
        cur.execute("UPDATE words SET status = 'active' WHERE status IS NULL OR status = ''")

    conn.commit()
    conn.close()

    if added:
        print(f"Added columns: {', '.join(added)}")
    else:
        print("All columns already present. No changes made.")
    return added


if __name__ == "__main__":
    migrate()