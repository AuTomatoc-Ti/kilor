"""Export all words as an audit sheet markdown file for human review & editing."""

import os
from datetime import datetime

from ..db import get_db
from ..phonology import get_case_forms, count_syllables, split_syllables, to_ipa

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _word_type_label(w):
    """Human-readable word type."""
    if w["is_function_word"]:
        return "function"
    if w["is_compound"]:
        return f"compound-{w['compound_type']}" if w['compound_type'] else "compound"
    return "root"


def _format_meanings(conn, word_id):
    """Format meanings as 'gloss (POS), gloss (POS)'."""
    rows = conn.execute(
        "SELECT gloss, pos FROM meanings WHERE word_id = ? ORDER BY sort_order",
        (word_id,),
    ).fetchall()
    if not rows:
        return "(none)"
    parts = []
    for r in rows:
        pos = r["pos"] or ""
        if pos:
            parts.append(f"{r['gloss']} ({pos})")
        else:
            parts.append(r["gloss"])
    return ", ".join(parts)


def _format_inflections(conn, word_id):
    """Format inflections including ACC/GEN as: 'noun: form, verb: form, acc: form, gen: form'."""
    rows = conn.execute(
        "SELECT form_type, form FROM inflections WHERE word_id = ? ORDER BY form_type",
        (word_id,),
    ).fetchall()
    if not rows:
        return "(none)"
    parts = []
    for r in rows:
        parts.append(f"{r['form_type']}: {r['form']}")
    return ", ".join(parts)


def _format_components(conn, word_id):
    """Format compound components for display."""
    if not conn.execute(
        "SELECT 1 FROM compound_components WHERE compound_id = ?", (word_id,)
    ).fetchone():
        return "--"
    comps = conn.execute(
        """SELECT w2.form
           FROM compound_components cc
           JOIN words w2 ON cc.component_id = w2.id
           WHERE cc.compound_id = ?
           ORDER BY cc.position""",
        (word_id,),
    ).fetchall()
    return " + ".join(c["form"] for c in comps)


def _format_pattern(conn, word_id):
    """Format compound pattern metadata."""
    row = conn.execute(
        "SELECT pattern, rule_ref FROM compound_meta WHERE compound_id = ?",
        (word_id,),
    ).fetchone()
    if not row:
        return "--", "--"
    return row["pattern"] or "--", row["rule_ref"] or "--"


def _format_examples(conn, word_id):
    """Return count of examples."""
    count = conn.execute(
        "SELECT COUNT(*) FROM examples WHERE word_id = ?", (word_id,)
    ).fetchone()[0]
    return f"{count} example(s)"


def _generate_word_section(conn, w):
    """Generate the markdown section for one word."""
    word_id = w["id"]
    form = w["form"]
    wtype = _word_type_label(w)
    mask = w["derivation_mask"] or "(closed-class)"
    prefix = w["consensus_prefix"] or "o-"
    status = w["status"] or "active"
    notes = w["notes"] or "--"
    syl_count = str(w["syl_count"])
    syllables = w["syllables"] or split_syllables(form)
    ipa_str = w["ipa"] or to_ipa(form)

    meanings = _format_meanings(conn, word_id)
    inflections = _format_inflections(conn, word_id)
    components = _format_components(conn, word_id)
    pattern, rule_ref = _format_pattern(conn, word_id)
    examples = _format_examples(conn, word_id)

    lines = []
    lines.append(f"### {form} (id: {word_id}) — {wtype}")
    lines.append("")
    lines.append("| Field                | Current Value                        | Desired Change (-- = no change) |")
    lines.append("|----------------------|--------------------------------------|----------------------------------|")
    lines.append(f"| Reviewed             | [ ]                                  | --                               |")
    lines.append(f"| Form                 | {form}                               | --                               |")
    lines.append(f"| IPA                  | {ipa_str}                            | --                               |")
    lines.append(f"| Word Type            | {wtype}                               | --                               |")
    lines.append(f"| Consensus Prefix     | {prefix}                             | --                               |")
    lines.append(f"| Derivation Mask      | {mask}                               | --                               |")
    lines.append(f"| Meanings             | {meanings}                           | --                               |")
    lines.append(f"| Status               | {status}                             | --                               |")
    lines.append(f"| Notes                | {notes}                              | --                               |")
    lines.append(f"| Syllable Count       | {syl_count}                          | --                               |")
    lines.append(f"| Syllable Division    | {syllables}                          | --                               |")
    lines.append(f"| Inflections          | {inflections}                        | --                               |")
    lines.append(f"| Components           | {components}                         | --                               |")
    lines.append(f"| Pattern              | {pattern}                            | --                               |")
    lines.append(f"| Rule Ref             | {rule_ref}                           | --                               |")
    lines.append(f"| Examples             | {examples}                           | --                               |")
    lines.append("")
    lines.append("> **Auto-computed:** IPA, Syllable Count, Syllable Division auto-compute when Form changes. Inflections + ACC/GEN auto-regenerate when Form or Mask changes — unless you explicitly fill a Desired Change value.")
    lines.append("")
    return "\n".join(lines)


def _build_header_lines(word_count, batch_num=None, total_batches=None,
                        word_start=None, word_end=None):
    """Build markdown header + instruction lines."""
    lines = []
    lines.append("<!-- Kilor Audit Sheet — generated for human review -->")
    lines.append(f"<!-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->")
    if batch_num is not None:
        lines.append(f"<!-- Batch {batch_num}/{total_batches} — words {word_start}–{word_end} -->")
    lines.append(f"<!-- Total words in this file: {word_count} -->")
    lines.append("<!-- Instructions: Replace '--' in the 'Desired Change' column with the complete desired value. -->")
    lines.append("<!--                Write '(none)' to clear a field. Leave '--' for no change. -->")
    lines.append("<!--                Mark 'Reviewed' as [x] when finished reviewing this word. -->")
    lines.append("<!--                Changing 'Components' from '--' to a value converts a root → compound. -->")
    lines.append("<!--                Changing 'Components' to '(none)' converts a compound → root. -->")
    lines.append("")
    if batch_num is not None:
        lines.append(f"# Kilor Audit — Batch {batch_num}/{total_batches} (words {word_start}–{word_end})")
    else:
        lines.append(f"# Kilor Audit Sheet — {word_count} words")
    lines.append("")
    return lines


def cmd_audit_export(output_path=None, split=False, batch_size=50):
    """Export all words to an audit sheet markdown file.

    Usage:
        python kilor.py audit-export [--output draft/audit-batch.md]
        python kilor.py audit-export --split [--batch-size 50]
    """
    conn = get_db()
    words = conn.execute("SELECT * FROM words ORDER BY form").fetchall()
    conn.close()

    if split:
        output_dir = output_path or os.path.join(SCRIPT_DIR, "draft", "audit")
        os.makedirs(output_dir, exist_ok=True)

        total_batches = (len(words) + batch_size - 1) // batch_size
        batch_index_lines = [
            "# Kilor Audit Index",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total words:** {len(words)}",
            f"**Batches:** {total_batches} × ~{batch_size} words",
            "",
            "| Batch | File | Words | Reviewed |",
            "|-------|------|-------|----------|",
        ]

        for i in range(total_batches):
            batch_num = i + 1
            start = i * batch_size
            end = min(start + batch_size, len(words))
            batch_words = words[start:end]

            batch_file = f"batch-{batch_num:03d}.md"
            batch_path = os.path.join(output_dir, batch_file)

            lines = _build_header_lines(
                len(batch_words), batch_num=batch_num,
                total_batches=total_batches, word_start=start + 1, word_end=end,
            )

            conn2 = get_db()
            for w in batch_words:
                lines.append(_generate_word_section(conn2, w))
            conn2.close()

            with open(batch_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            # Always start unreviewed — count reviewed from checked [x] in the file
            batch_index_lines.append(
                f"| {batch_num} | `{batch_file}` | {len(batch_words)} ({start + 1}–{end}) | 0/{len(batch_words)} |"
            )

        # Write index
        index_path = os.path.join(output_dir, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(batch_index_lines))

        print(f"Exported {len(words)} words to {output_dir}/ ({total_batches} batch files + index.md)")

    else:
        if output_path is None:
            output_path = os.path.join(SCRIPT_DIR, "draft", "audit-batch.md")

        lines = _build_header_lines(len(words))

        conn2 = get_db()
        for w in words:
            lines.append(_generate_word_section(conn2, w))
        conn2.close()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Exported {len(words)} words to {output_path}")

    return True