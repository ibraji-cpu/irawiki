#!/usr/bin/env python3
"""SEO artifacts for wiki.iraamalia.id — runs after every Quartz build.

1. copies seo/robots.txt and seo/llms.txt to public/ (web root)
2. regenerates public/llms-full.txt from content/*.md

llms-full.txt layout:
  header -> root hub pages -> /peristiwa/* -> /analisis/* (full markdown)
  -> /aktor/* as grouped link list (no full text)
"""
import os
import re
import sys
from datetime import date

REPO = "/home/ubuntu/irawiki"
CONTENT = os.path.join(REPO, "content")
PUBLIC = os.path.join(REPO, "public")
SEO = os.path.join(REPO, "seo")
BASE = "https://wiki.iraamalia.id"
SKIP = {"index.md", "iraamalia-id.md"}


def split_fm(text):
    if not text.startswith("---"):
        return "", text
    parts = text.split("\n---", 1)
    if len(parts) != 2:
        return "", text
    body = parts[1]
    if body.startswith("\n"):
        body = body[1:]
    return parts[0][3:], body


def fm_value(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v or None


def strip_meta(body):
    """Drop property/relationship blocks that are not narrative."""
    out, skip = [], False
    for ln in body.split("\n"):
        if re.match(r"^##\s+(Relasi|Sumber)\b", ln, re.I):
            skip = True
            continue
        if skip and re.match(r"^##\s+", ln):
            skip = False
        if not skip:
            out.append(ln)
    return "\n".join(out).strip()


def collect():
    title_by_slug = {}
    pages = []
    for dirpath, _, files in os.walk(CONTENT):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, CONTENT)
            slug = rel[:-3]
            text = open(path, encoding="utf-8").read()
            fm, body = split_fm(text)
            title = fm_value(fm, "title") or f[:-3]
            title_by_slug[slug] = title
            title_by_slug[slug.split("/")[-1]] = title
            pages.append({
                "slug": slug,
                "title": title,
                "fm": fm,
                "body": body,
                "dir": "root" if "/" not in rel else rel.split("/")[0],
                "fname": f,
            })
    return pages, title_by_slug


def unlink(md, title_by_slug):
    def rep(m):
        inner = m.group(1)
        if "|" in inner:
            return inner.split("|", 1)[1]
        return title_by_slug.get(inner.strip(), inner.strip().replace("-", " "))
    md = re.sub(r"\[\[([^\]]+)\]\]", rep, md)
    return md


def updated_of(page):
    return fm_value(page["fm"], "updated") or fm_value(page["fm"], "date") or ""


def render(page, title_by_slug):
    body = strip_meta(page["body"])
    body = unlink(body, title_by_slug)
    # drop duplicated leading H1 (the page title is printed by the file header)
    lines = body.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^#{1,2}\s+", lines[0]):
        heading = re.sub(r"^#{1,2}\s+", "", lines[0]).strip()
        if heading.lower().strip(":") == page["title"].lower().strip(":"):
            lines.pop(0)
    body = "\n".join(lines).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    head = [f"# {page['title']}", ""]
    head.append(f"URL: {BASE}/{page['slug']}")
    upd = updated_of(page)
    if upd:
        head.append(f"Diperbarui: {upd[:10]}")
    head.append("")
    return "\n".join(head) + "\n" + body + "\n"


def main():
    pages, title_by_slug = collect()
    published = [p for p in pages if p["fname"] not in SKIP]

    roots = sorted([p for p in published if p["dir"] == "root"], key=lambda p: p["slug"])
    event = sorted([p for p in published if p["dir"] == "peristiwa"], key=lambda p: p["slug"])
    analysis = sorted([p for p in published if p["dir"] == "analisis"], key=lambda p: p["slug"])
    actors = sorted([p for p in published if p["dir"] == "aktor"], key=lambda p: p["title"].lower())

    out = []
    out.append("# Personal Wiki Ira Amalia — korpus lengkap")
    out.append("")
    out.append(f"> Dibuat otomatis: {date.today().isoformat()}. Sumber: {BASE}")
    out.append("> Wiki politik Indonesia: aktor, relasi kuasa, kronologi kebijakan.")
    out.append("> Teks halaman /aktor/* disediakan sebagai daftar tautan, bukan teks penuh.")
    out.append("")
    out.append(f"Isi: {len(roots)} hub, {len(event)} peristiwa, {len(analysis)} analisis, "
               f"{len(actors)} aktor.")
    out.append("")

    sections = [
        ("Hub", roots),
        ("Peristiwa", event),
        ("Analisis", analysis),
    ]
    for name, group in sections:
        out.append(f"\n---\n\n# Bagian: {name}\n")
        for p in group:
            out.append(render(p, title_by_slug))
            out.append("\n")

    out.append("\n---\n\n# Bagian: Aktor (daftar tautan)\n")
    groups = {}
    for p in actors:
        key = p["title"][:1].upper()
        if not key.isalpha():
            key = "#"
        groups.setdefault(key, []).append(p)
    for key in sorted(groups):
        out.append(f"## {key}")
        for p in groups[key]:
            out.append(f"- [{p['title']}]({BASE}/{p['slug']})")
        out.append("")

    os.makedirs(PUBLIC, exist_ok=True)
    target = os.path.join(PUBLIC, "llms-full.txt")
    text = "\n".join(out).rstrip() + "\n"
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(text)

    for name in ("robots.txt", "llms.txt"):
        src = os.path.join(SEO, name)
        if os.path.exists(src):
            with open(src, encoding="utf-8") as fh:
                data = fh.read()
            with open(os.path.join(PUBLIC, name), "w", encoding="utf-8") as fh:
                fh.write(data)
        else:
            print(f"[!] missing {src}", file=sys.stderr)

    print(f"[seo] llms-full.txt {len(text)/1024:.0f} KB "
          f"({len(roots)} hub / {len(event)} peristiwa / {len(analysis)} analisis / {len(actors)} aktor)")


if __name__ == "__main__":
    main()
