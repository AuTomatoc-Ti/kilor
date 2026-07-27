import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import Header from './components/Header';
import Toolbar from './components/Toolbar';
import FilterPanel from './components/FilterPanel';
import { TableHeader, TableBody, WordDetailPage } from './components/TableView';
import { initDatabase, queryWords, getMeta, reloadDatabase, autocompleteSearch, fuzzySearch } from './db';

const PREFIX_INFO = {
  "a-":  { cls: "Alive / Energy",    emotion: "Anger",   color: "#ef4444" },
  "e-":  { cls: "Crafted / Tool",    emotion: "Joy",     color: "#f59e0b" },
  "i-":  { cls: "Fluid / Vast",      emotion: "Sadness", color: "#3b82f6" },
  "o-":  { cls: "Abstract / Void",   emotion: "Surprise",color: "#d2d2d2" },
  "u-":  { cls: "Organic / Growth",  emotion: "Calm",    color: "#22c55e" },
  "y-":  { cls: "Dense / Mass",      emotion: "Fear",    color: "#6b7280" },
  "ae-": { cls: "Earth / Boundary",  emotion: "Disgust", color: "#a16207" },
};

const TYPE_LABELS = { root: 'Roots', compound: 'Compounds', function: 'Function words' };
const MASK_LABELS = { N: 'Noun', V: 'Verb', A: 'Adjective', D: 'Adverb' };

// ── URL state helpers ──────────────────────────────────────────────────────

function readStateFromURL() {
  const sp = new URLSearchParams(window.location.search);
  const parseList = (key) => sp.get(key) ? sp.get(key).split(',').filter(Boolean) : [];
  const parseIntSafe = (key, fallback) => {
    const v = parseInt(sp.get(key));
    return isNaN(v) ? fallback : v;
  };
  const detailRaw = parseInt(sp.get('detail'));
  return {
    search: sp.get('q') || '',
    types: parseList('type'),
    masks: parseList('mask'),
    prefixes: parseList('pfx'),
    sylMin: parseIntSafe('sylMin', 1),
    sylMax: parseIntSafe('sylMax', 10),
    sortCol: sp.get('sort') || 'form',
    sortDir: sp.get('dir') === 'desc' ? 'desc' : 'asc',
    filterOpen: sp.get('filt') === '1',
    showModified: sp.get('mod') === '1',
    page: parseIntSafe('page', 1),
    detailId: isNaN(detailRaw) ? null : detailRaw,
  };
}

function writeStateToURL(state) {
  const sp = new URLSearchParams();
  if (state.search) sp.set('q', state.search);
  if (state.types.length) sp.set('type', state.types.join(','));
  if (state.masks.length) sp.set('mask', state.masks.join(','));
  if (state.prefixes.length) sp.set('pfx', state.prefixes.join(','));
  if (state.sylMin > 1) sp.set('sylMin', state.sylMin);
  if (state.sylMax < 10) sp.set('sylMax', state.sylMax);
  if (state.sortCol !== 'form') sp.set('sort', state.sortCol);
  if (state.sortDir !== 'asc') sp.set('dir', state.sortDir);
  if (state.filterOpen) sp.set('filt', '1');
  if (state.showModified) sp.set('mod', '1');
  if (state.page > 1) sp.set('page', state.page);
  if (state.detailId) sp.set('detail', state.detailId);
  const qs = sp.toString();
  const url = window.location.pathname + (qs ? '?' + qs : '');
  window.history.replaceState(null, '', url);
}

// ── Clipboard toast ─────────────────────────────────────────────────────────

function Toast({ text, onDone }) {
  useEffect(() => {
    const t = setTimeout(onDone, 2000);
    return () => clearTimeout(t);
  }, [onDone]);
  return <div className="toast">{text}</div>;
}

// ── Filter chips ────────────────────────────────────────────────────────────

function FilterChips({
  types, masks, prefixes, sylMin, sylMax,
  onRemoveType, onRemoveMask, onRemovePrefix, onClearAll,
}) {
  const chips = [];
  for (const t of types) chips.push({ label: TYPE_LABELS[t] || t, onRemove: () => onRemoveType(t) });
  for (const m of masks) chips.push({ label: MASK_LABELS[m] || m, onRemove: () => onRemoveMask(m) });
  for (const p of prefixes) {
    const info = PREFIX_INFO[p];
    chips.push({ label: info ? `${p} ${info.cls}` : p, onRemove: () => onRemovePrefix(p) });
  }
  const hasSylRange = sylMin > 1 || sylMax < 10;
  if (hasSylRange) chips.push({ label: `Syl: ${sylMin}–${sylMax}`, onRemove: null });
  if (chips.length === 0) return null;
  return (
    <div className="filter-chips">
      {chips.map((c, i) => (
        <span key={i} className="filter-chip">
          {c.label}
          {c.onRemove && <button className="chip-close" onClick={c.onRemove} title="Remove filter">✕</button>}
        </span>
      ))}
      {chips.length > 0 && (
        <button className="chip-close chip-clear-all" onClick={onClearAll} title="Clear all filters">
          Clear all
        </button>
      )}
    </div>
  );
}

// ── Main App ────────────────────────────────────────────────────────────────

const PAGE_SIZE = 50;

export default function App() {
  const initial = readStateFromURL();

  const [searchDraft, setSearchDraft] = useState(initial.search);
  const [search, setSearch] = useState(initial.search);
  const [dbVersion, setDbVersion] = useState(0);
  const [filterTypes, setFilterTypes] = useState(initial.types);
  const [filterMasks, setFilterMasks] = useState(initial.masks);
  const [filterPrefixes, setFilterPrefixes] = useState(initial.prefixes);
  const [sylMin, setSylMin] = useState(initial.sylMin);
  const [sylMax, setSylMax] = useState(initial.sylMax);
  const [sortCol, setSortCol] = useState(initial.sortCol);
  const [sortDir, setSortDir] = useState(initial.sortDir);
  const [filterOpen, setFilterOpen] = useState(initial.filterOpen);
  const [expandedRow, setExpandedRow] = useState(null);
  const [detailId, setDetailId] = useState(initial.detailId);
  const [showModified, setShowModified] = useState(initial.showModified);
  const [showAudio, setShowAudio] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalWordCount, setTotalWordCount] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  const [toast, setToast] = useState(null);
  const [autocompleteItems, setAutocompleteItems] = useState([]);
  const [autocompleteIndex, setAutocompleteIndex] = useState(-1);
  const [keyboardRowIndex, setKeyboardRowIndex] = useState(-1);
  const [page, setPage] = useState(initial.page);
  const [queryTotalCount, setQueryTotalCount] = useState(0);

  const searchRef = useRef(null);

  // ── 300ms debounce for search ─────────────────────────────────────────
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearch(searchDraft);
      setPage(1); // reset to page 1 on new search
    }, 300);
    return () => clearTimeout(timer);
  }, [searchDraft]);

  // Reset page when filters change
  useEffect(() => {
    setPage(1);
  }, [filterTypes, filterMasks, filterPrefixes, sylMin, sylMax, sortCol, sortDir]);

  // URL sync
  useEffect(() => {
    if (!loading) {
      writeStateToURL({ search, types: filterTypes, masks: filterMasks, prefixes: filterPrefixes, sylMin, sylMax, sortCol, sortDir, filterOpen, showModified, page, detailId });
    }
  }, [search, filterTypes, filterMasks, filterPrefixes, sylMin, sylMax, sortCol, sortDir, filterOpen, showModified, loading, page, detailId]);

  // Autocomplete
  const handleSearchChange = useCallback((val) => {
    setSearchDraft(val);
    const items = autocompleteSearch(val);
    setAutocompleteItems(items);
    setAutocompleteIndex(-1);
  }, []);

  const selectAutocomplete = useCallback((form) => {
    setSearchDraft(form);
    setSearch(form);
    setAutocompleteItems([]);
    setAutocompleteIndex(-1);
  }, []);

  useEffect(() => {
    initDatabase()
      .then(() => {
        setTotalWordCount(getMeta().total);
        setLoading(false);
      })
      .catch(err => {
        setError('Cannot load dictionary data: ' + err.message + '. Run "python kilor.py export --format html" first.');
        setLoading(false);
      });
  }, []);

  const result = useMemo(
    () => queryWords({
      search, types: filterTypes, masks: filterMasks,
      prefixes: filterPrefixes, sylMin, sylMax, sortCol, sortDir,
      page, pageSize: PAGE_SIZE,
    }),
    [search, filterTypes, filterMasks, filterPrefixes, sylMin, sylMax, sortCol, sortDir, loading, dbVersion, page]
  );

  // Sync query total count for display
  useEffect(() => {
    setQueryTotalCount(result.totalCount);
  }, [result.totalCount]);

  const entries = result.rows;
  const totalPages = Math.max(1, Math.ceil(result.totalCount / PAGE_SIZE));

  const handleSort = useCallback((col) => {
    if (sortCol === col) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortCol(col);
      setSortDir('asc');
    }
  }, [sortCol]);

  const handleResetFilters = useCallback(() => {
    setFilterTypes([]);
    setFilterMasks([]);
    setFilterPrefixes([]);
    setSylMin(1);
    setSylMax(10);
  }, []);

  const removeFilterType = useCallback((t) => setFilterTypes(prev => prev.filter(x => x !== t)), []);
  const removeFilterMask = useCallback((m) => setFilterMasks(prev => prev.filter(x => x !== m)), []);
  const removeFilterPrefix = useCallback((p) => setFilterPrefixes(prev => prev.filter(x => x !== p)), []);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      const count = await reloadDatabase();
      setTotalWordCount(count);
      setDbVersion(v => v + 1);
      setPage(1);
    } catch (err) {
      setError('Cannot refresh: ' + err.message);
    } finally {
      setRefreshing(false);
    }
  }, []);

  const handleSearchByForm = useCallback((form) => {
    setSearchDraft(form);
    setSearch(form);
    setFilterTypes([]);
    setFilterMasks([]);
  }, []);

  const handleCopyToast = useCallback((msg) => {
    setToast(msg);
  }, []);

  const handleViewFull = useCallback((id) => {
    setDetailId(id);
    setExpandedRow(null);
  }, []);

  const handleBackFromDetail = useCallback(() => {
    setDetailId(null);
  }, []);

  // ── Keyboard handler (only active when search input is focused) ──────
  useEffect(() => {
    const handler = (e) => {
      const target = e.target;
      const isSearchFocused = target && target.id === 'search';

      if (!isSearchFocused && target !== document.body && target !== document.documentElement) return;

      // Autocomplete open → navigate autocomplete
      if (autocompleteItems.length > 0) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          setAutocompleteIndex(i => Math.min(i + 1, autocompleteItems.length - 1));
          return;
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          setAutocompleteIndex(i => Math.max(i - 1, -1));
          return;
        }
        if (e.key === 'Enter' && autocompleteIndex >= 0) {
          e.preventDefault();
          selectAutocomplete(autocompleteItems[autocompleteIndex].form);
          return;
        }
        if (e.key === 'Escape') {
          e.preventDefault();
          setAutocompleteItems([]);
          setAutocompleteIndex(-1);
          return;
        }
      }

      // Row keyboard navigation
      if (e.key === 'ArrowDown' && entries.length > 0) {
        e.preventDefault();
        setKeyboardRowIndex(i => Math.min(i + 1, entries.length - 1));
        return;
      }
      if (e.key === 'ArrowUp' && entries.length > 0) {
        e.preventDefault();
        setKeyboardRowIndex(i => Math.max(i - 1, -1));
        return;
      }
      if (e.key === 'Enter' && keyboardRowIndex >= 0 && keyboardRowIndex < entries.length) {
        e.preventDefault();
        const entry = entries[keyboardRowIndex];
        setExpandedRow(prev => prev === entry.id ? null : entry.id);
        return;
      }
      if (e.key === 'Escape') {
        e.preventDefault();
        if (expandedRow) { setExpandedRow(null); return; }
        if (filterOpen) { setFilterOpen(false); return; }
        setSearchDraft('');
        setSearch('');
        setKeyboardRowIndex(-1);
        return;
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [autocompleteItems, autocompleteIndex, entries, keyboardRowIndex, expandedRow, filterOpen, selectAutocomplete]);

  const hasFilters = filterTypes.length > 0 || filterMasks.length > 0 || filterPrefixes.length > 0 || sylMin > 1 || sylMax < 10;

  // Find the currently-viewed detail entry
  const detailEntry = useMemo(() => {
    if (!detailId) return null;
    return entries.find(e => e.id === detailId) || null;
  }, [detailId, entries]);

  // Fuzzy fallback: if search returns 0 exact results, try fuzzy
  const fuzzyResult = useMemo(() => {
    if (search && entries.length === 0 && !filterTypes.length && !filterMasks.length && !filterPrefixes.length && sylMin <= 1 && sylMax >= 10) {
      return fuzzySearch(search);
    }
    return { rows: [], totalCount: 0 };
  }, [search, entries.length, filterTypes, filterMasks, filterPrefixes, sylMin, sylMax]);

  if (loading) {
    return (
      <div className="no-results">
        <div className="icon">📖</div>
        <p>Loading dictionary data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="no-results">
        <div className="icon">⚠️</div>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <>
      <audio id="audio-player" preload="auto" style={{ display: 'none' }} />
      {toast && <Toast text={toast} onDone={() => setToast(null)} />}
      <div className="top-bar">
        <Header
          total={totalWordCount}
          settingsOpen={settingsOpen}
          onSettingsToggle={() => setSettingsOpen(o => !o)}
          showModified={showModified}
          onToggleModified={() => setShowModified(m => !m)}
          showAudio={showAudio}
          onToggleAudio={() => setShowAudio(a => !a)}
        />
        <Toolbar
          search={searchDraft}
          onSearchChange={handleSearchChange}
          resultCount={result.totalCount}
          totalCount={totalWordCount}
          filterOpen={filterOpen}
          onFilterToggle={() => setFilterOpen(o => !o)}
          onRefresh={handleRefresh}
          refreshing={refreshing}
          autocompleteItems={autocompleteItems}
          autocompleteIndex={autocompleteIndex}
          onSelectAutocomplete={selectAutocomplete}
          searchRef={searchRef}
        />
        {filterOpen && (
          <FilterPanel
            prefixInfo={PREFIX_INFO}
            filterPrefixes={filterPrefixes}
            onFilterPrefixesChange={setFilterPrefixes}
            filterTypes={filterTypes}
            onFilterTypesChange={setFilterTypes}
            filterMasks={filterMasks}
            onFilterMasksChange={setFilterMasks}
            sylMin={sylMin}
            onSylMinChange={setSylMin}
            sylMax={sylMax}
            onSylMaxChange={setSylMax}
            onResetFilters={handleResetFilters}
          />
        )}
      </div>
      {hasFilters && (
        <div className="filter-chips-bar">
          <FilterChips
            types={filterTypes}
            masks={filterMasks}
            prefixes={filterPrefixes}
            sylMin={sylMin}
            sylMax={sylMax}
            onRemoveType={removeFilterType}
            onRemoveMask={removeFilterMask}
            onRemovePrefix={removeFilterPrefix}
            onClearAll={handleResetFilters}
          />
        </div>
      )}
      {detailId ? (
        <WordDetailPage
          entry={detailEntry}
          prefixInfo={PREFIX_INFO}
          onBack={handleBackFromDetail}
          onSearchByForm={handleSearchByForm}
          onCopyToast={handleCopyToast}
          showAudio={showAudio}
        />
      ) : (
        <>
          <div className="table-header-bar" onMouseEnter={() => setAutocompleteItems([])}>
            <TableHeader sortCol={sortCol} sortDir={sortDir} onSort={handleSort} showModified={showModified} />
          </div>
          <div className="main-content" onMouseEnter={() => setAutocompleteItems([])}>
            {fuzzyResult.rows.length > 0 && (
              <div className="fuzzy-banner">
                No exact matches for "<strong>{search}</strong>". Showing similar words:
              </div>
            )}
            <TableBody
              entries={fuzzyResult.rows.length > 0 ? fuzzyResult.rows : entries}
              prefixInfo={PREFIX_INFO}
              onSearchByForm={handleSearchByForm}
              expandedRow={expandedRow}
              onToggleExpand={setExpandedRow}
              search={search}
              keyboardRowIndex={keyboardRowIndex}
              onCopyToast={handleCopyToast}
              onViewFull={handleViewFull}
              page={page}
              totalPages={totalPages}
              totalCount={result.totalCount}
              onPageChange={setPage}
              showAudio={showAudio}
              showModified={showModified}
            />
          </div>
        </>
      )}
    </>
  );
}