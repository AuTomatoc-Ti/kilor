"""Phonotactics, syllable counting, and validation for Kilor words."""

VOWELS = set("aeiouy")
DIPHTHONGS = {"ai", "au", "ei", "eu", "iu", "oi", "ou"}
CORE_CONS = set("pbmfwtdnslrckgh")
START_ONLYS = {"sh", "ch", "th", "sl", "kl", "tl", "bl", "ml"}
END_ONLYS = {"ng", "x"}

S_FINAL_WHITELIST = {
    "gus", "fos", "aus", "ous", "les", "mangus",
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
    """Greedy left-to-right syllable parser."""
    n = len(word)
    if n == 0:
        return []

    syllables = []
    i = 0
    while i < n:
        onset = ""
        if i == 0 and i + 2 <= n and word[i : i + 2] in START_ONLYS:
            onset = word[i : i + 2]
            i += 2
        elif i < n and word[i] in CORE_CONS:
            onset = word[i]
            i += 1

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

        coda = ""
        if i < n:
            if i + 2 <= n and word[i : i + 2] in END_ONLYS:
                coda = word[i : i + 2]
                i += 2
            elif word[i] in CORE_CONS:
                coda = word[i]
                i += 1

        syllables.append(onset + nucleus + coda)

    return syllables


def validate_root(root):
    """Validate a bare root against phonotactics. Returns (is_valid, error_message)."""
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
    "ki":  ("kin",  "kis"),
    "ti":  ("tin",  "tis"),
    "si":  ("sin",  "sis"),
    "ni":  ("nin",  "nis"),
    "kil": ("kilin", "kilis"),
    "til": ("tilin", "tilis"),
    "sil": ("silin", "silis"),
    "nil": ("nilin", "nilis"),
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
