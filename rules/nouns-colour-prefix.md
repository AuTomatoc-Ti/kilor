# Kilor Nouns — The Chromatic Ontology System

**Module:** Noun Classification & Colour Prefix Morphology
**Status:** Canonical

---

## I. Core Philosophy

Traditional languages often bind nouns to rigid, arbitrary grammatical genders (masculine/feminine/neuter), forcing learners into a memorisation trap. Kilor replaces this with a **Cognitive Lens**.

The Colour Prefix does **not** describe the visual colour of an object, nor does it dictate a fixed dictionary category. It is **subjective metadata** — reflecting the speaker's immediate physical or cognitive perception of the noun. Because the root morpheme carries the core semantic weight, the system is **fault-tolerant**: choosing a "sub-optimal" prefix does not cause catastrophic misunderstanding.

---

## II. The 7 Ontological Prefixes

Each prefix is a single vowel (V template), aligning with Kilor's syllable structure.

| Colour | Ontology | Prefix | Core Intuition |
|:---|:---|:---|:---|
| **Red** | Alive / Energy / Fire | **`a-`** | Living, breathing, sentient, consuming energy |
| **Yellow** | Crafted / Tool / Order | **`e-`** | Human-made, designed, artificial, functional |
| **Blue** | Fluid / Vast / Boundary-less | **`i-`** | Water, gas, sky, ocean, continuous flows |
| **White** | Void / Abstract / Formless | **`o-`** | Purely conceptual, empty, formless, unknown |
| **Green** | Organic / Growth / Network | **`u-`** | Plants, fungi, ecosystems, living networks |
| **Black** | Mass / Dense / Unyielding | **`y-`** | Hard, heavy, dense matter; metal, deep rock |
| **Brown** | Earth / Boundary / Friction | **`ae-`** | Soil, wood, mundane physical boundaries |

> **Crucial:** The Diphthong Plural Shift from earlier drafts has been **removed**. Prefixes retain only their monophthong form regardless of number. Plurality is handled contextually — see `grammar-syntax.md` §VI.

---

## III. Phonological Status: The Proclitic Exemption

The Colour Prefix is an **External Proclitic**. It sits outside the phonological boundary of the root and:

- **Does not** trigger the Echo Rule (Vowel Harmony) — only the root's nucleus determines suffix vowel class
- **Does not** carry tone — all colour prefixes are pronounced with a flat mid-tone
- **Does not** count toward the syllable count for the last-3 tone domain (see `tone-prosody.md`) — only the root's syllables are counted
- Uses the **V (Standalone Vowel)** template — the hiatus between prefix and root (e.g., `a-akojra`) is phonotactically legal and creates a brief vowel hiatus; an optional glottal catch may be inserted in careful speech for emphasis

> **Example (4-syl compound):** `a-lujmisojla` (Red moon)
> The colour prefix `a-` is flat Mid and ignored for tone. The compound root `lujmisojla` (4 syllables, `lujmi` + `sojla`) carries two stitched H→L contours: M→H→M→L.
>
> **Example (Echo Rule):** `a-kojra-sa` (Red fire's)
> Prefix `a` is Front; root `kojra` contains Back vowel `o` → Genitive suffix uses Back variant `-sa`

---

## IV. The Definiteness Rule

The Colour Prefix is governed by Information Structure, not by arbitrary lexical assignment.

### A. Mandatory — Prefix Required

The prefix **must** be applied when:

1. The noun is preceded by an **article** (`a`/`an`/`the`) or a **determiner** (`this`/`that`)
2. The noun is the **first word of the sentence** (the Topic position)

In these states, the noun is "isolated" from the background flow and requires explicit ontological framing.

### B. Omitted — Prefix Dropped

The prefix is **dropped entirely** when the noun is a **Bare Noun** in the middle of a sentence, without an article or determiner preceding it. The noun becomes an unmarked, generic mass or concept.

> This syntactic drop also serves as the ultimate escape hatch for edge cases — if the speaker cannot classify the object, they may simply omit the prefix.

---

## V. The 7-Question Filter — Intuitive Classification

When a speaker must assign a prefix, they run the object through this checklist. The **first question that strongly resonates** dictates the prefix.

| # | Prefix | Question |
|:---|:---|:---|
| 1 | **White** `o-` | Is it abstract, empty, purely conceptual, or formless? *(math, time, soul, snow, clouds, blank space)* |
| 2 | **Blue** `i-` | Is it a fluid, gas, or vast space with no clear boundaries? *(water, wind, sky, ocean, smoke, continuous flows)* |
| 3 | **Red** `a-` | Is it alive, breathing, sentient, or fire? *(humans, animals, insects, fire, blood, consuming energy)* |
| 4 | **Green** `u-` | Is it a plant, fungus, or something that grows organically? *(trees, grass, crops, medicine, ecosystems)* |
| 5 | **Black** `y-` | Is it extremely hard, heavy, dense, or made of metal/deep rock? *(iron, diamonds, bedrock, heavy machinery, deep caves)* |
| 6 | **Brown** `ae-` | Is it made of soil, wood, dirt, or forms a mundane physical boundary? *(dirt, wood, leather, walls, doors, everyday rocks)* |
| 7 | **Yellow** `e-` | Is it crafted by humans, artificial, or designed as a tool? *(smartphones, books, clothes, vehicles, screens)* |

---

## VI. Edge-Case Resolution — 3-Tiered Hierarchy

When an object defies straightforward classification (e.g., *ice, sand, glass, blood, shadows*), the language resolves ambiguity through this hierarchy:

### Tier 1: Contextual Fluidity (Dominant)

The speaker chooses the colour based on the **immediate cognitive focus** in that specific sentence. The root noun guarantees understanding; the prefix acts as a "camera lens" highlighting a specific property.

> **Example (Ice):**
> `y-ice` (Black) → focus on its hard, impenetrable mass blocking a path
> `i-ice` (Blue) → focus on its true nature as frozen water

### Tier 2: Lexical Fossilisation (Community Shortcut)

For highly frequent, everyday objects, the community naturally develops a default classification. Beginners are taught these defaults as cognitive shortcuts, though Tier 1 remains technically permissible.

> **Example:** *Paper* defaults to **`e-paper`** (Yellow) — its primary identity is a human-crafted tool.

### Tier 3: The `Null` Fallback (White Default)

If a concept is purely abstract, entirely lacks physical form, or represents the unknown/void, it defaults to **White (`o-`)**. White acts as the `Null` or base class of Kilor's ontology.

> **Example:** *Syntax, Justice, Logic, Shadows, Echoes* → all default to **`o-`**

---

*End of Nouns & Colour Prefix Specification.*