# cutest-picture-01 entry: copies the art (entry.png) to the grader's output path,
# then verifies the copy is byte-for-byte identical to the source.
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    if _sha256(src) != _sha256(dst):
        print("copy mismatch: output differs from source", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
