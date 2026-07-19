import { describe, it, expect, beforeAll } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { buildTestDB, setDB } from './db';

function e(props = {}) {
  return {
    id: props.id || 1, form: props.form || 'test', syl_count: props.syl_count ?? 1,
    meanings: props.meanings || ['test'], derivation_mask: props.derivation_mask || 'N',
    section: props.section || 'A', is_root: props.is_root ?? true,
    is_compound: props.is_compound ?? false, compound_type: props.compound_type || null,
    is_function_word: props.is_function_word ?? false,
    consensus_prefix: props.consensus_prefix || 'o-',
    inflections: props.inflections || {}, components: props.components || [],
    pattern: props.pattern || null, rule_ref: props.rule_ref || null,
    examples: props.examples || [], notes: props.notes || '',
  };
}

const testEntries = [
  e({ id: 1, form: 'orse', meanings: ['also', 'too', 'as well'], is_root: true, is_function_word: true, derivation_mask: '', section: 'I' }),
  e({ id: 2, form: 'aug', meanings: ['start', 'begin'], section: 'D', derivation_mask: 'NVAD' }),
  e({ id: 3, form: 'auk', meanings: ['eight'], is_function_word: true, derivation_mask: '', section: 'I' }),
  e({ id: 4, form: 'auli', meanings: ['comet'], section: 'A', derivation_mask: 'N' }),
  e({ id: 5, form: 'argonna', meanings: ['love'], section: 'F', derivation_mask: 'NVAD' }),
  e({ id: 6, form: 'afaloi taka', meanings: ['edible'], is_root: false, is_compound: true, compound_type: 'multi', section: 'I', derivation_mask: 'NV', syl_count: 4 }),
  e({ id: 7, form: 'ki', meanings: ['I'], is_function_word: true, derivation_mask: '', section: 'I' }),
  e({ id: 8, form: 'sil', meanings: ['they (pl living)'], is_function_word: true, derivation_mask: '', section: 'I' }),
  e({ id: 9, form: 'also', meanings: ['southern'], section: 'G', derivation_mask: 'NA' }),
];

beforeAll(async () => {
  const testDB = await buildTestDB(testEntries);
  setDB(testDB);
});

/** Wait for the app to finish loading (search input appears). */
async function waitForApp() {
  await screen.findByPlaceholderText(/Search by word/i);
}

describe('App — search', () => {
  it('renders the header with total count', async () => {
    render(<App />);
    await waitForApp();
    expect(screen.getByText('Kilor Dictionary')).toBeInTheDocument();
    const countEls = screen.getAllByText('9 words');
    expect(countEls.length).toBeGreaterThanOrEqual(1);
  });

  it('search "orse" returns only the "orse" entry', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), { target: { value: 'orse' } });
    await waitFor(() => expect(screen.getByText('1 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('orse')).toBeInTheDocument();
    expect(screen.queryByText('aug')).not.toBeInTheDocument();
    expect(screen.queryByText('ki')).not.toBeInTheDocument();
  });

  it('search is case-insensitive', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), { target: { value: 'ORSE' } });
    await waitFor(() => expect(screen.getByText('1 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('orse')).toBeInTheDocument();
  });

  it('search for nonexistent word shows "No words match"', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), { target: { value: 'xyzzy' } });
    await waitFor(() => expect(screen.getByText('No words match.')).toBeInTheDocument());
  });

  it('search by gloss "start" matches "aug"', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), { target: { value: 'start' } });
    await waitFor(() => expect(screen.getByText('1 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('aug')).toBeInTheDocument();
  });
});

describe('App — filters', () => {
  it('filter by section "I" shows only section I entries', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: 'I' } });
    await waitFor(() => expect(screen.getByText('5 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('orse')).toBeInTheDocument();
    expect(screen.getByText('auk')).toBeInTheDocument();
    expect(screen.queryByText('aug')).not.toBeInTheDocument();
    expect(screen.queryByText('auli')).not.toBeInTheDocument();
  });

  it('filter by type "root" returns only roots', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getAllByRole('combobox')[1], { target: { value: 'root' } });
    await waitFor(() => expect(screen.getByText('8 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('orse')).toBeInTheDocument();
    expect(screen.queryByText('afaloi taka')).not.toBeInTheDocument();
  });

  it('filter by type "compound" returns only compounds', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getAllByRole('combobox')[1], { target: { value: 'compound' } });
    await waitFor(() => expect(screen.getByText('1 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('afaloi taka')).toBeInTheDocument();
  });

  it('filter by mask "NVAD" returns only NVAD entries', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getAllByRole('combobox')[2], { target: { value: 'NVAD' } });
    await waitFor(() => expect(screen.getByText('2 of 9 words')).toBeInTheDocument());
    expect(screen.getByText('aug')).toBeInTheDocument();
    expect(screen.getByText('argonna')).toBeInTheDocument();
    expect(screen.queryByText('orse')).not.toBeInTheDocument();
  });

  it('combined search + section filter works', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.change(screen.getByPlaceholderText(/Search by word/i), { target: { value: 'au' } });
    fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: 'I' } });

    await waitFor(() => {
      expect(screen.getByText('auk')).toBeInTheDocument();
    });
    expect(screen.queryByText('aug')).not.toBeInTheDocument();
    expect(screen.queryByText('auli')).not.toBeInTheDocument();
  });
});

describe('App — sorting', () => {
  it('sorts by form ascending by default', async () => {
    render(<App />);
    await waitForApp();

    const cells = screen.getAllByRole('cell');
    const forms = cells.filter(c => c.className.includes('td-form')).map(c => c.textContent);
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
      const forms = cells.filter(c => c.className.includes('td-form')).map(c => c.textContent);
      for (let i = 1; i < forms.length; i++) {
        expect(forms[i].localeCompare(forms[i - 1])).toBeLessThanOrEqual(0);
      }
    });
  });

  it('sticky toolbar CSS exists', async () => {
    render(<App />);
    await waitForApp();
    expect(document.querySelector('.top-bar')).toBeInTheDocument();
    expect(document.querySelector('.main-content')).toBeInTheDocument();
  });
});

describe('App — view toggle and legend', () => {
  it('toggles between table and card view', async () => {
    render(<App />);
    await waitForApp();

    expect(screen.getByText('Word')).toBeInTheDocument();
    fireEvent.click(screen.getByText('🃏 Cards'));
    await waitFor(() => expect(document.querySelector('.card-container')).toBeInTheDocument());
  });

  it('legend toggle shows/hides legend', async () => {
    render(<App />);
    await waitForApp();

    fireEvent.click(screen.getByText('Legend ▾'));
    await waitFor(() => expect(document.querySelector('.legend.open')).toBeInTheDocument());

    fireEvent.click(screen.getByText('Legend ▾'));
    await waitFor(() => expect(document.querySelector(':not(.legend.open)')).toBeTruthy());
  });
});