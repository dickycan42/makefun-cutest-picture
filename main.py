# cutest-picture-01 entry: places the kitten picture at the grader's output path.
#
# The program copies entry.png (the picture that lives next to this script)
# into the output directory and then checks that the copy is exactly the
# same bytes as the original, by comparing their SHA-256 digests. If the
# two digests do not match it reports the problem and exits non-zero.
#
# The output directory comes from MAKEFUN_OUTPUT_DIR; when that variable
# is unset it defaults to /output. Outside the grader's container you can
# try it with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
#
# Deterministic by design: it only copies bytes, no network, no randomness,
# no timestamps, so two runs always produce the same output.

import hashlib
import os
import shutil
import sys
from pathlib import Path


def digest(path):
    """SHA-256 hex digest of a file's bytes."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.png"

    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"

    shutil.copyfile(source, destination)

    if digest(source) != digest(destination):
        print("error: output does not match source", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
