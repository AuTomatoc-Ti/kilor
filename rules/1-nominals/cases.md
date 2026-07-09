# Kilor Cases — The 3-Case Syntactic Engine

**Module:** Syntactic Role Marking & Poetic Freedom
**Status:** Canonical
**Last updated:** 2026-07-09
**Version:** 1.0.0
**Depends on:** `0-foundation/grammar-syntax.md`

---

## I. Core Philosophy

Traditional case languages overwhelm learners with 10+ morphological slots. Kilor simplifies to exactly **3 cases**, mirroring the most intuitive grammatical mapping for learners: **I (Actor) / me (Target) / my (Owner)**.

This minimal system achieves two goals:

1. **Zero Cognitive Friction** — learners only need two suffixes. The subject (Nominative) is unmarked.
2. **Poetic Freedom** — case suffixes mark syntactic roles explicitly, so word order can be shuffled for rhythm, emphasis, and aesthetic beauty. In everyday casual SOV speech, the Accusative may be dropped for simplicity (see §III-A); in formal writing and non-SOV orders, all case suffixes are mandatory, ensuring full disambiguation.

---

## II. The 3-Case Paradigm

Case suffixes use simple CV (Consonant-Vowel) forms to maintain rhythmic purity.

| Case | Function | Front/Bright Suffix | Back/Deep Suffix | Phonetic Intuition |
|:---|:---|:---|:---|:---|
| **Nominative** | The Actor / Subject *(Who does it?)* | *(unmarked)* | *(unmarked)* | Zero effort. The default, grounded state. |
| **Accusative** | The Target / Object *(Who receives it?)* | **`-ni`** | **`-na`** | `n` is a nasal resonance — it phonetically flows *toward* a target. |
| **Genitive** | The Owner / Possession *(Whose? / "Of")* | **`-si`** | **`-sa`** | `s` is continuous fricative — it implies a lingering connection. |

### Contrastive Suffix Assignment

Suffixes use the vowel class **opposite** to the last syllable's nucleus of the **root**. This creates a pleasant front↔back alternation at the root-suffix boundary.

The colour prefix is an external proclitic — it sits outside the phonological boundary of the root and does **not** trigger or participate in the Contrastive Suffix Rule. Only the root's last-syllable nucleus determines suffix vowel class (see `1-nominals/nouns-colour-prefix.md` §III, `0-foundation/grammar-syntax.md` §II).

| Front Vowels (last syllable) | Back Suffix |
|:---|:---|
| e, i, y, ae, ei, eu, iu | `-na` (ACC), `-sa` (GEN) |

| Back Vowels (last syllable) | Front Suffix |
|:---|:---|
| a, o, u, ai, au, oi, ou | `-ni` (ACC), `-si` (GEN) |

> **Example (contrast):** `fojra` (fire, last vowel `a` = back) + Accusative → `fojrani` (front `-ni`)
> **Example (contrast):** `lujmi` (light, last vowel `i` = front) + Accusative → `lujmina` (back `-na`)
> **Example (contrast):** `fojra` (fire, last vowel `a` = back) + Genitive → `fojrasi` (front `-si`)
> **Example (contrast):** `lujmi` (light, last vowel `i` = front) + Genitive → `lujmisa` (back `-sa`)
> **Example (proclitic exemption):** `a-fojra` (Red-fire, prefix `a` = Front) + Genitive → `a-fojrasi` (front `-si`, not `-sa`). The prefix `a` is ignored; root's last vowel `a` (Back) selects front `-si`.

---

## III. Accusative Usage — Optional in Speech

The Accusative suffix (`-ni`/`-na`) has a **two-tier usage rule**:

### A. Optional — Everyday Speech (SOV Order)

When a sentence follows the **default SOV order**, the Accusative may be **dropped** in everyday conversation. The object's position between Subject and Verb already signals its role sufficiently.

> **Conceptual example (SOV speech):** `fojra lujmi tavka` — *lujmi* (light) is unambiguously the object by position.

### B. Mandatory — Formal Writing & Non-SOV Order

The Accusative becomes **mandatory** in two contexts:

1. **Formal writing** (even in SOV order) — for precision and clarity
2. **Any non-SOV word order** (OSV, VSO, or other poetic inversions) — because position no longer signals objecthood, the suffix is the sole disambiguator

> **Conceptual example (OSV):** `lujmina fojra tavka` — the `-na` on *lujmi* confirms it as the object despite being sentence-initial.

### C. Multi-Word Vocabs — Suffix Placement

When the noun receiving a case suffix is a **multi-word vocab** (a semantic unit composed of multiple orthographic words; see `0-foundation/grammar-syntax.md` §IV-B), the case suffix attaches **only to the last word** of the vocab. The earlier words remain unmarked.

> **Example (Accusative, multi-word vocab):** `lujmi sojla` (star-light) + Accusative → `lujmi sojlani` (star-light as object)
> **Example (Genitive, multi-word vocab):** `lujmi sojla` (star-light) + Genitive → `lujmi sojlasi` (star-light's / of the star-light)

The colour prefix (if present) attaches orthographically to the first word and does not affect suffix placement:

> **Example (with prefix):** `a-lujmi sojla` (Red-star-light) + Accusative → `a-lujmi sojlani`

---

## IV. Genitive Usage — Possession

The Genitive (`-si`/`-sa`) is the **only mechanism for expressing possession** in Kilor. There is no separate possessive particle or agglutinative possessive suffix.

### Single Possessor — Word Order Flexibility

The Genitive-marked possessor may appear before or after the possessed noun:

> `fojrasi lujmi` (fire's light) ≡ `lujmi fojrasi` (light of fire)

### Nested Possession — Fixed Recursive Order

When **multiple Genitive-marked nouns** chain together (nested possession), Kilor uses a **fixed recursive order** to prevent structural ambiguity: each possessor must **precede** what it owns.

```
[Possessor-GEN] [Possessed] → recursive nesting
```

In a chain, the outermost possessor comes first, followed by each successively nested pair:

> `kis fojrasi lujmi` = "my fire's light" — `kis` (my) owns `fojrasi` (fire's), which owns `lujmi` (light)
> 
> Parse: `[kis [fojrasi lujmi]]` — `kis` is the outermost possessor; `fojrasi` is nested inside

Free order (`lujmi fojrasi kis`) is **not valid** for nested possession — the fixed possessor-first recursive order disambiguates the nesting structure.

### Absence of Possessive Pronouns

There are no dedicated possessive pronouns (no equivalent to English *my*, *your*, *his*). Possession by pronoun is expressed by attaching the Genitive suffix to the pronoun root.

> **Pronoun exception:** Pronouns use **reduced case endings** — Accusative `-n` and Genitive `-s` — instead of the standard `-ni`/`-na` and `-si`/`-sa`. These endings are invariant (exempt from the Contrastive Suffix Rule). See `1-nominals/pronouns.md` §III for the full declension table.
---

## V. Oblique Particles & Prepositions

Kilor intentionally restricts the case system to 3 slots. All other semantic roles are handled by a set of **analytic prepositions** — standalone particles that precede their noun phrase. These are closed-class function words: 1–2 syllables, toneless, no `j`/`v`, exempt from the `-s` constraint.

### A. Oblique Prepositions

| Role | Meaning | Particle | Usage |
|:---|:---|:---|:---|
| **Dative** | to / for (recipient, direction) | **`te`** | Placed before the recipient/goal noun |
| **Comitative** | with / together (companion) | **`mer`** | Placed before the companion noun |
| **Instrumental** | by / with / using (means, tool, agent) | **`sy`** | Placed before the instrument/agent noun |
| **Ablative** | from (origin, source) | **`ar`** | Placed before the source noun |
| **Locative-relational** | between | **`tilpe`** | Placed before the location/reference noun |

### B. Conjunctions

Conjunctions connect words, phrases, or clauses:

| Role | Meaning | Particle |
|:---|:---|:---|
| **Additive** | and | **`ei`** |
| **Alternative** | or | **`po`** |
| **Adversative** | but | **`amer`** |

### C. Subordinators

Subordinator particles introduce adverbial clauses (when/because/if). See `2-predication/subordination.md` for full clause-embedding rules.

| Role | Meaning | Particle |
|:---|:---|:---|
| **Temporal** | when / while | **`tu`** |
| **Conditional** | if | **`li`** |
| **Causal** | because | **`aiga`** |
| **Concessive** | although | **`hoskar`** |

### D. Comparative Particles

Comparative particles mark the standard of comparison and form comparative, equative, and superlative constructions. See `3-subsystems/comparatives.md` for full usage rules and example sentences.

| Role | Meaning | Particle |
|:---|:---|:---|
| **Comparative** | than | **`tor`** |
| **Equative** | as | **`les`** |
| **Superlative** | most | **`torra`** |
| **Intensified comparative** | much more than | **`wetor`** |
| **Restrictive** | among / among all | **`mangus`** |

These particles are **standalone words** that sit outside the case suffix system. They do not participate in the Contrastive Suffix Rule and carry flat mid-tone.

### E. Passive `sy`

The instrumental particle **`sy`** (§V-A) is extended to serve as the **passive marker** — a valency-reducing operation that promotes the patient to subject and demotes the agent to an optional oblique. This follows the same design logic as English "by" or Chinese 被: one particle handles both instrumental ("with/by a tool") and passive-agent ("by someone").

`sy` occupies a fixed position between the patient (promoted to unmarked NOM) and the verb phrase. Three usage patterns are distinguished by what follows `sy`:

| Usage | Pattern | Example |
|:---|:---|:---|
| **Instrumental** (active SOV) | `Agent object-ACC sy instrument verb` | `ki bau-ni sy maliu cut.` — "I cut bread with a knife." |
| **Passive, agent deleted** | `Patient sy verb` | `hawu sy tavka.` — "The animal was eaten." |
| **Passive, agent expressed** | `Patient sy agent verb` | `hawu sy a-fojra tavka.` — "The animal was eaten by the fire." |

> **Design notes:**
> - When the agent is expressed after `sy`, it carries no case suffix — `sy` itself marks the agent's oblique role. The verb carries no morphological change; valency reduction is signalled entirely by `sy`.
> - The patient is unmarked (NOM default), occupying the subject slot.
> - The listener disambiguates `sy`'s function via what follows it: a tool noun in an active SOV frame → instrumental; a verb (or agent + verb) after the patient → passive.
> - In the agent-deleted pattern, OSV word order (§I-B of `0-foundation/grammar-syntax.md`) would place the patient before the verb without `sy` — but this is **topicalisation** (agent is still present and marked NOM elsewhere), not agent deletion. Passive `sy` is the only mechanism for structurally omitting the agent.

---

## VI. Phonological Integration — The Tone Lock Rule

When a case suffix is attached to a root, the tonal architecture of the root is completely preserved:

- The tone marker (`j` or `v`) **never migrates**
- It remains ontologically locked to its original anchor syllable
- The case suffix itself is pronounced with a **neutral, flat mid-tone**
- The case suffix does **not** count toward the last-3 tone domain (see `0-foundation/tone-prosody.md`)

> **Example:** `aujli` (noun, 2 syllables, H(`j`)→L) + Genitive `-sa` → `aujlisa`
> The `j` stays locked on `au`; `-sa` is flat mid-tone.

---

*End of Cases Specification.*
