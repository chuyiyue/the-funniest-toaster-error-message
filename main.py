"""Write one toaster error message for the make.fun bounty.

The grader runs this file as ``python3 -P -s /bot/main.py`` and reads
``/output/entry.txt``. The message is a fixed string, so two runs match.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Deadpan fault line: one code, one fact, no second sentence to explain it.
MESSAGE = "E7: Only the raisin was toasted."

MIN_CHARS = 1
MAX_CHARS = 120


def validate(message: str) -> None:
    """Refuse a message the sealed gate would not judge."""
    if not isinstance(message, str):
        raise SystemExit("entry must be text")
    if message != message.strip():
        raise SystemExit("entry has leading or trailing whitespace")
    if any(ch in message for ch in "\n\r"):
        raise SystemExit("entry must be a single line")
    if message.strip() == "":
        raise SystemExit("entry is only whitespace")
    # Count code points. The line is ASCII, so this matches UTF-8 bytes too.
    length = len(message)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise SystemExit(f"entry is {length} characters; need {MIN_CHARS} to {MAX_CHARS}")
    try:
        raw = message.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise SystemExit(f"entry is not UTF-8: {exc}") from exc
    if len(raw) < MIN_CHARS or len(raw) > MAX_CHARS:
        raise SystemExit(f"entry is {len(raw)} bytes; need {MIN_CHARS} to {MAX_CHARS}")


def output_path() -> Path:
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(directory) / "entry.txt"


def main() -> None:
    validate(MESSAGE)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(MESSAGE.encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        print(f"could not write {output_path()}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
