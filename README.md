# The Funniest Toaster Error Message

A make.fun contest entry. `main.py` writes one toaster error line to `/output/entry.txt`.

The line is a single clipped fault, the way a small appliance display talks: specific, short, and finished in one read.

```
Slot 2: eye contact (raisin). Abort.
```

## Run

Requires Python 3.13 (the entrypoint also runs on any recent Python 3). No packages, network, or environment variables.

```bash
python3 main.py
```

The program creates `/output` if it is missing and overwrites `/output/entry.txt`. The file is UTF-8 with no BOM and no trailing newline. That exact text is the whole entry.

## Test

From this directory:

```bash
python3 -m unittest discover -s tests -v
```

The tests run `main.py` and check that `/output/entry.txt` is valid UTF-8 text of 1 to 120 characters and not only whitespace.
