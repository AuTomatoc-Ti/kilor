import { describe, it, expect, beforeAll } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
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

beforeAll(async () => {
  await initDatabase();
});

/** Wait for the app to finish loading (search input visible). */
async function waitForApp() {
  await screen.findByPlaceholderText(/Search by word/i);
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
  it('renders header with real total word count', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.getByText('Kilor Dictionary')).toBeInTheDocument();

    // All filters start empty (= no filter applied), so all 361 words show
    const countEls = screen.getAllByText('361 words');
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

    const formCells = document.querySelectorAll('.td-form');
    expect(formCells.length).toBeGreaterThan(10);

    expect(screen.getAllByText('fora').length).toBeGreaterThanOrEqual(1);
  });

  it('shows all 361 words when no filters are active (= empty arrays)', async () => {
    render(<App />);
    await waitForApp();

    // Result count should show "361 words" — use getAllByText since header+toolbar both show it
    const countEls = screen.getAllByText('361 words');
    expect(countEls).toHaveLength(2);
    // The toolbar's .result-count span should read "361 words"
    const resultSpan = document.querySelector('.result-count');
    expect(resultSpan.textContent).toBe('361 words');
  });
});

describe('App — search (real DB)', () => {
  it('search by exact form "fora" returns that entry', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'fora' },
    });
    await waitFor(() => expect(screen.getByText(/of 361 words/)).toBeInTheDocument());
    const foraEls = screen.getAllByText('fora');
    expect(foraEls.length).toBeGreaterThanOrEqual(1);
  });

  it('search is case-insensitive ("FORA" matches "fora")', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'FORA' },
    });
    await waitFor(() => {
      const els = screen.getAllByText('fora');
      expect(els.length).toBeGreaterThanOrEqual(1);
    });
  });

  it('search by gloss "fire" matches "fora"', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'fire' },
    });
    await waitFor(() => {
      const els = screen.getAllByText('fora');
      expect(els.length).toBeGreaterThanOrEqual(1);
    });
  });

  it('search nonexistent word shows "No words match"', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'xyzzyzzz' },
    });
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

  it('checking section 1 filters to only section 1 words', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('1 — Concrete');

    // Count should drop from 361
    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe('361 words');
    });

    // Every visible entry should have section "1"
    const sectionTds = document.querySelectorAll('.td-section');
    const sections = [...sectionTds].map((td) => td.textContent.trim());
    for (const s of sections) {
      expect(s).toBe('1');
    }
  });

  it('checking "Function words" type shows only function words', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('Function words');

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe('361 words');
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
      expect(resultSpan.textContent).not.toBe('361 words');
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
      expect(resultSpan.textContent).not.toBe('361 words');
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
      expect(resultSpan.textContent).not.toBe('361 words');
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
      expect(resultSpan.textContent).not.toBe('361 words');
    });

    // "fora" (2 syllables) should be visible
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

  it('reset filters button clears all filters back to showing 361 words', async () => {
    render(<App />);
    await waitForApp();

    // Apply some filters first
    await toggleFilterCheckbox('1 — Concrete');
    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe('361 words');
    });

    // Click "Reset filters"
    const resetBtn = document.querySelector('.filter-reset-btn');
    fireEvent.click(resetBtn);

    // Should be back to showing "361 words" in the result count
    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).toBe('361 words');
    });
  });
});

describe('App — prefix filter (real DB)', () => {
  it('checking a single prefix shows only words with that prefix', async () => {
    render(<App />);
    await waitForApp();

    await toggleFilterCheckbox('a-');
    // Note: "a-" partial matches "ae-" too, so use the <b>a-</b> more carefully
    // Actually "a-" appears inside <b>a-</b> and also as "ae-" prefix label.
    // The label textContent includes both "a-" and "Alive / Energy" so it matches correctly.

    await waitFor(() => {
      const resultSpan = document.querySelector('.result-count');
      expect(resultSpan.textContent).not.toBe('361 words');
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
    fireEvent.click(firstCell);

    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );
  });

  it('clicking expanded row again collapses it', async () => {
    render(<App />);
    await waitForApp();

    const firstCell = document.querySelector('.td-form');
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
    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'fora' },
    });
    await waitFor(() => {
      const tds = document.querySelectorAll('.td-form');
      expect(tds.length).toBeGreaterThanOrEqual(1);
    });

    // Click to expand
    const cell = document.querySelector('.td-form');
    fireEvent.click(cell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    // Should show "Syllables" label
    expect(screen.getByText('Syllables')).toBeInTheDocument();

    // The detail panel should contain syllable division like "2 (fo/ra)"
    // Find the detail-row that mentions the syllable count + division
    const detailPanel = document.querySelector('.detail-panel');
    const text = detailPanel.textContent;
    expect(text).toMatch(/Syllables/);
    // Should contain count and division separated by /
    expect(text).toMatch(/fo\/ra/);
  });

  it('detail panel syllable division for single-syllable word shows no slashes', async () => {
    render(<App />);
    await waitForApp();

    // Search for "song" — a single-syllable word
    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'song' },
    });
    await waitFor(() => {
      const tds = document.querySelectorAll('.td-form');
      expect(tds.length).toBeGreaterThanOrEqual(1);
    });

    // Click to expand
    const cell = document.querySelector('.td-form');
    fireEvent.click(cell);
    await waitFor(() =>
      expect(document.querySelector('.detail-panel')).toBeInTheDocument()
    );

    const detailPanel = document.querySelector('.detail-panel');
    const text = detailPanel.textContent;
    // Should show "Syllables 1 (song)" — no / between syllables
    expect(text).toMatch(/Syllables/);
    expect(text).toContain('(song)');
  });
});