import React from 'react';

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
  const infl = entry.inflections || {};
  const inflOrder = ['noun', 'verb', 'adjective', 'adverb'];
  const inflPresent = inflOrder.filter(k => infl[k]);
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

          {entry.consensus_prefix && (
            <div className="detail-row">
              <strong>Prefix</strong> {entry.consensus_prefix}
              {prefixInfo[entry.consensus_prefix]
                ? ` (${prefixInfo[entry.consensus_prefix].cls} · ${prefixInfo[entry.consensus_prefix].emotion})`
                : ''}
            </div>
          )}

           <div className="detail-row">
             <strong>Syllables</strong> {entry.syl_count}{entry.syllables ? ` (${entry.syllables})` : ''}
           </div>

          {entry.ipa && (
            <div className="detail-row">
              <strong>IPA</strong> <span className="ipa-text">/{entry.ipa}/</span>
            </div>
          )}
        </div>

        <div className="detail-col">
          {inflPresent.length > 0 && (
            <div className="detail-row">
              <strong>Inflections</strong>
              <div className="infl-list">
                {inflPresent.map(k => {
                  const val = infl[k];
                  // Single-mask words have array [base, tonemarked]
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

export function TableBody({ entries, prefixInfo, onSearchByForm, expandedRow, onToggleExpand, search, keyboardRowIndex, onCopyToast }) {
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
            const gloss = e.meanings[0] || '';
            const mask = e.derivation_mask
              ? <span className="tag-sm" style={{ background: '#e8f0fe', color: '#1a56db', fontSize: '.7rem', padding: '1px 6px', borderRadius: '10px' }}>{e.derivation_mask}</span>
              : <span className="empty-cell">—</span>;
            const isExpanded = expandedRow === e.id;
            const isKeyboardSelected = keyboardRowIndex === i;
            return (
              <React.Fragment key={e.id}>
                <tr
                  className={(isExpanded ? 'row-expanded' : '') + (isKeyboardSelected ? ' row-keyboard-selected' : '')}
                  onClick={() => onToggleExpand(isExpanded ? null : e.id)}
                >
                  <td className="td-form" title={e.meanings.join(' / ')} onClick={(ev) => handleCopy(ev, e.form)}>
                    {highlightMatch(e.form, search)}
                  </td>
                  <td className="td-gloss">
                    {highlightMatch(gloss, search)}
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
      />
    </>
  );
}