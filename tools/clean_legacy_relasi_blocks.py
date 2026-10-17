#!/usr/bin/env python3
"""Bersihkan blok `relasi:` skema LAMA secara TEKSTUAL -> `relasi: []`.

Menangani dua bentuk:
  A. `relasi:` + item terindentasi 2 spasi   -> ganti jadi `relasi: []`
  B. `relasi: []` + item lepas indent 0      -> hapus item lepas (fix regresi)

Tidak memakai parser YAML (file frontmatter rusak tetap bisa dibersihkan).
Hanya menyentuh file yang masih punya jejak `objek_id`/`predikat`.
"""
import os
import re
import sys
from pathlib import Path

CONTENT_ROOT = Path("/home/ubuntu/irawiki/content")
SUBDIRS = ("aktor", "peristiwa", "analisis")

TOP_KEY_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*\s*:')


def atomic_write(path: Path, text: str):
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, text.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(str(tmp), str(path))


def is_item_or_continuation(line: str) -> bool:
    s = line.strip()
    if s == "":
        return True
    if line.startswith((" ", "\t")):
        return True
    if line.startswith("- "):
        return True
    return False


def clean(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^relasi\s*:\s*(\[\s*\]\s*)?$', line):
            out.append("relasi: []")
            i += 1
            # consume legacy item / continuation lines
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "---":
                    break
                if TOP_KEY_RE.match(nxt):
                    break
                if not is_item_or_continuation(nxt):
                    break
                # don't swallow blank line that precedes a top-level key
                if nxt.strip() == "":
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        j += 1
                    if j < len(lines) and (TOP_KEY_RE.match(lines[j]) or lines[j].strip() == "---"):
                        break
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def main():
    targets = []
    for sub in SUBDIRS:
        for md in sorted((CONTENT_ROOT / sub).glob("*.md")):
            t = md.read_text(encoding="utf-8")
            if "objek_id" in t or "predikat" in t:
                targets.append(md)

    print(f"file dengan jejak skema lama: {len(targets)}")
    for md in targets:
        t = md.read_text(encoding="utf-8")
        new = clean(t)
        if new != t:
            atomic_write(md, new)
            left = "objek_id" in new or "predikat" in new
            print(f"  cleaned {md.parent.name}/{md.name}  (sisa jejak: {left})")
        else:
            print(f"  unchanged {md.parent.name}/{md.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
