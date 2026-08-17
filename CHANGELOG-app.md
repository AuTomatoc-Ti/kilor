**Current Version:** v2.19.0
**Last Updated:** 2026-08-17
**Format:** `**file** — what changed`

## Template (for next entry):

## workspace v{VERSION} — {DATE}

{One-line summary}

**Frontend:**
- **`file.jsx`** — What changed
- **`file.css`** — What changed

**DB / Backend:**
- **`file.py`** — What changed

**Validation:**
- `python kilor.py check` — ✅ All N entries pass
- `npx vitest --run src/App.test.jsx` — ✅ N/N pass

## workspace v2.19.0 — 2026-08-17

31 new words across three batches (672→703): the `ek-` leg & movement family (walk-actions),
the `hil-`/`hin-` hand & digit family, and a weather/household/inspiration/club set. The `ek-`
movement verbs carry external-body `u-` like the leg nouns, except `ekmae` (pedestrian) which
takes person-class `a-` (user-locked over the family lean). The hand/digit words all take `u-`
(matching `hinar` hand) as bare roots in a fossilised `hil-`/`hin-` onset. Weather phenomena
`auwae`/`tlerahup` sit in the atmospheric `i-` family; household devices (`shaliklamtek`,
`marip`, `limarip`) are crafted `e-`; inspiration cluster (`urim`/`ureti`) is abstract `o-`
with `urimlise` at `o-`; `aurk` club is social-group `a-` and `aurk pos` club house is
location `ae-`. Also fixed a backend bug where multi-word compounds were syllabified as one
concatenated token (breaking `aurk pos` → `aurkpos`); they now syllabify per element.

**DB / Backend:**
- **`data/kilor.db`** — 672→703 (31 new rows; `draft/batch-2026-08-17.md`):
  - **A — `ek-` leg & movement:** `ekmae` pedestrian (root, `a-`, person-class); `ekke` lame (NA, `u-`); `ektoi` run (NV), `ekber` jump (NV), `ekfir` sprint (NV), `ekkae` kneel (NV), `eklun` crawl (NV), `ekkor` step on (NV), `ekkup` stomp (NV), `ekkum` squat (NV) — all roots, `u-`.
  - **B — `hil-`/`hin-` hand & digit (all `u-`):** `hinhil` finger, `hilfa` index finger/to point (NV), `blap` clap (NV), `hilmodir` thumb, `hilsenok` middle finger, `hilfoidir` ring finger, `hildoir` little finger, `hinod` palm, `hinat` wrist, `hilpae` elbow — all bare roots (fossilised `hil-`/`hin-` onset, not compounds; `hilsenok`/`hildoir` read "mid/little-digit" but `hil` is not a stored root).
  - **C — weather/household/inspiration/club:** `auwae` weather (root, `i-` N); `tlerahup` thunderstorm (`tlera`+`hup`, relational, `i-`); `shali` washing (NV, `i-`); `shaliklamtek` washing machine (3-root `shali`+`klam`+`tek`, instrument, `e-`); `marip` spout (root, `e-`); `limarip` faucet (`lira`+`marip`, relational, `e-`, lira elides to `li-`); `urim` inspire (NV, `o-`); `urimlise` revelation (`urim`+`lise`, ordained-occurrence, `o-`); `ureti` enlightenment (root, `o-`); `aurk` club (root, `a-`); `aurk pos` club house (multi `aurk`+`poska`, location, `ae-`).
- **`kilor/commands/add.py`** — Multi-word compounds are now syllabified per element (`" ".join(... for word in root.split())`) instead of as one concatenated token. Previously `aurk pos` was concatenated to `aurkpos`, which breaks at a medial coda cluster (e.g. `rk|p`) — `aurk` is phonotactically valid (§IV-D) but failed to insert. No spec change; aligns with `check.py` which already split multi-word for IPA.

**Validation:**
- `python -m kilor check` — ✅ all pre-existing errors/warnings only (nous, erolise isra, austarius, austareus, argonnamae lise, stale non-noun prefixes); none of the 31 new words appear.
- `CHANGELOG.md` (rules) intentionally NOT updated — pure-lexicon batch + one code fix, no spec/grammar change.

## workspace v2.18.0 — 2026-08-16

31 new words across three sets (641→672): the `wi-` numeracy/mathematics family, the
reckoning–accounting–wisdom block, and the `ek-` leg/body family with bones. The `wi-`
numeracy register uses abstract `o-` for concepts/operations, crafted `e-` for `-tek`
instruments (calculator/computer), `a-` for `-mae` agents, and inherits `o-`/`e-` from the
`mik`/`rum`/`kira` heads. Notable cells: `wimarem` (reckoning = count-the-former `wima+rem`)
is NV; `imuwimarem` (settle scores later) is V-only so stores no prefix; the 3-root flattens
`wimonikmae`/`wimaremmae`/`wimakirmae`/`thyramikmae` double as compounds; `wimakirmae`
(accountant, `wima+kira+maeha`) is carved from `wimaremmae` (reckoner, `wima+rem+maeha`).
`thyram` wisdom carries `e-` to hug the `thy-` thinking family. All `ek-` leg/body nouns and
bones take external-body `u-` (bones override to `u-`, not internal `a-`).

**DB / Backend:**
- **`data/kilor.db`** — 641→672 (31 new rows; `draft/batch-2026-08-16.md`):
  - **A — `wi-` mathematics:** `wimon` number, `wibom` calculate (NV), `wibar` compute (NV) (roots, `o-`); `wimonik` mathematics, `wibomis` arithmetic (`wibom`+`mlis`, method-to), `wibomik` HELD, `wibomtek` calculator (instrument, `e-`), `wiborum` plan (`wibom`+`rum` relational, `o-`), `wibartek` computer (instrument, `e-`), `wimonikmae` mathematician (3-root `wimon`+`mik`+`maeha`, agent, `a-`).
  - **B — reckoning/accounting/wisdom:** `wima` count (NV, `o-`); `wimarem` reckoning (`wima`+`rem`, NV, `o-`), `imuwimarem` settle-scores-later (`imu`+`wima`+`rem`, V, no prefix), `wimakira` account/ledger (`wima`+`kira`, `e-`), `wimaremmae` reckoner (3-root, agent, `a-`), `wimakirmae` accountant (3-root, agent, `a-`); `thyram` wisdom (NA, `e-`), `thyramik` philosophy (study-of, `o-`), `thyramikmae` philosopher (3-root, agent, `a-`), `thymae` thinker (`thy`+`maeha`, agent, `a-`); `wita` live (NV, `a-`); `paeti` turn/twist (NVAD, `o-`).
  - **C — `ek-` leg/body (all `u-`):** `eknim` leg/to-walk (NV), `ekmut` thigh, `eksim` knee, `ekdor` calf, `ekpae` ankle, `ekbod` feet, `ekhil` toe (bare root = foot-finger), `okre` bone, `ekdorokre` shinbone (`ekdor`+`okre`), `ekmutokre` femur (`ekmut`+`okre`, relational).

**Validation:**
- `python -m kilor check` — ✅ all pre-existing errors/warnings only (nous, erolise isra, austarius, austareus, argonnamae lise); none of the 31 new words appear.

## workspace v2.17.0 — 2026-08-15

31 new words across three batches (610→641): the `hem-` kinship group, the `lo-` flat→justice
family, and the education–science family. Kinship words prefix `a-` (living) except `hemsa`
home (`ae-`); the `lo-` family splits flatness/law `o-` from crafted `-tek` tools `e-` and the
location `ae-`; education keeps actions `o-`, books/tools `e-`, places `ae-`, agents `-mae`
`a-`. Notable cells: `loden` (to judge) is V-only so stores no prefix; `lodin` (flat) is NA to
preserve its `o-`; grandparents reuse `pima` (two-steps-back); `cetik` (science) is carved at
d=1 from the `mik` study head.

**DB / Backend:**
- **`data/kilor.db`** — 610→641 (31 new rows; `draft/batch-2026-08-15.md`, `-b`, `-c`):
  - **A — `hem-` kinship:** `hemo` family (`a-`), `hemsa` home (`ae-`), `hemra` relative (`a-`); `pimafmae`/`pimamae` grandfather/grandmother (comp `pima`+`famae`/`mamae`, relational); `hytam` brother, `lerra` sister, `poboi` baby, `tiha` aunt, `titam` uncle (roots, `a-`).
  - **B — `lo-` flat/justice:** `lodin` flat (NA, `o-`), `lodam` balance (NVAD, `o-`); `lodintek` spirit level, `lodamtek` libra/scales (instrument, `e-`); `laedin` horizon (root, `ae-`); `loden` to judge (V-only, no prefix), `lodenmae` judge (agent, `a-`), `lodenpar` judgment (process, `o-`), `lodici` trial (root, `o-`), `lodicipos` court (location, `ae-`).
  - **C — education/science:** `tlowtek` clock (instrument, `e-`); `nomikpos` school (location, `ae-`), `nomikmae` scholar (agent, `a-`); `nofa` learn (NV, `o-`), `nofamae` student (agent, `a-`); `nofsy` teach (NV, `o-`), `nofsykira` textbook (relational §III, `e-`), `nofsymae` teacher (agent, `a-`); `cetik` science (NA, `o-`), `cetikmae` scientist (agent, `a-`).

**Validation:**
- `python -m kilor check` — ✅ all pre-existing errors/warnings only (nous, erolise isra, austarius, austereus, argonnamae lise); none of the 31 new words appear.

## workspace v2.16.0 — 2026-08-14

31 new words across three batches (579→610): the kir-/thes- writing & energy cluster,
the lan-/epilo- shape & summary families, and the bas- combat + emotion/time words.
New `thes-` electricity family (whitelisted `thes` per the `fos` precedent, see
`CHANGELOG.md` v2.12.0), `bas-` combat family, `epilo-` summary register, `lan-`
shape family. `kirosefon` reclassified from bare root to compound (`kiro`+`sefon`,
text-shape) once `sefon` (shape) was added.

**DB / Backend:**
- **`data/kilor.db`** — 579→610 (31 new words, see `draft/batch-2026-08-14-{a,b,c}.md`):
  - **Batch A** (`thes-` electricity + kir- science; +`kirosefon` reclass):
    - `kiramik`: library science, study of books (N). N, `o-`. compound-mono (`kira`+`mik`, study-of).
    - `kiromik`: literary studies (N). N, `o-`. compound-mono (`kiro`+`mik`, study-of).
    - `kirowes`: literature, body of written works (N). N, `o-`. compound-mono (`kiro`+`wes`, collective).
    - `kirosefon`: font, typeface (N). N, `o-`. **root → reclassified compound-mono** (`kiro`+`sefon`, relational) in batch B.
    - `kiratek`: printer (N). N, `e-`. compound-mono (`kira`+`tek`, instrument).
    - `thes`: electricity (N); to electrify (V); electric (A). NVA, `a-`. root. `thes-` head; whitelisted 1-syl `-s` root.
    - `theskira`: e-book (N). N, `e-`. compound-mono (`thes`+`kira`, relational).
    - `thespiliu`: electric door (N). N, `e-`. compound-mono (`thes`+`piliu`, relational). User overrode door-head ae-→e-.
    - `thestek`: electric equipment (N). N, `e-`. compound-mono (`thes`+`tek`, instrument).
    - `thesau`: lightning (N). N, `a-`. root. `thes-` family.
    - `thesis`: power/electricity generation (N). N, `a-`. compound-mono (`thes`+`mlis`, method-to). User overrode e-→a-.
  - **Batch B** (shapes + epilo- + weather/divine):
    - `lanko`: angle (N); angular (A). NA, `o-`. root. `lan-` family.
    - `breso`: circle (N); circular (A). NA, `o-`. root.
    - `lanfo`: square (N); square, quadrangular (A). NA, `o-`. root. `lan-` family.
    - `rolanko`: triangle (N); triangular (A). NA, `o-`. compound-mono (`ro`+`lanko`, relational).
    - `sefon`: shape, form (N); to shape (V); shaped (A). NVA, `o-`. root. Head of font.
    - `elmin`: cloud (N); cloudy (A). NA, `i-`. root. atmospheric family.
    - `augor`: angel (N); angelic (A). NA, `y-`. root. divine register.
    - `epilo`: summary, overview (N); to summarize (V); summarised (A). NVA, `o-`. root. `epilo-` head.
    - `epilobim`: conclusion (N); to conclude (V); concluding (A). NVA, `o-`. compound-mono (single root `epilo`).
    - `epiloril`: epilogue (N). N, `o-`. compound-mono (single root `epilo`).
  - **Batch C** (temperament/combat/emotion/time/divine):
    - `romah`: passive (N/A). NA, `o-`. root.
    - `sourom`: to receive (V); reception (N). NV, `o-`. root. sou- give/receive family.
    - `brostima`: to protect (V); protection (N); protective (A). NVA, `o-`. root.
    - `basto`: battle (N); to battle (V); combative (A). NVA, `a-`. root. `bas-` head.
    - `basma`: to attack (V); attack (N); attacking (A). NVA, `a-`. root. `bas-` family.
    - `basrom`: defense (N); to defend (V); defensive (A). NVA, `a-`. root. `bas-` family.
    - `aeter`: eternal (A); eternity (N); eternally (D). NAD, `o-`. root.
    - `irae`: wrath, rage, indignation (N); to rage (V); wrathful (A); wrathfully (D). NVAD, `a-`. root. Carve vs losga.
    - `grase`: to confuse (V); confusion (N); confused (A). NVA, `o-`. root.
    - `symrilsemik`: mythology (N). N, `o-`. compound-mono (`sym`+`rilse`+`mik`, study-of, 3-root flat).

**Validation:**
- `python -m kilor check` — ✅ No warnings for any batch word.
- `draft/batch-2026-08-14-{a,b,c}.md` (temp-clone validated); backups in `data/backup/{database,today}/`.

## workspace v2.15.0 — 2026-08-13

13 new words across two families (566→579): `arma-` affection (dear/wife/darling,
all `a-`) and the `kir-` writing family (text, paragraph, section, writer, article,
writing, pen, book, chapter, library). `kirolote` (paragraph) is the first generalised
**non-human `lote`** collective.

**DB / Backend:**
- **`data/kilor.db`** — 13 new entries (see `draft/batch-2026-08-13-e.md`):
  - `arma`: dear, beloved (N); dear, beloved, endearing (A). pos_mask=NA, `a-`. root. arma- family head.
  - `morsa`: wife, spouse (female) (N). pos_mask=N, `a-`. root. Kinship.
  - `armati`: darling, sweetheart (N); darling, cherished (A). pos_mask=NA, `a-`. root. arma- family.
  - `kiro`: text, written content (N); textual, written (A). pos_mask=NA, `o-`. root. kir- family head.
  - `kirolote`: paragraph, a block of text (N). pos_mask=N, `o-`. compound-mono (`kiro`+`lote`, collective). Non-human lote (head-class o-).
  - `kiroli`: section, a portion of text (N). pos_mask=N, `o-`. compound-mono (`kiro`+`roli`, relational). = a lot of text.
  - `kiromae`: writer, author (N). pos_mask=N, `a-`. compound-mono (`kiro`+`maeha`, agent).
  - `kiroparam`: article, a written piece (N). pos_mask=N, `e-`. compound-mono (`kiro`+`param`, result). Lexicalised.
  - `kiropar`: writing, the act/process of writing (N). pos_mask=N, `e-`. compound-mono (`kiro`+`par`, process).
  - `kirotek`: pen, a writing instrument (N). pos_mask=N, `e-`. compound-mono (`kiro`+`tek`, instrument).
  - `kira`: book, a bound volume (N). pos_mask=N, `e-`. root. kira- book subfamily head. Near-collision kora/lira/okira (d=1, diff domains — tolerated).
  - `kiraruson`: chapter, a separate section of a book (N). pos_mask=N, `ae-`. compound-mono (`kira`+`ruson`, property).
  - `kirapos`: library, a book-place (N). pos_mask=N, `ae-`. compound-mono (`kira`+`poska`, location).

**Validation:**
- `python -m kilor check` — ✅ No warnings for any batch word.
- `draft/batch-2026-08-13-e.md` (temp-clone validated).

## workspace v2.14.0 — 2026-08-13

17 new words across two batches (549→566). New families: `sik-` moral/theological
(sins → salvation/lord/savior), `-ron` life-stage (childhood→elderly, 5 words all `ae-`),
and the **`wino` colour-term closed class** (`awino` red → `ywino` black, 7 words) —
lexicalised `{hue-prefix}+wino` forms used bare without a colour prefix (spec
`nouns-colour-prefix.md` §II-A).

**DB / Backend:**
- **`data/kilor.db`** — 17 new entries (see `draft/batch-2026-08-13-c.md` + `draft/batch-2026-08-13-d.md`):
  - Batch C (`sik-` + `-ron` families):
  - `sik`: sins (N); to sin (V); sinful (A); sinfully (D). pos_mask=NVAD, `y-`. root. sik- family head. Near-collision si/sin/sis pronouns (d=1, different domain/POS — tolerated).
  - `siklatif`: salvation, deliverance from sin (N). pos_mask=N, `y-`. compound-mono (`sik`+`latif`, result).
  - `tifor`: lord, sovereign, master (N). pos_mask=N, `o-`. root. Secular (vs `sym` god).
  - `siklatifor`: savior, deliverer (N). pos_mask=N, `y-`. compound-mono (`sik`+`latif`+`tifor`, relational).
  - `senok`: middle, mid of a span (N); mid, middle (A). pos_mask=NA, `ae-`. root. ron- family head.
  - `chelron`: childhood (N). pos_mask=N, `ae-`. compound-mono (`chel`+`ron`, relational).
  - `senokron`: middle-aged (N). pos_mask=N, `ae-`. compound-mono (`senok`+`ron`, relational).
  - `nobaron`: elderly, old age (N). pos_mask=N, `ae-`. compound-mono (`noba`+`ron`, relational).
  - `nibaron`: teenage, adolescence (N). pos_mask=N, `ae-`. compound-mono (`niba`+`ron`, relational).
  - `logerron`: adult, prime of life (N). pos_mask=N, `ae-`. compound-mono (`loger`+`ron`, relational). Reuses `loger` (strength) = age of strength.
  - Batch D (`wino` colour-term closed class, all root, NA, self-matching prefix):
  - `awino`: red, the colour red (N); red, red-coloured (A). pos_mask=NA, `a-`.
  - `ewino`: yellow (N/A). pos_mask=NA, `e-`.
  - `aewino`: brown (N/A). pos_mask=NA, `ae-`.
  - `owino`: white (N/A). pos_mask=NA, `o-`.
  - `iwino`: blue (N/A). pos_mask=NA, `i-`.
  - `uwino`: green (N/A). pos_mask=NA, `u-`.
  - `ywino`: black (N/A). pos_mask=NA, `y-`.

**Validation:**
- `python -m kilor check` — ✅ No warnings for any batch word.
- `draft/batch-2026-08-13-c.md`, `draft/batch-2026-08-13-d.md` (temp-clone validated).

## workspace v2.13.0 — 2026-08-13

20 new words added across two batches (529→549). New families: `grid-` (trust → promise), `alt-` persona/performing (personality, drama, mask, roles), `alkam-` dressing (dress up → accessories), `hilo-` (expose ↔ nude), `syl-` mystery/magic, `amo-` causal (because / because of), plus `-rin` measure (height) and `-ia` abundative (flowery). Correct/wrong (`mic`/`bli`) carved as error-free vs `ema` true, and wrong vs `bonak` bad.

**DB / Backend:**
- **`data/kilor.db`** — 20 new entries (see `draft/batch-2026-08-13.md`):
  - `grid`: trust, faith (N); to trust (V); trusting (A). pos_mask=NAV, `u-`. root. grid- family head.
  - `gridin`: promise, pledge (N); to promise (V). pos_mask=NV, `u-`. bare root, grid- family.
  - `sylor`: mystery (N); to mystify (V); mysterious (A). pos_mask=NVA, `y-`. root. Redesigned from `sylos` (2-syl root may not end in `-s`).
  - `syloris`: magic, art of the mysterious (N); magical (A). pos_mask=NA, `y-`. compound-mono (`sylor`+`mlis`, method-to).
  - `tesar param`: art work (N). pos_mask=N, `e-`. compound-multi (`tesar`+`param`, result).
  - `hilorus`: exposure (N); to expose, reveal (V); exposed (A). pos_mask=NVA, `u-`. root. Standalone (NOT rus-/ruso- family).
  - `hilora`: nudity (N); nude (A); to bare, strip (V). pos_mask=NVA, `u-`. root. hilo- family.
  - `hasti`: forgiveness (N); to forgive (V); forgiving (A). pos_mask=NAV, `o-`. root.
  - `enlirin`: height, measure of high (N). pos_mask=N, `o-`. compound-mono (`enli`+`rin`, measure).
  - `amosi`: because of, due to. pos_mask="", `o-`. function ADP. amo- sibling of `amo` (because, PART); noun-phrase reason vs clause reason.
  - `altem`: personality, character, temperament (N); personal (A). pos_mask=NA, `o-`. root. alt- family head.
  - `altid`: acting, drama, role-play (N); to act, perform (V); dramatic (A). pos_mask=NVA, `o-`. root. alt- family; performative vs `chap` (a deed).
  - `altirma`: mask (N); to mask, disguise (V). pos_mask=NV, `e-`. root. alt- family; `e-` (crafted) over family `o-`.
  - `altor`: role, part, function, persona (N). pos_mask=N, `o-`. root. alt- family.
  - `alkam`: dressing-up, costume (N); to dress up (V); dressed-up (A). pos_mask=NVA, `o-`. root. Near `klam` (cloth, d=2) accepted.
  - `alkamer`: accessories, trappings of an outfit (N). pos_mask=N, `e-`. root. alkam- family.
  - `frunia`: floweriness (N); flowery (A). pos_mask=NA, `u-`. compound-mono (`fru`+`nia`, abundative). Base-inherit `u-`. A-only → NA to preserve prefix.
  - `tyse`: goodbye (INTERJ); farewell, send-off (N); valedictory (A). pos_mask=NA, `o-`. root. Mixed content+function (cf. `hei`).
  - `mic`: correctness (N); to correct (V); correct (A); correctly (D). pos_mask=NVAD, `o-`. root. Correct = error-free, distinct from `ema` true.
  - `bli`: wrongness, error (N); to wrong, err (V); wrong, incorrect (A); wrongly (D). pos_mask=NVAD, `o-`. root. Antonym of `mic`; distinct from `bonak` bad.
- **`hei`** — added `hello` INTERJ sense via `kilor edit` (mask stays NA). Structural twin of `tyse`.

**Validation:**
- `python kilor.py add --file draft/batch-2026-08-13.md` — ✅ 20 added, 0 errors (validated against temp DB clones first; `--dry-run` not implemented on `add`)
- `python kilor.py check` — ✅ no new errors

## workspace v2.12.0 — 2026-08-12

10 new territorial / state words added (519→529): `pos-` land family expansions (nation, country, province, city), `rus-` district/canton family, `pegloce` (county), plus closed/open state roots (`ikke`, `wone`).

**DB / Backend:**
- **`data/kilor.db`** — 10 new entries (see `draft/batch-2026-08-12.md`):
  - `posim`: nation, the people sharing identity (N); national (A). pos_mask=NA, `ae-`. root. Near-collision with `posia` (state/land, d=1) accepted — nation = the people, distinct from the polity.
  - `poskae`: country, land, territory (N); country-wide, of the land (A). pos_mask=NA, `ae-`. root. Country = physical territory, distinct from `posia` (state).
  - `posloce`: province (N); provincial (A). pos_mask=NA, `ae-`. compound-mono (`poska`+`loce`, land+administration; head-last).
  - `poslam`: city, urban settlement (N); urban, of the city (A). pos_mask=NA, `ae-`. root. Urban settlement, distinct from `posia`'s city-state/polity reading.
  - `ruson`: separation (N); to separate (V); separate, distinct (A); separately (D). pos_mask=NVAD, `ae-`. root. `rus-` family (rusome); phonesthetic pairing set `ae-`.
  - `rusomi`: district, civil division (N); district-level, of a district (A). pos_mask=NA, `ae-`. root. Near-collision `rusome` (room, d=1) accepted — enclosed space vs bounded admin region.
  - `pegloce`: county (N); county-level (A). pos_mask=NA, `ae-`. root. Near-collision `poska` (place, d=1) accepted.
  - `ikke`: closure, closing (N); to close, to shut (V); closed (A). pos_mask=NVA, `o-`. root. Near-collision `ikne` (inside, d=1) accepted — locative vs closed-state.
  - `wone`: opening, breadth (N); to open, to widen (V); open, broad, wide (A); openly, broadly (D). pos_mask=NVAD, `o-`. root. `wonli`/`wonir` (sea/ocean) kept their separate `i-` sub-family.
  - `rusoloce`: canton (N); canton-level, of a canton (A). pos_mask=NA, `ae-`. root. `rus-` family; bare root (no `rus` root to form `rus`+`loce` compound).

**Validation:**
- `python kilor.py add --file draft/batch-2026-08-12.md` — ✅ 10 added, 0 errors (note: `--dry-run` is not implemented on `add`; validated against a temp DB clone first)
- `python kilor.py check` — ✅ no new errors

## workspace v2.11.0 — 2026-08-12

30 new words added (489→519) across three Phase 0 pre-pipeline batches: `aka-` alternative/synonym family, `-lith` stone family, `sel-` birth family, narrative/religion/art terms, `nom-` study/governance family, and `sou-`/`fid-` process/purpose families.

**DB / Backend:**
- **`data/kilor.db`** — 30 new entries:
  - `aka`: an alternate form, variant (N). pos_mask=N, `o-`. root. Head of `aka-` family.
  - `akaur`: an alternative/option (N); alternative, alternate (A); alternatively (D). pos_mask=NAD, `o-`. root. Renamed from `akau` to avoid near-collision with `kau` (arrive).
  - `akaberat`: synonym (N); synonymous (A). pos_mask=NA, `o-`. compound-mono (`aka`+`berat`).
  - `akanumin`: alias, assumed name (N); by the alias of, a.k.a. (D). pos_mask=ND, `o-`. compound-mono (`aka`+`numin`).
  - `akauselo`: backup plan, alternative way (N); as a backup (D). pos_mask=ND, `ae-`. compound-mono (`akaur`+`selo`; `r` elides → `akauselo`).
  - `lith`: stone (N); stony, made of stone (A). pos_mask=NA, `y-`. root. Head of `-lith` family.
  - `galith`: rock (N); rocky (A). pos_mask=NA, `y-`. root.
  - `gilith`: mineral(s)/ore (N); mineral, mineral-rich (A). pos_mask=NA, `y-`. root.
  - `shilim`: small stream, brook, creek (N). pos_mask=N, `i-`. root.
  - `wonlira`: seawater (N). pos_mask=N, `i-`. compound-mono (`wonli`+`lira`; medial `li` collapses → `wonlira`).
  - `seli`: birth (N); to be born (V). pos_mask=NV, `a-`. root. Head of `sel-` family.
  - `seliroi`: birthday (N). pos_mask=N, `a-`. compound-mono (`seli`+`roi`).
  - `selise`: the appointed time of birth (N). pos_mask=N, `a-`. compound-mono (`seli`+`lise`, ordained-occurrence).
  - `rilse`: legend (N); legendary (A). pos_mask=NA, `o-`. root.
  - `beril`: story, tale, narrative (N). pos_mask=N, `o-`. root. A "story-like" intentionally omitted — similative `-ius` covers it.
  - `sym`: god, deity (N); divine (A). pos_mask=NA, `y-`. root.
  - `symrilse`: myth (N); mythical (A). pos_mask=NA, `o-`. compound-mono (`sym`+`rilse`).
  - `shinobi`: ninja, hidden covert agent (N). pos_mask=N, `a-`. root. Cultural loanword.
  - `hula`: dance (N); to dance (V). pos_mask=NV, `u-`. root.
  - `priko`: laziness (N); lazy (A); lazily (D). pos_mask=NAD, `o-`. root. Quality root.
  - `lifa`: transformation (N); to transform (V); transformative (A). pos_mask=NVA, `o-`. root.
  - `nomik`: study, field of study (N); to study (V); studious (A). pos_mask=NVA, `o-`. root. Full content root; `mik` is its shortened combining form (source of `-ik`/`-mik` suffix).
  - `nomir`: order, law, rule (N); ordered, lawful (A); to order, to decree (V). pos_mask=NAV, `o-`. root.
  - `misomik`: musicology, study of music (N); musicological (A). pos_mask=NA, `o-`. compound-mono (`miso`+`mik`, study-of pattern).
  - `loce`: administration, governance (N); to administer/govern (V); administrative (A). pos_mask=NVA, `o-`. root. Source/combining form for `locemir`.
  - `locemir`: council, governing body (N). pos_mask=N, `o-`. compound-mono (`loce`+`nomir`; `no-` elides → `locemir`).
  - `sou`: continuation (N); to continue/proceed (V); ongoing (A). pos_mask=NVA, `o-`. root.
  - `ilsou`: sufficiency, enough (N); enough, sufficient (A); sufficiently (D). pos_mask=NAD, `o-`. compound-mono (`il`+`sou`).
  - `fid`: goal, aim, objective (N); to aim/target/intend (V). pos_mask=NV, `o-`. root.
  - `fidden`: reason, rationale (N); to reason/rationalise (V). pos_mask=NV, `o-`. root.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new
## workspace v2.10.1 — 2026-08-11

Bug fix: compound-mono entries ending in `-s` were incorrectly rejected by the `-s` constraint. The `is_compound` check only looked for spaces in the form, missing mono-word compounds.

**DB / Backend:**
- **`kilor/commands/add.py`** — Fixed `is_compound` detection (line 308): now checks `entry_type` for `compound-mono`/`compound-multi` in addition to spaces-in-form. Previously, mono-word compounds like `pires` (pi- + res) and `pares` (pa- + res) were treated as bare roots and rejected by the 1-2 syllable `-s` constraint.

**Validation:**
- `python kilor.py check` — ✅ 12 pre-existing errors, 0 new

See also: CHANGELOG.md v2.9.1.



## workspace v2.10.0 — 2026-08-09

Backend meaning-separation refactor: the `today.md` `Meaning` field is now a JSON array (`[{"gloss","pos"}, ...]`). `add.py` and `edit.py` parse arrays and no longer comma-split glosses; legacy per-PoS fields remain supported. Re-grouped the 6 comma-split meaning pairs from the v2.9.0 batch into single items.

**DB / Backend:**
- **`kilor/commands/add.py`** — Parses `| Meaning | [{"gloss":..., "pos":...}] |` as a JSON array; validates each `pos` against `VALID_POS` (blocking error on malformed/invalid); inserts one `meanings` row per array item with no comma-splitting. Legacy per-PoS `Meaning (N)` fields kept as fallback.
- **`kilor/commands/edit.py`** — `--add-meaning` now also accepts a JSON object/array (`{"gloss","pos"}` or `[...]`) in addition to the plain-string form; inserts one row per item.
- **`data/kilor.db`** — Re-grouped 6 split meaning pairs into single items: `ipo` V "to trap, catch in a trap", `ipon` V "to truss, bind tightly", `ipot` V "to lure, tempt", `gaeth` V "to lance, pierce", `choumia` A "fruitful, bountiful", `kacit` V "to fence, enclose".

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new
- `draft/test_array.py` / `draft/test_edit.py` — ✅ Array parse + JSON `edit --add-meaning` verified on a throwaway DB copy

See also: CHANGELOG.md v2.8.0.

## workspace v2.9.0 — 2026-08-09

9 new words added (428→437) + 1 rename (`donar`→`piliu`). Family batches: `ip-` hunting (trap/truss/lure), `pil-` boundary (door/gate), `choum-` harvest (sickle/bountiful harvest), plus metal (`talo`), weapon (`gaeth`), and boundary (`kacit`). First `choum-`/materials batch through the Phase 0 pre-pipeline workflow.

**DB / Backend:**
- **`data/kilor.db`** — 9 new entries + 1 rename:
  - `talo`: copper (N), copper-coloured (A). pos_mask=NA, `y-`. Metal family (cf. `giliu`).
  - `ipo`: trap (N), to trap/catch in a trap (V). pos_mask=NV, `e-`. `ip-` hunting frame.
  - `ipon`: truss (N), to truss/bind tightly (V). pos_mask=NV, `e-`.
  - `ipot`: lure (N), to lure/tempt (V). pos_mask=NV, `e-`.
  - `gaeth`: lance (N), to lance/pierce (V). pos_mask=NV, `e-`. 1 syllable.
  - `piliu`: door (N). Renamed from `donar`; form/IPA/syllables/inflection recomputed (clean 2-syl). pos_mask=N, `ae-`.
  - `pilau`: gate (N). pos_mask=N, `ae-`. Paired with `piliu` (LD1, intended).
  - `choumtek`: sickle (N). compound-mono (`choum`+`tek`, instrument). pos_mask=N, `e-`.
  - `choumia`: bountiful harvest (N), fruitful/bountiful (A). compound-mono (`choum`+`nia`, abundative). pos_mask=NA, `u-`. 3-syl tonal inflections set to `choujmia`/`choumija`.
  - `kacit`: fence (N), to fence/enclose (V). pos_mask=NV, `ae-`.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new (12 pre-existing warnings)
## workspace v2.8.0 — 2026-08-09

10 new words added: 9 roots + 1 compound (weikra–sefe batch). First batch processed through the new pre-pipeline Phase 0 workflow. See also: CHANGELOG.md v2.7.0.

**DB / Backend:**
- **`data/kilor.db`** — 10 new entries (428→438):
  - `weikra`: weakness (N), to weaken (V), weak (A), weakly (D). pos_mask=NVAD, `o-`.
  - `saelom`: peace (N), to pacify/make peace (V), peaceful (A), peacefully (D). pos_mask=NVAD, `o-`.
  - `arse`: buttocks/arse/ass (N). pos_mask=N, `u-`.
  - `tesar`: art (N), artistic (A), artistically (D). pos_mask=NAD, `e-`. Phonologically paired with `tesak` (create).
  - `lausta`: song (N), to sing (V), lyrical/songful (A), lyrically (D). pos_mask=NVAD, `u-`.
  - `messa`: greatness (N), great (A), greatly (D). pos_mask=NAD, `o-`.
  - `raekum`: rest/repose (N), to rest/relax (V), restful (A), restfully (D). pos_mask=NVAD, `o-`.
  - `raekumlausta`: requiem (N). compound-mono (raekum + lausta). pos_mask=N, `u-`.
  - `mlaska`: sword (N). pos_mask=N, `e-`. `ml-` frame paired with `maliu` (knife).
  - `sefe`: hammer (N), to hammer (V). pos_mask=NV, `e-`.

**Validation:**
- `python kilor.py check` — ✅ 8 pre-existing errors, 0 new


## workspace v2.7.0 — 2026-08-09

Two new source roots: `aigan` and `konta`. Existing root `rolifor` designated as source for `-rolif` suffix. See also: CHANGELOG.md v2.6.0.

**DB / Backend:**
- **`data/kilor.db`** — 2 new root entries (416→418):
  - `aigan`: repetition, renewal (N); repeated, renewed (A); to repeat, to do again (V); repeatedly (D). pos_mask=NAVD, `o-`.
  - `konta`: opposition, adversary (N); opposing, contrary (A); to oppose, to counter (V). pos_mask=NAV, `o-`.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.6.0 — 2026-08-09

Two new source roots for derivational suffixes: `mik` and `mlis`. `mlis` added to `S_FINAL_WHITELIST`. See also: CHANGELOG.md v2.5.0.

**DB / Backend:**
- **`data/kilor.db`** — 2 new root entries (414→416):
  - `mik`: study, field of study (N). pos_mask=N, `o-`.
  - `mlis`: method, way (N). pos_mask=N, `e-`. Grandfathered -s final root (A/D = `mlises`).
- **`kilor/phonology.py`** — `S_FINAL_WHITELIST`: added `mlis`.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.5.0 — 2026-08-09

Two new source roots for derivational prefixes: `doir` and `meson`. See also: CHANGELOG.md v2.4.0.

**DB / Backend:**
- **`data/kilor.db`** — 2 new root entries (412→414):
  - `doir`: little, small, young, cute (A); little one, young one (N). pos_mask=NA, `u-`.
  - `meson`: huge, giant, enormous (A); giant, enormous thing (N); trillion / 10¹² (NUM). pos_mask=NA, `y-`.
- **`kilor/commands/edit.py`** — Used `--add-meaning --pos NUM` for `meson`'s trillion sense.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.4.0 — 2026-08-09

Three new source roots for derivational prefixes: `pih`, `pah`, `seftah`. Each has ADP + A meanings, pos_mask = A, `o-` prefix. See also: CHANGELOG.md v2.3.0.

**DB / Backend:**
- **`data/kilor.db`** — 3 new root entries (409→412):
  - `pih`: prior, previous (A); before (in time) (ADP). pos_mask=A, `o-`.
  - `pah`: subsequent, later (A); after (in time) (ADP). pos_mask=A, `o-`.
  - `seftah`: meta, transcendent (A); beyond (ADP). pos_mask=A, `o-`.
- **`kilor/commands/edit.py`** — Used `--add-meaning --pos ADP` for the three adposition senses.
- **`kilor/commands/add.py`** — unchanged; three roots inserted via `python kilor.py add today.md`.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new


## workspace v2.2.0 — 2026-08-06

`-es` allomorph for s-final roots: four grandfathered 1-syllable roots (`fos`, `gus`, `meus`, `rius`) now produce `foses`/`guses`/`meuses`/`riuses` for adjective/adverb instead of illegal `*-ss`. Single-category omission (§IV-G) extended to 1–2 syllable words (returns `[bare, inflected]` tuple). See also: CHANGELOG.md v1.26.0.

**Frontend:**
- **`kilor/dictionary/src/db.js`** — `computeInflections()`: toneless A/D branch checks `form.endsWith('s')` and appends `'es'`. Single-mask toneless words return `[bare, inflected]` tuple (e.g. `meus` mask=`A`: both `meus` and `meuses`). Rebuilt `dictionary.html` via `python kilor.py export --format html`.

**DB / Backend:**
- **`kilor/phonology.py`** — `compute_tonal_inflections()`: toneless A/D branch checks `form.endswith('s')` and appends `'es'`. Single-mask toneless words return `[bare, inflected]` tuple.
- **`kilor/db.py`** — `populate_search_text()`: flattens list-valued inflections (single-mask tuples) into search_text. Now sets `updated_at = datetime('now')` when search_text changes. Only updates rows where search_text actually changed.
- **`data/kilor.db`** — `search_text` regenerated: `meus` search_text now includes both `meus` and `meuses` (single-mask tuple); `updated_at` bumped for `meus` only (other 3 words unchanged — multi-mask, search_text identical).

**Validation:**
- `python kilor.py check` — ✅ 7 pre-existing errors, 0 new
- Frontend: `dictionary.html` rebuilt with updated JS

## workspace v2.3.0 — 2026-08-06

Phonology v2.0.0 frontend/backend sync: sl→sr rename, all IPA mappings updated, new `qy` /j/ multi-char core consonant. See also: CHANGELOG.md v2.0.0.

**Frontend:**
- **`kilor/dictionary/src/db.js`** — Synced `_START_ONLYS` (sl→sr), `_IPA_MAP` (all v2.0.0 vowel/consonant mappings: a→a, e→e, r→ɹ, g→ɡ, iu→i̯u, lateral-release /Cˡ/, approximant-release /Cɹ/), `_CORE_CONS` split to single-char + `_MULTICHAR_CORE` (new `qy` /j/), `splitSyllablesJS` and `_syllablePositions` updated for multi-char core consonant support in onset and coda.

**DB / Backend:**
- **`kilor/phonology.py`** — IPA lookup tables synced to v2.0.0. `START_ONLYS` updated (sl→sr). `_MULTICHAR_CORE = {"qy"}` for multi-char core consonant. `split_syllables`, `syllable_positions`, `_syllable_to_ipa` all support multi-char core consonants in onset/coda.
- **`data/kilor.db`** — sl→sr rename: 4 words (slato, slo, slosaka, slote → srato, sro, srosaka, srote). Full IPA recomputation: 405 of 406 words updated to v2.0.0 phonology.

**Validation:**
- `python kilor.py check` — ✅ 6 pre-existing errors, 0 new

## workspace v2.1.0 — 2026-08-05

Compound pattern system overhaul: auto-compute from last component (zero human judgment), DB normalization (36→17 canonical patterns, 45 non-spec patterns cleared), misomae fix.

**DB / Backend:**
- **`kilor/schema.py`** — Added `COMPOUND_PATTERN_MAP` (SSOT): 16 canonical pattern names keyed by full-root component forms (e.g. `maeha`→`agent`, `lise`→`ordained-occurrence`, `poska`→`location`). When adding a new suffix or compounding head, update both this dict and the corresponding spec file.
- **`kilor/commands/add.py`** — `_insert_compound_data()` now auto-computes `pattern` from `COMPOUND_PATTERN_MAP.get(last_component)` when no manual pattern is specified in `today.md`. Zero human judgment needed for spec-defined heads. Manual `Pattern` field still works as override.
- **`data/kilor.db`** — Fix script normalized all compound patterns: 32 renamed (e.g. `Fate`→`ordained-occurrence`, `agentive-suffix`→`agent`, `Life-condition`→`ordained-occurrence`), 45 non-spec `compound_meta` rows deleted (ordinary content-root compounds: `nominal-compound`, `temporal-day`, `numeral-compound`, `frequency`, etc.), one component fix (`misomae` now has `maeha` component matching all other agent compounds). From ~36 different pattern names → 17 canonical.
- **`draft/fix_compounds.py`** (new, temp, deleted after use) — One-shot script for DB normalization. Investigated 8 single-component compounds: `lokisra` (doctrine, missing `loki` root), `bamares`/`hostakes` (legitimate epistemic modals), `auronte`/`foske`/`lunlagak`/`walunla` (missing components). No deletion — investigation only.

**Validation:**
- `python kilor.py check` — ✅ 7 errors, 12 warnings (all pre-existing, 0 new)

> See also: `CHANGELOG.md` v1.25.0 (spec split) and v1.24.0 (mono/multi rules).

## workspace v2.0.4 — 2026-08-04

`amo`/`aiga` swapped (because ↔ again), `fru` gloss edit (flowery→floral), `argonnamae` + `argonnamae lise` added.

**DB / Backend:**
- **`data/kilor.db`** — `fru`: gloss `flowery` (A) → `floral` (A). `amo`: meaning "again" (D) → "because" (PART), pos_mask `D`→``, is_function_word 0→1. `aiga`: meaning "because" (PART) → "again" (D), pos_mask empty→`D`, is_function_word 1→0. 2 new compounds: `argonnamae` (id=425, agent: argonna+maeha, N, `a-`) and `argonnamae lise` (id=426, ordained occurrence: argonnamae+lise, N, `a-`). `search_text` regenerated.

**Validation:**
- `python kilor.py check` — ✅ 0 new errors

> See also: `CHANGELOG.md` v1.23.0.

## workspace v2.0.3 — 2026-08-04

`-lise` compound audit: 14 compounds reviewed, 13 meaning sets revised, 1 removed (`song lise`). Root `lise` redefined.

**DB / Backend:**
- **`data/kilor.db`** — Root `lise`: meaning changed from "fate, destiny" to "assigned state; divine season; appointed time; providential ordering; sacred rhythm". 13 compounds with revised meanings per `CHANGELOG.md` v1.22.0: `elise`, `milise`, `halise`, `rildalise`, `erolise`, `bonaklise`, `gorlise`, `hoplise`, `huplise`, `luminlise`, `mylise`, `shenlise`, `maelise`. Deleted: `song lise` (id=377). `search_text` regenerated via `populate_search_text()`.
- **`draft/update_lise_meanings.py`** (new, temp) — Batch update script for the above changes.

**Validation:**
- `python kilor.py check` — ✅

> See also: `CHANGELOG.md` v1.22.0.

## workspace v2.0.2 — 2026-08-03

Grammar badge consolidation, tonal inflection search, compound fixes, type sort fix, reloadDatabase guard.

**Frontend:**
- **`kilor/dictionary/src/db.js`** — `is_grammar` badge changed from `pos_mask == ''` to per-meaning POS check via `GRAMMAR_TAGS` Set — matches filter logic (e.g. `aniu` with meaning "zero/NUM" now shows `[grammar]`). `buildFilterClauses` supports `grammar` type with EXISTS subquery. `reloadDatabase()` null-guard: auto-reinitializes if `db` is null. Type sort CASE uses EXISTS subquery instead of `pos_mask` — eliminates root→root+grammar→root jumble. Fixed `buildTestDB` INSERT column count (10→11) to include `pos_mask`.
- **`kilor/dictionary/src/components/FilterPanel.jsx`** — Added synced "Grammar" checkbox in Word Type column (pink label): toggling it checks/unchecks all 11 grammar POS tags, and "All Grammar" toggle syncs back. Fixed `React.Fragment` crash by importing `Fragment`. Added mono/multi sub-checkboxes under "Compounds" (indented, `compound-sub-row`).
- **`kilor/dictionary/src/App.jsx`** — `filterCompoundTypes` state wired through to `queryWords()`; `TYPE_LABELS` removed `function`.
- **`kilor/dictionary/src/components/TableView.jsx`** — `TypeTag` renders two independent badges (structural + grammar). NVAD column removed (7-col table). Type sort column header updated.
- **`kilor/dictionary/src/App.css`** — Added `.compound-sub-row { padding-left: 22px }` for indented mono/multi sub-options. Fixed `.filter-columns` flex-wrap (removed) to prevent third column wrapping.

**DB / Backend:**
- **`kilor/phonology.py`** — Added `syllable_positions()` and `compute_tonal_inflections()` — ported from JS for 3+ syllable tonal form generation.
- **`kilor/db.py`** — `populate_search_text()` uses `compute_tonal_inflections()` for 3+ syllable words.
- **`data/kilor.db`** — Fixed 4 multi-word compounds mislabeled as mono (hamin pos, lira naras, song rius, song meus → multi). Regenerated inflections + search_text for all 299 content words — 99 tonal forms now stored (e.g. `wajlunla`, `waluvnla`).

**Tests:**
- **`kilor/dictionary/src/FilterPanel.test.jsx`** (new) — jsdom tests: verifies mono/multi sub-checkboxes render/hide correctly. 2 tests passing.
- `npx vitest run` — ✅ 11/11 pass (2 FilterPanel + 9 db.reload)
- `npm run build` — ✅ 45 modules, 743ms
- `python kilor.py check` — ✅ 5 pre-existing errors, 0 new


## workspace v2.0.1 — 2026-08-03

UI/UX overhaul: full POS filter grid, NVAD column removed, independent structural+grammar badges, POS legend modal, 25/45/30 layout.

**Frontend:**
- **`kilor/dictionary/src/components/FilterPanel.jsx`** — Replaced NVAD mask checkboxes with full 17-tag POS grid: Content (6 tags) and Grammar (11 tags), 3 per row via CSS grid. Added "All Content" and "All Grammar" toggle checkboxes. POS Legend modal with 2-column safe layout (70px tag + flex desc). Columns: 25% | 45% | 30%. Word Type filter removed "Grammar" option.
- **`kilor/dictionary/src/db.js`** — `buildFilterClauses` mask filter uses `EXISTS (SELECT 1 FROM meanings WHERE ... pos = ?)` — per-meaning POS matching. Type filter dropped `function`.
- **`kilor/dictionary/src/components/TableView.jsx`** — `TypeTag` renders two independent badges (structural + grammar). NVAD column removed (8→7 cols). `colSpan` updated.
- **`kilor/dictionary/src/App.jsx`** — `TYPE_LABELS` removed `function`.
- **`kilor/dictionary/src/App.css`** — Added `.pos-grid`, `.pos-grid-row`, `.pos-toggle-all`, `.pos-legend-*` styles. Removed `.td-mask`. Fixed `.filter-columns` flex-wrap causing third column to drop.

**Validation:**
- `npm run build` — ✅ 45 modules, 769ms

## workspace v2.0.0 — 2026-08-03

POS mask system: replaced `derivation_mask` + `is_function_word` with unified `pos_mask` column auto-computed from `meanings.pos` on every write.

**Frontend:**
- **`kilor/dictionary/src/db.js`** — `enrichEntries()` uses `pos_mask || derivation_mask` as `effectiveMask`, emits `is_grammar` flag; `buildFilterClauses` matches against `pos_mask` with fallback to `derivation_mask`; `buildTestDB` includes `pos_mask` column
- **`kilor/dictionary/src/components/FilterPanel.jsx`** — Type filter relabeled "Function words" → "Grammar"; mask column relabeled "NVAD Mask" → "POS Mask"
- **`kilor/dictionary/src/components/TableView.jsx`** — `TypeTag` uses `entry.is_grammar` (was `is_function_word`); `DetailPanel` uses `pos_mask` for mask display
- **`kilor/dictionary/src/App.jsx`** — `TYPE_LABELS.function` → "Grammar"

**DB / Backend:**
- **`kilor/schema.py`** — Added `pos_mask` column, `compute_pos_mask()`, `POS_TO_INFLECTION` mapping, `CLOSED_CLASS_POS` set, `CASE_SUFFIXES` list, `generate_inflection_forms()`
- **`kilor/db.py`** — `populate_search_text()` reads `pos_mask` with `derivation_mask` fallback
- **`kilor/commands/add.py`** — Writes `pos_mask = ""` on insert, computes from meanings after insert, regenerates inflections from `POS_TO_INFLECTION`; D-must-co-occur-with-A constraint removed
- **`kilor/commands/edit.py`** — Recomputation of pos_mask + inflection regeneration on meaning add/remove; `--set-mask` updates both `derivation_mask` and `pos_mask`
- **`kilor/commands/check.py`** — Validates pos_mask matches computed from meanings; validates inflections match pos_mask; reports drift
- **`kilor/api.py`** — `_word_to_dict()` uses `pos_mask` with fallback, emits `pos_mask` and `is_grammar` fields; `/api/status` queries and `/api/word-of-day` use `pos_mask`
- **`kilor/commands/export.py`** — `_export_dictionary_data()` emits `pos_mask` and `is_grammar` fields
- **`data/kilor.db`** — Migration: added `pos_mask` column, populated 299 words, fixed 5 root modals (mug,som,sew,hostak,shunle) from function→content with V mask, cleaned 290 non-standard inflection rows (case forms were incorrectly stored)
- **`data/SCHEMA.md`** — Documented `pos_mask`, deprecated `derivation_mask`/`is_function_word`

**Validation:**
- `python kilor.py check` — ✅ 5 pre-existing errors (unrelated), 12 pre-existing warnings; 0 new pos_mask mismatches

> See also `CHANGELOG.md` for rule-level documentation changes.

## workspace v1.8.0 — 2026-08-03

Prefix-mask consistency enforcement: add.py requires prefix for nouns, edit.py warns/blocks on mask changes, check.py validates, dictionary app hides stale prefixes on non-nouns.

**Frontend:**
- **`kilor/dictionary/src/db.js`** — `enrichEntries()` now nulls `consensus_prefix` when N ∉ derivation_mask (stale prefixes hidden in display, filtering, detail page)

**DB / Backend:**
- **`kilor/commands/add.py`** — `_validate_and_resolve_prefix()` now requires non-empty `consensus_prefix` when N ∈ mask (blocking error); auto-clears to NULL when N ∉ mask
- **`kilor/commands/edit.py`** — `--set-mask` warns when removing N while prefix still set; blocks when adding N to mask without existing prefix
- **`kilor/commands/check.py`** — New validation: error for noun with no prefix, warning for non-noun with stale prefix
- **`data/kilor.db`** — 20 nouns assigned missing `consensus_prefix` via batch edit (asdo, aultake, gor, gus, hostak, kau, kop, meki, mekri, mug, naram, niba, noba, pusar, retanik, roli, rolifor, taka, taki, tle)

**Validation:**
- `python kilor.py check` — 0 prefix-mask errors, 12 prefix-mask warnings (pre-existing stale prefixes on non-nouns)

> **Data corrections** tracked in `CHANGELOG.md` v1.20.1.

## workspace v1.7.0 — 2026-08-02

Derivational suffix audit DB cleanup: removed 4 redundant -lu doublets, created `klush lu` compound, unified question word POS to Q. See also: CHANGELOG.md v1.20.0.

**DB / Backend:**
- **`data/kilor.db`** — Deleted: gorlu (305), mylu (306), emalu (114), wemlu (307) — 4 redundant -lu doublets of quality roots. Modified: wem (55) — added "warmth" as noun meaning. Created: `klush lu` (423) — multi-word compound, mask=N, prefix=a-, meaning=courage (血性), components klush+lu. Question word POS unified to Q: awei, aeweisan, aewei updated in meanings table.

**Validation:**
- `python kilor.py check` — 35 errors (all pre-existing noise)

## workspace v1.6.0 — 2026-08-02

Full lexicon audit complete: 9 batches, ~411 words human-reviewed. Meanings, derivation masks, consensus prefixes, word types, POS tags, notes, and inflections corrected across all existing DB entries. New `audit-apply` and `audit-export` pipeline. Subscript form guards in Python & JS phonology. `updated_at` discipline fixed (application-layer only; recursive trigger removed). `D`-without-`A` mask constraint relaxed.

**Frontend:**
- **`db.js`** — `splitSyllablesJS()`: subscript guard — words with Unicode subscript characters (U+2080–U+2089) skip syllable parsing and return `[word]`. Prevents crash on subscripted pipeline escape-hatch forms like `ero₁`.
- **`TableView.jsx`** — Minor subscript display handling.

**DB / Backend:**
- **`kilor/commands/audit_apply.py`** (new) — Batch audit change application. Parses human-reviewed audit `.md` sheets; applies form renames, word type reclassifications, derivation mask changes, consensus prefix updates, meaning/POS corrections, notes cleanup, compound component re-links, and inflection auto-regeneration. Handles `(CLOSED-CLASS)`→`""` normalization, POS canonicalization (`adj`→`A`, `adv`→`D`, `v`→`V`, `n`→`N`), `(clear)`/`(delete)`/`(remove)`→`""` Notes normalization, and `wrong tone marker` diagnostic→auto-regeneration. 4-phase workflow: preview→commit with `--commit` flag. Sets `updated_at` on every mutation.
- **`kilor/commands/audit_export.py`** (new) — Generates per-batch human-review audit sheets (`.md` format) from the DB. Each word rendered as a table with current values and blank Desired Change column.
- **`kilor/__main__.py`** — Wired `audit-apply` and `audit-export` subcommands. `audit-apply` accepts `--file`, `--batch-size` (default 50), and `--commit`.
- **`kilor/commands/check.py`** — Subscript guard: words with Unicode subscript characters (U+2080–U+2089) skip IPA validation and syllable count checks (subscripted forms are metadata-only per pipeline §VI). Removed `D`-without-`A` mask validation — standalone `D` is valid per grammar spec.
- **`kilor/commands/edit.py`** — `--fix-typo` now sets `updated_at = datetime('now')` on the words table UPDATE.
- **`kilor/schema.py`** — `VALID_POS` added `MODAL`, `DEM`, `Q`, `CLF`, `INTERJ`, `PROPN` tags for future/partial use.
- **`kilor/tests/test_updated_at.py`** (new) — Tests verifying `updated_at` is set on INSERT and bumped on UPDATE via `audit_apply.py` and `edit.py`.
- **`data/kilor.db`** — Audit batches 001–009 applied: all ~411 existing words human-reviewed. Corrections across meanings (typos, missing glosses, POS tag canonicalization), derivation masks (VAD→NVAD, NAD→D, N→NAD, etc.), consensus prefixes (o-/None→e-/u-/a-, etc.), word types (root↔function per Mistake 13), forms (thanar→thaki, wonar→wonir, tlaure→tlaurhak), notes (tor/torra cleanup), compound components (tesakmae, shemae, tamae, takamae → maeha), and inflections (auto-regenerated for all mask-change words + "wrong tone marker" diagnostics). `updated_at` timestamps updated for all modified words via application-layer discipline.
- **`data/fix/drop_timestamp_trigger.sql`** (new) — Cleanup script to drop the recursive `AFTER UPDATE` trigger (postmortem Mistake 14). Not applied — informational only.

**Validation:**
- `python kilor.py check` — ✅ 35 errors (5 new from batch-008 single-form masks, 30 pre-existing; no regressions)
- See `draft/audit-batch-postmortem.md` for full audit pipeline postmortem (16 documented mistakes & lessons)

## workspace v1.5.1 — 2026-07-28

Audio hygiene: orphaned file detection & cleanup, bidirectional `audio --check`, auto-regenerate audio after `--fix-typo` rename.

**DB / Backend:**
- **`kilor/commands/edit.py`** — `--fix-typo` now auto-regenerates audio for the renamed word (if espeak-ng + ffmpeg are available). Falls back to a warning with manual regeneration command if toolchain is unavailable. Added `_regenerate_audio_after_rename()` helper.
- **`kilor/commands/audio.py`** — Added `--check-orphaned` action: lists `.ogg` files with no matching DB row. Added `--cleanup` action: deletes orphaned files (prompts for confirmation unless `--yes` passed). `--check` is now bidirectional: reports both missing files (DB→disk) and orphaned files (disk→DB). Added `_find_orphaned_audio()` helper.
- **`kilor/__main__.py`** — Wired `--check-orphaned`, `--cleanup`, and `--yes` flags for the `audio` subcommand.

**Validation:**
- `python kilor.py check` — ✅ All entries pass

## workspace v1.5.0 — 2026-07-28

IPA-to-speech audio pronunciation (experimental, off by default). espeak-ng + ffmpeg generate Ogg Opus files. 🔊 button appears next to IPA when enabled in Settings.

**Frontend:**
- **`TableView.jsx`** — Added `PronounceButton` component (🔊) in IPA column of table rows, detail panel, and word detail page. Button renders only when `showAudio` is true. Uses persistent `<audio id="audio-player">` element to avoid browser autoplay-policy issues. Audio URL is `./audio/{id}.ogg` (relative, works with Vite base path).
- **`SettingsPanel.jsx`** — Added "Audio pronunciation 🔊 (experimental)" checkbox (default off).
- **`Header.jsx`** — Forwards `showAudio`/`onToggleAudio` props to SettingsPanel.
- **`App.jsx`** — Added `showAudio` state (default false), passes to Header, TableBody, and WordDetailPage. Added hidden `<audio id="audio-player" preload="auto">` element.
- **`App.css`** — `.pronounce-btn`, `.pronounce-btn-inline`, `.pronounce-btn-detail` styles. `.td-form` cursor:copy moved to `.td-form-text`.

**DB / Backend:**
- **`kilor/commands/audio.py`** (new) — CLI command: `python kilor.py audio --generate` synthesizes `.ogg` Opus files for all words via espeak-ng → temp WAV → ffmpeg pipeline. Also supports `--id WORD_ID` and `--check`.
- **`kilor/__main__.py`** — Registered `audio` subcommand.
- **`kilor/dictionary/public/audio/`** — 403 `.ogg` audio files (2.0 MB total, ~9.5× smaller than WAV). Tracked in git (removed from .gitignore).

**Validation:**
- `python kilor.py check` — ✅ All entries pass
- `npx vitest --run src/App.test.jsx` — ✅ 50/50 pass


## workspace v1.4.1 — 2026-07-27

Settings panel, last-modified column, table header/body column alignment fix, autocomplete dismissal on table hover.

**Frontend:**
- **`SettingsPanel.jsx`** (new) — Gear icon (⚙) in header opens settings dropdown with "Show Last Modified column" checkbox. Dropdown dismissed by clicking outside or the close button.
- **`Header.jsx`** — Added gear icon button and `SettingsPanel` to header-right.
- **`App.jsx`** — Added `showModified` state (default false, persisted to URL `?mod=1`) and `settingsOpen` state. Passed `showModified` to `TableHeader` and `TableBody`. Added `onMouseEnter={() => setAutocompleteItems([])}` to `.table-header-bar` and `.main-content` — moving cursor to table area dismisses autocomplete suggestions so results are visible.
- **`Toolbar.jsx`** — Added `onFocus` handler to re-show autocomplete suggestions when clicking back into the search box after dismissal.
- **`TableView.jsx`** — `buildColGroup()` now takes `showModified` prop and returns 7 or 8 `<col>` elements. `TableHeader` and `TableBody` render conditional "Modified" column. `formatUpdatedAt()` formats `updated_at` as `YYYY-MM-DD HH:MM`. Detail row `colSpan` is dynamic (7 or 8).
- **`App.css`** — `.settings-gear-btn`, `.settings-overlay`, `.settings-dropdown`, `.settings-header`, `.settings-row` styles. Settings dropdown: `position: fixed; top: 56px; right: 24px`. `.table-header-bar`: `overflow-y: auto; scrollbar-gutter: stable` (was `overflow: hidden` — needed for `scrollbar-gutter` to work). `.word-table-header`: added `width: 100%; border-collapse: separate; border-spacing: 0` to match `.word-table-body` exactly. `.td-modified` style.

**DB / Backend:**
- **`db.js`** — `queryWords()` SELECT includes `w.updated_at`. `enrichEntries()` passes `updated_at` through to entry objects. `buildTestDB()` table schema includes `updated_at TEXT`. Added `case 'updated'` sort switch handler. Fuzzy search query also fetches `w.updated_at`.

**Validation:**
- `npx vitest run` — ✅ 39/39 pass (30 App + 9 db.reload)
- New tests: 5 table alignment tests (dual `scrollbar-gutter`, column parity default & with modified column, gear button existence, colgroup width match)

## workspace v1.4.0 — 2026-07-27

Stream C UI features + export flags: IPA column in table, colour prefix legend modal, --lite and --no-standalone export flags, schema indexes. See also: CHANGELOG.md v1.19.0.

**Frontend:**
- **`TableView.jsx`** — New IPA column in main table (7-column layout: Word, IPA, Gloss, Type, Prefix, NVAD, Syl). New `PrefixLegend` component: `?` icon in Prefix header opens modal overlay with all 7 colour prefixes, swatches, class names, and emotions. `detail-tr` colSpan updated to 7.
- **`App.css`** — IPA column styles (`.td-ipa`, serif font). Prefix legend styles: trigger button (`.prefix-legend-trigger`), overlay (`.prefix-legend-overlay`), modal (`.prefix-legend-modal`), grid rows (`.prefix-legend-row`, `.prefix-legend-swatch`, `.prefix-legend-label`), close button. Pagination bar styles (`.pagination-bar`, `.pagination-btn`).

**DB / Backend:**
- **`export.py`** — `_export_html()` and `cmd_export()` accept `lite` and `no_standalone` kwargs. `--lite`: creates temp stripped DB (drops `examples`, `compound_meta`, `compound_components`, `inflections`) and VACUUMs. `--no-standalone`: skips base64 embedding, outputs companion `dictionary.db` alongside `dictionary.html`; app fetches via `./dictionary.db`. Temp dir cleanup after export.
- **`__main__.py`** — Parses `--lite` and `--no-standalone` flags for `export` command, passes to `cmd_export()`.
- **`data/kilor.db`** — `idx_words_colour` and `idx_words_syl_count` indexes created on live DB (already in `SCHEMA_SQL`).

**Validation:**
- `npx vitest run` — ✅ 34/34 pass
- `npx vite build` — ✅ Clean: 274KB JS, 12KB CSS, 660KB WASM
- `python kilor.py check` — ✅ 25 pre-existing errors (none new)

## workspace v1.3.0 — 2026-07-27

Frontend scaling: SQL-level pagination (50 words/page), 300ms search debounce, fuzzy search capped at 30 results. Stale `react-window` dependency removed. See also: CHANGELOG.md v1.19.0.

**Frontend:**
- **`db.js`** — `queryWords()` now returns `{ rows, totalCount }` with `page`/`pageSize` params. Added `LIMIT`/`OFFSET` to SQL queries. Added separate COUNT query for total. Extracted `buildFilterClauses()` to share WHERE logic across both queries. `fuzzySearch()` returns `{ rows, totalCount }`, capped to top 30 (was unbounded). `buildTestDB()` schema: added `pos` column to `meanings` table + accepts mixed string/object meanings.
- **`App.jsx`** — Added `searchDraft`/`search` split with 300ms debounce via `useEffect` + `setTimeout`. Added `page` state, resets to 1 on search/filter/sort change. Wires `page` and `totalPages` to `TableView`. Updated `fuzzySearch` caller to use `fuzzyResult.rows`.
- **`TableView.jsx`** — New `PaginationBar` component (Previous/Next buttons, "X–Y of Z" indicator, page count, attached below table). Hidden when only 1 page. `TableBody` accepts and forwards `page`, `totalPages`, `totalCount`, `onPageChange` props.
- **`vite.config.js`** — Fixed WASM path: `fs.allow` from `['..']` to `['../..']` (sql.js WASM lives at root `node_modules/`, two levels up from `kilor/dictionary/`).
- **`package.json`** — Removed stale `react-window` dependency (leftover from 3 failed virtual scrolling attempts).

**Tests:**
- **`App.test.jsx`** — Updated all tests: dynamic word count (no hardcoded "361"), `typeAndWait()` helper for 300ms debounce, `beforeEach`/`afterEach` for URL reset + cleanup. Removed stale `.section` references. Added "view full entry" workflow test (search → expand → full detail → back). 25/25 pass.
- **`db.reload.test.js`** — Updated all tests for `{ rows, totalCount }` return type from `queryWords()`. Fixed all synthetic test words to use valid Kilor forms (consonant-final words crashed `splitSyllablesJS`). 9/9 pass.

**Validation:**
- `npx vitest run` — ✅ 34/34 pass (25 App + 9 db.reload)
- `npx vite build` — ✅ 44 modules, 272KB JS, 10KB CSS, 660KB WASM
- `python kilor.py check` — ✅ 25 pre-existing errors (none new)

## workspace v1.2.0 — 2026-07-27

Compound backfill review applied to live DB. 67 flagged compounds corrected: 6 prefix updates, 16 component re-links, 51 is_root conversions, 1 deletion (arrinna), 1 rename (ero isra→erolise isra), 2 meaning updates. Four new suffix roots added (lu, rin, par, nous). ous renamed to nous. Spec updated: derivational-compounding.md v2.5.0→2.6.0.

**DB / Backend:**
- **`data/kilor.db`** — 67 compound entries updated across `words`, `meanings`, `compound_components`, `compound_meta` tables. 1 word deleted (arrinna, ID 246). 1 word renamed (ero isra→erolise isra, ID 313). 4 new roots added: `lu` (o-, N), `rin` (o-, N), `par` (e-, NV), `nous` (o-, N, renamed from `ous` ID 177). 1 new compound: `rinok param` (ID 413, multi, result pattern, measurement). `rinok` mask N→NV. `pireilu` is_compound→0, is_root→1. `nous` is_function_word=1. FTS rebuilt.

**Spec:**
- **`rules/3-subsystems/derivational-compounding.md`** — v2.5.0→2.6.0. §I table: From Root updated (pireilu→lu, rinok→rin, chap→par). §I-E Process prefix: o-→e-. §V-A: Process nouns moved from Abstract to Crafted.

**Validation:**
- `python kilor.py check` — ✅ 25 errors (all pre-existing; no new errors from our changes)

See also: `CHANGELOG.md` v1.18.0 for spec-side details.

## workspace v1.1.0 — 2026-07-26

Added `pos` column to `meanings` table (15-value PoS taxonomy). Word detail subpage with PoS-grouped meaning display. Pipeline: `add.py` parses new per-PoS `today.md` templates; `edit.py` `--add-meaning` accepts `--pos` flag.

**Frontend:**
- **`TableView.jsx`** — New `GlossWithPos` component: inline PoS tags in table gloss column (N, V, A, D, CONJ, ADP, PART etc.). Click "View full entry →" in accordion opens subpage. New `WordDetailPage` component: full-width dictionary entry with identity card, meanings grouped by PoS sections, inflections, case forms, components, pattern, examples, notes. Two-tier PoS labels: minimal abbreviations in table rows with hover tooltips; full descriptive labels (Noun, Verb, Pronoun, Demonstrative, etc.) in subpage sections.
- **`App.jsx`** — Added `detailId` state (from `?detail=` URL param). Conditional rendering: table body vs `WordDetailPage`. Back button preserves filter state. Import `WordDetailPage` from TableView.
- **`App.css`** — PoS inline tag styles (`.pos-tag-inline`, `.gloss-sep`, `.gloss-more`). Detail subpage layout (`.word-detail-page`, `.detail-identity-card`, `.detail-content-columns`, `.detail-main`, `.detail-sidebar`). PoS section headers (`.pos-section-header`, `.pos-meaning-list`). Responsive sidebar collapse. Back button, "View full entry" link.
- **`db.js`** — `queryWords` now selects `GROUP_CONCAT(m.pos, ' | ') AS poses_concat`. `enrichEntries` zips glosses with poses into `[{gloss, pos}]` arrays.

**DB / Backend:**
- **`data/kilor.db`** — `ALTER TABLE meanings ADD COLUMN pos TEXT DEFAULT ''`. Backfilled 483 meanings across 15 PoS tags (N, V, A, D, PRON, NUM, CCONJ, SCONJ, ADP, PART, MODAL, DEM, Q, CLF, INTERJ, PROPN).
- **`kilor/schema.py`** — `SCHEMA_SQL` includes `pos` column. Added `VALID_POS` frozenset (15 tags + empty for legacy). Added `POS_LABELS` dict mapping tags to display names.
- **`kilor/api.py`** — `_word_to_dict` returns meanings as `{"gloss": "...", "pos": "..."}` objects. Fixed search text aggregation for new format.
- **`kilor/commands/add.py`** — New `_parse_field()` function parses two `today.md` template formats: content word (per-PoS `Meaning (N)`, `Meaning (V)` fields) and function word (`POS` field + single `Meaning`). Inserts `pos` on all meanings rows. Comma-separated senses in per-PoS fields become multiple rows with same `pos`. Function words flag `is_function_word=1` and skip inflection generation. Legacy `| Meaning |` field still supported with empty `pos`.
- **`kilor/commands/edit.py`** — `--add-meaning` accepts optional `--pos` flag. `sort_order` now scoped within same `pos`. Import `VALID_POS` for validation.
- **`kilor/__main__.py`** — Wired `--pos` flag for `edit` command in CLI argument parser.

**Validation:**
- `python kilor.py check` — ✅ 22 errors / 1,224 warnings (all pre-existing)
- Frontend build: ✅ 44 modules, 551ms, no new errors

---

## workspace v1.0.0 — 2026-07-26

Dictionary frontend overhaul: sticky table headers, bidirectional sort, relevance-ranked search, inflection/case form search, fuzzy "Did you mean?" fallback, IPA notation, filter chips, keyboard shortcuts, autocomplete, copy-to-clipboard, URL state persistence. Backend: `search_text` column for precomputed search forms.

**Frontend — Layout:**
- **`kilor/dictionary/src/App.css`** — Grid-based layout (`grid-template-rows: auto auto auto 1fr`) with HTML body overflow lock. Table header row physically separated from scrollable body table. `border-collapse: separate` on body table. Sticky column headers replaced with fixed-position separate table. Fuzzy banner style, filter chips bar, autocomplete dropdown, search match highlighting (`mark.search-highlight`), toast notification, row-keyboard-selected outline.
- **`kilor/dictionary/src/components/TableView.jsx`** — Split into `TableHeader` (exports `TableHeader`, `TableBody`, default `TableView`). Shared `COLGROUP` with `table-layout: fixed` for column alignment. Sort arrows: inactive `↕`, active `▲`/`▼`. `highlightMatch()` for search term highlighting. `DetailPanel` shows inflections in N→V→A→D order, IPA line, single-mask tuple display. Copy-to-clipboard on word click with guard for jsdom environment.
- **`kilor/dictionary/src/components/Toolbar.jsx`** — Added search-wrapper div with autocomplete dropdown (`autocomplete-dropdown` UL). Autocomplete items navigable by arrow keys.
- **`kilor/dictionary/src/App.jsx`** — Added filter chips (FilterChips component), keyboard shortcuts (Esc/↑↓/Enter, gated to search focus), clipboard toast, fuzzy fallback with yellow banner, URL state read/write for shareable searches. Imports `fuzzySearch`, `autocompleteSearch`. `handleSort` refactored from nested-state-updater to flat if/else.
- **`kilor/dictionary/src/main.jsx`** — Unchanged.

**Frontend — Data Layer:**
- **`kilor/dictionary/src/db.js`** — Major additions:
  - `queryWords()`: 4-tier relevance scoring via `CASE WHEN` (form-prefix > form-contains > search_text > gloss). WHERE clause includes `w.search_text` for inflection/case form matching. Search overrides sortCol with relevance ordering.
  - `autocompleteSearch(term)`: top 5 form matches, prefix-priority ordered.
  - `fuzzySearch(term)`: Levenshtein distance ≤1 (≤3 chars) / ≤2 (4–6 chars) / ≤3 (7+ chars). Returns enriched entries with `fuzzyDistance`.
  - `computeInflections(form, syl_count, derivationMask)`: client-side inflection computation from prosody rules — 1–2 syl toneless (N/V=bare, A/D=+s), 3+ syl tone markers (j on 1st of last-3 for N/V, 2nd for A/D; v on 1st for V, 2nd for D). Single-mask words return `[base, tonemarked]` tuples. N→V→A→D order. Replaces stored `inflections` table.
  - `toIPA(word)`: full IPA mapper from `phonology.md` — 7 monophthongs, 7 diphthongs, 34 consonants. Tone markers: j→˥, v→˩.
  - `_syllablePositions(word)`: tone-preserving syllable splitter for inflection anchor calculation.
  - `enrichEntries(rows)`: batch enrichment — 4 queries per result set instead of N×4 (from 40,000 queries at 10k results to 4). Wired to `computeInflections` + `toIPA`.
  - `buildTestDB()`: Added `search_text` column.

**Backend:**
- **`kilor/schema.py`** — Added `search_text TEXT DEFAULT ''` column to `words` table.
- **`kilor/db.py`** — Added `populate_search_text(conn)`: computes all inflection forms (toneless + tonemarked) + case forms (ACC, GEN) per word and stores in `search_text`. Auto-creates column if missing. Called after DB changes.
- **`kilor/commands/add.py`** — Calls `populate_search_text()` after inserting new words.
- **`kilor/commands/edit.py`** — Calls `populate_search_text()` after any edit (mask change, typo fix, prefix, meaning, example).

**DB:**
- **`data/kilor.db`** — `search_text` column populated for all 400 existing entries via `populate_search_text()` migration.
- DB size may have changed due to new column and extended text data.

**Validation:**
- `python kilor.py check` — Not yet verified (please run before finalizing this entry).
- `npx vitest --run src/App.test.jsx` — 15/24 pass. 5 pre-existing `'361'` vs `'400'` count mismatch failures. 4 URL state cross-test contamination (all pass individually).