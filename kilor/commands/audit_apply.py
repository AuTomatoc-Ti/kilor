"""Apply changes from an annotated audit sheet back to the database."""

import os
import re
import sys

from ..db import get_db, rebuild_fts, populate_search_text
from ..phonology import (
    validate_content_root,
    count_syllables,
    split_syllables,
    to_ipa,
    get_case_forms,
)
from ..schema import VALID_POS

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _parse_audit_sheet(filepath):
    """Parse audit-batch.md into a list of word sections.

    Returns: list of dicts with keys:
        word_id (int), form (str), fields (list of (name, current, desired))
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    sections = []
    # Split on ### header lines
    parts = re.split(r"\n(?=### )", text)
    for part in parts:
        if not part.startswith("### "):
            continue
        header_match = re.match(r"### (.+) \(id: (\d+)\)", part)
        if not header_match:
            print(f"  ⚠ Skipping unparseable section header: {part[:80]}...")
            continue
        form_name = header_match.group(1)
        word_id = int(header_match.group(2))

        fields = []
        # Parse each table row: | Field | Current | Desired |
        for line in part.split("\n"):
            line = line.strip()
            if not line.startswith("|") or "---" in line or "Desired Change" in line:
                continue
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) < 3:
                continue
            field_name = cols[0]
            current_val = cols[1]
            desired_val = cols[2]
            fields.append((field_name, current_val, desired_val))

        sections.append({"word_id": word_id, "form": form_name, "fields": fields})

    return sections


def _parse_meanings(desired_str):
    """Parse 'gloss (POS), gloss (POS)' into [(gloss, pos), ...].

    Returns None if desired_str is '(none)' (clear all meanings).
    Returns None if '--' (no change, caller should skip).
    """
    if desired_str.strip() == "--":
        return None  # signal: no change
    if desired_str.strip().lower() == "(none)":
        return []  # signal: clear all

    results = []
    # Normalize human-written POS tags to canonical values
    _POS_NORMALIZE = {
        "adj": "A", "adjective": "A",
        "adv": "D", "adverb": "D",
        "v": "V", "verb": "V",
        "n": "N", "noun": "N",
    }
    # Split on "), " — this strips the closing paren from all parts except the last.
    # To handle both "gloss (POS)" and "gloss (POS" (split fragment), strip
    # any trailing close-paren before matching.
    parts = re.split(r"\),\s*", desired_str)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Strip trailing ) so both "gloss (POS)" and "gloss (POS" normalize to "gloss (POS"
        part = part.rstrip(")")
        m = re.match(r"^(.+?)\s*\(([^)]+)$", part)
        if m:
            gloss = m.group(1).strip()
            pos = m.group(2).strip()
        else:
            gloss = part.strip()
            pos = ""
        # Normalize POS to canonical uppercase single-letter
        pos = _POS_NORMALIZE.get(pos.lower(), pos.upper() if pos else "")
        if gloss and gloss.lower() != "(none)":
            results.append((gloss, pos))
    return results if results else []


def _parse_inflections(desired_str):
    """Parse 'noun: form, verb: form, acc: form' into [(type, form), ...].

    Returns None if '--' (no change).
    Returns [] if '(none)' (clear all).
    """
    if desired_str.strip() == "--":
        return None
    if desired_str.strip().lower() == "(none)":
        return []

    results = []
    for part in desired_str.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\S+):\s*(.+)$", part)
        if m:
            results.append((m.group(1), m.group(2).strip()))
        else:
            print(f"    ⚠ Could not parse inflection: '{part}'")
    return results


def _parse_components(desired_str):
    """Parse 'root1 + root2 + root3' into [form1, form2, form3].

    Returns None if '--' (no change).
    Returns [] if '(none)' (clear/convert compound → root).
    """
    if desired_str.strip() == "--":
        return None
    if desired_str.strip().lower() == "(none)":
        return []
    return [c.strip() for c in desired_str.split("+") if c.strip()]


def _word_type_label(w):
    if w["is_function_word"]:
        return "function"
    if w["is_compound"]:
        return f"compound-{w['compound_type']}" if w["compound_type"] else "compound"
    return "root"


def _apply_form_change(conn, word_id, old_form, new_form, is_func, is_compound):
    """Validate and apply a form change. Returns (new_form, ipa, syl_count, syllables) or None on error."""
    valid, err = validate_content_root(new_form, is_func=is_func, is_compound=is_compound)
    if not valid:
        return f"invalid form: {err}"

    existing = conn.execute(
        "SELECT id FROM words WHERE form = ? AND id != ?", (new_form, word_id)
    ).fetchone()
    if existing:
        return f"form '{new_form}' already exists (id={existing['id']})"

    syl = count_syllables(new_form)
    syl_div = split_syllables(new_form)
    if isinstance(syl_div, list):
        syl_div = ".".join(syl_div)
    ipa_str = to_ipa(new_form)

    conn.execute(
        "UPDATE words SET form = ?, syl_count = ?, syllables = ?, ipa = ?, updated_at = datetime('now') WHERE id = ?",
        (new_form, syl, syl_div, ipa_str, word_id),
    )
    return (new_form, ipa_str, syl, syl_div), None


def _apply_inflections(conn, word_id, infl_list, derivation_mask):
    """Replace inflections for a word. Applies ACC/GEN via get_case_forms.

    If infl_list is None (user left --), regenerate from derivation_mask.
    If infl_list is empty list (user wrote (none)), clear all.
    """
    conn.execute("DELETE FROM inflections WHERE word_id = ?", (word_id,))

    if infl_list is None:
        # Auto-regenerate from mask
        word = conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
        if not word:
            return
        mask = derivation_mask or word["derivation_mask"] or ""
        form = word["form"]
        mask = mask.upper()

        # Standard inflections by mask
        mask_to_forms = {
            "N": ["noun"], "V": ["verb"], "A": ["adjective"], "D": ["adverb"],
            "NV": ["noun", "verb"], "NA": ["noun", "adjective"],
            "AV": ["adjective", "verb"], "AD": ["adjective", "adverb"],
            "ND": ["noun", "adverb"], "VD": ["verb", "adverb"],
            "NVAD": ["noun", "verb", "adjective", "adverb"],
            "NVA": ["noun", "verb", "adjective"],
            "NAD": ["noun", "adjective", "adverb"],
            "VAD": ["verb", "adjective", "adverb"],
        }
        form_types = mask_to_forms.get(mask, [])
        for ft in form_types:
            infl_form = f"{form}s" if ft in ("adjective", "adverb") else form
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, ft, infl_form),
            )

        # ACC/GEN
        is_func = bool(word["is_function_word"])
        compound_type = word["compound_type"]
        acc, gen = get_case_forms(form, derivation_mask=mask or None,
                                   is_function_word=is_func, compound_type=compound_type)
        if acc:
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, "accusative", acc),
            )
        if gen:
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, "genitive", gen),
            )
    else:
        # User provided explicit list
        for ft, f in infl_list:
            conn.execute(
                "INSERT INTO inflections (word_id, form_type, form) VALUES (?, ?, ?)",
                (word_id, ft, f),
            )

    conn.execute("UPDATE words SET updated_at = datetime('now') WHERE id = ?", (word_id,))


def _apply_compound_components(conn, word_id, comp_forms):
    """Rebuild compound_components from a list of component forms.

    Validates all components exist, then replaces entries.
    """
    conn.execute("DELETE FROM compound_components WHERE compound_id = ?", (word_id,))
    comp_ids = []
    for pos, cform in enumerate(comp_forms):
        row = conn.execute("SELECT id FROM words WHERE form = ?", (cform,)).fetchone()
        if not row:
            return f"component '{cform}' not found in database"
        comp_ids.append(row["id"])
        conn.execute(
            "INSERT INTO compound_components (compound_id, component_id, position) VALUES (?, ?, ?)",
            (word_id, row["id"], pos),
        )
    return None


def cmd_audit_apply(filepath=None, batch_size=20, batch_start=0,
                    dry_run=False, commit=False, only_reviewed=False):
    """Apply changes from an annotated audit sheet.

    Usage:
        python kilor.py audit-apply [--file draft/audit-batch.md] [--batch-size 20] [--batch-start 0]
        python kilor.py audit-apply --dry-run   # preview changes only
        python kilor.py audit-apply             # apply first batch (0..20)
        python kilor.py audit-apply --batch-start 20  # apply second batch
        python kilor.py audit-apply --only-reviewed --commit  # only apply [x] reviewed words
    """
    if filepath is None:
        filepath = os.path.join(SCRIPT_DIR, "draft", "audit-batch.md")

    if not os.path.exists(filepath):
        print(f"Error: audit sheet not found at {filepath}")
        return False

    sections = _parse_audit_sheet(filepath)
    conn = get_db()

    # Track review status per word
    not_reviewed_count = 0
    relevant = []
    for sec in sections:
        # Extract reviewed status: look for "Reviewed" field
        reviewed = False
        for fname, _cur, desired in sec["fields"]:
            if fname == "Reviewed":
                reviewed = "x" in _cur.lower()
                break

        has_changes = any(
            desired.strip() != "--" for fname, _cur, desired in sec["fields"]
            if fname != "Reviewed"
        )
        if has_changes:
            if only_reviewed and not reviewed:
                not_reviewed_count += 1
                continue
            relevant.append(sec)

    print(f"Parsed {len(sections)} words, {len(relevant)} with changes to apply.")
    if only_reviewed:
        print(f"  ({not_reviewed_count} unreviewed words skipped)")
    else:
        unreviewed = sum(
            1 for sec in relevant
            if not any("x" in _cur.lower() for fname, _cur, desired in sec["fields"] if fname == "Reviewed")
        )
        if unreviewed:
            print(f"  (⚠ {unreviewed} words with changes are not yet reviewed)")

    if len(relevant) == 0:
        print("No changes to apply.")
        conn.close()
        return True

    if dry_run:
        print("\n=== DRY RUN — no changes will be committed ===\n")
    else:
        print(f"\nApplying batch {batch_start // batch_size + 1} ({batch_start}..{batch_start + batch_size})")
        print(f"  ({commit = })")

    # Slice to batch
    batch = relevant[batch_start:batch_start + batch_size]
    if not batch:
        print("No words in this batch range.")
        conn.close()
        return True

    errors = []
    applied_count = 0
    skip_count = 0
    applied_reviewed = 0

    for sec in batch:
        word_id = sec["word_id"]
        form = sec["form"]

        word = conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
        if not word:
            errors.append(f"  ❌ Word '{form}' (id={word_id}) not found in DB — skipped")
            skip_count += 1
            continue

        changes_made = []
        needs_infl_regenerate = False
        form_changed = False
        mask_changed = False

        # Build a dict: field_name → desired_value
        desired_map = {}
        for fname, _cur, desired in sec["fields"]:
            desired_map[fname] = desired.strip()

        # --- Apply changes in order ---

        # 1. Form
        if desired_map.get("Form", "--") != "--":
            new_form = desired_map["Form"]
            if new_form.lower() == "(none)":
                errors.append(f"  ❌ {form} (id={word_id}): Form cannot be (none) — skipped")
                skip_count += 1
                continue
            is_func = bool(word["is_function_word"])
            is_compound = bool(word["is_compound"])
            result = _apply_form_change(conn, word_id, form, new_form, is_func, is_compound)
            if isinstance(result, str):
                errors.append(f"  ❌ {form} (id={word_id}): {result}")
                skip_count += 1
                continue
            else:
                new_form_data, _ = result
                form = new_form_data[0]
                changes_made.append(f"Form: {new_form}")
                form_changed = True
                needs_infl_regenerate = True

        # 2. Word Type (conversion root ↔ compound)
        if desired_map.get("Word Type", "--") != "--":
            new_type = desired_map["Word Type"]
            if new_type.startswith("compound"):
                conn.execute(
                    "UPDATE words SET is_compound = 1, is_root = 0, is_function_word = 0, compound_type = ?, updated_at = datetime('now') WHERE id = ?",
                    (new_type.split("-")[1] if "-" in new_type else "mono", word_id),
                )
                changes_made.append(f"Word Type → {new_type}")
            elif new_type == "root":
                conn.execute(
                    "UPDATE words SET is_compound = 0, is_root = 1, is_function_word = 0, compound_type = NULL, updated_at = datetime('now') WHERE id = ?",
                    (word_id,),
                )
                changes_made.append("Word Type → root")
            elif new_type == "function":
                conn.execute(
                    "UPDATE words SET is_compound = 0, is_root = 0, is_function_word = 1, compound_type = NULL, derivation_mask = '', updated_at = datetime('now') WHERE id = ?",
                    (word_id,),
                )
                changes_made.append("Word Type → function")

        # 3. Consensus Prefix
        if desired_map.get("Consensus Prefix", "--") != "--":
            new_prefix = desired_map["Consensus Prefix"]
            if new_prefix.lower() != "(none)":
                conn.execute(
                    "UPDATE words SET consensus_prefix = ?, updated_at = datetime('now') WHERE id = ?",
                    (new_prefix, word_id),
                )
                changes_made.append(f"Prefix: {new_prefix}")

        # 4. Derivation Mask
        if desired_map.get("Derivation Mask", "--") != "--":
            new_mask = desired_map["Derivation Mask"]
            if new_mask.lower() == "(none)":
                new_mask = ""
            if new_mask.lower() == "null":
                new_mask = ""
            new_mask = new_mask.upper()
            if new_mask == "(CLOSED-CLASS)":
                new_mask = ""
            if new_mask:
                valid_chars = set("NVAD")
                if not all(c in valid_chars for c in new_mask):
                    errors.append(f"  ❌ {form} (id={word_id}): invalid mask '{new_mask}'")
                    skip_count += 1
                    continue
            conn.execute(
                "UPDATE words SET derivation_mask = ?, updated_at = datetime('now') WHERE id = ?",
                (new_mask, word_id),
            )
            changes_made.append(f"Mask: {new_mask or '(closed-class)'}")
            mask_changed = True
            needs_infl_regenerate = True

        # 5. Meanings
        parsed_meanings = _parse_meanings(desired_map.get("Meanings", "--"))
        if parsed_meanings is not None:
            conn.execute("DELETE FROM meanings WHERE word_id = ?", (word_id,))
            for sort_order, (gloss, pos) in enumerate(parsed_meanings):
                conn.execute(
                    "INSERT INTO meanings (word_id, gloss, language, sort_order, pos) VALUES (?, ?, 'en', ?, ?)",
                    (word_id, gloss, sort_order, pos),
                )
            conn.execute(
                "UPDATE words SET updated_at = datetime('now') WHERE id = ?",
                (word_id,),
            )
            if parsed_meanings:
                changes_made.append(f"Meanings: {len(parsed_meanings)} gloss(es)")
            else:
                changes_made.append("Meanings: cleared")

        # 6. Status
        if desired_map.get("Status", "--") != "--":
            new_status = desired_map["Status"]
            if new_status.lower() not in ("(none)", "--"):
                valid_statuses = ("draft", "active", "deprecated", "superseded")
                if new_status in valid_statuses:
                    conn.execute(
                        "UPDATE words SET status = ?, updated_at = datetime('now') WHERE id = ?",
                        (new_status, word_id),
                    )
                    changes_made.append(f"Status: {new_status}")
                else:
                    errors.append(f"  ❌ {form} (id={word_id}): invalid status '{new_status}'")

        # 7. Notes
        if desired_map.get("Notes", "--") != "--":
            new_notes = desired_map["Notes"]
            if new_notes.lower() in ("(none)", "(clear)", "(delete)", "(remove)"):
                new_notes = ""
            conn.execute(
                "UPDATE words SET notes = ?, updated_at = datetime('now') WHERE id = ?",
                (new_notes, word_id),
            )
            changes_made.append(f"Notes: {'(cleared)' if new_notes == '' else new_notes}")

        # 8. Syllable Count (explicit — only if form didn't change)
        if desired_map.get("Syllable Count", "--") != "--" and not form_changed:
            val = desired_map["Syllable Count"]
            if val.lower() not in ("--", "(none)"):
                try:
                    sc = int(val)
                    conn.execute(
                        "UPDATE words SET syl_count = ?, updated_at = datetime('now') WHERE id = ?",
                        (sc, word_id),
                    )
                    changes_made.append(f"Syl Count: {sc}")
                except ValueError:
                    errors.append(f"  ❌ {form} (id={word_id}): invalid syllable count '{val}'")

        # 9. Syllable Division (explicit — only if form didn't change)
        if desired_map.get("Syllable Division", "--") != "--" and not form_changed:
            val = desired_map["Syllable Division"]
            if val.lower() not in ("--", "(none)"):
                conn.execute(
                    "UPDATE words SET syllables = ?, updated_at = datetime('now') WHERE id = ?",
                    (val, word_id),
                )
                changes_made.append(f"Syllables: {val}")

        # 10. Components
        parsed_comps = _parse_components(desired_map.get("Components", "--"))
        if parsed_comps is not None:
            if parsed_comps:
                err = _apply_compound_components(conn, word_id, parsed_comps)
                if err:
                    errors.append(f"  ❌ {form} (id={word_id}): {err}")
                    skip_count += 1
                    continue
                # Ensure word is set as compound
                conn.execute(
                    "UPDATE words SET is_compound = 1, is_root = 0, is_function_word = 0, compound_type = 'mono', updated_at = datetime('now') WHERE id = ?",
                    (word_id,),
                )
                changes_made.append(f"Components: {' + '.join(parsed_comps)}")
            else:
                # Clearing components → convert to root
                conn.execute("DELETE FROM compound_components WHERE compound_id = ?", (word_id,))
                conn.execute("DELETE FROM compound_meta WHERE compound_id = ?", (word_id,))
                conn.execute(
                    "UPDATE words SET is_compound = 0, is_root = 1, compound_type = NULL, updated_at = datetime('now') WHERE id = ?",
                    (word_id,),
                )
                changes_made.append("Components: cleared (→ root)")

        # 11. Pattern
        if desired_map.get("Pattern", "--") != "--":
            new_pat = desired_map["Pattern"]
            if new_pat.lower() == "(none)":
                conn.execute("DELETE FROM compound_meta WHERE compound_id = ?", (word_id,))
                changes_made.append("Pattern: cleared")
            else:
                existing = conn.execute(
                    "SELECT 1 FROM compound_meta WHERE compound_id = ?", (word_id,)
                ).fetchone()
                if existing:
                    conn.execute(
                        "UPDATE compound_meta SET pattern = ? WHERE compound_id = ?",
                        (new_pat, word_id),
                    )
                else:
                    conn.execute(
                        "INSERT INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, ?, '')",
                        (word_id, new_pat),
                    )
                changes_made.append(f"Pattern: {new_pat}")

        # 12. Rule Ref
        if desired_map.get("Rule Ref", "--") != "--":
            new_rule_ref = desired_map["Rule Ref"]
            if new_rule_ref.lower() == "(none)":
                new_rule_ref = ""
            existing = conn.execute(
                "SELECT 1 FROM compound_meta WHERE compound_id = ?", (word_id,)
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE compound_meta SET rule_ref = ? WHERE compound_id = ?",
                    (new_rule_ref, word_id),
                )
            elif new_rule_ref:
                conn.execute(
                    "INSERT INTO compound_meta (compound_id, pattern, rule_ref) VALUES (?, '', ?)",
                    (word_id, new_rule_ref),
                )
            if new_rule_ref:
                changes_made.append(f"Rule Ref: {new_rule_ref}")

        # 13. Inflections (apply last, after form/mask changes)
        infl_desired = desired_map.get("Inflections", "--")
        # Detect diagnostic comments (e.g. "wrong tone marker") → force regenerate
        if infl_desired != "--" and infl_desired.lower() != "(none)":
            if any(kw in infl_desired.lower() for kw in ("wrong", "miss")):
                needs_infl_regenerate = True
                infl_desired = "--"
        parsed_infls = _parse_inflections(infl_desired)
        if parsed_infls is not None:
            # User explicitly set inflections — use those
            _apply_inflections(conn, word_id, parsed_infls, None)
            changes_made.append(f"Inflections: {len(parsed_infls)} form(s)")
        elif needs_infl_regenerate:
            # User left -- but form or mask changed → auto-regenerate
            # Pass None so _apply_inflections refetches the word (mask was already updated in DB)
            _apply_inflections(conn, word_id, None, None)
            changes_made.append("Inflections: auto-regenerated")

        # --- Done with this word ---
        if changes_made:
            applied_count += 1
            if commit:
                conn.commit()
                print(f"  ✅ {form} (id={word_id}):")
                for cm in changes_made:
                    print(f"      {cm}")
            else:
                print(f"  🔍 {form} (id={word_id}):")
                for cm in changes_made:
                    print(f"      {cm}")
                conn.rollback()

    # Post-batch operations
    if commit and not dry_run:
        populate_search_text(conn)
        rebuild_fts(conn)

    print(f"\nBatch complete: {applied_count} applied, {len(errors)} errors, {skip_count} skipped.")

    if errors:
        for e in errors:
            print(e)

    if not commit and not dry_run:
        print("\n⚠  This was a preview. Use --commit to actually apply changes.")

    conn.close()
    return len(errors) == 0