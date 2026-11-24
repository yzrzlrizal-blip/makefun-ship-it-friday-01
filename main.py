#!/usr/bin/env python3
"""Ship It Friday — make.fun bounty u-mgwals-ship-it-friday-30bd407a.

Writes a single line (at most 159 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output): the funniest one-line
git commit message an AI coding agent writes right before breaking
production on a Friday.

Pure standard library; deterministic — the same bytes on every run.
"""

import os
import sys

# The entry: a cheerful agent ships to prod on a Friday afternoon,
# perfectly confident. The joke lands on a single read: the tests never
# ran anywhere but inside the agent's own head, and production is
# reframed as staging that happens to have real users in it — the
# confident, unaware voice of an agent about to break everything.
LINE = "feat: ship it Friday, tests pass in my head and prod is just staging with real users"

MAX_CHARS = 159


def main() -> int:
    line = LINE
    if not line or not line.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"entry is {len(line)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    if line != line.strip():
        print("entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Re-read and verify the bytes we wrote, and that the file decodes
    # as clean single-line UTF-8 with no trailing newline (the gate
    # counts every byte, so nothing extra may sneak in).
    with open(path, "rb") as f:
        raw = f.read()
    if raw != data:
        print("verification failed: entry.txt differs", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if text.endswith("\n") or text != text.strip():
        print("verification failed: entry has trailing whitespace",
              file=sys.stderr)
        return 1
    print(f"wrote {len(data)} bytes ({len(line)} chars) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
