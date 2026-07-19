import React from 'react';

const SECTION_LABELS = { A:'Worlds & Elements', B:'Living Things', C:'Physical Objects', D:'Actions & Motion', E:'Qualities & States', F:'Mind & Emotion', G:'Time & Space', H:'Social & Relational', I:'Abstract', J:'Sensation' };

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
      <br />
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

function DetailPanel({ entry, prefixInfo }) {
  const inflKeys = Object.keys(entry.inflections);
  const mask = entry.derivation_mask || '';

  return (
    <div className="detail-panel">
      <div className="detail-columns">
        <div className="detail-col">
          <div className="detail-row">
            <strong>Meanings</strong>
            <ul className="detail-meaning-list">
              {entry.meanings.map((m, i) => <li key={i}>{m}</li>)}
            </ul>
          </div>

          {mask && (
            <div className="detail-row">
              <strong>NVAD Mask</strong> <span className="tag-mask">{mask}</span>
            </div>
          )}

          <div className="detail-row">
            <strong>Section</strong> {entry.section || '—'} — {SECTION_LABELS[entry.section] || 'Other'}
          </div>

          {entry.consensus_prefix && (
            <div className="detail-row">
              <strong>Prefix</strong> {entry.consensus_prefix}
              {prefixInfo[entry.consensus_prefix]
                ? ` (${prefixInfo[entry.consensus_prefix].cls} · ${prefixInfo[entry.consensus_prefix].emotion})`
                : ''}
            </div>
          )}

          <div className="detail-row">
            <strong>Syllables</strong> {entry.syl_count}
          </div>
        </div>

        <div className="detail-col">
          {inflKeys.length > 0 && (
            <div className="detail-row">
              <strong>Inflections</strong>
              <div className="infl-list">
                {inflKeys.map(ft => (
                  <span key={ft} className="infl-item">
                    {entry.inflections[ft]} <span className="infl-type">({ft})</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {entry.case_forms && Object.keys(entry.case_forms).length > 0 && (
            <div className="detail-row">
              <strong>Case Forms</strong>
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

          {entry.components && entry.components.length > 0 && (
            <div className="detail-row">
              <strong>Components</strong>
              <div className="component-list">
                {entry.components.map((c, i) => (
                  <span key={i} className="component-item">{c.form}</span>
                ))}
              </div>
            </div>
          )}

          {entry.pattern && (
            <div className="detail-row">
              <strong>Pattern</strong>
              <div className="pattern-ref">
                <span>{entry.pattern}</span>
                {entry.rule_ref && <span className="infl-rule">{entry.rule_ref}</span>}
              </div>
            </div>
          )}

          {entry.notes && (
            <div className="detail-row">
              <strong>Notes</strong> {entry.notes}
            </div>
          )}

          {entry.examples && entry.examples.length > 0 && (
            <div className="detail-row">
              <strong>Examples</strong>
              {entry.examples.map((ex, i) => (
                <div key={i} className="example-block">
                  <span className="kilor-text">{ex.kilor}</span>
                  <span className="english-text">{ex.english}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TableView({ entries, sortCol, sortDir, onSort, prefixInfo, onSearchByForm, expandedRow, onToggleExpand }) {
  function arrow(col) {
    if (sortCol !== col) return <span className="sort-arrow">▲</span>;
    return <span className="sort-arrow">{sortDir === 'asc' ? '▲' : '▼'}</span>;
  }

  if (entries.length === 0) {
    return (
      <div className="no-results">
        <div className="icon">🔍</div>
        <p>No words match.</p>
      </div>
    );
  }

  return (
    <div className="table-wrap">
      <table className="word-table">
        <thead>
          <tr>
            <th className={sortCol === 'form' ? 'sorted' : ''} onClick={() => onSort('form')}>
              Word {arrow('form')}
            </th>
            <th className={sortCol === 'gloss' ? 'sorted' : ''} onClick={() => onSort('gloss')}>
              Gloss {arrow('gloss')}
            </th>
            <th className={sortCol === 'section' ? 'sorted' : ''} onClick={() => onSort('section')}>
              § {arrow('section')}
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
        <tbody>
          {entries.map(e => {
            const gloss = e.meanings[0] || '';
            const mask = e.derivation_mask
              ? <span className="tag-sm" style={{ background: '#e8f0fe', color: '#1a56db', fontSize: '.7rem', padding: '1px 6px', borderRadius: '10px' }}>{e.derivation_mask}</span>
              : <span className="empty-cell">—</span>;
            const isExpanded = expandedRow === e.id;
            return (
              <React.Fragment key={e.id}>
                <tr
                  className={isExpanded ? 'row-expanded' : ''}
                  onClick={() => onToggleExpand(isExpanded ? null : e.id)}
                >
                  <td className="td-form" title={e.meanings.join(' / ')}>{e.form}</td>
                  <td className="td-gloss">
                    {gloss}
                    <ComponentChips components={e.components} onSearchByForm={onSearchByForm} />
                  </td>
                  <td className="td-section">{e.section || '—'}</td>
                  <td className="td-type"><TypeTag entry={e} /></td>
                  <td className="td-prefix"><PrefixBadge prefix={e.consensus_prefix} info={prefixInfo[e.consensus_prefix]} /></td>
                  <td className="td-mask">{mask}</td>
                  <td className="td-syl">{e.syl_count}</td>
                </tr>
                {isExpanded && (
                  <tr className="detail-tr">
                    <td colSpan={7}>
                      <DetailPanel entry={e} prefixInfo={prefixInfo} />
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