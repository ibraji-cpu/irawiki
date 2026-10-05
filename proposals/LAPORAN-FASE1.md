# Laporan Fase 1 — Ekstraksi & Normalisasi Frontmatter Wiki (FINAL)

**Tanggal:** 5 Oktober 2026 · **Repo:** /home/ubuntu/irawiki (main) · **Status:** sudah di-push ke origin

## Hasil akhir

| Metrik | Nilai |
|---|---|
| Total halaman | 334 |
| Punya `entity_type` | 332 (2 pengecualian di proposals/) |
| `sumber:` terstruktur | 59 file (100 record) |
| `sumber_status: prosa` | 143 file (backlog) |
| `relasi:` terstruktur | **98 file, 355 relasi** |
| `status: stub` | 45 file |
| YAML invalid | **0** |
| Prosa body terhapus | **0** |
| Quartz build | OK (334 → 928 output, 18 detik) |

## Skema relasi yang diterapkan (keputusan: (a)+(b), tolak (c))

```yaml
relasi:
  - subjek_id: "gksr-gerakan-kedaulatan-suara-rakyat"   # opsional
    objek_id: "aktor/muhammad-said-iqbal"               # wajib, path kanonis
    predikat: "terkait_dengan"                          # predikat terkontrol
    confidence: "medium"                                # medium|low
    sumber: null                                        # fallback sumber level halaman
    keterangan: "Ketua Umum GKSR dan Presiden Partai Buruh..."
```

- `confidence: medium` (98) = halaman punya `sumber:` ber-URL → provenance tertelusur
- `confidence: low` (257) = halaman tanpa URL
- **URL tidak pernah ditebak dari link inline body** (aturan (c) ditolak)
- Semua relasi dipetakan ke `terkait_dengan`; pemetaan teks→predikat spesifik
  (`memimpin`, `anggota_dari`, dst.) butuh review manusia, tidak dilakukan otomatis

## Angka relasi

- Bullet relasi total: 585 → 141 placeholder ("_belum ada data_") → **444 nyata**
- 407 punya wikilink; resolusi alias ke halaman kanonis: **98,3%** (index 1.088 nama)
- 37 bullet tanpa link (prosa/nama bold) tidak diekstraksi — tidak bisa diresolve aman
- 98 file menghasilkan relasi; sisanya section placeholder

## Riwayat commit (semua pushed)

| Commit | Isi |
|---|---|
| `39e1be2` | fase1a: backfill entity_type (133 file) |
| `353577d` | fase1d: tandai 45 stub |
| `6d5f211` | fase1b: sumber terstruktur (56 file) |
| `4dd9833` | wiki: perkaya 3 profil aktor (perubahan lama, di-commit terpisah) |
| `66efcee` | fase1b: lanjutan 3 file tertunda |
| `8c91366` | fase1b2: sumber_status prosa (142 file) |
| `2750ed5` | wiki: halaman analisis Jokowi/RUU (sebelumnya untracked) |
| `4551a4a` | fase1c: relasi terstruktur (98 file, 355 relasi) |

## File perlu keputusan

| File | Masalah |
|---|---|
| `content/index.md` | bukan entitas; belum ada `entity_type` |
| `content/iraamalia-id.md` | jenis entitas belum ditetapkan |
| 143 file | `sumber_status: prosa` — backlog, dilengkapi oportunistik |
| 141 section relasi | masih placeholder "_belum ada data_" |
| 37 bullet relasi | tanpa wikilink, tidak dapat diresolve otomatis |

## Catatan teknis

- Index alias dibangun dari: path, basename, `title`, `aliases` (1.088 entri, case-insensitive)
- Setiap penulisan frontmatter divalidasi `yaml.safe_load` + cek jumlah record sebelum ditulis
- Commit dipecah agar perubahan pra-Fase 1 tidak tercampur (history bersih)
- `content/index.md` masih modified di working tree — di luar scope, tidak disentuh
