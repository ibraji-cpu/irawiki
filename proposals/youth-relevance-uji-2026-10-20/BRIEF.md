# BRIEF — Uji Generator "Apa relevansinya dengan anak muda?" (Fase 1)

Tanggal brief: 2026-10-20
Konteks: revisi dari kritik user 2026-10-20 — section Gen Z tidak boleh jadi tempelan; relevansi harus diturunkan dari fakta halaman via rantai mekanisme yang tertelusur. Paket youth-relevance (hasil diskusi user + ChatGPT, 5 file markdown) adalah fondasi fase ini. Brief playbook halaman-rujukan DITAHAN — track ini yang jalan duluan; jika uji lolos, metodenya menjadi generator untuk section relevansi di playbook.

## 0. Setup (SUDAH SELESAI — jangan diulang, jangan diedit)

Repo: `/home/ubuntu/irawiki`, branch `konten/youth-relevance-uji-2026-10-20`.
Paket 5 file sudah disimpan VERBATIM (md5 cocok dengan sumber) di `docs/youth-relevance/` dan sudah di-commit (`e05a238`).

File sumber mentah (paket + halaman uji) tersedia di direktori kerja:
`/home/ubuntu/irawiki/proposals/youth-relevance-uji-2026-10-20/`

## 1. Peran masing-masing file (aturan keras)

- `youth-relevance-map.md` = referensi pengetahuan: untuk menghasilkan hipotesis/pertanyaan pemeriksaan (domain YR-01 s.d. YR-13). JANGAN menempel isi peta ke halaman hasil, JANGAN memperlakukannya sebagai bukti faktual.
- `youth-relevance-method.md` = instruksi generator: ikuti 7 langkah prosedur, standar editorial, aturan sebab-akibat, format keluaran (judul persis `## Apa relevansinya dengan anak muda?`, 1–3 paragraf).
- `youth-relevance-sources.md` = daftar awal, BUKAN tinjauan riset lengkap: klaim kausal harus tertelusur ke fakta halaman wiki itu sendiri atau sumber terverifikasi; jika tidak ada, klaim dipersempit atau tidak dibuat.
- `youth-relevance-test-cases.md` = rubrik evaluasi: 6 kasus uji + rubrik skor 0–2 × 7 aspek (maks 14).

## 2. Uji coba — 5 halaman yang sangat berbeda

Jalankan generator pada 5 halaman ini (salinan di direktori kerja di atas). Keluaran HANYA section `## Apa relevansinya dengan anak muda?` (1–3 paragraf).

**JANGAN edit halaman wiki-nya** — hasil uji dikumpulkan sebagai draf di laporan.

1. `perang-ultra-modern-dan-geopolitik.md` — makro/keuangan (uji rantai: indeks → portofolio ritel → biaya modal → lowongan).
2. `sepak-terjang-haji-isam.md` — jaringan korporasi-politik (kasus sulit: uji apakah LLM memaksa hubungan).
3. `uu-pelindungan-ketenagakerjaan-2026.md` — regulasi ketenagakerjaan (uji kasus upah: siapa tercakup, upah riil vs nominal).
4. `analisis-satgas-pkh-uang-vs-nilai.md` — angka fiskal (uji bedakan Rp52 T kas nyata vs Rp400 T valuasi).
5. `zainudin-hasan.md` — halaman aktor yang dominan biografis dan paling minim data dampaknya (pilihan tetap, sudah ditetapkan: stub 372 byte, tanpa relasi, tanpa data dampak). Uji kasus 6: aturan menahan diri. Jika hubungan tak tertelusur, section harus sangat terbatas atau tidak dibuat sama sekali. Catat alasan pemilihan.

## 3. Evaluasi (wajib untuk tiap hasil)

1. Skor rubrik: 7 aspek × 0–2 (maks 14). **Aspek bukti = 0 → klaim kausal GAGAL apa pun skor totalnya.**
2. Cek fabrikasi sebab-akibat: untuk setiap panah kausal, tulis dasarnya (fakta halaman / sumber terverifikasi / inferensi berlabel / tidak didukung). Tandai mata rantai tak didukung.
3. Cek tempelan: apakah section menjawab "mengapa" via mekanisme spesifik, atau hanya parafrase generik?

## 4. Laporan (TUNGGU persetujuan user sebelum langkah apa pun setelah ini)

Isi laporan:
- konfirmasi paket tersimpan (path, jumlah file, md5, commit);
- per halaman uji — section verbatim + skor per aspek + status dukungan tiap mata rantai + penilaian;
- temuan pola (di mana LLM cenderung memfabrikasi/menempel, apakah method perlu pengetatan);
- rekomendasi rollout.

Simpan laporan sebagai file markdown di:
`/home/ubuntu/irawiki/proposals/youth-relevance-uji-2026-10-20/LAPORAN-UJI-FASE1.md`
Lalu laporkan ringkasan ke parent + path file.

**JANGAN terbitkan section ke halaman. JANGAN mulai retrofit massal. JANGAN edit file paket.**

## 5. Definisi selesai Fase 1

Paket berversi di repo; 5 section uji + skor + audit kausalitas terdokumentasi; rekomendasi diajukan; menunggu keputusan user.
