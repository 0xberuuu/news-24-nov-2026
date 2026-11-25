#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 entry.

Copies the front-page image (entry.png, already in this repository) into
an output directory so the result can be reproduced from this snapshot.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=out python3 main.py

The output directory is taken from the MAKEFUN_OUTPUT_DIR environment
variable and defaults to "out" when unset. It is created if needed.
The file written is entry.png, byte-identical to the one in the repo.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)
    print(f"Wrote {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
