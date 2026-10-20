#!/usr/bin/env python3
"""Cek tautan internal wiki: apakah setiap [[wikilink]] menunjuk halaman yang ada.

Resolusi mengikuti kebiasaan Quartz/Obsidian di repo ini:
- nama file (stem) di content/**, rekursif
- frontmatter `entity_id`
- frontmatter `title`
- frontmatter `aliases`
- path relatif terhadap content (mis. `aktor/andi-syamsuddin-arsyad`)

Pemakaian:
    python3 tools/link_check.py                # ringkasan seluruh wiki
    python3 tools/link_check.py --only a.md b.md  # hanya file tertentu (path repo)
    python3 tools/link_check.py --json out.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

WIKILINK = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|([^\]]*))?\]\]")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data: dict = {}
    key = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            data[key] = val
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and key:
            cur = data.get(key)
            if not isinstance(cur, list):
                cur = [] if cur in ("", None) else [cur]
            cur.append(m.group(1).strip())
            data[key] = cur
    return data


def unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def build_index() -> set[str]:
    names: set[str] = set()
    for p in CONTENT.rglob("*.md"):
        rel = p.relative_to(CONTENT).with_suffix("").as_posix()
        names.add(rel.lower())
        names.add(p.stem.lower())
        for suffix in ("/index", "/_index"):
            if rel.lower().endswith(suffix):
                names.add(rel[: -len(suffix)].lower())
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        for key in ("entity_id", "title"):
            v = fm.get(key)
            if isinstance(v, str) and unquote(v):
                names.add(unquote(v).lower())
        aliases = fm.get("aliases")
        if isinstance(aliases, list):
            for a in aliases:
                if unquote(a):
                    names.add(unquote(a).lower())
        elif isinstance(aliases, str) and unquote(aliases):
            names.add(unquote(aliases).lower())
    return names


def resolve(target: str, names: set[str]) -> bool:
    t = target.strip().lower()
    if t in names:
        return True
    # Quartz memakai slug: spasi -> "-"
    if t.replace(" ", "-") in names:
        return True
    if t.replace("-", " ") in names:
        return True
    return False


def check(files: list[Path], names: set[str]) -> dict:
    result = {"checked_files": 0, "links": 0, "broken": []}
    for p in files:
        text = p.read_text(encoding="utf-8")
        # buang frontmatter agar link di metadata tidak ikut dihitung
        body = text.split("\n---", 1)[1] if text.startswith("---") else text
        result["checked_files"] += 1
        for m in WIKILINK.finditer(body):
            target = m.group(1).strip()
            if not target or target.startswith("http"):
                continue
            result["links"] += 1
            if not resolve(target, names):
                rel = p.relative_to(ROOT).as_posix()
                result["broken"].append({"file": rel, "target": target})
    return result


def main() -> int:
    args = sys.argv[1:]
    names = build_index()
    if "--only" in args:
        i = args.index("--only")
        files = [ROOT / a for a in args[i + 1 :] if not a.startswith("--")]
    else:
        files = sorted(CONTENT.rglob("*.md"))
    res = check(files, names)
    if "--json" in args:
        out = args[args.index("--json") + 1]
        Path(out).write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(f"file diperiksa : {res['checked_files']}")
    print(f"wikilink total : {res['links']}")
    print(f"wikilink rusak : {len(res['broken'])}")
    for b in res["broken"][:40]:
        print(f"  - {b['file']} -> [[{b['target']}]]")
    return 0 if not res["broken"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
