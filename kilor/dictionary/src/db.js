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

// ── Autocomplete query (top 5 form matches) ──────────────────────────────────

/**
 * Returns up to 5 words whose form contains the search term,
 * ordered by prefix-match priority then alphabetically.
 * Used for the search-box autocomplete dropdown.
 */
export function autocompleteSearch(term) {
  if (!db || !term || term.length < 1) return [];
  const t = term.toLowerCase();
  const sql = `SELECT w.id, w.form FROM words w
    WHERE LOWER(w.form) LIKE ?
    ORDER BY
      CASE
        WHEN LOWER(w.form) LIKE ? THEN 0
        ELSE 1
      END,
      LOWER(w.form)
    LIMIT 5`;
  return queryAll(sql, [`%${t}%`, `${t}%`]).map((r) => ({ id: r.id, form: r.form }));
}

// ── SQL building helpers for queryWords / countWords ─────────────────────────

/**
 * Build the shared WHERE clause and params for filters.
 * Returns { whereClauses, params } to be joined with ' AND '.
 */
function buildFilterClauses({ search, types, masks, prefixes, sylMin, sylMax }) {
  const clauses = [];
  const params = [];

  const hasSearch = search && search.trim().length > 0;
  const searchTerm = hasSearch ? search.toLowerCase() : '';

  if (types.length > 0) {
    const typeConds = [];
    for (const t of types) {
      if (t === 'root') { typeConds.push('w.is_root = 1'); }
      else if (t === 'compound') { typeConds.push('w.is_compound = 1'); }
      else if (t === 'function') { typeConds.push('w.is_function_word = 1'); }
    }
    if (typeConds.length > 0) { clauses.push(`(${typeConds.join(' OR ')})`); }
  }

  if (masks.length > 0) {
    const maskConds = [];
    for (const m of masks) {
      maskConds.push('w.derivation_mask LIKE ?');
      params.push(`%${m}%`);
    }
    if (maskConds.length > 0) { clauses.push(`(${maskConds.join(' OR ')})`); }
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
    if (prefixConds.length > 0) { clauses.push(`(${prefixConds.join(' OR ')})`); }
  }

  if (sylMin != null && sylMin > 1) {
    clauses.push('w.syl_count >= ?');
    params.push(sylMin);
  }
  if (sylMax != null && sylMax < 10) {
    clauses.push('w.syl_count <= ?');
    params.push(sylMax);
  }

  // Search filter (pre-GROUP BY) — also matches search_text for inflection/case form search
  if (hasSearch) {
    clauses.push(`(LOWER(w.form) LIKE '%' || ? || '%' OR LOWER(m.gloss) LIKE '%' || ? || '%' OR LOWER(w.search_text) LIKE '%' || ? || '%')`);
    params.push(searchTerm, searchTerm, searchTerm);
  }

  return { clauses, params, hasSearch, searchTerm };
}

// ── Main word query with relevance-ranked search + pagination ────────────────

/**
 * Query words with optional filters, search, sorting, and pagination.
 *
 * @returns {{ rows: Array, totalCount: number }}
 *   - rows: enriched word entries for the current page (max pageSize items)
 *   - totalCount: total number of matching rows (for pagination controls)
 */
export function queryWords({
  search = '',
  types = [],
  masks = [],
  prefixes = [],
  sylMin = 1,
  sylMax = 10,
  sortCol = 'form',
  sortDir = 'asc',
  page = 1,
  pageSize = 50,
} = {}) {
  if (!db) return { rows: [], totalCount: 0 };

  const { clauses, params: filterParams, hasSearch, searchTerm } = buildFilterClauses({
    search, types, masks, prefixes, sylMin, sylMax,
  });

  // ── Total count query ──────────────────────────────────────────────
  let countSQL = `SELECT COUNT(DISTINCT w.id) AS cnt FROM words w LEFT JOIN meanings m ON w.id = m.word_id`;
  if (clauses.length > 0) {
    countSQL += ` WHERE ${clauses.join(' AND ')}`;
  }
  // For search: apply HAVING relevance > 0 which requires GROUP BY
  if (hasSearch) {
    countSQL = `SELECT COUNT(*) AS cnt FROM (
      SELECT w.id,
        CASE
          WHEN LOWER(w.form) LIKE '${searchTerm}%' THEN 4
          WHEN LOWER(w.form) LIKE '%${searchTerm}%' THEN 3
          WHEN LOWER(w.search_text) LIKE '%${searchTerm}%' THEN 2
          WHEN LOWER(GROUP_CONCAT(m.gloss, ' | ')) LIKE '%${searchTerm}%' THEN 1
          ELSE 0
        END AS relevance
      FROM words w LEFT JOIN meanings m ON w.id = m.word_id
      WHERE ${clauses.join(' AND ')}
      GROUP BY w.id
      HAVING relevance > 0
    )`;
  }
  const totalCount = queryValue(countSQL, [...filterParams]);
  if (totalCount === 0) return { rows: [], totalCount: 0 };

  // ── Data query with pagination ─────────────────────────────────────
  let cols = `w.id, w.form, w.syl_count, w.is_root, w.is_compound,
    w.compound_type, w.derivation_mask, w.consensus_prefix,
    w.is_function_word, w.notes, w.updated_at,
    GROUP_CONCAT(m.gloss, ' | ') AS glosses_concat,
    GROUP_CONCAT(m.pos, ' | ') AS poses_concat`;

  // Add relevance score when searching (4 tiers)
  if (hasSearch) {
    cols += `,
      CASE
        WHEN LOWER(w.form) LIKE '${searchTerm}%' THEN 4
        WHEN LOWER(w.form) LIKE '%${searchTerm}%' THEN 3
        WHEN LOWER(w.search_text) LIKE '%${searchTerm}%' THEN 2
        WHEN LOWER(GROUP_CONCAT(m.gloss, ' | ')) LIKE '%${searchTerm}%' THEN 1
        ELSE 0
      END AS relevance`;
  }

  let sql = `SELECT ${cols} FROM words w LEFT JOIN meanings m ON w.id = m.word_id`;
  if (clauses.length > 0) {
    sql += ` WHERE ${clauses.join(' AND ')}`;
  }
  sql += ' GROUP BY w.id';

  // Search filter (post-GROUP BY / HAVING)
  if (hasSearch) {
    sql += ` HAVING relevance > 0`;
  }

  const dir = sortDir === 'desc' ? 'DESC' : 'ASC';

  // When searching, always use relevance ordering (overrides sortCol)
  if (hasSearch) {
    sql += ` ORDER BY relevance DESC, LOWER(w.form) ASC`;
  } else {
    switch (sortCol) {
      case 'form': sql += ` ORDER BY LOWER(w.form) ${dir}`; break;
      case 'gloss': sql += ` ORDER BY LOWER(MIN(m.gloss)) ${dir}`; break;
      case 'prefix': sql += ` ORDER BY w.consensus_prefix ${dir}`; break;
      case 'mask': sql += ` ORDER BY w.derivation_mask ${dir}`; break;
      case 'syl': sql += ` ORDER BY w.syl_count ${dir}`; break;
      case 'type': sql += ` ORDER BY w.is_function_word ${dir}, w.is_compound ${dir}`; break;
      case 'updated': sql += ` ORDER BY w.updated_at ${dir}`; break;
      default: sql += ` ORDER BY LOWER(w.form) ${dir}`;
    }
  }

  // Pagination
  const safePage = Math.max(1, page);
  const safePageSize = Math.max(1, Math.min(pageSize, 200));
  const offset = (safePage - 1) * safePageSize;
  sql += ` LIMIT ? OFFSET ?`;

  const allParams = [...filterParams, safePageSize, offset];
  const rows = queryAll(sql, allParams);
  return { rows: enrichEntries(rows), totalCount };
}

// ── Case-form generation (browser-side, mirrors kilor/phonology.py) ──────────

const _PRONOUN_ACC_GEN = {
  "ki":   ["kin",   "kis"],
  "ti":   ["tin",   "tis"],
  "si":   ["sin",   "sis"],
  "ni":   ["nin",   "nis"],
  "kilo": ["kilon", "kilos"],
  "tilo": ["tilon", "tilos"],
  "silo": ["silon", "silos"],
  "nilo": ["nilon", "nilos"],
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

// ── IPA mapping ─────────────────────────────────────────────────────────────

const _IPA_MAP = {
  a: 'ɑ', e: 'ɛ', i: 'i', o: 'ɔ', u: 'u', y: 'y', ae: 'æ',
  p: 'p', b: 'b', m: 'm', f: 'f', w: 'w',
  t: 't', d: 'd', n: 'n', s: 's', l: 'l', r: 'r', c: 'ts',
  k: 'k', g: 'g', h: 'h',
  sh: 'ʃ', ch: 'tʃ', th: 'θ', ng: 'ŋ', x: 'x', rk: 'ɾk',
  sl: 's͜l', kl: 'k͜l', tl: 't͜l', bl: 'b͜l', ml: 'm͜l',
  kr: 'k͡r', br: 'b͡r', gr: 'ɡ͡r', fr: 'f͡r', pr: 'p͡r',
  j: '˥', v: '˩',
  'ai': 'aɪ', 'au': 'aʊ', 'ei': 'eɪ', 'eu': 'eʊ',
  'iu': 'ju', 'oi': 'ɔɪ', 'ou': 'oʊ',
  '-': '', ' ': ' ',
};

const _IPA_MULTICHAR_KEYS = Object.keys(_IPA_MAP).filter((k) => k.length > 1).sort((a, b) => b.length - a.length);

function toIPA(word) {
  if (!word) return '';
  let result = '';
  let i = 0;
  while (i < word.length) {
    let matched = false;
    for (const mk of _IPA_MULTICHAR_KEYS) {
      if (word.slice(i, i + mk.length).toLowerCase() === mk) {
        result += _IPA_MAP[mk] || mk;
        i += mk.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      const ch = word[i].toLowerCase();
      result += _IPA_MAP[ch] || word[i];
      i += 1;
    }
  }
  return result;
}

// ── Tone-preserving syllable splitter ───────────────────────────────────────

/**
 * Split a word into syllable objects with start/end offsets in the *original* string.
 * Unlike splitSyllablesJS, this preserves tone marker positions — j/v are not
 * stripped; they float between syllables.
 *
 * Returns array of { onset, nucleus, coda, start, end } where start/end
 * reference positions in the *cleaned* word (after stripping tone markers for
 * parsing, but we track where the vowel of each syllable lives).
 */
function _syllablePositions(word) {
  const cleaned = word.replace(/[jv]/g, '').replace(/-/g, '');
  const toneStripped = word.replace(/[jv]/g, '');

  // Build mapping: each position in cleaned → position in original word
  const cleanedToOrig = [];
  let ci = 0;
  for (let oi = 0; oi < word.length; oi++) {
    const ch = word[oi];
    if (ch === 'j' || ch === 'v' || ch === '-') continue;
    if (ci < cleaned.length && cleaned[ci] === ch) {
      cleanedToOrig[ci] = oi;
      ci++;
    }
  }

  const n = cleaned.length;
  if (n === 0) return [];

  const syllables = [];
  let i = 0;
  while (i < n) {
    const onsetStart = i;

    let onset = '';
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

    if (i >= n) throw new Error(`incomplete syllable in '${cleaned}' at position ${i}`);

    const nucleusStart = i;
    if (_VOWELS.has(cleaned[i])) {
      if (cleaned.slice(i, i + 2) === 'ae') {
        i += 2;
      } else if (i + 1 < n && _DIPHTHONGS.has(cleaned.slice(i, i + 2))) {
        i += 2;
      } else {
        i += 1;
      }
    }
    const nucleus = cleaned.slice(nucleusStart, i);

    let coda = '';
    if (i < n) {
      if (i + 2 <= n && _END_ONLYS.has(cleaned.slice(i, i + 2)) && i + 2 === n) {
        coda = cleaned.slice(i, i + 2);
        i += 2;
      } else if (i + 2 <= n && _EDGE_ONLYS.has(cleaned.slice(i, i + 2)) && i + 2 === n) {
        coda = cleaned.slice(i, i + 2);
        i += 2;
      } else if (i + 1 === n && _END_ONLYS.has(cleaned[i])) {
        coda = cleaned[i];
        i += 1;
      } else if (_CORE_CONS.has(cleaned[i])) {
        if (i + 1 >= n || !_VOWELS.has(cleaned[i + 1])) {
          coda = cleaned[i];
          i += 1;
        }
      }
    }

    // vowel end position in the *original* word (the position right after the
    // nucleus vowel, where we'd insert a tone marker)
    const vowelEndCleaned = nucleusStart + nucleus.length;
    const vowelEndOrig = cleanedToOrig[vowelEndCleaned - 1] !== undefined
      ? cleanedToOrig[vowelEndCleaned - 1] + 1
      : vowelEndCleaned;

    syllables.push({
      onset, nucleus, coda,
      vowelEndOrig,
    });
  }

  return syllables;
}

// ── Inflection computation (replaces stored inflections table) ──────────────

/**
 * Compute correct Kilor inflections from the prosody rules.
 *
 * Rules (from rules/0-foundation/tone-prosody.md §II, §III):
 *   - 1–2 syllable words: toneless. N/V = bare root, A/D = root + '-s'.
 *   - 3+ syllable words: tone markers j/v inserted into last-3 domain.
 *     Noun: j on 1st of last-3. Verb: v on 1st of last-3.
 *     Adj: j on 2nd of last-3. Adv: v on 2nd of last-3.
 *   - Only compute for categories present in the derivation_mask.
 *   - Single-mask words: include toneless form alongside tonemarked form.
 *   - For compounds: tone markers apply to the whole form (mono) or last word (multi).
 *   - Return result in N → V → A → D order with single-value entries.
 *
 * @returns {Object} — e.g. { noun: 'forajgilan', adjective: 'foragijlan' }
 */
function computeInflections(form, sylCount, derivationMask) {
  if (!derivationMask) return {};
  const mask = derivationMask.toUpperCase();
  const result = {};
  const maskLetters = ['N', 'V', 'A', 'D'];

  const isToneless = sylCount <= 2;

  // For multi-word compounds (with spaces), tone markers go on the last word.
  const words = form.split(' ');
  const lastWordIdx = words.length - 1;

  for (const letter of maskLetters) {
    if (!mask.includes(letter)) continue;

    if (isToneless) {
      if (letter === 'N' || letter === 'V') {
        result[_maskKey(letter)] = form;
      } else {
        result[_maskKey(letter)] = form + 's';
      }
    } else {
      // 3+ syllable word — apply tone markers to the last word (for multi-word)
      // or the only word (for mono).
      const targetWord = words[lastWordIdx];
      const syls = _syllablePositions(targetWord);

      if (syls.length < 3) {
        // Fallback: should not happen for 3+ syllable words, but just in case
        result[_maskKey(letter)] = form;
        continue;
      }

      const last3 = syls.slice(-3);
      const anchorIdx = letter === 'N' || letter === 'V' ? 0 : 1;
      const anchor = last3[anchorIdx];
      const toneChar = letter === 'N' || letter === 'A' ? 'j' : 'v';

      // Insert tone marker after the vowel nucleus of the anchor syllable
      const vowelEnd = anchor.vowelEndOrig;
      const tonedLastWord = targetWord.slice(0, vowelEnd) + toneChar + targetWord.slice(vowelEnd);

      if (words.length === 1) {
        result[_maskKey(letter)] = tonedLastWord;
      } else {
        result[_maskKey(letter)] = [...words.slice(0, -1), tonedLastWord].join(' ');
      }

      // For single-mask words: also include the base form (toneless).
      if (mask.length === 1) {
        const base = form;
        result[_maskKey(letter)] = [base, result[_maskKey(letter)]];
      }
    }
  }

  return result;
}

function _maskKey(letter) {
  switch (letter) {
    case 'N': return 'noun';
    case 'V': return 'verb';
    case 'A': return 'adjective';
    case 'D': return 'adverb';
    default: return '';
  }
}

// ── Batch enrichment — avoids N+1 query pattern ─────────────────────────────

/**
 * Enrich all result rows in one pass using 4 batched queries instead of
 * 4 queries per row. At 10k results, goes from 40,000 queries to 4.
 */
function enrichEntries(rows) {
  if (rows.length === 0) return [];

  const ids = rows.map((r) => r.id);
  const idSet = new Set(ids);
  const idList = ids.join(',');
  if (!idList) return [];

  // Build id → enriched fragment maps
  const wordMap = {};
  for (const row of rows) {
    wordMap[row.id] = {
      row,
      inflections: {},
      components: [],
      meta: null,
      examples: [],
    };
  }

  // 1. Batch inflections
  for (const ir of queryAll(
    `SELECT word_id, form_type, form FROM inflections WHERE word_id IN (${idList})`
  )) {
    if (wordMap[ir.word_id]) {
      wordMap[ir.word_id].inflections[ir.form_type] = ir.form;
    }
  }

  // 2. Batch compound components (only for compound words)
  const compoundIds = rows.filter((r) => r.is_compound).map((r) => r.id);
  if (compoundIds.length > 0) {
    const cList = compoundIds.join(',');
    const compRows = queryAll(
      `SELECT cc.compound_id, w2.form, w2.id AS component_wid, cc.position
       FROM compound_components cc
       JOIN words w2 ON cc.component_id = w2.id
       WHERE cc.compound_id IN (${cList})
       ORDER BY cc.compound_id, cc.position`
    );
    const compMap = {};
    for (const cr of compRows) {
      if (!compMap[cr.compound_id]) compMap[cr.compound_id] = [];
      compMap[cr.compound_id].push({ form: cr.form, id: cr.component_wid });
    }
    for (const cid of compoundIds) {
      if (wordMap[cid]) {
        wordMap[cid].components = compMap[cid] || [];
      }
    }
  }

  // 3. Batch compound meta
  if (compoundIds.length > 0) {
    const cmList = compoundIds.join(',');
    for (const cm of queryAll(
      `SELECT compound_id, pattern, rule_ref FROM compound_meta WHERE compound_id IN (${cmList})`
    )) {
      if (wordMap[cm.compound_id]) {
        wordMap[cm.compound_id].meta = { pattern: cm.pattern, rule_ref: cm.rule_ref };
      }
    }
  }

  // 4. Batch examples
  for (const ex of queryAll(
    `SELECT word_id, kilor_text, english_text, source FROM examples WHERE word_id IN (${idList})`
  )) {
    if (wordMap[ex.word_id]) {
      wordMap[ex.word_id].examples.push({
        kilor: ex.kilor_text,
        english: ex.english_text,
        source: ex.source,
      });
    }
  }

  // Assemble final entries
  return rows.map((row) => {
    const frag = wordMap[row.id];
    const glosses = (row.glosses_concat || '').split(' | ').filter(Boolean);
    const poses = (row.poses_concat || '').split(' | ');
    const meanings = glosses.map((gloss, i) => ({
      gloss,
      pos: poses[i] || '',
    }));
    const meta = frag.meta;
    const case_forms = getCaseForms(row.form, row.derivation_mask || null, Boolean(row.is_function_word));
    const mask = row.derivation_mask || '';
    const computedInfl = computeInflections(row.form, row.syl_count, mask);
    return {
      id: row.id,
      form: row.form,
      syl_count: row.syl_count,
      syllables: row.form.split(" ").map((w) => splitSyllablesJS(w).join("/")).join(" / "),
      ipa: row.form.split(" ").map((w) => toIPA(w)).join(" "),
      meanings,
      derivation_mask: mask,
      is_root: Boolean(row.is_root),
      is_compound: Boolean(row.is_compound),
      compound_type: row.compound_type || null,
      is_function_word: Boolean(row.is_function_word),
      consensus_prefix: row.consensus_prefix || null,
      inflections: computedInfl,
      components: frag.components,
      pattern: meta ? meta.pattern : null,
      rule_ref: meta ? meta.rule_ref : null,
      case_forms,
      examples: frag.examples,
      notes: row.notes || '',
      updated_at: row.updated_at || null,
      relevance: row.relevance != null ? row.relevance : undefined,
    };
  });
}

// ── Fuzzy search (Levenshtein fallback for 0-result queries) ───────────────

/**
 * Levenshtein distance between two strings.
 */
function levenshtein(a, b) {
  const alen = a.length;
  const blen = b.length;
  if (alen === 0) return blen;
  if (blen === 0) return alen;

  let prev = new Array(blen + 1);
  let curr = new Array(blen + 1);
  for (let j = 0; j <= blen; j++) prev[j] = j;

  for (let i = 1; i <= alen; i++) {
    curr[0] = i;
    for (let j = 1; j <= blen; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
    }
    const tmp = prev; prev = curr; curr = tmp;
  }
  return prev[blen];
}

/**
 * Returns up to 30 words within Levenshtein distance threshold.
 * Threshold: ≤1 for 1–3 char words, ≤2 for 4–6 char words, ≤3 for 7+ char words.
 *
 * @returns {{ rows: Array, totalCount: number }}
 */
export function fuzzySearch(term) {
  if (!db || !term || term.length < 2) return { rows: [], totalCount: 0 };
  const t = term.toLowerCase();
  const threshold = t.length <= 3 ? 1 : t.length <= 6 ? 2 : 3;

  const rows = queryAll('SELECT id, form FROM words');

  const scored = rows
    .map((r) => ({ ...r, dist: levenshtein(t, r.form.toLowerCase()) }))
    .filter((r) => r.dist <= threshold)
    .sort((a, b) => a.dist - b.dist || a.form.localeCompare(b.form))
    .slice(0, 30);

  if (scored.length === 0) return { rows: [], totalCount: 0 };

  // Fetch full word data for fuzzy-matched IDs
  const idList = scored.map((r) => r.id).join(',');
  const fullRows = queryAll(
    `SELECT w.id, w.form, w.syl_count, w.is_root, w.is_compound,
      w.compound_type, w.derivation_mask, w.consensus_prefix,
      w.is_function_word, w.notes,
      GROUP_CONCAT(m.gloss, ' | ') AS glosses_concat,
      GROUP_CONCAT(m.pos, ' | ') AS poses_concat
    FROM words w LEFT JOIN meanings m ON w.id = m.word_id
    WHERE w.id IN (${idList})
    GROUP BY w.id
    ORDER BY LOWER(w.form)`
  );

  const enriched = enrichEntries(fullRows);
  // Attach fuzzy distance to entries
  const distMap = {};
  for (const r of scored) distMap[r.id] = r.dist;
  return {
    rows: enriched.map((e) => ({ ...e, fuzzyDistance: distMap[e.id] })),
    totalCount: enriched.length,
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
  testDB.run(`CREATE TABLE words (id INTEGER PRIMARY KEY, form TEXT NOT NULL, syl_count INTEGER NOT NULL, is_root BOOLEAN DEFAULT 0, is_compound BOOLEAN DEFAULT 0, compound_type TEXT, derivation_mask TEXT, consensus_prefix TEXT, search_text TEXT DEFAULT '', is_function_word BOOLEAN DEFAULT 0, notes TEXT, updated_at TEXT)`);
  testDB.run(`CREATE TABLE meanings (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, gloss TEXT NOT NULL, pos TEXT DEFAULT '', sort_order INTEGER DEFAULT 0)`);
  testDB.run(`CREATE TABLE inflections (word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, form_type TEXT NOT NULL, form TEXT NOT NULL, PRIMARY KEY (word_id, form_type))`);
  testDB.run(`CREATE TABLE compound_components (compound_id INTEGER REFERENCES words(id) ON DELETE CASCADE, component_id INTEGER REFERENCES words(id) ON DELETE CASCADE, position INTEGER NOT NULL, PRIMARY KEY (compound_id, position))`);
  testDB.run(`CREATE TABLE compound_meta (compound_id INTEGER PRIMARY KEY REFERENCES words(id) ON DELETE CASCADE, pattern TEXT NOT NULL, rule_ref TEXT)`);
  testDB.run(`CREATE TABLE examples (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES words(id) ON DELETE CASCADE, kilor_text TEXT NOT NULL, english_text TEXT NOT NULL, source TEXT DEFAULT 'canonical')`);
  const iw = testDB.prepare('INSERT INTO words (id,form,syl_count,is_root,is_compound,compound_type,derivation_mask,consensus_prefix,is_function_word,notes) VALUES (?,?,?,?,?,?,?,?,?,?)');
  const im = testDB.prepare('INSERT INTO meanings (word_id, gloss, pos, sort_order) VALUES (?,?,?,?)');
  const ii = testDB.prepare('INSERT INTO inflections (word_id, form_type, form) VALUES (?,?,?)');
  for (const e of entries) {
    iw.run([e.id, e.form, e.syl_count, e.is_root?1:0, e.is_compound?1:0, e.compound_type||null, e.derivation_mask||'', e.consensus_prefix ?? 'o-', e.is_function_word?1:0, e.notes||'']);
    e.meanings.forEach((m, i) => {
      const gloss = typeof m === 'string' ? m : m.gloss;
      const pos = typeof m === 'string' ? '' : (m.pos || '');
      im.run([e.id, gloss, pos, i]);
    });
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