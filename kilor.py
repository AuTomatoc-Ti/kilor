#!/usr/bin/env python3
"""
Kilor Lexicon Management Tool.

Usage:
  python kilor.py next [--count N]    Generate today's translation template
  python kilor.py add --file FILE     Process filled-in template, validate, add to lexicon
  python kilor.py check               Validate all entries in the database
  python kilor.py status              Print lexicon statistics
  python kilor.py suggest WORD        Suggest how a word should be handled (root/compound/derivation)
  python kilor.py migrate             Migrate data from lexicon.csv + compounds.json to SQLite
  python kilor.py export [--format FMT]  Export lexicon (csv, json, html, dictionary)
"""

from kilor.__main__ import main

if __name__ == '__main__':
    main()