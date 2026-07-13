"""Generate today's translation template."""

import os
from datetime import datetime

from ..db import get_db

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORDLIST_DIR = os.path.join(SCRIPT_DIR, "wordlist")


def cmd_next(count=20):
    """Generate today's translation template."""
    conn = get_db()
    existing_meanings = set()

    for row in conn.execute("SELECT gloss FROM meanings WHERE language = 'en'").fetchall():
        existing_meanings.add(row["gloss"].strip().lower())

    conn.close()

    words_to_translate = []
    wordlist_files = sorted(os.listdir(WORDLIST_DIR)) if os.path.exists(WORDLIST_DIR) else []

    for wl_file in wordlist_files:
        if not wl_file.endswith(".txt"):
            continue
        path = os.path.join(WORDLIST_DIR, wl_file)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 1:
                    english = parts[0].strip()
                    category = parts[1].strip() if len(parts) >= 2 else "general"
                    if english.lower() not in existing_meanings:
                        words_to_translate.append((english, category))

    if not words_to_translate:
        print("All words in wordlists have been translated! Add more wordlist files or create new ones.")
        return

    batch = words_to_translate[:count]

    today_header = f"""# Kilor Translation — {datetime.now().strftime('%Y-%m-%d')}
# Fill in the Kilor column. Leave 'Decision' blank — the add command will classify.
# Decision options (auto-detected if blank): root / compound / derivation
# Constraints reminder: no j/v in bare roots; 1-2 syl roots cannot end in s

## Existing Roots for Reference

"""
    output = [today_header]

    for english, category in batch:
        output.append(f"""---
### {english} ({category})

| Field | Value |
|---|---|
| Kilor Root |  |
| Syllable Count |  |
| Category (n/v/a/av/nv/na) |  |
| Section (A-J) |  |
| Decision (root/compound/derivation) |  |
| Notes |  |

""")

    output.append(
        f"---\n\n*{len(batch)} words to translate. Run: python kilor.py add --file today.md when done.*"
    )

    today_path = os.path.join(SCRIPT_DIR, "today.md")
    with open(today_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"Generated today.md with {len(batch)} words to translate.")
    print(f"Words remaining in queue: {len(words_to_translate) - len(batch)}")