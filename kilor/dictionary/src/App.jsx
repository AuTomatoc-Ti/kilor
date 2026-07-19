import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Header from './components/Header';
import Toolbar from './components/Toolbar';
import Legend from './components/Legend';
import TableView from './components/TableView';
import CardView from './components/CardView';
import { initDatabase, queryWords, getMeta } from './db';

const PREFIX_INFO = {
  "a-":  { cls: "Alive / Energy",    emotion: "Anger",   color: "#ef4444" },
  "e-":  { cls: "Crafted / Tool",    emotion: "Joy",     color: "#f59e0b" },
  "i-":  { cls: "Fluid / Vast",      emotion: "Sadness", color: "#3b82f6" },
  "o-":  { cls: "Abstract / Void",   emotion: "Surprise",color: "#8b5cf6" },
  "u-":  { cls: "Organic / Growth",  emotion: "Calm",    color: "#22c55e" },
  "y-":  { cls: "Dense / Mass",      emotion: "Fear",    color: "#6b7280" },
  "ae-": { cls: "Earth / Boundary",  emotion: "Disgust", color: "#a16207" },
};

export default function App() {
  const [search, setSearch] = useState('');
  const [filterSection, setFilterSection] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterMask, setFilterMask] = useState('');
  const [sortCol, setSortCol] = useState('form');
  const [sortDir, setSortDir] = useState('asc');
  const [view, setView] = useState('table');
  const [legendOpen, setLegendOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalCount, setTotalCount] = useState(0);

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
    () => queryWords({ search, section: filterSection, filterType, filterMask, sortCol, sortDir }),
    [search, filterSection, filterType, filterMask, sortCol, sortDir]
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

  const handleSearchByForm = useCallback((form) => {
    setSearch(form);
    setFilterSection('');
    setFilterType('');
    setFilterMask('');
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
          filterSection={filterSection}
          onFilterSectionChange={setFilterSection}
          filterType={filterType}
          onFilterTypeChange={setFilterType}
          filterMask={filterMask}
          onFilterMaskChange={setFilterMask}
          view={view}
          onViewChange={setView}
          resultCount={entries.length}
          totalCount={totalCount}
          onLegendToggle={() => setLegendOpen(o => !o)}
        />
        <Legend
          open={legendOpen}
          prefixInfo={PREFIX_INFO}
        />
      </div>
      <div className="main-content">
        {view === 'table' ? (
          <TableView
            entries={entries}
            sortCol={sortCol}
            sortDir={sortDir}
            onSort={handleSort}
            prefixInfo={PREFIX_INFO}
            onSearchByForm={handleSearchByForm}
          />
        ) : (
          <CardView
            entries={entries}
            prefixInfo={PREFIX_INFO}
            onSearchByForm={handleSearchByForm}
          />
        )}
      </div>
    </>
  );
}