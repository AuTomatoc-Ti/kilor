"""TDD tests for updated_at timestamp integrity.

These tests verify that:
1. INSERT auto-populates created_at and updated_at
2. UPDATE without explicit updated_at preserves the old timestamp
3. populate_search_text() does NOT change any word's updated_at
4. Explicit UPDATE with updated_at works correctly
5. No trigger recursion on any UPDATE

The tests run against a copy of data/kilor.db so the real database is untouched.
"""

import os
import shutil
import sqlite3
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SCRIPT_DIR)

from kilor.db import populate_search_text


TEST_DB = os.path.join(SCRIPT_DIR, "data", "_test_updated_at_temp.db")
REAL_DB = os.path.join(SCRIPT_DIR, "data", "kilor.db")


def setUpModule():
    """Copy real DB to test DB once before all tests."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    shutil.copy2(REAL_DB, TEST_DB)


def tearDownModule():
    """Remove test DB after all tests."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def _connect():
    """Connect to test DB with foreign keys on."""
    conn = sqlite3.connect(TEST_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


class TestInsertTimestamp(unittest.TestCase):
    """INSERT auto-populates created_at and updated_at via DEFAULT."""

    def test_insert_root_gets_timestamps(self):
        conn = _connect()
        try:
            conn.execute("""
                INSERT INTO words (form, syl_count, is_root, section, consensus_prefix)
                VALUES ('testform', 2, 1, '1', 'o-')
            """)
            conn.commit()
            row = conn.execute("SELECT created_at, updated_at FROM words WHERE form = 'testform'").fetchone()
            self.assertIsNotNone(row["created_at"])
            self.assertIsNotNone(row["updated_at"])
            self.assertEqual(row["created_at"], row["updated_at"])
        finally:
            conn.execute("DELETE FROM words WHERE form = 'testform'")
            conn.commit()
            conn.close()


class TestUpdatePreservesTimestamp(unittest.TestCase):
    """UPDATE without explicit updated_at must preserve the old value."""

    def setUp(self):
        conn = _connect()
        conn.execute("""
            INSERT INTO words (form, syl_count, is_root, section, consensus_prefix)
            VALUES ('preservetest', 2, 1, '1', 'o-')
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = _connect()
        conn.execute("DELETE FROM words WHERE form = 'preservetest'")
        conn.commit()
        conn.close()

    def test_search_text_update_preserves_updated_at(self):
        conn = _connect()
        # Get original timestamp
        row = conn.execute("SELECT updated_at FROM words WHERE form = 'preservetest'").fetchone()
        original_ts = row["updated_at"]
        self.assertIsNotNone(original_ts)

        # Do an infrastructure UPDATE without setting updated_at
        conn.execute("UPDATE words SET search_text = 'test' WHERE form = 'preservetest'")
        conn.commit()

        row = conn.execute("SELECT updated_at FROM words WHERE form = 'preservetest'").fetchone()
        self.assertEqual(row["updated_at"], original_ts,
                         "updated_at must NOT change on infrastructure UPDATE")
        conn.close()


class TestExplicitUpdateTimestamp(unittest.TestCase):
    """Explicit updated_at = datetime('now') must work."""

    def setUp(self):
        conn = _connect()
        conn.execute("""
            INSERT INTO words (form, syl_count, is_root, section, consensus_prefix)
            VALUES ('explicittest', 2, 1, '1', 'o-')
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = _connect()
        conn.execute("DELETE FROM words WHERE form = 'explicittest'")
        conn.commit()
        conn.close()

    def test_explicit_update_bumps_timestamp(self):
        conn = _connect()
        row = conn.execute("SELECT updated_at FROM words WHERE form = 'explicittest'").fetchone()
        original_ts = row["updated_at"]

        # Use datetime arithmetic to guarantee a different timestamp
        conn.execute(
            "UPDATE words SET form = 'explicittest', notes = 'changed', updated_at = datetime('now', '+1 seconds') WHERE form = 'explicittest'"
        )
        conn.commit()

        row = conn.execute("SELECT updated_at FROM words WHERE form = 'explicittest'").fetchone()
        self.assertNotEqual(row["updated_at"], original_ts,
                            "Explicit updated_at must change the timestamp")
        conn.close()


class TestPopulateSearchTextPreservesTimestamps(unittest.TestCase):
    """populate_search_text() is infrastructure — it must NOT change any updated_at."""

    def test_populate_search_text_preserves_all_timestamps(self):
        conn = _connect()

        # Snapshot all updated_at values before
        before = {
            row["id"]: row["updated_at"]
            for row in conn.execute("SELECT id, updated_at FROM words").fetchall()
        }
        self.assertGreater(len(before), 0, "DB must have at least one word to test")

        # Run populate_search_text
        populate_search_text(conn)

        # Snapshot after — using same connection
        after = {
            row["id"]: row["updated_at"]
            for row in conn.execute("SELECT id, updated_at FROM words").fetchall()
        }

        changed = []
        for wid, ts_before in before.items():
            ts_after = after.get(wid)
            if ts_before != ts_after:
                form = conn.execute("SELECT form FROM words WHERE id = ?", (wid,)).fetchone()
                changed.append(f"  id={wid} ({form['form'] if form else '?'}): {ts_before} → {ts_after}")

        self.assertEqual(len(changed), 0,
                         f"populate_search_text() changed {len(changed)} updated_at values:\n" + "\n".join(changed))
        conn.close()


class TestNoTriggerRecursion(unittest.TestCase):
    """Any UPDATE on words must not cause trigger recursion errors."""

    def test_bulk_update_no_recursion(self):
        conn = _connect()
        try:
            # Update search_text on all words — must not hang or raise recursion error
            conn.execute("UPDATE words SET search_text = search_text || ''")
            conn.commit()
        except sqlite3.OperationalError as e:
            self.fail(f"Bulk UPDATE caused recursion/operational error: {e}")
        finally:
            conn.close()

    def test_single_row_update_no_recursion(self):
        conn = _connect()
        try:
            row = conn.execute("SELECT id FROM words LIMIT 1").fetchone()
            if row:
                conn.execute("UPDATE words SET search_text = search_text WHERE id = ?", (row["id"],))
                conn.commit()
        except sqlite3.OperationalError as e:
            self.fail(f"Single-row UPDATE caused recursion/operational error: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()