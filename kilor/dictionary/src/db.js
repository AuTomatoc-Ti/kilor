/**
 * SQLite database layer for the Kilor Dictionary.
 * Uses sql.js (SQLite compiled to WebAssembly) to read kilor.db directly.
 */

// sql.js browser build is CJS (module.exports = initSqlJs).
// Use namespace import + default extraction for compatibility with Vite's CJS interop.
import * as sqlJsModule from 'sql.js';
const initSqlJs = sqlJsModule.default || sqlJsModule;

// Import the wasm binary URL from the installed sql.js npm package.
// Vite's `?url` loader resolves this to a hashed asset URL at build time
// and serves it correctly in dev mode, avoiding MIME-type issues.
import sqlWasmUrl from 'sql.js/dist/sql-wasm.wasm?url';

let db = null;

export function isDatabaseLoaded() {
  return db !== null;
}

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

  return _loadDatabase();
}

async function _loadDatabase() {
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
    // Use the version-matched wasm from the installed sql.js package.
    // Vite's `?url` import gives us a properly served URL with correct MIME type.
    SQL = await initSqlJs({ locateFile: () => sqlWasmUrl });
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
  return db;
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
  sections = [],
  types = [],
  masks = [],
  prefixes = [],
  sylMin = 1,
  sylMax = 10,
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

  if (sections.length > 0) {
    sql += ` AND w.section IN (${sections.map(() => '?').join(',')})`;
    params.push(...sections);
  }

  if (types.length > 0) {
    const typeConds = [];
    for (const t of types) {
      if (t === 'root') { typeConds.push('w.is_root = 1'); }
      else if (t === 'compound') { typeConds.push('w.is_compound = 1'); }
      else if (t === 'function') { typeConds.push('w.is_function_word = 1'); }
    }
    if (typeConds.length > 0) { sql += ` AND (${typeConds.join(' OR ')})`; }
  }

  if (masks.length > 0) {
    const maskConds = [];
    for (const m of masks) {
      maskConds.push('w.derivation_mask LIKE ?');
      params.push(`%${m}%`);
    }
    if (maskConds.length > 0) { sql += ` AND (${maskConds.join(' OR ')})`; }
  }

  if (prefixes.length > 0) {
    const prefixConds = [];
    for (const p of prefixes) {
      if (p === 'NONE') {
        prefixConds.push("(w.consensus_prefix IS NULL OR w.consensus_prefix = '')");
      } else {
        prefixConds.push('w.consensus_prefix = ?');
        params.push(p);
      }
    }
    if (prefixConds.length > 0) { sql += ` AND (${prefixConds.join(' OR ')})`; }
  }

  if (sylMin != null && sylMin > 1) {
    sql += ' AND w.syl_count >= ?';
    params.push(sylMin);
  }
  if (sylMax != null && sylMax < 10) {
    sql += ' AND w.syl_count <= ?';
    params.push(sylMax);
  }

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

// ── Case-form generation (browser-side, mirrors kilor/phonology.py) ──────────

const _PRONOUN_ACC_GEN = {
  "ki":  ["kin",  "kis"],
  "ti":  ["tin",  "tis"],
  "si":  ["sin",  "sis"],
  "ni":  ["nin",  "nis"],
  "kil": ["kilin", "kilis"],
  "til": ["tilin", "tilis"],
  "sil": ["silin", "silis"],
  "nil": ["nilin", "nilis"],
};

const _COLOUR_PREFIXES = ["ae-", "a-", "e-", "i-", "o-", "u-", "y-"];

const _FRONT_VOWELS = new Set(["e", "i", "y", "ae", "ei", "eu", "iu"]);
const _BACK_VOWELS  = new Set(["a", "o", "u", "ai", "au", "oi", "ou"]);
const _VOWELS = new Set("aeiouy");
const _DIPHTHONGS = new Set(["ai", "au", "ei", "eu", "iu", "oi", "ou"]);
const _CORE_CONS = new Set("pbmfwtdnslrckgh".split(""));
const _EDGE_ONLYS = new Set(["sh", "ch", "th"]);
const _START_ONLYS = new Set(["sl", "kl", "tl", "bl", "ml", "kr", "br", "gr", "fr", "pr"]);
const _END_ONLYS = new Set(["ng", "x", "rk"]);

function lastNucleus(word) {
  /* Scan right-to-left for the last vowel or diphthong.
     Skip tone markers (j, v) and hyphens (extra-segmental). */
  const cleaned = word.replace(/[jv]/g, "").replace(/-/g, "").replace(/ /g, "");
  for (let i = cleaned.length - 1; i >= 0; i--) {
    const pair = cleaned.slice(i - 1, i + 1).toLowerCase();
    if (pair === "ae" || _DIPHTHONGS.has(pair)) return pair;
    const ch = cleaned[i].toLowerCase();
    if (_VOWELS.has(ch)) return ch;
  }
  return "";
}

function stripPrefix(form) {
  for (const pfx of _COLOUR_PREFIXES) {
    if (form.startsWith(pfx)) return [pfx, form.slice(pfx.length)];
  }
  return ["", form];
}

function getCaseForms(form, derivationMask, isFunctionWord) {
  if (isFunctionWord) return {};
  if (derivationMask && derivationMask.toUpperCase().indexOf("N") === -1) return {};

  // Pronouns (invariant)
  if (_PRONOUN_ACC_GEN[form]) {
    const [acc, gen] = _PRONOUN_ACC_GEN[form];
    return { acc, gen };
  }

  const words = form.split(" ");
  if (words.length === 0) return {};

  let lastWord = words[words.length - 1];
  const [prefix, root] = stripPrefix(lastWord);
  const nucleus = lastNucleus(root);
  if (!nucleus) return {};

  let accSuffix, genSuffix;
  if (_FRONT_VOWELS.has(nucleus)) {
    accSuffix = "na"; genSuffix = "sa";
  } else if (_BACK_VOWELS.has(nucleus)) {
    accSuffix = "ni"; genSuffix = "si";
  } else {
    return {};
  }

  let accForm, genForm;
  if (words.length === 1) {
    accForm = prefix + root + accSuffix;
    genForm = prefix + root + genSuffix;
  } else {
    accForm = words.slice(0, -1).concat([prefix + root + accSuffix]).join(" ");
    genForm = words.slice(0, -1).concat([prefix + root + genSuffix]).join(" ");
  }
  return { acc: accForm, gen: genForm };
}

// ──────────────────────────────────────────────────────────────────────────────

function splitSyllablesJS(word) {
  /* Greedy left-to-right syllable parser using the Maximal Onset Principle.
     Mirrors kilor/phonology.py:split_syllables().

     Strips tone markers (j, v) and prefix hyphens before parsing — these are
     extra-segmental and float outside the syllable structure.

     Positional consonant classes:
       - Start-only and edge-only only match at i == 0 (onset)
       - End-only and edge-only only match at word-final position (coda)
       - Mid-word multi-char sequences are separate core consonants
       - Intervocalic core consonant → onset of next syllable (maxonset)
  */
  const cleaned = word.replace(/[jv]/g, "").replace(/-/g, "");
  const n = cleaned.length;
  if (n === 0) return [];

  const syllables = [];
  let i = 0;
  while (i < n) {
    let onset = "";
    // Onset
    if (i === 0 && i + 2 <= n && _START_ONLYS.has(cleaned.slice(i, i + 2))) {
      onset = cleaned.slice(i, i + 2);
      i += 2;
    } else if (i === 0 && i + 2 <= n && _EDGE_ONLYS.has(cleaned.slice(i, i + 2))) {
      onset = cleaned.slice(i, i + 2);
      i += 2;
    } else if (i < n && _CORE_CONS.has(cleaned[i])) {
      onset = cleaned[i];
      i += 1;
    }

    // Nucleus
    if (i >= n) throw new Error(`incomplete syllable in '${cleaned}' at position ${i}`);
    const nucleusStart = i;
    if (_VOWELS.has(cleaned[i])) {
      if (cleaned.slice(i, i + 2) === "ae") {
        i += 2;
      } else if (i + 1 < n && _DIPHTHONGS.has(cleaned.slice(i, i + 2))) {
        i += 2;
      } else {
        i += 1;
      }
    }
    const nucleus = cleaned.slice(nucleusStart, i);
    if (!nucleus) {
      throw new Error(
        `degenerate syllable in '${cleaned}' at position ${i}: ` +
        "consonant taken as onset but no vowel follows"
      );
    }

    // Coda (maxonset: only take if no vowel follows)
    let coda = "";
    if (i < n) {
      if (i + 2 <= n && _END_ONLYS.has(cleaned.slice(i, i + 2)) && i + 2 === n) {
        coda = cleaned.slice(i, i + 2);
        i += 2;
      } else if (i + 2 <= n && _EDGE_ONLYS.has(cleaned.slice(i, i + 2)) && i + 2 === n) {
        coda = cleaned.slice(i, i + 2);
        i += 2;
      } else if (i + 1 === n && _END_ONLYS.has(cleaned[i])) {
        // Single-char end-only letter (e.g. 'x') at word-final position
        coda = cleaned[i];
        i += 1;
      } else if (_CORE_CONS.has(cleaned[i])) {
        if (i + 1 >= n || !_VOWELS.has(cleaned[i + 1])) {
          coda = cleaned[i];
          i += 1;
        }
      }
    }

    syllables.push(onset + nucleus + coda);
  }

  return syllables;
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
  const case_forms = getCaseForms(row.form, row.derivation_mask || null, Boolean(row.is_function_word));
  const SEC = { A:'Worlds & Elements', B:'Living Things', C:'Physical Objects', D:'Actions & Motion', E:'Qualities & States', F:'Mind & Emotion', G:'Time & Space', H:'Social & Relational', I:'Abstract', J:'Sensation' };
  return {
    id: wid, form: row.form, syl_count: row.syl_count,
    syllables: row.form.split(" ").map(w => splitSyllablesJS(w).join("/")).join(" / "),
    meanings,
    derivation_mask: row.derivation_mask || '', section: row.section,
    section_label: SEC[row.section] || 'Other',
    is_root: Boolean(row.is_root), is_compound: Boolean(row.is_compound),
    compound_type: row.compound_type || null,
    is_function_word: Boolean(row.is_function_word),
    consensus_prefix: row.consensus_prefix || null,
    inflections, components,
    pattern: meta ? meta.pattern : null,
    rule_ref: meta ? meta.rule_ref : null,
    case_forms, examples, notes: row.notes || '',
  };
}

export function getMeta() {
  if (!db) return { total: 0 };
  return { total: queryValue('SELECT COUNT(*) FROM words') || 0 };
}

export async function buildTestDB(entries) {
  const SQL = await initSqlJs({
    locateFile: isNode() ? undefined : () => sqlWasmUrl,
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
    iw.run([e.id, e.form, e.syl_count, e.is_root?1:0, e.is_compound?1:0, e.compound_type||null, e.derivation_mask||'', e.section, e.consensus_prefix ?? 'o-', e.is_function_word?1:0, e.notes||'']);
    e.meanings.forEach((m, i) => im.run([e.id, m, i]));
    if (e.inflections) Object.entries(e.inflections).forEach(([t, f]) => ii.run([e.id, t, f]));
  }
  iw.free(); im.free(); ii.free();
  return testDB;
}

export function setDB(testDB) { db = testDB; }
export async function reloadDatabase() {
  // Fetch fresh kilor.db via HTTP and replace the in-memory database.
  // Works because public/kilor.db is a symlink to data/kilor.db.
  const resp = await fetch('./kilor.db', { cache: 'no-store' });
  if (!resp.ok) {
    throw new Error(
      `Cannot reload database: HTTP ${resp.status} fetching ./kilor.db.`
    );
  }
  const buf = await resp.arrayBuffer();
  const DatabaseCtor = db.constructor; // the Database class (from new SQL.Database(...))
  const newDB = new DatabaseCtor(new Uint8Array(buf));

  // Safety check: verify the new DB is queryable before replacing the old one
  let count;
  try {
    count = newDB.exec('SELECT COUNT(*) FROM words')[0]?.values[0]?.[0] ?? 0;
  } catch (_e) {
    newDB.close();
    throw new Error('Reloaded database is corrupt or unreadable');
  }

  db.close();
  db = newDB;
  return count;
}

export function getDB() { return db; }
