# IRAWIKI Schema & Guidelines

> Dokumen ini adalah panduan (tata tertib) untuk penulis (manusia) dan Agen AI yang mengelola IRAWIKI.
> IRAWIKI mengadaptasi konsep "LLM Wiki", namun dimodifikasi khusus untuk arsitektur Markdown (Obsidian) -> Quartz.
> Revisi 2026-11-11 (Fase 1 audit GEO): diselaraskan dengan skema frontmatter
> dan struktur folder yang benar-benar live di repo.

## 1. Struktur folder (yang live)
- Hub living document di root `content/` (mis. `content/satgas-pkh.md`,
  `content/kinerja-pemerintahan-prabowo-gibran.md`).
- Subfolder yang ada: `content/aktor/`, `content/peristiwa/`,
  `content/kategori/` (dan `content/analisis/` bila ada halaman analisis
  yang terbit — saat ini belum ada).
- **JANGAN membuat subfolder baru** tanpa keputusan (mis. `raw/`,
  `entities/`, `concepts/`).
- Indeks: `content/index.md` (homepage wiki).

## 2. Klasifikasi halaman
Klasifikasi dilakukan lewat frontmatter — BUKAN lewat atribut `type:`
(`type: entity/concept/comparison/raw/query` sudah tidak dipakai):
- `entity_type`: `individu` | `perusahaan` | `organisasi` | `lembaga` |
  `peristiwa` | `topik` | `analisis` | `konsep`
- `kategori` (taksonomi 6, nama tampil diputuskan 2026-10-22):
  `sumber-daya-alam` | `pasar-dan-kepemilikan` | `aturan-main-demokrasi` |
  `hukum-dan-pertanahan` | `kinerja-pemerintahan` | `konsep`
- `kategori_tambahan`: list, opsional, bila satu halaman masuk dua kategori.
- `category`: penanda asal folder (`aktor` dsb., warisan template) —
  bukan taksonomi; jangan disamakan dengan `kategori`.

## 3. Frontmatter (yang live)
Field yang dipakai file-file di repo (contoh: `content/aktor/andi-syamsuddin-arsyad.md`,
`content/peristiwa/polemik-ijazah-gibran.md`):
- `title`, `description` (satu kalimat informatif), `date` (YYYY-MM-DD,
  tanggal terbit), `updated` (YYYY-MM-DD, tanggal pembaruan terakhir)
- `aliases`: list variasi nama/judul (untuk pencarian dan wikilink)
- `tags`: list topik
- `entity_type`, `entity_id` (slug konsisten untuk Wikilink, untuk hub/topik)
- `status`: mis. `aktif`
- `confidence` (1–10, angka — BUKAN `high/medium/low`): tingkat keyakinan
  terhadap kualitas informasi terkumpul; sumber terbatas → nilai rendah
- `risiko_editorial`: `rendah` | `sedang` | `tinggi` — kebutuhan
  kehati-hatian editorial, **bukan vonis terhadap aktor**
- `relasi`: list relasi terstruktur; boleh `[]` — relasi utama saat ini
  hidup di Wikilink body + seksi `## Aktor yang Terlibat` /
  `## Relasi Terkait` (lihat §8D). Jangan mengisi `relasi:` dengan
  dugaan; hanya relasi yang didukung sumber.
- `sumber`: list item `{url, tanggal}` — URL sumber asli + tanggal
  publikasi sumber; jangan hapus sumber lama saat sumber baru ditemukan
- `kategori`, `kategori_tambahan`, `last_verified` (YYYY-MM-DD,
  tanggal verifikasi terakhir — BUKAN `last_updated`)
- **Tidak dipakai lagi:** `type:`, `confidence: high/medium/low`,
  `contested:`, `contradictions:` — bila sumber saling bertentangan,
  tulis di seksi `## Catatan presisi` di body + naikkan `risiko_editorial`.
- Jangan buat field baru untuk info tambahan; info tanpa tempat jelas
  masuk body Markdown bila relevan. Jangan masukkan opini ke field fakta.
- Judul seksi relevansi di body: `## Apa relevansinya dengan anak muda?`
  (satu konvensi, diputuskan 2026-10-21). Judul lama
  `## Kenapa penting buat Gen Z` masih ada di 81 file dan diseragamkan
  bertahap; generator `tools/build_seo.py` menormalisasinya di `llms-full.txt`.

## 4. Kebijakan Jejak Rekam (Provenance)
- Jika sebuah halaman mensintesis lebih dari 3 dokumen sumber berbeda, sangat disarankan menempelkan penanda kutipan spesifik (seperti catatan kaki) di akhir paragraf, contoh: `^[nama-file-sumber.md]`.

## 5. Sistem Logging (No log.md)
- **TIDAK PERLU MEMBUAT `log.md`.**
- IRAWIKI murni bersandar pada **Git Log** sebagai *Single Source of Truth* untuk riwayat.
- Jika AI butuh orientasi (mengetahui apa yang terakhir dikerjakan), AI cukup menjalankan terminal: `git log --oneline -n 10` atau `git status`.

## 6. Threshold Halaman Baru
- Buat file `.md` baru HANYA jika entitas tersebut adalah fokus utama (signifikan) dari sebuah sumber, atau muncul di lebih dari satu sumber terpisah. Jangan membuat file baru hanya karena entitas tersebut "numpang lewat" di satu kalimat.

---

## 7. Template Standar (User memilih saat konversi)

Tiga template utama di `templates/`:
- `01_aktor_master_template.md` → untuk **Aktor** (individu, organisasi, perusahaan)
- `02_peristiwa_template.md` → untuk **Peristiwa** (kejadian substantif berwaktu)
- `03_analysis_template.md` → untuk **Analisis** (relasi, kepentingan, interpretasi)

Masing-masing template sudah include frontmatter lengkap dengan:
- `entity_id` (slug konsisten untuk Wikilink)
- `entity_type` (individu | peristiwa | analisis | topik | konsep | perusahaan | organisasi | lembaga)
- `confidence` (1–10)
- `risiko_editorial` (rendah | sedang | tinggi)
- `last_verified` (YYYY-MM-DD)

---

## 8. PETUNJUK AGEN AI — IRAWIKI (MANDATORY)

### Tujuan
Mengubah bahan raw menjadi file Markdown `.md` yang siap dimasukkan ke IraWiki.

Fokus utama hanya:
1. **Aktor**
2. **Peristiwa**
3. **Relasi**

Jangan memperluas pekerjaan ke pemetaan politik, kesimpulan jaringan, prediksi, atau analisis lain yang tidak diperlukan oleh bahan sumber.

### Prinsip Utama

#### 1. Fakta sebelum interpretasi
Ekstrak informasi yang didukung oleh sumber.
Jangan mengubah:
- dugaan menjadi fakta;
- opini menjadi fakta;
- korelasi menjadi hubungan kausal;
- kemunculan bersama dalam suatu berita menjadi relasi;
- kedekatan geografis, organisasi, partai, atau institusi menjadi bukti jejaring.
Jika sumber tidak menyatakan hubungan tersebut, jangan membuatnya.

#### 2. AI bukan hakim
Jangan menentukan sendiri apakah seorang aktor:
- bersekongkol;
- melakukan transaksi politik;
- mengendalikan aktor lain;
- memiliki agenda tersembunyi;
- menerima konsesi;
- melakukan operasi tertentu;
kecuali terdapat bukti yang secara jelas mendukung pernyataan tersebut.
Jika sebuah sumber membuat tuduhan atau interpretasi, pertahankan sebagai atribusi:
> [Nama sumber] menyatakan/menilai/menduga bahwa ...
Bukan:
> Aktor X melakukan ...

#### 3. Jangan melakukan reasoning yang tidak diperlukan
Tugas utama adalah: **identifikasi → ekstraksi → klasifikasi → WikiLink → penyusunan Markdown.**
Tidak perlu:
- membangun teori jaringan;
- mencari hubungan tersembunyi;
- memprediksi langkah aktor;
- mengisi field yang tidak tersedia;
- membuat konteks panjang;
- mengulang informasi yang sudah ada di halaman aktor.

### A. ATURAN AKTOR
**Jika aktor belum ada**: Buat halaman menggunakan `01_aktor_master_template.md`. Isi hanya field yang didukung bahan sumber. Field tidak diketahui → kosongkan atau `tidak diketahui`. Jangan mengarang.
**Jika aktor sudah ada**: Jangan membuat ulang seluruh profil. Perbarui hanya informasi yang berubah atau informasi baru yang relevan. Pindahkan jabatan lama ke `jabatan_historis`. Tambahkan perkembangan baru pada `## Perkembangan Terakhir` dengan Wikilink ke peristiwa terkait.

### B. ATURAN PERISTIWA
Satu kejadian substantif = satu file peristiwa.
**Buat file peristiwa BARU jika**: keputusan baru, tindakan baru, perubahan status, respons baru substantif, perkembangan baru dengan waktu/peristiwa tersendiri.
Hubungkan dengan `peristiwa_terkait:`. Jangan menyalin seluruh kronologi lama. Gunakan `## Perkembangan Terakhir` untuk catatan terbaru.

### C. ATURAN ANALISIS
Analisis bertumpu pada: fakta, sumber, relasi terdokumentasi, kepentingan yang ditunjukkan sumber.
Jangan memaksa setiap peristiwa punya analisis. Analisis baru hanya jika ada pertanyaan/perkembangan analitis berbeda.
Jika lanjutan, gunakan `analisis_sebelumnya:`. Jangan salin seluruh analisis lama.
Pisahkan `## Fakta yang Relevan` dari `## Perspektif / Interpretasi`.

### D. ATURAN RELASI
Relasi hanya dicatat jika: (1) disebutkan eksplisit oleh sumber, ATAU (2) didukung bukti dokumenter jelas.
Contoh relasi valid: jabatan, kepemilikan, keanggotaan, hubungan keluarga, organisasi, perusahaan, hubungan formal.
**JANGAN** menyimpulkan relasi hanya karena: hadir acara sama, diberitakan bersama, daerah sama, pemerintahan sama, kepentingan sama, mendukung kebijakan sama.

### E. ATURAN WIKILINK
Gunakan `[[Nama Aktor]]`, `[[Nama Peristiwa]]`, `[[Nama Perusahaan]]`, `[[Nama Organisasi]]` jika entitas sudah ada atau harus dibuat.
Jangan buat variasi nama untuk entitas sama. Pertahankan konsistensi `entity_id`.

### F. ATURAN FOLLOW-UP
- **Aktor sama**: Jangan ulang profil. Update perubahan saja.
- **Peristiwa sama**: Pembaruan kecil → gunakan `peristiwa_terkait` + `## Perkembangan Terakhir`.
- **Peristiwa baru**: Buat file baru + hubungkan `peristiwa_terkait`.
- **Analisis lanjutan**: Buat file analisis baru + hubungkan `analisis_sebelumnya`.

### G. ATURAN FRONTMATTER
Frontmatter harus stabil dan sederhana.
Jangan buat field baru untuk info menarik tambahan. Gunakan field yang tersedia di template.
Info tanpa tempat jelas → masuk body Markdown jika relevan.
Jangan masukkan opini ke field fakta.

### H. ATURAN `confidence` (1–10)
Menunjukkan tingkat keyakinan terhadap kualitas informasi terkumpul.
Jangan naikkan confidence hanya karena LLM merasa masuk akal.
Sumber terbatas / info belum jelas → nilai lebih rendah.

### I. ATURAN `risiko_editorial`
Tandai kebutuhan kehati-hatian editorial. **Bukan vonis terhadap aktor.**
Klaim sensitif, tuduhan, info diperdebatkan → tetap harus punya atribusi/sumber.

### J. OUTPUT
Output akhir: Markdown bersih, siap disimpan `.md`.
JANGAN beri:
- penjelasan panjang proses reasoning;
- teori jaringan tidak diminta;
- prediksi;
- kesimpulan politik tanpa bukti sumber;
- info tidak ada dalam bahan.
**Info tidak tersedia → jangan mengarang.**
**Hubungan tidak terbukti → jangan bikin Wikilink seolah terbukti.**
**Sumber hanya dugaan → pertahankan sebagai dugaan + atribusi ke sumber.**

---

> **Prinsip kerja terakhir**
> **AI mencari dan menyusun titik-titiknya. IraWiki menyimpan titik-titik beserta sumbernya. Relasi dibangun dari bukti yang terdokumentasi. Pembaca dapat melihat garis di antara titik-titik tersebut.**