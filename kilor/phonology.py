"""Phonotactics, syllable counting, and validation for Kilor words.

Positional consonant classes (SSOT: rules/0-foundation/phonology.md §IV):
  - Core (§IV-A): 15 consonants, appear anywhere
  - Edge-Only (§IV-B): 3 consonants, word-initial or word-final only (sh, ch, th)
  - Start-Only (§IV-C): 13 consonants, absolute word-initial only
  - End-Only (§IV-D): 3 consonants, absolute word-final only (ng, x, rk)

Mid-word disambiguation (§IV-E): multi-character sequences appearing anywhere
other than absolute word edges are always two separate core consonants, never
the single Kilor letter.
"""

VOWELS = set("aeiouy")
DIPHTHONGS = {"ai", "au", "ei", "eu", "iu", "oi", "ou"}
CORE_CONS = set("pbmfwtdnslrckgh")
EDGE_ONLYS = {"sh", "ch", "th"}
START_ONLYS = {"kl", "tl", "bl", "ml", "kr", "br", "gr", "fr", "pr", "sr"}
END_ONLYS = {"ng", "x", "rk"}
_MULTICHAR_CORE = {"qy"}  # Core consonants represented by two ASCII characters

# All multi-character single-letter sequences (for mid-word disambiguation)
_ALL_MULTICHAR = EDGE_ONLYS | START_ONLYS | END_ONLYS | _MULTICHAR_CORE

S_FINAL_WHITELIST = {
    "os", "gus", "fos", "thes", "aus", "ous", "les", "mangus",
    "rius", "meus",
    "kas", "hus", "tus", "rakas", "fidak",
    "wes", "mlis",
}


def count_syllables(word):
    """Count vowel nuclei in a Kilor word."""
    count = 0
    i = 0
    while i < len(word):
        if word[i].lower() in VOWELS:
            count += 1
            if word[i : i + 2].lower() == "ae":
                i += 2
            elif i + 1 < len(word) and word[i : i + 2].lower() in DIPHTHONGS:
                i += 2
            else:
                i += 1
        else:
            i += 1
    return count


def split_syllables(word):
    """Greedy left-to-right syllable parser.

    Uses the Maximal Onset Principle: an intervocalic core consonant is assigned
    to the onset of the next syllable, not the coda of the current one.

    Respects positional consonant classes:
      - Start-only and edge-only letters only match at i == 0 (onset)
      - End-only and edge-only letters only match at word-final position (coda)
      - Mid-word multi-character sequences are parsed as separate core consonants

    Strips tone markers (j, v), prefix hyphens, and spaces before parsing.
    Tone markers are extra-segmental (§V-A). Spaces indicate multi-word
    compounds and are handled by splitting before this function is called;
    stripping them here is a defensive fallback.
    """
    word = word.replace("j", "").replace("v", "").replace("-", "").replace(" ", "")
    n = len(word)
    if n == 0:
        return []

    syllables = []
    i = 0
    while i < n:
        onset = ""
        # --- Onset ---
        # Multi-char core consonants (e.g. qy) can be onset anywhere
        if i + 2 <= n and word[i : i + 2] in _MULTICHAR_CORE:
            onset = word[i : i + 2]
            i += 2
        elif i == 0 and i + 2 <= n and word[i : i + 2] in START_ONLYS:
            onset = word[i : i + 2]
            i += 2
        elif i == 0 and i + 2 <= n and word[i : i + 2] in EDGE_ONLYS:
            onset = word[i : i + 2]
            i += 2
        elif i < n and word[i] in CORE_CONS:
            onset = word[i]
            i += 1

        # --- Nucleus ---
        if i >= n:
            raise ValueError(f"incomplete syllable in '{word}' at position {i}")
        nucleus_start = i
        if word[i] in VOWELS:
            if word[i : i + 2] == "ae":
                i += 2
            elif i + 1 < n and word[i : i + 2] in DIPHTHONGS:
                i += 2
            else:
                i += 1
        nucleus = word[nucleus_start:i]
        if not nucleus:
            raise ValueError(
                f"degenerate syllable in '{word}' at position {i}: "
                "consonant taken as onset but no vowel follows"
            )

        # --- Coda ---
        # Maxonset principle: an intervocalic consonant goes to the onset of
        # the next syllable. A consonant is only taken as coda when:
        #   - it is a multi-char end-only/edge-only letter at absolute word end, OR
        #   - it is a single-char end-only letter at absolute word end, OR
        #   - it is a multi-char core consonant at word end, OR
        #   - it is a core consonant at word end (no following vowel), OR
        #   - it is a core consonant followed by another consonant
        coda = ""
        if i < n:
            # Multi-char core consonants: can be coda at word-final
            if i + 2 <= n and word[i : i + 2] in _MULTICHAR_CORE and i + 2 == n:
                coda = word[i : i + 2]
                i += 2
            # End-only letters (multi-char): only at absolute word-final position
            elif i + 2 <= n and word[i : i + 2] in END_ONLYS and i + 2 == n:
                coda = word[i : i + 2]
                i += 2
            # Edge-only letters (multi-char): may appear as coda only at word-final
            elif i + 2 <= n and word[i : i + 2] in EDGE_ONLYS and i + 2 == n:
                coda = word[i : i + 2]
                i += 2
            # End-only letters (single-char, e.g. 'x'): only at word-final
            elif i + 1 == n and word[i] in END_ONLYS:
                coda = word[i]
                i += 1
            elif word[i] in CORE_CONS:
                # Take as coda only if at word end OR next char is not a vowel
                if i + 1 >= n or word[i + 1] not in VOWELS:
                    coda = word[i]
                    i += 1
                # else: leave for next syllable's onset (maxonset)

        syllables.append(onset + nucleus + coda)

    return syllables


def validate_root(root):
    """Validate a bare root against phonotactics. Returns (is_valid, error_message).

    Positional consonant classes (start-only, end-only, edge-only) are enforced
    structurally by the syllable parser and the mid-word disambiguation rule
    (see rules/0-foundation/phonology.md §IV-E): any multi-character sequence
    appearing mid-word is always parsed as two separate core consonants, never
    as the single Kilor letter. Consequently, mid-word appearances of sequences
    like 'sh', 'ng', 'kr', etc. are always valid — they represent separate
    core consonants.

    The only positional validation needed is at word edges, and the syllable
    parser already enforces edge placement structurally.
    """
    if not root:
        return False, "empty root"
    if "j" in root or "v" in root:
        return False, f"root '{root}' contains 'j' or 'v' (reserved for tone)"
    syl_count = count_syllables(root)
    if syl_count == 0:
        return False, f"root '{root}' has no vowel nucleus"
    if syl_count > 5:
        # Rule 5 is a soft guideline, not a hard cap: most Kilor roots are
        # 1–5 syllables, but entrained/lexicalised compounds may exceed 5.
        # Real languages carry long exceptional forms, so this is advisory
        # only (non-blocking). User-settled 2026-08-21.
        return True, f"root '{root}' has {syl_count} syllables (over the usual 5-syllable guideline, permitted as an exception)"
    return True, ""


def validate_content_root(root, is_func=False, is_compound=False):
    """Validate a content root (not function word). Adds -s constraint."""
    if is_func:
        return True, ""
    valid, err = validate_root(root)
    if not valid:
        return False, err
    syl_count = count_syllables(root)
    if 1 <= syl_count <= 2 and root.endswith("s"):
        if root.lower() not in S_FINAL_WHITELIST and not is_compound:
            return False, (
                f"root '{root}' is {syl_count}-syllable and ends in 's' "
                "(-s is reserved for derivation)"
            )
    return True, ""


# ── Compound-boundary positional check (compounding.md §III Rule 2 / Rule 2b) ──
#
# Rule 2 (compounding.md §III): in a mono-word compound, a start-only, end-only,
# or edge-only consonant may NOT appear in a non-peripheral (medial) position —
# that forces a multi-word compound instead.
#
# Rule 2b — Boundary Vowel-Repair Exemption (general, covers ALL classes):
# a positionally-restricted consonant (start-only, end-only, or edge-only) is
# legal in a medial compound slot if and only if a vowel immediately adjoins it
# on the side its positional class forbids — i.e. the repair vowel sits on the
# consonant's restricted side, re-syllabifying it across the seam:
#   - start-only / edge-only ONSET ← needs the modifier-final vowel BEFORE it
#   - end-only / edge-only CODA → needs the head-initial vowel AFTER it
# The repair is symmetric and class-general (mirrors numerals.md §II-B `sl`).
# Only a boundary with no vowel on the required side stays a Rule-2 block.
#
# Surface-elision: a restricted digraph that does not survive in the stored
# surface (abbreviating suffix/combining heads like tlar→tar, mlis→is) does not
# occupy a medial slot at all, so it is not flagged.
#
# SSOT: rules/0-foundation/phonology.md §IV (positional classes), §IV-E (mid-word
# disambiguation); rules/3-subsystems/compounding.md §III Rule 2/2b.

def _strip_tone(word):
    return word.replace("j", "").replace("v", "").replace("-", "")


def _leading_letter(word):
    """Return the first Kilor letter of word (longest multichar match wins)."""
    w = _strip_tone(word)
    for fc in sorted(_ALL_MULTICHAR, key=len, reverse=True):
        if w.startswith(fc):
            return fc
    return w[0] if w else ""


def _trailing_letter(word):
    """Return the last Kilor letter of word (longest multichar match wins)."""
    w = _strip_tone(word)
    for lc in sorted(_ALL_MULTICHAR, key=len, reverse=True):
        if w.endswith(lc):
            return lc
    return w[-1] if w else ""


def _validate_mono_surface(components, surface):
    """Validate a mono compound's boundaries against Rule 2 / Rule 2b (general).

    Uses COMPONENTS only to classify each restricted letter's MORPHEMIC ROLE
    (which component it belongs to): first letter of a non-first component →
    ONSET (needs a vowel BEFORE it); last letter of a non-last component → CODA
    (needs a vowel AFTER it). The vowel-adjacency DECISION is made on the actual
    SURFACE, not the raw component edge — because a restricted digraph that is
    surface-elided or surface-bridged (e.g. `tlar`→`tar`, `mlis`→`is`,
    `ilat`+`thes`→`ilathes` where the merged `t`+`th` leaves a vowel before `th`)
    occupies no medial slot. So a restricted onset is legal iff a vowel
    immediately precedes its surface occurrence; a restricted coda iff a vowel
    immediately follows it.

    Returns a list of error message strings (empty if boundary-legal).
    """
    errors = []
    VOWEL_LIKE = VOWELS | {"ae"}
    surface_clean = _strip_tone(surface).lower()

    for i in range(len(components)):
        comp = components[i]

        # --- Onset role: first letter of a NON-first component ---
        if i >= 1:
            lead = _leading_letter(comp).lower()
            if lead in START_ONLYS or lead in EDGE_ONLYS:
                # Only enforce if the digraph actually survives in the surface
                if lead in surface_clean:
                    b = surface_clean.find(lead)
                    prev_seg = surface_clean[b - 1] if b - 1 >= 0 else ""
                    if prev_seg not in VOWEL_LIKE:
                        modifier = components[i - 1]
                        errors.append(
                            f"[Rule 2/2b] mono compound '{surface}': {lead} is the "
                            f"{'start-only' if lead in START_ONLYS else 'edge-only'} onset "
                            f"of '{comp}' but nothing before it in the surface is a vowel "
                            f"(prev='{prev_seg}') — use multi-word or a vowel-final modifier"
                        )

        # --- Coda role: last letter of a NON-last component ---
        if i < len(components) - 1:
            trail = _trailing_letter(comp).lower()
            if trail in END_ONLYS or trail in EDGE_ONLYS:
                # Only enforce if the digraph actually survives in the surface
                if trail in surface_clean:
                    b = surface_clean.find(trail)
                    nxt = surface_clean[b + len(trail) : b + len(trail) + 1]
                    if nxt not in VOWEL_LIKE:
                        head = components[i + 1]
                        errors.append(
                            f"[Rule 2/2b] mono compound '{surface}': {trail} is the "
                            f"{'end-only' if trail in END_ONLYS else 'edge-only'} coda "
                            f"of '{comp}' but nothing after it in the surface is a vowel "
                            f"(next='{nxt}') — use multi-word or a vowel-initial head"
                        )
    return errors


def validate_mono_compound_boundaries(components, surface=None):
    """Validate the internal morpheme boundaries of a mono-word compound.

    Components are the stored roots (by form) in order; `surface` is the fused
    word as actually stored (may elide letters, e.g. tlar→tar, mlis→is).

    Rule 2b (general, covers all positional classes): a positionally-restricted
    consonant at a compound boundary is legal mono when a vowel adjoins it on the
    side its morphemic role needs:
      - ONSET (head-initial start/edge-only) ← modifier-final vowel BEFORE
      - CODA (modifier-final end/edge-only) → head-initial vowel AFTER
    A restricted digraph that is elided in the surface (abbreviated suffix/
    combining head like `tlar`→`tar`, `mlis`→`is`) is not a medial-slot violation.

    Args:
        components: list of component root forms, in compound order.
        surface: the stored fused surface form (or None → concatenates components).

    Returns:
        list of error message strings (empty if the compound is boundary-legal).
    """
    if len(components) < 2:
        return []

    if surface is None:
        surface = "".join(_strip_tone(c) for c in components)

    return _validate_mono_surface(components, surface)


# ── Case-Form Generation ──────────────────────────────────────────────────────

# Pronouns use invariant reduced case endings (SSOT: rules/1-nominals/pronouns.md §III)
_PRONOUN_ACC_GEN = {
    "ki":   ("kin",   "kis"),
    "ti":   ("tin",   "tis"),
    "si":   ("sin",   "sis"),
    "ni":   ("nin",   "nis"),
    "kilo": ("kilon", "kilos"),
    "tilo": ("tilon", "tilos"),
    "silo": ("silon", "silos"),
    "nilo": ("nilon", "nilos"),
}

# Colour prefixes that may appear on the form (SSOT: rules/0-foundation/philosophy.md)
_COLOUR_PREFIXES = {"a-", "e-", "i-", "o-", "u-", "y-", "ae-"}

# Front vowels → use back suffixes (-na, -sa). Back vowels → use front suffixes (-ni, -si)
_FRONT_VOWELS = {"e", "i", "y", "ae", "ei", "eu", "iu"}
_BACK_VOWELS  = {"a", "o", "u", "ai", "au", "oi", "ou"}


def _last_nucleus(word):
    """Return the last syllable's vowel nucleus from a Kilor word.

    Scans from right to left, skipping trailing consonants. Does NOT use
    split_syllables (which can infinite-loop on tone markers or other
    characters outside the core consonant/vowel sets).

    Strips tone markers (j, v) and prefix hyphens first — both are
    extra-segmental per the phonology spec.
    """
    cleaned = word.replace("j", "").replace("v", "").replace("-", "")
    if not cleaned:
        return ""
    n = len(cleaned)

    # Scan backwards to find the last vowel/diphthong
    i = n - 1
    while i >= 0:
        ch = cleaned[i].lower()
        # Check for diphthong starting at i-1 (2-char nucleus)
        if i >= 1:
            pair = cleaned[i - 1 : i + 1].lower()
            if pair in DIPHTHONGS:
                return pair
            if pair == "ae":
                return "ae"
        # Check for single vowel
        if ch in VOWELS:
            return ch
        i -= 1
    return ""


def _strip_prefix(form):
    """Strip the colour prefix from a form. Returns (prefix, root)."""
    for pfx in sorted(_COLOUR_PREFIXES, key=len, reverse=True):
        if form.startswith(pfx):
            return pfx, form[len(pfx):]
    return "", form


def get_case_forms(form, derivation_mask=None, is_function_word=False, compound_type=None):
    """Compute ACC and GEN case forms for a Kilor word.

    Returns (acc_form, gen_form) or (None, None) if the word is not case-eligible.

    Args:
        form: The word form as stored in the DB (e.g. 'fora', 'a-fora', 'lumi sola')
        derivation_mask: NVAD mask string (e.g. 'NVA', 'NA'). None if unknown.
        is_function_word: True for closed-class particles (case-exempt).
        compound_type: 'mono', 'multi', or None for roots.

    Rules (SSOT: rules/1-nominals/cases.md §II–IV):
      - Function words are case-exempt → (None, None)
      - Words without 'N' in derivation_mask cannot take case → (None, None)
      - Pronouns use invariant reduced endings (-n, -s)
      - Multi-word compounds: suffix attaches to the last word only
      - Colour prefix is ignored for suffix vowel selection but preserved in output
      - Contrastive Suffix Rule: suffix vowel opposite to root's last nucleus
    """
    if is_function_word:
        return None, None
    if derivation_mask is not None and "N" not in derivation_mask.upper():
        return None, None

    # Check for pronouns (invariant forms)
    if form in _PRONOUN_ACC_GEN:
        return _PRONOUN_ACC_GEN[form]

    # Multiple words (e.g. 'lumi sola') → find the last word
    words = form.split()
    if not words:
        return None, None

    if len(words) == 1:
        # Single word — strip prefix, apply suffix to root, then reattach prefix
        prefix, root = _strip_prefix(form)
        if not root:
            return None, None
        nucleus = _last_nucleus(root)
    # Compound type = 'multi': even if form is stored with spaces, handle it
    # For multi-word compounds, suffix goes on the last word
    elif len(words) > 1:
        prefix, last_root = _strip_prefix(words[-1])
        nucleus = _last_nucleus(last_root)
    else:
        return None, None

    if not nucleus:
        return None, None

    # Determine suffix vowel class
    if nucleus in _FRONT_VOWELS:
        acc_suffix = "na"
        gen_suffix = "sa"
    elif nucleus in _BACK_VOWELS:
        acc_suffix = "ni"
        gen_suffix = "si"
    else:
        return None, None

    if len(words) == 1:
        acc = prefix + root + acc_suffix
        gen = prefix + root + gen_suffix
    else:
        # Multi-word: suffix on last word only
        prefix_last, root_last = _strip_prefix(words[-1])
        last_acc = prefix_last + root_last + acc_suffix
        last_gen = prefix_last + root_last + gen_suffix
        acc = " ".join(words[:-1] + [last_acc])
        gen = " ".join(words[:-1] + [last_gen])

    return acc, gen


# ── Ambiguity Detection ───────────────────────────────────────────────────────

def detect_syllable_ambiguities(db_path):
    """Scan the lexicon for syllable-boundary ambiguities at compound boundaries.

    Returns a list of dicts, each describing one ambiguous word:
        {
            "word_id": int,
            "form": str,
            "parser_syllables": str,      # e.g. "mai.ka"
            "parser_count": int,          # e.g. 2
            "issue": str,      # "diphthong_across_boundary" | "ae_across_boundary" | "vowel_hiatus"
            "components": str,            # e.g. "ma + ika"
            "boundary_pair": str,
            "note": str,
        }

    Only mono-compounds (compound_type='mono') are checked — these fuse
    multiple roots into a single word form, creating potential boundary
    collisions where diphthongs or 'ae' sequences span morpheme edges.
    """
    import sqlite3

    db = sqlite3.connect(db_path)
    cur = db.cursor()

    cur.execute("""
        SELECT DISTINCT w.id, w.form, w.syl_count
        FROM words w
        JOIN compound_components cc ON cc.compound_id = w.id
        WHERE w.is_compound = 1 AND w.compound_type = 'mono'
        ORDER BY w.form
    """)
    compounds = cur.fetchall()

    ambiguities = []

    for wid, form, syl_count in compounds:
        cur.execute("""
            SELECT r.form, cc.position
            FROM compound_components cc
            JOIN words r ON r.id = cc.component_id
            WHERE cc.compound_id = ?
            ORDER BY cc.position
        """, (wid,))
        components = cur.fetchall()
        if len(components) < 2:
            continue

        component_forms = [c[0] for c in components]
        reconstituted = "".join(component_forms)

        offset = 0
        for idx, comp_form in enumerate(component_forms[:-1]):
            next_form = component_forms[idx + 1]
            boundary_pos = offset + len(comp_form)

            if boundary_pos > 0 and boundary_pos < len(reconstituted):
                # Two-char sequence spanning boundary
                if boundary_pos + 1 <= len(reconstituted):
                    pair = reconstituted[boundary_pos - 1 : boundary_pos + 1]
                    if pair == "ae":
                        parser_syls = ".".join(split_syllables(form))
                        ambiguities.append({
                            "word_id": wid,
                            "form": form,
                            "parser_syllables": parser_syls,
                            "parser_count": syl_count,
                            "issue": "ae_across_boundary",
                            "components": " + ".join(component_forms),
                            "boundary_pair": pair,
                            "note": (
                                f"'ae' at boundary between '{comp_form}' and "
                                f"'{next_form}' — may be /æ/ (1 nucleus) "
                                "or a.e (2 nuclei)"
                            ),
                        })
                    elif pair in DIPHTHONGS:
                        parser_syls = ".".join(split_syllables(form))
                        ambiguities.append({
                            "word_id": wid,
                            "form": form,
                            "parser_syllables": parser_syls,
                            "parser_count": syl_count,
                            "issue": "diphthong_across_boundary",
                            "components": " + ".join(component_forms),
                            "boundary_pair": pair,
                            "note": (
                                f"diphthong '{pair}' at boundary between "
                                f"'{comp_form}' and '{next_form}' — may be "
                                "1 nucleus or 2 separate nuclei"
                            ),
                        })

                # Vowel hiatus (two adjacent vowels not forming ae or diphthong)
                last_char = reconstituted[boundary_pos - 1].lower()
                first_char = (
                    reconstituted[boundary_pos].lower()
                    if boundary_pos < len(reconstituted)
                    else ""
                )
                if last_char in VOWELS and first_char in VOWELS:
                    pair2 = last_char + first_char
                    if pair2 != "ae" and pair2 not in DIPHTHONGS:
                        parser_syls = ".".join(split_syllables(form))
                        ambiguities.append({
                            "word_id": wid,
                            "form": form,
                            "parser_syllables": parser_syls,
                            "parser_count": syl_count,
                            "issue": "vowel_hiatus",
                            "components": " + ".join(component_forms),
                            "boundary_pair": pair2,
                            "note": (
                                f"vowel hiatus '{pair2}' at boundary between "
                                f"'{comp_form}' and '{next_form}' — "
                                "always 2 separate syllables"
                            ),
                        })

            offset += len(comp_form)

    db.close()
    return ambiguities


# ── IPA Transcription ─────────────────────────────────────────────────────────

# Kilor → IPA mappings (SSOT: rules/0-foundation/phonology.md §II–IV)
_VOWEL_IPA = {
    "a": "a", "e": "e", "i": "i", "o": "ɔ", "u": "u", "y": "y", "ae": "æ",
}
_DIPHTHONG_IPA = {
    "ai": "aɪ", "au": "aʊ", "ei": "eɪ", "eu": "eʊ",
    "iu": "i̯u", "oi": "ɔɪ", "ou": "oʊ",
}
_CORE_IPA = {
    "p": "p", "b": "b", "m": "m", "f": "f", "w": "w",
    "t": "t", "d": "d", "n": "n", "s": "s", "l": "l",
    "r": "ɹ", "c": "ts", "k": "k", "g": "ɡ", "h": "h",
    "qy": "j",
}
_EDGE_IPA = {"sh": "ʃ", "ch": "tʃ", "th": "θ"}
_START_IPA = {
    "kl": "kˡ", "tl": "tˡ", "bl": "bˡ", "ml": "mˡ",
    "kr": "kɹ", "br": "bɹ", "gr": "ɡɹ", "fr": "fɹ", "pr": "pɹ",
    "sr": "sɹ",
}
_END_IPA = {"ng": "ŋ", "x": "x", "rk": "ɹk"}


def _syllable_to_ipa(syl, is_word_start=False, is_word_end=False):
    """Map a single Kilor syllable string to its IPA segments.
    
    Uses positional consonant class rules from phonology.md:
    - Start-only consonants only at word-initial (§IV-C)
    - End-only consonants only at word-final (§IV-D)
    - Edge-only consonants only at word edges (§IV-B)
    - Mid-word multi-char sequences are separate core consonants (§IV-E)
    """
    n = len(syl)
    i = 0
    segments = []

    # ── Onset ──
    if i < n and syl[i] not in VOWELS:
        if is_word_start:
            # Word-initial onset: check start-only, then edge-only, then core
            if i + 2 <= n and syl[i:i+2] in _START_IPA:
                segments.append(_START_IPA[syl[i:i+2]])
                i += 2
            elif i + 2 <= n and syl[i:i+2] in _EDGE_IPA:
                segments.append(_EDGE_IPA[syl[i:i+2]])
                i += 2
            elif i + 2 <= n and syl[i:i+2] in _CORE_IPA:
                segments.append(_CORE_IPA[syl[i:i+2]])
                i += 2
            elif syl[i] in _CORE_IPA:
                segments.append(_CORE_IPA[syl[i]])
                i += 1
        else:
            # Mid-word onset: only core consonants (single-char or multi-char)
            if i + 2 <= n and syl[i:i+2] in _CORE_IPA:
                segments.append(_CORE_IPA[syl[i:i+2]])
                i += 2
            elif syl[i] in _CORE_IPA:
                segments.append(_CORE_IPA[syl[i]])
                i += 1

    # ── Nucleus ──
    if i >= n:
        return segments
    if syl[i:i+2] == "ae":
        segments.append(_VOWEL_IPA["ae"])
        i += 2
    elif i + 1 < n and syl[i:i+2] in _DIPHTHONG_IPA:
        segments.append(_DIPHTHONG_IPA[syl[i:i+2]])
        i += 2
    elif syl[i] in _VOWEL_IPA:
        segments.append(_VOWEL_IPA[syl[i]])
        i += 1

    # ── Coda ──
    if i >= n:
        return segments
    if is_word_end:
        # Word-final coda: check end-only, then edge-only, then core (incl. multi-char)
        if i + 2 <= n and syl[i:i+2] in _END_IPA and i + 2 == n:
            segments.append(_END_IPA[syl[i:i+2]])
            i += 2
        elif i + 2 <= n and syl[i:i+2] in _EDGE_IPA and i + 2 == n:
            segments.append(_EDGE_IPA[syl[i:i+2]])
            i += 2
        elif i + 1 == n and syl[i] in _END_IPA:
            segments.append(_END_IPA[syl[i]])
            i += 1
        elif i + 2 <= n and syl[i:i+2] in _CORE_IPA:
            segments.append(_CORE_IPA[syl[i:i+2]])
            i += 2
        elif syl[i] in _CORE_IPA:
            segments.append(_CORE_IPA[syl[i]])
            i += 1
    else:
        # Mid-word coda: only core consonants (single-char or multi-char)
        if i + 2 <= n and syl[i:i+2] in _CORE_IPA:
            segments.append(_CORE_IPA[syl[i:i+2]])
            i += 2
        elif syl[i] in _CORE_IPA:
            segments.append(_CORE_IPA[syl[i]])
            i += 1

    return segments


def to_ipa(form):
    """Convert a Kilor written form to IPA transcription with syllable boundaries.
    
    Returns a string like "/ˈfɔ.rɑ.gi.lɑn/" with stress mark on the first syllable
    and syllable dots between syllables. Multi-word compounds return space-separated
    IPA blocks: "/ˈfɔs/ /ˈbˡɔn/".
    
    Uses positional consonant class rules from phonology.md §IV.
    Tone markers (j, v) are stripped — they are extra-segmental (§V-A).
    """
    # Multi-word compounds: process each word separately
    words = form.split()
    if len(words) > 1:
        ipa_blocks = []
        for word in words:
            block = to_ipa(word)
            if block:
                ipa_blocks.append(block)
        return " ".join(ipa_blocks) if ipa_blocks else ""

    syllables = split_syllables(form)
    if not syllables:
        return ""
    
    ipa_parts = []
    for idx, syl in enumerate(syllables):
        is_first = (idx == 0)
        is_last = (idx == len(syllables) - 1)
        segs = _syllable_to_ipa(syl, is_word_start=is_first, is_word_end=is_last)
        ipa_parts.append("".join(segs))
    
    return "/ˈ" + ".".join(ipa_parts) + "/"


# ── Tonal Inflection Computation (3+ syllable words) ─────────────────────────

def syllable_positions(word):
    """Split a word into syllable objects with vowel-end offsets.

    Like split_syllables() but returns each syllable as a dict with:
      onset, nucleus, coda, vowel_end: int (position in the cleaned word
      right after the nucleus vowel, where tone markers are inserted).

    Tone markers (j, v) and hyphens are stripped before parsing.
    Mirrors db.js:_syllablePositions().

    Returns:
        list of dicts, one per syllable.
    """
    import re as _re
    cleaned = _re.sub(r'[jv-]', '', word)
    n = len(cleaned)
    if n == 0:
        return []

    # Build mapping: cleaned[i] → index in the original (pre-strip) word
    cleaned_to_orig = []
    ci = 0
    for oi, ch in enumerate(word):
        if ch in ('j', 'v', '-'):
            continue
        if ci < n and cleaned[ci] == ch:
            cleaned_to_orig.append(oi)
            ci += 1

    syllables = []
    i = 0
    while i < n:
        onset = ''
        # Onset — multi-char core (e.g. qy) can be onset anywhere
        if i + 2 <= n and cleaned[i:i+2] in _MULTICHAR_CORE:
            onset = cleaned[i:i+2]
            i += 2
        elif i == 0 and i + 2 <= n and cleaned[i:i+2] in START_ONLYS:
            onset = cleaned[i:i+2]
            i += 2
        elif i == 0 and i + 2 <= n and cleaned[i:i+2] in EDGE_ONLYS:
            onset = cleaned[i:i+2]
            i += 2
        elif i < n and cleaned[i] in CORE_CONS:
            onset = cleaned[i]
            i += 1

        if i >= n:
            raise ValueError(f"incomplete syllable in '{cleaned}' at position {i}")

        nucleus_start = i
        if cleaned[i] in VOWELS:
            if cleaned[i:i+2] == 'ae':
                i += 2
            elif i + 1 < n and cleaned[i:i+2] in DIPHTHONGS:
                i += 2
            else:
                i += 1
        nucleus = cleaned[nucleus_start:i]

        coda = ''
        if i < n:
            # Multi-char core: can be coda at word-final
            if i + 2 <= n and cleaned[i:i+2] in _MULTICHAR_CORE and i + 2 == n:
                coda = cleaned[i:i+2]
                i += 2
            elif i + 2 <= n and cleaned[i:i+2] in END_ONLYS and i + 2 == n:
                coda = cleaned[i:i+2]
                i += 2
            elif i + 2 <= n and cleaned[i:i+2] in EDGE_ONLYS and i + 2 == n:
                coda = cleaned[i:i+2]
                i += 2
            elif i + 1 == n and cleaned[i] in END_ONLYS:
                coda = cleaned[i]
                i += 1
            elif cleaned[i] in CORE_CONS:
                if i + 1 >= n or cleaned[i + 1] not in VOWELS:
                    coda = cleaned[i]
                    i += 1

        # Vowel end position in the cleaned word (after the nucleus)
        vowel_end_cleaned = nucleus_start + len(nucleus)
        vowel_end_orig = cleaned_to_orig[vowel_end_cleaned - 1] + 1 if vowel_end_cleaned > 0 and (vowel_end_cleaned - 1) < len(cleaned_to_orig) else vowel_end_cleaned

        syllables.append({
            'onset': onset,
            'nucleus': nucleus,
            'coda': coda,
            'vowel_end_orig': vowel_end_orig,
        })

    return syllables


def compute_tonal_inflections(form, syl_count, pos_mask):
    """Compute tonal inflection forms for a Kilor word.

    Args:
        form: bare word form (e.g. 'walunla', 'foragilan')
        syl_count: integer syllable count
        pos_mask: NVAD mask string (e.g. 'NV', 'AD', 'NVAD')

    Returns:
        dict: {form_type: form} e.g. {'noun': 'walujnla', 'adverb': 'waluvnla'}
        For 1-2 syllable words, returns toneless forms (N/V=bare, A/D=+s).

    Rules (SSOT: tone-prosody.md §II-III):
        - 1-2 syl: toneless. N/V = bare root, A/D = root + 's'
        - 3+ syl: Last-3 Domain tone markers.
          N: j on 1st of last-3.  V: v on 1st of last-3.
          A: j on 2nd of last-3. D: v on 2nd of last-3.
        - Multi-word compounds: tone markers on last word only.
    """
    if not pos_mask:
        return {}

    mask = pos_mask.upper()
    mask_len = len(mask)
    result = {}
    mask_letters = ['N', 'V', 'A', 'D']
    is_toneless = syl_count <= 2

    words = form.split(' ')
    last_word_idx = len(words) - 1

    form_type_map = {'N': 'noun', 'V': 'verb', 'A': 'adjective', 'D': 'adverb'}

    for letter in mask_letters:
        if letter not in mask:
            continue

        ft = form_type_map[letter]

        if is_toneless:
            if letter in ('N', 'V'):
                if mask_len == 1:
                    result[ft] = [form, form]
                else:
                    result[ft] = form
            elif form.endswith('s'):
                # -es allomorph: roots ending in 's' take '-es' instead of '-s'
                # to avoid illegal geminate -ss. Only 4 grandfathered roots
                # (fos, gus, meus, rius) — new roots should not end in 's'.
                # See tone-prosody.md §II-B.
                inflected = form + 'es'
                if mask_len == 1:
                    result[ft] = [form, inflected]
                else:
                    result[ft] = inflected
            else:
                inflected = form + 's'
                if mask_len == 1:
                    result[ft] = [form, inflected]
                else:
                    result[ft] = inflected
        else:
            target_word = words[last_word_idx]
            syls = syllable_positions(target_word)

            if len(syls) < 3:
                result[ft] = form
                continue

            last3 = syls[-3:]
            anchor_idx = 0 if letter in ('N', 'V') else 1
            anchor = last3[anchor_idx]
            tone_char = 'j' if letter in ('N', 'A') else 'v'

            vowel_end = anchor['vowel_end_orig']
            toned_last = target_word[:vowel_end] + tone_char + target_word[vowel_end:]

            if len(words) == 1:
                result[ft] = toned_last
            else:
                result[ft] = ' '.join(words[:-1] + [toned_last])

    return result
