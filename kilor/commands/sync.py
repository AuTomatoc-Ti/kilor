"""Sync the dictionary app's public database with the master database."""

import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def cmd_sync():
    """Copy data/kilor.db → kilor/dictionary/public/kilor.db so the app sees latest data."""
    src = os.path.join(SCRIPT_DIR, "data", "kilor.db")
    dst = os.path.join(SCRIPT_DIR, "kilor", "dictionary", "public", "kilor.db")

    if not os.path.exists(src):
        print("Error: data/kilor.db not found.")
        return

    # Resolve real paths — if dst is a symlink to src, they're already the same file
    src_real = os.path.realpath(src)
    if os.path.exists(dst):
        dst_real = os.path.realpath(dst)
        if src_real == dst_real:
            print("Already synced — public/kilor.db is a symlink to data/kilor.db.")
            return

    shutil.copy2(src, dst)
    print("Synced: data/kilor.db → kilor/dictionary/public/kilor.db")
