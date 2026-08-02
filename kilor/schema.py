"""Database schema constants — single source of truth for table structure."""

# ── Core Schema ──────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form TEXT NOT NULL UNIQUE,
    syl_count INTEGER NOT NULL,
    is_root BOOLEAN DEFAULT 0,
    is_compound BOOLEAN DEFAULT 0,
    compound_type TEXT,                -- 'mono' or 'multi'; NULL for roots
    derivation_mask TEXT,              -- NVAD mask (N=noun, V=verb, A=adjective, D=adverb); empty for closed-class
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
