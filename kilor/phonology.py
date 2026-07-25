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
START_ONLYS = {"sl", "kl", "tl", "bl", "ml", "kr", "br", "gr", "fr", "pr"}
END_ONLYS = {"ng", "x", "rk"}

# All multi-character single-letter sequences (for mid-word disambiguation)
_ALL_MULTICHAR = EDGE_ONLYS | START_ONLYS | END_ONLYS

S_FINAL_WHITELIST = {
    "gus", "fos", "aus", "ous", "les", "mangus",
    "rius", "meus",
    "kas", "hus", "tus", "rakas", "fidak",
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
        if i == 0 and i + 2 <= n and word[i : i + 2] in START_ONLYS:
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
        #   - it is a core consonant at word end (no following vowel), OR
        #   - it is a core consonant followed by another consonant
        coda = ""
        if i < n:
            # End-only letters (multi-char): only at absolute word-final position
            if i + 2 <= n and word[i : i + 2] in END_ONLYS and i + 2 == n:
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
        return False, f"root '{root}' has {syl_count} syllables (max 5)"
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