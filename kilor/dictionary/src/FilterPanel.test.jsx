/** @vitest-environment jsdom */
import React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import FilterPanel from './components/FilterPanel.jsx';

const PREFIX_INFO = {
  "a-":  { cls: "Alive / Energy", emotion: "Anger", color: "#ef4444" },
  "e-":  { cls: "Crafted / Tool",  emotion: "Joy",   color: "#f59e0b" },
};

describe('FilterPanel compound sub-filter', () => {
  afterEach(() => { cleanup(); });

  it('does NOT render mono/multi when compounds is unchecked', () => {
    render(<FilterPanel
      prefixInfo={PREFIX_INFO}
      filterPrefixes={[]} onFilterPrefixesChange={() => {}}
      filterTypes={['root']} onFilterTypesChange={() => {}}
      filterCompoundTypes={[]} onFilterCompoundTypesChange={() => {}}
      filterMasks={[]} onFilterMasksChange={() => {}}
      sylMin={1} onSylMinChange={() => {}}
      sylMax={10} onSylMaxChange={() => {}}
      onResetFilters={() => {}}
    />);
    expect(screen.getByText('Compounds')).toBeTruthy();
    expect(screen.queryByText('mono')).toBeNull();
    expect(screen.queryByText('multi')).toBeNull();
  });

  it('renders mono and multi sub-options when compounds IS checked', () => {
    render(<FilterPanel
      prefixInfo={PREFIX_INFO}
      filterPrefixes={[]} onFilterPrefixesChange={() => {}}
      filterTypes={['compound']} onFilterTypesChange={() => {}}
      filterCompoundTypes={[]} onFilterCompoundTypesChange={() => {}}
      filterMasks={[]} onFilterMasksChange={() => {}}
      sylMin={1} onSylMinChange={() => {}}
      sylMax={10} onSylMaxChange={() => {}}
      onResetFilters={() => {}}
    />);
    // Debug: dump rendered HTML
    const compoundRow = screen.getByText('Compounds').closest('label');
    console.log('Compound section HTML:', compoundRow?.parentElement?.innerHTML);
    expect(screen.getByText('mono')).toBeTruthy();
    expect(screen.getByText('multi')).toBeTruthy();
  });
});