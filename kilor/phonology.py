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