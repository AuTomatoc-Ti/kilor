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
    vi.restoreAllMocks();
  });

  afterEach(() => {
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
      makeEntry(2, 'testiba', 'banana'),
      makeEntry(3, 'testica', 'cherry'),
      makeEntry(4, 'testida', 'date'),
      makeEntry(5, 'testiea', 'elderberry'),
    ];
    await initWithEntries(oldEntries);
    expect(getMeta().total).toBe(5);
    expect(queryWords({}).totalCount).toBe(5);

    const newEntries = [
      makeEntry(10, 'novora', 'new meaning', { consensus_prefix: 'i-' }),
      makeEntry(11, 'anotera', 'another meaning', { consensus_prefix: 'a-' }),
      makeEntry(12, 'tira', 'third meaning'),
    ];
    const newDB = await buildTestDB(newEntries);
    const newBuf = dbToArrayBuffer(newDB);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(newBuf),
    });

    const count = await reloadDatabase();
    expect(count).toBe(3);
    expect(getMeta().total).toBe(3);

    const results = queryWords({});
    expect(results.totalCount).toBe(3);
    expect(results.rows.map(r => r.form).sort()).toEqual(['anotera', 'novora', 'tira']);

    const filtered = queryWords({ prefixes: ['i-'] });
    expect(filtered.totalCount).toBe(1);
    expect(filtered.rows[0].form).toBe('novora');
    expect(filtered.rows[0].consensus_prefix).toBe('i-');
  });

  // ─── 2. Double reload ───────────────────────────────────────────────────

  it('Scenario 2: Double reload — both reloads work independently', async () => {
    await initWithEntries([makeEntry(1, 'fira', 'first word')]);
    expect(getMeta().total).toBe(1);

    const midDB = await buildTestDB([makeEntry(20, 'midola', 'middle word')]);
    const finalDB = await buildTestDB([makeEntry(30, 'finala', 'final word')]);

    const midBuf = dbToArrayBuffer(midDB);
    const finalBuf = dbToArrayBuffer(finalDB);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(midBuf),
    });
    await reloadDatabase();
    expect(getMeta().total).toBe(1);
    expect(queryWords({}).rows[0].form).toBe('midola');

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(finalBuf),
    });
    await reloadDatabase();
    expect(getMeta().total).toBe(1);
    expect(queryWords({}).rows[0].form).toBe('finala');
  });

  // ─── 3. Empty DB ────────────────────────────────────────────────────────

  it('Scenario 3: Empty DB — reloadDatabase() returns 0, queries return empty', async () => {
    await initWithEntries([makeEntry(1, 'hasada', 'has data')]);
    expect(getMeta().total).toBe(1);

    const emptyDB = await buildTestDB([]);
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(emptyDB)),
    });

    const count = await reloadDatabase();
    expect(count).toBe(0);
    expect(getMeta().total).toBe(0);
    const result = queryWords({});
    expect(result.rows).toEqual([]);
    expect(result.totalCount).toBe(0);
    expect(queryWords({ search: 'anything' }).totalCount).toBe(0);
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

    expect(getDB()).toBe(oldDB);
    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    const results = queryWords({});
    expect(results.totalCount).toBe(1);
    expect(results.rows[0].form).toBe('safe');
    expect(results.rows[0].consensus_prefix).toBe('a-');
  });

  // ─── 5. Corrupt binary ──────────────────────────────────────────────────

  it('Scenario 5: Corrupt binary — reloadDatabase() throws, old state preserved', async () => {
    await initWithEntries([makeEntry(1, 'safe', 'safe word')]);
    expect(getMeta().total).toBe(1);

    const corrupt = new Uint8Array([0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x01, 0x02, 0x03]);
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(corrupt.buffer),
    });

    await expect(reloadDatabase()).rejects.toThrow();

    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    expect(queryWords({}).rows[0].form).toBe('safe');
  });

  // ─── 6. Network rejection (fetch throws, not HTTP error) ────────────────

  it('Scenario 6: Network failure — fetch() rejects, old state preserved', async () => {
    await initWithEntries([makeEntry(1, 'netora', 'network safe')]);
    expect(getMeta().total).toBe(1);

    global.fetch = vi.fn().mockRejectedValue(new Error('Network timeout'));

    await expect(reloadDatabase()).rejects.toThrow('Network timeout');

    expect(isDatabaseLoaded()).toBe(true);
    expect(getMeta().total).toBe(1);
    expect(queryWords({}).rows[0].form).toBe('netora');
  });

  // ─── 7. Rapid sequential reloads (concurrency stress) ───────────────────

  it('Scenario 7: Three rapid reloads — all resolve, last one wins coherently', async () => {
    await initWithEntries([makeEntry(1, 'inila', 'initial word')]);

    const db1 = await buildTestDB([makeEntry(100, 'dibona', 'DB1 word')]);
    const db2 = await buildTestDB([makeEntry(200, 'dibita', 'DB2 word')]);
    const db3 = await buildTestDB([
      makeEntry(300, 'terealfa', 'DB3 word A'),
      makeEntry(301, 'terebeta', 'DB3 word B'),
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

    const [r1, r2, r3] = await Promise.all([
      reloadDatabase(),
      reloadDatabase(),
      reloadDatabase(),
    ]);

    expect(r1).toBeGreaterThanOrEqual(1);
    expect(r2).toBeGreaterThanOrEqual(1);
    expect(r3).toBeGreaterThanOrEqual(1);

    expect(isDatabaseLoaded()).toBe(true);
    const results = queryWords({});
    expect(results.totalCount).toBeGreaterThanOrEqual(1);

    for (const r of results.rows) {
      expect(r.form).toBeTruthy();
      expect(r.meanings.length).toBeGreaterThan(0);
    }
  });

  // ─── 8. Query with filters after reload ─────────────────────────────────

  it('Scenario 8: Filtered queries work after reload', async () => {
    await initWithEntries([makeEntry(1, 'oloda', 'old word')]);

    const newDB = await buildTestDB([
      makeEntry(10, 'afis', 'fish', { consensus_prefix: 'a-' }),
      makeEntry(11, 'iwota', 'water', { consensus_prefix: 'i-' }),
      makeEntry(12, 'yroka', 'rock', { consensus_prefix: 'y-' }),
      makeEntry(13, 'nulora', 'no prefix', { consensus_prefix: '' }),
    ]);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(newDB)),
    });

    await reloadDatabase();

    // Filter by prefix
    expect(queryWords({ prefixes: ['a-'] }).totalCount).toBe(1);
    expect(queryWords({ prefixes: ['a-'] }).rows[0].form).toBe('afis');

    // Filter by NONE prefix
    expect(queryWords({ prefixes: ['NONE'] }).totalCount).toBe(1);
    expect(queryWords({ prefixes: ['NONE'] }).rows[0].form).toBe('nulora');

    // Combined filters
    const combined = queryWords({ prefixes: ['i-'] });
    expect(combined.totalCount).toBe(1);
    expect(combined.rows[0].form).toBe('iwota');

    // Search filter
    const searched = queryWords({ search: 'water' });
    expect(searched.totalCount).toBe(1);
    expect(searched.rows[0].form).toBe('iwota');
  });

  // ─── 9. Integration — reload from actual project DB artifact ────────────

  it('Scenario 9: Integration — reload from actual kilor.db artifact', async () => {
    const realEntries = [
      makeEntry(1, 'fora', 'fire', { consensus_prefix: 'a-', derivation_mask: 'NVAD' }),
      makeEntry(2, 'lira', 'water', { consensus_prefix: 'i-', derivation_mask: 'N' }),
      makeEntry(3, 'lunla', 'tree', { consensus_prefix: 'u-', derivation_mask: 'N' }),
      makeEntry(4, 'tlow', 'time', { consensus_prefix: 'o-', derivation_mask: 'NA' }),
    ];
    const realDB = await buildTestDB(realEntries);

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      arrayBuffer: () => Promise.resolve(dbToArrayBuffer(realDB)),
    });

    await initWithEntries([makeEntry(1, 'dumila', 'placeholder')]);
    await reloadDatabase();

    expect(getMeta().total).toBe(4);

    // Verify each ontology domain is represented
    const all = queryWords({}).rows;
    const prefixes = all.map(r => r.consensus_prefix).sort();
    expect(prefixes).toContain('a-');
    expect(prefixes).toContain('i-');
    expect(prefixes).toContain('u-');
    expect(prefixes).toContain('o-');

    // Verify enrichment (inflections, case forms) — meanings are now objects
    const fora = all.find(r => r.form === 'fora');
    expect(fora).toBeTruthy();
    expect(fora.meanings.map(m => m.gloss)).toContain('fire');
    expect(fora.consensus_prefix).toBe('a-');
  });
});