# Sistem Wiki Ira Amalia — Panduan Teknis

## Arsitektur

```
irawiki/
├── content/          # Semua file markdown artikel (.md) — 147 file
├── templates/        # Template artikel (01_aktor, 02_peristiwa, 03_analisis)
├── quartz/           # Quartz v5.0.0 (static site generator)
├── public/           # Output build (HTML, XML, tags, sitemap) — di-generate ulang setiap build
├── SCHEMA.md         # Schema frontmatter & panduan penulisan
├── quartz.config.yaml # Konfigurasi Quartz (plugin, tema, layout)
├── build_wiki.sh     # Script build utama
└── pull-rebuild.sh   # Script pull + build (jika dari repo lain)
```

## Alur Kerja

```
Edit .md di content/ → build_wiki.sh → Quartz parse → public/ → deploy ke iraamalia.id
```

## Script Build: `build_wiki.sh`

```bash
#!/bin/bash
set -e
echo "[*] Build Quartz..."
cd /home/ubuntu/irawiki
node ./quartz/bootstrap-cli.mjs build
echo "[✅] Selesai."
```

Yang dijalankan: `node ./quartz/bootstrap-cli.mjs build` — ini command resmi Quartz v5. Outputnya:
- Clean `public/`
- Parse 147 file markdown dari `content/`
- Emit ~400 file HTML ke `public/`
- Generate `sitemap.xml`, `index.xml`, `contentIndex.json`, tag pages, dll.

## Wiki Links Sistem

**Mekanisme:**
Quartz v5 mendukung **Obsidian-flavored markdown** (plugin `@quartz-community/obsidian-flavored-markdown`). Format wiki link:

```markdown
[[nama-file|mexkan teks]]
[[nama-file]]
```

- `nama-file` = nama file `.md` di `content/` tanpa ekstensi
- Contoh: `[[haji-isam|Haji Isam]]` → link ke `haji-isam.md`
- Jika file target tidak ada, Quartz tetap me-render link (tapi akan menunjuk ke halaman 404)

**Graph View:**
Quartz mengekstrak wiki links dari body markdown, lalu me-render graph interaktif (Ctrl+G di halaman). Graph node = setiap halaman, edge = wiki link.

**Backlinks:**
Plugin `@quartz-community/backlinks` menampilkan daftar halaman yang link ke halaman saat ini. Backlinks hanya muncul jika halaman lain memiliki wiki link ke halaman tersebut.

**Peringkat:** Wiki links muncul di:
- Body artikel (inline)
- Graph view (visual)
- Backlinks panel (sidebar kanan)

## Relasi / Knowledge Graph dalam Frontmatter

Beberapa file menggunakan frontmatter `related:` untuk mendeklarasikan hubungan:

```yaml
---
related:
- bayan-resources
- bursa-efek-indonesia
- haji-isam
---
```

**Penting:** Frontmatter `related:` **tidak** otomatis menghasilkan wiki links di body. Hanya decorative/meta. Untuk hubungan yang muncul di graph dan backlinks, harus pakai wiki links `[[...]]` di body markdown.

Beberapa file juga menggunakan frontmatter standar GraphQL-like:
```yaml
entity_type: individual
entity_id: haji-isam
source: kg-documents[haji-isam-saham-bayan-2026]
attributes: '{"birth_year": 1977, ...}'
```

Ini berasal dari pipeline `kg-documents` (Knowledge Graph documents). Frontmatter ini tidak mempengaruhi rendering wiki, hanya metadata.

## File yang Wajib Ada

| Komponen | Path | Fungsi |
|----------|------|--------|
| `content/index.md` | → halaman "/all" | Daftar semua artikel |
| `content/iraamalia-id.md` | → halaman "/iraamalia-id" | Tentang wiki |
| `content/akuisisi-bayan-haji-isam-2026.md` | → "/akuisisi-bayan-haji-isam-2026" | Artikel utama (contoh) |

## Template Artikel

3 template di `templates/`:
- `01_aktor_master_template.md` — template untuk halaman aktor/individu
- `02_peristiwa_template.md` — template untuk halaman peristiwa
- `03_analysis_template.md` — template untuk analisis

## Plugins Quartz yang Aktif (dari `quartz.config.yaml`)

- `@quartz-community/created-modified-date` — tanggal di halaman
- `@quartz-community/syntax-highlighting` — code block
- `@quartz-community/obsidian-flavored-markdown` — **wiki links [[...]]**
- `@quartz-community/crawl-links` — resolusi link
- `@quartz-community/description` — meta description
- `@quartz-community/backlinks` — panel backlinks (sidebar kanan)
- `@quartz-community/graph` — graph view
- `@quartz-community/search` — pencarian
- `@quartz-community/tags` — tag pages
- `@quartz-community/note-properties` — tampilkan frontmatter di halaman
- `@quartz-community/explorer` — navigasi sidebar kiri
- `@quartz-community/content-index` — sitemap + RSS

## Best Practice

1. **Wiki link di body**, bukan hanya di frontmatter `related:`. Frontmatter `related:` hanya metadata.
2. **Nama file wiki link** = nama file `.md` tanpa ekstensi. Case-sensitive.
3. **File duplikat** — hindari. Jika ada `low-tuck-kwong.md` dan `dato-low-tuck-kwong.md` untuk orang yang sama, gabung atau hapus satu.
4. **Body file entitas** — wajib ada konten, bukan hanya frontmatter. File dengan body kosong tidak akan muncul di graph.
5. **Setelah edit**, jalankan `bash build_wiki.sh` lalu `git push`.

## File yang Patut Diketahui

- `content/akuisisi-bayan-haji-isam-2026.md` — artikel utama, 23 wiki links
- `content/haji-isam.md` — halaman aktor Haji Isam
- `content/dato-low-tuck-kwong.md` — halaman aktor Low Tuck Kwong
- `content/pt-bayan-resources-tbk.md` — halaman perusahaan BYAN
- `content/pt-jhonlin-baratama.md` — kendaraan akuisisi
- `content/pt-jhonlin-agro-raya.md` — entitas terkait (bukan pembeli)
- `content/peristiwa_haji_isam_akuisisi_saham_bayan_resources_byan.md` — halaman peristiwa
- `content/relasi-aktor-20260830-haji-isam-andi-syamsuddin-arsyad.md` — relasi aktor

## Lokasi Server

- Repo: `github.com:ibraji-cpu/irawiki.git` (branch `main`)
- Build: dijalankan lokal, output `public/` di-deploy ke `iraamalia.id` (Nginx)

---

Jika agen lain perlu menjalankan perubahan:
1. Edit file `.md` di `content/`
2. `cd /home/ubuntu/irawiki && bash build_wiki.sh`
3. `cd /home/ubuntu/irawiki && git add -A && git commit -m "..." && git push origin main`
4. Tunggu deploy (Nginx pull) — biasanya otomatis via webhook atau cron
