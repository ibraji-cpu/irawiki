#!/usr/bin/env python3
"""Cek tautan MATI di HTML hasil build Quartz (gate yang benar).

Beda dengan tools/link_check.py: script ini membaca `href` dari file HTML di
`public/`, bukan dari sumber Markdown. Ini menangkap kelas bug yang tidak
terlihat link_check — wikilink berbasis judul yang di-resolve Quartz menjadi
slug judul (mis. [[Nama Judul]] -> /nama-judul) padahal halaman asli berada di
path lain -> 404.

Yang diperhitungkan sebagai VALID:
  - slug halaman canonical (public/<slug>.html)
  - halaman redirect alias (public/<alias>.html, berukuran <1200 byte)
  - folder arsip (aktor, analisis, kategori, peristiwa, tags)
  - placeholder editorial: _belum ada data_, tidak diketahui

Pemakaian:
    python3 tools/check_broken_links.py                 # seluruh wiki
    python3 tools/check_broken_links.py public/kategori # satu folder
    python3 tools/check_broken_links.py --json out.json
Keluar 1 bila ada tautan mati.
"""
from __future__ import annotations

import html as htmllib
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PUBLIC = REPO / "public"

ANCHOR = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.S)
FOLDERS = {p.name for p in PUBLIC.iterdir() if p.is_dir() and p.name != "static"}
PLACEHOLDER = {"", "404", "_belum ada data_", "tidak diketahui"} | FOLDERS


def collect_alias_pages() -> set[str]:
    """Halaman redirect alias: HTML kecil (<1.2 KB) berisi meta refresh."""
    found = set()
    for p in PUBLIC.rglob("*.html"):
        if p.stat().st_size < 1200 and "http-equiv" in p.read_text(encoding="utf-8", errors="replace"):
            found.add(p.relative_to(PUBLIC).with_suffix("").as_posix().lower())
    return found


def resolve(page_rel: str, href: str) -> str | None:
    """Kembalikan path tujuan (relatif terhadap root) atau None bila di luar wiki."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if href.endswith((".css", ".js", ".png", ".jpg", ".svg")):
        return None
    if href.startswith("/"):
        target = href.lstrip("/")
    else:
        target = urllib.parse.urljoin(page_rel, href)
    target = target.split("#")[0].strip("/")
    return target or None


def main() -> int:
    argv = sys.argv[1:]
    out_json = None
    if "--json" in argv:
        i = argv.index("--json")
        out_json = argv[i + 1]
        argv = argv[:i] + argv[i + 2 :]
    only = [a for a in argv if not a.startswith("--")][:1]

    canon = {p.relative_to(PUBLIC).with_suffix("").as_posix().lower() for p in PUBLIC.rglob("*.html")}
    aliases = collect_alias_pages()
    roots = [PUBLIC / only[0]] if only else [PUBLIC]

    broken: dict[str, set[str]] = {}
    checked = 0
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.html")):
            page_rel = p.relative_to(PUBLIC).as_posix()
            text = p.read_text(encoding="utf-8", errors="replace")
            if len(text) < 1200 and "http-equiv" in text:
                continue  # halaman alias, bukan konten
            checked += 1
            for href, _label in ANCHOR.findall(text):
                target = resolve(page_rel, href)
                if target is None:
                    continue
                low = target.lower()
                if low in PLACEHOLDER:
                    continue
                if low in canon or low in aliases:
                    continue
                broken.setdefault(page_rel, set()).add(htmllib.unescape(target))

    result = {
        "pages_checked": checked,
        "pages_with_broken_links": len(broken),
        "broken_total": sum(len(v) for v in broken.values()),
        "broken": {k: sorted(v) for k, v in sorted(broken.items())},
    }
    if out_json:
        Path(out_json).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"halaman diperiksa      : {checked}")
    print(f"halaman dengan mati    : {len(broken)}")
    print(f"total tautan mati      : {result['broken_total']}")
    for page, targets in sorted(broken.items()):
        print(f"  - {page}")
        for t in sorted(targets):
            print(f"      /{t}")
    return 0 if not broken else 1


if __name__ == "__main__":
    raise SystemExit(main())
