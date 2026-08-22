# Kilor Spatial Postpositions — The `-ne` Suffix

**Module:** Spatial Postpositions
**Status:** Canonical
**Last updated:** 2026-08-23
**Version:** 1.3.0
**Depends on:** `0-foundation/grammar-syntax.md`, `1-nominals/cases.md`

---

## I. Overview

Kilor expresses precise spatial relationships through a set of **relational noun roots + invariable `-ne` suffix**, forming spatial postpositions. These occupy the same oblique slot as `tilpe` ("between") in the clause template.

This system replaces the earlier catch-all use of `tilpe` for "at/on/in/near" (now deprecated). `tilpe` is redefined to mean **"between"** exclusively.

---

## II. The `-ne` Suffix

`-ne` is an **invariable** spatial suffix. It does not participate in the Contrastive Suffix Rule — it is always `-ne`, never `-ni`. This avoids confusion with the Accusative case suffix `-ni`.

`-ne` is:
- Closed-class-like in form (invariable, toneless)
- Attached to open-class spatial noun roots
- Pronounced with flat mid-tone like other closed-class particles

The `-ne` suffix creates a spatial postposition that denotes a location or path relative to a landmark.

---

## III. Spatial Postposition Inventory

| Root | Root Meaning | +`-ne` Form | Spatial Meaning | Notes |
|---|---|---|---|---|
| `ik` | in | `ikne` | inside | New root |
| `ouk` | out | `oukne` | outside | New root |
| `um` | under | `umne` | under | New root |
| `rap` | top / peak | `rapne` | above | Existing root (category G in lexicon) |
| `fim` | left | `fimne` | on the left | Existing root (left side) |
| `hap` | right | `hapne` | on the right | Existing root (right) |
| `bop` | bottom | `bopne` | below | Existing root (bottom) |
| `hau` | back | `haune` | behind | New root |
| `pau` | front | `paune` | in front of | New root |
| `hin` | side | `hinne` | beside / near / next to | New root |
| `te` | to / towards | `tene` | towards | Root is also the dative particle (dual-use) |
| `ora` | along | `orane` | along | New root |
| `meipo` | around | `meipone` | around | New root |
| `orak` | across | `orakne` | across | New root |
| `inou` | through / via | `inoune` | through | New root |
| `pos` | point / locus | `posne` | at (neutral point-locative) | Combines the location head `pos` (from `poska`) with `-ne` |
| `tilpe` | between | — | between | Existing closed-class particle (redefined; no `-ne`) |

All roots are open-class Category G (spatial/temporal). `te` is unique in serving as both a closed-class dative particle and an open-class spatial root.

---

## IV. Syntax

### A. Landmark Construction

Spatial postpositions follow the landmark noun, which carries **Genitive case**:

```
[landmark]-GEN [spatial-ne]
```

> `slato-si ikne` — "house's inside" = "inside the house"
> `lunla-si umne` — "tree's under" = "under the tree"
> `gilan-si rapne` — "mountain's above" = "above the mountain"
> `donar-si haune` — "door's behind" = "behind the door"
> `slato-si paune` — "house's in front of" = "in front of the house"
> `shilisa hinne` — "river's beside" = "beside the river"
> `gilan-si tene` — "mountain's towards" = "towards the mountain"
> `shilisa orane` — "river's along" = "along the river"
> `slato-si meipone` — "house's around" = "around the house"
> `shilisa orakne` — "river's across" = "across the river"
> `selo-si inoune` — "road's through" = "through the road"
> `lunla do-si tilpe` — "two trees' between" = "between two trees"

### B. Pronoun Landmarks

Pronouns use their Genitive form (`kis`, `tis`, `sis`, `nis`, `kilos`, `tilos`, `silos`, `nilos`; see `1-nominals/pronouns.md` §III):

> `kis hinne` — "beside me" / "near me"
> `sis paune` — "in front of them"

### C. Tene vs. Te (Dual-Use of `te`)

**`te`** serves two distinct roles, disambiguated by context:

| Form | Function | Example |
|---|---|---|
| `te` | Dative particle ("to/for") | `ki bau te ti sounar.` — "I give bread to you." |
| `[landmark]-GEN tene` | Spatial postposition ("towards") | `ki gilan-si tene kau.` — "I come towards the mountain." |

### D. Case Roles of Spatial Postpositions

The spatial postpositions (plus the illative `ikte` below) map onto the traditional Finnish-style local cases. Kilor expresses them analytically rather than via case suffixes:

| Local case | 中文 | Kilor realisation | Form / construction | Example |
|---|---|---|---|---|
| **Locative** | 方位格 | at (point, neutral) | `[landmark]-GEN posne` | `ki slato-si posne os.` — "I am at the house." |
| **Inessive** | 內格 | in / inside (containment) | `[landmark]-GEN ikne` | `lira slato-si ikne os.` — "There is water in the house." |
| **Elative** | 出格 | out of / from (motion out) | `ar [source] ouk` + motion verb | `ki ar slato ouk.` — "I get out of the house." |
| **Illative** | 入格 | into (motion in) | `[goal] ikte` + motion verb | `ki ikte slato aug.` — "I enter into the house." |
| **Adessive** | 接格 | at / on / near (proximity) | `posne`, `rapne`, `hinne` (per relation) | `e-buk slato-si rapne os.` — "There is a book on the table." |
| **Allative** | 向格 | towards (goal-direction) | `[landmark]-GEN tene` | `ki gilan-si tene kau.` — "I come towards the mountain." |

Key distinctions:

- **`posne` (at) vs `ikne` (in) vs `rapne` (on):** `posne` is a neutral *point* locative; `ikne` asserts *containment*; `rapne` asserts *surface contact*. They are complementary, not interchangeable — `posne` does not substitute for `ikne`/`rapne`, and vice-versa.
- **Illative `ikte`:** built on the `ik` ("in") root + the goal particle `te` → *"to the inside of"* = **into**. It is a motion-goal marker (contrast static `ikne` = "inside"). Placement: **before** the goal noun, mirroring `te`/`ar`: `ki ikte slato aug.`
- **Elative composition:** Kilor's "out of" = source marker `ar` (**before** the source) + the exit-motion verb `ouk` ("get out"). Emphatic "from *inside*": `ki ar slato-si ikne ouk.`
- **Allative vs dative vs illative (goal split):** `tene` = allative "towards"; `te` = dative "to/for" (recipient); `ikte` = illative "into". These three are distinct, mirroring English *towards / to / into*. See `1-nominals/cases.md` §V-A.
- For temporal "since/from (a time)", use the subordinator `shoun` (`2-predication/subordination.md`), not the spatial `ar` (see `1-nominals/cases.md` §V-A).

---

## V. Position in the Oblique PP Order

Spatial postpositions occupy the same slot as `tilpe` in the oblique PP order. When multiple spatial postpositions co-occur, they follow the order: `ikne` / `oukne` / `posne` > `paune` / `haune` > `hinne` > `rapne` / `umne` > `orane` > `meipone` > `tilpe` > `tene`.

The full oblique PP order (see `0-foundation/grammar-syntax.md` §I-E) is:

```
[Numeral] — [sy Instr] — [mer Com] — [spatial-ne / tilpe] — [ar Abl] — [te Dat] — [Manner Adv] — Verb
```

> `ki bauni ro sy maliu mer kis song slato-si ikne ar a-fora te ti shuks sounar.`
> "I quickly give three breads to you with a knife with my friend inside the house from the fire."

---

## VI. Prominent Spatial Roots as Standalone Nouns

The spatial roots can also function as ordinary nouns:

> `a-hin` — "the side" (definite, Red = living/sentient association)
> `o-rap` — "the top" (definite, White = abstract/void)
> `ae-um` — "the underside" (definite, Brown = earth/boundary)

---

*End of Spatial Postpositions Specification.*