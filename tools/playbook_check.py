#!/usr/bin/env python3
"""Validasi struktur "halaman rujukan" sesuai docs/playbook-halaman-rujukan.md.

Yang diperiksa (hanya struktur, bukan selera):
- ketujuh heading wajib ada dan berurutan
- "Kenapa penting buat Gen Z" berisi 3-6 kalimat
- "Fakta kunci" berisi 4-6 butir, tiap butir memuat angka/tanggal/nomor
- "Catatan presisi" ada dan tidak kosong
- bagian wajib tidak berada di bawah "## Sumber"

Pemakaian:
    python3 tools/playbook_check.py content/peristiwa/foo.md
    python3 tools/playbook_check.py --all content/...   # banyak berkas
Kode keluar 1 jika ada kegagalan (FAIL); peringatan (WARN) tidak memblokir.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SECTIONS = [
    "Ringkasan",
    "Kenapa penting buat Gen Z",
    "Fakta kunci",
    "Kronologi",
    "Aktor yang Terlibat",
    "Sumber",
    "Catatan presisi",
]

# bagian wajib yang boleh punya variasi judul
ALIASES = {
    "Aktor yang Terlibat": ("aktor yang terlibat", "aktor"),
    "Ringkasan": ("ringkasan", "ringkasan topik", "ringkasan polemik", "ringkasan soeharto pahlawan nasional"),
}

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)
SENTENCE_END = re.compile(r"[.!?](?=\s|$)")


def split_sections(text: str) -> tuple[str, dict[str, str], list[tuple[int, str]]]:
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            body = text[end + 4 :]
    heads = [(len(m.group(1)), m.group(2)) for m in HEADING.finditer(body)]
    sections: dict[str, str] = {}
    order: list[tuple[int, str]] = []
    matches = list(HEADING.finditer(body))
    for i, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        stop = len(body)
        for follow in matches[i + 1 :]:
            if len(follow.group(1)) <= level:
                stop = follow.start()
                break
        if level == 2:
            order.append((i, title))
            sections[title.lower()] = body[start:stop].strip()
    return body, sections, order


def find_section(sections: dict[str, str], want: str) -> str | None:
    keys = ALIASES.get(want, (want.lower(),))
    for k in keys:
        if k in sections:
            return sections[k]
    # longgar: heading yang diawali nama bagian
    for k, v in sections.items():
        if k.startswith(want.lower()):
            return v
    return None


def count_sentences(block: str) -> int:
    text = re.sub(r"```.*?```", " ", block, flags=re.S)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    text = re.sub(r"\[\[([^\]\|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return 0
    return len(SENTENCE_END.findall(text + " "))


def bullets(block: str) -> list[str]:
    return [ln.strip() for ln in block.splitlines() if re.match(r"^\s*[-*]\s+\S", ln)]


def has_hard_fact(bullet: str) -> bool:
    return bool(
        re.search(r"\d", bullet)
        or re.search(r"\(|\[", bullet)
        or re.search(r"Nomor|No\.", bullet, re.I)
    )


def check_file(path: Path) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []
    text = path.read_text(encoding="utf-8")
    body, sections, order = split_sections(text)

    if not re.search(r"^#\s+\S", body, re.M):
        fails.append("H1 judul tidak ada")

    titles = [t.lower() for _, t in order]
    idx = {}
    for want in SECTIONS:
        block = find_section(sections, want)
        if block is None:
            fails.append(f"bagian wajib hilang: ## {want}")
            continue
        # posisi untuk cek urutan
        for i, (_, t) in enumerate(order):
            if t.lower() == want.lower() or t.lower().startswith(want.lower()) or t.lower() in ALIASES.get(want, ()):
                idx[want] = i
                break
        if not block.strip():
            fails.append(f"bagian kosong: ## {want}")

    for prev, nxt in zip(SECTIONS, SECTIONS[1:]):
        if prev in idx and nxt in idx and idx[prev] > idx[nxt]:
            fails.append(f"urutan salah: ## {prev} muncul setelah ## {nxt}")

    if "Sumber" in idx and "Catatan presisi" in idx and idx["Catatan presisi"] < idx["Sumber"]:
        fails.append("## Catatan presisi harus berada setelah ## Sumber")

    genz = find_section(sections, "Kenapa penting buat Gen Z")
    if genz:
        n = count_sentences(genz)
        if n < 3:
            fails.append(f"Gen Z: {n} kalimat (minimal 3)")
        elif n > 6:
            fails.append(f"Gen Z: {n} kalimat (maksimal 6)")
        for bad in ("guys", "gaes", "literally", "kamu ", "!", "😀", "🔥"):
            if bad in genz.lower():
                fails.append(f"Gen Z: memuat larangan '{bad.strip()}'")

    fakta = find_section(sections, "Fakta kunci")
    if fakta:
        b = bullets(fakta)
        if len(b) < 4:
            fails.append(f"Fakta kunci: {len(b)} butir (minimal 4)")
        elif len(b) > 6:
            fails.append(f"Fakta kunci: {len(b)} butir (maksimal 6)")
        soft = [x for x in b if not has_hard_fact(x)]
        if soft:
            warns.append(f"Fakta kunci: {len(soft)} butir tanpa angka/tanggal")

    catatan = find_section(sections, "Catatan presisi")
    if catatan is not None and len(catatan) < 80:
        warns.append("Catatan presisi sangat pendek (<80 karakter)")

    kron = find_section(sections, "Kronologi")
    if kron:
        entries = re.findall(r"^###\s+\S", kron, re.M)
        if len(entries) < 2:
            warns.append(f"Kronologi: {len(entries)} entri")

    return fails, warns


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    total_fail = 0
    for a in args:
        p = Path(a)
        if not p.is_absolute():
            p = ROOT / p
        fails, warns = check_file(p)
        status = "OK  " if not fails else "FAIL"
        print(f"[{status}] {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")
        for f in fails:
            print(f"        ✗ {f}")
        for w in warns:
            print(f"        ! {w}")
        total_fail += 1 if fails else 0
    print(f"\n{len(args) - total_fail}/{len(args)} halaman lolos struktur.")
    return 1 if total_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
