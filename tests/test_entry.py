"""Local checks for the toaster entry gate.

The sealed scorer accepts /output/entry.txt only when it is UTF-8 text of
1 to 120 characters and not only whitespace. These tests run the program the
way the grader does and check that file.
"""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = Path("/output/entry.txt")
MIN_CHARS = 1
MAX_CHARS = 120


def ensure_output_dir() -> None:
    """Make /output writable. The grader mounts it; locally it may be missing."""
    if ENTRY.parent.is_dir() and os.access(ENTRY.parent, os.W_OK):
        return
    subprocess.run(["sudo", "-n", "mkdir", "-p", str(ENTRY.parent)], check=True)
    subprocess.run(
        ["sudo", "-n", "chown", f"{os.getuid()}:{os.getgid()}", str(ENTRY.parent)],
        check=True,
    )


def run_program() -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["MAKEFUN_OUTPUT_DIR"] = "/output"
    env["MAKEFUN_BOT_DIR"] = str(ROOT)
    env["TZ"] = "UTC"
    env["PYTHONHASHSEED"] = "0"
    env["LANG"] = "C.UTF-8"
    # -P -s matches the grader: no script directory on sys.path, no user site.
    return subprocess.run(
        ["python3", "-P", "-s", str(ROOT / "main.py")],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
    )


class EntryTests(unittest.TestCase):
    def setUp(self) -> None:
        ensure_output_dir()
        if ENTRY.exists():
            ENTRY.unlink()

    def test_writes_valid_utf8_line(self) -> None:
        first = run_program()
        self.assertEqual(first.returncode, 0, first.stderr.decode("utf-8", "replace"))
        self.assertTrue(ENTRY.is_file(), "/output/entry.txt was not written")

        raw = ENTRY.read_bytes()
        text = raw.decode("utf-8")  # strict: invalid UTF-8 raises
        self.assertEqual(text.encode("utf-8"), raw)
        self.assertGreaterEqual(len(text), MIN_CHARS)
        self.assertLessEqual(len(text), MAX_CHARS)
        self.assertGreaterEqual(len(raw), MIN_CHARS)
        self.assertLessEqual(len(raw), MAX_CHARS)
        self.assertNotEqual(text.strip(), "")
        self.assertEqual(text, text.strip())
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

        second = run_program()
        self.assertEqual(second.returncode, 0, second.stderr.decode("utf-8", "replace"))
        self.assertEqual(ENTRY.read_bytes(), raw, "two runs wrote different bytes")


if __name__ == "__main__":
    unittest.main()
