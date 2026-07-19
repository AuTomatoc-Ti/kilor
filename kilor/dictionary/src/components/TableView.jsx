const SECTION_LABELS = { A:'Worlds & Elements', B:'Living Things', C:'Physical Objects', D:'Actions & Motion', E:'Qualities & States', F:'Mind & Emotion', G:'Time & Space', H:'Social & Relational', I:'Abstract', J:'Sensation' };

function PrefixBadge({ prefix, info }) {
  if (!prefix || prefix === 'o-' || prefix === '' || prefix === '-') return <span className="empty-cell">—</span>;
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

export default function TableView({ entries, sortCol, sortDir, onSort, prefixInfo, onSearchByForm }) {
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
            return (
              <tr key={e.id}>
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
            );
          })}
        </tbody>
      </table>
    </div>
  );
}