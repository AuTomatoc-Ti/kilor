"""Print lexicon statistics from the database."""

from ..db import get_db


def cmd_status():
    """Print lexicon statistics from the database."""
    conn = get_db()

    words = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
    meanings = conn.execute("SELECT COUNT(*) FROM meanings").fetchone()[0]

    cats = conn.execute(
        "SELECT derivation_mask, COUNT(*) as cnt FROM words GROUP BY derivation_mask ORDER BY cnt DESC"
    ).fetchall()

    syls = conn.execute(
        "SELECT syl_count, COUNT(*) as cnt FROM words GROUP BY syl_count ORDER BY syl_count"
    ).fetchall()

    print("=== Kilor Lexicon Status ===")
    print(f"Words: {words}")
    print(f"Meanings: {meanings}")
    print()

    print("-- By Derivation Mask --")
    for c in cats:
        label = c['derivation_mask'] or '(closed-class)'
        print(f"  {label}: {c['cnt']}")

    print()
    print("-- By Syllable Count --")
    for s in syls:
        print(f"  {s['syl_count']}-syl: {s['cnt']}")

    print()
    print("-- Roadmap Progress --")
    print(f"  {'Phase':30s} {'Words':>14s} {'Meanings':>14s}")
    print(f"  {'-'*30} {'-'*14} {'-'*14}")
    targets = [
        (1, 1000, 2000, "Phase 1 — Basic Daily"),
        (2, 2000, 4000, "Phase 2 — Elementary"),
        (3, 6000, 12000, "Phase 3 — Intermediate"),
        (4, 9000, 18000, "Phase 4 — Advanced"),
        (5, 12000, 24000, "Phase 5 — Proficient"),
        (6, 15000, 30000, "Phase 6 — Native / Literary"),
    ]
    for phase, word_target, meaning_target, label in targets:
        word_pct = words / word_target * 100
        meaning_pct = meanings / meaning_target * 100
        bar_w = '█' * min(int(word_pct / 5), 20) + '░' * max(20 - int(word_pct / 5), 0)
        bar_m = '█' * min(int(meaning_pct / 5), 20) + '░' * max(20 - int(meaning_pct / 5), 0)
        print(f"  {label:30s} {bar_w} {words:>4}/{word_target:>4} = {word_pct:.1f}%")
        print(f"  {'':30s} {bar_m} {meanings:>4}/{meaning_target:>4} = {meaning_pct:.1f}%")

    conn.close()