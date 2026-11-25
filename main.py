#!/usr/bin/env python3
"""Write this contest's toaster error line to /output/entry.txt."""

import sys
from pathlib import Path

# One appliance fault: clipped, specific, and done in a single read.
MESSAGE = "Slot 2: eye contact (raisin). Abort."
OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 120
# Line breaks the sealed scorer would not treat as a single line.
_LINE_BREAKS = ("\n", "\r", "\u2028", "\u2029")


def validate_message(message: str) -> None:
    """Refuse text that would fail the sealed scorer.

    The written file must be UTF-8, a single line, 1 to 120 characters,
    and not only whitespace. Raises ValueError when a check fails.
    """
    if not isinstance(message, str):
        raise ValueError("message must be text")

    if any(mark in message for mark in _LINE_BREAKS):
        raise ValueError("message must be a single line")

    if not 1 <= len(message) <= MAX_CHARS:
        raise ValueError("message must be 1 to 120 characters")

    if message.strip() == "":
        raise ValueError("message must not be only whitespace")

    try:
        message.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("message must be valid UTF-8") from exc


def write_entry(message: str, path: Path = OUTPUT_PATH) -> None:
    """Validate, then write the line. Writes nothing if validation fails."""
    validate_message(message)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(message.encode("utf-8"))


def main() -> None:
    try:
        write_entry(MESSAGE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
