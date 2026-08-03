import { useState } from 'react';

const TYPE_OPTIONS = [
  { value: 'root', label: 'Roots' },
  { value: 'compound', label: 'Compounds' },
];

const POS_CONTENT = [
  { value: 'N', label: 'Noun' },
  { value: 'V', label: 'Verb' },
  { value: 'A', label: 'Adjective' },
  { value: 'D', label: 'Adverb' },
  { value: 'MODAL', label: 'Modal Verb' },
  { value: 'PROPN', label: 'Proper Noun' },
];

const POS_GRAMMAR = [
  { value: 'PRON', label: 'Pronoun' },
  { value: 'PART', label: 'Particle' },
  { value: 'NUM', label: 'Numeral' },
  { value: 'ADP', label: 'Adposition' },
  { value: 'DET', label: 'Determiner' },
  { value: 'DEM', label: 'Demonstrative' },
  { value: 'CCONJ', label: 'Coord Conj' },
  { value: 'SCONJ', label: 'Subord Conj' },
  { value: 'Q', label: 'Question Word' },
  { value: 'CLF', label: 'Classifier' },
  { value: 'INTERJ', label: 'Interjection' },
];

/** Full descriptions for the POS legend modal. */
const POS_LEGEND = [
  { tag: 'N',     desc: 'Person, place, thing, concept' },
  { tag: 'V',     desc: 'Action, event, state' },
  { tag: 'A',     desc: 'Quality, property' },
  { tag: 'D',     desc: 'Manner, degree' },
  { tag: 'MODAL', desc: 'Ability, obligation, possibility' },
  { tag: 'PROPN', desc: 'Name of person, place' },
  { tag: 'PRON',  desc: 'Personal, demonstrative pronouns' },
  { tag: 'NUM',   desc: 'Cardinal numbers' },
  { tag: 'DET',   desc: 'Articles, quantifiers' },
  { tag: 'CCONJ', desc: 'and, but, or' },
  { tag: 'SCONJ', desc: 'because, if, when' },
  { tag: 'ADP',   desc: 'Preposition / postposition' },
  { tag: 'PART',  desc: 'Negation, interrogative, emphasis' },
  { tag: 'DEM',   desc: 'this, that' },
  { tag: 'Q',     desc: 'who, what, where, when' },
  { tag: 'CLF',   desc: 'Measure word / counter' },
  { tag: 'INTERJ',desc: 'Exclamation, response particle' },
];

function CheckboxRow({ checked, onChange, children }) {
  return (
    <label className="filter-checkbox-row">
      <input type="checkbox" checked={checked} onChange={onChange} />
      {children}
    </label>
  );
}

/** POS Legend modal — triggered by ℹ icon in POS header. */
function POSLegend() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <span
        className="prefix-legend-trigger"
        onClick={(e) => { e.stopPropagation(); setOpen(true); }}
        title="Part-of-speech legend"
      >
        ?
      </span>
      {open && (
        <div className="prefix-legend-overlay" onClick={() => setOpen(false)}>
          <div className="prefix-legend-modal pos-legend-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Part of Speech Legend</h3>
            <div className="pos-legend-grid">
              {POS_LEGEND.map((p) => (
                <div key={p.tag} className="pos-legend-row">
                  <span className="pos-legend-tag">{p.tag}</span>
                  <span className="pos-legend-desc">{p.desc}</span>
                </div>
              ))}
            </div>
            <p className="prefix-legend-note">
              POS tags are stored per-meaning. Filtering by a tag shows words that have at least one meaning with that tag.
            </p>
            <button className="prefix-legend-close" onClick={() => setOpen(false)}>Close</button>
          </div>
        </div>
      )}
    </>
  );
}

export default function FilterPanel({
  prefixInfo,
  filterPrefixes, onFilterPrefixesChange,
  filterTypes, onFilterTypesChange,
  filterMasks, onFilterMasksChange,
  sylMin, onSylMinChange,
  sylMax, onSylMaxChange,
  onResetFilters,
}) {
  const allPrefixKeys = Object.keys(prefixInfo);

  function toggleInList(list, onChange, value) {
    if (list.includes(value)) {
      onChange(list.filter(v => v !== value));
    } else {
      onChange([...list, value]);
    }
  }

  return (
    <div className="filter-panel">
      <div className="filter-columns">
        {/* Column: Colour Prefix */}
        <div className="filter-section">
          <h4>Colour Prefix</h4>
          {allPrefixKeys.map(key => {
            const info = prefixInfo[key];
            return (
              <CheckboxRow
                key={key}
                checked={filterPrefixes.includes(key)}
                onChange={() => toggleInList(filterPrefixes, onFilterPrefixesChange, key)}
              >
                <span className="legend-swatch" style={{ background: info.color }}></span>
                <b>{key}</b> <span className="filter-hint">{info.cls}</span>
              </CheckboxRow>
            );
          })}
          <CheckboxRow
            key="NONE"
            checked={filterPrefixes.includes('NONE')}
            onChange={() => toggleInList(filterPrefixes, onFilterPrefixesChange, 'NONE')}
          >
            <span className="legend-swatch none-swatch"></span>
            <b>(none)</b> <span className="filter-hint">No prefix</span>
          </CheckboxRow>
        </div>

        {/* Column: Part of Speech */}
        <div className="filter-section">
          <h4>
            Part of Speech
            <POSLegend />
          </h4>
          <div className="pos-grid">
            {/* Content section */}
            <label className="pos-toggle-all">
              <input
                type="checkbox"
                checked={POS_CONTENT.every(opt => filterMasks.includes(opt.value))}
                onChange={() => {
                  const allTags = POS_CONTENT.map(opt => opt.value);
                  const allChecked = allTags.every(t => filterMasks.includes(t));
                  if (allChecked) {
                    onFilterMasksChange(filterMasks.filter(m => !allTags.includes(m)));
                  } else {
                    onFilterMasksChange([...new Set([...filterMasks, ...allTags])]);
                  }
                }}
              />
              All Content
            </label>
            <div className="pos-section-label">▸ Content</div>
            <div className="pos-grid-row">
              {POS_CONTENT.slice(0, 3).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>
            <div className="pos-grid-row">
              {POS_CONTENT.slice(3, 6).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>

            {/* Grammar section */}
            <label className="pos-toggle-all" style={{ marginTop: 4 }}>
              <input
                type="checkbox"
                checked={POS_GRAMMAR.every(opt => filterMasks.includes(opt.value))}
                onChange={() => {
                  const allTags = POS_GRAMMAR.map(opt => opt.value);
                  const allChecked = allTags.every(t => filterMasks.includes(t));
                  if (allChecked) {
                    onFilterMasksChange(filterMasks.filter(m => !allTags.includes(m)));
                  } else {
                    onFilterMasksChange([...new Set([...filterMasks, ...allTags])]);
                  }
                }}
              />
              All Grammar
            </label>
            <div className="pos-section-label" style={{ marginTop: 6 }}>▸ Grammar</div>
            <div className="pos-grid-row">
              {POS_GRAMMAR.slice(0, 3).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>
            <div className="pos-grid-row">
              {POS_GRAMMAR.slice(3, 6).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>
            <div className="pos-grid-row">
              {POS_GRAMMAR.slice(6, 9).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>
            <div className="pos-grid-row">
              {POS_GRAMMAR.slice(9, 11).map(opt => (
                <CheckboxRow
                  key={opt.value}
                  checked={filterMasks.includes(opt.value)}
                  onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)}
                >
                  <b>{opt.value}</b> <span className="filter-hint">{opt.label}</span>
                </CheckboxRow>
              ))}
            </div>
          </div>
        </div>

        {/* Column: Word Type + Syllable Range */}
        <div className="filter-section">
          <h4>Word Type</h4>
          {TYPE_OPTIONS.map(opt => (
            <CheckboxRow
              key={opt.value}
              checked={filterTypes.includes(opt.value)}
              onChange={() => toggleInList(filterTypes, onFilterTypesChange, opt.value)}
            >
              {opt.label}
            </CheckboxRow>
          ))}

          <h4 style={{ marginTop: 12 }}>Syllable Range</h4>
          <div className="syl-range-row">
            <label>
              Min:&nbsp;
              <input
                type="number"
                className="syl-input"
                min={1}
                max={10}
                value={sylMin}
                onChange={e => onSylMinChange(Math.max(1, Math.min(10, parseInt(e.target.value) || 1)))}
              />
            </label>
            <label>
              Max:&nbsp;
              <input
                type="number"
                className="syl-input"
                min={1}
                max={10}
                value={sylMax}
                onChange={e => onSylMaxChange(Math.max(1, Math.min(10, parseInt(e.target.value) || 10)))}
              />
            </label>
          </div>
        </div>
      </div>
      <div className="filter-footer">
        <span className="filter-reset-btn" onClick={onResetFilters}>
          Reset filters
        </span>
      </div>
    </div>
  );
}