#!/usr/bin/env python3
"""
Kilor Lexicon Management Tool.

Usage:
  python kilor.py next [--count N]    Generate today's translation template
  python kilor.py add --file FILE     Process filled-in template, validate, add to lexicon
  python kilor.py check               Validate all entries in lexicon.csv
  python kilor.py status              Print lexicon statistics
  python kilor.py suggest WORD        Suggest how a word should be handled (root/compound/derivation)
"""

import csv
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "lexicon.csv")
WORDLIST_DIR = os.path.join(SCRIPT_DIR, "wordlist")

# ── Constants ───────────────────────────────────────────────────────────

VOWELS = set('aeiouy')
DIPHTHONGS = {'ai','au','ei','eu','iu','oi','ou'}
CORE_CONS = set('pbmfwtdnslrckgh')
START_ONLYS = {'sh','ch','th','sl','kl','tl','bl','ml'}
END_ONLYS = {'ng','x'}

CONSTRAINT_CHEATSHEET = """
Phonotactic constraints:
  - No 'j' or 'v' in bare roots (reserved for tone)
  - Syllables: CV, CVC, VC, V only — no consonant clusters
  - 1-2 syllable roots must NOT end in 's' (except closed-class function words)
  - 3+ syllable roots MAY end in 's'
  - Start-only onsets: sh, ch, th, sl, kl, tl, bl, ml (word-initial only)
  - Ending-only consonants: ng, x (word-final only)
"""

# ── Lexicon I/O ─────────────────────────────────────────────────────────

def load_lexicon():
    """Load lexicon.csv into list of dicts."""
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_lexicon(rows):
    """Save list of dicts back to lexicon.csv."""
    fieldnames = ["bare_root","syl","meaning","category","section","noun","verb",
                  "adjective","adverb","consensus_prefix","is_function_word","notes"]
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# ── Validation ──────────────────────────────────────────────────────────

def validate_root(root):
    """Validate a bare root against phonotactics. Returns (is_valid, error_message)."""
    if not root:
        return False, "empty root"
    
    # Check for j/v
    if 'j' in root or 'v' in root:
        return False, f"root '{root}' contains 'j' or 'v' (reserved for tone)"
    
    # Count syllables
    syl_count = count_syllables(root)
    if syl_count == 0:
        return False, f"root '{root}' has no vowel nucleus"
    if syl_count > 5:
        return False, f"root '{root}' has {syl_count} syllables (max 5)"
    
    return True, ""

# ── -s Exception Whitelist ──────────────────────────────────────────────

# Content roots that end in -s despite being 1-2 syllables. These are
# exceptional: their noun/adj forms are the same bare root (the -s is
# part of the root, not the derivational suffix).
S_FINAL_WHITELIST = {'gus', 'fos'}

def validate_content_root(root):
    """Validate a content root (not function word). Adds -s constraint."""
    valid, err = validate_root(root)
    if not valid:
        return False, err
    syl_count = count_syllables(root)
    if 1 <= syl_count <= 2 and root.endswith('s'):
        if root not in S_FINAL_WHITELIST:
            return False, f"root '{root}' is {syl_count}-syllable and ends in 's' (-s is reserved for derivation)"
    return True, ""

def validate_row(row, all_bare_roots=None):
    """Validate a full lexicon row. Returns (is_valid, error_message).
    all_bare_roots: set of existing bare roots to check duplicates against (optional).
    """
    root = row.get('bare_root', '').strip()
    if not root:
        return False, "missing bare_root"
    
    valid, err = validate_root(root)
    if not valid:
        return False, err
    
    if not row.get('meaning', '').strip():
        return False, "missing meaning"
    
    if all_bare_roots is not None:
        # Count occurrences of this root across all rows
        if all_bare_roots.get(root, 0) > 1:
            return False, f"duplicate root '{root}'"
    
    return True, ""

# ── Syllable Counting ───────────────────────────────────────────────────

def count_syllables(word):
    """Count vowel nuclei in a Kilor word."""
    count = 0
    i = 0
    while i < len(word):
        if word[i] in VOWELS:
            count += 1
            if word[i:i+2] == 'ae':
                i += 2
            elif i+1 < len(word) and word[i:i+2] in DIPHTHONGS:
                i += 2
            else:
                i += 1
        else:
            i += 1
    return count

def split_syllables(word):
    """Greedy left-to-right syllable parser."""
    n = len(word)
    if n == 0:
        return []
    
    syllables = []
    i = 0
    while i < n:
        start = i
        onset = ''
        
        # Onset
        if i == 0 and i+2 <= n and word[i:i+2] in START_ONLYS:
            onset = word[i:i+2]
            i += 2
        elif i < n and word[i] in CORE_CONS:
            onset = word[i]
            i += 1
        
        # Nucleus
        if i >= n:
            raise ValueError(f"incomplete syllable in '{word}' at position {i}")
        nucleus_start = i
        if word[i] in VOWELS:
            if word[i:i+2] == 'ae':
                i += 2
            elif i+1 < n and word[i:i+2] in DIPHTHONGS:
                i += 2
            else:
                i += 1
        nucleus = word[nucleus_start:i]
        
        # Coda
        coda = ''
        if i < n:
            if i+2 <= n and word[i:i+2] in END_ONLYS:
                coda = word[i:i+2]
                i += 2
            elif word[i] in CORE_CONS:
                coda = word[i]
                i += 1
        
        syllables.append(onset + nucleus + coda)
    
    return syllables

# ── Suggestion Engine ───────────────────────────────────────────────────

def suggest_handling(word, lexicon):
    """Suggest how an English concept should be handled: new root, compound, or derivation."""
    suggestions = []
    
    # Check if it's an adjective that could derive from an existing noun
    # Common adjective patterns: X-ish, X-y, X-ful, X-less
    for row in lexicon:
        if row.get('is_function_word') == 'true':
            continue
        meaning = row['meaning'].split('/')[0].strip()
        bare = row['bare_root']
        cat = row.get('category', '')
        
        # If existing noun/verb, suggest adjective/adverb derivation
        if cat in ('n', 'na', 'nv'):
            suggestions.append(f"  Adjective via {bare} + -s → {row['adjective']} (from noun '{meaning}')")
        if cat in ('v', 'nv'):
            suggestions.append(f"  Adverb via {bare} + -s → {row['adverb']} (from verb '{meaning}')")
    
    # Check for potential compounds
    # Look for compound candidates (2-word English concepts)
    for row1 in lexicon:
        m1 = row1['meaning'].split('/')[0].strip()
        for row2 in lexicon:
            m2 = row2['meaning'].split('/')[0].strip()
            if m1 != m2:
                suggestions.append(f"  Compound: {row1['bare_root']} ({m1}) + {row2['bare_root']} ({m2})")
    
    return suggestions[:10]  # Cap suggestions

def find_related_roots(word, lexicon):
    """Find existing roots semantically related to the given word."""
    # Simple keyword matching
    related = []
    for row in lexicon:
        if row.get('is_function_word') == 'true':
            continue
        meaning = row['meaning'].lower()
        bare = row['bare_root']
        # Check word overlap
        word_parts = set(word.lower().split())
        meaning_parts = set(meaning.replace('/', ' ').split())
        if word_parts & meaning_parts:
            related.append(f"  {bare} = {row['meaning']} ({row.get('category','?')})")
    return related[:8]

# ── next command ────────────────────────────────────────────────────────

def cmd_next(count=20):
    """Generate today's translation template."""
    lexicon = load_lexicon()
    existing_meanings = {row['meaning'].strip().lower() for row in lexicon}
    existing_roots = {row['bare_root'] for row in lexicon}
    
    # Read all wordlists
    words_to_translate = []
    wordlist_files = sorted(os.listdir(WORDLIST_DIR)) if os.path.exists(WORDLIST_DIR) else []
    
    for wl_file in wordlist_files:
        if not wl_file.endswith('.txt'):
            continue
        path = os.path.join(WORDLIST_DIR, wl_file)
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('|')
                if len(parts) >= 1:
                    english = parts[0].strip()
                    category = parts[1].strip() if len(parts) >= 2 else "general"
                    if english.lower() not in existing_meanings:
                        words_to_translate.append((english, category))
    
    if not words_to_translate:
        print("All words in wordlists have been translated! Add more wordlist files or create new ones.")
        return
    
    # Take the requested count
    batch = words_to_translate[:count]
    
    # Build today's template
    today_header = f"""# Kilor Translation — {datetime.now().strftime('%Y-%m-%d')}
# Fill in the Kilor column. Leave 'Decision' blank — the add command will classify.
# Decision options (auto-detected if blank): root / compound / derivation
# Constraints reminder: no j/v in bare roots; 1-2 syl roots cannot end in s

## Existing Roots for Reference ({len(lexicon)} total)

"""
    # List recent relevant roots
    ref_roots = defaultdict(list)
    for row in lexicon[-20:]:
        ref_roots[row.get('section', '?')].append(row)
    
    output = [today_header]
    
    for english, category in batch:
        # Find related roots
        related = find_related_roots(english, lexicon)
        related_str = "\n".join(related) if related else "  (none found)"
        
        output.append(f"""---
### {english} ({category})

| Field | Value |
|---|---|
| Kilor Root |  |
| Syllable Count |  |
| Category (n/v/a/av/nv/na) |  |
| Section (A-J) |  |
| Decision (root/compound/derivation) |  |
| Notes |  |

**Related existing roots:**
{related_str}
""")
    
    output.append(f"---\n\n*{len(batch)} words to translate. Run: python kilor.py add --file today.md when done.*")
    
    # Write to today.md
    today_path = os.path.join(SCRIPT_DIR, "today.md")
    with open(today_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Generated today.md with {len(batch)} words to translate.")
    print(f"Words remaining in queue: {len(words_to_translate) - len(batch)}")

# ── add command ─────────────────────────────────────────────────────────

def cmd_add(filepath):
    """Process a filled-in today.md and add entries to lexicon."""
    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse entries from the markdown
    entries = []
    current_english = None
    current_category = None
    
    for line in content.split('\n'):
        line = line.strip()
        # Match section headers like "### fire (body)"
        m = re.match(r'^### (.+?) \((.+?)\)$', line)
        if m:
            current_english = m.group(1).strip()
            current_category = m.group(2).strip()
            continue
        
        # Match table rows for Kilor Root
        if '| Kilor Root |' in line and current_english:
            # Extract value from the next line or same line
            parts = line.split('|')
            if len(parts) >= 3:
                value = parts[2].strip()
                if value and value != ' ':
                    entries.append({
                        'english': current_english,
                        'category': current_category,
                        'root': value,
                    })
    
    # Now find the actual values from the markdown tables
    # Re-parse more carefully
    entries_clean = []
    current = None
    for line in content.split('\n'):
        line = line.strip()
        m_sec = re.match(r'^### (.+?) \((.+?)\)$', line)
        if m_sec:
            if current and current.get('root'):
                entries_clean.append(current)
            current = {'english': m_sec.group(1).strip(), 'domain': m_sec.group(2).strip()}
            continue
        
        if current:
            if '| Kilor Root |' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current['root'] = val
            elif '| Category' in line and 'n/v/a' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current['cat'] = val
            elif '| Syllable Count |' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val and val.isdigit():
                        current['syl'] = val
            elif '| Decision' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current['decision'] = val
            elif '| Notes |' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    val = parts[2].strip()
                    if val:
                        current['notes'] = val
    
    if current and current.get('root'):
        entries_clean.append(current)
    
    if not entries_clean:
        print("No entries found in today.md. Make sure you've filled in the Kilor Root column.")
        return
    
    # Process each entry
    lexicon = load_lexicon()
    added = 0
    errors = []
    
    for entry in entries_clean:
        root = entry.get('root', '')
        english = entry.get('english', '')
        domain = entry.get('domain', '?')
        
        if not root:
            errors.append(f"'{english}': no Kilor root provided")
            continue
        
        # Validate (content roots only — function words are added separately)
        valid, err = validate_content_root(root)
        if not valid:
            errors.append(f"'{root}' ({english}): {err}")
            continue
        
        # Check duplicates
        if any(r['bare_root'] == root for r in lexicon):
            errors.append(f"'{root}' ({english}): duplicate — already exists")
            continue
        
        # Determine syllable count, category
        syl = str(count_syllables(root))
        cat = entry.get('cat', 'n')
        decision = entry.get('decision', 'root')
        notes = entry.get('notes', decision)
        
        # Map domain to section letter
        section_map = {
            'body': 'B', 'people': 'B', 'action': 'D', 'food': 'C',
            'clothing': 'C', 'home': 'C', 'quality': 'E', 'nature': 'A',
            'animal': 'B', 'direction': 'G', 'tool': 'C', 'social': 'H',
            'general': 'I',
        }
        section = section_map.get(domain, 'I')
        
        # Build row
        row = {
            'bare_root': root,
            'syl': syl,
            'meaning': english,
            'category': cat,
            'section': section,
            'noun': root,
            'verb': root,
            'adjective': root + 's' if cat in ('n','na','nv','a') else root,
            'adverb': root + 's' if cat in ('v','nv','a') else root,
            'consensus_prefix': 'o-',
            'is_function_word': 'false',
            'notes': notes,
        }
        lexicon.append(row)
        added += 1
    
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
    
    if added > 0:
        save_lexicon(lexicon)
        print(f"\nAdded {added} entries to lexicon.csv.")
    
    print(f"Total entries: {len(lexicon)}")
    print("\n⚠️  Tone-marked forms (noun/verb/adjective/adverb columns) are placeholders.")
    print("Run: python kilor.py expand  to regenerate full tone-marked forms.")

# ── check command ───────────────────────────────────────────────────────

def cmd_check():
    """Validate all entries in lexicon.csv."""
    lexicon = load_lexicon()
    from collections import Counter
    bare_counts = Counter(r['bare_root'] for r in lexicon)
    
    errors = []
    seen = set()
    for row in lexicon:
        root = row.get('bare_root', '')
        if root in seen:
            continue
        seen.add(root)
        
        is_func = row.get('is_function_word', 'false') == 'true'
        
        # Use content-root validation for non-function words
        if is_func:
            valid, err = True, ""  # function words have their own rules
        else:
            valid, err = validate_content_root(root)
            if not err and not row.get('meaning', '').strip():
                err = "missing meaning"
            if not err and bare_counts.get(root, 0) > 1:
                err = f"duplicate root '{root}'"
        
        if not valid:
            errors.append(f"  {root}: {err}")
    
    if errors:
        print(f"{len(errors)} validation error(s):")
        for e in errors:
            print(e)
    else:
        print(f"✅ All {len(lexicon)} entries pass validation.")
    
    roots = sum(1 for r in lexicon if r.get('is_function_word') != 'true')
    func = sum(1 for r in lexicon if r.get('is_function_word') == 'true')
    print(f"  Content roots: {roots}")
    print(f"  Function words: {func}")

# ── status command ──────────────────────────────────────────────────────

def cmd_status():
    """Print lexicon statistics."""
    lexicon = load_lexicon()
    content = [r for r in lexicon if r.get('is_function_word') != 'true']
    func = [r for r in lexicon if r.get('is_function_word') == 'true']
    
    # By category
    cats = defaultdict(int)
    for r in content:
        cats[r.get('category', 'n')] += 1
    
    # By section
    secs = defaultdict(int)
    for r in content:
        secs[r.get('section', '?')] += 1
    
    # Syllable distribution
    syls = defaultdict(int)
    for r in content:
        syls[int(r.get('syl', '1'))] += 1
    
    print("=== Kilor Lexicon Status ===")
    print(f"Content roots: {len(content)}")
    print(f"Function words: {len(func)}")
    print(f"Total entries: {len(lexicon)}")
    print()
    print("-- By Category --")
    for cat in ['n','v','a','nv','na']:
        if cats[cat]:
            print(f"  {cat}: {cats[cat]}")
    print()
    print("-- By Section --")
    sections = {'A':'Worlds & Elements','B':'Living Things','C':'Physical Objects',
                'D':'Actions & Motion','E':'Qualities & States','F':'Mind & Emotion',
                'G':'Time & Space','H':'Social & Relational','I':'Abstract','J':'Sensation'}
    for s, name in sections.items():
        if secs[s]:
            print(f"  {s} ({name}): {secs[s]}")
    print()
    print("-- By Syllable Count --")
    for s in sorted(syls.keys()):
        print(f"  {s}-syl: {syls[s]}")
    
    # Progress toward targets
    print()
    print("-- Roadmap Progress --")
    targets = [(500, "Phase 1 — Basic Daily"), (1000, "Phase 2 — Functional"),
               (3000, "Phase 3 — Fluent Non-Native"), (4500, "Phase 4 — Professional"),
               (6000, "Phase 5 — Complete")]
    for target, label in targets:
        pct = len(content) / target * 100
        bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
        print(f"  {label:30s}: {bar} {len(content):>4}/{target:>4} = {pct:.1f}%")

# ── suggest command ──────────────────────────────────────────────────────

def cmd_suggest(word):
    """Suggest how a concept should be handled."""
    lexicon = load_lexicon()
    content = [r for r in lexicon if r.get('is_function_word') != 'true']
    
    print(f"\nSuggestions for '{word}':\n")
    
    # Check if already exists
    for r in lexicon:
        if word.lower() in r['meaning'].lower():
            print(f"⚠️  Already exists: {r['bare_root']} = {r['meaning']}")
            return
    
    # Check derivation candidates (adjective/adverb from existing roots)
    word_lower = word.lower()
    for r in content:
        meaning = r['meaning'].lower().split('/')[0].strip()
        bare = r['bare_root']
        cat = r.get('category', 'n')
        
        # Derivation suggestions
        if cat in ('n','na','nv'):
            adj_form = r.get('adjective', bare + 's')
            print(f"  Derivative (adj): {bare} + -s → {adj_form} (from {r['meaning']})")
        if cat in ('v','nv'):
            adv_form = r.get('adverb', bare + 's')
            print(f"  Derivative (adv): {bare} + -s → {adv_form} (from {r['meaning']})")
    
    # Find related roots
    related = find_related_roots(word, lexicon)
    if related:
        print(f"\n  Related existing roots:")
        for r in related:
            print(r)
    
    print(f"\n  → If none fit, coin a new root.")
    print(f"  → Or define as compound of: [root1] [root2] = '{word}'")

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'next':
        count = 20
        if '--count' in sys.argv:
            idx = sys.argv.index('--count')
            if idx + 1 < len(sys.argv):
                count = int(sys.argv[idx + 1])
        cmd_next(count)
    
    elif cmd == 'add':
        filepath = None
        if '--file' in sys.argv:
            idx = sys.argv.index('--file')
            if idx + 1 < len(sys.argv):
                filepath = sys.argv[idx + 1]
        if not filepath:
            filepath = os.path.join(SCRIPT_DIR, "today.md")
        cmd_add(filepath)
    
    elif cmd == 'check':
        cmd_check()
    
    elif cmd == 'status':
        cmd_status()
    
    elif cmd == 'suggest':
        if len(sys.argv) < 3:
            print("Usage: python kilor.py suggest WORD")
            return
        cmd_suggest(sys.argv[2])
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == '__main__':
    main()