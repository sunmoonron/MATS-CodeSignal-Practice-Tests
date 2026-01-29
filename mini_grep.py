from __future__ import annotations
import argparse
import re
import sys
from typing import TextIO

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="minigrep")
    p.add_argument("pattern")
    p.add_argument("file")
    p.add_argument("--ignore-case", action="store_true")
    p.add_argument("--regex", action="store_true", help="Treat pattern as regex")
    p.add_argument("--count", action="store_true")
    p.add_argument("--line-numbers", action="store_true")
    return p

def run(pattern: str, file: str, *, ignore_case: bool, regex: bool, count: bool, line_numbers: bool,
        stdout: TextIO, stderr: TextIO) -> int:
    """
    Behavior:
      - Read file as UTF-8 text (errors='replace')
      - If regex=False: match if pattern is a substring
      - If regex=True: match if re.search succeeds
      - ignore_case applies to both modes
      - If count=True: print just the number of matching lines and newline
      - Else: print each matching line; if line_numbers=True prefix 'N:' (1-based)
      - Exit code: 0 if at least one match else 1
    """
    raise NotImplementedError

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return run(
        args.pattern,
        args.file,
        ignore_case=args.ignore_case,
        regex=args.regex,
        count=args.count,
        line_numbers=args.line_numbers,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

if __name__ == "__main__":
    raise SystemExit(main())
