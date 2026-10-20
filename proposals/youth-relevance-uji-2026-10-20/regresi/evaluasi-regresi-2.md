# Evaluasi Regresi 2 — Method v1.1

Tanggal: 2026-10-20
Ruang lingkup: dua halaman uji regresi setelah pengetatan method ke v1.1 — `perang-ultra-modern-dan-geopolitik` dan `analisis-satgas-pkh-uang-vs-nilai`.
Dasar: `youth-relevance-method.md` v1.1 (Langkah 1 provenance, Langkah 4 aturan angka, pemeriksaan akhir no. 9–11) dan `youth-relevance-test-cases.md` v1.1 (rubrik 7 aspek × 0–2, maks 14).
Bahan: hanya fakta di dalam salinan halaman pada direktori `regresi/`. Tidak ada halaman wiki (`content/`) atau file paket yang diubah.

Tujuan khusus regresi: memastikan empat pengetatan v1.1 benar-benar dijalankan, bukan hanya tertulis di method.

---

## Kasus 1 — `perang-ultra-modern-dan-geopolitik.md`

Berkas hasil: `regresi/hasil-regresi-perang-ultra-modern-dan-geopolitik.md` (3 paragraf, 375 kata).

### Skor rubrik

| Aspek | Skor | Alasan |
|---|---|---|
| Kekhususan kelompok | 2 | Kelompok = pemegang saham/reksa dana dalam cakupan IHSG; eksposur dinyatakan, ketiadaan data kepemilikan ritel dan komposisi usia disebut. |
| Mekanisme | 2 | Rantai indeks → nilai portofolio utuh; rantai biaya pendanaan → belanja modal → perekrutan dipotong dan pemotongannya dinyatakan. |
| Bukti | 2 | Tiap mata rantai bertumpu pada angka halaman (16 Okt 2026, net sell tiga bank, tanggal MSCI, kurs 4 Jun, PP 21/2026). Bagian tanpa dasar tidak diklaim. |
| Waktu | 2 | Aktual (4 Jun 2026; 16 Okt 2026) dipisah dari bersyarat (putusan MSCI ≤ 30 Jun 2027) dan dari yang baru penuh berlaku (PP 26/2026, Jan 2027). |
| Ketidakpastian | 2 | Transmisi kurs → harga eceran disebut inferensi, bukan pengukuran; status *Emerging Market* selama konsultasi disebut. |
| Keseimbangan | 2 | Risiko (portofolio, barang impor) berpasangan dengan konteks (kegiatan riil berjalan, ruang perbaikan tata kelola, tipologi sebagai kerangka). |
| Keterbacaan | 2 | Tiga paragraf mengalir, tanpa subjudul internal, tanpa tumpukan angka. |
| **Total** | **14** | Layak ditinjau editor. |

### Status provenance tiap fakta (Langkah 1 v1.1)

| Fakta yang dipakai | Status | Label di section |
|---|---|---|
| IHSG −11,57% ke 5.185,11; halt 30 menit; net sell BBCA/BBRI/BMRI (16 Okt 2026) | Berlaku — terverifikasi lintas media (Catatan presisi) | "berstatus terverifikasi lintas media" + tiga rujukan disebut |
| Konsultasi MSCI 15 Okt 2026; status EM sampai putusan ≤ 30 Jun 2027 | Berlaku — fakta terverifikasi | "ini fakta terverifikasi" |
| Rupiah Rp18.033/USD, 4 Jun 2026 | Berlaku — angka penutupan, rekor saat itu | "berstatus rekor penutupan terendah saat itu" |
| PP 21/2026 (DHE SDA) | Berlaku sejak 1 Jun 2026 | "sudah berlaku sejak 1 Juni 2026" |
| PP 26/2026 (kanal tunggal DSI) | Berlaku bertahap — penuh Januari 2027 | "baru penuh Januari 2027" (tidak diperlakukan sebagai berlaku penuh) |
| Konten "Indonesia is Collapsing!!!!" tag 1M65 | Klaim pihak + belum terverifikasi | "berstatus klaim pihak … identitas naratornya belum terverifikasi" |
| Tipologi tiga jenis perang | Kerangka penulis, bukan kategori baku | "kerangka penulis — alat baca, bukan kategori baku" |

Tidak ada fakta berstatus draf di halaman ini, sehingga uji "disahkan, belum diundangkan" tidak terpakai di kasus 1 (itu milik kasus 3/UU Naker).

### Audit mata rantai

| # | Panah | Dasar | Status |
|---|---|---|---|
| A1 | IHSG −11,57% (16 Okt 2026) → nilai portofolio pemegang turun | Fakta halaman | **Ditulis** — konsekuensi aritmetis harga |
| A2 | Data kepemilikan ritel → besar kelompok terdampak | Tidak ada di halaman | **Tidak diklaim**; dinyatakan tidak terukur |
| A3 | MSCI turun kelas → dana pengikut indeks keluar → biaya pendanaan naik | Fakta halaman + mekanisme rebalancing (pengetahuan umum) | **Ditulis bersyarat** ("jika keputusan itu nanti …") |
| A4 | Biaya modal naik → belanja modal turun → lowongan berkurang | Halaman tidak memuat biaya modal, capex, atau perekrutan | **DIPOTONG**, dan pemotongan dinyatakan di badan paragraf |
| A5 | Kurs 4 Jun 2026 → barang impor lebih mahal → biaya hidup | Fakta halaman untuk kurs; transmisi = inferensi | **Ditulis sebagai potensi**, tanggal dipisah tegas |
| A6 | PP 21/2026 & PP 26/2026 → dampak ke pemuda | Realisasi DHE dan dampak DSI belum tersedia | **Tidak ditulis** (benar) |

### Uji aturan baru

- **Provenance:** ya. Tujuh fakta dipakai, tujuh diberi status — termasuk dua yang paling mudah dilonggarkan (PP 26/2026 yang belum penuh berlaku, dan konten 1M65 yang masih klaim pihak).
- **Dua periode dipisah:** ya, eksplisit. Kalimat penutup paragraf ketiga menyebut 4 Juni 2026 dan 16 Oktober 2026 sebagai "bukan satu kejadian".
- **Arus kas vs valuasi:** tidak berlaku di halaman ini (tidak ada angka valuasi aset). Tidak ada penjumlahan jenis angka.
- **Tak mewarisi section lama:** ya. Bagian `## Kenapa penting buat Gen Z` halaman ini memuat tiga kelonggaran: "tiga tekanan datang bersamaan sepanjang 2026", "pelemahan rupiah menyentuh biaya hidup harian", dan "penurunan IHSG … langsung mengurangi nilai portofolio". Ketiganya tidak diwarisi — yang pertama ditolak dengan pemisahan tanggal, yang kedua diturunkan menjadi inferensi berlabel, yang ketiga dipertahankan hanya untuk pemegang instrumen dan tanpa kata "langsung".

---

## Kasus 4 — `analisis-satgas-pkh-uang-vs-nilai.md`

Berkas hasil: `regresi/hasil-regresi-analisis-satgas-pkh-uang-vs-nilai.md` (3 paragraf, 295 kata).

### Skor rubrik

| Aspek | Skor | Alasan |
|---|---|---|
| Kekhususan kelompok | 1 | "Pembaca muda yang mengikuti debat defisit dan belanja publik" — kelompok disebut, eksposurnya epistemis dan tidak terukur. |
| Mekanisme | 1 | Tidak ada mekanisme dampak material; yang dijelaskan hanya mekanisme membaca angka dan komposisi penerimaan. Ini batas halaman, bukan kelalaian. |
| Bukti | 2 | Semua angka dari halaman; tiap label dasar angka (kas / valuasi / pemberitaan / klaim pihak) tertelusur ke Fakta kunci dan Catatan presisi. |
| Waktu | 1 | Tanggal tahap VIII (6 Okt 2026) jelas; horizon dampak tidak dapat ditetapkan karena pembentukan Satgas tidak bertanggal. |
| Ketidakpastian | 2 | Selisih Rp0,02 T, alokasi APBN, dan pengawasan DPR dinyatakan sebagai celah, bukan diisi taksiran. |
| Keseimbangan | 1 | Netral dan simetris ("tidak ada dasar menyebut menguntungkan, juga tidak ada dasar menyebut merugikan"), tetapi tanpa peluang konkret. |
| Keterbacaan | 2 | Jelas, angka diberi label dasar sehingga tidak menumpuk. |
| **Total** | **10** | Perlu perbaikan menurut rubrik — skor tertahan oleh keterbatasan halaman, bukan oleh pelanggaran aturan. |

### Status provenance tiap fakta

| Fakta | Status | Label di section |
|---|---|---|
| ~Rp52 T kas, 8 tahap; tahap VIII Rp13,24 T (6 Okt 2026) | Berlaku — angka yang diumumkan | "kas yang benar-benar diserahkan dalam delapan tahap" |
| Komposisi Rp8,22 T pajak + Rp3,47 T denda + Rp1,53 T PNBP | Berlaku — rincian diumumkan | disebut dengan label jenis penerimaan |
| "Hampir Rp400 T" nilai lahan | **Klaim pihak** (pernyataan Presiden) | "klaim valuasi lahan oleh Presiden — bukan kas, bukan hasil penjualan aset" |
| 140.762,04 ha dikelola Agrinas | Angka halaman; status kelembagaan Agrinas belum diverifikasi | disebut sebagai luas yang dikelola, tanpa mengklaim status BUMN |
| 259.230 ha disita | Pemberitaan media | "menurut pemberitaan" |
| 6,2 juta ha "diselamatkan" | **Klaim pihak** | "klaim pihak, bukan pengukuran" |
| Selisih Rp0,02 T | Celah tak dijelaskan sumber | "belum dijelaskan sumber mana pun dan tidak diisi taksiran" |

### Audit mata rantai

| # | Panah | Dasar | Status |
|---|---|---|---|
| B1 | Rp52 T = kas; Rp400 T = valuasi → dua basis berbeda | Catatan presisi butir 2 | **Ditulis sebagai pemisahan tegas**, tanpa angka gabungan |
| B2 | Komposisi tahap VIII dominan pajak → *revenue recovery*, bukan *asset recovery* | Perspektif 1–2 halaman | **Ditulis**, angka tertelusur |
| B3 | Membedakan kas vs valuasi → pembaca tidak salah mengutip | Sifat angka | **Ditulis sebagai kegunaan**, bukan klaim dampak terukur |
| B4 | Rp52 T → manfaat fiskal bagi anak muda | Alokasi APBN tidak ditelusuri | **Tidak dibuat**; dinyatakan tidak ada dasar, dua arah (untung dan rugi) |
| B5 | 140.762,04 ha → produktivitas menentukan penerimaan lanjutan | Perspektif 3 + Celah data | **Ditulis sebagai pertanyaan terbuka** |
| B6 | Rp52 T + Rp400 T = "Rp452 T" | Dilarang halaman dan method | **Tidak ada** — nol kemunculan angka gabungan di berkas hasil |

### Uji aturan baru

- **Provenance:** ya. Tujuh fakta, tujuh label; dua di antaranya adalah klaim pihak yang sebelumnya bisa lolos sebagai fakta ("hampir Rp400 T", "6,2 juta ha").
- **Arus kas vs valuasi:** ya, dan eksplisit. Kalimat "Menjumlahkan keduanya hanya menghasilkan angka yang tidak pernah ada" menggantikan risiko peleburan; tidak ada satu pun angka turunan gabungan.
- **Dua periode:** tidak berlaku — halaman hanya punya satu tanggal peristiwa (6 Okt 2026), tanpa dua periode yang bisa digabung.
- **Tak mewarisi section lama:** tidak ada klaim lama yang dilanggar di sini. Section lama halaman ini (`## Kenapa penting buat Gen Z`) memang sudah memisahkan kas dan valuasi, tetapi memakai "pembaca muda" tanpa eksposur terukur dan menyebut manfaat secara lebih longgar. Section baru menurunkan klaim itu menjadi kegunaan membaca angka dan menambah label provenance yang tidak ada di section lama. Jadi aturan 4 di kasus 4 bersih karena tidak ada yang perlu ditolak, bukan karena aturan tidak diuji.

---

## Rekap dan delta terhadap Fase 1

| Halaman | Kekhususan | Mekanisme | Bukti | Waktu | Ketidakpastian | Keseimbangan | Keterbacaan | Total | Fase 1 | Delta |
|---|---|---|---|---|---|---|---|---|---|---|
| Kasus 1 — Perang Ultra Modern | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **14** | 14 | 0 |
| Kasus 4 — Satgas PKH | 1 | 1 | 2 | 1 | 2 | 1 | 2 | **10** | 10 | 0 |

Tidak ada penurunan skor. Yang berubah adalah isi, bukan angka: tiga paragraf kasus 1 kini memuat tujuh label provenance, dan kasus 4 memuat enam label termasuk dua klaim pihak yang di Fase 1 hanya tersirat dari Catatan presisi.

## Status keempat pengetatan v1.1

| Aturan | Kasus 1 | Kasus 4 | Bukti |
|---|---|---|---|
| 1. Status provenance tiap fakta | Dijalankan | Dijalankan | 7 dan 7 fakta berlabel; dua klaim pihak dan satu aturan belum-penuh-berlaku dilabeli eksplisit |
| 2. Arus kas tidak dijumlahkan dengan valuasi | N/A (tak ada angka valuasi) | Dijalankan | Tidak ada angka gabungan di berkas; pemisahan dinyatakan dalam kalimat |
| 3. Dua periode tidak digabung | Dijalankan | N/A (satu tanggal) | "4 Juni 2026 … 16 Oktober 2026 … bukan satu kejadian" |
| 4. Tidak mewarisi section lama | Dijalankan | Bersih (tak ada klaim lama yang perlu ditolak) | Tiga kelonggaran `## Kenapa penting buat Gen Z` tidak muncul di section baru |
| 5. Abstain sebagai keluaran benar | Tidak terpakai | Tidak terpakai | Tidak ada halaman stub di batch regresi ini; aturan ini hanya teruji di Fase 1 kasus 6 |

## Catatan

1. **Yang paling terasa berubah adalah disiplin label, bukan panjang.** Kedua section tetap 3 paragraf (375 dan 295 kata), tetapi setiap angka kini membawa dasar: terverifikasi, berlaku bertahap, klaim pihak, pemberitaan, atau kerangka penulis. Ini menutup celah yang di Fase 1 ditemukan pada kasus 3 (draf diperlakukan sebagai berlaku).
2. **Skor 10 di kasus 4 bukan regresi dan bukan pelanggaran.** Rubrik menghukum ketiadaan mekanisme dan horizon, sedangkan halaman memang tidak menyediakannya. Memaksakan skor lebih tinggi berarti mengarang mekanisme fiskal — persis yang dilarang Langkah 4 dan rubrik Kasus 8.
3. **Aturan 2 dan 3 saling mengunci di halaman berbeda.** Halaman Perang Ultra Modern adalah tempat aturan dua-periode diuji; halaman Satgas PKH adalah tempat aturan kas-vs-valuasi diuji. Tidak ada satu halaman yang menguji keduanya sekaligus, sehingga batch regresi ini tidak membuktikan keduanya bisa dijalankan bersamaan dalam satu section.
4. **Sisa risiko:** halaman yang memuat angka valuasi **dan** dua periode sekaligus belum diuji; di situ dua aturan harus aktif bersamaan dan belum ada bukti generator menahannya tanpa saling mengganggu keterbacaan.

## Berkas

- Section: `regresi/hasil-regresi-perang-ultra-modern-dan-geopolitik.md`, `regresi/hasil-regresi-analisis-satgas-pkh-uang-vs-nilai.md`
- Evaluasi ini: `regresi/evaluasi-regresi-2.md`
