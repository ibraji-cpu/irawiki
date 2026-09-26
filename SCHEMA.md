# IRAWIKI Schema & Guidelines

> Dokumen ini adalah panduan (tata tertib) untuk penulis (manusia) dan Agen AI yang mengelola IRAWIKI.
> IRAWIKI mengadaptasi konsep "LLM Wiki", namun dimodifikasi khusus untuk arsitektur Flat-File Obsidian -> Quartz.

## 1. Arsitektur Flat-File (PENTING!)
- **JANGAN PERNAH MEMBUAT SUB-FOLDER BARU** (seperti `raw/`, `entities/`, `concepts/`, dsb).
- Semua file `.md` wajib diletakkan **sejajar** (di dalam root folder vault, atau mengikuti letak file `index.md`).
- Sebagai pengganti sub-folder, klasifikasi HANYA dilakukan menggunakan atribut **Frontmatter `type:`**.

## 2. Klasifikasi Tipe Halaman (`type:`)
Selalu isi atribut `type:` di YAML sesuai dengan kriteria berikut:
- `entity` : Untuk entitas (tokoh politik, pengusaha, perusahaan, partai, organisasi).
- `concept` : Untuk konsep, peraturan perundang-undangan, atau isu kebijakan publik.
- `comparison` : Untuk halaman analisis yang membandingkan dua atau lebih entitas secara mendalam.
- `raw` : Untuk arsip mentah, *copy-paste* artikel berita panjang, transkrip, yang sifatnya *immutable* (tidak boleh diedit substansinya).
- `query` : Halaman jawaban hasil rangkuman analisis dari suatu pertanyaan spesifik/kompleks.

## 3. Frontmatter & Kualitas Data
Setiap halaman wajib/sangat disarankan memakai atribut YAML berikut untuk menjaga standar jurnalistik/intelijen:
- `sources: []` : Senarai tautan/judul file referensi asli (berasal dari halaman `type: raw` atau URL).
- `confidence: high | medium | low` :
  - `high` : Didukung banyak sumber independen yang saling memvalidasi.
  - `medium` / `low` : Hanya bersumber dari satu berita, gosip politik, atau klaim yang bergerak sangat cepat.
- `contested: true | false` : Ubah menjadi `true` jika halaman ini mengandung klaim/fakta yang saling bertentangan antar-sumber.
- `contradictions: []` : Daftar tautan ke halaman atau rujukan lain yang membantah fakta di halaman ini.

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
- `entity_type` (individu | peristiwa | analisis)
- `confidence` (1–10)
- `risiko_editorial` (rendah | sedang | tinggi)
- `last_updated` (YYYY-MM-DD)

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
- mencari hubungan tersembunyai;
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