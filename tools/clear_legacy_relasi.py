#!/usr/bin/env python3
"""Kosongkan `relasi` skema LAMA (objek_id/predikat/subjek_id) menjadi `relasi: []`.

Skema lama tidak memenuhi kontrak baru (predikat di luar vocabulary, sumber null).
Relasi lama TIDAK diinventarisasi ulang — dikosongkan, diisi penulis ke depan.

Backup: salinan file asli + dump JSON disimpan sebelum diubah.
"""
import json
import os
import re
import sys
import datetime
from pathlib import Path

CONTENT_ROOT = Path("/home/ubuntu/irawiki/content")
BACKUP_DIR = Path("/home/ubuntu/irawiki_legacy_relasi_backup")
SUBDIRS = ("aktor", "peristiwa", "analisis")

try:
    import yaml
except ImportError:
    yaml = None


def atomic_write(path: Path, text: str):
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, text.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(str(tmp), str(path))


def replace_relasi_block(fm: str) -> str:
    """Replace a multi-line `relasi:` block with `relasi: []`.

    Keeps the key position; drops all indented continuation lines.
    """
    lines = fm.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^relasi\s*:\s*$', line):
            out.append("relasi: []")
            i += 1
            # skip indented continuation lines
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or lines[i].strip() == ""):
                if lines[i].strip() == "" and i + 1 < len(lines) and not lines[i + 1].startswith((" ", "\t")):
                    break
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dump = []
    changed = 0
    skipped_new = 0

    for sub in SUBDIRS:
        base = CONTENT_ROOT / sub
        if not base.exists():
            continue
        for md in sorted(base.glob("*.md")):
            text = md.read_text(encoding="utf-8")
            m = re.search(r'^---\s*$', text[3:], re.MULTILINE)
            if not m:
                continue
            fm = text[3:3 + m.start()]
            body = text[3 + m.start():]

            # parse relasi value
            if yaml is None:
                continue
            try:
                d = yaml.safe_load(fm) or {}
            except Exception:
                continue
            rel = d.get("relasi", None)
            if not rel:
                continue
            keys = set()
            for item in rel:
                if isinstance(item, dict):
                    keys |= set(item.keys())
            if "tipe" in keys or "target" in keys:
                skipped_new += 1
                continue  # already new schema, leave alone

            # backup original file + record legacy data
            rel_path = f"{sub}/{md.name}"
            dst = BACKUP_DIR / rel_path.replace("/", "__")
            dst.write_text(text, encoding="utf-8")
            dump.append({"file": rel_path, "legacy_relasi": rel})

            new_fm = replace_relasi_block(fm)
            atomic_write(md, "---" + new_fm + body)
            changed += 1

    (BACKUP_DIR / f"legacy-relasi-{stamp}.json").write_text(
        json.dumps(dump, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== CLEAR LEGACY RELASI ===")
    print(f"files changed to relasi: [] : {changed}")
    print(f"left alone (new schema)     : {skipped_new}")
    print(f"backup dir                  : {BACKUP_DIR}")
    print(f"legacy data dump            : {BACKUP_DIR}/legacy-relasi-{stamp}.json ({len(dump)} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
