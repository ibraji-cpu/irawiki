# DRAF Prompt untuk Agen Teknisi — Kalender B+ Minggu 1 Ira Amalia

Status draf: dibuat 25 Oktober 2026, atas perintah user di chat web. JANGAN dikirim
ke teknisi sebelum user mengisi bagian [DIISI SAAT MERGE PETA] dan menyetujuinya.
Prompt ini menggantikan, untuk Minggu 1 ini saja, cara lama teknisi mengambil paket
dari folder media-queue — untuk Minggu 1, sumber teks adalah peta yang sudah di-merge
user, bukan folder media-queue.
KEPUTUSAN USER 25 Oktober 2026: sumber teks = GitHub saja (opsi 1); teknisi
mengerjakan KETIGA format (image+text, carousel, reels) — kemampuannya untuk
ketiganya sudah dikonfirmasi user. Gerbangnya: user MENGECEK TEKS DULU sebelum
teks apa pun di-push ke GitHub; teknisi hanya mengambil versi yang sudah di-merge,
tidak pernah mengambil draf workspace/Drive yang belum dicek.

---

## Perintah untuk teknisi (salin dari sini ke bawah saat sudah disetujui user)

Halo, ini permintaan produksi media untuk Kalender Konten B+ Minggu 1 Ira Amalia
(@iraamaliabot + blog.iraamalia.id).

### 1. Tema dan minggu
- Tema: Kinerja Pemerintahan + Kepuasan Publik, payung "Menagih Janji dan Bukti".
- Minggu: Senin 26 Oktober – Jumat 30 Oktober 2026.
- Jadwal feed minggu ini (7 posting): Senin 2× image+text (pagi dan sore), Selasa
  carousel, Rabu reel, Kamis 2× image+text (pagi dan sore), Jumat carousel.
  Story harian format bebas tidak termasuk dalam permintaan ini, kecuali user
  memintanya terpisah.

### 2. Sumber teks — ambil dari GitHub setelah user merge peta
- Repo GitHub: ibraji-cpu/irawiki
- Path file peta yang sudah di-merge user: peta/peta-kinerja-kepuasan-publik-2026-10-25.md
  (di luar folder content/, jadi BUKAN halaman wiki)
- Branch yang sudah di-merge: main (setelah PR #62 di-merge manual oleh user)
- PR peta (SUDAH di-merge manual oleh user, terverifikasi 25 Oktober 2026 09:13 WIB):
  https://github.com/ibraji-cpu/irawiki/pull/62
  dari branch konten/peta-kinerja-kepuasan-publik-2026-10-25, commit 4bc4b797,
  merged_at 2026-10-25T02:12:39Z; file terverifikasi ada di main dengan SHA
  48b90b3e1fbb23894df107db73096f6649aa733d yang sama dengan versi branch.
  Gerbang merge SUDAH terpenuhi — teknisi boleh mulai dari versi main ini.
- Ambil teks HANYA dari peta yang sudah di-merge itu, plus teks yang disetujui
  user yang dilampirkan bersama perintah ini (jika ada).
- GERBANG PENGECEKAN: teks itu sudah dicek user SEBELUM di-push ke GitHub.
  Teknisi hanya bekerja dari versi yang sudah di-merge — jangan pernah mengambil
  draf dari workspace, folder Drive, atau spreadsheet pelacak, dan jangan pernah
  memakai versi sebelum merge.
- LAMPIRAN TEKS FINAL (DISETUJUI user 25 Oktober 2026, setelah user mengedit):
  file `teks-final-ig-minggu-1-2026-10-25.md` yang ikut terkirim bersama prompt
  ini. File itu berisi naskah persis ketujuh posting (Senin pagi/sore, carousel
  Selasa, reel Rabu, Kamis pagi/sore, carousel Jumat). Produksi HARUS dari
  file lampiran itu, BUKAN menyusun kalimat sendiri dari data peta. Jika ada
  perbedaan antara peta dan lampiran, lampiran yang menang — karena lampiran
  itulah yang sudah disetujui user. Jangan mengubah satu kata pun dari lampiran.
- JANGAN mengarang teks, angka, kutipan, atau klaim baru. JANGAN mengambil teks
  dari sumber lain, dari artikel lama, atau dari ingatan.
- Jika path GitHub di atas tidak ditemukan, atau peta belum di-merge: BERHENTI,
  laporkan "sumber teks tidak ditemukan / peta belum di-merge", dan JANGAN
  memproduksi apa pun dari tebakan.

### 3. Aturan keras yang tidak boleh dilanggar
- Teknisi TIDAK mengubah teks sama sekali: tidak menambah, mengurangi, menyingkat,
  atau mempercantik kata. Teks yang melebihi batas = produksi berhenti untuk item
  itu, laporkan ke user, dan item itu menunggu teks revisi — bukan dipotong diam-diam.
- Teknisi TIDAK membuka PR, TIDAK merge, dan TIDAK memposting ke Instagram.
  Pengiriman hasil ke Drive di bawah ini BUKAN persetujuan untuk posting.
  Posting hanya dilakukan setelah user menyetujui media finalnya secara eksplisit.
- Teknisi TIDAK menulis ulang artikel blog, wiki, atau caption. Pekerjaan teknisi
  hanya merender media dari teks yang sudah disetujui.

### 4. Spesifikasi per format

#### A. Image+text (Senin pagi/sore dan Kamis pagi/sore)
- Isi teks: FAKTA/DATA SAJA. Tanpa kutipan tokoh — otomatisasi tidak bisa memasang
  foto tokohnya, dan kutipan tanpa foto tokoh rawan salah atribusi.
- Batas keras teks: maksimal 170 karakter per gambar.
- Background: file `background-gambar-teks.jpg` di folder Drive 03 Gambar+Teks
  (lihat §5). Rasio background 3:4 (ukuran file 1792×2400).
- Penempatan: teks di area atas yang gelap. Jangan menutupi perempuan berkamera
  di kiri bawah dan jangan menutupi logo iraamalia.id di kanan bawah.
- Hasil akhir: file gambar per posting, disimpan di folder Drive 03 Gambar+Teks.

#### B. Carousel (Selasa dan Jumat)
- Cover: background `background-cover-carousel.jpg` di folder Drive 05 Carousel.
- Slide isi: background `background-isi-carousel.jpg` di folder Drive 05 Carousel
  (versi gelap/bertekstur dari foto yang sama, supaya teks lebih terbaca).
- Ukuran background: 1792×2400, rasio mendekati 3:4.
- Teks cover dan slide isi diambil persis dari teks yang disetujui — tidak diubah.
  Jika teks slide melebihi area yang terbaca, berhenti untuk slide itu dan laporkan,
  jangan mengecilkan teks sampai tidak terbaca tanpa seizin user.
- Hasil akhir: file gambar per slide, dalam urutan tampil, disimpan di folder
  Drive 05 Carousel, dengan nama yang jelas per hari dan per nomor slide.

#### C. Reels (Rabu) — hyperframes
- Durasi: 60–90 detik. Format vertikal 1080×1920 (rasio 9:16).
- Background: file `background-reels.jpg` di folder Drive 04 Reels
  (latar terang bergaris grid, tagar #politiktanpaanakmuda di atas,
  logo iraamalia.id di kiri bawah).
- Catatan: background ini MENGGANTIKAN template "Video Anak Muda" lama untuk
  Minggu 1 ini. Jangan memakai background potret Ira Amalia lama kecuali user
  memerintahkan lain secara eksplisit.
- Narasi/VO dan caption di video diambil persis dari naskah yang disetujui —
  tidak diubah, tidak ditambah kata.
- Hasil akhir: file video MP4/MOV per reel, disimpan di folder Drive 04 Reels.

### 5. URL background untuk teknisi (terverifikasi di Drive 25 Oktober 2026)
- Image+text — `background-gambar-teks.jpg` (folder 03 Gambar+Teks):
  https://drive.google.com/file/d/1d0eQNf_BoXKU5NAbWjFd67nn9bRfViR_/view?usp=drivesdk
- Carousel cover — `background-cover-carousel.jpg` (folder 05 Carousel):
  https://drive.google.com/file/d/14xT6xjKCfZ87SCQbMzWWNq1kiCWZnZf2/view?usp=drivesdk
- Carousel isi — `background-isi-carousel.jpg` (folder 05 Carousel):
  https://drive.google.com/file/d/1et_zourIG9zJptBc0tOG_cODjuObSpXB/view?usp=drivesdk
- Reels — `background-reels.jpg` (folder 04 Reels):
  https://drive.google.com/file/d/1rdy9y6BG5d6ZQtSXcwcV-pXsbKSALgl2/view?usp=drivesdk
- Jika satu URL tidak bisa dibuka teknisi: berhenti untuk format itu dan laporkan,
  jangan memakai background pengganti tanpa perintah user.

### 5. Folder tujuan di Google Drive (sudah dibuat oleh agen konten)
- Folder induk: "Kalender Konten B+ Ira Amalia - Minggu 1 (26-30 Okt 2026)"
- 01 Blog — bukan untuk teknisi (artikel blog, diurus agen konten + user).
- 02 Instagram Teks — bukan untuk teknisi (teks Instagram, diurus agen konten).
- 03 Gambar+Teks — hasil akhir image+text teknisi ke sini.
- 04 Reels — hasil akhir video reels teknisi ke sini, plus file background-reels.jpg
  sudah ada di sini sebagai acuan.
- 05 Carousel — hasil akhir carousel teknisi ke sini, plus kedua file background
  carousel sudah ada di sini sebagai acuan.
- Tautan folder induk (TERKONFIRMASI bisa diakses user 25 Oktober 2026): https://drive.google.com/drive/folders/1pNaOlaJS8nUAgJqmpfhCH-TlgDA19YvI
- Jika folder tujuan tidak bisa diakses: berhenti dan laporkan, jangan mengirim
  hasil ke tempat lain tanpa perintah user.

### 6. Laporan selesai dari teknisi
Setelah semua item selesai, laporkan kembali ke user (lewat agen konten):
- Daftar file hasil per hari dan per format, dengan nama file persisnya.
- Item apa pun yang TIDAK jadi, beserta alasannya (misalnya teks melebihi batas,
  sumber tidak ditemukan, folder tidak bisa diakses).
- Konfirmasi bahwa tidak ada PR, merge, atau posting Instagram yang dilakukan.

---

## Catatan untuk user (bukan bagian dari perintah ke teknisi)

- UPDATE 25 Oktober 2026: folder tujuan Drive TERKONFIRMASI bisa diakses user —
  tautan di §5 sudah diisi. KEPUTUSAN USER 25 Oktober 2026: sumber = GitHub saja
  (opsi 1), format = KETIGA format (image+text, carousel, reels — kemampuan
  teknisi untuk ketiganya sudah dikonfirmasi user), dan gerbang pengecekan =
  user cek teks dulu sebelum push ke GitHub.
- UPDATE 25 Oktober 2026, jalan 2 (repo irawiki): pembuatan repo baru
  iraamalia-peta-konten GAGAL (403, App tidak bisa membuat repo), lalu user
  memilih jalan 2. Peta di-push ke irawiki di path peta/ (di luar content/),
  branch konten/peta-kinerja-kepuasan-publik-2026-10-25, commit 4bc4b797,
  PR #62 ke main — SUDAH di-merge manual oleh user 25 Oktober 2026
  (merged_at 02:12:39Z, file terverifikasi di main, SHA sama). Gerbang merge
  TERPENUHI; draf prompt ini sekarang LENGKAP dan siap diteruskan ke teknisi.
- PENTING — spreadsheet bukan peta: spreadsheet "Kalender Konten B+ Ira Amalia -
  26 Okt-20 Nov 2026" di Drive adalah lembar pelacak kalender (6 sheet: Ringkasan,
  Minggu 1–4, Evaluasi; tiap minggu 17 baris judul/tanggal/status), BUKAN peta
  teks. Peta yang dimaksud draf ini adalah file
  `peta-kinerja-kepuasan-publik-2026-10-25.md` (5 artikel Minggu 1 + paket data
  PPI/SMRC/Voxpol + turunan IG), yang saat ini masih di workspace, BELUM di
  GitHub dan BELUM di-merge. Jadi spreadsheet tidak bisa menggantikan peta
  sebagai sumber teks teknisi — teknisi butuh teks persis, bukan judul baris.
- TIDAK ADA LAGI yang menghalangi pengiriman: PR #62 sudah di-merge manual dan
  file terverifikasi di main. Teks final per hari yang sudah disetujui (jika
  teks belum ada di peta itu sendiri) tetap dilampirkan saat pengiriman. Opsi
  sumber Drive sudah DITOLAK user (pilih opsi 1: GitHub saja) — jangan
  dihidupkan lagi tanpa perintah baru.
- Keputusan format SUDAH DIPUTUSKAN user: ketiga format dikerjakan teknisi.
  Tidak ada lagi yang dicoret.
- Prompt lama teknisi (media-queue, STATUS READY/TAKEN/DONE, template Video Anak
  Muda dan Ira Kafe) tidak dipakai untuk Minggu 1 ini, kecuali user memerintahkan
  kembali secara eksplisit.
