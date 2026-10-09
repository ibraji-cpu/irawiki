"""
wiki_query.py — Lapisan baca untuk wiki_index.db (Fase 3).

Dipakai oleh:
  - irawiki_api/mcp_server.py  (tools MCP)
  - irawiki_api/main.py        (endpoint HTTP /search)

Read-only. Tidak pernah menulis ke DB maupun Markdown.

CATATAN SKEMA (Fase 2):
  - Node relasi = `page_path`, BUKAN nama. Setiap input nama harus di-resolve
    dulu via tabel `aliases` -> `page_path`.
  - `relations` punya `origin` (frontmatter|wikilink) dan `confidence`.
  - Ada 4 alias duplikat: resolver mengembalikan SEMUA kandidat, tidak menebak.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

DB_PATH = Path("/home/ubuntu/irawiki/wiki_index.db")

# Bobot BM25: page_path, title, section, body (title x3, section x2, body x1)
BM25_WEIGHTS = (1.0, 3.0, 2.0, 1.0)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def available() -> bool:
    return DB_PATH.is_file()


# --------------------------------------------------------------- resolver

def resolve(name: str) -> dict:
    """Resolve nama/alias -> halaman kanonis.

    Return:
      {"status":"unique", "page_path":..., "nama":..., "type":...}
      {"status":"ambiguous", "candidates":[...]}
      {"status":"not_found", "query":...}
    """
    if not name or not name.strip():
        return {"status": "not_found", "query": name}
    q = name.strip()

    with _connect() as conn:
        rows = conn.execute(
            """SELECT DISTINCT e.page_path, e.nama, e.type
               FROM aliases a JOIN entities e ON e.page_path = a.page_path
               WHERE LOWER(a.alias) = LOWER(?)""", (q,)).fetchall()
        if not rows:  # fallback: exact nama
            rows = conn.execute(
                """SELECT page_path, nama, type FROM entities
                   WHERE LOWER(nama) = LOWER(?)""", (q,)).fetchall()

    if not rows:
        return {"status": "not_found", "query": q}
    if len(rows) == 1:
        r = rows[0]
        return {"status": "unique", "page_path": r["page_path"],
                "nama": r["nama"], "type": r["type"]}
    return {"status": "ambiguous",
            "candidates": [{"page_path": r["page_path"], "nama": r["nama"],
                            "type": r["type"]} for r in rows]}


def _fts_quote(q: str) -> str:
    """Quote tiap token agar aman untuk MATCH FTS5."""
    toks = [t for t in q.replace('"', " ").split() if t]
    return " ".join(f'"{t}"' for t in toks)


# ----------------------------------------------------------------- search

def search(query: str, tipe: str | None = None, limit: int = 10) -> dict:
    """FTS5 BM25 berbobot + ekspansi alias otomatis."""
    if not query or not query.strip():
        return {"query": query, "count": 0, "results": []}

    terms = [query.strip()]
    alias_note = None

    with _connect() as conn:
        # ekspansi alias: query cocok dengan alias -> tambah nama kanonisnya
        canon = conn.execute(
            """SELECT DISTINCT e.nama FROM aliases a
               JOIN entities e ON e.page_path = a.page_path
               WHERE LOWER(a.alias) = LOWER(?)""", (query.strip(),)).fetchall()
        if canon:
            names = [c["nama"] for c in canon]
            terms.extend(names)
            alias_note = names

        match = " OR ".join(_fts_quote(t) for t in dict.fromkeys(terms))
        sql = f"""SELECT c.page_path, c.title, c.section,
                         snippet(chunks_fts, 3, '[', ']', '…', 14) AS snippet,
                         bm25(chunks_fts, {','.join(str(w) for w in BM25_WEIGHTS)}) AS score,
                         p.type, p.status
                  FROM chunks_fts c
                  JOIN pages p ON p.path = c.page_path
                  WHERE chunks_fts MATCH ?"""
        args: list = [match]
        if tipe:
            # `tipe` menerima DUA bentuk:
            #   - nilai kolom pages.type  : individu | organisasi | peristiwa | analisis
            #   - nama folder konten      : aktor | peristiwa | analisis
            # (Fase 1 menetapkan entity_type = individu/organisasi, sedangkan
            #  "aktor" adalah folder — keduanya harus bisa dipakai sebagai filter)
            sql += " AND (p.type = ? OR p.path LIKE ?)"
            args.extend([tipe, f"{tipe}/%"])
        sql += " ORDER BY score LIMIT ?"
        args.append(max(1, min(int(limit), 100)))

        try:
            rows = conn.execute(sql, args).fetchall()
        except sqlite3.OperationalError:
            return {"query": query, "count": 0, "results": [],
                    "error": "query tidak dapat diparse untuk FTS5"}

    results = [{
        "title": r["title"], "type": r["type"], "page_path": r["page_path"],
        "section": r["section"], "snippet": r["snippet"],
        "score": round(-r["score"], 4),  # bm25 negatif -> dibalik agar besar = relevan
    } for r in rows]
    out = {"query": query, "count": len(results), "results": results}
    if alias_note:
        out["alias_expanded_to"] = alias_note
    return out


# --------------------------------------------------------------- relations

def _edge_rows(conn, page_path: str, origin: str | None = None):
    sql = """SELECT r.id, r.subjek, r.predikat, r.objek, r.sumber, r.confidence,
                    r.origin, r.keterangan,
                    COALESCE(es.nama, r.subjek) AS subjek_nama,
                    COALESCE(eo.nama, r.objek)  AS objek_nama
             FROM relations r
             LEFT JOIN entities es ON es.page_path = r.subjek
             LEFT JOIN entities eo ON eo.page_path = r.objek
             WHERE (r.subjek = ? OR r.objek = ?)"""
    args: list = [page_path, page_path]
    if origin and origin != "all":
        sql += " AND r.origin = ?"
        args.append(origin)
    return conn.execute(sql, args).fetchall()


def _edge_dict(r) -> dict:
    return {
        "subjek": r["subjek_nama"], "predikat": r["predikat"],
        "objek": r["objek_nama"], "subjek_path": r["subjek"],
        "objek_path": r["objek"], "sumber": r["sumber"],
        "confidence": r["confidence"], "origin": r["origin"],
        "keterangan": r["keterangan"],
    }


def get_relations(entitas: str, depth: int = 1, origin: str = "all") -> dict:
    """Traversal N-hop (BFS) dari sebuah entitas."""
    res = resolve(entitas)
    if res["status"] == "ambiguous":
        return {"status": "ambiguous", "query": entitas, "candidates": res["candidates"]}
    if res["status"] == "not_found":
        return {"status": "not_found", "query": entitas,
                "message": f"Entitas '{entitas}' tidak ditemukan di tabel aliases/entities."}

    depth = max(1, min(int(depth), 3))
    start = res["page_path"]
    visited = {start}
    frontier = [start]
    edges: list[dict] = []
    seen_edges: set = set()

    with _connect() as conn:
        for level in range(1, depth + 1):
            nxt: list[str] = []
            for node in frontier:
                for r in _edge_rows(conn, node, origin):
                    key = (r["subjek"], r["predikat"], r["objek"], r["origin"])
                    if key in seen_edges:
                        continue
                    seen_edges.add(key)
                    d = _edge_dict(r)
                    d["hop"] = level
                    edges.append(d)
                    for other in (r["subjek"], r["objek"]):
                        if other not in visited:
                            visited.add(other)
                            nxt.append(other)
            frontier = nxt
            if not frontier:
                break

    return {
        "status": "ok", "entitas": res["nama"], "page_path": start,
        "depth": depth, "origin_filter": origin,
        "edge_count": len(edges), "node_count": len(visited), "edges": edges,
    }


# ---------------------------------------------------------------- entity

def get_entity(nama: str) -> dict:
    """Metadata halaman + seluruh relasi keluar/masuk + sumber."""
    res = resolve(nama)
    if res["status"] == "ambiguous":
        return {"status": "ambiguous", "query": nama, "candidates": res["candidates"],
                "message": "Alias ambigu — pilih salah satu page_path, lalu panggil ulang."}
    if res["status"] == "not_found":
        return {"status": "not_found", "query": nama,
                "message": f"Entitas '{nama}' tidak ditemukan."}

    pp = res["page_path"]
    with _connect() as conn:
        page = conn.execute("SELECT * FROM pages WHERE path=?", (pp,)).fetchone()
        if page is None:
            return {"status": "not_found", "query": nama, "message": "Halaman tidak ada di index."}
        out_edges = [_edge_dict(r) for r in _edge_rows(conn, pp) if r["subjek"] == pp]
        in_edges = [_edge_dict(r) for r in _edge_rows(conn, pp) if r["objek"] == pp]
        sources = [dict(r) for r in conn.execute(
            """SELECT url, judul, tanggal, dokumen, sumber_status FROM sources
               WHERE page_path=?""", (pp,))]
        aliases = [r["alias"] for r in conn.execute(
            "SELECT alias FROM aliases WHERE page_path=? ORDER BY alias", (pp,))]
        deg = conn.execute(
            "SELECT out_deg, in_deg FROM entity_degree WHERE page_path=?", (pp,)).fetchone()

    return {
        "status": "ok",
        "nama": page["title"], "page_path": pp, "type": page["type"],
        "status_halaman": page["status"], "risiko_editorial": page["risiko_editorial"],
        "updated_at": page["updated_at"],
        "aliases": aliases,
        "degree": {"out": deg["out_deg"], "in": deg["in_deg"]} if deg else None,
        "sumber": sources,
        "relasi_keluar": out_edges, "relasi_masuk": in_edges,
    }


# ------------------------------------------------------------- relations_between

def relations_between(a: str, b: str, max_depth: int = 4) -> dict:
    """BFS jalur terpendek antara dua entitas."""
    ra, rb = resolve(a), resolve(b)
    for r, label in ((ra, a), (rb, b)):
        if r["status"] == "ambiguous":
            return {"status": "ambiguous", "query": label, "candidates": r["candidates"]}
        if r["status"] == "not_found":
            return {"status": "not_found", "query": label,
                    "message": f"Entitas '{label}' tidak ditemukan."}

    start, goal = ra["page_path"], rb["page_path"]
    if start == goal:
        return {"status": "ok", "from": ra["nama"], "to": rb["nama"],
                "hops": 0, "path": [], "message": "Kedua nama menunjuk halaman yang sama."}

    max_depth = max(1, min(int(max_depth), 5))
    prev: dict[str, tuple] = {}
    visited = {start}
    frontier = [start]
    found = False

    with _connect() as conn:
        for _ in range(max_depth):
            nxt: list[str] = []
            for node in frontier:
                for r in _edge_rows(conn, node):
                    for other in (r["subjek"], r["objek"]):
                        if other in visited:
                            continue
                        visited.add(other)
                        prev[other] = (node, _edge_dict(r))
                        nxt.append(other)
                        if other == goal:
                            found = True
            if found:
                break
            frontier = nxt
            if not frontier:
                break

    if not found:
        return {"status": "ok", "from": ra["nama"], "to": rb["nama"], "hops": None,
                "path": [], "max_depth": max_depth,
                "message": f"Tidak ada jalur relasi dalam {max_depth} hop."}

    # rekonstruksi jalur
    chain = []
    cur = goal
    while cur in prev:
        parent, edge = prev[cur]
        chain.append(edge)
        cur = parent
    chain.reverse()
    return {"status": "ok", "from": ra["nama"], "to": rb["nama"],
            "hops": len(chain), "path": chain}


# ---------------------------------------------------------------- timeline

def timeline(entitas: str) -> dict:
    """Peristiwa dan kronologi hub yang terhubung ke entitas, urut kronologis."""
    res = resolve(entitas)
    if res["status"] == "ambiguous":
        return {"status": "ambiguous", "query": entitas, "candidates": res["candidates"]}
    if res["status"] == "not_found":
        return {"status": "not_found", "query": entitas,
                "message": f"Entitas '{entitas}' tidak ditemukan."}

    pp = res["page_path"]
    with _connect() as conn:
        # 1. Query relasional halaman peristiwa
        rows = conn.execute(
            """SELECT DISTINCT p.path, p.title, p.updated_at,
                      (SELECT MIN(s.tanggal) FROM sources s
                        WHERE s.page_path = p.path AND s.tanggal IS NOT NULL) AS tanggal,
                      r.predikat, r.confidence, r.origin
               FROM relations r
               JOIN pages p ON p.path = CASE WHEN r.subjek = ? THEN r.objek ELSE r.subjek END
               WHERE (r.subjek = ? OR r.objek = ?) AND p.type = 'peristiwa'""",
            (pp, pp, pp)).fetchall()

        # 2. Query sub-event dari topic_timeline_events untuk hub relevan
        hub_rows = []
        try:
            hub_rows = conn.execute(
                """SELECT t.id, t.hub_path, t.hub_title, t.event_date, t.event_title,
                          t.event_summary, t.links
                   FROM topic_timeline_events t
                   WHERE t.hub_path = ?
                      OR t.hub_path IN (
                          SELECT r.subjek FROM relations r WHERE r.objek = ?
                          UNION
                          SELECT r.objek FROM relations r WHERE r.subjek = ?
                      )
                   ORDER BY t.event_date ASC, t.id ASC""",
                (pp, pp, pp)).fetchall()
        except sqlite3.OperationalError:
            hub_rows = []

    # Map dan deduplikasi relasi ganda ke page peristiwa yang sama
    page_events = {}
    for r in rows:
        path = r["path"]
        m_dt = re.search(r"(\d{4}-\d{2}-\d{2})", path)
        dt = m_dt.group(1) if m_dt else (r["tanggal"] or r["updated_at"])

        # Prioritas relasi: frontmatter lebih diutamakan daripada wikilink
        if path not in page_events or (r["origin"] == "frontmatter" and page_events[path]["origin"] != "frontmatter"):
            page_events[path] = {
                "tanggal": dt,
                "title": r["title"],
                "page_path": path,
                "predikat": r["predikat"],
                "confidence": r["confidence"],
                "origin": r["origin"],
                "source": "page",
            }

    # Deduplikasi sub-event hub terhadap page event
    merged_events = list(page_events.values())
    for hr in hub_rows:
        h_date = hr["event_date"]
        h_links = []
        if hr["links"]:
            try:
                h_links = json.loads(hr["links"])
            except Exception:
                h_links = [hr["links"]]

        is_dup = False
        for pe in page_events.values():
            pe_dt = str(pe["tanggal"] or "")
            dt_match = (h_date == pe_dt or h_date.startswith(pe_dt) or Path(pe["page_path"]).name.startswith(h_date))
            stem = Path(pe["page_path"]).stem
            name = Path(pe["page_path"]).name
            link_match = any(l in (pe["page_path"], pe["title"], stem, name) for l in h_links)
            if dt_match and link_match:
                is_dup = True
                if len(pe_dt) < 10 and len(h_date) == 10:
                    pe["tanggal"] = h_date
                break

        if not is_dup:
            merged_events.append({
                "tanggal": h_date,
                "title": hr["event_title"],
                "summary": hr["event_summary"],
                "hub_path": hr["hub_path"],
                "predikat": "kronologi_hub",
                "confidence": "high",
                "origin": "hub_body",
                "source": "hub",
            })

    merged_events.sort(key=lambda e: (e["tanggal"] or "9999"))
    return {"status": "ok", "entitas": res["nama"], "count": len(merged_events), "events": merged_events}


# ------------------------------------------------------------------ page

def get_page(path: str) -> dict:
    """Baca konten penuh halaman dari Markdown (source of truth)."""
    from pathlib import Path as _P
    root = _P("/home/ubuntu/irawiki/content")
    cand = root / f"{path}.md"
    if not cand.is_file():
        return {"status": "not_found", "page_path": path}
    return {"status": "ok", "page_path": path,
            "markdown": cand.read_text(encoding="utf-8")}
