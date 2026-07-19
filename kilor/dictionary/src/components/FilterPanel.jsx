import { useState } from 'react';

const SECTION_OPTIONS = [
  { value: 'A', label: 'A — Worlds & Elements' },
  { value: 'B', label: 'B — Living Things' },
  { value: 'C', label: 'C — Physical Objects' },
  { value: 'D', label: 'D — Actions & Motion' },
  { value: 'E', label: 'E — Qualities & States' },
  { value: 'F', label: 'F — Mind & Emotion' },
  { value: 'G', label: 'G — Time & Space' },
  { value: 'H', label: 'H — Social & Relational' },
  { value: 'I', label: 'I — Abstract' },
  { value: 'J', label: 'J — Sensation' },
];

const TYPE_OPTIONS = [
  { value: 'root', label: 'Roots' },
  { value: 'compound', label: 'Compounds' },
  { value: 'function', label: 'Function words' },
];

const MASK_OPTIONS = [
  { value: 'N', label: 'N' },
  { value: 'V', label: 'V' },
  { value: 'A', label: 'Adj' },
  { value: 'D', label: 'Adv' },
];

function CheckboxRow({ checked, onChange, children }) {
  return (
    <label className="filter-checkbox-row">
      <input type="checkbox" checked={checked} onChange={onChange} />
      {children}
    </label>
  );
}

export default function FilterPanel({
  prefixInfo,
  filterPrefixes, onFilterPrefixesChange,
  filterSections, onFilterSectionsChange,
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

        {/* Column: Section */}
        <div className="filter-section">
          <h4>Section</h4>
          {SECTION_OPTIONS.map(opt => (
            <CheckboxRow
              key={opt.value}
              checked={filterSections.includes(opt.value)}
              onChange={() => toggleInList(filterSections, onFilterSectionsChange, opt.value)}
            >
              {opt.label}
            </CheckboxRow>
          ))}
        </div>

        {/* Column: Type */}
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
        </div>

        {/* Column: NVAD Mask + Syllable Range */}
        <div className="filter-section">
          <h4>
            NVAD Mask
            <span className="mask-info-icon" title="Derivation masks — each word can function as Noun, Verb, Adjective, and/or Adverb. Check a box to show words that can function in that role.">
              ℹ
            </span>
          </h4>
          <div className="mask-grid" data-testid="mask-grid">
            {MASK_OPTIONS.map(opt => (
              <label key={opt.value} className="filter-checkbox-row" data-mask={opt.value}>
                <input type="checkbox" checked={filterMasks.includes(opt.value)} onChange={() => toggleInList(filterMasks, onFilterMasksChange, opt.value)} />
                {opt.label}
              </label>
            ))}
          </div>

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