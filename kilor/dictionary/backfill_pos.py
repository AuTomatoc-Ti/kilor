"""One-shot script: backfill pos column in meanings table.

- Single-mask (N only, D only): all meanings get that pos
- Multi-mask with meanings_count == mask_length: positional inference
- Multi-mask with mismatch: leave pos='' for manual review
- Function words (is_function_word=1): classify by form into POS tags
- Pronouns: by form match
- Numerals: by form match
- Empty mask content words: leave pos='' for manual review

Run once. Safe to re-run (no data loss).
"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "kilor.db")

# SSOT: closed-class particle inventory from grammar-syntax.md §IV-C
FUNCTION_WORD_POS = {
    "ei": "CCONJ", "amer": "CCONJ", "tu": "CCONJ",
    "li": "SCONJ", "bam": "SCONJ", "kus": "SCONJ", "tor": "SCONJ", "les": "SCONJ",
    "te": "ADP", "sy": "ADP", "mer": "ADP", "ar": "ADP", "tilpe": "ADP", "na": "ADP", "ne": "ADP",
    "nar": "PART", "po": "PART", "pem": "PART", "pona": "PART", "pemna": "PART",
    "gin": "PART", "ger": "PART", "gou": "PART", "sor": "PART", "chom": "PART", "maug": "PART",
    "bam": "SCONJ",  # bam appears in both SCONJ and PART; SCONJ is primary (conditional)
    "fidak": "PART", "arfi": "PART", "orse": "PART", "tilpi": "PART", "tilpa": "PART",
    "shoun": "PART", "mitok": "PART",
    "aiga": "PART", "hoskar": "PART",
    "torra": "SCONJ", "wetor": "SCONJ", "mangus": "SCONJ",
    "thin": "DEM", "tha": "DEM",
    "res": "PART", "os": "PART", "iu": "PART",
    # Spatial postpositions (ADP)
    "ikne": "ADP", "oukne": "ADP", "umne": "ADP", "rapne": "ADP",
    "haune": "ADP", "paune": "ADP", "hinne": "ADP", "tene": "ADP",
    "orane": "ADP", "meipone": "ADP",
    # Emotional particle variants (PART)
    "awei": "PART", "aewei": "PART", "ewei": "PART", "iwei": "PART",
    "owei": "PART", "uwei": "PART", "ywei": "PART",
    "aeweisan": "PART",
    # Misc
    "dir": "PART",
}

MODAL_FORMS = {"mug", "som", "sew", "hostak", "shunle"}

PRONOUN_FORMS = {"ki", "ti", "si", "ni", "kilo", "tilo", "silo", "nilo",
                  "kin", "tin", "sin", "nin", "kilon", "tilon", "silon", "nilon",
                  "kis", "tis", "sis", "nis", "kilos", "tilos", "silos", "nilos"}

NUMERAL_FORMS = {"mo", "do", "ro", "foi", "tai", "slo", "lai", "auk", "wy", "gau",
                  "mai", "doi", "rai", "aniu", "cu", "kas", "hus", "tus", "rakas",
                  "roli", "es", "esa"}


def backfill():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all words with their masks and types
    words = cur.execute("""
        SELECT id, form, derivation_mask, is_root, is_function_word, is_compound, compound_type
        FROM words
    """).fetchall()

    word_map = {}
    for w in words:
        word_map[w["id"]] = dict(w)

    # Get all meanings
    meanings = cur.execute("""
        SELECT m.id, m.word_id, m.gloss, m.sort_order,
               w.derivation_mask, w.is_function_word, w.form
        FROM meanings m
        JOIN words w ON m.word_id = w.id
        ORDER BY m.word_id, m.sort_order
    """).fetchall()

    # Group meanings by word_id
    from collections import defaultdict
    word_meanings = defaultdict(list)
    for m in meanings:
        word_meanings[m["word_id"]].append(dict(m))

    updated = 0
    skipped = 0

    for wid, mlist in word_meanings.items():
        winfo = word_map.get(wid)
        if not winfo:
            continue
        mask = (winfo["derivation_mask"] or "").strip().upper()
        is_func = winfo["is_function_word"]
        form = winfo["form"]
        mcount = len(mlist)
        mask_len = len(mask)

        # ── Case 1: Pronouns (check before is_func — may be marked as func word in DB) ──
        if form in PRONOUN_FORMS:
            for m in mlist:
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", ("PRON", m["id"]))
            updated += mcount
            continue

        # ── Case 2: Numerals (check before is_func) ──────────
        if form.lower() in NUMERAL_FORMS:
            for m in mlist:
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", ("NUM", m["id"]))
            updated += mcount
            continue

        # ── Case 3: Modal verbs (check before is_func) ───────
        if form.lower() in MODAL_FORMS:
            for m in mlist:
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", ("MODAL", m["id"]))
            updated += mcount
            continue

        # ── Case 4: Function words ────────────────────────────
        if is_func:
            pos = FUNCTION_WORD_POS.get(form.lower(), "")
            if not pos:
                print(f"  WARNING: function word '{form}' not in POS map — leaving empty")
            for m in mlist:
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", (pos, m["id"]))
            if pos:
                updated += mcount
            else:
                skipped += mcount
            continue

        # ── Case 5: Empty mask (other content words) ──────────
        if not mask:
            # Some roots have empty mask — leave for manual review
            skipped += mcount
            continue

        # ── Case 6: Content words with mask ───────────────────
        # Single-letter mask: all meanings get that pos
        if mask_len == 1:
            for m in mlist:
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", (mask, m["id"]))
            updated += mcount
            continue

        # Multi-letter mask with exact match
        if mcount == mask_len:
            for i, m in enumerate(mlist):
                if i < mask_len:
                    cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", (mask[i], m["id"]))
            updated += mcount
            continue

        # Multi-letter mask with fewer meanings: assign first meanings to first mask letters
        if mcount < mask_len:
            for i, m in enumerate(mlist):
                cur.execute("UPDATE meanings SET pos = ? WHERE id = ?", (mask[i], m["id"]))
            updated += mcount
            continue

        # More meanings than mask letters: undecidable, leave for manual review
        skipped += mcount

    conn.commit()
    conn.close()

    print(f"Backfill complete: {updated} meanings updated, {skipped} skipped (need manual review)")
    return updated, skipped


if __name__ == "__main__":
    backfill()