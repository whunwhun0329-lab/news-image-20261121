#!/usr/bin/env python3
"""Entry program for the make.fun bounty "news-image-20261121".

Copies the entry image (entry.png, stored beside this file) to the
output directory as entry.png. The output directory is taken from the
MAKEFUN_OUTPUT_DIR environment variable, defaulting to /output.
Standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        sys.exit(f"error: source image not found: {SOURCE}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(dest) != sha256_of(SOURCE):
        raise SystemExit(
            f"error: copied file failed integrity check: {dest} "
            f"does not match {SOURCE}"
        )


if __name__ == "__main__":
    main()
