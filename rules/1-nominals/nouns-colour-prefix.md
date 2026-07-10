# Kilor Nouns — The Chromatic Ontology System

**Module:** Noun Classification & Colour Prefix Morphology
**Status:** Canonical
**Last updated:** 2026-07-10
**Version:** 1.1.1
**Depends on:** `0-foundation/philosophy.md` (dual-concepts), `0-foundation/grammar-syntax.md` §IV-C (closed-class particles), `0-foundation/tone-prosody.md` (tone), `3-subsystems/colour-emotion.md` (emotional override on nouns)

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

> **Crucial:** The Diphthong Plural Shift from earlier drafts has been **removed**. Prefixes retain only their monophthong form regardless of number. Plurality is handled contextually — see `0-foundation/grammar-syntax.md` §VI.

### A. Hyphen — Mandatory Orthographic Rule

The hyphen between the colour prefix and the root is **mandatory** in written Kilor. It is never omitted. This ensures unambiguous parsing between the two-letter Brown prefix `ae-` and roots beginning with `/æ/` (`ae`):

| Written | Parsing |
|---|---|
| `ae-kora` | Brown prefix `ae-` + root `kora` |
| `a-ekora` | Red prefix `a-` + root `ekora` |
| `aekora` | Single bare root `aekora` — no prefix (generic/indefinite) |

Without the mandatory hyphen, `aekora` would be ambiguous: Brown-prefix `kora` vs bare root `aekora`. The hyphen eliminates this ambiguity entirely.

> **Exception — Question words:** Question words formed from `wei` with a colour prefix (`awei`, `ewei`, `iwei`, `owei`, `uwei`, `ywei`, `aewei`) are **exempt** from the mandatory hyphen rule. The merged form without a hyphen is the sole written form for question words. See `2-predication/interrogative.md` §II.

---

## III. Phonological Status: The Proclitic Exemption

The Colour Prefix is an **External Proclitic**. It sits outside the phonological boundary of the root and:

- **Does not** trigger the Contrastive Suffix Rule — only the root's last-syllable nucleus determines suffix vowel class
- **Does not** carry tone — all colour prefixes are pronounced with a flat mid-tone
- **Does not** count toward the syllable count for the last-3 tone domain (see `0-foundation/tone-prosody.md`) — only the root's syllables are counted
- Uses the **V (Standalone Vowel)** template — the hiatus between prefix and root (e.g., `a-akora`) is phonotactically legal and creates a brief vowel hiatus; an optional glottal catch may be inserted in careful speech for emphasis

> **Example (multi-word vocab):** `a-lumi sola` (Red star-light)
> The colour prefix `a-` is flat Mid and ignored for tone. The multi-word vocab `lumi sola` (2-syl noun + 2-syl noun) is toneless (flat mid).
>
> **Example (Contrastive Suffix Rule):** `a-fora-si` (Red fire's)
> Prefix `a` is Front but ignored; root's last vowel `a` is Back → Genitive suffix uses front variant `-si`

---

## IV. The Definiteness Rule

The Colour Prefix is governed by syntactic context, not by arbitrary lexical assignment. Kilor has **no separate articles or demonstratives** — the colour prefix itself encodes definiteness, indefiniteness, and demonstrative force, fused with ontological framing into a single vowel.

### A. Foregrounded (Definite / Specific / Demonstrative) — Prefix Required

The prefix **must** be applied when the noun is **foregrounded** — i.e., definite, specific, or demonstratively marked. The prefix simultaneously signals:

- **Definiteness** — the noun refers to a specific, identifiable referent (like English *the*)
- **Demonstrative force** — the noun is pointed to (like English *this*/*that*)
- **Ontological framing** — the speaker's cognitive lens on the noun (Red, Blue, etc.)

In this state, the noun is grammatically foregrounded and requires explicit ontological framing.

> **Example:** `a-fora` = "the fire" or "this fire" (specific, identifiable fire, framed as Red/Alive)
> **Example:** `o-lumi` = "the light" or "that light" (specific light, framed as White/Abstract)

### B. Generic / Indefinite — Prefix Omitted

When the noun is **generic or indefinite** (not tied to a specific referent), the prefix is **dropped by default**. The noun appears as an unmarked, generic concept without ontological commitment.

> **Example:** `fora` = "fire" (generic concept, not a specific fire)
> **Example:** `lumi` = "light" (light in general)

> **Soft guideline:** This is not a hard rule. A speaker may optionally retain a colour prefix on a generic noun to **emphasise a specific ontological property** or convey **emotional colouring**. The system is fault-tolerant: the root morpheme carries the core semantic weight, so using a "wrong" or unexpected prefix does not cause catastrophic misunderstanding.
>
> **Emotional colouring on indefinite nouns:** When a colour prefix is used on an indefinite noun purely for emotional effect, the prefix carries the speaker's subjective emotional register toward the noun rather than an ontological claim. The same 7 colours used for ontological classification double as emotional registers (see `3-subsystems/colour-emotion.md` for the full emotional register system). This is distinct from definiteness — the noun remains grammatically indefinite, but the prefix adds an expressive layer:
>
> > **Example:** `a-lumi` (Red-anger light) — "light" as indefinite concept, but spoken with anger-tinted emotional weight
> > **Example:** `i-lira` (Blue-sadness water) — "water" as an indefinite, generic substance, tinted with sadness
> > **Example:** `y-gilan` (Black-awe mountain) — "a mountain" (indefinite), but the speaker feels awe toward it
>
> This usage is optional and expressive; omitting the prefix remains the default for generic reference. The emotional register is recoverable from context and does not override the noun's grammatical indefiniteness.


### C. Proper Nouns — Cultural Convention

Proper nouns (personal names, place names, etc.) are **exempt from both the definiteness prefix requirement (§IV-A) and the classification rules (§V)**:

- A proper name **may** carry any colour prefix, or **no prefix at all** — both are common. Unlike common nouns, proper nouns are **not** required to carry a prefix when definite (they are inherently definite by nature). In practice, some proper terms in everyday usage appear without a colour prefix, and others carry one assigned by **historical or cultural convention** rather than by the ontological properties of the referent.
- The 7-Question Filter (§V) applies only to common nouns and should not be used to determine a proper noun's prefix.
- When a prefix is used on a proper name, the same city might carry a different prefix in different historical eras, or a person's name might inherit a prefix from a founding myth.

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

### Tier 2: 共識 — Community-Consensus Defaults

Every **common noun** in Kilor has a **community-consensus default prefix (共識)** — the conventionalised ontological framing that the speech community has settled on as the unmarked, neutral choice. This is not limited to highly frequent everyday objects; it applies to the entire common-noun lexicon. Beginners are taught these defaults as cognitive shortcuts, and they serve as the baseline for everyday communication.

Proper nouns may also have conventionalised default prefixes (e.g., a city named with a culturally assigned colour), but they are **exempt** from the 共識 requirement — a proper name may carry any colour prefix, or no prefix at all (see §IV-C).

> **Example:** *Paper* defaults to **`e-paper`** (Yellow) — its primary identity is a human-crafted tool.
> **Example:** *Fire* defaults to **`a-fora`** (Red/Alive) — its primary identity is as a living, energy-consuming force.

#### Speaker Override (異體字)

The 共識 default is the conventional form, but a speaker may intentionally substitute their own colour prefix based on **context, emphasis, or personal intent**. This is analogous to 異體字 (variant characters) in written Chinese — the standard form is known and accepted, but variant forms are understood and tolerated without breaking communication.

A speaker who uses a non-standard prefix does not cause confusion; the root morpheme carries the core semantic weight. The variant prefix acts as a deliberate "camera lens" that highlights a specific property the speaker wishes to foreground, even if it deviates from convention.

> **Example (共識 + 異體字):**
> 共識: `a-fora` (Red) — fire's conventional framing as alive/energy
> 異體字: `y-fora` (Black) — fire framed as a dangerous, dense, unyielding destructive mass
> 異體字: `o-fora` (White) — fire framed abstractly, as concept or spirit

Tier 1 (Contextual Fluidity) and the 異體字 override are distinct: Tier 1 applies to objects that genuinely have no single conventional framing and the speaker selects freely; 異體字 applies to nouns that have a known 共識 default which the speaker chooses to override. Emotional colouring is one legitimate motivation for a 異體字 override — a speaker may deliberately substitute a non-standard colour prefix to tint a definite noun with a specific emotional register, independent of its ontological properties (see `3-subsystems/colour-emotion.md` for the full emotional register system).


### Tier 3: The `Null` Fallback (White Default)

If a concept is purely abstract, entirely lacks physical form, or represents the unknown/void, it defaults to **White (`o-`)**. White acts as the `Null` or base class of Kilor's ontology.

> **Example:** *Syntax, Justice, Logic, Shadows, Echoes* → all default to **`o-`**

---

*End of Nouns & Colour Prefix Specification.*