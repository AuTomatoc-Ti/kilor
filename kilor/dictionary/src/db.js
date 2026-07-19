/**
 * SQLite database layer for the Kilor Dictionary.
 * Uses sql.js (SQLite compiled to WebAssembly) to read kilor.db directly.
 */

import initSqlJs from 'sql.js';

let db = null;

function isNode() {
  return typeof process !== 'undefined' && process.versions && process.versions.node;
}

function b64toBuf(b64) {
  const bin = atob(b64);
  const buf = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  return buf;
}

export async function initDatabase() {
  if (db) return;

  if (isNode()) {
    const SQL = await initSqlJs();
    const { readFile } = await import('node:fs/promises');
    const { resolve, dirname } = await import('node:path');
    const { fileURLToPath } = await import('node:url');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const dbPath = resolve(__dirname, '..', '..', '..', 'data', 'kilor.db');
    const buf = await readFile(dbPath);
    db = new SQL.Database(new Uint8Array(buf));
    return;
  }

  // Browser: prefer base64-inlined wasm + db for production (self-contained HTML)
  let SQL;
  const wasmB64 = typeof window !== 'undefined' && window.__SQL_WASM_B64__;
  if (wasmB64) {
    SQL = await initSqlJs({ wasmBinary: b64toBuf(wasmB64) });
  } else {
    SQL = await initSqlJs({ locateFile: (file) => `/${file}` });
  }

  const dbB64 = typeof window !== 'undefined' && window.__KILOR_DB_B64__;
  if (dbB64) {
    db = new SQL.Database(b64toBuf(dbB64));
    return;
  }

  // Fallback: fetch kilor.db via HTTP (dev mode, served from public/)
  const resp = await fetch('./kilor.db', { cache: 'no-store' });
  if (!resp.ok) {
    throw new Error(
      `Cannot load database: HTTP ${resp.status} fetching ./kilor.db. Run "python kilor.py export --format html" first.`
    );
  }
  const buf = await resp.arrayBuffer();
  db = new SQL.Database(new Uint8Array(buf));
}

function queryAll(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  const rows = [];
  while (stmt.step()) {
    const cols = stmt.getColumnNames();
    const vals = stmt.get();
    const obj = {};
    cols.forEach((c, i) => { obj[c] = vals[i]; });
    rows.push(obj);
  }
  stmt.free();
  return rows;
}

function queryValue(sql, params = []) {
  const rows = queryAll(sql, params);
  if (rows.length === 0) return null;
  return Object.values(rows[0])[0];
}

export function queryWords({
  search = '',
  section = '',
  filterType = '',
  filterMask = '',
  sortCol = 'form',
  sortDir = 'asc',
} = {}) {
  if (!db) return [];

  const cols = `w.id, w.form, w.syl_count, w.is_root, w.is_compound,
    w.compound_type, w.derivation_mask, w.section, w.consensus_prefix,
    w.is_function_word, w.notes,
    GROUP_CONCAT(m.gloss, ' | ') AS glosses_concat`;

  let sql = `SELECT ${cols} FROM words w LEFT JOIN meanings m ON w.id = m.word_id WHERE 1=1`;
  const params = [];

  if (section) { sql += ' AND w.section = ?'; params.push(section); }
  if (filterType === 'root') { sql += ' AND w.is_root = 1'; }
  else if (filterType === 'compound') { sql += ' AND w.is_compound = 1'; }
  else if (filterType === 'function') { sql += ' AND w.is_function_word = 1'; }
  if (filterMask === 'EMPTY') { sql += " AND (w.derivation_mask IS NULL OR w.derivation_mask = '')"; }
  else if (filterMask) { sql += ' AND w.derivation_mask = ?'; params.push(filterMask); }
  if (search) {
    sql += ' AND (LOWER(w.form) LIKE ? OR LOWER(m.gloss) LIKE ?)';
    const t = `%${search.toLowerCase()}%`;
    params.push(t, t);
  }

  sql += ' GROUP BY w.id';

  if (search) {
    sql += ' HAVING LOWER(w.form) LIKE ? OR LOWER(GROUP_CONCAT(m.gloss, \' | \')) LIKE ?';
    const t = `%${search.toLowerCase()}%`;
    params.push(t, t);
  }

  const dir = sortDir === 'desc' ? 'DESC' : 'ASC';
  switch (sortCol) {
    case 'form': sql += ` ORDER BY LOWER(w.form) ${dir}`; break;
    case 'gloss': sql += ` ORDER BY LOWER(MIN(m.gloss)) ${dir}`; break;
    case 'section': sql += ` ORDER BY w.section ${dir}`; break;
    case 'prefix': sql += ` ORDER BY w.consensus_prefix ${dir}`; break;
    case 'mask': sql += ` ORDER BY w.derivation_mask ${dir}`; break;
    case 'syl': sql += ` ORDER BY w.syl_count ${dir}`; break;
    case 'type': sql += ` ORDER BY w.is_function_word ${dir}, w.is_compound ${dir}`; break;
    default: sql += ` ORDER BY LOWER(w.form) ${dir}`;
  }

  return queryAll(sql, params).map((row) => enrichEntry(row));
}

function enrichEntry(row) {
  const wid = row.id;
  const meanings = (row.glosses_concat || '').split(' | ').filter(Boolean);
  const inflections = {};
  for (const ir of queryAll('SELECT form_type, form FROM inflections WHERE word_id = ?', [wid])) {
    inflections[ir.form_type] = ir.form;
  }
  let components = [];
  if (row.is_compound) {
    components = queryAll(
      `SELECT w2.form, w2.id, cc.position FROM compound_components cc
       JOIN words w2 ON cc.component_id = w2.id
       WHERE cc.compound_id = ? ORDER BY cc.position`, [wid]
    ).map((c) => ({ form: c.form, id: c.id }));
  }
  const meta = queryAll('SELECT pattern, rule_ref FROM compound_meta WHERE compound_id = ?', [wid])[0] || null;
  const examples = queryAll('SELECT kilor_text, english_text, source FROM examples WHERE word_id = ?', [wid])
    .map((ex) => ({ kilor: ex.kilor_text, english: ex.english_text, source: ex.source }));
  const SEC = { A:'Worlds & Elements', B:'Living Things', C:'Physical Objects', D:'Actions & Motion', E:'Qualities & States', F:'Mind & Emotion', G:'Time & Space', H:'Social & Relational', I:'Abstract', J:'Sensation' };
  return {
    id: wid, form: row.form, syl_count: row.syl_count, meanings,
    derivation_mask: row.derivation_mask || '', section: row.section,
    section_label: SEC[row.section] || 'Other',
    is_root: Boolean(row.is_root), is_compound: Boolean(row.is_compound),
    compound_type: row.compound_type || null,
    is_function_word: Boolean(row.is_function_word),
    consensus_prefix: row.consensus_prefix || 'o-',
    inflections, components,
    pattern: meta ? meta.pattern : null,
    rule_ref: meta ? meta.rule_ref : null,
    examples, notes: row.notes || '',
  };
}

export function getMeta() {
  if (!db) return { total: 0 };
  return { total: queryValue('SELECT COUNT(*) FROM words') || 0 };
}

export async function buildTestDB(entries) {
  const SQL = await initSqlJs({
    locateFile: isNode() ? undefined : (file) => `/${file}`,
  });
  const testDB = new SQL.Database();
  testDB.run(`CREATE TABLE words (id INTEGER PRIMARY KEY, form TEXT NOT NULL, syl_count INTEGER NOT NULL, is_root BOOLEAN DEFAULT 0, is_compound BOOLEAN DEFAULT 0, compound_type TEXT, derivation_mask TEXT, section TEXT NOT NULL, consensus_prefix TEXT, is_function_word BOOLEAN DEFAULT 0, notes TEXT)`);
  testDB.run(`CREATE TABLE meanings (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, gloss TEXT NOT NULL, sort_order INTEGER DEFAULT 0)`);
  testDB.run(`CREATE TABLE inflections (word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, form_type TEXT NOT NULL, form TEXT NOT NULL, PRIMARY KEY (word_id, form_type))`);
  testDB.run(`CREATE TABLE compound_components (compound_id INTEGER REFERENCES words(id) ON DELETE CASCADE, component_id INTEGER REFERENCES words(id) ON DELETE CASCADE, position INTEGER NOT NULL, PRIMARY KEY (compound_id, position))`);
  testDB.run(`CREATE TABLE compound_meta (compound_id INTEGER PRIMARY KEY REFERENCES words(id) ON DELETE CASCADE, pattern TEXT NOT NULL, rule_ref TEXT)`);
  testDB.run(`CREATE TABLE examples (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, kilor_text TEXT NOT NULL, english_text TEXT NOT NULL, source TEXT DEFAULT 'canonical')`);
  const iw = testDB.prepare('INSERT INTO words (id,form,syl_count,is_root,is_compound,compound_type,derivation_mask,section,consensus_prefix,is_function_word,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)');
  const im = testDB.prepare('INSERT INTO meanings (word_id, gloss, sort_order) VALUES (?,?,?)');
  const ii = testDB.prepare('INSERT INTO inflections (word_id, form_type, form) VALUES (?,?,?)');
  for (const e of entries) {
    iw.run([e.id, e.form, e.syl_count, e.is_root?1:0, e.is_compound?1:0, e.compound_type||null, e.derivation_mask||'', e.section, e.consensus_prefix||'o-', e.is_function_word?1:0, e.notes||'']);
    e.meanings.forEach((m, i) => im.run([e.id, m, i]));
    if (e.inflections) Object.entries(e.inflections).forEach(([t, f]) => ii.run([e.id, t, f]));
  }
  iw.free(); im.free(); ii.free();
  return testDB;
}

export function setDB(testDB) { db = testDB; }
export function getDB() { return db; }