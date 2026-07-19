export default function Toolbar({
  search, onSearchChange,
  filterSection, onFilterSectionChange,
  filterType, onFilterTypeChange,
  filterMask, onFilterMaskChange,
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
      <select value={filterSection} onChange={e => onFilterSectionChange(e.target.value)}>
        <option value="">All sections</option>
        <option value="A">A — Worlds & Elements</option>
        <option value="B">B — Living Things</option>
        <option value="C">C — Physical Objects</option>
        <option value="D">D — Actions & Motion</option>
        <option value="E">E — Qualities & States</option>
        <option value="F">F — Mind & Emotion</option>
        <option value="G">G — Time & Space</option>
        <option value="H">H — Social & Relational</option>
        <option value="I">I — Abstract</option>
        <option value="J">J — Sensation</option>
      </select>
      <select value={filterType} onChange={e => onFilterTypeChange(e.target.value)}>
        <option value="">All types</option>
        <option value="root">Roots</option>
        <option value="compound">Compounds</option>
        <option value="function">Function words</option>
      </select>
      <select value={filterMask} onChange={e => onFilterMaskChange(e.target.value)}>
        <option value="">All masks</option>
        <option value="N">N</option>
        <option value="V">V</option>
        <option value="A">A</option>
        <option value="D">D</option>
        <option value="NAD">NAD</option>
        <option value="NV">NV</option>
        <option value="NA">NA</option>
        <option value="NVA">NVA</option>
        <option value="NVAD">NVAD</option>
        <option value="VAD">VAD</option>
        <option value="AD">AD</option>
        <option value="EMPTY">(closed-class)</option>
      </select>
      <button className={view === 'table' ? 'active' : ''} onClick={() => onViewChange('table')}>📋 Table</button>
      <button className={view === 'card' ? 'active' : ''} onClick={() => onViewChange('card')}>🃏 Cards</button>
      <span className="result-count">
        {resultCount === totalCount ? totalCount + ' words' : resultCount + ' of ' + totalCount + ' words'}
      </span>
      <span className="legend-toggle" onClick={onLegendToggle}>Legend ▾</span>
    </div>
  );
}