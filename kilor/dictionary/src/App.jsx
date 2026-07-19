import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Header from './components/Header';
import Toolbar from './components/Toolbar';
import FilterPanel from './components/FilterPanel';
import TableView from './components/TableView';
import { initDatabase, queryWords, getMeta, reloadDatabase } from './db';

const PREFIX_INFO = {
  "a-":  { cls: "Alive / Energy",    emotion: "Anger",   color: "#ef4444" },
  "e-":  { cls: "Crafted / Tool",    emotion: "Joy",     color: "#f59e0b" },
  "i-":  { cls: "Fluid / Vast",      emotion: "Sadness", color: "#3b82f6" },
  "o-":  { cls: "Abstract / Void",   emotion: "Surprise",color: "#f5f5f5" },
  "u-":  { cls: "Organic / Growth",  emotion: "Calm",    color: "#22c55e" },
  "y-":  { cls: "Dense / Mass",      emotion: "Fear",    color: "#6b7280" },
  "ae-": { cls: "Earth / Boundary",  emotion: "Disgust", color: "#a16207" },
};

const ALL_PREFIX_KEYS = Object.keys(PREFIX_INFO);

export default function App() {
  const [search, setSearch] = useState('');
  const [dbVersion, setDbVersion] = useState(0);

  const [filterSections, setFilterSections] = useState([]);
  const [filterTypes, setFilterTypes] = useState([]);
  const [filterMasks, setFilterMasks] = useState([]);
  const [filterPrefixes, setFilterPrefixes] = useState([]);
  const [sylMin, setSylMin] = useState(1);
  const [sylMax, setSylMax] = useState(10);
  const [sortCol, setSortCol] = useState('form');
  const [sortDir, setSortDir] = useState('asc');
  const [filterOpen, setFilterOpen] = useState(false);
  const [expandedRow, setExpandedRow] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalCount, setTotalCount] = useState(0);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    initDatabase()
      .then(() => {
        setTotalCount(getMeta().total);
        setLoading(false);
      })
      .catch(err => {
        setError('Cannot load dictionary data: ' + err.message + '. Run "python kilor.py export --format html" first.');
        setLoading(false);
      });
  }, []);

  const entries = useMemo(
    () => queryWords({
      search, sections: filterSections, types: filterTypes, masks: filterMasks,
      prefixes: filterPrefixes, sylMin, sylMax, sortCol, sortDir,
    }),
    [search, filterSections, filterTypes, filterMasks, filterPrefixes, sylMin, sylMax, sortCol, sortDir, loading, dbVersion]
  );

  const handleSort = useCallback((col) => {
    setSortCol(prev => {
      if (prev === col) {
        setSortDir(d => d === 'asc' ? 'desc' : 'asc');
        return prev;
      }
      setSortDir('asc');
      return col;
    });
  }, []);

  const handleResetFilters = useCallback(() => {
    setFilterSections([]);
    setFilterTypes([]);
    setFilterMasks([]);
    setFilterPrefixes([]);
    setSylMin(1);
    setSylMax(10);
  }, []);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      const count = await reloadDatabase();
      setTotalCount(count);
      setDbVersion(v => v + 1);
    } catch (err) {
      setError('Cannot refresh: ' + err.message);
    } finally {
      setRefreshing(false);
    }
  }, []);

  const handleSearchByForm = useCallback((form) => {
    setSearch(form);
    setFilterSections([]);
    setFilterTypes([]);
    setFilterMasks([]);
  }, []);

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
      <div className="top-bar">
        <Header total={totalCount} />
        <Toolbar
          search={search}
          onSearchChange={setSearch}
          resultCount={entries.length}
          totalCount={totalCount}
          filterOpen={filterOpen}
          onFilterToggle={() => setFilterOpen(o => !o)}
          onRefresh={handleRefresh}
          refreshing={refreshing}
        />
        {filterOpen && (
          <FilterPanel
            prefixInfo={PREFIX_INFO}
            filterPrefixes={filterPrefixes}
            onFilterPrefixesChange={setFilterPrefixes}
            filterSections={filterSections}
            onFilterSectionsChange={setFilterSections}
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
      <div className="main-content">
        <TableView
          entries={entries}
          sortCol={sortCol}
          sortDir={sortDir}
          onSort={handleSort}
          prefixInfo={PREFIX_INFO}
          onSearchByForm={handleSearchByForm}
          expandedRow={expandedRow}
          onToggleExpand={setExpandedRow}
        />
      </div>
    </>
  );
}