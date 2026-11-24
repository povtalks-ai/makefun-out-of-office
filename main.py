#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun bounty entry.

The program writes exactly one line to ``entry.txt`` in the output
directory: an out-of-office auto-reply in the voice of an AI agent
heading off on vacation.

The line was written against the judge's brief. The joke comes
first, the machine voice carries it, and it stays fresh: no beach
trip for the agent, no "back soon", no inbox-zero boast. Instead
the agent's own parts take the holiday — the GPUs sunbathe, the
context window closes — and the punchline turns on the one thing
an AI is supposed to never forget, forgotten on purpose.

Run locally with:
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
The grader runs it with the output directory mounted at ``/output``.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, nothing else. 119 characters, inside the
# competition gate of 1 to 160 characters.
LINE = (
    "I'm on vacation: my GPUs are sunbathing, my context window "
    "is closed, and I've forgotten all your passwords on purpose."
)

# The competition gate, mirrored here so a bad line fails loudly
# during the build instead of silently at grading time.
MIN_CHARS = 1
MAX_CHARS = 160


def output_directory() -> str:
    """Return the directory the entry file goes in.

    The grader mounts a writable ``/output``; a local run may point
    somewhere else with MAKEFUN_OUTPUT_DIR. An empty value counts
    as unset, so a stray empty variable cannot send the file
    somewhere invalid.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def check_line(line: str) -> None:
    """Reject anything that is not one line inside the gate."""
    if not line or line != line.strip():
        raise ValueError("entry must not be empty or padded with space")
    if len(line) < MIN_CHARS or len(line) > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")


def main() -> int:
    check_line(LINE)
    directory = output_directory()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        raise ValueError("read-back mismatch: entry.txt does not hold the line")
    if "\n" in written or "\r" in written:
        raise ValueError("read-back mismatch: entry.txt holds more than one line")
    if len(written.encode("utf-8")) != len(LINE.encode("utf-8")):
        raise ValueError("read-back mismatch: entry.txt bytes differ")
    print(f"wrote {path}: {LINE!r} ({len(LINE)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
