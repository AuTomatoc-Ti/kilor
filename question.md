# Kilor — Deferred Design Questions

**Status:** Open for review
**Created:** 2026-07-04

---

## 1. Pronoun Inventory

**Context:** Currently deferred. `cases.md` §IV-B states that possession by pronoun is expressed by attaching the Genitive suffix to the pronoun root, but no pronoun roots exist yet.

**Questions:**
- Person system: 1st / 2nd / 3rd? Inclusive/exclusive we?
- Number: singular / plural only, or dual/trial as well?
- Gender distinction in 3rd person?
- Formality levels (casual vs polite)?

---

## 2. Article System

**Context:** Deferred. `nouns-colour-prefix.md` §IV-A references articles (`a`/`an`/`the`) and determiners (`this`/`that`) as triggers for mandatory colour prefix usage, but the article inventory is undefined.

**Questions:**
- Will there be a definite article (`the`) and indefinite article (`a`/`an`)?
- Or will definiteness be handled entirely by the colour prefix's definiteness rules (§IV)?
- If articles exist, what are they phonologically?

---

## 3. Dative & Instrumental Particle Expansion

**Context:** `te` (dative: to/for) and `su` (instrumental: with/by) are reserved slots. `cases.md` §V defines them as standalone single-syllable words with flat mid-tone.

**Questions:**
- Will there be additional particles beyond `te` and `su`? (e.g., locative, ablative, comitative, benefactive)
- Or will all other oblique roles be handled by context + the 3 case system?

---

## 4. Interrogative Structure

**Context:** Entirely deferred. No mechanism exists to form questions.

**Questions:**
- Particle-based (e.g., sentence-final `ma` like Mandarin 嗎)?
- Wh-words in situ (like Japanese) or fronted (like English)?
- Yes/no questions via intonation alone?
- Tag questions?

---

## 5. Negation

**Context:** Not mentioned in any rule file. The language currently has no way to express negation (e.g., "I do not eat").

**Questions:**
- Standalone negation particle (like English `not`)?
- Prefix on verbs (like Esperanto `ne-`)?
- Separate negative verb conjugation (like Finnish)?
- Where does the negator sit in the sentence?

---

## 6. Numeral & Classifier System

**Context:** Deferred. `grammar-syntax.md` §VII references numeral + classifier constructions for explicit quantification, but no numerals or classifiers are defined.

**Questions:**
- Base system: base-10, base-7 (matching the 7 colours), or other?
- Are classifiers required with numerals (like Chinese/Japanese) or optional (like English)?
- If classifiers, what semantic categories (shape, animacy, function)?

---

## 7. Subordinate Clauses & Relativization

**Context:** Not mentioned in any rule file. No mechanism exists for embedding clauses (e.g., "the fire that burns", "I know that you came").

**Questions:**
- Relative clauses: prenominal (like Japanese), postnominal (like English), or correlative?
- Complement clauses (e.g., "I know that..."): particle, nominalization, or parataxis?
- Adverbial subordination (when, because, if): particles or conjunctions?

---

## 8. Copula & Existential Verbs

**Context:** Not mentioned. No "to be" verb is defined.

**Questions:**
- Is there a copula (like English `is`), or is it zero-copula (like Chinese 是 being optional)?
- Existential constructions ("there is/are"): separate verb, particle, or context?
- Predicate adjectives (e.g., "the fire is hot"): how are they expressed?

---

## 9. Phonetic Root Inventory — `ae` as Prefix vs Monophthong

**Context:** `ae` is both a 7-monophthong vowel (/æ/) in `phonology.md` and a colour prefix (`ae-` for Brown). It's also listed in the Front/Bright vowel class for harmony purposes. The two-letter representation is unambiguous in isolation but could create parsing issues at word boundaries.

**Questions:**
- Could `ae` at word start ever be ambiguous between "Brown prefix" vs "word beginning with /æ/"? 
- Is this a theoretical concern or worth addressing now?

---

## General Design Philosophy Questions

- **Priority order:** Which of these 9 areas should be addressed first?
- **Simplicity vs expressiveness:** On a spectrum from Toki Pona (~120 words) to Esperanto (full expressive grammar), where should Kilor land?
- **Naturalism vs regularity:** Should Kilor aim for natural-language-like quirks and exceptions, or remain fully regular?

---

*End of Deferred Design Questions.*