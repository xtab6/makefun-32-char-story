#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes one Wi-Fi network name to /output/entry.txt (via MAKEFUN_OUTPUT_DIR).
Gate: UTF-8 text, 1 to 32 characters, not only whitespace.

The name: "My Wi-Fi is my emergency contact"
  A whole story in one line — a person whose closest contact, the one
  they'd list on a hospital form, is the router. The joke lands on the
  first read (an SSID as an emergency contact), it implies a character,
  a situation and a life behind it, and it is fresh against a field full
  of breakups and stolen routers.
"""

import os
import sys

ENTRY = "My Wi-Fi is my emergency contact"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

    # Clean only the output folder's contents, never the folder itself:
    # the grader mounts this folder, removing it fails with EPERM.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)

    text = ENTRY
    if not (1 <= len(text) <= 32):
        raise SystemExit("entry must be 1-32 characters, got %d" % len(text))
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")

    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    # Read back and verify byte-for-byte what the gate will see: exact
    # text, exact byte length, and no trailing newline sneaking in.
    with open(target, "rb") as fh:
        raw = fh.read()
    if raw.decode("utf-8") != text:
        raise SystemExit("read-back mismatch")
    if len(raw) != len(text.encode("utf-8")):
        raise SystemExit("byte-length mismatch: %d" % len(raw))
    if raw.endswith(b"\n"):
        raise SystemExit("trailing newline would count against the 32-char gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
