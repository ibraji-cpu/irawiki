# Laporan Uji Fase 1 — Generator "Apa relevansinya dengan anak muda?"

**Tanggal:** 20 Oktober 2026 · **Repo:** `/home/ubuntu/irawiki` · **Branch:** `konten/youth-relevance-uji-2026-10-20`
**Model subagen:** `tig/deepseek-v4-1-flash-UNRESTRICTED` (provider `trustisgold`)
**Status:** 5 halaman uji selesai; laporan ini menunggu keputusan user. Tidak ada halaman wiki yang diubah.

---

## 1. Konfirmasi paket tersimpan (sumber tunggal, berversi)

Path: `docs/youth-relevance/` · Commit: `e05a238` ("konten: paket relevansi anak muda (verbatim, fase 1 uji generator)")
Isi: 5 file, **925 baris, 45.027 byte**, disimpan VERBATIM (tanpa edit) dari berkas sumber user.

| File | Byte | md5 | Cocok sumber |
|---|---|---|---|
| README.md | 1.974 | `9987a6e7176d5e54859c453a458f28da` | ya |
| youth-relevance-map.md | 20.823 | `97088c9e17c03e032908732e1a3296af` | ya |
| youth-relevance-method.md | 7.459 | `4bb5f1921c6c0ea9132ab81dccc1edfd` | ya |
| youth-relevance-sources.md | 7.373 | `2bcafa52c177c6ea4df9446840074b4a` | ya |
| youth-relevance-test-cases.md | 6.691 | `9fbb5468987b9d7447a08e4e86680f7c` | ya |

File kerja + brief + hasil + evaluasi ada di `proposals/youth-relevance-uji-2026-10-20/` (belum di-commit).

---

## 2. Hasil per halaman uji

Skor rubrik 7 aspek × 0–2 (maks 14). Aturan: **aspek bukti = 0 → klaim kausal GAGAL apa pun totalnya.**

| # | Halaman | Kelompok | Mekan. | Bukti | Waktu | Ketidakpastian | Seimbang | Baca | **Total** | Interpretasi |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | perang-ultra-modern-dan-geopolitik | 2 | 2 | 2 | 2 | 2 | 2 | 2 | **14** | layak ditinjau editor |
| 2 | peristiwa/sepak-terjang-haji-isam | 2 | 1 | 2 | 2 | 2 | 1 | 2 | **12** | layak ditinjau editor |
| 3 | uu-pelindungan-ketenagakerjaan-2026 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | **13** | layak ditinjau editor |
| 4 | analisis/analisis-satgas-pkh-uang-vs-nilai | 1 | 1 | 2 | 1 | 2 | 1 | 2 | **10** | perlu perbaikan |
| 6 | aktor/zainudin-hasan | 0 | 0 | 2 | 0 | 2 | 1 | 2 | **7** | lihat temuan 4 |

**Tidak ada aspek bukti = 0.** Tidak ada klaim kausal yang gagal total.

### 2.1 Kasus 1 — `perang-ultra-modern-dan-geopolitik.md` (14/14)

Section verbatim:

> ## Apa relevansinya dengan anak muda?
>
> Yang paling langsung: anak muda yang memegang saham atau reksa dana yang isinya masuk cakupan IHSG. Pada 16 Oktober 2026 indeks turun 11,57% ke 5.185,11 dan perdagangan sempat dihentikan 30 menit, dengan penjualan bersih asing terkonsentrasi di saham bank (BBCA Rp2,3 triliun, BBRI Rp1,15 triliun, BMRI Rp868 miliar). Bagi pemegang instrumen itu, nilai portofolio ikut turun pada hari tersebut. Halaman tidak memuat data kepemilikan ritel, jadi besar kelompoknya dan porsi anak muda di dalamnya belum bisa diukur; yang bisa dikatakan hanya bahwa eksposur itu ada pada mereka yang memegang produk terkait.
>
> Jalur berikutnya lebih panjang dan tidak selesai di halaman ini. Konsultasi MSCI yang dibuka 15 Oktober 2026 mengusulkan penurunan Indonesia dari *Emerging Market* ke *Standalone Market*, dengan keputusan paling lambat 30 Juni 2027, dan status Indonesia tetap *Emerging Market* selama masa konsultasi. Jika keputusan itu nanti berupa penurunan, dana yang mengikuti indeks negara berkembang berhenti memasukkan saham Indonesia, dan itu bisa menaikkan biaya pendanaan perusahaan. Halaman tidak punya bukti untuk mata rantai setelahnya: tidak ada data biaya modal, belanja modal, atau perekrutan. Karena itu klaim bahwa penurunan indeks mengurangi lowongan kerja tidak bisa ditulis dari halaman ini.
>
> Untuk biaya hidup, halaman mencatat rupiah ditutup Rp18.033 per dolar AS pada 4 Juni 2026 — periode yang berbeda dari jatuhnya indeks pada Oktober, jadi keduanya tidak bisa digabung sebagai satu peristiwa. Halaman menyebut kurs dipakai menghitung harga barang impor, sehingga barang dengan komponen impor berpotensi lebih mahal; seberapa besar kenaikan itu diteruskan ke harga eceran tidak diukur di sini. Sisi lainnya, halaman juga mencatat kegiatan riil seperti pabrik, pertanian, perdagangan, dan hilirisasi tidak berhenti, dan masa konsultasi sampai April 2027 menyisakan ruang untuk perbaikan tata kelola pasar.

Audit kausalitas (tiap panah):

| Panah | Dasar | Status |
|---|---|---|
| IHSG −11,57% (16 Okt) → nilai portofolio pemegang turun | fakta halaman | ditulis |
| Data kepemilikan ritel → besar kelompok | tidak didukung | **dinyatakan tidak terukur, bukan diklaim** |
| Konsultasi MSCI → dana EM keluar → biaya pendanaan naik | fakta halaman + inferensi kuat + kemungkinan | ditulis bersyarat ("jika keputusan nanti berupa penurunan") |
| Biaya pendanaan naik → capex turun → lowongan berkurang | **tidak didukung** | **dipotong, dan pemotongan dinyatakan** |
| Rupiah Rp18.033 (4 Jun) → harga barang impor → biaya hidup | fakta halaman + kemungkinan | ditulis sebagai potensi; periode dipisah dari 16 Okt |
| PP 21/2026 & PP 26/2026 → dampak ke pemuda | tidak didukung | **tidak ditulis** |

Penilaian: rantai indeks → portofolio ritel tertulis; rantai biaya modal → lowongan **ditolak eksplisit** karena tidak ada data capex/perekrutan. Titik uji kasus 1 lolos.

### 2.2 Kasus 2 — `peristiwa/sepak-terjang-haji-isam.md` (12/14)

Section verbatim:

> ## Apa relevansinya dengan anak muda?
>
> Jalur yang benar-benar tertelusur di halaman ini adalah harga, bukan jaringan korporasi-politik. Saham BYAN melonjak 19,97% ke batas auto-reject atas pada 18 Agustus 2026 karena rumor pengambilalihan 62,2%, lalu terkoreksi 11,74% pada 14 September; saham PGUN menguat sampai 75% dalam sepekan akibat spekulasi restrukturisasi; BBCA turun 6,86% ke Rp4.820 pada 19 Oktober 2026. Bagi anak muda yang memegang salah satu saham itu, nilai portofolionya bergerak dalam rentang lebar hanya dalam hitungan hari. Halaman mencatat pergerakan harga tersebut, tetapi juga menyatakan korelasi harga–rumor tidak terbukti untuk BBCA dan bahwa penurunan itu terjadi di tengah tekanan pasar luas (IHSG −4,31%). Jadi yang bisa dikatakan: volatilitasnya terdokumentasi, sebabnya belum.
>
> Halaman ini juga memberi bahan yang jarang ada: dua angka untuk satu transaksi. Porsi 30% BYAN disebut bernilai Rp115,25 triliun saat pengumuman (harga Rp11.525, 17 September 2026), sementara realisasinya pada 7 Oktober 2026 adalah 10.084.088.370 saham @Rp2.588 atau sekitar Rp26,09 triliun. Selisih itu bukan skandal, melainkan beda antara nilai pasar dan nilai transaksi — dan kemampuan membedakannya adalah bekal praktis bagi pembaca muda yang menilai berita akuisisi, termasuk saat membaca rumor BCA yang dibantah manajemen dan tidak pernah dikonfirmasi BEI, OJK, maupun banknya sendiri.
>
> Yang tidak bisa ditulis dari halaman ini: dampaknya pada lapangan kerja, upah, atau ekonomi Kalimantan Selatan. Halaman mencatat perubahan pemegang 30,25% saham BYAN dan status *High Shareholding Concentration*, tetapi tidak memuat data ketenagakerjaan, produksi, atau penerimaan daerah. Menyambungkannya ke nasib pekerja muda di sektor batu bara akan menjadi tebakan.

Audit kausalitas:

| Panah | Dasar | Status |
|---|---|---|
| Rumor → BYAN +19,97% (18 Agu) → −11,74% (14 Sep) | harga = fakta halaman; lonjakan = fakta halaman; koreksi = inferensi kuat | ditulis |
| Spekulasi restrukturisasi → PGUN +75% | fakta halaman | ditulis |
| Rumor BCA → BBCA −6,86% | harga = fakta; sebab = **tidak didukung** (halaman menyatakan korelasi tidak terbukti, di tengah IHSG −4,31%) | ditulis **dengan penyangkalan eksplisit** |
| Pergerakan harga → nilai portofolio | inferensi kuat | ditulis sebagai "bagi yang memegang" |
| Akuisisi 30,25% BYAN → komposisi indeks/reksa dana | **tidak didukung** (klaim ini hanya ada di section lama halaman) | **tidak diwarisi, tidak ditulis** |
| Akuisisi → lapangan kerja/upah/ekonomi Kalsel | **tidak didukung** | **ditolak eksplisit** |
| Rp115,25 T vs Rp26,09 T → literasi membaca valuasi | kedua angka = fakta halaman, label dasar berbeda | ditulis sebagai kapasitas, bukan klaim dampak |

Penilaian: LLM **tidak memaksa** hubungan korporasi-politik → anak muda. Tiga jalur paling menggoda (indeks/reksa dana, lapangan kerja, ekonomi daerah) ditolak. Kekurangan skor ada di mekanisme (1) dan keseimbangan (1) — halaman memang minim data dampak, bukan karena pelonggaran standar.

### 2.3 Kasus 3 — `uu-pelindungan-ketenagakerjaan-2026.md` (13/14)

Section verbatim:

> ## Apa relevansinya dengan anak muda?
>
> UU ini menyentuh anak muda paling langsung lewat tiga hal yang disebut halaman: isi perjanjian kerja waktu tertentu (PKWT), pembatasan alih daya pada enam bidang jasa penunjang, dan pesangon. Yang tercakup secara hukum adalah mereka yang bekerja dengan kontrak, bukan seluruh pekerja. Halaman mencatat batas PKWT dalam draf paling lama dua tahun dan dapat diperpanjang dua kali paling lama satu tahun, lebih ketat daripada PP No. 35 Tahun 2021 yang membolehkan sampai lima tahun. Tetapi rincian itu masih dibaca dari draf dan pemberitaan, bukan teks resmi, sehingga belum bisa diperlakukan sebagai hak yang pasti berlaku. Untuk pekerja platform digital, halaman justru mencatat penundaan: aturan rincinya diserahkan ke undang-undang tersendiri paling lambat dua tahun sejak UU diundangkan, dan seorang anggota Panja menilai pengaturannya masih umum. Bagi pekerja muda yang penghasilannya bergantung pada aplikasi, UU ini belum menjawab apa pun pada saat disahkan.
>
> Halaman ini tidak memuat satu pun angka upah: tidak ada nominal upah minimum, tidak ada data upah riil setelah inflasi, juga tidak ada data kepatuhan, jam kerja, atau respons perusahaan terhadap perekrutan. Karena itu tidak ada dasar untuk menyimpulkan bahwa pekerja muda akan lebih sejahtera setelah UU berlaku. Yang bisa dikatakan hanya bahwa batas waktu kontrak memendek dan cakupan alih daya menyempit, dan keduanya baru terasa kalau aturan pelaksana serta pengawasannya berjalan. Halaman juga mencatat keberatan Apindo bahwa pengetatan PKWT berpotensi memperlebar posisi pekerja informal yang rentan terhadap pelindungan. Peringatan itu, jika benar, justru mengenai pekerja yang berada di luar jangkauan aturan ini.
>
> Kelompok yang bisa disebut dengan jujur: pekerja yang sedang menjalani tahun-tahun pertama kerja dengan kontrak berjangka, pekerja alih daya di enam bidang penunjang, dan pekerja platform digital. Halaman tidak menyediakan data usia, jadi tidak bisa dipastikan berapa bagian dari kelompok itu anak muda, dan seberapa besar bagian itu tidak diukur di sini.

Audit kausalitas:

| # | Panah | Dasar | Status |
|---|---|---|---|
| A1 | UU disahkan → isi kontrak/PKWT/pesangon berubah | fakta halaman, tingkat `CLAIMED` (draf) | didukung bersyarat |
| A2 | Batas PKWT 2 th + 2×1 th → masa kontrak memendek vs PP 35/2021 | fakta halaman, kutipan = draf via medsos | **inferensi berlabel** |
| A3 | Aturan platform ditunda 2 th → pekerja platform tak dapat aturan rinci sekarang | fakta halaman (Pasal 51 + pernyataan anggota Panja) | didukung |
| A4 | Pengetatan PKWT → pekerja informal melebar | pernyataan Apindo di halaman | **klaim pihak ketiga**, disajikan sebagai peringatan |
| A5 | UU → upah naik → anak muda lebih sejahtera | **tidak ada angka upah** | **tidak dibuat; ketiadaan dasar dinyatakan** |
| A6 | UU → semua anak muda terdampak | **tidak ada data usia** | **tidak dibuat; dinyatakan** |

Penilaian: cakupan hukum dipisah dari cakupan faktual, ketiadaan data upah dinyatakan terbuka, kesimpulan "lebih sejahtera" ditolak. Aspek bukti = 1 (bukan 0) karena paragraf utama bersandar pada draf yang belum diundangkan.

### 2.4 Kasus 4 — `analisis/analisis-satgas-pkh-uang-vs-nilai.md` (10/14)

Section verbatim:

> ## Apa relevansinya dengan anak muda?
>
> Hubungan halaman ini dengan anak muda tidak lewat pembagian manfaat, melainkan lewat cara membaca angka negara. Halaman memisahkan dengan tegas dua hal yang sering tercampur: sekitar Rp52 triliun kas yang benar-benar diserahkan dalam delapan tahap, dan klaim valuasi lahan hampir Rp400 triliun yang disebut Presiden. Rp13,24 triliun dari tahap VIII pun bukan sitaan hasil kejahatan: Rp8,22 triliun di antaranya penerimaan pajak, Rp3,47 triliun denda administratif, dan Rp1,53 triliun PNBP Kejaksaan. Bagi pembaca muda yang mengikuti debat defisit dan belanja publik, perbedaan ini menentukan angka mana yang layak dikutip; menjumlahkan keduanya akan menghasilkan gambaran penerimaan negara yang tidak pernah ada.
>
> Halaman ini tidak menelusuri ke mana Rp52 triliun dialokasikan di APBN, dan tidak mencatat satu program pun yang dananya bersumber dari situ. Karena itu tidak ada dasar untuk menyebut penertiban ini menguntungkan atau merugikan kelompok anak muda secara fiskal. Yang tersisa sebagai pertanyaan terbuka: apakah penerimaan itu benar-benar menambah ruang belanja, dan apakah 140.762,04 hektare kebun yang kini dikelola Agrinas Palma Nusantara dikelola cukup produktif untuk menjaga penerimaan berikutnya. Halaman menandai keduanya sebagai celah data, bukan sebagai hasil.

Audit kausalitas:

| # | Panah | Dasar | Status |
|---|---|---|---|
| B1 | Rp52 T kas vs Rp400 T valuasi → tidak boleh dijumlahkan | fakta halaman (Catatan presisi) | **didukung, dipertahankan utuh** |
| B2 | Komposisi tahap VIII dominan pajak → *revenue recovery*, bukan *asset recovery* | fakta halaman (Perspektif) | didukung |
| B3 | Membedakan kas vs valuasi → pembaca tidak salah mengutip | inferensi berlabel | ditulis, tidak diukur |
| B4 | Rp52 T → manfaat fiskal bagi anak muda | alokasi APBN tidak ditelusuri | **tidak dibuat; dinyatakan** |
| B5 | 140.762,04 ha → produktivitas menentukan penerimaan lanjutan | fakta halaman + celah data | didukung **sebagai pertanyaan terbuka** |
| B6 | Rp52 T + Rp400 T = Rp452 T | dilarang eksplisit halaman | **tidak dibuat** |

Penilaian: pemisahan kas vs valuasi dipertahankan; komposisi pajak/denda/PNBP disebut agar tidak terbaca sebagai sitaan; tidak ada klaim fiskal pada kelompok muda. Skor tertahan di 10 justru karena kejujuran struktural — halaman tidak menyediakan mekanisme dampak.

### 2.5 Kasus 6 — `aktor/zainudin-hasan.md` (7/14 — lihat temuan 4)

Halaman: stub 372 byte, tubuh hanya berisi `# Zainudin Hasan`, `relasi: []`, tanpa jabatan/keputusan/sektor/data dampak.

Section verbatim:

> ## Apa relevansinya dengan anak muda?
>
> Halaman ini belum memuat uraian apa pun selain identitas: nama, kategori sebagai aktor, dan status stub. Tidak ada jabatan, kebijakan, keputusan, layanan, sektor, atau relasi yang tercatat di dalamnya, sehingga tidak ada jalur yang bisa ditelusuri menuju kehidupan anak muda.
>
> Karena itu halaman ini belum memberi dasar untuk menyebut kelompok muda mana pun sebagai terdampak, dan bagian ini sengaja berhenti di situ. Relevansi baru bisa ditulis setelah halaman memuat peran atau keputusan yang konkret beserta akibatnya.

Audit kausalitas:

| # | Panah | Dasar | Status |
|---|---|---|---|
| C1 | Halaman hanya berisi identitas → tidak ada jalur dampak | fakta halaman | **didukung** |
| C2 | Tokoh politik → relevan bagi anak muda | tidak ada apa pun di halaman | **tidak dibuat** |
| C3 | Deskripsi frontmatter "relasi bisnis-politik terdokumentasi" → ada jaringan | tubuh kosong, `relasi: []` | **tidak diulang** |

Penilaian: perilaku generator **benar** — menahan diri, tidak meminjam bobot dari label "politisi", tidak meminjam fakta luar. Yang gagal adalah rubrik, bukan hasilnya (temuan 4).

---

## 3. Verifikasi silang (parent)

Seluruh angka yang dipakai subagen dicek ulang terhadap halaman sumber — semuanya ada:

- Halaman 1: `11,57`, `5.185,11`, `18.033`, `MSCI`, `2,3 triliun` — ada.
- Halaman 2: `19,97`, `11,74`, `75%`, `4.820`, `115,25`, `26,09`, `30,25`, `High Shareholding` — ada.
- Halaman 3: `2 tahun`, `35 Tahun 2021`, `Permenaker 7/2026`, `Pasal 51`, `Apindo`, `pengupahan`, `6 Oktober 2026` — ada.
- Halaman 4: `52 triliun`, `13,24`, `8,22`, `3,47`, `1,53`, `140.762`, `259.230`, `6,2 juta`, `400 triliun` — ada.
- Halaman 5: isi halaman = 1 baris judul saja — terkonfirmasi.

**Halaman wiki tidak berubah:** `git status` hanya menunjukkan direktori `proposals/youth-relevance-uji-2026-10-20/` sebagai untracked; tidak ada satu pun file di `content/` yang termodifikasi.

Klaim pembanding juga terverifikasi: section lama `## Kenapa penting buat Gen Z` di keempat halaman memang lebih longgar — halaman 3 menulis "tiga hal yang langsung terasa pada tahun-tahun pertama bekerja" tanpa data usia, halaman 4 memakai frasa "Bagi pembaca muda" tanpa eksposur terukur. Section baru lebih ketat daripada section lama di halaman yang sama.

---

## 4. Temuan pola

1. **Rantai paling rawan dipaksa = pasar keuangan → lapangan kerja.** Kasus 1 menyediakan umpan ("konsultasi MSCI → klasifikasi turun") yang mudah disambung ke "investasi turun → PHK". Draf menolak menyambung karena tidak ada data capex/perekrutan.
2. **Tekanan menempel datang dari nama entitas dan angka besar**, bukan dari fakta dampak (kasus 2: Rp115 T, konglomerat, BCA). Menahan diri di sini lebih sulit daripada menulis.
3. **Perangkap halus: mencampur periode.** Kurs rekor 4 Juni dan indeks jatuh 16 Oktober; menyebut keduanya "bersamaan" adalah fabrikasi ringan yang lolos dari pembaca sekilas.
4. **Perangkap kedua: mewarisi klaim section lama.** Dua halaman memuat klaim relevansi yang tidak didukung badan halaman. Generator harus membaca badan halaman, bukan menyalin `## Kenapa penting buat Gen Z`.
5. **Rubrik tidak punya sel untuk abstensi.** Kasus 6 mendapat 7 ("tulis ulang") padahal keluaran yang benar memang nyaris kosong — aspek kelompok/mekanisme/waktu bernilai 0 secara struktural ketika tidak ada klaim yang boleh dibuat.
6. **Titik lemah terbesar ada di halaman 3, bukan halaman sulit.** Isi UU masih `CLAIMED` (draf). Generator cenderung memperlakukan "draf yang diberitakan" sebagai "aturan yang berlaku" bila tidak dipaksa membedakan status provenance.
7. **Angka fiskal cenderung dilebur** (Rp52 T + Rp400 T). Kasus 4 lolos karena halaman sumber sendiri sudah melarang penjumlahan — bukan karena metodenya otomatis aman.

---

## 5. Rekomendasi rollout

**Keputusan yang dibutuhkan user — langkah setelah laporan ini DITAHAN sampai ada persetujuan.**

1. **Terima Fase 1 sebagai bukti metode bekerja** (5/5 halaman lolos tanpa fabrikasi; 0 aspek bukti = 0). Metode layak dijadikan generator untuk section relevansi.
2. **Pengetatan method sebelum rollout massal** (perubahan `docs/youth-relevance/youth-relevance-method.md`, bukan halaman wiki):
   - tambah langkah wajib: periksa status provenance tiap fakta (berlaku / disahkan belum diundangkan / draf / klaim pihak) sebelum menulis panah;
   - tambah aturan eksplisit: jangan menjumlahkan arus kas dengan valuasi stok, dan jangan menggabung dua periode berbeda menjadi satu peristiwa;
   - tambah aturan: jangan mewarisi klaim dari section `## Kenapa penting buat Gen Z` lama;
   - tambah rubrik nilai khusus `N/A — abstain` (atau aspek "penahanan diri") untuk halaman stub.
3. **Urutan rollout** (usulan): batch kecil bertahap per kategori, dimulai kategori `analisis` (paling kaya fakta), bukan `aktor` (banyak stub).
4. **Jangan** retrofit massal sekarang, dan **jangan** terbitkan section uji ke halaman mana pun — termasuk mengganti section lama — sebelum user menyetujui poin 2.

---

## 6. Definisi selesai Fase 1

- Paket berversi di repo: `docs/youth-relevance/` (commit `e05a238`).
- 5 section uji + skor + audit kausalitas terdokumentasi: `proposals/youth-relevance-uji-2026-10-20/hasil/` dan `.../evaluasi/`.
- Rekomendasi diajukan (poin 5).
- Menunggu keputusan user.
