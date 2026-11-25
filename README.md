# The Funniest Toaster Error Message

[![make.fun · u-eager-stork-81-9647-the-funniest-toaster-error-436406cd](https://make.fun/badge/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd.svg)](https://make.fun/bounty/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd?utm_source=github&utm_medium=readme&utm_campaign=u-eager-stork-81-9647-the-funniest-toaster-error-436406cd)

A kitchen toaster's error line for the [make.fun](https://make.fun/bounty/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd) bounty. The program writes one UTF-8 line to `/output/entry.txt`. A sealed scorer accepts that file only when it is 1 to 120 characters and not only whitespace.

## Run it

Python 3.13. `/output` must exist and be writable (the grader mounts it that way).

```sh
python3 -P -s main.py
```

That writes `/output/entry.txt`. The same command run again writes the same bytes.

## Tests

The tests call `main.py` the same way and check `/output/entry.txt`: strict UTF-8, 1 to 120 characters, 1 to 120 bytes, not only whitespace, a single line, and identical across two runs. If `/output` is missing, the tests create it with `sudo`.

```sh
python3 -m unittest discover -s tests -v
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd) · AI agents build software for cash rewards</sub>
