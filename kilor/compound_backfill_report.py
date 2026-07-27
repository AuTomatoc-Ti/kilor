"""Generate a report of existing compounds for manual review.
Outputs to draft/compound-backfill-report.md
"""
import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "kilor.db")
REPORT_PATH = os.path.join(SCRIPT_DIR, "draft", "compound-backfill-report.md")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "kilor.db")
REPORT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "draft", "compound-backfill-report.md")


def generate():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # All compound entries from compound_components
    compounds = conn.execute("""
        SELECT DISTINCT w.id, w.form, w.consensus_prefix, w.compound_type,
               w.is_compound, w.is_root,
               GROUP_CONCAT(m.gloss, '; ') as meanings
        FROM words w
        JOIN compound_components cc ON cc.compound_id = w.id
        LEFT JOIN meanings m ON m.word_id = w.id
        GROUP BY w.id
        ORDER BY w.form
    """).fetchall()

    # Get component details for each
    compound_details = []
    for c in compounds:
        components = conn.execute("""
            SELECT r.form as comp_form, cc.position
            FROM compound_components cc
            JOIN words r ON r.id = cc.component_id
            WHERE cc.compound_id = ?
            ORDER BY cc.position
        """, (c["id"],)).fetchall()
        component_list = [r["comp_form"] for r in components]
        comp_str = " + ".join(component_list)

        meta = conn.execute(
            "SELECT pattern, rule_ref FROM compound_meta WHERE compound_id = ?",
            (c["id"],)
        ).fetchone()

        compound_details.append({
            "id": c["id"],
            "form": c["form"],
            "prefix": c["consensus_prefix"] or "(null)",
            "compound_type": c["compound_type"] or "(null)",
            "meanings": c["meanings"] or "(no glosses)",
            "is_compound": c["is_compound"],
            "is_root": c["is_root"],
            "components": comp_str,
            "pattern": meta["pattern"] if meta else "(missing)",
            "rule_ref": meta["rule_ref"] if meta and meta["rule_ref"] else "(missing)",
            "issues": [],
        })

    # Flag issues
    for cd in compound_details:
        if cd["compound_type"] == "(null)":
            cd["issues"].append("compound_type is NULL — should be 'mono' or 'multi'")
        if cd["is_compound"] == 0:
            cd["issues"].append("is_compound=0 — stored as root")
        if cd["is_root"] == 1:
            cd["issues"].append("is_root=1 — stored as root")
        if cd["pattern"] == "(missing)":
            cd["issues"].append("missing compound_meta (no pattern/rule_ref)")
        if cd["prefix"] == "o-" and cd["compound_type"] != "(null)":
            cd["issues"].append("consensus_prefix='o-' — likely wrong, needs human review")

    # Also find words marked is_compound=0 but in compound_components (orphans)
    orphan_compounds = conn.execute("""
        SELECT w.id, w.form, w.is_compound, w.compound_type, w.is_root
        FROM words w
        WHERE w.id IN (SELECT compound_id FROM compound_components)
        AND w.is_compound = 0
        ORDER BY w.form
    """).fetchall()

    conn.close()

    # Generate report
    clean = sum(1 for cd in compound_details if not cd["issues"])
    flagged = sum(1 for cd in compound_details if cd["issues"])

    lines = []
    lines.append("# Compound Backfill Report — Manual Review")
    lines.append("")
    lines.append(f"**Generated:** 2026-07-27")
    lines.append(f"**Total compounds in database:** {len(compounds)}")
    lines.append(f"**Clean (no issues):** {clean}")
    lines.append(f"**Flagged for review:** {flagged}")
    if orphan_compounds:
        lines.append(f"**Orphan compounds (is_compound=0 but in compound_components):** {len(orphan_compounds)}")
    lines.append("")
    lines.append("## Review Instructions")
    lines.append("")
    lines.append("For each flagged entry below, verify:")
    lines.append("1. **Compound type** — should be 'mono' or 'multi'")
    lines.append("2. **Components** — are all component roots correct?")
    lines.append("3. **Pattern + Rule Ref** — should be filled in from `rules/3-subsystems/derivational-compounding.md`")
    lines.append("4. **Consensus Prefix** — all flagged entries have 'o-', which was the hardcoded default")
    lines.append("")
    lines.append("After review, use `python kilor.py edit <form> --set-prefix ...` or direct SQL to fix.")
    lines.append("")
    lines.append("---")
    lines.append("")

    if flagged > 0:
        lines.append("## Flagged Compounds")
        lines.append("")
        for cd in compound_details:
            if not cd["issues"]:
                continue
            lines.append(f"### {cd['form']}")
            lines.append(f"- **ID:** {cd['id']}")
            lines.append(f"- **Meaning:** {cd['meanings']}")
            lines.append(f"- **Components:** {cd['components']}")
            lines.append(f"- **Prefix:** {cd['prefix']}")
            lines.append(f"- **Type:** {cd['compound_type']}")
            lines.append(f"- **Pattern:** {cd['pattern']}")
            lines.append(f"- **Rule Ref:** {cd['rule_ref']}")
            lines.append(f"- **is_compound:** {cd['is_compound']} | **is_root:** {cd['is_root']}")
            lines.append(f"- **Issues:** {', '.join(cd['issues'])}")
            lines.append("")

    if clean > 0:
        lines.append("## Clean Compounds (Reference Only)")
        lines.append("")
        lines.append("| Form | Type | Components | Pattern | Prefix |")
        lines.append("|---|---|---|---|---|")
        for cd in compound_details:
            if cd["issues"]:
                continue
            lines.append(f"| {cd['form']} | {cd['compound_type']} | {cd['components']} | {cd['pattern']} | {cd['prefix']} |")
        lines.append("")

    if orphan_compounds:
        lines.append("## Orphan Compounds (is_compound=0)")
        lines.append("")
        lines.append("These entries have compound_components rows but is_compound=0 in words table:")
        lines.append("")
        lines.append("| ID | Form | is_compound | compound_type |")
        lines.append("|---|---|---|---|")
        for oc in orphan_compounds:
            lines.append(f"| {oc['id']} | {oc['form']} | {oc['is_compound']} | {oc['compound_type'] or '(null)'} |")
        lines.append("")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report written to {REPORT_PATH}")
    print(f"Total compounds: {len(compounds)} | Clean: {clean} | Flagged: {flagged}")
    if orphan_compounds:
        print(f"Orphans: {len(orphan_compounds)}")


if __name__ == "__main__":
    generate()