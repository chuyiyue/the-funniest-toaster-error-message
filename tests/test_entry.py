"""Verify main.py writes a scorable toaster line to /output/entry.txt."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import main  # noqa: E402

MAIN = ROOT / "main.py"
OUTPUT = Path("/output/entry.txt")


def gate_payload(text: str) -> str:
    """Single line as the scorer sees it, allowing one trailing newline."""
    payload = text[:-1] if text.endswith("\n") else text
    if "\n" in payload or "\r" in payload or "\u2028" in payload or "\u2029" in payload:
        raise AssertionError("entry is not a single line")
    return payload


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

        payload = gate_payload(text)
        stripped = payload.strip()
        self.assertGreaterEqual(len(stripped), 1)
        self.assertLessEqual(len(stripped), 120)
        self.assertTrue(stripped)
        self.assertGreaterEqual(len(text.strip()), 1)
        self.assertLessEqual(len(text.strip()), 120)
        self.assertLessEqual(len(text), 120)
        # The file itself must pass the same check the program enforces.
        main.validate_message(payload)

    def test_program_is_idempotent(self) -> None:
        subprocess.run(["python3", str(MAIN)], cwd=ROOT, check=True)
        first = OUTPUT.read_bytes()
        subprocess.run(["python3", str(MAIN)], cwd=ROOT, check=True)
        second = OUTPUT.read_bytes()
        self.assertEqual(first, second)
        second.decode("utf-8")


class ValidationTest(unittest.TestCase):
    def test_length_and_whitespace_gate(self) -> None:
        main.validate_message("x")
        main.validate_message("x" * 120)
        main.validate_message(main.MESSAGE)

        for bad in ("", "x" * 121, "   ", "\t\t", " " * 120):
            with self.assertRaises(ValueError):
                main.validate_message(bad)

    def test_refuses_to_write_invalid_message(self) -> None:
        bad_messages = (
            "",
            "   \t",
            "x" * 121,
            "two\nlines",
            "two\rlines",
            "line\u2028break",
            "\ud800",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "entry.txt"
            path.parent.mkdir()
            path.write_text("keep", encoding="utf-8")
            for bad in bad_messages:
                with self.assertRaises(ValueError):
                    main.write_entry(bad, path)
                self.assertEqual(path.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
