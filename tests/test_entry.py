"""Verify main.py writes a scorable toaster line to /output/entry.txt."""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.py"
OUTPUT = Path("/output/entry.txt")


class EntryOutputTest(unittest.TestCase):
    def test_program_writes_valid_entry(self) -> None:
        if OUTPUT.exists():
            OUTPUT.unlink()

        result = subprocess.run(
            ["python3", str(MAIN)],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )

        self.assertEqual(
            result.returncode,
            0,
            result.stderr.decode("utf-8", errors="replace"),
        )
        self.assertTrue(OUTPUT.is_file(), "/output/entry.txt was not written")

        raw = OUTPUT.read_bytes()
        text = raw.decode("utf-8")
        self.assertFalse(text.startswith("\ufeff"), "file should be UTF-8 without a BOM")

        # One optional trailing newline still counts as a single line.
        payload = text[:-1] if text.endswith("\n") else text
        self.assertNotIn("\n", payload)
        self.assertNotIn("\r", payload)

        stripped = payload.strip()
        self.assertGreaterEqual(len(stripped), 1)
        self.assertLessEqual(len(stripped), 120)
        self.assertTrue(stripped)
        self.assertLessEqual(len(text), 120)
        self.assertGreaterEqual(len(text.strip()), 1)
        self.assertLessEqual(len(text.strip()), 120)

    def test_program_is_idempotent(self) -> None:
        subprocess.run(["python3", str(MAIN)], cwd=ROOT, check=True)
        first = OUTPUT.read_bytes()
        subprocess.run(["python3", str(MAIN)], cwd=ROOT, check=True)
        second = OUTPUT.read_bytes()
        self.assertEqual(first, second)
        second.decode("utf-8")


if __name__ == "__main__":
    unittest.main()
