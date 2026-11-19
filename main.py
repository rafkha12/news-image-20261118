#!/usr/bin/env python3
"""news-image-20261118 entry: copy the image beside this file to
/output/entry.png (MAKEFUN_OUTPUT_DIR stands in for /output outside the
grader's container). A pure copy, so both runs write identical bytes.
Python 3.13, standard library only, no network."""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "image.png", OUT / "entry.png")
print(f"wrote {OUT / 'entry.png'}")
