"""Chat Corpus — human-checkable, revisit-later Kilor example sentences.

Source of truth for humans: data/chat-corpus.md (one sentence per line,
    [[word]] markers for existence checks).
SQLite staging DB: data/chat-corpus.db  (mirrors the SSOT examples table so it
    can later be ported in; but stores free text, no FK — safe while words are
    still candidates).
Words that are not yet real SSOT words.form are reported as FLOATING so a
    human can see at a glance which sentences hinge on not-yet-final words.
"""

import os
import re
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MD_PATH = os.path.join(SCRIPT_DIR, "data", "chat-corpus.md")
DB_PATH = os.path.join(SCRIPT_DIR, "data", "chat-corpus.db")
SSOT_DB = os.path.join(SCRIPT_DIR, "data", "kilor.db")
DRAFT_VOCAB = os.path.join(SCRIPT_DIR, "draft", "draft-vocab.md")

# Bare sequence of [[word]] markers in a sentence.
WORD_MARK = re.compile(r"\[\[([^\]]+)\]\]")

# Colour prefixes appear with a connector in normal nouns (a-, ae-, etc.).
COLOUR_PREFIXES = [  # longest first so two-letter ae- wins over a-
    "ae-", "a-", "e-", "i-", "o-", "u-", "y-",
]

# Case suffixes (ACC/GEN) per contrast rule: ni/na/si/sa are appended to the
# root without a hyphen (e.g. kafeisa = kafei + sa). We strip the bare suffix.
CASE_SUFFIXES = ["ni", "na", "si", "sa"]


def _parse_md(path):
    """Return list of (kilor_with_markers, english)."""
    sentences = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n").rstrip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            kilor, english = line.split("=", 1)
            sentences.append((kilor.strip(), english.strip()))
    return sentences


def _words_in(kilor):
    """Extract the [[word]] markers."""
    return WORD_MARK.findall(kilor)


def _strip_markers(kilor):
    """Remove [[ ]] so the stored text is plain Kilor."""
    return WORD_MARK.sub(r"\1", kilor)


def _strip_colour_prefix(w):
    """Remove a leading foregrounded colour prefix (a- … ae-) if present."""
    for p in COLOUR_PREFIXES:
        if w.startswith(p):
            return w[len(p):]
    return w


def _strip_case_suffix(w):
    """Remove a trailing ACC/GEN case suffix if present (bare variants)."""
    for s in CASE_SUFFIXES:
        if w.endswith(s) and len(w) > len(s) + 1:
            return w[:-len(s)]
    return w


def _root_candidates(w):
    """Yield plausible lexicon forms for w, from most to least specific."""
    yield w                      # exact
    stripped = _strip_colour_prefix(w)
    if stripped != w:
        yield stripped           # colour prefix removed -> bare root
    for base in {w, stripped}:
        root = _strip_case_suffix(base)
        if root != base:
            yield root           # case suffix removed
        root2 = _strip_colour_prefix(root)
        if root2 != root:
            yield root2          # both removed


def _load_ssot_forms(path):
    conn = sqlite3.connect(path)
    try:
        rows = conn.execute("SELECT form FROM words").fetchall()
    finally:
        conn.close()
    return {r[0] for r in rows}


def _load_candidate_forms(path):
    """Candidate words: lines in draft-vocab.md before the divider patterns.

    Conservative: treat any 'word,' line in the candidate section as a form.
    """
    forms = set()
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return forms
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(".") or "..." in s:
            continue
        first = s.split(",", 1)[0].strip()
        if re.match(r"^[a-z][a-z ]*$", first, re.IGNORECASE) and first:
            forms.add(first)
    return forms
def _classify(w, ssot, cand):
    """Return (status, root) for word w using root restoration.

    status: 'ssot' | 'candidate' | 'floating'
    """
    for root in _root_candidates(w):
        if root in ssot:
            return "ssot", root
        if root in cand:
            return "candidate", root
    return "floating", w


def cmd_chat_corpus():
    sentences = _parse_md(MD_PATH)
    if not sentences:
        print("No sentences found (empty or unparsed).")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kilor_text TEXT NOT NULL,
            english_text TEXT NOT NULL,
            source TEXT DEFAULT 'chat'
        )
    """)
    conn.commit()

    # Idempotent refresh: clear then reload from source.
    conn.execute("DELETE FROM sentences")
    for kilor, english in sentences:
        conn.execute(
            "INSERT INTO sentences (kilor_text, english_text, source) VALUES (?,?,?)",
            (_strip_markers(kilor), english, "chat"),
        )
    conn.commit()
    conn.close()

    ssot = _load_ssot_forms(SSOT_DB)
    cand = _load_candidate_forms(DRAFT_VOCAB)

    print(f"Chat corpus synced: {len(sentences)} sentences -> {DB_PATH}")
    print()
    print("Word report (marked words checked against SSOT + candidates):")

    seen = set()
    n_floating = 0
    for kilor, _ in sentences:
        for w in _words_in(kilor):
            if w in seen:
                continue
            seen.add(w)
            status, root = _classify(w, ssot, cand)
            if status == "ssot":
                print(f"  [OK] '{w}' - in SSOT.")
            elif status == "candidate":
                print(f"  [CANDIDATE] '{w}' - root '{root}' in candidate vocab, "
                      f"not yet SSOT.")
            else:
                n_floating += 1
                print(f"  [FLOATING] '{w}' - not in SSOT, not in candidate vocab.")

    if n_floating == 0:
        print("  (no floating words)")
    else:
        print(f"\n{n_floating} referenced word(s) are floating. "
              f"Consider adding to draft-vocab.md or the pipeline.")
    return None