**Module:** Section Taxonomy
**Status:** Canonical
**Last updated:** 2026-07-21
**Version:** 1.0.0
**Depends on:** None

---

## I. Overview

Every Kilor word belongs to exactly one of eight sections. The taxonomy partitions by ontological category — **what kind of entity or concept the word denotes** — not by traditional dictionary domain (nature, food, tools, etc.).

Sections are numbered 1–8, ordered from most concrete to most abstract. This ordering is intentional: the same precedence informs the tiebreak rule for polysemous words.

---

## II. Section Definitions

| # | Name | Denotes | Boundary Test |
|---|---|---|---|
| 1 | Concrete | Tangible matter: substances, objects, artifacts, buildings, materials, geographic features, celestial bodies | Could you touch it (in principle)? |
| 2 | Living | Organisms and their parts: plants, animals, body parts, life processes | Does it have biology? Is it part of something alive? |
| 3 | Action | Events, motions, changes, processes: what happens | Does it happen in time? Can it start/stop? |
| 4 | Quality | Properties, attributes, sensory qualities, conditions | Does it describe *how* something is? |
| 5 | Mental | Internal experience: cognition, emotion, perception, art | Does it exist only in a mind? Is it felt? |
| 6 | Relational | Positioning between entities: spatial, temporal, social, kinship, communication | Does it connect two things? Is it deictic? |
| 7 | Abstract | Ideas, concepts, values, systems, spirit, existence | Can you define it but not point to it? |
| 8 | Grammar | Closed-class operators: pronouns, numerals, question words, particles, modals, reflexives | Is it a language-internal tool, not a world-concept? |

---

## III. Tiebreak Rule

When a word has multiple glosses that would fall into different sections, assign the section with the **lowest code number** (most concrete).

Precedence: **1 > 2 > 3 > 4 > 5 > 6 > 7 > 8**

### Rationale

The most physical meaning of a word is its primary identity. A word that can mean both a substance and an action is fundamentally the substance first. This is deterministic — consistent across all words, requiring no subjective judgment.

### Examples

| Word | Glosses | Sections | Assigned |
|---|---|---|---|
| `fos` | ice (1), freeze (3) | 1, 3 | **1** — Concrete |
| `lumi` | light (n, 1), bright (4) | 1, 4 | **1** — Concrete |
| `fora` | fire (1) | 1 | **1** |
| `lir` | fish (2) | 2 | **2** |
| `fei` | fly (action, 3), flying (adj, 4) | 3, 4 | **3** — Action |
| `slu` | flower (2) | 2 | **2** |
| `miso` | music (5) | 5 | **5** — Mental (art = internal experience) |
| `lorrak` | language (6) | 6 | **6** — Relational (communication = connecting) |
| `isra` | idea (7) | 7 | **7** — Abstract |
| `ki` | I (pronoun, 8) | 8 | **8** — Grammar |

---

## IV. Section Mutually Exclusive Guarantee

The eight questions each section answers are fundamentally different:

| Section | Question |
|---|---|
| 1 — Concrete | "What is it made of?" |
| 2 — Living | "Is it alive?" |
| 3 — Action | "What happens?" |
| 4 — Quality | "How is it?" |
| 5 — Mental | "What is experienced inside?" |
| 6 — Relational | "What is its position relative to…?" |
| 7 — Abstract | "What does it mean?" |
| 8 — Grammar | "What does it do in the sentence?" |

No word can simultaneously answer two of these as its primary identity. A word's section is determined by asking these questions in order (1→8) and stopping at the first "yes."

---

## V. Implementation

The SSOT for section labels is `kilor/schema.py` — `SECTION_LABELS`. All consumers (export, status, dictionary UI) derive from this dict.

The `today.md` `Section (A-J)` field is a legacy artifact. Section is assigned by the wordlist domain via `SECTION_MAP` in `kilor/commands/add.py` (default: 7 — Abstract). Manual override requires editing the `SECTION_MAP` or post-insertion SQL.