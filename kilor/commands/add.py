"""Process a filled-in today.md and add entries to the database."""

import os
import re

from ..db import get_db, rebuild_fts
from ..phonology import validate_content_root, count_syllables, get_case_forms

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECTION_MAP = {
    "nature": "1", "body": "2", "animal": "2", "food": "1",
    "clothing": "1", "home": "1", "tool": "1", "action": "3",
    "quality": "4", "direction": "6", "people": "6", "social": "6",
    "general": "7",
}

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

        if current:
            if "| Kilor Root |" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current["root"] = val
            elif "| Category" in line or "| Derivation Mask" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current["mask"] = val
            elif "| Syllable Count |" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val and val.isdigit():
                        current["syl"] = val
            elif "| Decision" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current["decision"] = val
            elif "| Notes |" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current["notes"] = val

    if current and current.get("root"):
        entries.append(current)

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

        valid, err = validate_content_root(root)
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
        section = SECTION_MAP.get(domain, "7")

        try:
            conn.execute(
                """INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                   derivation_mask, section, consensus_prefix, is_function_word, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (root, int(syl), 1, 0, None, mask, section, "o-", 0, notes),
            )
            word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError as e:
            errors.append(f"'{root}' ({english}): {e}")
            continue

        conn.execute(
            "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, ?, ?)",
            (word_id, english, "en", 0),
        )

        # Conditional inflection generation based on derivation mask
        # (SSOT: rules/4-meta/word-creation-pipeline.md §V-D)
        mask = (mask or "").upper()
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