# Kilor Chat-Corpus Workflow

**Module:** Guided conversation practice → reusable corpus → pipeline
**Status:** Canonical
**Last updated:** 2026-09-01
**Version:** 1.0.0
**Depends on:** `0-foundation/grammar-syntax.md`, `1-nominals/nouns-colour-prefix.md`, `1-nominals/cases.md`, `2-predication/interrogative.md`, `2-predication/negation.md`, `4-meta/word-creation-pipeline.md`, `data/SCHEMA.md`

---

## I. Purpose

Kilor is practiced through **guided conversation** (role-play, dialogue, scenario
sketches) between the human and an LLM agent. The goal is **productive skill
building**: the human is forced to *retrieve* vocabulary and *apply* grammar in
context, which surfaces real lexical gaps and grammar blind spots far better than
reading wordlists.

This workflow turns every conversation into **reusable scaffolding**: new words go
to candidate vocab, confirmed sentences go to a checkable chat corpus, and the
SSOT (`data/kilor.db`) is never touched until the formal pipeline.

**Division of labour:** the agent writes nothing to `data/kilor.db` in this flow.
Words and sentences are staged in gitignored draft + tracked corpus files, then
formalized later by the human via the 4-phase pipeline.

---

## II. Invariants (non-negotiable)

| # | Invariant | Where enforced |
|---|---|---|
| 1 | `data/kilor.db` is **never modified** during conversation practice | `kilor/commands/chat_corpus.py` (read-only on SSOT) |
| 2 | `rules/` files are the **grammar authority** — never guessed | agent discipline, this file §IV |
| 3 | Word existence is checked by **`words.form` direct query**, not by `suggest` gloss search | `chat_corpus.py` `_load_ssot_forms` |
| 4 | Candidate words carry **no colour prefix** yet — decided in the formal pipeline | `draft-vocab.md` convention |
| 5 | Chat sentences list **every referenced word** in `[[ ]]` for existence checks | `data/chat-corpus.md` schema |

---

## III. Files in the Flow

| File | Role | Tracked? |
|---|---|---|
| `rules/*` | Grammar authority (read, never edit unless spec change) | git |
| `data/chat-corpus.md` | Human-editable source of confirmed sentences | git |
| `data/chat-corpus.db` | Staging DB mirroring SSOT `examples` (no FK) | git |
| `draft/draft-vocab.md` | Candidate words from chat (gitignored) | draft/ |
| `data/kilor.db` | SSOT lexicon — read-only here | git |

**Schema (`data/chat-corpus.db`):** table `sentences(id, kilor_text, english_text, source='chat')`
— intentionally mirrors the SSOT `examples` table so rows port cleanly later,
but stores free text with **no FK** so not-yet-final words are safe.

---

## IV. Agent Rules for Producing Kilor Sentences

Before writing any Kilor sentence, the agent must satisfy all of these:

1. **Check each word exists.** Query `data/kilor.db` `words.form` directly (or via
   the `meanings`/`examples` joins). `suggest` is an *English gloss* search — a
   miss there does **not** mean the word is absent.
2. **Verify uncertain grammar against `rules/`.** When unsure, check specifically:
   - word order & clause template → `0-foundation/grammar-syntax.md`
   - colour prefix & definiteness → `1-nominals/nouns-colour-prefix.md`
   - case suffixes & contrast rule → `1-nominals/cases.md`
   - question-word fronting → `2-predication/interrogative.md`
   - negation `nar` position → `2-predication/negation.md`
   Do not guess. Cite the file to the human when a rule is in play.
3. **Voiced rules on request.** When asked "why / is X right?", the agent answers
   by naming the rule and its source file, and may open it for cross-check.
4. **No invented grammar.** If a construct falls outside `rules/`, say so plainly
   and flag for `question.md`, rather than inventing a de-facto rule.
5. **Watch the two classic construction traps** (note: these are reminders of the
   correct behaviour, not a growing mistake log):
   - *Living vs abstract colour prefix*: people/animals use `a-`; abstract uses `o-`.
   - *Question words are fronted*: `ewei ti mug` (What do you want?), not mid-sentence.
---

## V. Word Cohosting During Chat

When a new word is coined/locked in conversation:

1. Add **one line** to `draft/draft-vocab.md` under a `# candidate word` section:
   `FORM, gloss (POS; POS)`
2. **Do not** assign a colour prefix, tone, inflections, or examples — those are
   decided/computed in the formal pipeline (see `4-meta/word-creation-pipeline.md`).
3. Note genuine lexicon gaps (e.g. "no cafe root, but `pos` exists as a compound
   head") as a `# NOTE (...)` comment, not inside the word line.
4. Keep it **one word per line** for clean parsing and diffing.

---

## VI. Recording & Syncing Sentences

Once a sentence is confirmed correct:

1. Append to `data/chat-corpus.md`:
   `KILOR = english`
   with **every referenced word** wrapped in `[[ ]]` for existence checks.
2. Run `python kilor.py chat-corpus`. This:
   - rebuilds `data/chat-corpus.db` from the source (idempotent),
   - strips `[[ ]]` and stores plain Kilor text,
   - restores each marked word to its **root** (strips colour prefix `a-`/`ae-`
     and case suffixes `ni/na/si/sa`) and reports status: `[OK]` (in SSOT),
     `[CANDIDATE]` (in draft-vocab only), or `[FLOATING]` (nowhere).
3. **Review the report.** Every `[FLOATING]` is a word not yet registered — list it
   for the human and propose adding to `draft-vocab.md` (if real) or investigate
   the root restoration.
4. A clean report (no `[FLOATING]`) means every referenced word is at least a
   candidate — the sentence is safe to keep long-term.

---

## VII. Lifecycle: From Chat to Dictionary

```
conversation → candidate word (draft-vocab.md) ──────────┐
              └─ confirmed sentence (chat-corpus .md/.db) ─┤
                                                           │
    formal pipeline (today.md → add → human A–J check) ◄───┘
                          │
                          ▼
                  data/kilor.db (SSOT) + examples (FK)
                          │
                          ▼
                dictionary app (WordDetailPage)
```

The staging `.db` mirrors `examples` so once candidate words pass the pipeline,
their confirmed sentences can be ported into the SSOT `examples` table with a
`source='corpus'` marker — feeding the dictionary app's example display.

---

## VIII. Anti-Patterns (fail loud, not hard-coded)

| Anti-pattern | Correct behaviour |
|---|---|
| Guessing a word order/particle instead of checking `rules/` | Open the spec file, cite it |
| Trusting `suggest` miss as "word absent" | Confirm via `words.form` direct query |
| Prefixing a candidate word, deferring only tone | Defer *nothing* — form + gloss only |
| Copying every past mistake into docs | General rules live in `rules/`; reuse the tool + workflow |
| Editing SSOT during conversation | Always route through the pipeline |

---

## IX. Cross-References

- **Formal word entry:** `4-meta/word-creation-pipeline.md`
- **Colour prefix 7-Question Filter:** `1-nominals/nouns-colour-prefix.md`
- **Case suffix contrast rule:** `1-nominals/cases.md` §II
- **Interrogative fronting:** `2-predication/interrogative.md`
- **Tooling:** `kilor/commands/chat_corpus.py`, `.clinerules/kilor.md` §0

---

*End of Chat-Corpus Workflow Specification.*