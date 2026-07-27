"""One-shot backfill: populate ipa and syllables columns for all existing words.

Handles multi-word compounds by processing each word separately.
Safe to re-run — overwrites existing values with recomputed output.
"""
import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "kilor.db")

sys.path.insert(0, SCRIPT_DIR)
from kilor.phonology import to_ipa, split_syllables


def backfill():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    words = cur.execute("SELECT id, form FROM words ORDER BY id").fetchall()

    updated = 0
    errors = 0

    for w in words:
        form = w["form"]
        try:
            if " " in form:
                # Multi-word compound: process each word, join with space
                subwords = form.split()
                ipa_parts = [to_ipa(sw) for sw in subwords]
                syl_parts = [".".join(split_syllables(sw)) for sw in subwords]
                ipa_val = " ".join(ipa_parts)
                syl_val = " ".join(syl_parts)
            else:
                ipa_val = to_ipa(form)
                syl_val = ".".join(split_syllables(form))
            cur.execute(
                "UPDATE words SET ipa = ?, syllables = ? WHERE id = ?",
                (ipa_val, syl_val, w["id"]),
            )
            updated += 1
        except Exception as e:
            print(f"  ERROR on '{form}' (id={w['id']}): {e}")
            errors += 1

    conn.commit()
    conn.close()

    print(f"Backfill complete: {updated} words updated, {errors} errors")

    # Show a few samples
    conn2 = sqlite3.connect(DB_PATH)
    conn2.row_factory = sqlite3.Row
    samples = conn2.execute(
        "SELECT form, ipa, syllables FROM words WHERE ipa != '' LIMIT 10"
    ).fetchall()
    print("\nSample output:")
    for s in samples:
        print(f"  {s['form']:20s} → {s['ipa']:35s} | {s['syllables']}")

    # Show multi-word samples
    multi = conn2.execute(
        "SELECT form, ipa, syllables FROM words WHERE form LIKE '% %' AND ipa != '' LIMIT 5"
    ).fetchall()
    if multi:
        print("\nMulti-word samples:")
        for s in multi:
            print(f"  {s['form']:20s} → {s['ipa']}")
            print(f"  {'':20s}   {s['syllables']}")
    conn2.close()


if __name__ == "__main__":
    backfill()