"""Migrate data from lexicon.csv + compounds.json into SQLite."""

import csv
import json
import os
import sqlite3

from .. import phonology as ph
from ..db import get_db, DB_PATH, _rebuild_fts

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(SCRIPT_DIR, "data", "archive", "lexicon.csv")
COMPOUNDS_PATH = os.path.join(SCRIPT_DIR, "data", "archive", "compounds.json")


def load_legacy_csv():
    """Load lexicon.csv into list of dicts."""
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            clean = {k: (v if v is not None else "") for k, v in row.items()}
            rows.append(clean)
        return rows


def load_legacy_compounds():
    """Load compounds.json."""
    if not os.path.exists(COMPOUNDS_PATH):
        return {}
    with open(COMPOUNDS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("compounds", {})


def cmd_migrate():
    """Migrate data from lexicon.csv + compounds.json into SQLite."""
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    if existing > 0:
        print(f"Database already has {existing} words. This command is for initial migration only.")
        print("To re-migrate, delete data/kilor.db first.")
        return

    lexicon = load_legacy_csv()
    compounds = load_legacy_compounds()

    if not lexicon:
        print("No lexicon.csv found. Nothing to migrate.")
        return

    root_map = {}
    compound_root_form_map = {}
    compound_bare_roots = set()
    bare_root_to_form = {}

    # First pass: collect compound indicators
    for row in lexicon:
        bare = row.get("bare_root", "").strip()
        notes_val = (row.get("notes") or "").strip().lower()
        if not bare:
            continue
        if notes_val.startswith("compound:"):
            compound_bare_roots.add(bare)
            bare_root_to_form[bare] = bare
        else:
            bare_root_to_form[bare] = bare

    # Phase 1: Insert all lexicon.csv entries
    print("Migrating roots...")
    root_count = 0
    func_count = 0

    for row in lexicon:
        bare = row.get("bare_root", "").strip()
        if not bare:
            continue

        raw_is_func = (row.get("is_function_word") or "").strip()
        raw_prefix = (row.get("consensus_prefix") or "").strip()
        raw_adverb = (row.get("adverb") or "").strip()

        # Auto-detect column-shift in legacy CSV
        if raw_adverb.lower() == "true" and raw_is_func.lower() not in ("true", "false"):
            is_func = True
            notes_val = raw_prefix
            consensus_prefix = ""
        elif raw_prefix.lower() in ("true", "false") and raw_is_func.lower() not in ("true", "false"):
            is_func = raw_prefix.lower() == "true"
            notes_val = raw_is_func
            consensus_prefix = ""
        else:
            is_func = raw_is_func.lower() == "true"
            notes_val = (row.get("notes") or "").strip()
            consensus_prefix = raw_prefix

        is_compound = bare in compound_bare_roots
        is_root = not is_compound

        syl_raw = row.get("syl", "").strip()
        if syl_raw.isdigit():
            syl = int(syl_raw)
        elif syl_raw == "":
            # Toneless closed-class particles / empty syl column
            syl = 0
        else:
            syl = ph.count_syllables(bare)
        mask = row.get("derivation_mask", row.get("category", "")).strip()
        section = row.get("section", "").strip() or "I"

        try:
            conn.execute(
                """INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                   derivation_mask, section, consensus_prefix, is_function_word, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (bare, syl, 1, 0, None, mask, section, consensus_prefix or "o-", 1 if is_func else 0, notes_val),
            )
            word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError as e:
            print(f"  Skipping duplicate: {bare} ({e})")
            continue

        # Inflections — only for content roots (not function words / particles)
        if not is_func:
            for ft in ("noun", "verb", "adjective", "adverb"):
                ft_form = row.get(ft, "").strip()
                if ft_form:
                    conn.execute(
                        "INSERT OR IGNORE INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                        (word_id, ft, ft_form),
                    )

        # Meanings — split on '/'
        meaning_raw = row.get("meaning", "").strip()
        if meaning_raw:
            glosses = [g.strip() for g in meaning_raw.split("/")]
            for i, gloss in enumerate(glosses):
                if gloss:
                    conn.execute(
                        "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, ?, ?)",
                        (word_id, gloss, "en", i),
                    )

        root_map[bare] = word_id
        if is_func:
            func_count += 1
        else:
            root_count += 1

    conn.commit()
    print(f"  Roots: {root_count}, Function words: {func_count}")

    # Phase 2: Multi-word compounds
    print("Migrating multi-word compounds...")
    multi_count = 0
    for form, comp in compounds.items():
        if comp.get("type") != "multi":
            continue

        existing_check = conn.execute("SELECT id FROM words WHERE form = ?", (form,)).fetchone()
        if existing_check:
            continue

        meaning = comp.get("meaning", "")
        pattern = comp.get("pattern", "")
        rule_ref = comp.get("rule_ref", None)
        construction = comp.get("construction", [])

        mask_map = {
            "agentive": "N", "instrument": "N", "property": "N", "measure": "N",
            "process": "N", "location": "N", "doctrine": "N", "capability": "NV",
            "without": "N", "epistemic-modal": "D",
        }
        mask = mask_map.get(pattern, "N")
        sec = "I"
        syl_total = sum(ph.count_syllables(c) for c in construction)

        try:
            conn.execute(
                """INSERT INTO words (form, syl_count, is_root, is_compound, compound_type,
                   derivation_mask, section, consensus_prefix, is_function_word, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (form, syl_total, 0, 1, "multi", mask, sec, "o-", 0, ""),
            )
            word_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        except sqlite3.IntegrityError:
            continue

        if meaning:
            conn.execute(
                "INSERT INTO meanings (word_id, gloss, language, sort_order) VALUES (?, ?, ?, ?)",
                (word_id, meaning, "en", 0),
            )

        for pos, comp_form in enumerate(construction):
            comp_id = root_map.get(comp_form)
            if comp_id:
                conn.execute(
                    "INSERT OR IGNORE INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
                    (word_id, comp_id, pos),
                )

        conn.execute(
            "INSERT OR REPLACE INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, ?)",
            (word_id, pattern, rule_ref),
        )
        multi_count += 1

    conn.commit()
    print(f"  Multi-word compounds: {multi_count}")

    # Phase 3: Mono-word compound metadata
    print("Linking mono-word compound metadata...")
    mono_meta_count = 0
    for form, comp in compounds.items():
        if comp.get("type") != "mono":
            continue

        word_row = conn.execute("SELECT id FROM words WHERE form = ?", (form,)).fetchone()
        if not word_row:
            continue

        word_id = word_row["id"]
        pattern = comp.get("pattern", "")
        rule_ref = comp.get("rule_ref", None)
        construction = comp.get("construction", [])

        conn.execute(
            "INSERT OR REPLACE INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, ?)",
            (word_id, pattern, rule_ref),
        )

        for pos, comp_form in enumerate(construction):
            comp_id = root_map.get(comp_form)
            if comp_id:
                conn.execute(
                    "INSERT OR IGNORE INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
                    (word_id, comp_id, pos),
                )

        conn.execute("UPDATE words SET is_compound = 1, compound_type = 'mono' WHERE id = ?", (word_id,))
        mono_meta_count += 1

    conn.commit()
    print(f"  Mono-word compound metadata: {mono_meta_count}")

    _rebuild_fts(conn)

    total = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    print(f"\n✅ Migration complete. {total} total words in database.")