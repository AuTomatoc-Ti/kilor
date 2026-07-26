"""Validate all entries in the database."""

from ..db import get_db
from ..phonology import validate_content_root, count_syllables, split_syllables


def cmd_check():
    """Validate all entries in the database."""
    conn = get_db()
    errors = []
    warnings = []

    words = conn.execute("SELECT * FROM words ORDER BY id").fetchall()

    for w in words:
        form = w["form"]
        is_func = bool(w["is_function_word"])
        is_compound = bool(w["is_compound"])
        syl_count = w["syl_count"]

        # Phonotactic validation
        valid, err = validate_content_root(form, is_func=is_func, is_compound=is_compound)
        if not valid:
            errors.append(f"  {form}: {err}")

        # Meaning check
        meaning_count = conn.execute(
            "SELECT COUNT(*) FROM meanings WHERE word_id = ?", (w["id"],)
        ).fetchone()[0]
        if meaning_count == 0 and not is_func:
            errors.append(f"  {form}: missing meaning")

        # Inflection check
        if not is_func and not is_compound:
            infl_count = conn.execute(
                "SELECT COUNT(*) FROM inflections WHERE word_id = ?", (w["id"],)
            ).fetchone()[0]
            if infl_count < 2:
                errors.append(f"  {form}: has only {infl_count} inflected form(s)")
            
            # Check that inflections match derivation mask
            mask = (w["derivation_mask"] or "").upper()
            expected_types = set()
            if 'N' in mask:
                expected_types.add('noun')
            if 'V' in mask:
                expected_types.add('verb')
            if 'A' in mask:
                expected_types.add('adjective')
            if 'D' in mask:
                expected_types.add('adverb')
            
            actual_types = set(
                row["form_type"] for row in conn.execute(
                    "SELECT form_type FROM inflections WHERE word_id = ?", (w["id"],)
                ).fetchall()
            )
            
            if expected_types and not expected_types.issubset(actual_types):
                missing = expected_types - actual_types
                errors.append(f"  {form}: missing inflections for {', '.join(missing)} (mask: {mask})")

        # Compound validation
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
            
            # Verify components are roots (not compounds)
            for c in comps:
                comp_row = conn.execute(
                    "SELECT is_compound FROM words WHERE id = ?", (c["component_id"],)
                ).fetchone()
                if comp_row and comp_row["is_compound"]:
                    errors.append(f"  {form}: component '{c['component_form']}' is a compound, not a root")

        # Tone markers on 3+ syllable inflected forms
        if syl_count >= 3 and not is_func:
            for infl in conn.execute(
                "SELECT form_type, form FROM inflections WHERE word_id = ?", (w["id"],)
            ).fetchall():
                # Check if form should have tone markers but doesn't
                # (skip this check for now as it requires complex tone placement logic)
                pass

        # Syllable count verification
        computed = count_syllables(form)
        if computed != syl_count:
            errors.append(
                f"  {form}: syl_count mismatch — stored {syl_count}, computed {computed}"
            )

    # Duplicate forms
    dupes = conn.execute(
        "SELECT form, COUNT(*) as cnt FROM words GROUP BY form HAVING cnt > 1"
    ).fetchall()
    for d in dupes:
        errors.append(f"  DUPLICATE form: '{d['form']}' appears {d['cnt']} times")


    roots = [w for w in words if w["is_root"] and not w["is_function_word"]]

    # Near-collision detection (warning, not error)
    # comment it out for now, as it can be too sensitive
    collision_checking = False
    if collision_checking:
        for i, w1 in enumerate(roots):
            for w2 in roots[i+1:]:
                # Simple Levenshtein distance check (only for short words)
                if len(w1["form"]) <= 6 and len(w2["form"]) <= 6:
                    dist = _levenshtein(w1["form"], w2["form"])
                    if 1 <= dist <= 2:
                        warnings.append(f"  ⚠️  Near-collision: '{w1['form']}' vs '{w2['form']}' (distance {dist})")

    # Print results
    if errors:
        print(f"{len(errors)} validation error(s):")
        for e in errors:
            print(e)
    
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(w)
    
    if not errors and not warnings:
        total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        roots = conn.execute("SELECT COUNT(*) FROM words WHERE is_root = 1").fetchone()[0]
        func = conn.execute("SELECT COUNT(*) FROM words WHERE is_function_word = 1").fetchone()[0]
        compounds = conn.execute("SELECT COUNT(*) FROM words WHERE is_compound = 1").fetchone()[0]
        print(f"✅ All {total} entries pass validation.")
        print(f"  Roots: {roots}")
        print(f"  Function words: {func}")
        print(f"  Compounds: {compounds}")

    conn.close()


def _levenshtein(s1, s2):
    """Compute Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
