"""
Irawiki MCP server — Fase 3.

Tools baca bersumber dari wiki_index.db via lapisan `wiki_query` (bukan scan
file). `irawiki_save_draft` tetap satu-satunya jalur tulis dan TIDAK diubah
perilakunya (tetap menulis ke proposals/ untuk review manusia).

CATATAN SKEMA:
  - Node relasi = page_path, bukan nama; semua input nama di-resolve via `aliases`.
  - Setiap edge membawa `confidence` (high|medium|low) dan `origin`
    (frontmatter = hasil kurasi | wikilink = ekstraksi otomatis).
  - Alias duplikat: resolver mengembalikan daftar kandidat, tidak menebak.
"""

import datetime
import json
import os
import re
import sys

import requests
from mcp.server.mcpserver import MCPServer

sys.path.insert(0, "/home/ubuntu/irawiki_api")
import wiki_query  # noqa: E402

mcp = MCPServer("Irawiki MCP")
API_BASE = "http://127.0.0.1:8000"
TEMPLATES_DIR = "/home/ubuntu/irawiki_hermes_skill/templates"
DRAFTS_DIR = "/home/ubuntu/irawiki_drafts"


def _j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _last_rebuild() -> str:
    try:
        with wiki_query._connect() as conn:
            return conn.execute(
                "SELECT value FROM index_meta WHERE key='last_rebuild'").fetchone()[0]
    except Exception:
        return "unknown"


# ============================================================
# BACA — dari wiki_index.db
# ============================================================

@mcp.tool()
async def irawiki_search(query: str, tipe: str = "", limit: int = 10) -> str:
    """Cari di wiki via FTS5 (BM25 berbobot: title x3, section x2, body x1).

    Args:
        query: kata kunci. Alias otomatis diperluas ke nama kanonisnya.
        tipe: filter opsional — nilai pages.type (individu|organisasi|peristiwa|
              analisis) ATAU nama folder konten (aktor|peristiwa|analisis).
        limit: maksimum hasil (default 10).

    Returns:
        JSON {query, count, results:[{title, type, page_path, section,
        snippet, score}], alias_expanded_to?}
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.search(query, tipe=(tipe or None), limit=limit))


@mcp.tool()
async def irawiki_get_entity(nama: str) -> str:
    """Profil entitas: metadata halaman + relasi keluar/masuk + sumber.

    Args:
        nama: nama entitas, alias, atau page_path (mis. "Joko Widodo",
              "Haji Isam", "aktor/jokowi").

    Returns:
        status='ok' -> {nama, page_path, type, aliases, degree, sumber,
                        relasi_keluar[], relasi_masuk[]}
        status='ambiguous' -> {candidates:[{page_path, nama, type}]}
        status='not_found' -> pesan jelas

    Catatan: jika alias ambigu JANGAN menebak — pilih salah satu page_path dari
    `candidates`, lalu panggil ulang memakai page_path tersebut.
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.get_entity(nama))


@mcp.tool()
async def irawiki_get_relations(entitas: str, depth: int = 1, origin: str = "all") -> str:
    """Traversal relasi N-hop (BFS) dari sebuah entitas.

    Args:
        entitas: nama/alias/page_path entitas awal.
        depth: 1-3 (default 1).
        origin: 'all' | 'frontmatter' (hanya relasi hasil kurasi) |
                'wikilink' (hanya hasil ekstraksi otomatis dari [[wikilink]]).

    Returns:
        {status, entitas, page_path, depth, origin_filter, edge_count,
         node_count, edges:[{subjek, predikat, objek, subjek_path, objek_path,
         sumber, confidence, origin, keterangan, hop}]}

    Catatan: confidence low = halaman tanpa URL sumber; medium = halaman punya
    sumber ber-URL. origin membedakan relasi kurasi dari yang otomatis.
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.get_relations(entitas, depth=depth, origin=origin))


@mcp.tool()
async def irawiki_relations_between(a: str, b: str, max_depth: int = 4) -> str:
    """Cari jalur relasi terpendek antara dua entitas (BFS).

    Args:
        a: entitas awal (nama/alias/page_path).
        b: entitas tujuan.
        max_depth: maksimum hop yang dicari (default 4, maks 5).

    Returns:
        {status, from, to, hops, path:[edge...]} — tiap edge membawa sumber dan
        confidence. Jika tidak ada jalur: hops=null + message jelas.
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.relations_between(a, b, max_depth=max_depth))


@mcp.tool()
async def irawiki_timeline(entitas: str) -> str:
    """Peristiwa yang terhubung ke entitas, urut kronologis.

    Args:
        entitas: nama/alias/page_path entitas.

    Returns:
        {status, entitas, count, events:[{tanggal, title, page_path, predikat,
         confidence, origin}]} — tanggal dari tabel sources, fallback updated_at.
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.timeline(entitas))


@mcp.tool()
async def irawiki_get_page(page_path: str) -> str:
    """Baca konten Markdown penuh sebuah halaman (source of truth).

    Args:
        page_path: path relatif terhadap content/, tanpa .md
                   (mis. "aktor/jokowi" atau "peristiwa/nama-peristiwa").
    """
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    return _j(wiki_query.get_page(page_path))


@mcp.tool()
async def irawiki_stats() -> str:
    """Ringkasan isi index: halaman, entitas, relasi, sumber, stub, last_rebuild."""
    if not wiki_query.available():
        return _j({"error": "wiki_index.db belum tersedia"})
    with wiki_query._connect() as conn:
        def q(sql):
            return conn.execute(sql).fetchone()[0]
        return _j({
            "pages": q("SELECT COUNT(*) FROM pages"),
            "stub": q("SELECT COUNT(*) FROM pages WHERE status='stub'"),
            "entities": q("SELECT COUNT(*) FROM entities"),
            "relations": q("SELECT COUNT(*) FROM relations"),
            "relations_frontmatter": q("SELECT COUNT(*) FROM relations WHERE origin='frontmatter'"),
            "relations_wikilink": q("SELECT COUNT(*) FROM relations WHERE origin='wikilink'"),
            "aliases": q("SELECT COUNT(*) FROM aliases"),
            "sumber": q("SELECT COUNT(*) FROM sources"),
            "last_rebuild": conn.execute(
                "SELECT value FROM index_meta WHERE key='last_rebuild'").fetchone()[0],
        })


# ============================================================
# HTTP Knowledge API (fallback, dipertahankan)
# ============================================================

@mcp.tool()
async def irawiki_get_actor(id: str) -> str:
    """Ambil markdown mentah halaman aktor via HTTP API (fallback)."""
    try:
        r = requests.get(f"{API_BASE}/actors/{id}", timeout=10)
        r.raise_for_status()
        return _j(r.json())
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def irawiki_get_event(id: str) -> str:
    """Ambil markdown mentah halaman peristiwa via HTTP API (fallback)."""
    try:
        r = requests.get(f"{API_BASE}/events/{id}", timeout=10)
        r.raise_for_status()
        return _j(r.json())
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def irawiki_context(
    query: str, focus_actor: str = "", focus_event: str = "", depth: int = 1,
    include_sources: bool = True, include_analysis: bool = True,
    include_timeline: bool = True, include_relations: bool = True, max_tokens: int = 4000
) -> str:
    """Paket konteks siap-pakai untuk LLM: entitas + pencarian + relasi + timeline.

    Menggabungkan get_entity / search / get_relations / timeline menjadi satu
    blok markdown.
    """
    if not wiki_query.available():
        return "Error: wiki_index.db belum tersedia"

    entity = wiki_query.get_entity(focus_actor) if focus_actor else None
    if entity and entity.get("status") == "ambiguous":
        return ("# Context Pack\n\n**Alias ambigu** — pilih salah satu kandidat:\n\n"
                + _j(entity["candidates"]))
    event = wiki_query.get_entity(focus_event) if focus_event else None
    found = wiki_query.search(query, limit=5) if query else {"results": []}
    rels = None
    if include_relations:
        anchor = focus_actor or focus_event or (query or None)
        if anchor:
            rels = wiki_query.get_relations(anchor, depth=depth)
    tl = wiki_query.timeline(focus_actor) if (include_timeline and focus_actor) else None

    md = ["# Context Pack", "", "## Metadata",
          f"- generated_at: {datetime.datetime.now().isoformat()}",
          f"- index_last_rebuild: {_last_rebuild()}",
          f"- query: {query}",
          f"- primary_entity: {focus_actor or focus_event or query or 'None'}", ""]

    if entity and entity.get("status") == "ok":
        md += [f"## Entitas: {entity['nama']}",
               f"- page_path: `{entity['page_path']}`",
               f"- type: {entity['type']}",
               f"- aliases: {', '.join(entity['aliases'])}", ""]
        if include_sources and entity["sumber"]:
            md.append("### Sumber halaman")
            md += [f"- {s.get('tanggal') or '—'} — "
                   f"{s.get('judul') or s.get('url') or s.get('dokumen')}"
                   for s in entity["sumber"]]
            md.append("")
    if event and event.get("status") == "ok":
        md += [f"## Peristiwa: {event['nama']}", f"- page_path: `{event['page_path']}`", ""]

    md += ["## Hasil Pencarian", ""]
    if found["results"]:
        md += [f"- **{r['title']}** ({r['type']}, `{r['page_path']}`)\n  {r['snippet']}"
               for r in found["results"]]
    else:
        md.append("- tidak ada hasil")
    md.append("")

    if rels and rels.get("status") == "ok":
        md += [f"## Relasi (depth={depth}, origin={rels['origin_filter']})",
               f"Total {rels['edge_count']} edge / {rels['node_count']} node.", "",
               "| Subjek | Predikat | Objek | Confidence | Origin | Sumber |",
               "|---|---|---|---|---|---|"]
        for e in rels["edges"][:40]:
            md.append(f"| {e['subjek']} | {e['predikat']} | {e['objek']} | "
                      f"{e['confidence']} | {e['origin']} | {e['sumber'] or '—'} |")
        md.append("")

    if tl and tl.get("status") == "ok" and tl["events"]:
        md += ["## Timeline", ""]
        md += [f"- {e['tanggal'] or '—'} — {e['title']}" for e in tl["events"]]
        md.append("")

    if include_analysis:
        md += ["## Catatan untuk penulis",
               "> Relasi `origin=wikilink` adalah ekstraksi otomatis (confidence low) —",
               "> verifikasi sebelum dipakai sebagai klaim. `origin=frontmatter` hasil kurasi.",
               "> Materi analitis adalah INTERPRETASI, bukan fakta terdokumentasi.", ""]

    out = "\n".join(md)
    if max_tokens and len(out) > max_tokens * 4:
        out = out[: max_tokens * 4] + "\n\n… (dipotong karena max_tokens)"
    return out


# ============================================================
# TULIS — jalur proposal (TIDAK DIUBAH, tetap untuk review manusia)
# ============================================================

@mcp.tool()
async def irawiki_get_template(template_name: str) -> str:
    """Ambil template untuk format penulisan Hermes.
    Tersedia: 'content-brief', 'context-pack', 'visual-brief'."""
    try:
        path = os.path.join(TEMPLATES_DIR, f"{template_name}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return f"Template {template_name} not found. Available: content-brief, context-pack, visual-brief."
    except Exception as e:
        return f"Error loading template: {str(e)}"


@mcp.tool()
async def irawiki_save_draft(title: str, content: str, draft_type: str = "content-brief") -> str:
    """Simpan content brief atau usulan perubahan untuk REVIEW MANUSIA.

    Ini satu-satunya jalur tulis. Tidak ada penulisan langsung ke content/.
    draft_type: 'content-brief', 'proposal', 'visual-brief', dst.
    """
    try:
        safe_title = re.sub(r"[^a-zA-Z0-9_\-]", "_", title.lower())
        folder_path = os.path.join(DRAFTS_DIR, draft_type)
        os.makedirs(folder_path, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{safe_title}.md"
        filepath = os.path.join(folder_path, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Draft '{title}' saved successfully to {filepath}. Awaiting human review."
    except Exception as e:
        return f"Error saving draft: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
