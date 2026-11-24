#!/usr/bin/env python3
"""THE WORLD TODAY - Monday 23 November 2026.

Copies the entry image (entry.png, 1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.
Standard library only: the PNG header is parsed by hand with struct.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    width, height = png_size(SRC)
    if (width, height) != (1024, 1024):
        raise ValueError(f"unexpected size {width}x{height}, want 1024x1024")
    shutil.copyfile(SRC, dst)
    if sha256(SRC) != sha256(dst):
        raise ValueError("copy sha256 mismatch")
    dw, dh = png_size(dst)
    if (dw, dh) != (1024, 1024):
        raise ValueError(f"output size {dw}x{dh}, want 1024x1024")
    size = os.path.getsize(dst)
    if size > 1048576:
        raise ValueError(f"entry.png too large: {size} bytes")
    print(f"OK entry.png {width}x{height} {size} bytes sha256={sha256(dst)[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
