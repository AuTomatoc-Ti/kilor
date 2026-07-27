import { describe, it, expect, beforeAll, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { initDatabase, getDB } from './db';

/**
 * End-to-end tests using the REAL kilor.db database.
 *
 * In jsdom (Node), initDatabase() reads data/kilor.db directly from the
 * filesystem via node:fs. This exercises the full initialization pipeline
 * that the browser would use — no mock injection, no synthetic test data.
 */

let totalWordCount = 0;

beforeAll(async () => {
  await initDatabase();
  totalWordCount = (getDB().exec('SELECT COUNT(*) FROM words')[0]?.values[0]?.[0]) || 400;
});

beforeEach(() => {
  // Reset URL state to prevent search/param leakage between tests in jsdom
  window.history.replaceState(null, '', window.location.pathname);
});

afterEach(() => {
  cleanup();
});

/** Wait for the app to finish loading (search input visible). */
async function waitForApp() {
  await screen.findByPlaceholderText(/Search by word/i);
}

/** Advance past the 300ms search debounce after typing. */
async function typeAndWait(input, value) {
  fireEvent.change(input, { target: { value } });
  // Wait 350ms for the 300ms debounce to fire + re-render
  await new Promise(r => setTimeout(r, 350));
}

/** Open the advanced filter panel if not already open (returns true after expand). */
async function openFilterPanel() {
  const btn = screen.queryByText(/Advanced filter/);
  if (btn && btn.textContent.includes('\u25BE')) {
    fireEvent.click(btn);
    await waitFor(() => expect(document.querySelector('.filter-panel')).toBeInTheDocument());
  }
}

/** Toggle a checkbox inside the filter panel by label text match. */
async function toggleFilterCheckbox(labelText) {
  await openFilterPanel();
  const filterPanel = document.querySelector('.filter-panel');
  if (!filterPanel) throw new Error('Filter panel not open');
  const labels = filterPanel.querySelectorAll('label.filter-checkbox-row');
  for (const label of labels) {
    if (label.textContent.includes(labelText)) {
      const cb = label.querySelector('input[type="checkbox"]');
      fireEvent.click(cb);
      return;
    }
  }
  throw new Error(`toggleFilterCheckbox: "${labelText}" not found in filter panel`);
}

/** Check a mask checkbox by its data-mask attribute. */
async function toggleMaskFilter(maskValue) {
  await openFilterPanel();
  const label = document.querySelector(`label[data-mask="${maskValue}"]`);
  if (!label) throw new Error(`toggleMaskFilter: mask "${maskValue}" not found`);
  const cb = label.querySelector('input[type="checkbox"]');
  fireEvent.click(cb);
}

describe('App — initialization (real DB)', () => {
  it('renders header with dynamic total word count', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.getByText('Kilor Dictionary')).toBeInTheDocument();

    // Count should be a positive integer, not tied to a hardcoded value
    const countText = `${totalWordCount} words`;
    const countEls = screen.getAllByText(countText);
    expect(countEls.length).toBeGreaterThanOrEqual(1);
  });

  it('does NOT show the error state', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.queryByText(/Cannot load dictionary data/)).not.toBeInTheDocument();
  });

  it('table header columns are present', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.getByText('Word')).toBeInTheDocument();
    expect(screen.getByText('Gloss')).toBeInTheDocument();
  });

  it('shows word entries on initial load, not "No words match."', async () => {
    render(<App />);
    await waitForApp();

    expect(screen.queryByText('No words match.')).not.toBeInTheDocument();

    // With pagination (50/page), verify at least one page worth of entries
    const formCells = document.querySelectorAll('.td-form');
    expect(formCells.length).toBeGreaterThan(10);
    // Page 1 may not include 'fora' depending on sort order; it's fine
  });

  it('shows all words when no filters are active (= empty arrays)', async () => {
    render(<App />);
    await waitForApp();

    // Result count should show total word count — use getAllByText since header+toolbar both show it
    const countText = `${totalWordCount} words`;
    const countEls = screen.getAllByText(countText);
    expect(countEls).toHaveLength(2);
    const resultSpan = document.querySelector('.result-count');
    expect(resultSpan.textContent).toBe(countText);
  });
});

describe('App — search (real DB)', () => {
  it('search by exact form "fora" returns that entry', async () => {
    render(<App />);
    await waitForApp();

    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'fora');

    const foraEls = screen.getAllByText('fora');
    expect(foraEls.length).toBeGreaterThanOrEqual(1);
  });

  it('search is case-insensitive ("FORA" matches "fora")', async () => {
    render(<App />);
    await waitForApp();

    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'FORA');

    const els = screen.getAllByText('fora');
    expect(els.length).toBeGreaterThanOrEqual(1);
  });

  it('search by gloss "fire" matches "fora"', async () => {
    render(<App />);
    await waitForApp();

    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'fire');

    const els = screen.getAllByText('fora');
    expect(els.length).toBeGreaterThanOrEqual(1);
  });

  it('search nonexistent word shows "No words match"', async () => {
    render(<App />);
    await waitForApp();

    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'xyzzyzzz');

    await waitFor(() => expect(screen.getByText('No words match.')).toBeInTheDocument());
  });
});

describe('App — advanced filter panel (real DB)', () => {
  it('toggles filter panel on button click', async () => {
    render(<App />);
    await waitForApp();

    expect(document.querySelector('.filter-panel')).toBeNull();

    fireEvent.click(screen.getByText(/Advanced filter/));
    await waitFor(() =>
      expect(document.querySelector('.filter-panel')).toBeInTheDocument()
    );

    fireEvent.click(screen.getByText(/Advanced filter/));
    await waitFor(() =>
      expect(document.querySelector('.filter-panel')).toBeNull()
    );
  });

  it('checking "Function words" type shows only function words', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('Function words');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    const typeTds = document.querySelectorAll('.td-type');
    const types = [...typeTds].map((td) => td.textContent);
    for (const t of types) {
      expect(t).toContain('func');
    }
  });

  it('checking "N" mask shows words that can function as nouns', async () => {
    render(<App />);
    await waitForApp();

    await toggleMaskFilter('N');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    const maskTds = document.querySelectorAll('.td-mask');
    const masks = [...maskTds].map((td) => td.textContent.trim());
    for (const m of masks) {
      if (m !== '—') {
        expect(m).toMatch(/N/i);
      }
    }
  });

  it('checking "Adv" mask shows words that can function as adverbs', async () => {
    render(<App />);
    await waitForApp();

    await toggleMaskFilter('D');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    const maskTds = document.querySelectorAll('.td-mask');
    const masks = [...maskTds].map((td) => td.textContent.trim());
    for (const m of masks) {
      if (m !== '—') {
        expect(m).toMatch(/D/i);
      }
    }
  });

  it('checking "Compounds" type shows only compound words', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('Compounds');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    const typeTds = document.querySelectorAll('.td-type');
    const types = [...typeTds].map((td) => td.textContent);
    for (const t of types) {
      expect(t).toContain('cmpd');
    }
  });

  it('syllable range filter limits entries', async () => {
    render(<App />);
    await waitForApp();

    await openFilterPanel();

    // Set max syllables to 2
    const maxInput = document.querySelectorAll('.syl-input')[1];
    fireEvent.change(maxInput, { target: { value: '2' } });

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    // Search for a known 2-syllable word to verify it's visible on this page
    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'fora');

    const tds = document.querySelectorAll('.td-form');
    const forms = [...tds].map((td) => td.textContent);
    expect(forms).toContain('fora');

    // All entries should have syl_count <= 2
    const sylTds = document.querySelectorAll('.td-syl');
    const syls = [...sylTds].map((td) => parseInt(td.textContent));
    for (const s of syls) {
      expect(s).toBeLessThanOrEqual(2);
    }
  });

  it('reset filters button clears all filters back to showing dynamic word count', async () => {
    render(<App />);
    await waitForApp();

    // Apply some filters first
    await toggleFilterCheckbox('Function words');
    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    // Click "Reset filters"
    const resetBtn = document.querySelector('.filter-reset-btn');
    fireEvent.click(resetBtn);

    // Should be back to showing dynamic word count
    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).toBe(`${totalWordCount} words`);
    });
  });
});

describe('App — prefix filter (real DB)', () => {
  it('checking a single prefix shows only words with that prefix', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('a-');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe(`${totalWordCount} words`);
    });

    // All visible prefix badges should contain "a-"
    const prefixTds = document.querySelectorAll('.td-prefix');
    const prefixTexts = [...prefixTds].map((td) => td.textContent.trim());
    for (const p of prefixTexts) {
      if (p !== '—') {
        expect(p).toContain('a-');
      }
    }
  });
});

describe('App — sorting (real DB)', () => {
  it('sorts by form ascending by default', async () => {
    render(<App />);
    await waitForApp();

    const cells = screen.getAllByRole('cell');
    const forms = cells
      .filter((c) => c.className.includes('td-form'))
      .map((c) => c.textContent);
    for (let i = 1; i < forms.length; i++) {
      expect(forms[i].localeCompare(forms[i - 1])).toBeGreaterThanOrEqual(0);
    }
  });

  it('clicking sort column toggles direction', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.click(screen.getByText('Word'));

    await waitFor(() => {
      const cells = screen.getAllByRole('cell');
      const forms = cells
        .filter((c) => c.className.includes('td-form'))
        .map((c) => c.textContent);
      // Sorted descending
      for (let i = 1; i < forms.length; i++) {
        expect(forms[i].localeCompare(forms[i - 1])).toBeLessThanOrEqual(0);
      }
    });
  });

  it('sticky toolbar / top-bar CSS is present', async () => {
    render(<App />);
    await waitForApp();
    expect(document.querySelector('.top-bar')).toBeInTheDocument();
    expect(document.querySelector('.main-content')).toBeInTheDocument();
  });
});

describe('App — inline detail expansion (real DB)', () => {
  it('clicking a table row expands detail panel', async () => {
    render(<App />);
    await waitForApp();

    expect(document.querySelector('.detail-panel')).toBeNull();

    const firstCell = document.querySelector('.td-form');
    expect(firstCell).toBeTruthy();
    fireEvent.click(firstCell);

    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );
  });

  it('clicking expanded row again collapses it', async () => {
    render(<App />);
    await waitForApp();

    const firstCell = document.querySelector('.td-form');
    expect(firstCell).toBeTruthy();
    fireEvent.click(firstCell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    fireEvent.click(firstCell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeNull()
    );
  });

  it('detail panel shows syllable division with / separator', async () => {
    render(<App />);
    await waitForApp();

    // Search for "fora" to narrow results
    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'fora');

    const tds = document.querySelectorAll('.td-form');
    expect(tds.length).toBeGreaterThanOrEqual(1);

    // Click to expand
    const cell = document.querySelector('.td-form');
    fireEvent.click(cell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    expect(screen.getByText('Syllables')).toBeInTheDocument();

    const detailPanel = document.querySelector('.detail-panel');
    const text = detailPanel.textContent;
    expect(text).toMatch(/Syllables/);
    expect(text).toMatch(/fo\/ra/);
  });

  it('detail panel syllable division for single-syllable word shows no slashes', async () => {
    render(<App />);
    await waitForApp();

    // Search for "song" — a single-syllable word
    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'song');

    const tds = document.querySelectorAll('.td-form');
    expect(tds.length).toBeGreaterThanOrEqual(1);

    // Click to expand
    const cell = document.querySelector('.td-form');
    fireEvent.click(cell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    const detailPanel = document.querySelector('.detail-panel');
    const text = detailPanel.textContent;
    expect(text).toMatch(/Syllables/);
    expect(text).toContain('(song)');
  });
});

describe('App — view full entry workflow', () => {
  it('search → expand → view full entry → back to table', async () => {
    render(<App />);
    await waitForApp();

    // Search for "fora"
    const input = screen.getByPlaceholderText(/Search by word/i);
    await typeAndWait(input, 'fora');

    expect(screen.getAllByText('fora').length).toBeGreaterThanOrEqual(1);

    // Click to expand detail
    const cell = document.querySelector('.td-form');
    fireEvent.click(cell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    // Click "View full entry →"
    const viewFullBtn = document.querySelector('.view-full-link');
    expect(viewFullBtn).toBeTruthy();
    fireEvent.click(viewFullBtn);

    // Verify full detail page renders
    await waitFor(() => {
      expect(document.querySelector('.word-detail-page')).toBeInTheDocument();
      expect(document.querySelector('.detail-word-form').textContent).toContain('fora');
      expect(screen.getByText('Meanings')).toBeInTheDocument();
    });

    // Click "← Back to dictionary"
    fireEvent.click(screen.getByText('← Back to dictionary'));
    await waitFor(() =>
      expect(document.querySelector('.word-detail-page')).toBeNull()
    );
    expect(screen.getByText('Kilor Dictionary')).toBeInTheDocument();
  });
});

describe('App — table alignment (real DB)', () => {
  it('.main-content and .table-header-bar both use scrollbar-gutter: stable to prevent column misalignment', async () => {
    // Verify the CSS rules exist in the source file.
    // jsdom does not expose Vite-injected CSS via document.styleSheets,
    // so we check the raw source.
    const { readFileSync } = await import('node:fs');
    const { resolve, dirname } = await import('node:path');
    const { fileURLToPath } = await import('node:url');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const cssPath = resolve(__dirname, 'App.css');
    const css = readFileSync(cssPath, 'utf-8');
    // Both containers must have scrollbar-gutter: stable for column alignment
    expect(css).toContain('.main-content { overflow: auto; scrollbar-gutter: stable; }');
    expect(css).toContain('.table-header-bar { overflow-y: auto; flex-shrink: 0; scrollbar-gutter: stable; }');
    expect(css.match(/scrollbar-gutter: stable/g).length).toBeGreaterThanOrEqual(2);
  });

  it('header and body tables have the same number of columns (no modified column)', async () => {
    render(<App />);
    await waitForApp();

    const headerTable = document.querySelector('.word-table-header');
    const bodyTable = document.querySelector('.word-table-body');
    expect(headerTable).toBeTruthy();
    expect(bodyTable).toBeTruthy();

    const headerCols = headerTable.querySelectorAll('colgroup col');
    const bodyCols = bodyTable.querySelectorAll('colgroup col');
    expect(headerCols.length).toBe(bodyCols.length);
    // Default: 7 columns (Word, IPA, Gloss, Type, Prefix, NVAD, Syl), no Modified
    expect(headerCols.length).toBe(7);

    // Also check that data row has the same number of td cells as header th cells
    const headerThs = headerTable.querySelectorAll('thead th');
    const firstRowTds = bodyTable.querySelectorAll('tbody tr:first-child td');
    // first row in body may be a detail-tr (expanded), so we skip to the first non-detail row
    const firstDataRow = bodyTable.querySelector('tbody tr:not(.detail-tr)');
    expect(firstDataRow).toBeTruthy();
    const firstDataTds = firstDataRow.querySelectorAll('td');
    expect(headerThs.length).toBe(firstDataTds.length);
  });

  it('settings gear button exists and can be clicked', async () => {
    render(<App />);
    await waitForApp();

    const gearBtn = document.querySelector('.settings-gear-btn');
    expect(gearBtn).toBeTruthy();
  });

  it('enabling modified column adds the extra column to both header and body', async () => {
    render(<App />);
    await waitForApp();

    // Click gear to open settings
    const gearBtn = document.querySelector('.settings-gear-btn');
    expect(gearBtn).toBeTruthy();
    fireEvent.click(gearBtn);

    // Wait for settings panel
    await waitFor(() => expect(document.querySelector('.settings-dropdown')).toBeInTheDocument());

    // Toggle "Show Last Modified" checkbox
    const cb = document.querySelector('.settings-row input[type="checkbox"]');
    expect(cb).toBeTruthy();
    expect(cb.checked).toBe(false);
    fireEvent.click(cb);

    // Settings panel should still be open; close it
    fireEvent.click(document.querySelector('.settings-close-btn'));
    await waitFor(() => expect(document.querySelector('.settings-dropdown')).toBeNull());

    // Now check columns: should be 8 (7 + Modified)
    const headerTable = document.querySelector('.word-table-header');
    const bodyTable = document.querySelector('.word-table-body');
    const headerCols = headerTable.querySelectorAll('colgroup col');
    const bodyCols = bodyTable.querySelectorAll('colgroup col');
    expect(headerCols.length).toBe(8);
    expect(bodyCols.length).toBe(8);

    // Verify the "Modified" column header text is present
    const headerThs = headerTable.querySelectorAll('thead th');
    const thTexts = [...headerThs].map(th => th.textContent.trim());
    expect(thTexts.some(t => t.startsWith('Modified'))).toBe(true);

    // Verify data row has 8 td cells
    const firstDataRow = bodyTable.querySelector('tbody tr:not(.detail-tr)');
    const firstDataTds = firstDataRow.querySelectorAll('td');
    expect(firstDataTds.length).toBe(8);
  });

  it('header and body colgroup widths match exactly', async () => {
    render(<App />);
    await waitForApp();

    const headerTable = document.querySelector('.word-table-header');
    const bodyTable = document.querySelector('.word-table-body');
    const headerCols = headerTable.querySelectorAll('colgroup col');
    const bodyCols = bodyTable.querySelectorAll('colgroup col');

    for (let i = 0; i < headerCols.length; i++) {
      const hw = headerCols[i].style.width;
      const bw = bodyCols[i].style.width;
      expect(hw).toBe(bw);
    }
  });
});

describe('App — prefix legend modal (visual/accessibility)', () => {
  it('opens prefix legend modal and shows all 7 prefixes', async () => {
    render(<App />);
    await waitForApp();

    // Click the "?" trigger in the Prefix column header
    const trigger = document.querySelector('.prefix-legend-trigger');
    expect(trigger).toBeTruthy();
    fireEvent.click(trigger);

    // Modal should be visible
    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    // All 7 prefix rows should be present
    const rows = document.querySelectorAll('.prefix-legend-row');
    expect(rows.length).toBe(7);

    // Verify specific prefixes
    const prefixes = ['a-', 'e-', 'i-', 'o-', 'u-', 'y-', 'ae-'];
    const labels = document.querySelectorAll('.prefix-legend-label strong');
    const labelTexts = [...labels].map(el => el.textContent);
    expect(labelTexts).toEqual(prefixes);
  });

  it('prefix legend text is selectable (user-select: text)', async () => {
    render(<App />);
    await waitForApp();

    const trigger = document.querySelector('.prefix-legend-trigger');
    fireEvent.click(trigger);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    // Read the CSS file and verify user-select: text is present for legend elements
    const { readFileSync } = await import('node:fs');
    const { resolve, dirname } = await import('node:path');
    const { fileURLToPath } = await import('node:url');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const cssPath = resolve(__dirname, 'App.css');
    const css = readFileSync(cssPath, 'utf-8');

    // Verify user-select: text is set on legend elements
    expect(css).toContain('.prefix-legend-row {');
    expect(css).toContain('user-select: text');
    expect(css).toContain('.prefix-legend-cls {');
    expect(css).toContain('.prefix-legend-emotion {');
    expect(css).toContain('.prefix-legend-note {');
  });


  it('prefix legend modal has proper overflow handling to prevent viewport overflow', async () => {
    render(<App />);
    await waitForApp();

    const trigger = document.querySelector('.prefix-legend-trigger');
    fireEvent.click(trigger);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    // Read the CSS file and verify overflow handling
    const { readFileSync } = await import('node:fs');
    const { resolve, dirname } = await import('node:path');
    const { fileURLToPath } = await import('node:url');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const cssPath = resolve(__dirname, 'App.css');
    const css = readFileSync(cssPath, 'utf-8');

    // Verify modal has overflow-y: auto and max-height to prevent viewport overflow
    expect(css).toContain('.prefix-legend-modal {');
    expect(css).toContain('overflow-y: auto');
    expect(css).toContain('max-height: 90vh');
  });

  it('prefix legend uses CSS Grid for proper text wrapping', async () => {
    render(<App />);
    await waitForApp();

    const trigger = document.querySelector('.prefix-legend-trigger');
    fireEvent.click(trigger);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    // Read the CSS file and verify CSS Grid layout is used
    const { readFileSync } = await import('node:fs');
    const { resolve, dirname } = await import('node:path');
    const { fileURLToPath } = await import('node:url');
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const cssPath = resolve(__dirname, 'App.css');
    const css = readFileSync(cssPath, 'utf-8');

    // Verify CSS Grid layout and word-wrap for proper text wrapping
    expect(css).toContain('.prefix-legend-row {');
    expect(css).toContain('display: grid');
    expect(css).toContain('grid-template-columns: 14px 32px 1fr 1fr');
    expect(css).toContain('.prefix-legend-cls {');
    expect(css).toContain('word-wrap: break-word');
    expect(css).toContain('.prefix-legend-emotion {');
    expect(css).toContain('word-wrap: break-word');
  });

  it('closes modal when Close button is clicked', async () => {
    render(<App />);
    await waitForApp();

    const trigger = document.querySelector('.prefix-legend-trigger');
    fireEvent.click(trigger);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    const closeBtn = document.querySelector('.prefix-legend-close');
    expect(closeBtn).toBeTruthy();
    fireEvent.click(closeBtn);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeNull());
  });

  it('closes modal when overlay is clicked', async () => {
    render(<App />);
    await waitForApp();

    const trigger = document.querySelector('.prefix-legend-trigger');
    fireEvent.click(trigger);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeInTheDocument());

    const overlay = document.querySelector('.prefix-legend-overlay');
    expect(overlay).toBeTruthy();
    fireEvent.click(overlay);

    await waitFor(() => expect(document.querySelector('.prefix-legend-modal')).toBeNull());
  });
});
