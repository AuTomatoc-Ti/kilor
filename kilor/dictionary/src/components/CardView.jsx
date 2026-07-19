import { useState } from 'react';

const SECTION_LABELS = { A:'Worlds & Elements', B:'Living Things', C:'Physical Objects', D:'Actions & Motion', E:'Qualities & States', F:'Mind & Emotion', G:'Time & Space', H:'Social & Relational', I:'Abstract', J:'Sensation' };
const SEC_ORDER = ['A','B','C','D','E','F','G','H','I','J','-'];

function EntryCard({ entry, prefixInfo, onSearchByForm }) {
  const [open, setOpen] = useState(false);

  const tags = [];
  tags.push(
    <span className="tag tag-mask" key="mask">{entry.derivation_mask || 'closed-class'}</span>
  );
  if (entry.is_function_word) tags.push(<span className="tag tag-function" key="func">function</span>);
  else if (entry.is_compound) tags.push(<span className="tag tag-compound" key="cmpd">{entry.compound_type}-compound</span>);
  else if (entry.is_root) tags.push(<span className="tag tag-root" key="root">root</span>);

  const inflKeys = Object.keys(entry.inflections);
  const isShortRoot = entry.is_root && !entry.is_function_word && entry.syl_count <= 2;
  let detail = (
    <>
      {inflKeys.length > 0 && (
        <div className="detail-row">
          <strong>Inflections:</strong>
          <span className="infl-list">
            {Object.entries(entry.inflections).map(([type, form]) => {
              const rule = (isShortRoot && (type === 'adjective' || type === 'adverb'))
                ? <span className="infl-rule"> (root + -s)</span>
                : null;
              return (
                <span className="infl-item" key={type}>
                  <span className="infl-type">{type}</span> {form}{rule}
                </span>
              );
            })}
          </span>
        </div>
      )}
      {entry.components.length > 0 && (
        <div className="detail-row">
          <strong>Components:</strong>
          <span className="component-list">
            {entry.components.map((comp, i) => {
              const name = typeof comp === 'string' ? comp : comp.form;
              return (
                <span className="component-item" key={i}>
                  <a href="#" onClick={e => { e.preventDefault(); onSearchByForm(name); }}>{name}</a>
                </span>
              );
            })}
          </span>
        </div>
      )}
      {entry.consensus_prefix && entry.consensus_prefix !== 'o-' && (() => {
        const pi = prefixInfo[entry.consensus_prefix];
        return (
          <div className="detail-row">
            <strong>Prefix:</strong>{' '}
            <span className="prefix-badge" style={{ background: pi ? pi.color : '#888' }}>
              <span className="prefix-swatch"></span>
              {entry.consensus_prefix} — {pi ? pi.cls + ' · ' + pi.emotion : ''}
            </span>
          </div>
        );
      })()}
      {entry.pattern && (
        <div className="detail-row">
          <strong>Pattern:</strong>
          <span className="pattern-ref"><span>{entry.pattern}</span></span>
        </div>
      )}
      <div className="detail-row"><strong>Syllables:</strong> {entry.syl_count}</div>
      {entry.notes && <div className="detail-row"><strong>Notes:</strong> {entry.notes}</div>}
      {entry.examples.length > 0 && (
        <div style={{ marginTop: 10 }}>
          <strong style={{ color: '#555' }}>Examples:</strong>
          {entry.examples.map((ex, i) => (
            <div className="example-block" key={i}>
              <span className="kilor-text">{ex.kilor}</span>
              <span className="english-text">— {ex.english}</span>
            </div>
          ))}
        </div>
      )}
    </>
  );

  return (
    <div className={'entry' + (open ? ' open' : '')}>
      <div className="entry-header" onClick={() => setOpen(o => !o)}>
        <span className="word">{entry.form}</span>
        <span className="meanings">— {entry.meanings.join(' / ')}</span>
        <span className="meta-tags">{tags}</span>
      </div>
      <div className="entry-body">{detail}</div>
    </div>
  );
}

export default function CardView({ entries, prefixInfo, onSearchByForm }) {
  if (entries.length === 0) {
    return (
      <div className="no-results">
        <div className="icon">🔍</div>
        <p>No words match.</p>
      </div>
    );
  }

  const grouped = {};
  SEC_ORDER.forEach(sec => { grouped[sec] = []; });
  entries.forEach(e => { const sec = e.section || '-'; if (!grouped[sec]) grouped[sec] = []; grouped[sec].push(e); });

  return (
    <div className="card-container">
      {SEC_ORDER.map(sec => {
        if (!grouped[sec] || grouped[sec].length === 0) return null;
        return (
          <div key={sec}>
            <div className="section-header">
              {sec} — {SECTION_LABELS[sec] || 'Other'}
              <span className="count">{grouped[sec].length}</span>
            </div>
            {grouped[sec].map(e => (
              <EntryCard key={e.id} entry={e} prefixInfo={prefixInfo} onSearchByForm={onSearchByForm} />
            ))}
          </div>
        );
      })}
    </div>
  );
}