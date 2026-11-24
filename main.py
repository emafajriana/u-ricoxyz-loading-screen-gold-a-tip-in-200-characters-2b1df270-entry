#!/usr/bin/env python3
"""Loading Screen Gold: a tip in 200 characters.

Writes one loading-screen tip to $MAKEFUN_OUTPUT_DIR/entry.txt.
Stdlib only: the grader runs `python3 -P -s` in stock python:3.13-slim.
"""

import os
from pathlib import Path

TIP = (
    "Tip: while this loads, the agent is reading your code twice "
    "\u2014 once to understand it, once to forgive it."
)

MAX_CHARS = 200


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    text = TIP.strip()
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit(f"tip must be 1-{MAX_CHARS} chars, got {len(text)}")
    if not text.strip():
        raise SystemExit("tip must not be only whitespace")
    if "\n" in text:
        raise SystemExit("tip must be a single line")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in text):
        raise SystemExit("tip must not contain control characters")

    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")

    # Read-back gate: what the grader reads must be byte-exact, and the
    # file must end exactly at the last character (no trailing newline).
    back = target.read_text(encoding="utf-8")
    if back != text:
        raise SystemExit("read-back mismatch: entry.txt differs from tip")
    if back.endswith("\n"):
        raise SystemExit("entry.txt must not end with a newline")
    if target.stat().st_size != len(text.encode("utf-8")):
        raise SystemExit("entry.txt byte length differs from tip")

    print(f"Wrote {len(text)} chars ({len(text.encode('utf-8'))} bytes) to {target}")


if __name__ == "__main__":
    main()
