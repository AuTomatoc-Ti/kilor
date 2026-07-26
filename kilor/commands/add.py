"""Process a filled-in today.md and add entries to the database."""

import os
import re
import sqlite3

from ..db import get_db, rebuild_fts, populate_search_text
from ..phonology import validate_content_root, count_syllables, get_case_forms
from ..schema import VALID_POS

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    # --- Syllable Count ---
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

    if not entries:
        print("No entries found in today.md. Make sure you've filled in the Kilor Root column.")
        return

    conn = get_db()
    added = 0
    errors = []

    for entry in entries:
        root = entry.get("root", "")
        english = entry.get("english", "")
        domain = entry.get("domain", "?")

        if not root:
            errors.append(f"'{english}': no Kilor root provided")
            continue

        is_compound = " " in root
        valid, err = validate_content_root(root, is_compound=is_compound)
        if not valid:
            errors.append(f"'{root}' ({english}): {err}")
            continue

        existing = conn.execute("SELECT id FROM words WHERE form = ?", (root,)).fetchone()
        if existing:
            errors.append(f"'{root}' ({english}): duplicate — already exists")
            continue

        syl = str(count_syllables(root))
        mask = entry.get("mask", "")
        notes = entry.get("notes", entry.get("decision", "root"))

        try:
            conn.execute(
                """INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                   derivation_mask, consensus_prefix, is_function_word, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (root, int(syl), 1, 0, None, mask, "o-", 0, notes),
            )
            word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError as e:
            errors.append(f"'{root}' ({english}): {e}")
            continue

        # Insert meanings with pos tags
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

        # Determine is_function_word
        is_func = 1 if entry.get("pos") else 0

        # Conditional inflection generation based on derivation mask
        # (SSOT: rules/4-meta/word-creation-pipeline.md §V-D)
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