#!/usr/bin/env python3
"""
wiki_update_notify.py — jembatan wiki -> blog.

Dijalankan setelah build Quartz (build_wiki.sh). Mendeteksi halaman wiki yang
baru ditambah (A) atau diedit (M) sejak deploy terakhir, membuat ringkasan
1-2 paragraf, lalu menyimpannya ke blog/data/wiki_updates.json agar dibaca
shortcode Hugo `wiki_updates`.

State: .wiki-last-sha (gitignored) — tahan rebuild manual / cron / CI.
Kalau file state belum ada, script hanya mencatat HEAD (tidak membanjiri blog
dengan ratusan halaman lama).

Exit code selalu 0 kecuali error fatal; pemanggil tetap pakai || true.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/ubuntu/irawiki")
CONTENT = REPO / "content"
PUBLIC = REPO / "public"
STATE = REPO / ".wiki-last-sha"
DATA = REPO / "blog/data/wiki_updates.json"

WIKI_BASE = "https://wiki.iraamalia.id"
HOME_ITEMS = 3
MAX_ITEMS = 60
MAX_PAGES_PER_BUILD = 8
BODY_CHARS = 2200

ENV_FILE = Path("/home/ubuntu/.hermes/.env")
LLM_CHAIN = [
    ("https://api.trustisgold.web.id/v1", "TRUSTISGOLD_API_KEY", "tig/deepseek-v4.1-flash"),
    ("https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
]


def log(msg: str) -> None:
    print(f"[notify] {msg}", flush=True)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.+)$", line)
        if m:
            val = m.group(2).strip().strip('"').strip("'")
            meta[m.group(1)] = val
    return meta, body


def first_paragraphs(body: str, limit: int = 2) -> str:
    """Fallback ekstraktif: paragraf naratif dulu, lalu poin-poin, lalu deskripsi."""
    out: list[str] = []
    chunk: list[str] = []
    bullets: list[str] = []
    in_code = False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith(("-", "*")) and not s.startswith("**"):
            bullets.append(s.lstrip("-* ").strip())
            continue
        if not s:
            if chunk:
                out.append(" ".join(chunk))
                chunk = []
                if len(out) >= limit:
                    break
            continue
        if s.startswith(("#", "|", ">", "!", "[")) or re.match(r"^\d+\.", s):
            if chunk:
                out.append(" ".join(chunk))
                chunk = []
                if len(out) >= limit:
                    break
            continue
        chunk.append(s)
    if chunk and len(out) < limit:
        out.append(" ".join(chunk))
    text = "\n\n".join(out)
    if not text:
        cand = [b for b in bullets if len(b) >= 40 and "belum ada data" not in b.lower()]
        text = "; ".join(cand[:2])
    text = re.sub(r"\[\[([^\]|]+)\|?([^\]]*)\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:900]


def llm_summary(title: str, desc: str, body: str, badge: str) -> str | None:
    prompt = (
        "Kamu editor wiki politik Indonesia. Tulis notifikasi 1-2 paragraf "
        f"(maks 90 kata) untuk pembaca blog tentang halaman wiki yang {badge}.\n"
        "Aturan: bahasa Indonesia, lugas, tanpa bullet, tanpa markdown, tanpa "
        "sapaan, tanpa 'dalam update kali ini'. Sebut nama tokoh/entitas dan "
        "substansi barunya. Jangan mengarang di luar bahan.\n\n"
        f"Judul: {title}\nDeskripsi: {desc}\nIsi:\n{body[:BODY_CHARS]}"
    )
    payload = json.dumps(
        {
            "model": None,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 400,
        }
    )
    for base, key_env, model in LLM_CHAIN:
        key = os.environ.get(key_env)
        if not key:
            continue
        try:
            body_obj = json.loads(payload)
            body_obj["model"] = model
            req = urllib.request.Request(
                f"{base}/chat/completions",
                data=json.dumps(body_obj).encode(),
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = json.load(resp)
            txt = (data["choices"][0]["message"].get("content") or "").strip()
            txt = re.sub(r"\s+", " ", re.sub(r"[*_`#>]", "", txt)).strip()
            if len(txt) >= 80:
                log(f"ringkasan via {model}")
                return txt[:1200]
        except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
            log(f"LLM {model} gagal: {exc}")
    return None


def build_item(path: Path, status: str) -> dict | None:
    rel = path.relative_to(CONTENT).as_posix()
    slug = rel[:-3] if rel.endswith(".md") else rel
    if Path(slug).name.lower() in {"index", "_index"}:
        return None
    if not (PUBLIC / f"{slug}.html").exists():
        log(f"lewati (belum ada di public/): {rel}")
        return None
    meta, body = split_frontmatter(path.read_text(errors="ignore"))
    title = meta.get("title") or Path(slug).name.replace("-", " ").title()
    desc = meta.get("description", "")
    badge = "baru" if status == "A" else "diperbarui"
    summary = llm_summary(title, desc, body, badge)
    if not summary:
        summary = first_paragraphs(body)
    if not summary and desc:
        summary = desc
    if not summary or len(summary) < 60:
        log(f"lewati (ringkasan terlalu pendek): {rel}")
        return None
    return {
        "title": title,
        "url": f"{WIKI_BASE}/{slug}",
        "badge": badge,
        "summary": summary,
        "source": rel,
        "date": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }


def main() -> int:
    load_env()
    head = git("rev-parse", "HEAD").strip()
    prev = STATE.read_text().strip() if STATE.exists() else ""

    if not prev:
        STATE.write_text(head + "\n")
        log(f"init state -> {head[:8]} (tanpa notifikasi)")
        return 0
    if prev == head:
        log("tidak ada commit baru, dilewati")
        return 0

    try:
        diff = git("diff", "--name-status", prev, head, "--", "content/")
    except subprocess.CalledProcessError as exc:
        log(f"git diff gagal ({exc}); state disegarkan")
        STATE.write_text(head + "\n")
        return 0

    targets: list[tuple[Path, str]] = []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, rel = parts[0][:1], parts[-1]
        if status not in {"A", "M"} or not rel.endswith(".md"):
            continue
        if rel.startswith("content/"):
            rel = rel[len("content/") :]
        targets.append((CONTENT / rel, status))
    log(f"kandidat: {len(targets)} halaman ({prev[:8]}..{head[:8]})")

    if not targets:
        STATE.write_text(head + "\n")
        log("tidak ada halaman .md berubah")
        return 0

    items = []
    for path, status in targets[:MAX_PAGES_PER_BUILD]:
        if not path.exists():
            continue
        item = build_item(path, status)
        if item:
            items.append(item)

    if not items:
        STATE.write_text(head + "\n")
        log("tidak ada item valid")
        return 0

    existing = {"items": []}
    if DATA.exists():
        try:
            existing = json.loads(DATA.read_text())
        except json.JSONDecodeError:
            log("data lama korup, ditulis ulang")
    old = existing.get("items", [])
    seen = {(i.get("url"), i.get("date", "")[:10]) for i in items}
    merged = items + [i for i in old if (i.get("url"), i.get("date", "")[:10]) not in seen]
    merged = merged[:MAX_ITEMS]

    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(
        json.dumps(
            {
                "generated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "commit": head[:12],
                "home_items": HOME_ITEMS,
                "items": merged,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    STATE.write_text(head + "\n")
    log(f"{len(items)} item ditulis -> {DATA} (total {len(merged)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
