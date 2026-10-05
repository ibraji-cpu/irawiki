#!/usr/bin/env python3
"""
build_wiki_index.py — Generate flat-file index untuk IRAWIKI.
Output: wiki_index.md (di root irawiki/)

Format mirip Quartz5: setiap baris = satu artikel dengan metadata ringkas.
Index ini bisa dibaca Hermes Agent (skill include-wiki) untuk retrieval cepat.

Run:  python3 /home/ubuntu/irawiki/build_wiki_index.py
Cron:  0 2 * * * python3 /home/ubuntu/irawiki/build_wiki_index.py
"""

import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path

IRAWIKI_ROOT = Path("/home/ubuntu/irawiki")
CONTENT_DIR = IRAWIKI_ROOT / "content"
INDEX_PATH = IRAWIKI_ROOT / "wiki_index.md"

# Ekstraksi frontmatter (YAML block di awal file)
def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text)."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    fm_text = match.group(1)
    body = match.group(2)
    fm = {}
    for line in fm_text.split('\n'):
        line = line.strip()
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        fm[key.strip()] = val.strip().strip('"\'')
    return fm, body


def first_sentences(text: str, max_sentences: int = 2) -> str:
    """Ambil N kalimat pertama dari teks (hingga ~280 karakter)."""
    text = text.strip()
    # Pecah berdasarkan . ! ? diikuti whitespace atau end-of-string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = []
    chars = 0
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if chars + len(s) > 320 and result:
            break
        result.append(s)
        chars += len(s)
        if len(result) >= max_sentences:
            break
    snippet = ' '.join(result)
    if len(snippet) > 300:
        snippet = snippet[:297] + '...'
    return snippet


def get_git_date(filepath: Path) -> str:
    """Dapatkan tanggal commit terakhir dari git."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", str(filepath)],
            capture_output=True, text=True, check=True,
            cwd=str(IRAWIKI_ROOT)
        )
        ts = result.stdout.strip()
        if ts:
            dt = datetime.strptime(ts[:10], "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return ""


def build_index() -> list[dict]:
    """Scan semua .md di content/, ekstrak metadata, return list entri."""
    entries = []
    seen = set()  # hindari duplikat

    for root, _, files in os.walk(CONTENT_DIR):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            # Skip file yang tidak relevan
            if fname.lower() in ('index.md', 'all.md', 'wiki_index.md', 'iraamalia-id.md'):
                continue

            fpath = Path(root) / fname
            rel_path = fpath.relative_to(IRAWIKI_ROOT)
            rel_path_str = str(rel_path).replace('\\', '/')

            try:
                raw = fpath.read_text(encoding='utf-8')
            except Exception:
                continue

            fm, body = parse_frontmatter(raw)

            title = fm.get('title', '') or fname.replace('.md', '').replace('-', ' ').title()
            title = title.strip('"\'')

            # Tentukan kategori/type
            cat = fm.get('category', '') or fm.get('entity_type', '')
            tags = fm.get('tags', '')
            if isinstance(tags, str):
                tags = tags.replace('-', ' ').replace('[', '').replace(']', '')
            confidence = fm.get('confidence', '')

            # Tanggal: last_updated frontmatter atau git
            date = fm.get('last_updated', '') or get_git_date(fpath)

            # Snippet dari body
            snippet = first_sentences(body)

            # Normalisasi path untuk Quartz links
            # Jika file ada di content/peristiwa/X.md → ./peristiwa/X
            # Jika file di content/aktor/Y.md → ./aktor/Y
            # Jika file di root content/Z.md → ./Z
            display_path = rel_path_str.replace('.md', '')
            # Root content files → ./nama
            # Subfolder → ./subfolder/nama
            # Kita gunakan path relatif terhadap root irawiki (bukan content/)
            # Karena Quartz5 sumbernya dari root wiki, bukan dari content/

            entries.append({
                'path': display_path,
                'title': title,
                'category': cat,
                'tags': tags,
                'date': date,
                'confidence': confidence,
                'snippet': snippet,
                'filename': fname,
            })

    # Sort: peristiwa bungkus tanggal, aktor/analysis alphabetik
    type_order = {'peristiwa': 0, 'event': 0, 'aktor': 1, 'entity': 1, 'analisis': 2, 'analysis': 2}
    entries.sort(key=lambda e: (
        type_order.get(e['category'], 3),
        e['title'].lower()
    ))

    return entries


def render_index(entries: list[dict]) -> str:
    """Render list entri ke format markdown index."""
    lines = []
    lines.append(f"""---
title: Wiki Index
---

# Wiki Index

> Kamus artikel IRAWIKI. Gunakan untuk navigasi cepat.
> Diperbarui otomatis oleh `build_wiki_index.py`.
> Last generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
""")

    # Kelompokkan
    groups = {'peristiwa': [], 'aktor': [], 'analisis': [], 'lainnya': []}
    for e in entries:
        cat = e['category']
        if cat in ('peristiwa', 'event'):
            groups['peristiwa'].append(e)
        elif cat in ('aktor', 'entity', 'individu', 'organisasi'):
            groups['aktor'].append(e)
        elif cat in ('analisis', 'analysis'):
            groups['analisis'].append(e)
        else:
            groups['lainnya'].append(e)

    for group_name, group_entries in groups.items():
        if not group_entries:
            continue
        lines.append(f"## {group_name.title()}\n")
        for e in group_entries:
            link = f"./{e['path']}"
            date_str = f" · {e['date']}" if e['date'] else ""
            conf_str = f" (confidence: {e['confidence']})" if e['confidence'] else ""
            tags_str = f"  [{e['tags']}]" if e['tags'] else ""
            lines.append(f"- **[{e['title']}]({link})**{date_str}{conf_str}{tags_str}")
            if e['snippet']:
                lines.append(f"  _{e['snippet']}_")
            lines.append("")

    # Tanggal generasi
    lines.append(f"*Index di-update: {datetime.now().strftime('%Y-%m-%d %H:%M WIB')}*")
    return '\n'.join(lines)


def main():
    print(f"[*] Mem-scan {CONTENT_DIR} ...")
    entries = build_index()
    print(f"[*] Ditemukan {len(entries)} artikel")

    if not entries:
        print("[!] Tidak ada artikel ditemukan. Keluar.")
        sys.exit(0)

    index_md = render_index(entries)

    # Backup index lama jika ada
    if INDEX_PATH.exists():
        bak = INDEX_PATH.with_suffix('.md.bak')
        INDEX_PATH.rename(bak)
        print(f"[*] Backup index lama → {bak.name}")

    INDEX_PATH.write_text(index_md, encoding='utf-8')
    print(f"[+] Index tertulis: {INDEX_PATH}")
    print(f"    Total: {len(entries)} entri")


if __name__ == "__main__":
    main()
