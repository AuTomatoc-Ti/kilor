"""Edit existing words in the database."""

import os
import sys

from ..db import get_db, rebuild_fts, populate_search_text
from ..phonology import validate_content_root, count_syllables
from ..schema import VALID_POS

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
        label = f"'{gloss}'"
        if pos:
            label += f" (pos={pos})"
        changes.append(f"Added meaning: {label}")
    
    # Set prefix
    if "set_prefix" in kwargs:
        new_prefix = kwargs["set_prefix"]
        conn.execute(
            "UPDATE words SET consensus_prefix = ? WHERE id = ?",
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
        if 'D' in new_mask and 'A' not in new_mask:
            print(f"Error: mask '{new_mask}' invalid — D (adverb) requires A (adjective).")
            conn.close()
            return False
        
        conn.execute(
            "UPDATE words SET derivation_mask = ? WHERE id = ?",
            (new_mask, word_id),
        )
        changes.append(f"Set derivation mask to '{new_mask}'")
        
        # Regenerate inflections based on new mask
        conn.execute("DELETE FROM inflections WHERE word_id = ?", (word_id,))
        root = word["form"]
        mask_to_forms = {
            'N': ['noun'], 'V': ['verb'], 'A': ['adjective'], 'D': ['adverb'],
            'NV': ['noun', 'verb'], 'NA': ['noun', 'adjective'],
            'AV': ['adjective', 'verb'], 'AD': ['adjective', 'adverb'],
            'NVAD': ['noun', 'verb', 'adjective', 'adverb'],
            'NVA': ['noun', 'verb', 'adjective'],
            'NAD': ['noun', 'adjective', 'adverb'],
            'VAD': ['verb', 'adjective', 'adverb'],
        }
        form_types = mask_to_forms.get(new_mask, ['noun', 'verb', 'adjective', 'adverb'])
        for ft in form_types:
            form = f"{root}s" if ft in ("adjective", "adverb") else root
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, ft, form),
            )
        changes.append(f"Regenerated inflections for mask '{new_mask}'")
    
    # Add example
    if "add_example" in kwargs:
        kilor_text, english_text = kwargs["add_example"]
        conn.execute(
            "INSERT INTO examples (word_id, kilor_text, english_text, source) VALUES (?, ?, ?, ?)",
            (word_id, kilor_text, english_text, "canonical"),
        )
        changes.append(f"Added example: '{kilor_text}' = '{english_text}'")
    
    # Remove example
    if "remove_example" in kwargs:
        example_id = int(kwargs["remove_example"])
        conn.execute("DELETE FROM examples WHERE id = ? AND word_id = ?", (example_id, word_id))
        if conn.rowcount > 0:
            changes.append(f"Removed example ID {example_id}")
        else:
            print(f"Warning: example ID {example_id} not found for this word.")
    
    # Fix typo (change form)
    if "fix_typo" in kwargs:
        new_form = kwargs["fix_typo"]
        # Validate new form
        is_func = bool(word["is_function_word"])
        is_compound = bool(word["is_compound"])
        valid, err = validate_content_root(new_form, is_func=is_func, is_compound=is_compound)
        if not valid:
            print(f"Error: new form '{new_form}' is invalid: {err}")
            conn.close()
            return False
        
        # Check for duplicates
        existing = conn.execute("SELECT id FROM words WHERE form = ? AND id != ?", (new_form, word_id)).fetchone()
        if existing:
            print(f"Error: '{new_form}' already exists in database.")
            conn.close()
            return False
        
        # Update form and syllable count
        new_syl = count_syllables(new_form)
        conn.execute(
            "UPDATE words SET form = ?, syl_count = ? WHERE id = ?",
            (new_form, new_syl, word_id),
        )
        changes.append(f"Changed form from '{form}' to '{new_form}'")
        
        # Regenerate audio for the renamed word
        _regenerate_audio_after_rename(word_id, new_form)
    
    if not changes:
        print(f"No changes specified for '{form}'.")
        conn.close()
        return False
    
    # Commit changes
    conn.commit()
    populate_search_text(conn)
    rebuild_fts(conn)
    conn.close()
    
    print(f"✅ Updated '{form}':")
    for change in changes:
        print(f"  • {change}")
    
    return True
