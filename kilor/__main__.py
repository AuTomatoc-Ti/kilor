"""CLI entry point for Kilor Lexicon Management Tool.

Usage: python -m kilor [command] [options]
"""

import os
import sys

from .commands.add import cmd_add
from .commands.check import cmd_check
from .commands.export import cmd_export
from .commands.migrate import cmd_migrate
from .commands.next import cmd_next
from .commands.status import cmd_status
from .commands.suggest import cmd_suggest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "migrate":
        cmd_migrate()

    elif cmd == "next":
        count = 20
        if "--count" in sys.argv:
            idx = sys.argv.index("--count")
            if idx + 1 < len(sys.argv):
                count = int(sys.argv[idx + 1])
        cmd_next(count)

    elif cmd == "add":
        filepath = None
        if "--file" in sys.argv:
            idx = sys.argv.index("--file")
            if idx + 1 < len(sys.argv):
                filepath = sys.argv[idx + 1]
        if not filepath:
            filepath = os.path.join(SCRIPT_DIR, "today.md")
        cmd_add(filepath)

    elif cmd == "check":
        cmd_check()

    elif cmd == "status":
        cmd_status()

    elif cmd == "export":
        fmt = "json"
        if "--format" in sys.argv:
            idx = sys.argv.index("--format")
            if idx + 1 < len(sys.argv):
                fmt = sys.argv[idx + 1]
        cmd_export(fmt)

    elif cmd == "serve":
        port = 8765
        if "--port" in sys.argv:
            idx = sys.argv.index("--port")
            if idx + 1 < len(sys.argv):
                port = int(sys.argv[idx + 1])
        import uvicorn
        print(f"Starting Kilor Dictionary API on http://localhost:{port}")
        print(f"Interactive docs at http://localhost:{port}/docs")
        uvicorn.run("kilor.api:app", host="127.0.0.1", port=port, log_level="info")

    elif cmd == "suggest":
        if len(sys.argv) < 3:
            print("Usage: python -m kilor suggest WORD")
            return
        cmd_suggest(sys.argv[2])

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()