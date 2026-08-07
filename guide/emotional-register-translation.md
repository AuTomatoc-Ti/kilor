# Kilor Emotional Register — Translation Guide

**Module:** Conveying colour emotional particles in target languages (English, Chinese, etc.)
**Last updated:** 2026-08-07
**Spec reference:** `rules/3-subsystems/colour-emotion.md`

---

## I. Why Emotional Particles Are Hard to Translate

Kilor **grammaticalizes an emotional pole** into a closed-class particle (a = Red-Anger, u = Green-Calm, etc.). Target languages like English and Chinese express emotion **lexically**, not grammatically — they have no equivalent particle slot. So there is never a 1:1 mapping.

Compounding this, the particle is **"tint, not define"** (see `rules/3-subsystems/colour-emotion.md` §III-B): it supplies a *pole* (an emotional family), not a precise emotion. The exact feeling is completed by the root, the context, and the reader. The translator's job is therefore to **de-grammaticalize** the pole back into a lexical or stylistic choice in the target language.

---

## II. The Method — Pole → Contextual Realization

1. **Lock the pole.** Map the particle to its emotional family (the 7-base table in `rules/3-subsystems/colour-emotion.md` §II). u = Calm / serenity / peace (high-arousal: deep peace; low: quiet ease), and it resonates with Green's philosophical pole of 救贖 (Salvation).
2. **Check the context.** Does the sentence's content and register resolve a *more specific* flavor **inside that family**?
3. **Render the best-fitting family flavor.** Choose the target-language word that the pole + context most naturally realize.

Even though the specific English/Chinese word is supplied by the translator, the particle still does real work: it **constrains the field** — it excludes the opposite poles (an u god cannot read as angry or terrifying), which is exactly why a bad rendering can be detected.

---

## III. The Three-Case Test (Under / Legitimate / Over)

| Case | Behavior | Verdict |
|---|---|---|
| **Under-translation** | Always render the bare dictionary emotion, even when it clashes with context | ✗ loses the author's intended resonance |
| **Legitimate contextual realization** | Resolve the pole to the specific flavor the context supports, staying inside the pole's family | ✓ this is what the system is designed for |
| **Over-translation (超譯)** | Import a flavor **outside** the pole's family, or one the context actively contradicts, as if it were literally in the text | ✗ fabrication |

The boundary between the second and third cases is the whole question. The rule: **staying inside the pole's family + backed by context = legitimate; departing the family or contradicting context = over-translation.**

---

## IV. Worked Example — u'sym maeha winar (「憐憫的神看着人類」)

Parse: u' is a Green 異體字 override on sym (god). Green's pole = calm / serenity / **salvation**.

Rendering "compassionate / merciful god" is **legitimate**, not 超譯:

- **Inside the family:** compassion (憐憫/慈悲) sits squarely in Green's family — calm + salvation + a benevolent watcher.
- **Backed by context:** a deity *watching over humankind* naturally reads as merciful, which is why the author likely chose u- in the first place.
- **The over-translation test fails:** nothing is added outside the pole, and nothing contradicts the context.

Note the honest ambiguity: "calm god" and "merciful god" are *both* within Green's family — the translator resolves it via context and world-knowledge, so "serene," "blessed," "merciful," and "compassionate" are all defensible. Choosing the one that best carries the implied benevolence is good judgment, not invention.

---

## V. Guidance for Translators

- **Prefer the family flavor** over the bare dictionary emotion whenever the dictionary emotion sounds wrong in context.
- **Root meaning stays dominant** — the particle tints, it never redefines the root it modifies.
- **If context forces a reading outside the pole family**, stop and flag it: either a genuine ambiguity (add a brief footnote) or a deliberate, non-standard usage.
- **When precision matters**, render the pole *and* note the flavor — e.g. "a serene/merciful god (u = Green-Calm, resolved by context to compassion)" — so the reader sees both the grammatical pole and the translator's reasoning.
- Because the particle is a pole, **agreement can vary by translator**; this is a feature of the system, not a translation error.

---

*End of Emotional Register Translation Guide.*
