# Laporan Pelaksanaan Pilot Hub Topik Wiki (2 Hub) — Final Klarifikasi

**Tanggal:** 9 Oktober 2026 · **Branch:** `pilot/hub-topik` (terisolasi, bukan main) · **Status:** Siap Review & Merge

---

## 1. Konfirmasi Risiko Editorial & Milestone (§1 Tindak Lanjut)

Setiap file proposal hub telah dilengkapi field `risiko_editorial` komprehensif:

### Hub 1: `Polemik Ijazah Gibran` (`proposals/polemik-ijazah-gibran.md`)
- **Daftar Digabung:** 10 halaman peristiwa dilipat penuh ke entri kronologi.
- **Halaman Dipertahankan & Justifikasi Milestone:**
  1. `2026-10-06-putusan-mk-phpu-ijazah-gibran.md`: **Milestone Peristiwa Independen** berdasarkan kriteria §3 kebijakan: merupakan putusan peradilan konstitusi tertinggi yang bersifat mengikat secara hukum (*final and binding*) pada Perkara Nomor 01/PHPU.PRES-XXIV/2026, memuat amar putusan resmi dan pertimbangan faktual majelis hakim. Ditautkan dua arah pada entri kronologi 2026-10-06.
  2. `sengketa-ijazah-gibran-2026.md`: **Halaman Analisis Independen** yang membedah anatomi hukum perkara konstitusi, temuan bukti pemohon, dan risiko ketatanegaraan. Ditautkan dua arah pada bagian "Analisis Terkait".

### Hub 2: `Sepak Terjang Haji Isam` (`proposals/sepak-terjang-haji-isam.md`)
- **Daftar Digabung:** 13 halaman peristiwa dilipat penuh ke entri kronologi.
- **Halaman Dipertahankan & Justifikasi Milestone:**
  1. `Haji Isam Sepakat Beli 30% Saham BYAN dari Low Tuck Kwong.md`: **Milestone Peristiwa Independen** berdasarkan 4 kriteria §3 kebijakan:
     - *Dokumen Hukum Riil & Definitif:* Menandai penandatanganan resmi CSPA (*Conditional Share Purchase Agreement*) pengalihan 10.000.000.500 lembar saham (30% saham BYAN) antara pengendali pendiri (Low Tuck Kwong & Elaine Low) dengan pembeli (PT Jhonlin Baratama) pada 16 September 2026.
     - *Signifikansi Material Skala Nasional:* Nilai pasar porsi saham mencapai ±Rp115,25 triliun (berdasarkan harga penutupan bursa Rp11.525/saham per 17 September 2026), menjadikannya aksi akuisisi emiten terbesar di BEI sepanjang September 2026.
     - *Perubahan Struktur Kepemilikan Definitif:* Mengubah peta kendali emiten batu bara berkapitalisasi terbesar kedua di Indonesia secara riil (Haji Isam masuk 30%, keluarga Low mempertahankan 32,25%).
     - *Keterbukaan Informasi Regulasi Resmi:* Diumumkan secara resmi kepada OJK & BEI dan memicu penetapan status High Shareholding Concentration (HSC) oleh BEI. Ditautkan dua arah pada entri kronologi 2026-09-16.

---

## 2. Analisis & Konfirmasi Fungsi `timeline()` (§2 Tindak Lanjut)

### Status Aktual Kode
- **Apakah indexer mengekstrak heading `### YYYY-MM-DD` di dalam badan hub menjadi event timeline?**
  **TIDAK.**
- **Penjelasan Teknis:**
  Fungsi `timeline(entitas)` pada `tools/irawiki_api/wiki_query.py` (baris 308–333) saat ini bekerja dengan melakukan query:
  ```sql
  SELECT DISTINCT p.path, p.title, ...
  FROM relations r
  JOIN pages p ON p.path = CASE WHEN r.subjek = ? THEN r.objek ELSE r.subjek END
  WHERE (r.subjek = ? OR r.objek = ?) AND p.type = 'peristiwa'
  ```
  Artinya, `timeline()` saat ini berbasis traversal graf relasi antardokumen (level halaman yang memiliki entri di tabel `pages` dengan tipe `peristiwa`). Indexer (`tools/irawiki_indexer.py`) mengekstrak heading `## ` untuk pencarian teks penuh di `chunks_fts`, namun belum mem-parsing sub-heading `### YYYY-MM-DD` di badan markdown menjadi entitas sub-event individual di basis data.

- **Dampak:**
  - `timeline("Polemik Ijazah Gibran")` saat ini mengembalikan 3 event level halaman yang terhubung via relasi (`2026-10-06-putusan-mk-phpu-ijazah-gibran` dan `sengketa-ijazah-gibran-2026`).
  - `timeline("Sepak Terjang Haji Isam")` mengembalikan event milestone `Haji Isam Sepakat Beli 30% Saham BYAN dari Low Tuck Kwong`.
  - Entri internal `### YYYY-MM-DD` di badan hub tidak muncul sebagai item terpisah di JSON output `timeline()`, tetapi terindeks penuh dan dapat dicari di FTS5 `search()`.

- **Pilihan Tindak Lanjut yang Direkomendasikan:**
  **Opsi (a) — Enhancement Indexer & Query API:**
  Di fase pengembangan berikutnya, indexer dapat ditingkatkan untuk memindai sub-heading dengan pola `r"^###\s+(\d{4}-\d{2}-\d{2})\s+[—-]\s+(.+)$"` pada halaman `entity_type: topik`, lalu menyimpannya ke tabel baru (mis. `topic_timeline_events`). Fungsi `timeline()` kemudian dapat menggabungkan event halaman relasional dengan sub-event internal hub.

---

## 3. Spot Check Kelengkapan Fakta & Sumber (§3 Tindak Lanjut)

Berikut adalah mapping per baris untuk memastikan seluruh 23 halaman yang dilipat telah bermigrasi tanpa ada fakta atau sumber yang hilang:

### Tugas 1: 10 Halaman Polemik Ijazah Gibran
1. `2025-09-14-jokowi-berkumis-tipis-buka-bukaan-sekolah-gibran-singapura.md` → Fakta gugatan Subhan di PN Jakpus pindah ke entri `2025-09-08`; tanggapan santai Jokowi & sumber detikJabar pindah ke entri `2025-09-12`.
2. `2025-09-25-kepsek-pastikan-gibran-lulusan-smpn-1-solo.md` → Fakta klarifikasi kepsek Wuryanti atas cuitan dr. Tifa & sumber detikJateng pindah ke entri `2025-09-25`.
3. `2025-10-03-mdis-angkat-bicara-psi-minta-polemik-ijazah-gibran-disetop.md` → Fakta verifikasi diploma/sarjana MDIS & respons Sekjen PSI Andy Budiman beserta sumber detikNews pindah ke entri `2025-10-03`.
4. `2026-09-24-Jokowi-Ungkap-Riwayat-Sekolah-Gibran.md` → Fakta runut riwayat sekolah (SDN 16, SMPN 1, Orchid Park, UTS Insearch, MDIS), respons Raja Juli Antoni, & sumber detikNews pindah ke entri `2026-09-24`.
5. `2026-09-24-Tanggapan-Jokowi-Ijazah-Gibran-Disoal.md` → Fakta penegasan syarat diterima KPU & penolakan pembatalan pencalonan serta sumber detikSumut pindah ke entri `2026-09-24`.
6. `2026-09-30-bambang-widjojanto-minta-mk-panggil-gibran.md` → Fakta surat permohonan 28 Sep pindah ke entri `2026-09-28`; desakan pemanggilan Gibran oleh BW & sumber detikNews pindah ke entri `2026-09-30`.
7. `2026-09-30-sidang-gugatan-ijazah-gibran-hakim-mk-sorot-paket-c.md` → Fakta pertanyaan Hakim Enny Nurbaningsih soal Paket C & disparitas pasal UU Pemilu serta sumber detikNews pindah ke entri `2026-09-30`.
8. `2026-09-30-tentang-pkpu-disorot-hakim-mk-sidang-syarat-ijazah-gibran.md` → Fakta sorotan Hakim Saldi Isra atas norma Pasal 18 ayat 3 PKPU 19/2023 & sumber detikNews pindah ke entri `2026-09-30`.
9. `gugatan-ijazah-gibran.md` (stub tanpa tanggal) → Dilipat ke entri perdata `2025-09-08` dan pendaftaran sengketa konstitusi `2026-09-10`.
10. `gugatan-phpu-syarat-pendidikan-gibran-rakabuming-raka.md` (stub tanpa tanggal) → Dilipat ke entri pendaftaran PHPU `2026-09-10` dan registrasi perkara `2026-09-17`.

### Tugas 2: 13 Halaman Sepak Terjang Haji Isam
1. `2026-09-27-akuisisi-byan-jhonlin-tak-bebani-jarr.md` → Fakta independensi operasional & keuangan JARR dari transaksi BYAN serta sumber CNBC Indonesia pindah ke entri `2026-09-27`.
2. `2026-09-28-haji-isam-siapkan-duit-caplok-bca.md` → Fakta kalkulasi kapitalisasi pasar BBCA Rp756 T & sumber CNBC Indonesia pindah ke entri `2026-09-28`.
3. `2026-09-28-mirip-seperti-byan-awal-mula-rumor-haji-isam-caplok-bca.md` → Fakta kemiripan pola rumor medsos BBCA dengan BYAN & sumber CNBC Indonesia pindah ke entri `2026-09-28`.
4. `2026-09-29-ramai-ramai-akuisisi-emiten-september-haji-isam.md` → Fakta rekapitulasi akuisisi emiten September di BEI & sumber CNBC Indonesia pindah ke entri `2026-09-29`.
5. `2026-09-29-rumor-akuisisi-bca-haji-isam.md` → Fakta transaksi negosiasi 21,8 juta saham BBCA di BEI & sumber CNBC Indonesia pindah ke entri `2026-09-29`.
6. `BCA Bantah Isu Rumor Akuisisi Saham BBCA oleh Haji Isam.md` → Fakta bantahan resmi Hera F. Haryn & Jahja Setiaatmadja serta sumber Bloomberg Technoz pindah ke entri `2026-09-28`.
7. `BYAN Membantah Rencana Akuisisi oleh Haji Isam.md` → Fakta respon Corsec Jenny Quantero atas rumor 62,2% & saham limit-up Rp17.275 pindah ke entri `2026-08-18`.
8. `BYAN Negatif Outlook Setelah Isu Akuisisi oleh Haji Isam.md` → Fakta revisi outlook Moody's Ratings ke negatif akibat force majeure RKAB pindah ke entri `2026-09-18`.
9. `Haji Isam Akuisisi Saham Bayan Resources (BYAN).md` → Fakta pernyataan RKAB Bahlil, status HSC BEI, dan pencabutan force majeure pindah ke entri `2026-09-18` & `2026-09-26`.
10. `Haji Isam Borong BYAN via Jhonlin Baratama.md` → Fakta eksekusi pembelian 10 miliar lembar saham via PT Jhonlin Baratama pindah ke entri `2026-09-16` & `2026-09-17`.
11. `Haji Isam Selangkah Lagi Jadi Pemegang 10 Miliar Saham BYAN.md` → Fakta finalisasi kesepakatan CSPA 10.000.000.500 saham pindah ke entri `2026-09-16`.
12. `akuisisi-byan-oleh-haji-isam.md` → Fakta umum proses akuisisi pindah terdistribusi ke entri `2026-08-18` sampai `2026-09-17`.
13. `Akuisisi Bayan Resources oleh Haji Isam, Dari Rumor hingga Transaksi Resmi.md` → Narasi komprehensif (rumor limit up 18 Ags, pembicaraan tertutup 26 Ags, saham PGUN melonjak 2 Sep, tawaran tunai US$3 M Bloomberg 9 Sep, koreksi saham 14 Sep, CSPA 16 Sep, hingga keterbukaan BEI 17 Sep) pindah utuh ke entri kronologi Agustus–September 2026.

---

## 4. Penambahan Entri Pasca-Putusan MK (§4 Tindak Lanjut)

Telah ditambahkan entri baru pada Hub Polemik Ijazah Gibran:
- **`2026-10-07 — Reaksi Lintas Partai Pasca-Putusan MK dan Wacana Penggunaan Hak Angket DPR`**:
  Memuat respons penolakan dari koalisi KIM Plus/Sugiat Santoso (Gerindra) vs dorongan pembentukan Pansus Hak Angket oleh Deddy Sitorus (PDI Perjuangan) pasca-pertimbangan faktual ketiadaan bukti dokumen fisik ijazah SMA, ditautkan langsung ke halaman analisis `[[hak-angket-ijazah-gibran|Hak Angket Ijazah Gibran: Peluang dan Hambatan di DPR]]`.

---

## 5. Ringkasan Verifikasi Teknis

- **Orphan Relations:** 0
- **Broken Links:** 0
- **Duplicate Aliases:** 0
- **FTS Ranking `search("ijazah gibran")`:** Hub Polemik Ijazah Gibran menduduki peringkat #1, #2, dan #3 (score 36.92).
- **Quartz Build:** 341 files diproses, 989 files output, status [✅] Selesai (14 detik).
