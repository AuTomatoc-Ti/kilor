"""Edit existing words in the database."""

import os
import sys

from ..db import get_db, rebuild_fts, populate_search_text
from ..phonology import validate_content_root, count_syllables
from ..schema import VALID_POS, POS_TO_INFLECTION, compute_pos_mask

_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "dictionary", "public", "audio")


def _regenerate_audio_after_rename(word_id, new_form):
    """Attempt to regenerate audio after a --fix-typo rename.

    The old audio file ({word_id}.ogg) still contains the old pronunciation.
    Try to regenerate it; warn if the toolchain is unavailable.
    """
    old_path = os.path.join(_AUDIO_DIR, f"{word_id}.ogg")
    if not os.path.isfile(old_path):
        # No existing audio — nothing to regenerate
        return
    try:
        from .audio import _generate_one
    except ImportError:
        print(f"\n  ⚠️  Audio for ID {word_id} still contains the old pronunciation.\n"
              f"     Regenerate manually:  python kilor.py audio --generate --id {word_id}")
        return
    print(f"\n  🔊 Regenerating audio for the new form '{new_form}'…")
    ok = _generate_one(word_id, new_form, old_path)
    if ok:
        print(f"  ✅ Audio regenerated for ID {word_id}")
    else:
        print(f"  ⚠️  Audio regeneration failed. Run manually:\n"
              f"     python kilor.py audio --generate --id {word_id}")


def cmd_edit(form, **kwargs):
    """Edit an existing word.
    
    Usage:
        python kilor.py edit <form> --add-meaning "new gloss" [--pos N|V|A|D|...]
        python kilor.py edit <form> --set-prefix "a-"
        python kilor.py edit <form> --set-mask "nv"
        python kilor.py edit <form> --add-example "kilor text" "english text"
        python kilor.py edit <form> --remove-example <example_id>
        python kilor.py edit <form> --fix-typo "newform"
    """
    conn = get_db()
    
    # Find the word
    word = conn.execute("SELECT * FROM words WHERE form = ?", (form,)).fetchone()
    if not word:
        print(f"Error: word '{form}' not found in database.")
        conn.close()
        return False
    
    word_id = word["id"]
    changes = []
    
    # Add meaning
    if "add_meaning" in kwargs:
        gloss = kwargs["add_meaning"]
        pos = kwargs.get("add_meaning_pos", "")
        if pos and pos not in VALID_POS:
            print(f"Warning: POS '{pos}' not in VALID_POS — storing as-is.")
        # sort_order scoped within the same pos
        if pos:
            sort_order = conn.execute(
                "SELECT MAX(sort_order) FROM meanings WHERE word_id = ? AND pos = ?",
                (word_id, pos),
            ).fetchone()[0] or 0
        else:
            sort_order = conn.execute(
                "SELECT MAX(sort_order) FROM meanings WHERE word_id = ?", (word_id,),
            ).fetchone()[0] or 0
        conn.execute(
            "INSERT INTO meanings (word_id, gloss, language, sort_order, pos) VALUES (?, ?, ?, ?, ?)",
            (word_id, gloss, "en", sort_order + 1, pos),
        )
        conn.execute(
            "UPDATE words SET updated_at = datetime('now') WHERE id = ?",
            (word_id,),
        )
        label = f"'{gloss}'"
        if pos:
            label += f" (pos={pos})"
        changes.append(f"Added meaning: {label}")
    
    # Set prefix
    if "set_prefix" in kwargs:
        new_prefix = kwargs["set_prefix"]
        conn.execute(
            "UPDATE words SET consensus_prefix = ?, updated_at = datetime('now') WHERE id = ?",
            (new_prefix, word_id),
        )
        changes.append(f"Set prefix to '{new_prefix}'")
    
    # Set derivation mask
    if "set_mask" in kwargs:
        new_mask = kwargs["set_mask"].upper()
        # Validate mask
        valid_chars = set("NVAD")
        if not all(c in valid_chars for c in new_mask):
            print(f"Error: invalid mask '{new_mask}'. Must contain only N, V, A, D.")
            conn.close()
            return False
        
        # ── Prefix-mask consistency check ──
        old_mask = (word["pos_mask"] or word["derivation_mask"] or "").upper()
        old_has_n = "N" in old_mask
        new_has_n = "N" in new_mask
        current_prefix = word["consensus_prefix"] or ""
        
        if new_has_n and not old_has_n and not current_prefix:
            print(
                f"Error: mask '{new_mask}' includes N but no consensus_prefix is set. "
                "Set it first with --set-prefix."
            )
            conn.close()
            return False
        
        if not new_has_n and old_has_n and current_prefix:
            print(
                f"Warning: N removed from mask (was '{old_mask}', now '{new_mask}'), "
                f"but consensus_prefix '{current_prefix}' is still set. "
                "The prefix will be ignored in display. "
                f"Clear it with --set-prefix '' if unintended."
            )
        
        conn.execute(
            "UPDATE words SET derivation_mask = ?, pos_mask = ?, updated_at = datetime('now') WHERE id = ?",
            (new_mask, new_mask, word_id),
        )
        changes.append(f"Set derivation mask to '{new_mask}'")
        
        _regenerate_inflections(conn, word_id, word["form"], word["syl_count"], new_mask)
        changes.append(f"Regenerated inflections for mask '{new_mask}'")
    
    # Add example
    if "add_example" in kwargs:
        kilor_text, english_text = kwargs["add_example"]
        conn.execute(
            "INSERT INTO examples (word_id, kilor_text, english_text, source) VALUES (?, ?, ?, ?)",
            (word_id, kilor_text, english_text, "canonical"),
        )
        conn.execute(
            "UPDATE words SET updated_at = datetime('now') WHERE id = ?",
            (word_id,),
        )
        changes.append(f"Added example: '{kilor_text}' = '{english_text}'")
    
    # Remove example
    if "remove_example" in kwargs:
        example_id = int(kwargs["remove_example"])
        conn.execute("DELETE FROM examples WHERE id = ? AND word_id = ?", (example_id, word_id))
        if conn.rowcount > 0:
            conn.execute(
                "UPDATE words SET updated_at = datetime('now') WHERE id = ?",
                (word_id,),
            )
            changes.append(f"Removed example ID {example_id}")
        else:
            print(f"Warning: example ID {example_id} not found for this word.")
    
    # Fix typo (change form)
    if "fix_typo" in kwargs:
        new_form = kwargs["fix_typo"]
        is_func = bool(word["is_function_word"])
        is_compound = bool(word["is_compound"])
        valid, err = validate_content_root(new_form, is_func=is_func, is_compound=is_compound)
        if not valid:
            print(f"Error: new form '{new_form}' is invalid: {err}")
            conn.close()
            return False
        
        existing = conn.execute("SELECT id FROM words WHERE form = ? AND id != ?", (new_form, word_id)).fetchone()
        if existing:
            print(f"Error: '{new_form}' already exists in database.")
            conn.close()
            return False
        
        new_syl = count_syllables(new_form)
        conn.execute(
            "UPDATE words SET form = ?, syl_count = ?, updated_at = datetime('now') WHERE id = ?",
            (new_form, new_syl, word_id),
        )
        changes.append(f"Changed form from '{form}' to '{new_form}'")
        
        _regenerate_audio_after_rename(word_id, new_form)
    
    if not changes:
        print(f"No changes specified for '{form}'.")
        conn.close()
        return False
    
    # ── Recompute pos_mask after meaning changes ──
    if "add_meaning" in kwargs or "remove_meaning" in kwargs:
        meanings_after = conn.execute(
            "SELECT pos FROM meanings WHERE word_id = ? AND pos != ''", (word_id,)
        ).fetchall()
        computed_mask = compute_pos_mask([{'pos': m['pos']} for m in meanings_after])
        
        has_explicit_mask = "set_mask" in kwargs
        if not has_explicit_mask:
            conn.execute(
                "UPDATE words SET pos_mask = ?, updated_at = datetime('now') WHERE id = ?",
                (computed_mask, word_id),
            )
            changes.append(f"Recomputed pos_mask = '{computed_mask}'")
            
            _regenerate_inflections(conn, word_id, word["form"], word["syl_count"], computed_mask)
            changes.append("Regenerated inflections")
        
        if computed_mask == '':
            conn.execute("UPDATE words SET is_function_word = 1 WHERE id = ?", (word_id,))
        else:
            conn.execute("UPDATE words SET is_function_word = 0 WHERE id = ?", (word_id,))
    
    # Commit changes
    conn.commit()
    populate_search_text(conn)
    rebuild_fts(conn)
    conn.close()
    
    print(f"✅ Updated '{form}':")
    for change in changes:
        print(f"  • {change}")
    
    return True


def _regenerate_inflections(conn, word_id, root, syl_count, pos_mask):
    """Delete existing and insert new inflections based on pos_mask."""
    conn.execute("DELETE FROM inflections WHERE word_id = ?", (word_id,))
    
    if not pos_mask:
        return
    
    form_types_list = []
    for letter in pos_mask:
        ft = POS_TO_INFLECTION.get(letter)
        if ft and ft not in form_types_list:
            form_types_list.append(ft)
    
    is_toneless = syl_count <= 2
    for ft in sorted(form_types_list):
        if is_toneless:
            sform = root if ft in ("noun", "verb") else f"{root}s"
        else:
            sform = root if ft in ("noun", "verb") else f"{root}s"
        conn.execute(
            "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
            (word_id, ft, sform),
        )