"""Test that _word_to_dict includes the 'syllables' field correctly."""
import sqlite3
import pytest
import sys
sys.path.insert(0, '.')

from kilor.api import _word_to_dict, PREFIX_INFO
from kilor.phonology import split_syllables


@pytest.fixture
def conn():
    """Create an in-memory DB with a minimal word for testing."""
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY,
            form TEXT NOT NULL,
            syl_count INTEGER NOT NULL DEFAULT 0,
            is_root BOOLEAN DEFAULT 1,
            is_compound BOOLEAN DEFAULT 0,
            compound_type TEXT,
            derivation_mask TEXT,
            section TEXT DEFAULT 'I',
            consensus_prefix TEXT DEFAULT 'o-',
            is_function_word BOOLEAN DEFAULT 0,
            notes TEXT DEFAULT ''
        )
    """)
    db.execute("CREATE TABLE meanings (id INTEGER PRIMARY KEY, word_id INTEGER, gloss TEXT, language TEXT DEFAULT 'en', sort_order INTEGER DEFAULT 0)")
    db.execute("CREATE TABLE inflections (word_id INTEGER, form_type TEXT, form TEXT)")
    db.execute("CREATE TABLE compound_components (compound_id INTEGER, component_id INTEGER, position INTEGER)")
    db.execute("CREATE TABLE compound_meta (compound_id INTEGER, pattern TEXT, rule_ref TEXT)")
    db.execute("CREATE TABLE examples (id INTEGER PRIMARY KEY, word_id INTEGER, kilor_text TEXT, english_text TEXT, source TEXT DEFAULT 'canonical')")
    return db


def _insert_word(conn, wid, form, syl_count, **kwargs):
    defaults = {
        "is_root": 1, "is_compound": 0, "compound_type": None,
        "derivation_mask": "NVA", "section": "I", "consensus_prefix": "o-",
        "is_function_word": 0, "notes": "",
    }
    defaults.update(kwargs)
    conn.execute(
        """INSERT INTO words (id, form, syl_count, is_root, is_compound,
           compound_type, derivation_mask, section, consensus_prefix,
           is_function_word, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (wid, form, syl_count, defaults["is_root"], defaults["is_compound"],
         defaults["compound_type"], defaults["derivation_mask"], defaults["section"],
         defaults["consensus_prefix"], defaults["is_function_word"], defaults["notes"]),
    )


class TestWordToDictSyllables:
    def test_simple_cv_word(self, conn):
        _insert_word(conn, 1, "fora", 2)
        row = conn.execute("SELECT * FROM words WHERE id = 1").fetchone()
        result = _word_to_dict(conn, row)
        assert result["form"] == "fora"
        assert result["syl_count"] == 2
        assert result["syllables"] == "fo/ra"

    def test_single_syllable_word(self, conn):
        _insert_word(conn, 2, "song", 1)
        row = conn.execute("SELECT * FROM words WHERE id = 2").fetchone()
        result = _word_to_dict(conn, row)
        assert result["form"] == "song"
        assert result["syl_count"] == 1
        assert result["syllables"] == "song"

    def test_function_word(self, conn):
        _insert_word(conn, 3, "amer", 2, is_function_word=1, derivation_mask=None)
        row = conn.execute("SELECT * FROM words WHERE id = 3").fetchone()
        result = _word_to_dict(conn, row)
        assert result["is_function_word"] is True
        assert result["syl_count"] == 2
        assert result["syllables"] == "a/mer"

    def test_three_syllable_word(self, conn):
        _insert_word(conn, 4, "chorogor", 3)
        row = conn.execute("SELECT * FROM words WHERE id = 4").fetchone()
        result = _word_to_dict(conn, row)
        assert result["syl_count"] == 3
        assert result["syllables"] == "cho/ro/gor"

    def test_word_with_start_only_onset(self, conn):
        _insert_word(conn, 5, "klang", 1)
        row = conn.execute("SELECT * FROM words WHERE id = 5").fetchone()
        result = _word_to_dict(conn, row)
        assert result["syl_count"] == 1
        assert result["syllables"] == "klang"

    def test_matches_split_syllables(self, conn):
        """The syllables field must match split_syllables joined with /."""
        form = "chorogor"
        _insert_word(conn, 6, form, 3)
        row = conn.execute("SELECT * FROM words WHERE id = 6").fetchone()
        result = _word_to_dict(conn, row)
        expected = "/".join(split_syllables(form))
        assert result["syllables"] == expected