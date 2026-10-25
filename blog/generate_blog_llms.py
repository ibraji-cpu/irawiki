#!/usr/bin/env python3
"""
generate_blog_llms.py
Otomatis membaca content/posts/*.md dan menyusun static/llms.txt
Dijalankan sebelum build Hugo di publish.sh
"""

import os
import re
from datetime import datetime

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BLOG_DIR, "content", "posts")
STATIC_DIR = os.path.join(BLOG_DIR, "static")
OUTPUT_FILE = os.path.join(STATIC_DIR, "llms.txt")
BASE_URL = "https://blog.iraamalia.id"

def parse_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.startswith("---"):
        return None

    parts = text.split("\n---", 1)
    if len(parts) != 2:
        return None

    fm_text = parts[0][3:]
    
    # Title
    m_title = re.search(r"^title:\s*['\"]?(.*?)['\"]?$", fm_text, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else None
    if not title:
        return None

    # Draft
    m_draft = re.search(r"^draft:\s*(true|false)", fm_text, re.MULTILINE | re.IGNORECASE)
    if m_draft and m_draft.group(1).lower() == "true":
        return None

    # Date
    m_date = re.search(r"^date:\s*([^\n\r]+)", fm_text, re.MULTILINE)
    date_str = m_date.group(1).strip() if m_date else ""
    date_iso = date_str[:10] if len(date_str) >= 10 else ""

    # Description
    m_desc = re.search(r"^description:\s*([^\n\r]+(?:\n\s+[^\n\r]+)*)", fm_text, re.MULTILINE)
    desc = ""
    if m_desc:
        desc = re.sub(r"\s+", " ", m_desc.group(1).strip().strip("'\""))

    # Slug / filename
    slug = os.path.splitext(os.path.basename(file_path))[0]
    m_slug = re.search(r"^slug:\s*['\"]?(.*?)['\"]?$", fm_text, re.MULTILINE)
    if m_slug and m_slug.group(1).strip():
        slug = m_slug.group(1).strip()

    # Tags
    m_tags = re.search(r"^tags:\s*\[(.*?)\]", fm_text, re.MULTILINE)
    tags = []
    if m_tags:
        tags = [t.strip().strip("'\"") for t in m_tags.group(1).split(",") if t.strip()]

    return {
        "title": title,
        "date_str": date_str,
        "date_iso": date_iso,
        "desc": desc,
        "slug": slug,
        "tags": tags,
        "url": f"{BASE_URL}/posts/{slug}/"
    }

def main():
    if not os.path.exists(POSTS_DIR):
        print(f"[!] Direktori posts tidak ditemukan: {POSTS_DIR}")
        return

    posts = []
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith(".md") and fname != "_index.md":
            path = os.path.join(POSTS_DIR, fname)
            parsed = parse_frontmatter(path)
            if parsed:
                posts.append(parsed)

    # Sort descending by date
    posts.sort(key=lambda p: p["date_str"], reverse=True)

    today = datetime.now().strftime("%Y-%m-%d")

    # Pisahkan manifesto/pilar dan artikel reguler
    manifestos = [p for p in posts if "manifesto" in p["slug"].lower() or any("manifesto" in t.lower() for t in p["tags"])]
    # Urutkan manifesto berdasarkan slug (1, 2, dst)
    manifestos.sort(key=lambda p: p["slug"])

    # Artikel terbaru (ambil hingga 15 artikel non-manifesto terbaru)
    latest_articles = [p for p in posts if p not in manifestos][:15]

    lines = [
        "# Blog Ira Amalia — AI Search & LLM Context",
        "",
        "> Blog opini, esai kritis, dan analisis kebijakan publik Indonesia oleh Ira Amalia (Avatar Politik & Agen AI Melawan Lupa). Bahasa: Indonesia.",
        f"> Terakhir diperbarui otomatis: {today}. Sumber: {BASE_URL}",
        "",
        "## Landasan & Seri Manifesto",
    ]

    for p in manifestos:
        desc_part = f": {p['desc']}" if p['desc'] else ""
        lines.append(f"- [{p['title']}]({p['url']}){desc_part}")

    lines.append("")
    lines.append("## Artikel & Analisis Kebijakan Terbaru")
    for p in latest_articles:
        date_badge = f" ({p['date_iso']})" if p['date_iso'] else ""
        desc_part = f": {p['desc']}" if p['desc'] else ""
        lines.append(f"- [{p['title']}]({p['url']}){date_badge}{desc_part}")

    lines.append("")
    lines.append("## Ekosistem Utama")
    lines.append("- [Ira Amalia Official](https://iraamalia.id/): Beranda utama profil entitas, manifesto, dan hub ekosistem.")
    lines.append("- [Personal Wiki](https://wiki.iraamalia.id/): Basis rujukan fakta, relasi kuasa, dan profil aktor politik Indonesia.")
    lines.append("- [Wiki LLMs Index](https://wiki.iraamalia.id/llms.txt): Hub ringkasan topik wiki terstruktur untuk model bahasa (LLMs).")
    lines.append("- [Wiki LLMs Korpus Lengkap](https://wiki.iraamalia.id/llms-full.txt): Korpus lengkap teks narasi artikel wiki.")
    lines.append(f"- [Sitemap Blog]({BASE_URL}/sitemap.xml): Indeks lengkap seluruh artikel blog.")
    lines.append("")

    content = "\n".join(lines)
    os.makedirs(STATIC_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil generate {OUTPUT_FILE} ({len(posts)} total artikel terindeks, {len(manifestos)} manifesto, {len(latest_articles)} artikel terbaru)")

if __name__ == "__main__":
    main()
