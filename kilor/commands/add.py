"""Process a filled-in today.md and add entries to the database."""

import os
import re
import sqlite3

from ..db import get_db, rebuild_fts, populate_search_text
from ..phonology import validate_content_root, count_syllables, get_case_forms, split_syllables, to_ipa
from ..schema import VALID_POS

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Valid colour prefix values (SSOT: kilor/phonology.py:_COLOUR_PREFIXES)
_VALID_PREFIXES = {"a-", "e-", "i-", "o-", "u-", "y-", "ae-"}

# Derivation mask to form_type mapping
MASK_TO_FORMS = {
    'N': ['noun'],
    'V': ['verb'],
    'A': ['adjective'],
    'D': ['adverb'],
    'NV': ['noun', 'verb'],
    'NA': ['noun', 'adjective'],
    'AV': ['adjective', 'verb'],
    'AD': ['adjective', 'adverb'],
    'NVAD': ['noun', 'verb', 'adjective', 'adverb'],
    'NVA': ['noun', 'verb', 'adjective'],
    'NAD': ['noun', 'adjective', 'adverb'],
    'VAD': ['verb', 'adjective', 'adverb'],
}


def _parse_field(line, current):
    """Parse a single table row line into the current entry dict.

    Supports both legacy formats and the new 2.1.0 templates:
    - Content words: | Meaning (N) | ... |, | Meaning (V) | ...
    - Function words: | POS | ... |
    - Compound fields: | Components | ... |, | Pattern | ... |, | Rule Ref | ... |, | Type | ... |
    """
    parts = line.split("|")
    if len(parts) < 3:
        return

    key = parts[1].strip()
    val = parts[2].strip()
    if not val:
        return

    # --- Kilor Form (legacy: "Kilor Root") ---
    if key in ("Kilor Root", "Kilor Form"):
        current["root"] = val

    # --- Derivation Mask ---
    elif "Derivation Mask" in key:
        current["mask"] = val

    # --- POS (function word template) ---
    elif key == "POS":
        pos_val = val.strip().upper()
        if pos_val in VALID_POS:
            current["pos"] = pos_val
            current["mask"] = ""  # function words have empty mask
        else:
            current["_pos_warn"] = f"POS '{pos_val}' not in VALID_POS"

    # --- Per-PoS Meaning: | Meaning (N) | ... | ---
    elif m := re.match(r"^Meaning \((N|V|A|D)\)$", key):
        pos = m.group(1)
        if "meanings" not in current:
            current["meanings"] = {}
        # Comma-separated multiple senses
        glosses = [g.strip() for g in val.split(",") if g.strip()]
        current["meanings"][pos] = glosses

    # --- Legacy single Meaning field ---
    elif key == "Meaning" and "meanings" not in current:
        current["_legacy_meaning"] = val

    # --- Syllable Count (deprecated: auto-computed now) ---
    elif key == "Syllable Count":
        if val.isdigit():
            current["syl"] = val

    # --- Decision ---
    elif key == "Decision":
        current["decision"] = val

    # --- Notes ---
    elif key == "Notes":
        current["notes"] = val

    # --- Consensus Prefix ---
    elif key == "Consensus Prefix":
        current["consensus_prefix"] = val

    # --- Compound-specific fields ---
    elif key == "Components":
        # Parse "root1-form + root2-form" into list
        current["components"] = [c.strip() for c in val.split("+")]

    elif key == "Pattern":
        current["compound_pattern"] = val

    elif key == "Rule Ref":
        current["compound_rule_ref"] = val

    elif key == "Type":
        current["entry_type"] = val  # 'root', 'function', 'compound-mono', 'compound-multi'


def _validate_and_resolve_prefix(entry, root, english, errors):
    """Validate the consensus prefix field and resolve to a stored value.
    
    Returns (prefix_value, should_continue).
    prefix_value: the string to store (or None for NULL).
    should_continue: False if a blocking error occurred and this entry should be skipped.
    """
    prefix = entry.get("consensus_prefix", "").strip()
    
    if not prefix:
        errors.append(
            f"'{root}' ({english}): missing consensus prefix — "
            "please fill in the Consensus Prefix field "
            "(see rules/1-nominals/nouns-colour-prefix.md §V). "
            "Use '--' or 'none' for words that do not take a colour prefix."
        )
        return None, False
    
    if prefix in ("--", "none"):
        return None, True
    
    if prefix not in _VALID_PREFIXES:
        errors.append(
            f"'{root}' ({english}): invalid consensus prefix '{prefix}' — "
            f"must be one of {sorted(_VALID_PREFIXES)} or '--' / 'none'"
        )
        return None, False
    
    return prefix, True


def _resolve_compound_type(entry, root, english, errors):
    """Resolve entry type and compound flags from the template.
    
    Returns (is_root, is_compound, compound_type, is_function_word, is_func, should_continue).
    """
    entry_type = entry.get("entry_type", "").strip().lower()
    is_func = 1 if entry.get("pos") else 0
    
    if entry_type == "function":
        return 0, 0, None, 1, 1, True
    
    if entry_type in ("compound-mono", "compound-multi"):
        is_compound_val = 1
        compound_type_val = "mono" if entry_type == "compound-mono" else "multi"
        return 0, is_compound_val, compound_type_val, 0, is_func, True
    
    if entry_type in ("root", ""):
        return 1, 0, None, is_func, is_func, True
    
    # Unknown type
    errors.append(
        f"'{root}' ({english}): unknown Type '{entry.get('entry_type', '')}' — "
        "must be 'root', 'function', 'compound-mono', or 'compound-multi'"
    )
    return None, None, None, None, None, False


def _insert_compound_data(conn, word_id, entry, root, english, errors):
    """Insert compound_components and compound_meta rows. Returns True on success."""
    components = entry.get("components", [])
    if not components:
        errors.append(f"'{root}' ({english}): compound has no Components listed")
        return False
    
    # Look up each component by form
    component_ids = []
    for comp_form in components:
        comp_row = conn.execute(
            "SELECT id, is_compound FROM words WHERE form = ?", (comp_form,)
        ).fetchone()
        if not comp_row:
            errors.append(
                f"'{root}' ({english}): component '{comp_form}' not found in database"
            )
            return False
        if comp_row["is_compound"]:
            errors.append(
                f"'{root}' ({english}): component '{comp_form}' is itself "
                "a compound, not a root — compounds can only be built from roots"
            )
            return False
        component_ids.append(comp_row["id"])
    
    # Insert compound_components
    for pos, cid in enumerate(component_ids):
        conn.execute(
            "INSERT INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
            (word_id, cid, pos),
        )
    
    # Insert compound_meta if pattern is provided
    pattern = entry.get("compound_pattern", "")
    rule_ref = entry.get("compound_rule_ref", "")
    if pattern:
        conn.execute(
            "INSERT INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, ?)",
            (word_id, pattern, rule_ref),
        )
    
    return True


def cmd_add(filepath):
    """Process a filled-in today.md and add entries to the database."""
    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse entries
    entries = []
    current = None
    for line in content.split("\n"):
        line = line.strip()
        m_sec = re.match(r"^### (.+?) \((.+?)\)$", line)
        if m_sec:
            if current and current.get("root"):
                entries.append(current)
            current = {"english": m_sec.group(1).strip(), "domain": m_sec.group(2).strip()}
            continue

        if not current:
            continue

        _parse_field(line, current)

    # Don't lose the last entry
    if current and current.get("root"):
        entries.append(current)

    if not entries:
        print("No entries found in today.md. Make sure you've filled in the Kilor Form column.")
        return

    conn = get_db()
    added = 0
    errors = []

    for entry in entries:
        root = entry.get("root", "")
        english = entry.get("english", "")

        if not root:
            errors.append(f"'{english}': no Kilor form provided")
            continue

        # ── Phonotactic validation ──
        is_compound_check = " " in root
        valid, err = validate_content_root(root, is_compound=is_compound_check)
        if not valid:
            errors.append(f"'{root}' ({english}): {err}")
            continue

        # ── Duplicate check ──
        existing = conn.execute("SELECT id FROM words WHERE form = ?", (root,)).fetchone()
        if existing:
            errors.append(f"'{root}' ({english}): duplicate — already exists")
            continue

        # ── Consensus prefix (required, no default) ──
        prefix, prefix_ok = _validate_and_resolve_prefix(entry, root, english, errors)
        if not prefix_ok:
            continue

        # ── Entry type resolution ──
        is_root_val, is_compound_val, compound_type_val, is_func_val, is_func, type_ok = \
            _resolve_compound_type(entry, root, english, errors)
        if not type_ok:
            continue

        # ── Auto-compute phonology fields ──
        syl = str(count_syllables(root))
        ipa_val = to_ipa(root)
        syl_division = ".".join(split_syllables(root))

        mask = entry.get("mask", "")
        notes = entry.get("notes", entry.get("decision", "root"))

        # ── Insert into words ──
        try:
            conn.execute(
                """INSERT INTO words 
                   (form, syl_count, is_root, is_compound, compound_type,
                    derivation_mask, consensus_prefix, is_function_word, notes,
                    ipa, syllables)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (root, int(syl), is_root_val, is_compound_val, compound_type_val,
                 mask, prefix, is_func_val, notes,
                 ipa_val, syl_division),
            )
            word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError as e:
            errors.append(f"'{root}' ({english}): {e}")
            continue

        # ── Insert meanings with pos tags ──
        meanings = entry.get("meanings")
        if meanings:
            # New template: per-PoS meaning fields
            sort_counter = {}
            for pos_letter in ("N", "V", "A", "D"):
                glosses = meanings.get(pos_letter, [])
                for gloss in glosses:
                    so = sort_counter.get(pos_letter, 0)
                    conn.execute(
                        "INSERT INTO meanings (word_id, gloss, language, sort_order, pos) VALUES (?, ?, ?, ?, ?)",
                        (word_id, gloss, "en", so, pos_letter),
                    )
                    sort_counter[pos_letter] = so + 1
        elif entry.get("pos") and entry.get("_legacy_meaning"):
            # Function word template: single meaning with explicit POS
            conn.execute(
                "INSERT INTO meanings (word_id, gloss, language, sort_order, pos) VALUES (?, ?, ?, ?, ?)",
                (word_id, entry["_legacy_meaning"], "en", 0, entry["pos"]),
            )
        elif entry.get("_legacy_meaning"):
            # Legacy template: meaning without pos — insert with empty pos
            conn.execute(
                "INSERT INTO meanings (word_id, gloss, language, sort_order, pos) VALUES (?, ?, ?, ?, ?)",
                (word_id, entry["_legacy_meaning"], "en", 0, ""),
            )

        # ── Compound data (compound_components + compound_meta) ──
        if is_compound_val:
            compound_ok = _insert_compound_data(conn, word_id, entry, root, english, errors)
            if not compound_ok:
                # Roll back this word — compound insertion failed
                conn.execute("DELETE FROM words WHERE id = ?", (word_id,))
                conn.execute("DELETE FROM meanings WHERE word_id = ?", (word_id,))
                continue

        # ── Inflection generation (conditional on derivation mask) ──
        # SSOT: rules/4-meta/word-creation-pipeline.md §V-D
        mask = (mask or "").upper()
        if is_func or not mask:
            form_types = []
        else:
            form_types = MASK_TO_FORMS.get(mask, ['noun', 'verb', 'adjective', 'adverb'])

        for ft in form_types:
            if ft in ("adjective", "adverb"):
                form = f"{root}s"
            else:
                form = root
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, ft, form),
            )

        added += 1

    conn.commit()
    populate_search_text(conn)
    rebuild_fts(conn)

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")

    if added > 0:
        total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        print(f"\nAdded {added} entries to database.")
        print(f"Total entries: {total}")

    conn.close()