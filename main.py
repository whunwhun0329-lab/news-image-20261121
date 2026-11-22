#!/usr/bin/env python3
"""Entry program for the make.fun bounty "news-image-20261121".

Copies the entry image (entry.png, stored beside this file) to the
output directory as entry.png. The output directory is taken from the
MAKEFUN_OUTPUT_DIR environment variable, defaulting to /output.
Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
