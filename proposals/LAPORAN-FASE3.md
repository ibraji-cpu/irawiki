# Laporan Fase 3 — Perbaikan MCP Server (FINAL)

**Tanggal:** 5 Oktober 2026 · **Status:** pushed ke origin
**Runtime:** `/home/ubuntu/irawiki_api/` (uvicorn :8000) · **Salinan VC:** `tools/irawiki_api/`
**SKILL.md:** `/home/ubuntu/.hermes/skills/irawiki/SKILL.md` (0 byte → 8.518 byte)

## Tools final (12)

| Tool | Sumber data | Catatan |
|---|---|---|
| `irawiki_search` | `chunks_fts` | BM25 title×3, section×2, body×1 + ekspansi alias |
| `irawiki_get_entity` | `entities`+`pages`+`relations`+`sources` | alias ambigu → `candidates[]`, tidak menebak |
| `irawiki_get_relations` | `relations` | BFS depth 1–3, filter `origin` |
| `irawiki_relations_between` | `relations` | BFS jalur terpendek |
| `irawiki_timeline` | `relations`+`pages`+`sources` | peristiwa, urut kronologis |
| `irawiki_get_page` | Markdown (source of truth) | baru |
| `irawiki_stats` | `index_meta` | baru |
| `irawiki_context` | gabungan | **dirombak** — sebelumnya placeholder |
| `irawiki_get_actor` / `_get_event` | HTTP :8000 | fallback, dipertahankan |
| `irawiki_get_template` | file | dipertahankan |
| `irawiki_save_draft` | file | **TIDAK DIUBAH** (satu-satunya jalur tulis) |

`irawiki_get_relations` sebelumnya `return []` (stub) → sekarang traversal nyata.

## Verifikasi via pemanggilan MCP langsung (stdio)

| Uji | Hasil |
|---|---|
| `search("korupsi")` | 3 hasil, KPK di atas ✓ |
| `search` `tipe="aktor"` | 3 hasil (folder aktor) ✓ |
| `search` `tipe="peristiwa"` | 3 hasil ✓ |
| `get_relations("Joko Widodo", depth=2)` | 142 edge / 58 node ✓ |
| `get_relations(origin="frontmatter")` | 6 edge, semua origin=frontmatter ✓ |
| `get_relations(origin="wikilink")` | 10 edge, semua origin=wikilink ✓ |
| `relations_between("Joko Widodo","Prabowo Subianto")` | 2 hop ✓ |
| `relations_between` tanpa jalur | `hops:null` + pesan jelas ✓ |
| `timeline("Haji Isam")` | 16 peristiwa kronologis ✓ |
| `get_entity` tidak ada | `not_found` + pesan ✓ |
| `get_entity` alias ambigu | `ambiguous` + `candidates[]` ✓ (uji DB sintetis) |
| `save_draft` | masih menulis ke `irawiki_drafts/`, perilaku tidak berubah ✓ |
| uvicorn restart | bersih, `/search` 200 ✓ |

## Uji regresi vs substring lama

| Query | FTS (baru) | Substring lama |
|---|---|---|
| `korupsi` | 6 hasil | 3 hasil |
| `bayan` | 10 hasil | 10 hasil |
| `haji isam` | 10 hasil | 10 hasil |

FTS ≥ lama pada ketiganya, dan ranking relevan (judul tepat di puncak).
Substring lama juga hanya memindai `aktor/` dan `peristiwa/` — FTS mencakup
seluruh 334 halaman.

## BUG ditemukan & diperbaiki (di luar brief, tapi memblokir)

**Kepemilikan alias tidak deterministik.** Pass-2 indexer menulis alias dengan
`ON CONFLICT DO UPDATE`, sehingga pemilik alias bergantung urutan index.
Terbukti: `resolve('jokowi')` bergantian antara `aktor/joko-widodo` dan
`aktor/jokowi` antar rebuild. Karena `'Jokowi'` dan `'jokowi'` berbeda
huruf besar/kecil, keduanya hidup berdampingan sebagai dua halaman.

**Fix** (`30c19c3`): kepemilikan ditentukan sekali di pass-1 (first-wins,
urutan path terurut), halaman hanya menulis alias yang dimilikinya, dan
rebuild dipaksa bila kepemilikan di DB berbeda. Diverifikasi 3× rebuild
`--full` → selalu `aktor/joko-widodo`.

## Perubahan cakupan (dilaporkan, bukan disembunyikan)

1. **`main.py /search` diubah** meski brief menyebut "3a → FTS5" untuk `main.py:146`;
   endpoint `/search` adalah sumber `irawiki_search` versi lama. Bentuk respons
   lama (`type`/`id`/`snippet`) dipertahankan agar tidak memutus pemakai.
2. **`irawiki_context` dirombak** — sebelumnya menghasilkan placeholder statis
   (`[Auto-generated timeline will be injected here]`, "No previous analyses").
3. **`tools/irawiki_api/` dibuat** — `irawiki_api/` tidak ada di repo git mana pun,
   jadi perubahan Fase 3 tidak bisa di-commit dari lokasinya. Salinan
   version-controlled; `.env` sengaja tidak disalin.
4. **2 tool tambahan** (`get_page`, `stats`) — di luar daftar brief.

## Yang perlu keputusan manusia

| Item | Detail |
|---|---|
| 3 pasang halaman duplikat | `joko-widodo`/`jokowi` (keduanya `Joko Widodo`, satu stub), `lim-hariyanto-wijaya-sarwono`/`lim-hariyanto`, 2 halaman PKPU. Perlu konsolidasi/merge. |
| Timer indexer | sudah **di-enable** sesuai instruksi; berjalan 15 menit, 1× diuji manual (exit 0, 21,5 MB peak). |
| 45 halaman stub | tidak masuk FTS — kalau dicari tidak akan muncul. |
| 143 file `sumber_status: prosa` | backlog, dilengkapi oportunistik. |

## Commit

`30c19c3` fase2-fix alias deterministik · `6e99115` salinan VC irawiki_api
