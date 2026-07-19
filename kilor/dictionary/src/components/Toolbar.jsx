import { useState, useRef, useEffect } from 'react';

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
  { value: 'A', label: 'A' },
  { value: 'D', label: 'D' },
  { value: 'NA', label: 'NA' },
  { value: 'NV', label: 'NV' },
  { value: 'NAD', label: 'NAD' },
  { value: 'NVA', label: 'NVA' },
  { value: 'NVAD', label: 'NVAD' },
  { value: 'VAD', label: 'VAD' },
  { value: 'AD', label: 'AD' },
  { value: 'EMPTY', label: '(closed-class)' },
];

function buttonLabel(selected, fallback) {
  if (selected.length === 0) return fallback;
  return selected.join(', ');
}

export default function Toolbar({
  search, onSearchChange,
  filterSections, onFilterSectionsChange,
  filterTypes, onFilterTypesChange,
  filterMasks, onFilterMasksChange,
  view, onViewChange,
  resultCount, totalCount,
  onLegendToggle,
}) {
  return (
    <div className="toolbar">
      <input
        type="text"
        id="search"
        placeholder="Search by word, gloss, component, example…"
        autoFocus
        value={search}
        onChange={e => onSearchChange(e.target.value)}
      />

      <MultiSelect
        label={buttonLabel(filterSections, 'All sections')}
        options={SECTION_OPTIONS}
        selected={filterSections}
        onChange={onFilterSectionsChange}
      />

      <MultiSelect
        label={buttonLabel(filterTypes, 'All types')}
        options={TYPE_OPTIONS}
        selected={filterTypes}
        onChange={onFilterTypesChange}
      />

      <MultiSelect
        label={buttonLabel(filterMasks, 'All masks')}
        options={MASK_OPTIONS}
        selected={filterMasks}
        onChange={onFilterMasksChange}
      />

      <button className={view === 'table' ? 'active' : ''} onClick={() => onViewChange('table')}>📋 Table</button>
      <button className={view === 'card' ? 'active' : ''} onClick={() => onViewChange('card')}>🃏 Cards</button>
      <span className="result-count">
        {resultCount === totalCount ? totalCount + ' words' : resultCount + ' of ' + totalCount + ' words'}
      </span>
      <span className="legend-toggle" onClick={onLegendToggle}>Legend ▾</span>
    </div>
  );
}

function MultiSelect({ label, options, selected, onChange }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const toggle = (value) => {
    if (selected.includes(value)) {
      onChange(selected.filter(v => v !== value));
    } else {
      onChange([...selected, value]);
    }
  };

  return (
    <div className="multiselect" ref={ref}>
      <button
        className={`multiselect-trigger${selected.length > 0 ? ' has-selection' : ''}`}
        onClick={() => setOpen(o => !o)}
      >
        {label}
        <span className="multiselect-arrow">▾</span>
      </button>
      {open && (
        <div className="multiselect-dropdown">
          {options.map(opt => (
            <label key={opt.value} className="multiselect-option">
              <input
                type="checkbox"
                checked={selected.includes(opt.value)}
                onChange={() => toggle(opt.value)}
              />
              <span>{opt.label}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}