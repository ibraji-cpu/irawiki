#!/usr/bin/env python3
"""
Irawiki SQLite Indexer — Fase 2b

Mengubah repo Markdown (source of truth, READ-ONLY) menjadi wiki_index.db:
FTS5 full-text + tabel pages/entities/relations/aliases/sources.

Prinsip:
  - Indexer TIDAK PERNAH menulis ke Markdown. Output hanya file SQLite.
  - Idempotent: re-run tanpa perubahan -> 0 file diproses, DB tidak berubah.
  - Incremental via content_hash (sha256); --full untuk rebuild penuh.

Pemakaian:
  python3 tools/irawiki_indexer.py            # incremental
  python3 tools/irawiki_indexer.py --full     # rebuild penuh
  python3 tools/irawiki_indexer.py --db /path/to/wiki_index.db
"""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML wajib: pip install pyyaml\n")
    raise

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTENT = REPO_ROOT / "content"
DEFAULT_DB = REPO_ROOT / "wiki_index.db"
SCHEMA = Path(__file__).resolve().parent / "init_schema.sql"

SCHEMA_VERSION = "1"

# Section yang isinya relasi, bukan narasi -> tidak dimasukkan ke FTS body
RELATION_SECTIONS = re.compile(
    r"^(Afiliasi\s*&\s*Relasi|Afiliasi Bisnis|Relasi Terkait|Relasi yang Terdokumentasi"
    r"|Aktor yang Terlibat|Sumber)$",
    re.I,
)
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
TOPIC_EVENT_HEADING = re.compile(
    r"^###\s+(\d{4}-\d{2}-\d{2})\s+[\u2014\u2013\-]\s+(.+)$",
    re.M,
)


# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(text: str):
    """Return (frontmatter_dict, body). Frontmatter invalid -> ({}, text)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4:]
    try:
        data = yaml.safe_load(raw)
    except Exception:
        return {}, body
    return (data if isinstance(data, dict) else {}), body


def split_sections(body: str):
    """Pecah body per heading '## '. Return [(section_title, section_body)]."""
    parts = re.split(r"^##\s+(.+)$", body, flags=re.M)
    # parts[0] = preamble sebelum heading pertama
    out = []
    if parts[0].strip():
        out.append(("", parts[0].strip()))
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        chunk = parts[i + 1].strip() if i + 1 < len(parts) else ""
        out.append((title, chunk))
    return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v not in (None, "")]
    return [value]


def clean(value):
    return "" if value is None else str(value).strip()


# ------------------------------------------------------------------- indexer

class Indexer:
    def __init__(self, content_dir: Path, db_path: Path):
        self.content_dir = content_dir
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.stats = {
            "scanned": 0, "changed": 0, "unchanged": 0, "removed": 0,
            "pages": 0, "chunks": 0, "entities": 0, "relations": 0,
            "aliases": 0, "sources": 0, "stubs_skipped_fts": 0,
            "topic_timeline_events": 0,
        }

    # -- schema ------------------------------------------------------------
    def init_schema(self):
        self.conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        self.conn.execute(
            "INSERT INTO index_meta(key,value) VALUES('schema_version',?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (SCHEMA_VERSION,))
        self.conn.commit()

    # -- helpers -----------------------------------------------------------
    def rel_path(self, p: Path) -> str:
        return str(p.relative_to(self.content_dir)).removesuffix(".md")

    def md_files(self):
        return sorted(p for p in self.content_dir.rglob("*.md") if p.is_file())

    def hash_map(self):
        return {r["path"]: r["content_hash"]
                for r in self.conn.execute("SELECT path, content_hash FROM pages")}

    def alias_lookup(self):
        """alias (lowercase) -> page_path (ID kanonis & unik)."""
        m = {}
        for r in self.conn.execute("SELECT alias, page_path FROM aliases"):
            m[r["alias"].lower()] = r["page_path"]
        return m

    def resolve(self, name: str, lookup: dict) -> str | None:
        return lookup.get(name.strip().lower())

    # -- per-file ----------------------------------------------------------
    def index_file(self, path: Path, lookup: dict, full: bool, owned_aliases=()):
        rel = self.rel_path(path)
        raw = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)

        title = clean(fm.get("title")) or path.stem
        etype = clean(fm.get("entity_type") or fm.get("type")) or None
        status = clean(fm.get("status")) or None
        risiko = clean(fm.get("risiko_editorial")) or None
        updated = clean(fm.get("last_updated") or fm.get("date")) or None
        is_stub = (status == "stub")

        # pages
        self.conn.execute(
            "INSERT INTO pages(path,title,type,risiko_editorial,status,updated_at,content_hash) "
            "VALUES(?,?,?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET "
            "title=excluded.title, type=excluded.type, risiko_editorial=excluded.risiko_editorial, "
            "status=excluded.status, updated_at=excluded.updated_at, content_hash=excluded.content_hash",
            (rel, title, etype, risiko, status, updated, sha256_file(path)))
        self.stats["pages"] += 1

        # bersihkan turunan lama untuk halaman ini (idempotent)
        self.conn.execute("DELETE FROM chunks_fts WHERE page_path=?", (rel,))
        self.conn.execute("DELETE FROM entities WHERE page_path=?", (rel,))
        self.conn.execute("DELETE FROM aliases WHERE page_path=?", (rel,))
        self.conn.execute("DELETE FROM relations WHERE page_path=?", (rel,))
        self.conn.execute("DELETE FROM sources WHERE page_path=?", (rel,))
        self.conn.execute("DELETE FROM topic_timeline_events WHERE hub_path=?", (rel,))

        # entities
        self.conn.execute(
            "INSERT INTO entities(page_path,nama,type) VALUES(?,?,?) "
            "ON CONFLICT(page_path) DO UPDATE SET nama=excluded.nama, type=excluded.type",
            (rel, title, etype))
        self.stats["entities"] += 1

        # aliases: HANYA yang dimiliki halaman ini (kepemilikan ditentukan pass 1,
        # first-wins deterministik). Alias yang sudah dimiliki halaman lain tidak
        # boleh direbut — kalau direbut, `resolve` bergantung urutan index.
        for a in owned_aliases:
            self.conn.execute(
                "INSERT OR REPLACE INTO aliases(alias,page_path) VALUES(?,?)", (a, rel))
            self.stats["aliases"] += 1

        # chunks_fts (stub dilewati dari FTS)
        if is_stub:
            self.stats["stubs_skipped_fts"] += 1
        else:
            for section, chunk in split_sections(body):
                if not chunk:
                    continue
                if RELATION_SECTIONS.match(section or ""):
                    continue  # section relasi/sumber bukan narasi
                self.conn.execute(
                    "INSERT INTO chunks_fts(page_path,title,section,body) VALUES(?,?,?,?)",
                    (rel, title, section, chunk))
                self.stats["chunks"] += 1

        # sources
        sumber_status = clean(fm.get("sumber_status")) or None
        for s in as_list(fm.get("sumber")):
            if isinstance(s, dict):
                self.conn.execute(
                    "INSERT OR IGNORE INTO sources(page_path,url,judul,tanggal,dokumen,sumber_status) "
                    "VALUES(?,?,?,?,?,?)",
                    (rel, clean(s.get("url")) or None, clean(s.get("judul")) or None,
                     clean(s.get("tanggal")) or None, clean(s.get("dokumen")) or None, sumber_status))
            elif isinstance(s, str) and s.strip():
                self.conn.execute(
                    "INSERT OR IGNORE INTO sources(page_path,url,judul,tanggal,dokumen,sumber_status) "
                    "VALUES(?,?,?,?,?,?)", (rel, None, s.strip(), None, None, sumber_status))
            self.stats["sources"] += 1
        if not as_list(fm.get("sumber")) and sumber_status:
            self.conn.execute(
                "INSERT OR IGNORE INTO sources(page_path,url,judul,tanggal,dokumen,sumber_status) "
                "VALUES(?,?,?,?,?,?)", (rel, None, None, None, None, sumber_status))

        # relations dari frontmatter (pertahankan sumber & confidence apa adanya)
        # Node key = page_path (unik). Nama tampilan diambil via entities.
        seen_rel = set()
        for r in as_list(fm.get("relasi")):
            if not isinstance(r, dict):
                continue
            subjek = self.resolve(clean(r.get("subjek_id") or r.get("subjek")), lookup) or rel
            objek = self.resolve(clean(r.get("objek_id") or r.get("objek")), lookup)
            if not objek or objek == rel:
                continue
            if objek == subjek:
                continue
            predikat = clean(r.get("predikat")) or "terkait_dengan"
            conf = clean(r.get("confidence")) or "low"
            key = (subjek, predikat, objek)
            if key in seen_rel:
                continue
            seen_rel.add(key)
            self.conn.execute(
                "INSERT OR IGNORE INTO relations(subjek,predikat,objek,sumber,confidence,origin,page_path,keterangan) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (subjek, predikat, objek, clean(r.get("sumber")) or None, conf,
                 "frontmatter", rel, clean(r.get("keterangan")) or None))
            self.stats["relations"] += 1

        # relations implisit dari wikilinks: predikat='menyebut', confidence='low'
        for m in WIKILINK.finditer(body):
            target = (m.group(2) or m.group(1)).strip()
            canonical = self.resolve(target, lookup)
            if not canonical or canonical == rel:
                continue
            key = (rel, "menyebut", canonical)
            if key in seen_rel:
                continue
            seen_rel.add(key)
            self.conn.execute(
                "INSERT OR IGNORE INTO relations(subjek,predikat,objek,sumber,confidence,origin,page_path,keterangan) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (rel, "menyebut", canonical, None, "low", "wikilink", rel, None))
            self.stats["relations"] += 1

        # topic_timeline_events: sub-event kronologi bila halaman bertipe topik
        if etype == "topik":
            self._index_topic_events(rel, title, body, lookup)

    def _index_topic_events(self, hub_path: str, hub_title: str, body: str, lookup: dict):
        matches = list(TOPIC_EVENT_HEADING.finditer(body))
        for m in matches:
            dt_str = m.group(1)
            event_title = clean(m.group(2))
            try:
                date.fromisoformat(dt_str)
            except ValueError:
                continue

            start_pos = m.end()
            nxt = re.search(r"^#{2,3}\s+", body[start_pos:], flags=re.M)
            chunk = body[start_pos : start_pos + nxt.start()].strip() if nxt else body[start_pos:].strip()
            summary = chunk[:500]

            links_list = []
            for lm in WIKILINK.finditer(chunk):
                t1 = lm.group(1).strip()
                t2 = lm.group(2).strip() if lm.group(2) else None
                for t in (t1, t2):
                    if not t:
                        continue
                    canonical = self.resolve(t, lookup)
                    if canonical and canonical not in links_list:
                        links_list.append(canonical)
                    if t not in links_list:
                        links_list.append(t)

            links_json = json.dumps(links_list, ensure_ascii=False)
            self.conn.execute(
                "INSERT INTO topic_timeline_events(hub_path, hub_title, event_date, event_title, event_summary, links) "
                "VALUES(?,?,?,?,?,?)",
                (hub_path, hub_title, dt_str, event_title, summary, links_json),
            )
            self.stats["topic_timeline_events"] += 1

    # -- run ---------------------------------------------------------------
    def run(self, full: bool = False):
        t0 = time.time()
        self.init_schema()
        if full:
            for t in ("chunks_fts", "names_fts", "relations", "aliases",
                      "entities", "sources", "pages", "topic_timeline_events"):
                self.conn.execute(f"DELETE FROM {t}")
            self.conn.commit()

        known = self.hash_map()
        files = self.md_files()
        self.stats["scanned"] = len(files)

        # pass 1: bangun alias lookup alias -> page_path dari SELURUH file di disk
        # (deterministik: file pertama menang; duplikat dilaporkan)
        lookup = {}
        self.duplicate_aliases = []
        owned: dict = {}          # alias asli (case) -> rel pemilik
        owner_of: dict = {}       # alias lower  -> rel pemilik
        for path in files:
            rel = self.rel_path(path)
            raw = path.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(raw)
            title = clean(fm.get("title")) or path.stem
            for a in sorted(set(as_list(fm.get("aliases"))) | {title, path.stem, rel}):
                a = clean(a)
                if not a:
                    continue
                k = a.lower()
                if k in owner_of and owner_of[k] != rel:
                    self.duplicate_aliases.append((a, owner_of[k], rel))
                    continue          # first-wins: halaman pertama mempertahankan alias
                owner_of[k] = rel
                owned.setdefault(rel, []).append(a)
                lookup.setdefault(k, rel)

        # force re-index bila kepemilikan alias berbeda dari yang ada di DB
        db_owner = {}
        for r in self.conn.execute(
                "SELECT a.alias, a.page_path FROM aliases a"):
            db_owner.setdefault(r["alias"].lower(), r["page_path"])
        force = set()
        for k, rel in owner_of.items():
            if db_owner.get(k) != rel:
                force.add(rel)
                if db_owner.get(k):
                    force.add(db_owner[k])

        # pass 2: index file yang berubah
        for path in files:
            rel = self.rel_path(path)
            h = sha256_file(path)
            if not full and known.get(rel) == h and rel not in force:
                self.stats["unchanged"] += 1
                continue
            self.index_file(path, lookup, full, owned.get(rel, ()))
            self.stats["changed"] += 1

        # hapus halaman yang filenya sudah tidak ada
        disk = {self.rel_path(p) for p in files}
        for rel in set(known) - disk:
            self.conn.execute("DELETE FROM chunks_fts WHERE page_path=?", (rel,))
            self.conn.execute("DELETE FROM relations WHERE page_path=?", (rel,))
            self.conn.execute("DELETE FROM sources WHERE page_path=?", (rel,))
            self.conn.execute("DELETE FROM aliases WHERE page_path=?", (rel,))
            self.conn.execute("DELETE FROM entities WHERE page_path=?", (rel,))
            self.conn.execute("DELETE FROM topic_timeline_events WHERE hub_path=?", (rel,))
            self.conn.execute("DELETE FROM pages WHERE path=?", (rel,))
            self.stats["removed"] += 1

        # names_fts dari entities
        self.conn.execute("DELETE FROM names_fts")
        for r in self.conn.execute("SELECT nama FROM entities"):
            self.conn.execute("INSERT INTO names_fts(name,canonical) VALUES(?,?)",
                              (r["nama"], r["nama"]))
        for r in self.conn.execute(
                "SELECT a.alias, e.nama FROM aliases a JOIN entities e ON e.page_path=a.page_path"):
            self.conn.execute("INSERT INTO names_fts(name,canonical) VALUES(?,?)",
                              (r["alias"], r["nama"]))

        self.conn.execute(
            "INSERT INTO index_meta(key,value) VALUES('last_rebuild',?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (time.strftime("%Y-%m-%dT%H:%M:%S"),))
        self.conn.commit()
        self.stats["duplicate_aliases"] = len(getattr(self, "duplicate_aliases", []))
        self.stats["elapsed_s"] = round(time.time() - t0, 2)
        return self.stats

    def close(self):
        self.conn.close()


def main():
    ap = argparse.ArgumentParser(description="Irawiki SQLite indexer")
    ap.add_argument("--content", default=str(DEFAULT_CONTENT))
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--full", action="store_true", help="rebuild penuh")
    args = ap.parse_args()

    idx = Indexer(Path(args.content), Path(args.db))
    stats = idx.run(full=args.full)
    idx.close()
    for k, v in stats.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
