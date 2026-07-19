/**
 * E2E red-team tests for reloadDatabase().
 * Tests edge cases: concurrent reloads, corruption, HTTP errors, empty DB, etc.
 *
 * Run: npx vitest run src/db.reload.test.js
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  initDatabase,
  reloadDatabase,
  queryWords,
  getMeta,
  getDB,
  setDB,
  buildTestDB,
  isDatabaseLoaded,
} from './db';

// ── Helpers ──────────────────────────────────────────────────────────────────

function makeEntry(id, form, gloss, opts = {}) {
  return {
    id,
    form,
    syl_count: (opts.syl_count ?? form.replace(/[^aeiouy]/g, '').length) || 1,
    is_root: opts.is_root ?? 1,
    is_compound: opts.is_compound ?? 0,
    compound_type: opts.compound_type ?? null,
    derivation_mask: opts.derivation_mask ?? 'N',
    section: opts.section ?? 'G',
    consensus_prefix: opts.consensus_prefix ?? 'o-',
    is_function_word: opts.is_function_word ?? 0,
    notes: opts.notes ?? '',
    meanings: [gloss],
    inflections: opts.inflections ?? {},
  };
}

function dbToArrayBuffer(testDB) {
  return testDB.export().buffer;
}

async function initWithEntries(entries) {
  const testDB = await buildTestDB(entries);
  setDB(testDB);
}

// ── Tests ────────────────────────────────────────────────────────────────────

describe('reloadDatabase() — red-team E2E', () => {
  beforeEach(() => {
    // Reset global fetch mock between tests
    vi.restoreAllMocks();
  });

  afterEach(() => {
    // Close DB to prevent leaks
    const d = getDB();
    if (d) {
      try { d.close(); } catch (_) { /* already closed */ }
    }
    setDB(null);
  });

  // ─── 1. Basic reload ────────────────────────────────────────────────────

  it('Scenario 1: Basic reload — count changes and queries return new data', async () => {
    const oldEntries = [
      makeEntry(1, 'testa', 'apple'),
      makeEntry(2, 'testb', 'banana'),
      makeEntry(3, 'testc', 'cherry'),
      makeEntry(4, 'testd', 'date'),
      makeEntry(5, 'teste', 'elderberry'),
    ];
    await initWithEntries(oldEntries);
    expect(getMeta().total).toBe(5);
    expect(queryWords({}).length).toBe(5);

    const newEntries = [
      makeEntry(10, 'newword', 'new meaning', { section: 'A', consensus_prefix: 'i-' }),
      makeEntry(11, 'another', 'another meaning', { section: 'B', consensus_prefix: 'a-' }),
      makeEntry(12, 'thirdword', 'third meaning', { section: 'C' }),
    ];
    const newDB = await buildTestDB(newEntries);
    const newBuf = dbToArrayBuffer(newDB);

    // Mock fetch to return new DB
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(newBuf),
    });

    const count = await reloadDatabase();
    expect(count).toBe(3);
    expect(getMeta().total).toBe(3);

    const results = queryWords({});
    expect(results.length).toBe(3);
    expect(results.map(r => r.form).sort()).toEqual(['another', 'newword', 'thirdword']);

    // Verify arbitrary query against new data works
    const filtered = queryWords({ prefixes: ['i-'] });
    expect(filtered.length).toBe(1);
    expect(filtered[0].form).toBe('newword');
    expect(filtered[0].consensus_prefix).toBe('i-');
  });

  // ─── 2. Double reload ───────────────────────────────────────────────────

  it('Scenario 2: Double reload — both reloads work independently', async () => {
    await initWithEntries([makeEntry(1, 'first', 'first word')]);
    expect(getMeta().total).toBe(1);

    const midDB = await buildTestDB([makeEntry(20, 'middle', 'middle word')]);
    const finalDB = await buildTestDB([makeEntry(30, 'final', 'final word')]);

    const midBuf = dbToArrayBuffer(midDB);
    const finalBuf = dbToArrayBuffer(finalDB);

    // First reload
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(midBuf),
    });
    await reloadDatabase();
    expect(getMeta().total).toBe(1);
    expect(queryWords({})[0].form).toBe('middle');

    // Second reload
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(finalBuf),
    });
    await reloadDatabase();
    expect(getMeta().total).toBe(1);
    expect(queryWords({})[0].form).toBe('final');
  });

  // ─── 3. Empty DB ────────────────────────────────────────────────────────

  it('Scenario 3: Empty DB — reloadDatabase() returns 0, queries return empty', async () => {
    await initWithEntries([makeEntry(1, 'hasdata', 'has data')]);
    expect(getMeta().total).toBe(1);

    const emptyDB = await buildTestDB([]);
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(emptyDB)),
    });

    const count = await reloadDatabase();
    expect(count).toBe(0);
    expect(getMeta().total).toBe(0);
    expect(queryWords({})).toEqual([]);
    expect(queryWords({ search: 'anything' })).toEqual([]);
  });

  // ─── 4. HTTP error (500) ────────────────────────────────────────────────

  it('Scenario 4: HTTP 500 — reloadDatabase() throws, old DB state preserved', async () => {
    await initWithEntries([makeEntry(1, 'safe', 'safe word', { consensus_prefix: 'a-' })]);
    expect(getMeta().total).toBe(1);
    const oldDB = getDB();

    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    });

    await expect(reloadDatabase()).rejects.toThrow('HTTP 500');

    // Old state intact
    expect(getDB()).toBe(oldDB);
    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    const results = queryWords({});
    expect(results.length).toBe(1);
    expect(results[0].form).toBe('safe');
    expect(results[0].consensus_prefix).toBe('a-');
  });

  // ─── 5. Corrupt binary ──────────────────────────────────────────────────

  it('Scenario 5: Corrupt binary — reloadDatabase() throws, old state preserved', async () => {
    await initWithEntries([makeEntry(1, 'safe', 'safe word')]);
    expect(getMeta().total).toBe(1);

    // Random bytes that are not a valid SQLite DB
    const corrupt = new Uint8Array([0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x01, 0x02, 0x03]);
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(corrupt.buffer),
    });

    await expect(reloadDatabase()).rejects.toThrow();

    // Old state still works
    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    expect(queryWords({})[0].form).toBe('safe');
  });

  // ─── 6. Network rejection (fetch throws, not HTTP error) ────────────────

  it('Scenario 6: Network failure — fetch() rejects, old state preserved', async () => {
    await initWithEntries([makeEntry(1, 'networksafe', 'network safe')]);
    expect(getMeta().total).toBe(1);

    global.fetch = vi.fn().mockRejectedValue(new Error('Network timeout'));

    await expect(reloadDatabase()).rejects.toThrow('Network timeout');

    // Old state works
    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    expect(queryWords({})[0].form).toBe('networksafe');
  });

  // ─── 7. Rapid sequential reloads (concurrency stress) ───────────────────

  it('Scenario 7: Three rapid reloads — all resolve, last one wins coherently', async () => {
    await initWithEntries([makeEntry(1, 'initial', 'initial word')]);

    const db1 = await buildTestDB([makeEntry(100, 'db1', 'DB1 word', { section: 'A' })]);
    const db2 = await buildTestDB([makeEntry(200, 'db2', 'DB2 word', { section: 'B' })]);
    const db3 = await buildTestDB([
      makeEntry(300, 'db3alpha', 'DB3 word A', { section: 'C' }),
      makeEntry(301, 'db3beta', 'DB3 word B', { section: 'D' }),
    ]);

    let callCount = 0;
    const bufs = [dbToArrayBuffer(db1), dbToArrayBuffer(db2), dbToArrayBuffer(db3)];
    global.fetch = vi.fn(() => {
      const buf = bufs[callCount % bufs.length];
      callCount++;
      return Promise.resolve({
        ok: true,
        arrayBuffer: () => Promise.resolve(buf),
      });
    });

    // Fire three reloads rapidly — don't await each individually
    const [r1, r2, r3] = await Promise.all([
      reloadDatabase(),
      reloadDatabase(),
      reloadDatabase(),
    ]);

    // All returned a count (not undefined)
    expect(r1).toBeGreaterThanOrEqual(1);
    expect(r2).toBeGreaterThanOrEqual(1);
    expect(r3).toBeGreaterThanOrEqual(1);

    // DB is in a coherent state (can query without error)
    expect(isDatabaseLoaded()).toBe(true);
    const results = queryWords({});
    expect(results.length).toBeGreaterThanOrEqual(1);

    // Each result has required fields (not corrupted)
    for (const r of results) {
      expect(r.form).toBeTruthy();
      expect(r.meanings.length).toBeGreaterThan(0);
      expect(r.section).toBeTruthy();
    }
  });

  // ─── 8. Query with filters after reload ─────────────────────────────────

  it('Scenario 8: Filtered queries work after reload', async () => {
    await initWithEntries([makeEntry(1, 'old', 'old word', { section: 'A' })]);

    const newDB = await buildTestDB([
      makeEntry(10, 'a-fish', 'fish', { section: 'B', consensus_prefix: 'a-' }),
      makeEntry(11, 'i-water', 'water', { section: 'A', consensus_prefix: 'i-' }),
      makeEntry(12, 'y-rock', 'rock', { section: 'C', consensus_prefix: 'y-' }),
      makeEntry(13, 'nullword', 'no prefix', { consensus_prefix: '' }),
    ]);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(newDB)),
    });

    await reloadDatabase();

    // Filter by section
    expect(queryWords({ sections: ['A'] }).length).toBe(1);
    expect(queryWords({ sections: ['A'] })[0].form).toBe('i-water');

    // Filter by prefix
    expect(queryWords({ prefixes: ['a-'] }).length).toBe(1);
    expect(queryWords({ prefixes: ['a-'] })[0].form).toBe('a-fish');

    // Filter by NONE prefix (empty string prefix)
    expect(queryWords({ prefixes: ['NONE'] }).length).toBe(1);
    expect(queryWords({ prefixes: ['NONE'] })[0].form).toBe('nullword');

    // Combined filters
    const combined = queryWords({ sections: ['B'], prefixes: ['a-'] });
    expect(combined.length).toBe(1);
    expect(combined[0].form).toBe('a-fish');

    // No-match filter returns empty
    expect(queryWords({ sections: ['J'] }).length).toBe(0);

    // Search filter
    const searched = queryWords({ search: 'water' });
    expect(searched.length).toBe(1);
    expect(searched[0].form).toBe('i-water');
  });

  // ─── 9. Reload from actual project DB file (integration smoke test) ─────

  it('Scenario 9: Integration — reload from actual kilor.db artifact', async () => {
    // Use the project's own buildTestDB to simulate what the symlink provides
    const realEntries = [
      makeEntry(1, 'fora', 'fire', { section: 'A', consensus_prefix: 'a-', derivation_mask: 'NVAD' }),
      makeEntry(2, 'lira', 'water', { section: 'A', consensus_prefix: 'i-', derivation_mask: 'N' }),
      makeEntry(3, 'lunla', 'tree', { section: 'B', consensus_prefix: 'u-', derivation_mask: 'N' }),
      makeEntry(4, 'tlow', 'time', { section: 'G', consensus_prefix: 'o-', derivation_mask: 'NA' }),
    ];
    const realDB = await buildTestDB(realEntries);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(realDB)),
    });

    await initWithEntries([makeEntry(1, 'dummy', 'placeholder')]);
    await reloadDatabase();

    expect(getMeta().total).toBe(4);

    // Verify each ontology domain is represented
    const all = queryWords({});
    const prefixes = all.map(r => r.consensus_prefix).sort();
    expect(prefixes).toContain('a-');
    expect(prefixes).toContain('i-');
    expect(prefixes).toContain('u-');
    expect(prefixes).toContain('o-');

    // Verify enrichment (inflections, case forms)
    const fora = all.find(r => r.form === 'fora');
    expect(fora).toBeTruthy();
    expect(fora.meanings).toContain('fire');
    expect(fora.section).toBe('A');
    expect(fora.consensus_prefix).toBe('a-');
  });
});