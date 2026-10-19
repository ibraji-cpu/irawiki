"""Konverter mekanis retrofit: bullet kronologi -> entri ###, pemindah bagian."""
import re
from pathlib import Path

ROOT = Path("/home/ubuntu/irawiki")


def rd(p):
    q = Path(p) if Path(p).is_absolute() else ROOT / p
    return q, q.read_text(encoding="utf-8")


def wr(q, t):
    q.write_text(t, encoding="utf-8")


def section_bounds(t, name):
    """Kembalikan (start, end) blok '## name' sampai heading ## berikutnya."""
    m = re.search(r"^## " + re.escape(name) + r"\s*$", t, re.M)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r"^## ", t[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(t)
    return start, end


def extract(t, name):
    b = section_bounds(t, name)
    if not b:
        return None, t
    s, e = b
    return t[s:e], t[:s] + t[e:]


def chrono_from_bullets(block, body_name="## Kronologi"):
    """Ubah '- **YYYY-MM-DD** — teks' menjadi '### YYYY-MM-DD — Judul' + paragraf."""
    out = [body_name, ""]
    for ln in block.splitlines():
        m = re.match(r"^\s*[-*]\s+\*\*(\d{4}-\d{2}(?:-\d{2})?)[^*]*\*\*\s*[—:-]\s*(.+)$", ln)
        if m:
            date, rest = m.group(1), m.group(2).strip()
            if len(date) == 7:  # YYYY-MM
                date = date + "-01"
            title = re.split(r"(?<=[a-z])\.\s| — |; ", rest)[0]
            if len(title) > 78:
                title = title[:75].rsplit(" ", 1)[0] + "..."
            title = title.rstrip(".")
            out += [f"### {date} — {title}", rest, ""]
            continue
        if re.match(r"^\s*[-*]\s+\*\*\d{4}", ln):
            # format '- **2026-10-06 (pagi)** — ...'
            m2 = re.match(r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*[—:-]\s*(.+)$", ln)
            if m2:
                head, rest = m2.group(1), m2.group(2).strip()
                dm = re.match(r"(\d{4}-\d{2}-\d{2})", head)
                tag = head[dm.end():].strip() if dm else ""
                title = re.split(r"(?<=[a-z])\.\s| — |; ", rest)[0][:75].rstrip(".")
                out += [f"### {dm.group(1)} — {title}{(' ' + tag) if tag else ''}", rest, ""]
                continue
        out.append(ln)
    return "\n".join(out).rstrip() + "\n"


def to_entries(t, name="Kronologi"):
    block, t2 = extract(t, name)
    if block is None:
        return t
    return t2
