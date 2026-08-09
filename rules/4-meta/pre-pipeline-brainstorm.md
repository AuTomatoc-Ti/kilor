# Kilor Pre-Pipeline Brainstorm Guide

**Module:** Pre-pipeline word brainstorming & structured discussion
**Status:** Canonical
**Last updated:** 2026-08-09
**Version:** 1.2.0
**Depends on:** `4-meta/word-creation-pipeline.md`, `0-foundation/phonology.md`, `1-nominals/nouns-colour-prefix.md`, `3-subsystems/compounding.md`

---

## I. Purpose

This guide covers **Phase 0** — the structured discussion that happens BEFORE filling in `today.md`. A human provides brainstorm entries in a bare format; the agent works through each entry to resolve meaning/POS expansion, root vs compound, and colour prefix. Only after all three dimensions are settled does the word enter Phase 1 (`today.md`).

---

## II. User Input Format

The human provides brainstorm entries in this format:

```
{form}, {meaning}
```

Examples from this session:

| Input | Form | Brief Meaning |
|:--|:--|:--|
| `weikra, weak` | `weikra` | weak |
| `saelom, peace` | `saelom` | peace |
| `arse, ass` | `arse` | ass |
| `raekumlausta, requiem` | `raekumlausta` | requiem |

**Key properties of the input:**

| Property | Implication |
|---|---|
| Meaning is **brief** (1–2 words) | Must be expanded across NVAD in discussion |
| **No POS markers** provided | Agent determines POS scope per §IV heuristics |
| **No type** (root/compound) indicated | Agent determines per §VI rules |
| **No colour prefix** suggested | Agent runs 7-Question Filter per §V |

**POS scope for content words:** Generally stays within **NVAD**. Rare exceptions (function words with PRON, NUM, etc.) use the closed-class template — see `word-creation-pipeline.md` §III-B.

---

## III. The Three Discussion Dimensions

For each brainstorm entry, resolve in order:

| # | Dimension | Questions to Answer |
|:--|:--|:--|
| 1 | **Meaning & POS** | What POS senses naturally extend from the brief meaning? Which are core vs marginal? (§IV) |
| 2 | **Root vs Compound** | Is this a bare root, or a compound of existing roots? If compound: what components, what pattern? (§VI) |
| 3 | **Colour Prefix** | Run 7-Question Filter. Check for existing phonological-family words. Resolve filter vs family consistency. (§V) |

Discuss **one word at a time**. Don't batch decisions — each word has unique considerations.

---

## IV. POS Decision Heuristics

### A. Content Word POS Patterns

| Pattern | Typical Word Types | Examples |
|:--|:--|:--|
| **NVAD** | Core qualities, states, actions with natural N/V/A/D extensions | weak, peace, rest, song |
| **NAD** | Qualities where V is marginal or forced | greatness, art |
| **NV** | Tool/instrument with a unique tool→action mapping | hammer (to hammer is intrinsic) |
| **N** | Concrete objects, body parts, proper nouns, compound nouns | sword, arse, requiem |

### B. Tool N→V Test

A tool noun qualifies for a V sense **only if** the action is intrinsic to that specific tool:

| Tool | V? | Reasoning |
|:--|:--|:--|
| hammer → to hammer | ✅ | Repeated striking is unique to hammers |
| sword → to sword | ❌ | Slashing/stabbing is not sword-specific; `maliu` (knife) already covers cutting |

### C. Quality Word A/D

| Question | Answer |
|---|---|
| Is A natural? | Almost always — the adjective is the primary sense for quality words |
| Is D natural? | If A is natural, D follows (manner adverb via `-s` derivation) |
| Is V natural? | Only if "to make X" or "to become X" is a common usage (weaken ✅, pacify ✅, ?great-en ❌) |

### D. General Rules

- Body parts → **N-only** (no V/A/D)
- Compound nouns → typically **N-only**
- Abstract qualities → minimum **NA**, often **NAD**
- When in doubt, present options to the human and ask

---

## V. Colour Prefix Patterns

### A. The 7-Question Filter (ordered)

Run `1-nominals/nouns-colour-prefix.md` §V. The **first question that strongly resonates** nominates the prefix. Present the nomination to the human.

### B. Family Consistency Override

When a phonologically related word already exists with a known prefix, the family prefix may override the filter:

| New Word | Family Word | Family Prefix | Filter Pick | Final |
|:--|:--|:--|:--|:--|
| `tesar` (art) | `tesak` (create) | `e-` | `o-` | `e-` — match family |
| `mlaska` (sword) | `maliu` (knife) | `e-` | `y-` | `e-` — match family |

**Rule:** Present both options (filter pick + family match). Let the human decide.

### C. Always Check Existing Prefixes

Before suggesting a prefix, query the DB for related words:

```sql
SELECT form, consensus_prefix, pos_mask FROM words 
WHERE form LIKE '%{substring}%' OR gloss LIKE '%{keyword}%'
```

This catches:
- Phonological family words (`tesak` → `tesar`)
- Semantic neighbours (`miso` → `lausta`)
- Category conventions (body parts: external → `u-`, internal → `a-`)

---

## VI. Root vs Compound Decision

### A. When to Check

Before settling on "root," verify:

| Check | Query |
|:--|:--|
| Are the sub-parts existing roots? | Search DB for `{first_half}` and `{second_half}` |
| Is there a semantic neighbour? | Search DB for related glosses |
| Could this be a compound? | Apply compounding rules from `3-subsystems/compounding.md` |

### B. Compound Decision Flow

```
Is the meaning compositional (X + Y = XY)?
├─ No → bare root
└─ Yes →
    ├─ Do all component roots exist in DB?
    │   └─ No → cannot compound; use bare root or defer
    └─ Yes →
        ├─ Is it a §I defined head compound (param, pos, isra...)?
        │   └─ Yes → apply compound template
        └─ No (ordinary content-root compound) →
            ├─ Rule 5 upgrade check:
            │   ├─ A. Lexicalised cultural concept?
            │   ├─ B. Fused length ≤ 5 syllables?
            │   └─ C. No phonotactic block?
            ├─ All yes → mono upgrade
            └─ Any no → multi-word
```

### C. Example Decisions

| Word | Components | Decision | Reasoning |
|:--|:--|:--|:--|
| `raekumlausta` (requiem) | `raekum` + `lausta` | compound-mono | Rule 5: lexicalised + 4 syl + no block |
| `grail` | — | **deferred** | Needs "holy" modifier first; `pei` (cup) already exists |
| `tesar` (art) | — | root | `tesak` exists but art ≠ create-result compositionally |

### D. Word Deferral

Defer a word when:

| Condition | Example |
|:--|:--|
| A required modifier doesn't exist yet | `grail` → needs "holy/sacred" word; `pei` (cup) exists |
| The concept is better as a compound whose components don't exist yet | "voice" needed for "song" compounds |
| The concept is overly culture-specific and compositional | Excalibur, Mjolnir → not universal enough for Kilor roots |

### E. Near-Minimal-Pair Judgment

When two words differ by ≤ 2 Levenshtein distance (near-collision flag in Phase 2), do not reject automatically. Natural languages tolerate minimal pairs routinely when **semantic domains differ enough to prevent real-world confusion**:

| Language | Pair | Distance | Domains |
|:--|:--|:--|:--|
| English | hat / hot | 1 vowel | clothing vs temperature |
| Mandarin | mā / má / mǎ / mà | 0 segmentally | tone carries distinct meanings |

**Decision rule:**

| Situation | Verdict | Example |
|:--|:--|:--|
| Same semantic domain + same POS | ⚠️ Redesign form | — |
| Different semantic domain or different POS | ✅ Tolerate | `srata` (rotate, NVAD) vs `srato` (house, NV) — action vs physical object |

**Checklist when a near-collision flag triggers:**
- Are the two words in the same semantic domain? (e.g., both animals, both emotions)
- Do they share the same primary POS?
- Would a listener plausibly confuse them in the same sentence?

If the answer to all three is "yes," change the form. Otherwise, note the flag in `today.md` Notes and proceed.

---

## VII. today.md Pitfalls (Phase 1 Mistakes)

These errors were discovered during the Aug 2026 batch (weikra–sefe).

### A. Meaning Representation — JSON Array (no comma-splitting)

**`add.py` parses the `Meaning` field as a JSON array of `{"gloss", "pos"}` items; glosses are NOT comma-split.** This removes the old comma-splitting footgun entirely.

| ❌ Old (comma-split) | ✅ New (single array item) |
|:--|:--|
| `| Meaning (V) | to lance, pierce |` → 2 rows | `{"gloss": "to lance, pierce", "pos": "V"}` → 1 row |
| `| Meaning (A) | fruitful, bountiful |` → 2 rows | `{"gloss": "fruitful, bountiful", "pos": "A"}` |
| `| Meaning (N) | weakness |` | `{"gloss": "weakness", "pos": "N"}` |

**Rule:** Each array item is **ONE sense**. Group near-synonyms into a single item's `gloss` (a comma inside a gloss is preserved as part of that sense). Genuinely distinct senses get separate array items (each with its own `pos`).

### B. Missing Derivation Mask → NULL Prefix

**The `add.py` parser requires a `Derivation Mask` field to validate the consensus prefix.** The pipeline's content word template (§III-A) does not include this field, but the parser silently sets the prefix to NULL without it.

**Fix:** Always add `| Derivation Mask | NVAD |` (or appropriate mask) to every `today.md` entry.

### C. Descriptive Phrases as Glosses

Glosses should be short words or phrases — not sentence definitions.

| ❌ | ✅ |
|:--|:--|
| `the rear part of the human body` | `buttocks` |
| `a musical composition with vocals` | `song` |
| `produce musical sounds with the voice` | `to sing` |

### D. Post-Insertion Verification

After `python kilor.py add today.md`, verify:
- `consensus_prefix` is not NULL for N-mask words
- Meanings are not fragmented (check for phantom rows from comma-splitting)
- `pos_mask` matches expectations
- Compound components are stored (for compound entries)

---

## VIII. Quick Per-Word Checklist

Run this for every brainstorm entry:

```
□ 1. Query DB for existing related words (form substring + gloss keyword)
□ 2. Propose POS expansion (NVAD / NAD / NV / N)
     □ Tool N→V test if applicable
□ 3. Check sub-parts: could this be a compound?
     □ If yes: do components exist? Rule 5 check?
     □ If deferral needed: document why and skip
     □ Does the bare form collide with an existing derivational prefix? (e.g., `kon` vs prefix `kon-`)
□ 4. Run 7-Question Filter
     □ Check DB for family-word prefixes
     □ Present filter pick + family option (if different)
□ 5. Present summary to human: form, POS, type, prefix
     □ Lock after human confirms
□ 6. When writing today.md:
     □ Include | Derivation Mask | row
     □ Comma-safe glosses only
     □ Short glosses, no descriptive phrases
```

---

## IX. Cross-References

- **Full pipeline:** `4-meta/word-creation-pipeline.md`
- **7-Question Filter:** `1-nominals/nouns-colour-prefix.md` §V
- **Compound rules:** `3-subsystems/compounding.md`
- **Phonotactics:** `0-foundation/phonology.md`
- **Agent quickstart:** `data/AGENT-QUICKSTART.md`

---

*End of Pre-Pipeline Brainstorm Guide.*
