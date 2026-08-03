import React, { useState } from 'react';

const MASK_LABELS = { N: 'Noun', V: 'Verb', A: 'Adjective', D: 'Adverb' };

/** Inline PoS tags (table row gloss column) — minimized abbreviations. */
const POS_INLINE = {
  N: 'N', V: 'V', A: 'A', D: 'D',
  PRON: 'PRON', NUM: 'NUM',
  DET: 'DET',
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
  DET: 'Determiner',
  CCONJ: 'Coordinating Conjunction', SCONJ: 'Subordinating Conjunction',
  ADP: 'Adposition', PART: 'Particle', MODAL: 'Modal Verb',
  DEM: 'Demonstrative', Q: 'Question Word',
  CLF: 'Classifier / Measure Word', INTERJ: 'Interjection', PROPN: 'Proper Noun',
  '': 'Other',
};

const PREFIX_LEGEND = [
  { prefix: 'a-',  cls: 'Alive / Energy',    emotion: 'Anger',   color: '#ef4444' },
  { prefix: 'e-',  cls: 'Crafted / Tool',    emotion: 'Joy',     color: '#f59e0b' },
  { prefix: 'i-',  cls: 'Fluid / Vast',      emotion: 'Sadness', color: '#3b82f6' },
  { prefix: 'o-',  cls: 'Abstract / Void',   emotion: 'Surprise',color: '#d2d2d2' },
  { prefix: 'u-',  cls: 'Organic / Growth',  emotion: 'Calm',    color: '#22c55e' },
  { prefix: 'y-',  cls: 'Dense / Mass',      emotion: 'Fear',    color: '#6b7280' },
  { prefix: 'ae-', cls: 'Earth / Boundary',  emotion: 'Disgust', color: '#a16207' },
];

/** Play audio for a word by its ID using a persistent audio element to
 *  avoid browser autoplay-policy issues with repeatedly-created Audio objects. */
function handlePronounce(e, wordId) {
  e.stopPropagation();
  const player = document.getElementById('audio-player');
  if (!player) return;
  player.src = `./audio/${wordId}.ogg`;
  player.load();
  const promise = player.play();
  if (promise) promise.catch(() => {});
}

/** Speaker icon used as pronounce button in multiple locations. */
function PronounceButton({ wordId, className }) {
  return (
    <span
      className={className || 'pronounce-btn'}
      onClick={(e) => handlePronounce(e, wordId)}
      title="Listen to pronunciation"
    >
      🔊
    </span>
  );
}

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
  const badges = [];
  // Structural badge
  if (entry.is_compound) {
    badges.push(<span key="struct" className="tag-sm tag-compound">{entry.compound_type || '?'}-cmpd</span>);
  } else if (entry.is_root) {
    badges.push(<span key="struct" className="tag-sm tag-root">root</span>);
  }
  // Grammar badge (independent of structural)
  if (entry.is_grammar) {
    badges.push(<span key="grammar" className="tag-sm tag-function">grammar</span>);
  }
  if (badges.length === 0) return null;
  return <>{badges}</>;
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

  const items = typeof meanings[0] === 'string'
    ? meanings.map((g, i) => ({ gloss: g, pos: '' }))
    : meanings;

  if (items.length === 1 && !items[0].pos) {
    return highlightMatch(items[0].gloss, search);
  }

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

/** Colour Prefix Legend — modal popup triggered by a "?" icon in table header. */
function PrefixLegend() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <span
        className="prefix-legend-trigger"
        onClick={(e) => { e.stopPropagation(); setOpen(true); }}
        title="Colour prefix legend"
      >
        ?
      </span>
      {open && (
        <div className="prefix-legend-overlay" onClick={() => setOpen(false)}>
          <div className="prefix-legend-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Colour Prefix Legend</h3>
            <div className="prefix-legend-grid">
              {PREFIX_LEGEND.map((p) => (
                <div key={p.prefix} className="prefix-legend-row">
                  <span className="prefix-legend-swatch" style={{ background: p.color }}></span>
                  <span className="prefix-legend-label"><strong>{p.prefix}</strong></span>
                  <span className="prefix-legend-cls">{p.cls}</span>
                  <span className="prefix-legend-emotion">({p.emotion})</span>
                </div>
              ))}
            </div>
            <p className="prefix-legend-note">
              The colour prefix is part of the word's identity, encoding its ontological class and associated emotion.
              {" "}See <em>rules/1-nominals/nouns-colour-prefix.md</em>.
            </p>
            <button className="prefix-legend-close" onClick={() => setOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </>
  );
}

/** Trimmed inline preview — form, IPA, prefix, mask, quick gloss view + link to full entry. */
function DetailPanel({ entry, prefixInfo, onViewFull, showAudio }) {
  const mask = entry.pos_mask || entry.derivation_mask || '';
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
              <strong>IPA</strong> {showAudio && <PronounceButton wordId={entry.id} className="pronounce-btn pronounce-btn-inline" />} <span className="ipa-text">/{entry.ipa}/</span>
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

export function WordDetailPage({ entry, prefixInfo, onBack, onSearchByForm, onCopyToast, showAudio }) {
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

  const grouped = {};
  for (const m of meanings) {
    const gl = typeof m === 'string' ? m : m.gloss;
    const p = typeof m === 'string' ? '' : (m.pos || '');
    if (!grouped[p]) grouped[p] = [];
    grouped[p].push(gl);
  }

  const posOrder = ['N', 'V', 'A', 'D'];
  const extraOrder = Object.keys(grouped).filter(p => p && !posOrder.includes(p));
  const sections = [...posOrder.filter(p => grouped[p]), ...extraOrder];

  const infl = entry.inflections || {};
  const inflOrder = ['noun', 'verb', 'adjective', 'adverb'];
  const inflPresent = inflOrder.filter(k => infl[k]);

  return (
    <div className="word-detail-page">
      <div className="detail-header">
        <button className="back-button" onClick={onBack}>← Back to dictionary</button>
      </div>

      <div className="detail-identity-card">
        <div className="detail-word-row">
          <h2 className="detail-word-form">{entry.form}</h2>
          <span className="detail-word-badges">
            <TypeTag entry={entry} />
            {mask && <span className="tag-mask">{mask}</span>}
          </span>
        </div>
        <div className="detail-word-meta">
          {showAudio && <PronounceButton wordId={entry.id} className="pronounce-btn pronounce-btn-detail" />}
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

          {entry.notes && (
            <div className="detail-section">
              <h3>Notes</h3>
              <div className="notes-text">{entry.notes}</div>
            </div>
          )}
        </div>

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

// ── Table Header ─────────────────────────────────────────────────────────

/** Build colgroup widths depending on whether the Modified column is shown.
 *  7 columns: Word | IPA | Gloss | Type | Prefix | Syl | Modified
 */
function buildColGroup(showModified) {
  if (showModified) {
    return (
      <colgroup>
        <col style={{ width: '15%' }} />
        <col style={{ width: '10%' }} />
        <col style={{ width: '27%' }} />
        <col style={{ width: '11%' }} />
        <col style={{ width: '15%' }} />
        <col style={{ width: '7%' }} />
        <col style={{ width: '15%' }} />
      </colgroup>
    );
  }
  return (
    <colgroup>
      <col style={{ width: '17%' }} />
      <col style={{ width: '11%' }} />
      <col style={{ width: '33%' }} />
      <col style={{ width: '13%' }} />
      <col style={{ width: '17%' }} />
      <col style={{ width: '9%' }} />
    </colgroup>
  );
}

export function TableHeader({ sortCol, sortDir, onSort, showModified }) {
  function arrow(col) {
    if (sortCol !== col) return <span className="sort-arrow sort-inactive">↕</span>;
    return <span className="sort-arrow sort-active">{sortDir === 'asc' ? '▲' : '▼'}</span>;
  }

  return (
    <div className="table-header-wrap">
      <table className="word-table word-table-header">
        {buildColGroup(showModified)}
        <thead>
          <tr>
            <th className={sortCol === 'form' ? 'sorted' : ''} onClick={() => onSort('form')}>
              Word {arrow('form')}
            </th>
            <th className={sortCol === 'form' ? 'sorted' : ''} onClick={() => onSort('form')}>
              IPA {arrow('form')}
            </th>
            <th className={sortCol === 'gloss' ? 'sorted' : ''} onClick={() => onSort('gloss')}>
              Gloss {arrow('gloss')}
            </th>
            <th className={sortCol === 'type' ? 'sorted' : ''} onClick={() => onSort('type')}>
              Type {arrow('type')}
            </th>
            <th className={sortCol === 'prefix' ? 'sorted' : ''} onClick={() => onSort('prefix')}>
              Prefix <PrefixLegend /> {arrow('prefix')}
            </th>
            <th className={sortCol === 'syl' ? 'sorted' : ''} onClick={() => onSort('syl')} style={{ textAlign: 'center' }}>
              Syl {arrow('syl')}
            </th>
            {showModified && (
              <th className={sortCol === 'updated' ? 'sorted' : ''} onClick={() => onSort('updated')}>
                Modified {arrow('updated')}
              </th>
            )}
          </tr>
        </thead>
      </table>
    </div>
  );
}

// ── Pagination Controls ──────────────────────────────────────────────────

function PaginationBar({ page, totalPages, totalCount, pageSize, onPageChange }) {
  if (totalPages <= 1) return null;

  const startItem = (page - 1) * pageSize + 1;
  const endItem = Math.min(page * pageSize, totalCount);

  return (
    <div className="pagination-bar">
      <span className="pagination-info">
        {startItem}–{endItem} of {totalCount}
      </span>
      <button
        className="pagination-btn"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
      >
        ← Previous
      </button>
      <span className="pagination-page">
        Page {page} of {totalPages}
      </span>
      <button
        className="pagination-btn"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Next →
      </button>
    </div>
  );
}

// ── Last Modified formatter ──────────────────────────────────────────────

function formatUpdatedAt(updated_at) {
  if (!updated_at) return '—';
  // updated_at is an ISO string like "2026-07-27T22:30:00.000Z" or "2026-07-27 22:30:00"
  try {
    const d = new Date(updated_at.replace(' ', 'T') + (updated_at.includes('Z') ? '' : 'Z'));
    if (isNaN(d.getTime())) return updated_at.slice(0, 10);
    // Show as YYYY-MM-DD HH:MM
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const min = String(d.getMinutes()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
  } catch (_e) {
    return updated_at.slice(0, 10);
  }
}

// ── Table Body ────────────────────────────────────────────────────────────

const PAGE_SIZE = 50;

export function TableBody({ entries, prefixInfo, onSearchByForm, expandedRow, onToggleExpand, search, keyboardRowIndex, onCopyToast, onViewFull, page, totalPages, totalCount, onPageChange, showAudio, showModified }) {
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

  const colSpan = showModified ? 7 : 6;

  return (
    <>
      <div className="table-body-wrap">
        <table className="word-table word-table-body">
          {buildColGroup(showModified)}
          <tbody>
            {entries.map((e, i) => {
              const isExpanded = expandedRow === e.id;
              const isKeyboardSelected = keyboardRowIndex === i;
              const allGlosses = (e.meanings || []).map(m => (typeof m === 'string' ? m : m.gloss)).join(' / ');
              return (
                <React.Fragment key={e.id}>
                  <tr
                    className={(isExpanded ? 'row-expanded' : '') + (isKeyboardSelected ? ' row-keyboard-selected' : '')}
                    onClick={() => onToggleExpand(isExpanded ? null : e.id)}
                  >
                    <td className="td-form" title={allGlosses}>
                      <span className="td-form-text" onClick={(ev) => handleCopy(ev, e.form)}>
                        {highlightMatch(e.form, search)}
                      </span>
                    </td>
                    <td className="td-ipa" title={e.ipa}>
                      {showAudio && <PronounceButton wordId={e.id} />}
                      <span className="ipa-text">/{e.ipa}/</span>
                    </td>
                    <td className="td-gloss">
                      <GlossWithPos meanings={e.meanings} search={search} />
                      <ComponentChips components={e.components} onSearchByForm={onSearchByForm} />
                    </td>
                    <td className="td-type"><TypeTag entry={e} /></td>
                    <td className="td-prefix"><PrefixBadge prefix={e.consensus_prefix} info={prefixInfo[e.consensus_prefix]} /></td>
                    <td className="td-syl">{e.syl_count}</td>
                    {showModified && <td className="td-modified">{formatUpdatedAt(e.updated_at)}</td>}
                  </tr>
                  {isExpanded && (
                    <tr className="detail-tr">
                      <td colSpan={colSpan}>
                        <DetailPanel entry={e} prefixInfo={prefixInfo} onViewFull={onViewFull} showAudio={showAudio} />
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      <PaginationBar
        page={page}
        totalPages={totalPages}
        totalCount={totalCount}
        pageSize={PAGE_SIZE}
        onPageChange={onPageChange}
      />
    </>
  );
}

export default function TableView(props) {
  return (
    <>
      <TableHeader sortCol={props.sortCol} sortDir={props.sortDir} onSort={props.onSort} showModified={props.showModified} />
      <TableBody
        entries={props.entries}
        showAudio={props.showAudio}
        prefixInfo={props.prefixInfo}
        onSearchByForm={props.onSearchByForm}
        expandedRow={props.expandedRow}
        onToggleExpand={props.onToggleExpand}
        search={props.search}
        keyboardRowIndex={props.keyboardRowIndex}
        onCopyToast={props.onCopyToast}
        onViewFull={props.onViewFull}
        page={props.page}
        totalPages={props.totalPages}
        totalCount={props.totalCount}
        onPageChange={props.onPageChange}
        showModified={props.showModified}
      />
    </>
  );
}