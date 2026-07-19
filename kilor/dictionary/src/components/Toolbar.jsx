export default function Toolbar({
  search, onSearchChange,
  resultCount, totalCount,
  filterOpen, onFilterToggle,
}) {
  return (
    <div className="toolbar">
      <div className="toolbar-main">
        <input
          type="text"
          id="search"
          placeholder="Search by word or gloss…"
          autoFocus
          value={search}
          onChange={e => onSearchChange(e.target.value)}
        />
        <div className="toolbar-right">
          <span className="result-count">
            {resultCount === totalCount ? totalCount + ' words' : resultCount + ' of ' + totalCount + ' words'}
          </span>
          <button
            className={'advanced-filter-btn' + (filterOpen ? ' active' : '')}
            onClick={onFilterToggle}
          >
            Advanced filter {filterOpen ? '▴' : '▾'}
          </button>
        </div>
      </div>
    </div>
  );
}