"""Generate audio pronunciation files for all words in the lexicon.

Uses espeak-ng (required: brew install espeak-ng) to synthesize each word's
IPA transcription, then converts to Ogg Opus via ffmpeg for small file sizes.
Files are saved to kilor/dictionary/public/audio/ and served as static assets
by the Vite dev server.

Usage:
    python kilor.py audio --generate       # generate audio for all words
    python kilor.py audio --generate --id 42  # generate audio for a single word
    python kilor.py audio --check           # report missing audio files
"""

import os
import sqlite3
import subprocess
import tempfile

from ..phonology import to_ipa

_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "kilor.db")
_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "dictionary", "public", "audio")


def _clean_for_espeak(ipa_str):
    """Strip IPA formatting that espeak-ng can't handle.

    espeak-ng --ipa mode accepts raw IPA but not delimiters, stress marks,
    tone markers, or Unicode tie bars.
    """
    s = ipa_str.replace("/", "").replace("\u02c8", "").replace(".", "")
    s = s.replace("\u02e5", "").replace("\u02e9", "")  # tone markers
    s = s.replace("\u035c", "").replace("\u0361", "")   # coarticulation ties
    return s


def _generate_one(word_id, form, output_path):
    """Generate a single Ogg Opus audio file for a word form.

    Pipeline: espeak-ng --ipa → temp WAV → ffmpeg → Opus-in-ogg.
    Returns True on success.
    """
    words = form.split()
    raw_parts = [_clean_for_espeak(to_ipa(w)) for w in words]
    raw_ipa = " ".join(raw_parts)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Step 1: espeak-ng → temp WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = tmp.name

    espeak_cmd = ["espeak-ng", "--ipa", "-v", "en", raw_ipa, "-w", tmp_wav]
    result = subprocess.run(espeak_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        os.unlink(tmp_wav)
        print(f"  FAIL word_id={word_id} form='{form}': espeak error")
        return False

    # Step 2: ffmpeg WAV → Ogg Opus
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", tmp_wav,
        "-c:a", "libopus", "-b:a", "24k",
        "-application", "voip",
        output_path,
    ]
    ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

    # Clean up temp WAV
    os.unlink(tmp_wav)

    if ffmpeg_result.returncode != 0:
        print(f"  FAIL word_id={word_id} form='{form}': ffmpeg: {ffmpeg_result.stderr.strip()[:120]}")
        return False
    return True


def cmd_audio(action=None, word_id=None):
    """Handle the 'audio' CLI command."""
    if action is None:
        print("Usage: python kilor.py audio --generate [--id WORD_ID]")
        print("       python kilor.py audio --check")
        return

    if action == "check":
        _cmd_check()
    elif action == "generate":
        _cmd_generate(word_id)
    else:
        print(f"Unknown audio action: {action}")


def _cmd_check():
    """Report which words are missing audio files."""
    db = sqlite3.connect(_DB_PATH)
    rows = db.execute("SELECT id, form FROM words ORDER BY id").fetchall()
    db.close()

    missing = 0
    present = 0
    for wid, form in rows:
        out_path = os.path.join(_AUDIO_DIR, f"{wid}.ogg")
        if os.path.exists(out_path):
            present += 1
        else:
            missing += 1
            print(f"  Missing: {wid:>5}  {form}")

    print(f"\nAudio status: {present} present, {missing} missing ({len(rows)} total)")


def _cmd_generate(word_id=None):
    """Generate .ogg Opus audio files for all words (or a single word)."""
    if not os.path.isfile(_DB_PATH):
        print(f"Database not found: {_DB_PATH}")
        return

    db = sqlite3.connect(_DB_PATH)
    if word_id is not None:
        rows = db.execute("SELECT id, form FROM words WHERE id = ?", (word_id,)).fetchall()
    else:
        rows = db.execute("SELECT id, form FROM words ORDER BY id").fetchall()
    db.close()

    if not rows:
        print("No words found.")
        return

    os.makedirs(_AUDIO_DIR, exist_ok=True)
    success = 0
    fail = 0

    for wid, form in rows:
        out_path = os.path.join(_AUDIO_DIR, f"{wid}.ogg")
        if _generate_one(wid, form, out_path):
            success += 1
        else:
            fail += 1

    print(f"\nAudio generation complete: {success} generated, {fail} failed ({len(rows)} total)")
    print(f"Output directory: {_AUDIO_DIR}")