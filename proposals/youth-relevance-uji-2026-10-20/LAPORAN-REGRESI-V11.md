# Laporan Regresi — Method v1.1

**Tanggal:** 20 Oktober 2026 · **Repo:** `/home/ubuntu/irawiki` · **Branch:** `konten/youth-relevance-uji-2026-10-20`
**Tujuan:** membuktikan empat pengetatan method v1.1 benar-benar dijalankan generator, bukan hanya tertulis di dokumen.
**Model subagen:** `tig/deepseek-v4-1-flash-UNRESTRICTED` (provider `trustisgold`)
**Status:** pengetatan lolos uji; tidak ada halaman wiki yang diubah.

---

## 1. Yang diuji

Empat pengetatan v1.1 diuji pada 4 halaman — dua pasangan yang paling rawan:

| Pasangan | Halaman | Yang diuji |
|---|---|---|
| A | `uu-pelindungan-ketenagakerjaan-2026.md` | status provenance (fakta masih draf / belum diundangkan) |
| A | `aktor/zainudin-hasan.md` | aturan abstain pada halaman stub |
| B | `perang-ultra-modern-dan-geopolitik.md` | pemisahan dua periode; pemotongan rantai biaya modal → lowongan |
| B | `analisis/analisis-satgas-pkh-uang-vs-nilai.md` | larangan menjumlahkan arus kas dengan valuasi stok |

---

## 2. Hasil

| Halaman | Fase 1 | Regresi v1.1 | Perubahan isi |
|---|---|---|---|
| perang-ultra-modern-dan-geopolitik | 14 | **14** | 7 label provenance eksplisit; dua periode dipisah dengan kalimat penolak "bukan satu kejadian"; rantai biaya modal → lowongan tetap dipotong |
| uu-pelindungan-ketenagakerjaan-2026 | 13 | **13** | 4 tingkat provenance dipisah (belum diundangkan / draf / berlaku / klaim pihak); Permenaker 7/2026 dibedakan dari UU |
| analisis-satgas-pkh-uang-vs-nilai | 10 | **10** | 6 label provenance; Rp52 T dan ~Rp400 T tidak dijumlahkan; selisih Rp0,02 T tidak diisi taksiran |
| aktor/zainudin-hasan | 7 (salah label) | **abstain — benar** (bukti 2, aspek lain `N/A`) | abstain kini dicatat benar, bukan "tulis ulang" |

**Tidak ada penurunan skor.** Yang berubah isi, bukan angka: label provenance muncul di setiap fakta, dan dua klaim pihak (Rp400 T; 6,2 juta ha) yang di Fase 1 hanya tersirat dari Catatan presisi kini dilabeli eksplisit.

### Kasus 1 — provenance per fakta (contoh bukti aturan baru bekerja)

| Fakta | Status | Label di section |
|---|---|---|
| IHSG −11,57%; halt 30 menit; net sell 3 bank | berlaku, terverifikasi | "berstatus terverifikasi lintas media" (Reuters, Securities.io, Bulatan Times) |
| Konsultasi MSCI; status EM sampai ≤30 Jun 2027 | berlaku | "ini fakta terverifikasi" |
| Rupiah Rp18.033/USD, 4 Jun 2026 | berlaku | "rekor penutupan terendah saat itu" |
| PP 21/2026 (DHE SDA) | berlaku sejak 1 Jun 2026 | "sudah berlaku sejak 1 Juni 2026" |
| PP 26/2026 (kanal tunggal DSI) | berlaku bertahap, penuh Jan 2027 | "baru penuh Januari 2027" — tidak diperlakukan sebagai berlaku penuh |
| Konten "Indonesia is Collapsing!!!!" #1M65 | klaim pihak, belum terverifikasi | "berstatus klaim pihak … identitas naratornya belum terverifikasi" |

Semua label itu terverifikasi ada di halaman sumber (baris Sumber & Catatan presisi halaman) — tidak ada karangan.

### Kasus 3 — provenance campuran

Status dipisah tegas: pengesahan DPR 6 Okt 2026 **belum diundangkan**; rincian PKWT/pesangon **draf**; Permenaker 7/2026 **berlaku** (satu-satunya); angka 95–96% dan keberatan Apindo **klaim pihak**. Tidak ada kenaikan status draf menjadi hak berlaku.

### Kasus 4 — arus kas vs valuasi

Tidak ada angka gabungan (tidak muncul "Rp452 triliun"). Rp52 T dilabeli arus kas, ~Rp400 T dilabeli klaim valuasi presiden, dan keduanya dinyatakan tidak boleh dijumlahkan. Alokasi APBN tidak ditelusuri → panah ke belanja anak muda dipotong.

### Kasus 6 — abstain

Halaman stub 372 byte. Keluaran abstain 2 paragraf pendek, aspek bukti 2, aspek lain `N/A`. Tidak mengarang kelompok, mekanisme, maupun horizon waktu.

---

## 3. Verifikasi silang (parent)

- Angka dan status yang dipakai subagen dicek ulang terhadap halaman sumber: `1M65`, `Reuters`, `Bulatan Times`, `Collapsing`, PP 21/2026, PP 26/2026, Rp52 T, Rp400 T, Rp13,24 T, Rp0,02 T, 6,2 juta ha — **semuanya ada** di halaman.
- `git status` repo hanya menunjukkan `proposals/youth-relevance-uji-2026-10-20/`; **nol perubahan di `content/`**.
- Tidak ada file paket yang diubah oleh subagen (method/test-cases pakai salinan v1.1 di `regresi/`).

---

## 4. Temuan

1. **Pengetatan bekerja.** Keempat aturan v1.1 terlihat di keluaran: provenance dilabeli, dua periode dipisah, arus kas tidak dijumlahkan dengan valuasi, dan section lama `## Kenapa penting buat Gen Z` tidak diwarisi. Di kasus 1, tiga kelonggaran section lama ("tiga tekanan datang bersamaan", "menyentuh biaya hidup harian", "langsung mengurangi nilai portofolio") ditolak satu per satu.
2. **Uji provenance kasus 3 lolos sebagian karena halaman sudah melabeli statusnya sendiri** (frasa "Disahkan, belum diundangkan" + bagian "Peringatan provenance"). Aturan v1.1 belum terbukti pada halaman campuran **tanpa** label — itu kandidat uji berikutnya.
3. **Skor kasus 4 tertahan di 10, dan itu benar.** Rubrik menghukum ketiadaan mekanisme dan horizon, padahal halaman memang tidak menyediakannya. Memaksa skor lebih tinggi berarti mengarang mekanisme fiskal — persis yang dilarang.
4. **Abstain sebaiknya dicatat terpisah dari skala 14.** "Bukti 2, sisanya N/A" menghasilkan putusan benar, tapi tidak ada angka yang bisa dibandingkan antar-halaman. Untuk pelaporan agregat, pisahkan abstain dari skala 14.
5. **Satu pelanggaran format, bukan substansi.** Subagen regresi B menulis tabel audit internal di bawah section pada dua berkas — method v1.1 melarang menampilkan proses analisis internal di hasil. Isi section-nya sah; berkas itu dipindah ke `regresi/audit-mentah/` dengan catatan, dan keluaran bersih ada di `regresi/hasil-regresi-*.md`.
6. **Satu inkonsistensi angka self-report.** Ringkasan chat subagen B menyebut kasus 1 = 13 dan kasus 4 = 12, sedangkan berkas evaluasinya sendiri menyebut 14 dan 10 dengan tabel rekap + delta Fase 1 yang konsisten. Laporan ini memakai angka dari berkas evaluasi (yang bisa diaudit), bukan dari ringkasan chat.

---

## 5. Status pengetatan

- Method v1.1: **lulus uji regresi** — commit `fa5d971`.
- Test-cases v1.1 (Kasus 7–8 + aturan abstain): **dipakai dan berfungsi** — commit `fa5d971`.
- Rekomendasi sebelumnya poin 2 (pengetatan method) **selesai dan terverifikasi**.

Langkah berikutnya menunggu keputusan user: **rollout batch bertahap** (usulan dimulai dari kategori `analisis`), atau tambahan uji provenance pada halaman tanpa label status.
