export default function Toolbar({
  search, onSearchChange,
  resultCount, totalCount,
  filterOpen, onFilterToggle,
  onRefresh, refreshing,
  autocompleteItems, autocompleteIndex,
  onSelectAutocomplete, searchRef,
}) {
  return (
    <div className="toolbar">
      <div className="toolbar-main">
        <div className="search-wrapper">
          <input
            ref={searchRef}
            type="text"
            id="search"
            placeholder="Search by word or gloss…"
            autoFocus
            value={search}
            onChange={e => onSearchChange(e.target.value)}
            onFocus={e => onSearchChange(e.target.value)}
          />
          {autocompleteItems.length > 0 && (
            <ul className="autocomplete-dropdown">
              {autocompleteItems.map((item, i) => (
                <li
                  key={item.id}
                  className={'autocomplete-item' + (i === autocompleteIndex ? ' active' : '')}
                  onMouseDown={(e) => { e.preventDefault(); onSelectAutocomplete(item.form); }}
                >
                  {item.form}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="toolbar-right">
          <span className="result-count">
            {resultCount === totalCount ? totalCount + ' words' : resultCount + ' of ' + totalCount + ' words'}
          </span>
          <button
            className="refresh-btn"
            onClick={onRefresh}
            disabled={refreshing}
            title="Reload database from kilor.db"
          >
            {refreshing ? '⟳' : '↻'}
          </button>
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