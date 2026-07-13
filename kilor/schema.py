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
    section TEXT NOT NULL,             -- A-J
    consensus_prefix TEXT,
    is_function_word BOOLEAN DEFAULT 0,
    notes TEXT,
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
    sort_order INTEGER DEFAULT 0
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
CREATE INDEX IF NOT EXISTS idx_words_section ON words(section);
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

# ── Section & Category Labels ────────────────────────────────────────────

SECTION_LABELS = {
    "A": "Worlds & Elements",
    "B": "Living Things",
    "C": "Physical Objects",
    "D": "Actions & Motion",
    "E": "Qualities & States",
    "F": "Mind & Emotion",
    "G": "Time & Space",
    "H": "Social & Relational",
    "I": "Abstract",
    "J": "Sensation",
}

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
