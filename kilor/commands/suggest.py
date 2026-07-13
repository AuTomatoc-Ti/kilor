"""Suggest how a concept should be handled (root/compound/derivation)."""

from ..db import get_db


def cmd_suggest(word):
    """Suggest how a concept should be handled."""
    conn = get_db()

    existing = conn.execute(
        """SELECT w.form, m.gloss FROM words w
           JOIN meanings m ON w.id = m.word_id
           WHERE LOWER(m.gloss) LIKE ? LIMIT 1""",
        (f"%{word.lower()}%",),
    ).fetchone()
    if existing:
        print(f"\n⚠️  Already exists: {existing['form']} = {existing['gloss']}")
        conn.close()
        return

    print(f"\nSuggestions for '{word}':\n")

    word_parts = set(word.lower().split())
    related = conn.execute(
        """SELECT w.form, m.gloss, w.derivation_mask FROM words w
            JOIN meanings m ON w.id = m.word_id WHERE w.is_function_word = 0"""
    ).fetchall()

    for r in related:
        meaning_parts = set(r["gloss"].lower().replace("/", " ").split())
        if word_parts & meaning_parts:
            mask = r['derivation_mask'] or ''
            print(f"  {r['form']} = {r['gloss']} ({mask})")

            if mask and 'N' in mask:
                print(f"    → Adverb form: {r['form']}s")
            if mask and 'V' in mask:
                print(f"    → Adjective form: {r['form']}s")
            if mask and 'A' in mask:
                print(f"    → Adjective form: {r['form']}s")
            if mask and 'D' in mask:
                print(f"    → Adverb form: {r['form']}s")

    print(f"\n  → If none fit, coin a new root.")
    print(f"  → Or define as compound of: [root1] [root2] = '{word}'")

    conn.close()