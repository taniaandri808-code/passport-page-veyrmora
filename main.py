#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

src = Path(__file__).parent / "entry.png"
dst_dir = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "./output"))
dst_dir.mkdir(parents=True, exist_ok=True)
dst = dst_dir / "entry.png"

shutil.copy2(src, dst)
print(dst)
