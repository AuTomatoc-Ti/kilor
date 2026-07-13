"""Print lexicon statistics from the database."""

from ..db import get_db
from ..schema import SECTION_LABELS


def cmd_status():
    """Print lexicon statistics from the database."""
    conn = get_db()

    roots = conn.execute(
        "SELECT COUNT(*) FROM words WHERE is_root = 1 AND is_function_word = 0"
    ).fetchone()[0]
    func = conn.execute("SELECT COUNT(*) FROM words WHERE is_function_word = 1").fetchone()[0]
    compounds = conn.execute("SELECT COUNT(*) FROM words WHERE is_compound = 1").fetchone()[0]
    mono = conn.execute("SELECT COUNT(*) FROM words WHERE compound_type = 'mono'").fetchone()[0]
    multi = conn.execute("SELECT COUNT(*) FROM words WHERE compound_type = 'multi'").fetchone()[0]

    # Derived words: count only forms allowed by the derivation_mask
    # N=1, NA=2, NV=2, AD=2, VAD=3, NAD=3, NVA=3, NVAD=4, D=1
    # Function words always count as 1 (no derivations)
    derived = conn.execute(
        """SELECT SUM(
               CASE w.derivation_mask
                   WHEN 'N' THEN 1 WHEN 'NA' THEN 2 WHEN 'NV' THEN 2
                   WHEN 'AD' THEN 2 WHEN 'VAD' THEN 3 WHEN 'NAD' THEN 3
                   WHEN 'NVA' THEN 3 WHEN 'NVAD' THEN 4 WHEN 'D' THEN 1
                   ELSE 0
               END
           ) FROM words w
           WHERE w.is_root = 1 AND w.is_function_word = 0"""
    ).fetchone()[0] or 0

    # Surface words from inflections = content-root-only inflections
    # (migrate.py no longer creates inflections for function words)
    derived_inflection_rows = conn.execute(
        """SELECT COUNT(*) FROM inflections"""
    ).fetchone()[0]

    # Total surface words = mask-derived forms + compounds + function words
    total_words = derived + compounds + func

    cats = conn.execute(
        "SELECT derivation_mask, COUNT(*) as cnt FROM words GROUP BY derivation_mask ORDER BY cnt DESC"
    ).fetchall()

    secs = conn.execute(
        "SELECT section, COUNT(*) as cnt FROM words WHERE section != '' GROUP BY section ORDER BY section"
    ).fetchall()

    syls = conn.execute(
        "SELECT syl_count, COUNT(*) as cnt FROM words GROUP BY syl_count ORDER BY syl_count"
    ).fetchall()

    print("=== Kilor Lexicon Status ===")
    print(f"Content roots: {roots}")
    print(f"Function words: {func}")
    print(f"Compounds (mono): {mono}")
    print(f"Compounds (multi): {multi}")
    print(f"Derived surface forms: {derived}")
    print(f"Total surface words: {total_words}")
    print()

    print("-- By Derivation Mask --")
    for c in cats:
        label = c['derivation_mask'] or '(closed-class)'
        print(f"  {label}: {c['cnt']}")

    print()
    print("-- By Section --")
    for s in secs:
        name = SECTION_LABELS.get(s['section'], 'Unknown')
        print(f"  {s['section']} ({name}): {s['cnt']}")

    print()
    print("-- By Syllable Count --")
    for s in syls:
        print(f"  {s['syl_count']}-syl: {s['cnt']}")

    content_total = roots
    print()
    print("-- Roadmap Progress --")
    print(f"  {'Phase':30s} {'Roots':>14s} {'Words':>14s}")
    print(f"  {'-'*30} {'-'*14} {'-'*14}")
    targets = [
        (1, 500, 1750, "Phase 1 — Basic Daily"),
        (2, 1000, 3500, "Phase 2 — Elementary"),
        (3, 3000, 10500, "Phase 3 — Intermediate"),
        (4, 4500, 15750, "Phase 4 — Advanced"),
        (5, 6000, 21000, "Phase 5 — Proficient"),
        (6, 8600, 30100, "Phase 6 — Near-Native / Literary"),
    ]
    for phase, root_target, word_target, label in targets:
        root_pct = content_total / root_target * 100
        word_pct = total_words / word_target * 100
        bar_r = '█' * min(int(root_pct / 5), 20) + '░' * max(20 - int(root_pct / 5), 0)
        bar_w = '█' * min(int(word_pct / 5), 20) + '░' * max(20 - int(word_pct / 5), 0)
        print(f"  {label:30s} {bar_r} {content_total:>4}/{root_target:>4} = {root_pct:.1f}%")
        print(f"  {'':30s} {bar_w} {total_words:>4}/{word_target:>4} = {word_pct:.1f}%")

    conn.close()
