# Laporan Konsolidasi Halaman Duplikat

**Tanggal:** 5 Oktober 2026 · **Commit:** `8509c79` · **Backup:** `backup/pre-konsolidasi-20261005`

## Ringkasan

| Sebelum | Sesudah |
|---|---|
| 334 halaman | **331 halaman** |
| 3 pasang judul duplikat | **0** |
| `duplicate_aliases` = 4 | **0** |
| 798 relasi | 777 relasi (self & duplikat dibuang) |
| 1.103 alias | 1.098 alias |

## Detail per pasangan

### 1. `aktor/jokowi` (stub, 372 B) → `aktor/joko-widodo` (kanonik)
- Halaman stub dihapus; alias `Jokowi` + `Joko Widodo` kini dimiliki kanonik
- Relasi self (`aktor/jokowi` → `aktor/jokowi`) dihapus
- `subjek_id` diperbaiki dari `aktor/jokowi` → `aktor/joko-widodo`
- Wikilink `[[jokowi|...]]` → `[[joko-widodo|...]]`
- `sumber_status: prosa` ditambahkan

### 2. `aktor/lim-hariyanto-wijaya-sarwono` (798 B) → `aktor/lim-hariyanto` (1.646 B)
- Konten unik dipertahankan: **catatan Forbes #9 RI (Rp 85,78 triliun / USD 4,9 M)**
- Alias `Lim Hariyanto Wijaya Sarwono` + `Lim Hariyanto` ditambahkan ke kanonik
- Relasi self dihapus, `subjek_id` diperbaiki
- 5 relasi bisnis kanonik dipertahankan (Harita Group, Bumitama Agri, Cita Mineral, Trimegah Bangun Persada, Lim Gunawan Hariyanto)

### 3. `peristiwa/2026-09-30-PKPU-Hakim-MK-Sidang-Ijazah-Gibran` (4.640 B)
→ `peristiwa/2026-09-30-tentang-pkpu-disorot-hakim-mk-sidang-syarat-ijazah-gibran` (kanonik)
- Konten unik dipertahankan dari halaman yang dihapus:
  - 2 poin kronologi spesifik (pertanyaan Hakim **Saldi Isra** & **Enny Nurbaningsih**)
  - Aktor + 2 relasi **Denny Indrayana**
  - Kategori isu `"pemilu"`
- Relasi kanonik: 5 → **7**

## Perbaikan referensi (8 file)

`index.md`, `lim-gunawan-hariyanto`, `andi-syamsuddin-arsyad`, `budi-arie-setiadi`,
`analisis-jokowi-ruu-satu-data`, `Di Balik Keceplosan Budi Arie…`,
`2026-09-24-Jokowi-Ungkap-Riwayat-Sekolah-Gibran`, `2026-09-24-Tanggapan-Jokowi-Ijazah-Gibran-Disoal`

Diperbaiki: `subjek_id`/`objek_id` di frontmatter, wikilink `[[...]]`, dan
link markdown di `index.md`.

## Verifikasi

| Uji | Hasil |
|---|---|
| YAML invalid (331 file) | **0** |
| Referensi ke halaman terhapus | **0** |
| Quartz build | OK — 331 file → 925 output, 15 detik |
| Broken link di output | **0** |
| Indexer `--full` | 331 pages, 777 relations, `duplicate_aliases: 0` |
| MCP `get_entity("Jokowi")` | → `aktor/joko-widodo` ✓ |
| MCP `get_entity("Jokowi")` ambigu? | tidak lagi — **1 alias = 1 halaman** ✓ |
| MCP `get_page("aktor/jokowi")` | `not_found` (benar, sudah dihapus) |
| MCP `get_page("aktor/joko-widodo")` | OK ✓ |

## Catatan

- Alias `jokowi` (lowercase) kini menunjuk `aktor/joko-widodo`; sebelumnya
  menunjuk halaman terpisah `aktor/jokowi` — inilah sumber ambiguitas yang
  ditemukan di Fase 3, sekarang hilang.
- `irawiki_get_relations(Joko Widodo, depth=1, origin=frontmatter)` = 10 edge
  (sebelumnya 6 dari kanonik + 4 dari stub).
