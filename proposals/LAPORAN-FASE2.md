# Laporan Fase 2 — Indexer SQLite (FINAL)

**Tanggal:** 5 Oktober 2026 · **Repo:** /home/ubuntu/irawiki · **Status:** pushed ke origin
**DB:** `/home/ubuntu/irawiki/wiki_index.db` (1,59 MB) — di `.gitignore`, tidak di-commit

## Hasil

| Kriteria | Target | Hasil |
|---|---|---|
| Skema §2a, journal_mode=wal | ya | ✅ wal, foreign_keys=ON |
| Backfill penuh | < 60 detik | **1,28 detik** (334 file) |
| `pages` | 334 | ✅ 334 (45 stub) |
| `entities` | ≈ file entitas | ✅ 334 |
| `relations` | ≥ 355 | ✅ **798** (355 frontmatter + 443 wikilink) |
| `aliases` | ≈ 1.088 | ✅ 1.103 |
| `chunks_fts` / `names_fts` | > 0 | ✅ 1.129 / 1.437 |
| Incremental terbukti | 1 file | ✅ changed=1, unchanged=333 |
| DB di .gitignore | ya | ✅ |
| Timer dibuat, belum enable | ya | ✅ `not-found` (belum terpasang) |

## Query uji (semua lolos)

1. **FTS** `korupsi` → Achmad Taufik Husein, Adrianto Pitojo Adhi, KPK ✓
2. **BM25 berbobot** (title ×3, section ×2, body ×1) `bayan` → PT Bayan Resources Tbk di puncak ✓
3. **Trigram substring** `Soekarnoputr` → Megawati Soekarnoputri ✓
4. **Relasi** `relations_view` → nama tampilan (bukan path) ✓
5. **VACUUM** → 1,59 MB, WAL ter-checkpoint ✓

## Keputusan desain yang menyimpang dari brief (dan alasannya)

**1. Node relasi = `page_path`, bukan nama entitas.**
Brief menetapkan `relations.subjek/objek` sebagai nama. Namun repo punya **3 pasang
halaman berjudul identik**: `joko-widodo`/`jokowi`, `lim-hariyanto-wijaya-sarwono`/`lim-hariyanto`,
dan dua halaman peristiwa PKPU. Memakai nama sebagai identitas node akan **menggabungkan
entitas berbeda** dan membuat edge ambigu. Maka:
- `entities` PK = `page_path` (bukan `nama`)
- `aliases.page_path` → halaman kanonis
- `relations.subjek/objek` = `page_path`
- View `relations_view` menampilkan nama via JOIN — pembacaan manusia tidak berubah

Dampak: **0 relasi yatim** (semua node resolve ke entity), 0 self-relation.

**2. `relations.origin` + `keterangan` ditambahkan.**
Brief tidak menyebutnya. Tanpa `origin`, relasi frontmatter (hasil kurasi) tidak bisa
dibedakan dari `menyebut` otomatis dari wikilink (jauh lebih lemah). Ini penting untuk Fase 3.

**3. Tokenizer `unicode61 remove_diacritics 2`** — brief hanya menyebut `unicode61`.

**4. Tabel `index_meta`** untuk `schema_version` + `last_rebuild`.

## Catatan verifikasi

- Stub dikecualikan dari FTS: **0 kebocoran** dari 45 halaman stub
- `PRAGMA foreign_key_check` → 0 pelanggaran
- Semua relasi frontmatter `sumber`/`confidence` dipertahankan apa adanya (medium 98, low 700)
- Section relasi & `## Sumber` tidak dimasukkan ke FTS body (bukan narasi)

## Yang perlu keputusan manusia

| Item | Detail |
|---|---|
| 4 alias duplikat | `Joko Widodo`+`jokowi`, `Lim Hariyanto Wijaya Sarwono`+`lim-hariyanto`, 2 halaman PKPU — file pertama menang. Perlu konsolidasi atau biarkan sebagai halaman terpisah. |
| Timer belum di-enable | Perlu `sudo cp tools/systemd/* /etc/systemd/system/ && sudo systemctl enable --now irawiki-indexer.timer` setelah review. |
| `content/index.md` | masih `M` di working tree (di luar scope Fase 2) |

## Commit

| Commit | Isi |
|---|---|
| `836aee2` | fase2a: skema wiki_index.db |
| `2a445d2` | fase2b: indexer incremental |
| `a8ab030` | fase2c: gitignore + systemd timer |

## File baru

- `tools/init_schema.sql` — skema + view
- `tools/irawiki_indexer.py` — indexer (stdlib + PyYAML)
- `tools/systemd/irawiki-indexer.{service,timer}` — belum di-enable
