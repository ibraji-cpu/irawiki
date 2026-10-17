#!/usr/bin/env python3
"""Backfill MEKANIS: tambah `last_verified` + `relasi: []` ke frontmatter halaman lama.

Aturan (mekanis, TIDAK menginventarisasi relasi):
  - last_verified = tanggal entri terakhir di section "Perkembangan Terakhir"
    (fallback: mtime file), format YYYY-MM-DD.
  - relasi = [] (kosong; diisi penulis ke depan).

Tidak menyentuh field lain. Idempoten: file yang sudah punya kedua field dilewati.
"""
import os
import re
import sys
import datetime
from pathlib import Path

CONTENT_ROOT = Path("/home/ubuntu/irawiki/content")
SUBDIRS = ("aktor", "peristiwa", "analisis")
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')


def split_frontmatter(text):
    """Return (fm_text, body) or (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    m = re.search(r'^---\s*$', text[3:], re.MULTILINE)
    if not m:
        return None, text
    end = 3 + m.start()
    return text[3:end], text[end + 3:]  # fm_text, body (after closing ---)


def last_development_date(body):
    """Latest YYYY-MM-DD inside the 'Perkembangan Terakhir' section, or None."""
    m = re.search(r'^##\s+Perkembangan Terakhir\s*$', body, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r'^##\s+', body[start:], re.MULTILINE)
    section = body[start:start + nxt.start()] if nxt else body[start:]
    dates = DATE_RE.findall(section)
    valid = []
    for d in dates:
        try:
            valid.append(datetime.date.fromisoformat(d))
        except ValueError:
            pass
    return max(valid).isoformat() if valid else None


def atomic_write(path: Path, text: str):
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, text.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(str(tmp), str(path))


def main():
    stats = {"scanned": 0, "updated": 0, "skipped_have_both": 0,
             "no_frontmatter": 0, "from_perkembangan": 0, "from_mtime": 0}
    details = []

    for sub in SUBDIRS:
        base = CONTENT_ROOT / sub
        if not base.exists():
            continue
        for md in sorted(base.glob("*.md")):
            stats["scanned"] += 1
            text = md.read_text(encoding="utf-8")
            fm, body = split_frontmatter(text)
            if fm is None:
                stats["no_frontmatter"] += 1
                continue

            has_lv = re.search(r'^last_verified\s*:', fm, re.MULTILINE) is not None
            has_rel = re.search(r'^relasi\s*:', fm, re.MULTILINE) is not None
            if has_lv and has_rel:
                stats["skipped_have_both"] += 1
                continue

            # last_verified: Perkembangan Terakhir -> fallback mtime
            lv = last_development_date(body)
            if lv:
                stats["from_perkembangan"] += 1
            else:
                lv = datetime.date.fromtimestamp(md.stat().st_mtime).isoformat()
                stats["from_mtime"] += 1

            # sisipkan sebelum penutup frontmatter
            add = ""
            if not has_lv:
                add += f'last_verified: "{lv}"\n'
            if not has_rel:
                add += "relasi: []\n"
            new_fm = fm.rstrip("\n") + "\n" + add
            new_text = "---" + new_fm + "---" + body

            atomic_write(md, new_text)
            stats["updated"] += 1
            details.append((sub, md.stem, lv, "perkembangan" if last_development_date(body) else "mtime"))

    print("=== BACKFILL REPORT ===")
    for k, v in stats.items():
        print(f"{k}: {v}")
    print("\nContoh 5 halaman:")
    for d in details[:5]:
        print(f"  {d[0]}/{d[1]} -> last_verified={d[2]} ({d[3]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
