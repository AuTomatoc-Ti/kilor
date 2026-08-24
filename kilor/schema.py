"""Database schema constants — single source of truth for table structure."""

# ── Core Schema ──────────────────────────────────────────────────────────

# ── Compound Pattern Auto-Computation ─────────────────────────────────────
# SSOT: rules/3-subsystems/derivational-suffixes.md §I + compounding.md §I.
# When adding a new suffix or compounding head, update BOTH this dict
# and the corresponding spec file.
# Key = full-root form of the head (as stored in compound_components).
# Value = canonical pattern name stored in compound_meta.pattern.
COMPOUND_PATTERN_MAP = {
    # ── Derivational suffixes (derivational-suffixes.md §I) ──
    "maeha": "agent",
    "tek": "instrument",
    "lu": "property",
    "rin": "measure",
    "par": "process",
    "lise": "ordained-occurrence",
    "rius": "similative",
    "meus": "relational",
    "nia": "abundative",
    "rum": "Prospective",
    # ── Compounding heads (compounding.md §I) ──
    "poska": "location",
    "param": "result",
    "isra": "doctrine",
    "lokisra": "doctrine",
    "afaloi": "capability",
    "narau": "without",
    "naras": "without",
    "posia": "realm",
    "lote": "collective",
}


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form TEXT NOT NULL UNIQUE,
    syl_count INTEGER NOT NULL,
    is_root BOOLEAN DEFAULT 0,
    is_compound BOOLEAN DEFAULT 0,
    compound_type TEXT,                -- 'mono' or 'multi'; NULL for roots
    derivation_mask TEXT,              -- DEPRECATED (superseded by pos_mask)
    pos_mask TEXT DEFAULT '',          -- POS aggregate for inflection generation (e.g. 'NV', 'AD', '' = grammar)
    section TEXT NOT NULL,             -- 1-8
    consensus_prefix TEXT,
    search_text TEXT DEFAULT '',
    is_function_word BOOLEAN DEFAULT 0,
    notes TEXT,
    ipa TEXT DEFAULT '',               -- auto-computed IPA transcription
    syllables TEXT DEFAULT '',         -- auto-computed syllable division (e.g. "ta.ma.e")
    status TEXT DEFAULT 'active' CHECK(status IN ('draft','active','deprecated','superseded')),
    superseded_by INTEGER REFERENCES words(id),
    source_wordlist TEXT DEFAULT '',   -- e.g. 'phase1-core300'
    source_line INTEGER DEFAULT 0,     -- line number in source wordlist
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS inflections (
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    form_type TEXT NOT NULL,           -- 'noun', 'verb', 'adjective', 'adverb'
    form TEXT NOT NULL,
    PRIMARY KEY (word_id, form_type)
);

CREATE TABLE IF NOT EXISTS meanings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    gloss TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    sort_order INTEGER DEFAULT 0,
    pos TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS compound_components (
    compound_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    component_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    PRIMARY KEY (compound_id, position)
);

CREATE TABLE IF NOT EXISTS compound_meta (
    compound_id INTEGER PRIMARY KEY REFERENCES words(id) ON DELETE CASCADE,
    pattern TEXT NOT NULL,
    rule_ref TEXT
);

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER REFERENCES words(id) ON DELETE CASCADE,
    kilor_text TEXT NOT NULL,
    english_text TEXT NOT NULL,
    source TEXT DEFAULT 'canonical'
);

CREATE INDEX IF NOT EXISTS idx_words_form ON words(form);
CREATE INDEX IF NOT EXISTS idx_words_derivation_mask ON words(derivation_mask);
CREATE INDEX IF NOT EXISTS idx_words_colour ON words(consensus_prefix);
CREATE INDEX IF NOT EXISTS idx_words_syl_count ON words(syl_count);
CREATE INDEX IF NOT EXISTS idx_meanings_word_id ON meanings(word_id);
CREATE INDEX IF NOT EXISTS idx_compound_components_component_id ON compound_components(component_id);
"""

# ── FTS5 Full-Text Search Schema ────────────────────────────────────────

FTS_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS words_fts USING fts5(
    form,
    gloss,
    kilor_examples,
    english_examples,
    content='',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS words_fts_insert AFTER INSERT ON words
BEGIN
    INSERT INTO words_fts(rowid, form, gloss, kilor_examples, english_examples)
    SELECT w.id, w.form,
           GROUP_CONCAT(m.gloss, ' | '),
           GROUP_CONCAT(e.kilor_text, ' | '),
           GROUP_CONCAT(e.english_text, ' | ')
    FROM words w
    LEFT JOIN meanings m ON w.id = m.word_id
    LEFT JOIN examples e ON w.id = e.word_id
    WHERE w.id = NEW.id
    GROUP BY w.id;
END;

CREATE TRIGGER IF NOT EXISTS words_fts_delete AFTER DELETE ON words
BEGIN
    INSERT INTO words_fts(words_fts, rowid, form, gloss, kilor_examples, english_examples)
    VALUES ('delete', OLD.id, OLD.form, '', '', '');
END;

CREATE TRIGGER IF NOT EXISTS words_fts_update AFTER UPDATE ON words
BEGIN
    INSERT INTO words_fts(words_fts, rowid, form, gloss, kilor_examples, english_examples)
    VALUES ('delete', OLD.id, OLD.form, '', '', '');
    INSERT INTO words_fts(rowid, form, gloss, kilor_examples, english_examples)
    SELECT w.id, w.form,
           GROUP_CONCAT(m.gloss, ' | '),
           GROUP_CONCAT(e.kilor_text, ' | '),
           GROUP_CONCAT(e.english_text, ' | ')
    FROM words w
    LEFT JOIN meanings m ON w.id = m.word_id
    LEFT JOIN examples e ON w.id = e.word_id
    WHERE w.id = NEW.id
    GROUP BY w.id;
END;
"""

# ── Category Labels ──────────────────────────────────────────────────────

DERIVATION_MASK_LABELS = {
    "N": "Noun",
    "V": "Verb",
    "A": "Adjective",
    "D": "Adverb",
    "NVA": "Noun / Verb / Adjective",
    "NA": "Noun / Adjective",
    "NV": "Noun / Verb",
    "NAD": "Noun / Adjective / Adverb",
    "NVAD": "Noun / Verb / Adjective / Adverb",
    "VAD": "Verb / Adjective / Adverb",
    "AD": "Adjective / Adverb",
    "": "Closed-class",
}

# ── Valid POS tags (application-layer validation; no DB CHECK constraint for future flexibility) ──

VALID_POS = frozenset({
    "N", "V", "A", "D",          # open-class content (derivation_mask letters)
    "PRON", "NUM",                # closed-class content-like (pronouns, numerals)
    "DET",                         # determiners / quantifiers (any, each, some, few, most, none)
    "CCONJ", "SCONJ",             # conjunctions (coordinating, subordinating)
    "ADP",                         # adpositions (te, sy, mer, ar, tilpe, na, spatial postpositions)
    "PART",                        # particles (negation, modal, interrogative, emotional)
    "MODAL", "DEM", "Q",          # modal verbs, demonstratives, question words
    "CLF", "INTERJ", "PROPN",     # classifiers, interjections, proper nouns (future/partial)
    "",                            # unset / legacy
})

POS_LABELS = {
    "N": "Noun",
    "V": "Verb",
    "A": "Adjective",
    "D": "Adverb",
    "PRON": "Pronoun",
    "NUM": "Numeral",
    "DET": "Determiner",
    "CCONJ": "Coordinating Conjunction",
    "SCONJ": "Subordinating Conjunction",
    "ADP": "Adposition",
    "PART": "Particle",
    "MODAL": "Modal Verb",
    "DEM": "Demonstrative",
    "Q": "Question Word",
    "CLF": "Classifier / Measure Word",
    "INTERJ": "Interjection",
    "PROPN": "Proper Noun",
    "": "Unset",
}

# ── POS → Inflection Mapping ─────────────────────────────────────────────

# POS tags that generate tonal inflections — maps to form_type in inflections table
POS_TO_INFLECTION = {
    "N":     "noun",
    "V":     "verb",
    "A":     "adjective",
    "D":     "adverb",
    "MODAL": "verb",      # modals surface in verb form
    "PROPN": "noun",      # proper names take noun form (for case suffixes)
}

# POS tags that are closed-class / grammar — produce NO inflections
CLOSED_CLASS_POS = {"PRON", "NUM", "DET", "CCONJ", "SCONJ", "ADP", "PART", "DEM", "Q", "CLF", "INTERJ"}

# Known case suffixes for search stripping
CASE_SUFFIXES = ["-ni", "-si", "-na", "-sa", "-va", "-ma", "-ke", "-to", "-las"]

# ── POS Mask Computation ─────────────────────────────────────────────────

def compute_pos_mask(word_meanings):
    """Compute pos_mask from a word's aggregate meanings.

    Args:
        word_meanings: list of dicts with 'pos' key, or list of POS strings.

    Returns:
        str: e.g. 'NV', 'AD', 'NAVD', or '' for grammar particles.

    Rules:
        - N, V, A, D → mapped directly
        - MODAL → V (modals surface in verb form)
        - PROPN → N (proper names take noun form)
        - Closed-class POS tags (PRON, NUM, PART, DET, etc.) → contribute nothing
        - A and D are independent (no forced co-occurrence)
        - Empty string if all POS tags are closed-class or no meanings exist
    """
    if not word_meanings:
        return ""

    # Collect POS tags
    pos_tags = set()
    for m in word_meanings:
        pos = m.get("pos", "") if isinstance(m, dict) else str(m)
        if pos:
            pos_tags.add(pos)

    if not pos_tags:
        return ""

    # Map to NVAD letters
    mapped = set()
    for tag in sorted(pos_tags):
        if tag in ("N", "V", "A", "D"):
            mapped.add(tag)
        elif tag == "MODAL":
            mapped.add("V")
        elif tag == "PROPN":
            mapped.add("N")
        # Closed-class tags → contribute nothing

    if not mapped:
        return ""

    # Sort: N → V → A → D
    order = {"N": 0, "V": 1, "A": 2, "D": 3}
    return "".join(sorted(mapped, key=lambda x: order.get(x, 99)))

# ── Inflection Form Generation ────────────────────────────────────────────

def generate_inflection_forms(root, form_type, syl_count):
    """Generate the surface form for a given inflection type.

    Args:
        root: bare word form (e.g. 'fora')
        form_type: 'noun' | 'verb' | 'adjective' | 'adverb'
        syl_count: integer syllable count

    Returns:
        str surface form.

    Rules:
        - 1-2 syllable: N/V = bare root, A/D = root + 's'
        - 3+ syllable: tone markers applied (handled by JS/computeInflections)
        - Python-side: we store the forms that are computable without tone marking
          (the JS-side computeInflections handles tonal variants)
    """
    is_toneless = syl_count <= 2
    if is_toneless:
        if form_type in ("noun", "verb"):
            return root
        else:
            return root + "s"
    else:
        # For 3+ syllable words, store bare/toneless as the DB form.
        # Tonal variants are computed client-side by computeInflections() in db.js.
        if form_type in ("noun", "verb"):
            return root
        else:
            return root + "s"
