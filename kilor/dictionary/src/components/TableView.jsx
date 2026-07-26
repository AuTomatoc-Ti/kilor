import React from 'react';

const MASK_LABELS = { N: 'Noun', V: 'Verb', A: 'Adjective', D: 'Adverb' };

/** Inline PoS tags (table row gloss column) — minimized abbreviations. */
const POS_INLINE = {
  N: 'N', V: 'V', A: 'A', D: 'D',
  PRON: 'PRON', NUM: 'NUM',
  CCONJ: 'CONJ', SCONJ: 'CONJ',
  ADP: 'ADP', PART: 'PART', MODAL: 'MOD',
  DEM: 'DEM', Q: 'Q',
  CLF: 'CLF', INTERJ: 'INTJ', PROPN: 'NAME',
  '': '',
};

/** Full descriptive labels for subpage PoS sections. */
const POS_FULL = {
  N: 'Noun', V: 'Verb', A: 'Adjective', D: 'Adverb',
  PRON: 'Pronoun', NUM: 'Numeral',
  CCONJ: 'Coordinating Conjunction', SCONJ: 'Subordinating Conjunction',
  ADP: 'Adposition', PART: 'Particle', MODAL: 'Modal Verb',
  DEM: 'Demonstrative', Q: 'Question Word',
  CLF: 'Classifier / Measure Word', INTERJ: 'Interjection', PROPN: 'Proper Noun',
  '': 'Other',
};

function highlightMatch(text, term) {
  if (!term || term.length === 0) return text;
  const idx = text.toLowerCase().indexOf(term.toLowerCase());
  if (idx === -1) return text;
  return (
    <>
      {text.slice(0, idx)}
      <mark className="search-highlight">{text.slice(idx, idx + term.length)}</mark>
      {text.slice(idx + term.length)}
    </>
  );
}

function PrefixBadge({ prefix, info }) {
  if (!prefix || prefix === '' || prefix === '-') return <span className="empty-cell">—</span>;
  if (!info) return <span className="empty-cell">—</span>;
  return (
    <span className="prefix-badge" style={{ background: info.color }}>
      <span className="prefix-swatch"></span>
      {prefix} {info.cls}
    </span>
  );
}

function TypeTag({ entry }) {
  if (entry.is_function_word) return <span className="tag-sm tag-function">func</span>;
  if (entry.is_compound) return <span className="tag-sm tag-compound">{entry.compound_type || '?'}-cmpd</span>;
  if (entry.is_root) return <span className="tag-sm tag-root">root</span>;
  return null;
}

function ComponentChips({ components, onSearchByForm }) {
  if (!components || components.length === 0) return null;
  return (
    <>
      {' '}
      {components.map((c, i) => {
        const name = typeof c === 'string' ? c : c.form;
        return (
          <span
            key={i}
            className="component-chip"
            onClick={(e) => { e.stopPropagation(); onSearchByForm(name); }}
            title={"Click to find '" + name + "'"}
          >
            {name}
          </span>
        );
      })}
    </>
  );
}

/** Display all glosses with abbreviated PoS tags, M-W style. */
function GlossWithPos({ meanings, search }) {
  if (!meanings || meanings.length === 0) return <span className="empty-cell">—</span>;

  // Get the gloss strings (works with both old flat array and new object array)
  const items = typeof meanings[0] === 'string'
    ? meanings.map((g, i) => ({ gloss: g, pos: '' }))
    : meanings;

  // For single-meaning words with no pos, show just the gloss
  if (items.length === 1 && !items[0].pos) {
    return highlightMatch(items[0].gloss, search);
  }

  // Limit display: show first 4, then "+N more"
  const maxShow = 4;
  const shown = items.slice(0, maxShow);
  const remaining = items.length - maxShow;

  return (
    <>
      {shown.map((m, i) => (
        <span key={i}>
          {i > 0 && <span className="gloss-sep"> · </span>}
          {m.pos && <span className="pos-tag-inline" title={POS_FULL[m.pos] || m.pos}>{POS_INLINE[m.pos] || m.pos}</span>}
          {highlightMatch(m.gloss, search)}
        </span>
      ))}
      {remaining > 0 && <span className="gloss-more"> +{remaining} more</span>}
    </>
  );
}

/** Trimmed inline preview — form, IPA, prefix, mask, quick gloss view + link to full entry. */
function DetailPanel({ entry, prefixInfo, onViewFull }) {
  const mask = entry.derivation_mask || '';
  const glossesAll = (entry.meanings || []).map(m => (typeof m === 'string' ? m : m.gloss)).join(' / ');

  return (
    <div className="detail-panel">
      <div className="detail-columns">
        <div className="detail-col">
          <div className="detail-row">
            <strong>Kilor</strong> {entry.form}
          </div>
          {entry.ipa && (
            <div className="detail-row">
              <strong>IPA</strong> <span className="ipa-text">/{entry.ipa}/</span>
            </div>
          )}
          <div className="detail-row">
            <strong>Syllables</strong> {entry.syl_count}{entry.syllables ? ` (${entry.syllables})` : ''}
          </div>
        </div>
        <div className="detail-col">
          {mask && (
            <div className="detail-row">
              <strong>NVAD</strong> <span className="tag-mask">{mask}</span>
            </div>
          )}
          {entry.consensus_prefix && (
            <div className="detail-row">
              <strong>Prefix</strong> {entry.consensus_prefix}
              {entry.consensus_prefix && prefixInfo[entry.consensus_prefix]
                ? ` (${prefixInfo[entry.consensus_prefix].cls} · ${prefixInfo[entry.consensus_prefix].emotion})`
                : ''}
            </div>
          )}
          <div className="detail-row">
            <strong>Gloss</strong> {glossesAll}
          </div>
        </div>
      </div>
      {onViewFull && (
        <div className="detail-view-full">
          <button className="view-full-link" onClick={(e) => { e.stopPropagation(); onViewFull(entry.id); }}>
            View full entry →
          </button>
        </div>
      )}
    </div>
  );
}

// ── Full Word Detail Page (subpage) ─────────────────────────────────────────

export function WordDetailPage({ entry, prefixInfo, onBack, onSearchByForm, onCopyToast }) {
  if (!entry) return null;

  const handleCopy = (e, form) => {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(form).then(() => {
        if (onCopyToast) onCopyToast('Copied: ' + form);
      }).catch(() => {});
    }
  };

  const mask = entry.derivation_mask || '';
  const meanings = entry.meanings || [];

  // Group meanings by pos
  const grouped = {};
  for (const m of meanings) {
    const gl = typeof m === 'string' ? m : m.gloss;
    const p = typeof m === 'string' ? '' : (m.pos || '');
    if (!grouped[p]) grouped[p] = [];
    grouped[p].push(gl);
  }

  // Determine display order: N, V, A, D first, then any other tags
  const posOrder = ['N', 'V', 'A', 'D'];
  const extraOrder = Object.keys(grouped).filter(p => p && !posOrder.includes(p));
  const sections = [...posOrder.filter(p => grouped[p]), ...extraOrder];

  // Inflections (N→V→A→D order)
  const infl = entry.inflections || {};
  const inflOrder = ['noun', 'verb', 'adjective', 'adverb'];
  const inflPresent = inflOrder.filter(k => infl[k]);

  return (
    <div className="word-detail-page">
      <div className="detail-header">
        <button className="back-button" onClick={onBack}>← Back to dictionary</button>
      </div>

      {/* ── Identity Card ─────────────────────────────────────── */}
      <div className="detail-identity-card">
        <div className="detail-word-row">
          <h2 className="detail-word-form">{entry.form}</h2>
          <span className="detail-word-badges">
            <TypeTag entry={entry} />
            {mask && <span className="tag-mask">{mask}</span>}
          </span>
        </div>
        <div className="detail-word-meta">
          {entry.ipa && <span className="meta-item">/{entry.ipa}/</span>}
          <span className="meta-item">{entry.syl_count} syll · {entry.syllables}</span>
          {entry.consensus_prefix && (
            <span className="meta-item">
              <PrefixBadge prefix={entry.consensus_prefix} info={prefixInfo[entry.consensus_prefix]} />
            </span>
          )}
        </div>
      </div>

      <div className="detail-content-columns">
        {/* ── Meanings by PoS ─────────────────────────────────── */}
        <div className="detail-main">
          <div className="detail-section">
            <h3>Meanings</h3>
            {sections.length === 0 ? (
              <p className="empty-cell">No meanings recorded.</p>
            ) : (
              sections.map(pos => (
                <div key={pos} className="pos-section">
                  <div className="pos-section-header">{POS_FULL[pos] || pos || 'Other'}</div>
                  <ol className="pos-meaning-list">
                    {grouped[pos].map((g, i) => (
                      <li key={i} className="pos-meaning-item">{g}</li>
                    ))}
                  </ol>
                </div>
              ))
            )}
          </div>

          {/* ── Inflections ────────────────────────────────────── */}
          {inflPresent.length > 0 && (
            <div className="detail-section">
              <h3>Inflections</h3>
              <div className="infl-list">
                {inflPresent.map(k => {
                  const val = infl[k];
                  if (Array.isArray(val)) {
                    const [base, toned] = val;
                    return (
                      <span key={k} className="infl-item">
                        {base} / {toned} <span className="infl-type">({k})</span>
                      </span>
                    );
                  }
                  return (
                    <span key={k} className="infl-item">
                      {val} <span className="infl-type">({k})</span>
                    </span>
                  );
                })}
              </div>
            </div>
          )}

          {/* ── Case Forms ─────────────────────────────────────── */}
          {entry.case_forms && Object.keys(entry.case_forms).length > 0 && (
            <div className="detail-section">
              <h3>Case Forms</h3>
              <div className="infl-list">
                {entry.case_forms.acc && (
                  <span className="infl-item case-form-acc">
                    {entry.case_forms.acc} <span className="infl-type">(ACC)</span>
                  </span>
                )}
                {entry.case_forms.gen && (
                  <span className="infl-item case-form-gen">
                    {entry.case_forms.gen} <span className="infl-type">(GEN)</span>
                  </span>
                )}
              </div>
            </div>
          )}

          {/* ── Notes ──────────────────────────────────────────── */}
          {entry.notes && (
            <div className="detail-section">
              <h3>Notes</h3>
              <div className="notes-text">{entry.notes}</div>
            </div>
          )}
        </div>

        {/* ── Sidebar: Components, Pattern, Examples ──────────── */}
        <div className="detail-sidebar">
          {entry.components && entry.components.length > 0 && (
            <div className="detail-section">
              <h3>Components</h3>
              <div className="component-list">
                {entry.components.map((c, i) => (
                  <span key={i} className="component-item" onClick={() => onSearchByForm(c.form)} title={"Find '" + c.form + "'"}>
                    {c.form}
                  </span>
                ))}
              </div>
            </div>
          )}

          {entry.pattern && (
            <div className="detail-section">
              <h3>Pattern</h3>
              <div className="pattern-ref">
                <span>{entry.pattern}</span>
                {entry.rule_ref && <span className="infl-rule">{entry.rule_ref}</span>}
              </div>
            </div>
          )}

          {entry.examples && entry.examples.length > 0 && (
            <div className="detail-section">
              <h3>Examples</h3>
              {entry.examples.map((ex, i) => (
                <div key={i} className="example-block">
                  <div className="kilor-text">{ex.kilor}</div>
                  <div className="english-text">{ex.english}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Table Header (unchanged) ────────────────────────────────────────────

const COLGROUP = (
  <colgroup>
    <col style={{ width: '18%' }} />
    <col style={{ width: '42%' }} />
    <col style={{ width: '12%' }} />
    <col style={{ width: '16%' }} />
    <col style={{ width: '6%' }} />
    <col style={{ width: '6%' }} />
  </colgroup>
);

export function TableHeader({ sortCol, sortDir, onSort }) {
  function arrow(col) {
    if (sortCol !== col) return <span className="sort-arrow sort-inactive">↕</span>;
    return <span className="sort-arrow sort-active">{sortDir === 'asc' ? '▲' : '▼'}</span>;
  }

  return (
    <div className="table-header-wrap">
      <table className="word-table word-table-header">
        {COLGROUP}
        <thead>
          <tr>
            <th className={sortCol === 'form' ? 'sorted' : ''} onClick={() => onSort('form')}>
              Word {arrow('form')}
            </th>
            <th className={sortCol === 'gloss' ? 'sorted' : ''} onClick={() => onSort('gloss')}>
              Gloss {arrow('gloss')}
            </th>
            <th className={sortCol === 'type' ? 'sorted' : ''} onClick={() => onSort('type')}>
              Type {arrow('type')}
            </th>
            <th className={sortCol === 'prefix' ? 'sorted' : ''} onClick={() => onSort('prefix')}>
              Prefix {arrow('prefix')}
            </th>
            <th className={sortCol === 'mask' ? 'sorted' : ''} onClick={() => onSort('mask')}>
              NVAD {arrow('mask')}
            </th>
            <th className={sortCol === 'syl' ? 'sorted' : ''} onClick={() => onSort('syl')} style={{ textAlign: 'center' }}>
              Syl {arrow('syl')}
            </th>
          </tr>
        </thead>
      </table>
    </div>
  );
}

// ── Table Body (updated: PoS gloss, trimmed detail, onViewFull prop) ───

export function TableBody({ entries, prefixInfo, onSearchByForm, expandedRow, onToggleExpand, search, keyboardRowIndex, onCopyToast, onViewFull }) {
  const handleCopy = (e, form) => {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(form).then(() => {
        if (onCopyToast) onCopyToast('Copied: ' + form);
      }).catch(() => {});
    }
  };

  if (entries.length === 0) {
    return (
      <div className="no-results">
        <div className="icon">🔍</div>
        <p>No words match.</p>
      </div>
    );
  }

  return (
    <div className="table-body-wrap">
      <table className="word-table word-table-body">
        {COLGROUP}
        <tbody>
          {entries.map((e, i) => {
            const mask = e.derivation_mask
              ? <span className="tag-sm" style={{ background: '#e8f0fe', color: '#1a56db', fontSize: '.7rem', padding: '1px 6px', borderRadius: '10px' }}>{e.derivation_mask}</span>
              : <span className="empty-cell">—</span>;
            const isExpanded = expandedRow === e.id;
            const isKeyboardSelected = keyboardRowIndex === i;
            // Build title for tooltip
            const allGlosses = (e.meanings || []).map(m => (typeof m === 'string' ? m : m.gloss)).join(' / ');
            return (
              <React.Fragment key={e.id}>
                <tr
                  className={(isExpanded ? 'row-expanded' : '') + (isKeyboardSelected ? ' row-keyboard-selected' : '')}
                  onClick={() => onToggleExpand(isExpanded ? null : e.id)}
                >
                  <td className="td-form" title={allGlosses} onClick={(ev) => handleCopy(ev, e.form)}>
                    {highlightMatch(e.form, search)}
                  </td>
                  <td className="td-gloss">
                    <GlossWithPos meanings={e.meanings} search={search} />
                    <ComponentChips components={e.components} onSearchByForm={onSearchByForm} />
                  </td>
                  <td className="td-type"><TypeTag entry={e} /></td>
                  <td className="td-prefix"><PrefixBadge prefix={e.consensus_prefix} info={prefixInfo[e.consensus_prefix]} /></td>
                  <td className="td-mask">{mask}</td>
                  <td className="td-syl">{e.syl_count}</td>
                </tr>
                {isExpanded && (
                  <tr className="detail-tr">
                    <td colSpan={6}>
                      <DetailPanel entry={e} prefixInfo={prefixInfo} onViewFull={onViewFull} />
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function TableView(props) {
  return (
    <>
      <TableHeader sortCol={props.sortCol} sortDir={props.sortDir} onSort={props.onSort} />
      <TableBody
        entries={props.entries}
        prefixInfo={props.prefixInfo}
        onSearchByForm={props.onSearchByForm}
        expandedRow={props.expandedRow}
        onToggleExpand={props.onToggleExpand}
        search={props.search}
        keyboardRowIndex={props.keyboardRowIndex}
        onCopyToast={props.onCopyToast}
        onViewFull={props.onViewFull}
      />
    </>
  );
}