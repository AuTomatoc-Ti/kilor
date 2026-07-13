"""Validate all entries in the database."""

from ..db import get_db
from ..phonology import validate_content_root


def cmd_check():
    """Validate all entries in the database."""
    conn = get_db()
    errors = []

    words = conn.execute("SELECT * FROM words ORDER BY id").fetchall()

    for w in words:
        form = w["form"]
        is_func = bool(w["is_function_word"])
        is_compound = bool(w["is_compound"])

        valid, err = validate_content_root(form, is_func=is_func, is_compound=is_compound)
        if not valid:
            errors.append(f"  {form}: {err}")

        meaning_count = conn.execute(
            "SELECT COUNT(*) FROM meanings WHERE word_id = ?", (w["id"],)
        ).fetchone()[0]
        if meaning_count == 0 and not is_func:
            errors.append(f"  {form}: missing meaning")

        if not is_func and not is_compound:
            infl_count = conn.execute(
                "SELECT COUNT(*) FROM inflections WHERE word_id = ?", (w["id"],)
            ).fetchone()[0]
            if infl_count < 2:
                errors.append(f"  {form}: has only {infl_count} inflected form(s)")

        if is_compound:
            has_meta = conn.execute(
                "SELECT 1 FROM compound_meta WHERE compound_id = ?", (w["id"],)
            ).fetchone() is not None
            comps = conn.execute(
                """SELECT cc.position, cc.component_id, w2.form as component_form
                   FROM compound_components cc
                   JOIN words w2 ON cc.component_id = w2.id
                   WHERE cc.compound_id = ? ORDER BY cc.position""",
                (w["id"],),
            ).fetchall()
            if not comps and not has_meta:
                errors.append(f"  {form}: compound has no components listed")
            for c in comps:
                if not c["component_id"]:
                    errors.append(f"  {form}: component at position {c['position']} not found")

    dupes = conn.execute(
        "SELECT form, COUNT(*) as cnt FROM words GROUP BY form HAVING cnt > 1"
    ).fetchall()
    for d in dupes:
        errors.append(f"  DUPLICATE form: '{d['form']}' appears {d['cnt']} times")

    if errors:
        print(f"{len(errors)} validation error(s):")
        for e in errors:
            print(e)
    else:
        total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        roots = conn.execute("SELECT COUNT(*) FROM words WHERE is_root = 1").fetchone()[0]
        func = conn.execute("SELECT COUNT(*) FROM words WHERE is_function_word = 1").fetchone()[0]
        compounds = conn.execute("SELECT COUNT(*) FROM words WHERE is_compound = 1").fetchone()[0]
        print(f"✅ All {total} entries pass validation.")
        print(f"  Roots: {roots}")
        print(f"  Function words: {func}")
        print(f"  Compounds: {compounds}")

    conn.close()