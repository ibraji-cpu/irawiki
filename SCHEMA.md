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
