### dear ({affection})
| Field | Value |
|---|---|
| Kilor Form | arma |
| Type | root |
| Derivation Mask | NA |
| Consensus Prefix | a- |
| Meaning | [{"gloss": "dear, beloved", "pos": "N"}, {"gloss": "dear, beloved, endearing", "pos": "A"}] |
| Notes | arma- affection family head. a- (living/person-oriented). Distinguish argonna (love). |

### wife ({affection})
| Field | Value |
|---|---|
| Kilor Form | morsa |
| Type | root |
| Derivation Mask | N |
| Consensus Prefix | a- |
| Meaning | [{"gloss": "wife, spouse (female)", "pos": "N"}] |
| Notes | Kinship term. a- (living). |

### darling ({affection})
| Field | Value |
|---|---|
| Kilor Form | armati |
| Type | root |
| Derivation Mask | NA |
| Consensus Prefix | a- |
| Meaning | [{"gloss": "darling, sweetheart", "pos": "N"}, {"gloss": "darling, cherished", "pos": "A"}] |
| Notes | arma- family. NOT arma+ti (ti = "you" pronoun); fossilised root. a-. |

### text ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiro |
| Type | root |
| Derivation Mask | NA |
| Consensus Prefix | o- |
| Meaning | [{"gloss": "text, written content", "pos": "N"}, {"gloss": "textual, written", "pos": "A"}] |
| Notes | kir- writing family head. o- (abstract content). Distinguish berat (word), kira (book). |

### paragraph ({writing})
| Field | Value |
|---|---|
| Kilor Form | kirolote |
| Type | compound-mono |
| Components | kiro + lote |
| Pattern | collective |
| Rule Ref | rules/3-subsystems/compounding.md §I-G |
| Derivation Mask | N |
| Consensus Prefix | o- |
| Meaning | [{"gloss": "paragraph, a block of text", "pos": "N"}] |
| Notes | kiro (text) + lote (group). Non-human lote → head-class o-. First generalised non-human lote compound (spec §I-G amended). |

### section ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiroli |
| Type | compound-mono |
| Components | kiro + roli |
| Pattern | relational |
| Rule Ref | rules/3-subsystems/compounding.md §III |
| Derivation Mask | N |
| Consensus Prefix | o- |
| Meaning | [{"gloss": "section, a portion of text", "pos": "N"}] |
| Notes | kiro (text) + roli (a lot / many) = a lot of text. o-. Not kiro+li (li = "if" subordinator). |

### writer ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiromae |
| Type | compound-mono |
| Components | kiro + maeha |
| Pattern | agent |
| Rule Ref | rules/3-subsystems/compounding.md §I |
| Derivation Mask | N |
| Consensus Prefix | a- |
| Meaning | [{"gloss": "writer, author", "pos": "N"}] |
| Notes | kiro (text) + maeha (person). Agent. a- (living). |

### article ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiroparam |
| Type | compound-mono |
| Components | kiro + param |
| Pattern | result |
| Rule Ref | rules/3-subsystems/compounding.md §I |
| Derivation Mask | N |
| Consensus Prefix | e- |
| Meaning | [{"gloss": "article, a written piece", "pos": "N"}] |
| Notes | kiro (text) + param (result) = lexicalised article. e- (crafted head, cf. tesar param). |

### writing ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiropar |
| Type | compound-mono |
| Components | kiro + par |
| Pattern | process |
| Rule Ref | rules/3-subsystems/compounding.md §I |
| Derivation Mask | N |
| Consensus Prefix | e- |
| Meaning | [{"gloss": "writing, the act/process of writing", "pos": "N"}] |
| Notes | kiro (text) + par (process). e- (process head, cf. tesakpar). |

### pen ({writing})
| Field | Value |
|---|---|
| Kilor Form | kirotek |
| Type | compound-mono |
| Components | kiro + tek |
| Pattern | instrument |
| Rule Ref | rules/3-subsystems/compounding.md §I |
| Derivation Mask | N |
| Consensus Prefix | e- |
| Meaning | [{"gloss": "pen, a writing instrument", "pos": "N"}] |
| Notes | kiro (text) + tek (tool). instrument. e- (crafted). |

### book ({writing})
| Field | Value |
|---|---|
| Kilor Form | kira |
| Type | root |
| Derivation Mask | N |
| Consensus Prefix | e- |
| Meaning | [{"gloss": "book, a bound volume", "pos": "N"}] |
| Notes | kira- book subfamily head. e- (crafted artifact). Distinguish kiro (text). Near-collision kora/lira/okira (d=1, diff domains — tolerated). |

### chapter ({writing})
| Field | Value |
|---|---|
| Kilor Form | kiraruson |
| Type | compound-mono |
| Components | kira + ruson |
| Pattern | property |
| Rule Ref | rules/3-subsystems/compounding.md §III |
| Derivation Mask | N |
| Consensus Prefix | ae- |
| Meaning | [{"gloss": "chapter, a separate section of a book", "pos": "N"}] |
| Notes | kira (book) + ruson (separate) = separate part of book. ae- (ruso- family head-inherit). |

### library ({writing})
| Field | Value |
|---|---|
| Kilor Form | kirapos |
| Type | compound-mono |
| Components | kira + poska |
| Pattern | location |
| Rule Ref | rules/3-subsystems/compounding.md §I |
| Derivation Mask | N |
| Consensus Prefix | ae- |
| Meaning | [{"gloss": "library, a book-place", "pos": "N"}] |
| Notes | kira (book) + poska (place/location head). location. ae- (earth). |
---

## PENDING A–J REVIEW — Local-case particles (grammar proposal 2026-08-23)

These four forms were designed during the case-function discussion. They are **proposed entries only** — none are inserted into the DB. To actually add them, confirm fields **A–J** (per the 4-phase workflow in `4-meta/word-creation-pipeline.md`) so `python kilor.py add` can process them.

### at ({spatial})

| Field | Value |
|---|---|
| Kilor Form | posne |
| Type | function |
| POS | ADP |
| Consensus Prefix | o- |
| Meaning | at (neutral point-locative) |
| Notes | PENDING A–J. Locative #1. `pos` (location head from `poska`) + `-ne`. `[landmark]-GEN posne` = "at the landmark". Complements `ikne` (in) / `rapne` (on). See `3-subsystems/spatials.md` §III, §IV-D. |

### into ({spatial})

| Field | Value |
|---|---|
| Kilor Form | ikte |
| Type | function |
| POS | ADP |
| Consensus Prefix | o- |
| Meaning | into (motion goal into the interior) |
| Notes | PENDING A–J. Illative #6. `ik` (in root) + `te` (goal particle). `[goal] ikte` + motion verb (`aug`). Goal split: `te` dative ≠ `tene` allative ≠ `ikte` illative. See `3-subsystems/spatials.md` §IV-D. |

### as ({relation})

| Field | Value |
|---|---|
| Kilor Form | raus |
| Type | function |
| POS | ADP |
| Consensus Prefix | o- |
| Meaning | as / in the capacity of (role) |
| Notes | PENDING A–J. Essive #9. Preposed before the role noun. Distinct from `les` (equative "as … as") and `-ius` (similative "like"). See `1-nominals/cases.md` §V-A. |

### become ({relation})

| Field | Value |
|---|---|
| Kilor Form | lik |
| Type | function |
| POS | ADP |
| Consensus Prefix | o- |
| Meaning | become / turn into (resultant state) |
| Notes | PENDING A–J. Translative #10. Preposed before the result noun: `SUBJ lik RESULT`. Contrast `lifa` (process verb "transform"); `lik` is the resultative marker. See `1-nominals/cases.md` §V-A. |