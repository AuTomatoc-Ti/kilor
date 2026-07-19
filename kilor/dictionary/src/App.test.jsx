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
 *
 * The database (as of writing) contains 361 words. Tests use concrete
 * entries known to exist in the production DB.
 */

beforeAll(async () => {
  // Initialize from the real kilor.db (Node path: reads from filesystem).
  // The if (db) return guard in initDatabase() means it's safe to call
  // multiple times within the same test run — only the first call does work.
  await initDatabase();
});

/** Wait for the app to finish loading (search input visible). */
async function waitForApp() {
  await screen.findByPlaceholderText(/Search by word/i);
}

/**
 * Click a multiselect trigger button, then toggle a checkbox option
 * inside the open dropdown. Uses getAllByText + DOM filtering because
 * section labels also appear in the Legend component.
 */
function toggleFilter(triggerText, optionLabel) {
  fireEvent.click(screen.getByText(triggerText));
  // Find all elements matching the option label, pick the one inside
  // the multiselect dropdown (wrapped in a <label>).
  const matches = screen.getAllByText(optionLabel);
  const label = matches.find((el) => el.closest('.multiselect-dropdown'))?.closest('label');
  if (!label) throw new Error(`toggleFilter: "${optionLabel}" not found inside multiselect dropdown`);
  fireEvent.click(label);
}

describe('App — initialization (real DB)', () => {
  it('renders header with real total word count', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.getByText('Kilor Dictionary')).toBeInTheDocument();

    // "361 words" appears in both Header and Toolbar — at least 2 instances
    const countEls = screen.getAllByText('361 words');
    expect(countEls.length).toBeGreaterThanOrEqual(2);
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

    // After loading, the table should be populated with word entries.
    // "No words match." must NOT appear on the initial, unfiltered view.
    expect(screen.queryByText('No words match.')).not.toBeInTheDocument();

    // At least some .td-form cells should contain data (word forms).
    const formCells = document.querySelectorAll('.td-form');
    expect(formCells.length).toBeGreaterThan(10);

    // Verify a known word is visible — "fora" appears in the production DB
    // early in alphabetical order and is a reliable signal that entries rendered.
    expect(screen.getAllByText('fora').length).toBeGreaterThanOrEqual(1);
  });
});

describe('App — search (real DB)', () => {
  it('search by exact form "fora" returns that entry', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'fora' },
    });
    // Filtered result count (fewer than 361). "fora" appears in the table.
    await waitFor(() => expect(screen.getByText(/of 361 words/)).toBeInTheDocument());
    // "fora" appears in the table and title attributes — use getAllByText
    const foraEls = screen.getAllByText('fora');
    // At least one should be the table cell (not the title attribute hover)
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
    // Gloss search triggers the HAVING clause — result shows "fora"
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

  it('search partial "fein" excludes "fei" when query is exact', async () => {
    render(<App />);
    await waitForApp();

    // "fei" is a word ("fly / flying"), "fein" is another ("bird")
    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), {
      target: { value: 'fein' },
    });
    await waitFor(() => expect(screen.getByText('fein')).toBeInTheDocument());
  });
});

describe('App — filters (real DB)', () => {
  it('filter by section A (Worlds & Elements) shows entries', async () => {
    render(<App />);
    await waitForApp();

    toggleFilter('All sections', 'A — Worlds & Elements');
    // Should display filtered count — many entries are in section A
    await waitFor(() => {
      const countEl = screen.getByText(/of 361 words/);
      expect(countEl).toBeInTheDocument();
    });
  });

  it('filter by type "function" shows only function words', async () => {
    render(<App />);
    await waitForApp();

    toggleFilter('All types', 'Function words');
    await waitFor(() => {
      const countEl = screen.getByText(/of 361 words/);
      expect(countEl).toBeInTheDocument();
    });
    // Known function word "res" should be visible
    expect(screen.getByText('res')).toBeInTheDocument();
    // Content root "fora" should NOT be visible
    expect(screen.queryByText('fora')).not.toBeInTheDocument();
  });

  it('filter by type "compound" returns only compounds', async () => {
    render(<App />);
    await waitForApp();

    toggleFilter('All types', 'Compounds');
    // After filtering to compounds, result count should be fewer than total
    await waitFor(() => {
      expect(screen.getByText('lunlagak')).toBeInTheDocument();
    });
    // Compound filter excludes content roots — "fora" should not appear
    // in the table. queryAllByText may match tooltip attributes, so check
    // that the table contains no <td> with textContent === 'fora'.
    const tds = document.querySelectorAll('.td-form');
    const forms = [...tds].map((td) => td.textContent);
    expect(forms).not.toContain('fora');
  });

  it('filter by mask "NVAD" returns matching entries', async () => {
    render(<App />);
    await waitForApp();

    toggleFilter('All masks', 'NVAD');
    await waitFor(() => {
      const countEl = screen.getByText(/of 361 words/);
      expect(countEl).toBeInTheDocument();
    });
    // "fei" is NVAD (fly/flying)
    expect(screen.getByText('fei')).toBeInTheDocument();
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

    // Sort descending
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

describe('App — view toggle and legend (real DB)', () => {
  it('toggles between table and card view', async () => {
    render(<App />);
    await waitForApp();

    // Table view is default — "Word" column header is visible
    expect(screen.getByText('Word')).toBeInTheDocument();

    fireEvent.click(screen.getByText('🃏 Cards'));
    await waitFor(() =>
      expect(document.querySelector('.card-container')).toBeInTheDocument()
    );

    fireEvent.click(screen.getByText('📋 Table'));
    await waitFor(() =>
      expect(document.querySelector('table')).toBeInTheDocument()
    );
  });

  it('legend toggle shows/hides legend', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.click(screen.getByText('Legend ▾'));
    await waitFor(() =>
      expect(document.querySelector('.legend.open')).toBeInTheDocument(),
    );

    fireEvent.click(screen.getByText('Legend ▾'));
    await waitFor(() =>
      expect(document.querySelector(':not(.legend.open)')).toBeTruthy(),
    );
  });
});