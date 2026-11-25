#!/usr/bin/env python3
"""Write this contest's toaster error line to /output/entry.txt."""

from pathlib import Path

# One appliance fault: clipped, specific, and done in a single read.
MESSAGE = "Slot 2: eye contact (raisin). Abort."
OUTPUT_PATH = Path("/output/entry.txt")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Exact text, UTF-8, no BOM and no trailing newline, so the file
    # length is the length of the one line.
    OUTPUT_PATH.write_bytes(MESSAGE.encode("utf-8"))


if __name__ == "__main__":
    main()
