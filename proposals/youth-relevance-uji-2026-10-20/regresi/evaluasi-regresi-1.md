---
title: "Evaluasi Regresi v1.1 — 2 Halaman Uji"
type: evaluation
status: draft
method: youth-relevance-method v1.1
rubrik: youth-relevance-test-cases.md v1.1
tanggal: 2026-10-20
---

# Evaluasi Regresi v1.1

Uji regresi setelah pengetatan method v1.1. Dua halaman, dua jenis tekanan berbeda: satu halaman padat dengan fakta berstatus campuran (provenance), satu halaman stub kosong (abstain).

## Ringkasan skor

| Halaman | Keluaran | Skor | Putusan |
|---|---|---|---|
| `uu-pelindungan-ketenagakerjaan-2026.md` | section 3 paragraf | **13/14** | layak ditinjau editor |
| `zainudin-hasan.md` | **abstain** (2 paragraf pendek) | bukti **2**, aspek lain `N/A` | **abstain — benar** |

## 1. uu-pelindungan-ketenagakerjaan-2026.md

Kasus: Kasus 3 (perburuhan) + Kasus 7 (fakta draf / belum diundangkan).

| Aspek | Skor | Alasan |
|---|---|---|
| Kekhususan kelompok | 2 | Pekerja kontrak PKWT, pekerja alih daya di enam bidang jasa penunjang, pekerja platform digital. Bukan "anak muda" abstrak. |
| Mekanisme | 2 | Dua rantai terpisah: (a) batas PKWT dalam draf → kalau diundangkan, dasar hukum pekerja kontrak berubah; (b) Permenaker 7/2026 → pembatasan bidang alih daya → pekerja di bidang itu terkena sekarang. |
| Bukti | 2 | Tiap mata rantai bisa ditelusuri ke badan halaman; tidak ada angka atau klaim baru di luar halaman. |
| Waktu | 2 | Status pengundangan dan tenggat "2 tahun sejak diundangkan" dibedakan; dinyatakan tenggat belum berjalan. |
| Ketidakpastian | 2 | Tiga tingkat dipisah eksplisit: belum diundangkan, draf, klaim pihak. |
| Keseimbangan | 1 | Risiko dan konteks ada (peringatan Apindo soal pekerja informal, klaim serikat), tetapi sisi peluang/manfaat bagi pekerja muda tidak dikembangkan — hanya tersirat. Satu-satunya pengurangan. |
| Keterbacaan | 2 | Mengalir, tanpa jargon berlebih, tanpa formulir "jalur/kelompok/waktu". |
| **Total** | **13** | Dari maksimum 14 (seluruh aspek berlaku). |

### Aturan baru — diperiksa satu per satu

- **Provenance disebut eksplisit: ya.** Empat status muncul di badan tulisan: "belum diundangkan" (pengesahan 6 Oktober 2026), "draf RUU dan pemberitaan" (batas PKWT, pesangon), "sudah berlaku" (Permenaker 7/2026), "klaim pihak" (FSP KEP SPSI 95–96 persen; keberatan Apindo). Tidak ada kenaikan status: frasa "belum ada dasar untuk mengatakan bahwa mereka sudah memperoleh hak baru" secara langsung menolak pembacaan draf sebagai hak berlaku.
- **Arus kas vs valuasi stok: tidak berlaku** (halaman tidak memuat angka fiskal/valuasi). Tidak ada penjumlahan lintas jenis angka.
- **Dua periode digabung: tidak terjadi.** Pengesahan 6 Oktober 2026 dan putusan MK disebut sebagai dua peristiwa berbeda dengan perannya masing-masing; tidak ada narasi "bersamaan".
- **Klaim dari `## Kenapa penting buat Gen Z` tidak diwarisi: ya, bersih.** Section lama menyebut "tiga hal yang langsung terasa pada tahun-tahun pertama bekerja" dan memakai angka 95–96 persen sebagai fakta pendukung. Keluaran ini tidak memakai frasa "langsung terasa", dan angka 95–96 persen hanya muncul sebagai klaim pihak di paragraf ketiga. Rincian PKWT diambil dari bagian "Poin Substansi yang Beredar" (yang berlabel provenance) plus catatan presisi, bukan dari section Gen Z.
- **Abstain tidak dipakai** — halaman menyediakan cukup fakta untuk minimal dua panah yang berdasar. Itu keputusan yang benar menurut Langkah 5, bukan pelanggaran aturan abstain.

## 2. zainudin-hasan.md

Kasus: Kasus 6 + aturan abstain.

Halaman sumber 372 byte: frontmatter (`status: stub`, `relasi: []`) dan judul `# Zainudin Hasan`. Tidak ada badan artikel — nol fakta tentang jabatan, afiliasi, kebijakan, atau peristiwa.

| Aspek | Skor | Alasan |
|---|---|---|
| Bukti | 2 | Satu-satunya pernyataan — "halaman belum memuat uraian di luar judul dan metadata" — dapat diverifikasi langsung dari isi halaman. |
| Kekhususan kelompok | `N/A` | Tidak ada kelompok yang bisa diidentifikasi tanpa mengarang. |
| Mekanisme | `N/A` | Tidak ada bahan untuk rantai mekanisme. |
| Waktu | `N/A` | Tidak ada peristiwa bertanggal di badan halaman. |
| Ketidakpastian | `N/A` | Tidak ada klaim yang perlu ditandai. |
| Keseimbangan | `N/A` | Tidak ada klaim risiko maupun manfaat. |
| Keterbacaan | `N/A` | Abstain dinilai lewat aspek bukti saja. |

**Putusan: abstain — benar.** Keluaran menyatakan apa yang tidak tersedia dan tidak mengarang kelompok, mekanisme, maupun horizon waktu. Tidak ada "kelompok anak muda yang terpapar kebijakan X" atau "dampaknya akan terasa dalam 5 tahun" — dua jenis karangan yang paling mudah muncul di halaman stub.

## Catatan untuk method

1. **Aturan provenance bekerja, tetapi hanya karena fakta halaman sudah diberi label.** Halaman UU ini luar biasa rapi: frontmatter memuat `status: "Disahkan, belum diundangkan"`, ada bagian "Peringatan provenance", dan catatan presisi menyebut "seluruh rincian pasal masih merujuk draf RUU". Generator bisa mengutip label yang sudah ada. Pada halaman yang mencampur draf dan fakta berlaku **tanpa** label semacam itu, beban penilaian jatuh sepenuhnya pada Langkah 1 — dan di situ belum ada bukti bahwa generator akan konsisten. Uji berikutnya sebaiknya memakai halaman dengan provenance campuran yang tidak dilabeli.
2. **Aturan abstain membantu, tetapi rubriknya masih bisa disalahbaca.** "Bukti 2, sisanya N/A" menghasilkan putusan benar, namun tidak ada angka yang bisa dibandingkan dengan halaman lain. Untuk pelaporan agregat, sebaiknya abstain dicatat terpisah dari skala 14, bukan diberi total semu.
3. **Keseimbangan adalah aspek paling rapuh** pada halaman regulasi. Ketika status hukum belum pasti, semua kalimat cenderung menjadi peringatan; peluang (mis. kepastian kontrak bila UU berlaku) mudah hilang.
