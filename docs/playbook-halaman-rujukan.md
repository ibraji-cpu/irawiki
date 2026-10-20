---
title: "Playbook Halaman Rujukan"
description: "Standar baku halaman rujukan IRAWIKI: struktur tujuh bagian, aturan bahasa Gen Z, fakta kunci, catatan presisi, dan prosedur verifikasi."
date: 2026-10-20
updated: "2026-10-20"
entity_type: dokumen
entity_id: "playbook-halaman-rujukan"
status: "aktif"
confidence: 9
risiko_editorial: "rendah"
last_updated: "2026-10-20"
last_verified: "2026-10-20"
relasi: []
---

# Playbook Halaman Rujukan

> **Status dokumen:** sumber kebenaran (*source of truth*) untuk struktur dan mutu **halaman rujukan** IRAWIKI. Jika playbook ini berbeda dengan kebiasaan lama sebuah halaman, playbook yang menang. Perubahan aturan wajib lewat dokumen ini, bukan lewat satu halaman.

## 1. Tujuan dan ruang lingkup

Halaman rujukan adalah halaman yang **dibaca orang luar**, bukan hanya penulis wiki: pelajar, mahasiswa, jurnalis pemula, pembuat konten, dan pembaca yang mendarat dari mesin pencari. Mereka datang tanpa konteks, sering dari ponsel, sering berhenti membaca dalam 20 detik.

Halaman rujukan punya tiga tugas:

1. **Menjawab** — apa yang terjadi, kapan, siapa, dan seberapa pasti.
2. **Memberi konteks** — kenapa urusan ini menyentuh hidup pembaca muda.
3. **Tidak menyesatkan** — memisahkan yang terverifikasi dari yang masih laporan, rumor, atau klaim satu pihak.

Playbook ini mengatur **struktur wajib** (Bagian 3), **aturan bahasa** (Bagian 4–5), **aturan presisi** (Bagian 6), dan **prosedur verifikasi** (Bagian 9). Playbook **tidak** mengatur taksonomi aktor/peristiwa/analisis di `SCHEMA.md` — keduanya berlaku bersamaan: `SCHEMA.md` mengatur cara mengekstrak fakta, playbook ini mengatur cara menyajikannya.

### Yang termasuk halaman rujukan

- Halaman **topik/hub** yang merangkum satu isu lintas waktu (mis. `peristiwa/sepak-terjang-haji-isam`).
- Halaman **peristiwa tunggal** yang berdiri sendiri dan layak dikutip (mis. `peristiwa/soeharto-pahlawan-nasional`).
- Halaman **analisis** yang menjawab satu pertanyaan pembaca (mis. `analisis/analisis-satgas-pkh-uang-vs-nilai`).

### Yang tidak termasuk

- Halaman **aktor** (memakai `templates/01_aktor_master_template.md`).
- Halaman **stub**, **disambiguasi**, dan **indeks**.
- Arsip `raw/` (immutable, tidak boleh diubah).

---

## 2. Kriteria memilih halaman untuk retrofit

Prioritas retrofit, berurutan:

| Prioritas | Kriteria | Alasan |
|---|---|---|
| P1 | Punya >1.000 tayangan/bulan atau muncul di 3 kueri pencarian teratas | dampak terbesar per jam kerja |
| P2 | Sering dibagikan di media sosial (masuk feed, jadi rujukan thread) | butuh ringkasan cepat & konteks |
| P3 | Menyangkut uang, hukum, atau hak warga (harga, pajak, putusan, ijazah, lahan) | pembaca muda paling terdampak |
| P4 | Isinya sudah stabil (tidak berubah tiap hari) | hasil retrofit tidak cepat basi |
| P5 | Panjang >800 kata dan tidak punya ringkasan | biaya baca terlalu tinggi |

Aturan tambahan:

- **Jangan retrofiti halaman yang sedang develop cepat** (mis. perkara yang sidangnya mingguan). Tunggu satu putaran, lalu kerjakan.
- **Satu halaman = satu commit** agar mudah di-*revert* per halaman.
- Retrofit **tidak menghapus** isi. Yang ada hanya ditambah, dipindah ke urutan baku, atau dirapikan bahasanya.

---

## 3. Struktur wajib: tujuh bagian

Urutan ini **tetap**. Nama heading **tetap**. Bagian yang tidak relevan tidak dihapus — diisi pernyataan singkat bahwa datanya belum ada (lihat 3.7).

```
# Judul halaman

## Ringkasan
## Kenapa penting buat Gen Z
## Fakta kunci
## Kronologi
## Aktor yang Terlibat
## Sumber
## Catatan presisi
```

### Slot tambahan (boleh, tidak wajib)

Bagian khas halaman boleh disisipkan, tetapi hanya di dua slot:

- **Slot konteks** — setelah `## Fakta kunci`, sebelum `## Kronologi`. Untuk kerangka konsep atau latar historis (`## Tipologi Perang Ultra Modern`, `## Latar Belakang`, `## Objek Sengketa`).
- **Slot rincian** — setelah `## Aktor yang Terlibat`, sebelum `## Sumber`. Untuk rincian hukum/status (`## Pokok Sengketa Hukum`, `## Putusan 50/G/2026/PTUN.JKT`, `## Status Terkini`, `## Analisis Terkait`, `## Peristiwa Terkait & Milestone`).

Tidak boleh ada bagian wajib yang tergeser ke bawah `## Sumber`. `## Catatan presisi` selalu **paling akhir**.

### 3.1 `## Ringkasan`

- 2–4 kalimat. Bukan daftar. Bukan tempelan kutipan.
- Harus menjawab: **apa**, **siapa**, **kapan**, **status sekarang** (selesai / berjalan / rumor).
- Sebut angka hanya jika angka itu muncul lagi di Fakta kunci (jangan dua versi angka).
- Hari ini banyak halaman memakai blockquote `> **Ringkasan Topik:** ...`. Bentuk itu **dipertahankan** bila sudah ada; kalimat pembukanya tetap harus memenuhi syarat di atas.

### 3.2 `## Kenapa penting buat Gen Z`

Bagian ini yang membedakan halaman rujukan dari siaran pers. Aturannya ketat:

- **3–6 kalimat.** Kurang dari 3 = tidak menjelaskan apa-apa; lebih dari 6 = berubah jadi esai.
- **Semua kalimat harus faktual.** Setiap kalimat harus bisa dilacak ke isi halaman atau sumber di bagian Sumber. Tidak ada opini, tidak ada ramalan, tidak ada "generasi kita harus...".
- **Satu kalimat = satu ide.** Kalimat pertama menyebut **apa yang menyentuh pembaca** (biaya, kerja, pendidikan, hak, kepercayaan pasar). Kalimat berikutnya menyebut **mekanismenya**.
- **Sebutkan dampak yang konkret**, bukan yang abstrak: "harga saham turun" bukan "stabilitas terganggu"; "syarat ijazah masuk berkas pencalonan" bukan "integritas pemilu dipertanyakan".
- **Larangan:** kata "guys", "gaes", "literally", "ribet banget sih", emoji, tanda seru, sapaan "kamu", dan semua bentuk *hype*. Nada: dewasa, tenang, langsung.
- **Larangan kedua:** mengarang alasan. Jika hubungan sebab-akibat belum terbukti di halaman, tulis sebagai kemungkinan yang belum terverifikasi — atau jangan tulis.
- Jika topik jelas tidak menyentuh pembaca muda secara langsung, katakan apa adanya dalam 3 kalimat: topik ini jauh dari hidup sehari-hari, tetapi relevan karena X (dan X harus faktual). **Jangan memaksakan relevansi.**

Contoh bentuk yang benar (satu kalimat per ide, tanpa hype):

> Kebijakan ini menentukan ke mana devisa ekspor pergi, dan itu memengaruhi kurs yang dipakai untuk harga barang impor. Bagi pekerja muda, efek paling terasa ada di biaya hidup dan kesempatan kerja di sektor yang bergantung ekspor. Halaman ini mencatat apa yang sudah resmi dan apa yang masih klaim.

### 3.3 `## Fakta kunci`

- **4–6 butir**, bukan 10. Ini ringkasan yang dipindai, bukan daftar isi.
- Setiap butir wajib mengandung minimal satu **angka, tanggal, nomor perkara/keppres, atau nama lembaga**.
- Angka harus **sama persis** dengan yang ada di Kronologi/Sumber. Tidak boleh ada pembulatan baru yang menimbulkan angka ketiga.
- Format: `- **Label:** nilai (konteks, tanggal)`.
- Dilarang mengisi butir dengan penilaian ("sangat besar", "kontroversial"). Penilaian masuk ke Catatan presisi atau dinyatakan sebagai atribusi.
- Jika halaman hanya punya 4 fakta keras, tulis 4. Jangan menambah butir dengan fakta lunak.

### 3.4 `## Kronologi`

- Entri berurutan **lama → baru**.
- Format heading entri: `### YYYY-MM-DD — Judul singkat`. Jika tanggal tidak diketahui, **jangan mengarang tanggal**: pakai `### Tanggal tidak diketahui — Judul` dan sebutkan alasannya di Catatan presisi.
- Satu entri = satu kejadian. Jangan mencampur tiga peristiwa dalam satu entri hanya karena sebulan.
- Setiap entri menyebut **sumbernya secara implisit** lewat nama lembaga/tokoh yang faktual (mis. "Keterbukaan Informasi BEI", "Putusan MK No. 01/PHPU.PRES-XXIV/2026"), dan detailnya dirujuk ke bagian Sumber.
- Klaim yang masih dugaan ditulis dengan atribusi: "menurut dokumen ringkasan kasus", "dilaporkan", "belum terverifikasi".
- Jangan menambah entri hanya untuk mengisi ruang. Kronologi dua entri lebih baik daripada enam entri berisi pengulangan.

### 3.5 `## Aktor yang Terlibat`

- Bentuk baku: daftar butir `- [[wikilink|Nama]] — peran dalam satu frasa.`
- Halaman yang sudah memakai **tabel** (kasus `soeharto-pahlawan-nasional`) boleh tetap tabel; jangan diubah hanya demi keseragaman bentuk.
- Peran harus menggambarkan **kedudukan dalam peristiwa**, bukan profil biografi. Biografi ada di halaman aktor.
- Jangan menautkan aktor yang tidak punya halaman; tulis namanya sebagai teks biasa (lihat 3.8 soal tautan).
- Urutan: pihak utama → pihak lawan/penyeimbang → lembaga → pihak yang hanya dikutip.

### 3.6 `## Sumber`

- Kelompokkan per tanggal peristiwa dengan sub-heading `### Sumber Peristiwa YYYY-MM-DD`, atau per jenis (`### Sumber Putusan`, `### Dokumen Sumber`). Halaman yang sudah punya pengelompokan rapi tidak perlu diubah.
- Setiap butir: `- [Judul](URL) — Penerbit, tanggal.` Jika berupa dokumen (putusan, keppres), tulis identitas dokumennya secara lengkap.
- **Jangan menambah URL baru saat retrofit** kecuali untuk menggantikan URL yang mati. Retrofit adalah pekerjaan struktur, bukan peliputan baru.
- Sumber yang dipakai untuk klaim sensitif wajib disebut **sumber tunggal** secara eksplisit.

### 3.7 Bagian yang belum ada datanya

Jika sebuah halaman belum punya bahan untuk satu bagian wajib, tulis satu baris jujur:

> Belum tersedia: kronologi terperinci belum disusun karena sumber yang ada hanya memuat dua tanggal.

Jangan menghapus heading, dan jangan mengarang isi. Heading kosong tanpa penjelasan dianggap **gagal template**.

### 3.8 Aturan tautan

- `[[wikilink]]` hanya untuk halaman yang **sudah ada** di `content/`. Setiap tautan baru wajib dicek dengan `tools/link_check.py`.
- Nama entitas yang tidak punya halaman ditulis sebagai teks biasa.
- Jangan mengubah `entity_id` halaman lain, dan jangan membuat varian nama baru untuk entitas yang sudah ada.

---

## 4. Aturan bahasa

1. **Indonesia baku, kalimat pendek.** Rata-rata di bawah 25 kata. Satu kalimat, satu klaim.
2. **Aktif, bukan pasif berantai.** "MK memutus" bukan "perkara telah diputuskan oleh MK".
3. **Tanpa istilah asing yang tidak perlu.** Jika harus, miringkan dan jelaskan sekali: *legal standing* (kedudukan hukum untuk menggugat).
4. **Tanpa bahasa birokrasi.** "penyerahan dilakukan" → "Satgas menyerahkan".
5. **Tanpa kata penguat kosong**: sangat, amat, luar biasa, tentu saja, jelas sekali.
6. **Angka mengikuti gaya Indonesia**: `Rp13,24 triliun`, `140.762,04 ha`, `6,86%`, tanggal `6 Oktober 2026`.
7. **Nama lembaga lengkap saat pertama muncul**, singkatan setelahnya.
8. **Konsisten ejaan**: "Soeharto", "Joko Widodo", "Mahkamah Konstitusi (MK)".
9. **Jangan mencampur bahasa asing ke dalam kalimat Indonesia.** Kata serapan Prancis/Inggris yang bocor ("selon", "avec", "between") adalah cacat yang wajib diperbaiki saat retrofit.
10. **Tanpa *typo* yang dibiarkan.** Retrofit termasuk *copy-edit*.

---

## 5. Suara: tegas, bukan provokatif

- Tulis seperti menjelaskan ke orang cerdas yang belum tahu apa-apa soal topik ini.
- Boleh menyebut kontroversi. Tidak boleh memihak.
- Setiap tuduhan diberi atribusi: "penggugat mendalilkan", "Moody's menilai", "dilaporkan".
- Jangan memakai kata yang memvonis: "korup", "curang", "boneka", "rezim" — kecuali sebagai kutipan yang diatribusikan.
- Judul bagian tidak boleh *clickbait*. `## Fakta kunci`, bukan `## Yang Tidak Diberitahu Media`.

---

## 6. `## Catatan presisi`

Bagian penutup ini yang membuat halaman bisa dipercaya. Isinya **status bukti**, bukan ringkasan ulang.

Wajib memuat, bila relevan:

1. **Apa yang terverifikasi** — dan dari dokumen apa (mis. "amar putusan diverifikasi dari salinan resmi 117 halaman").
2. **Apa yang masih laporan/klaim tunggal** — dengan penanda tegas: *dilaporkan*, *belum terverifikasi independen*.
3. **Apa yang masih rumor** — dan apa yang **tidak boleh** disimpulkan darinya (mis. korelasi harga–rumor tidak terbukti).
4. **Angka yang berbeda antar sumber** — sebutkan kedua versi dan sebab perbedaannya jika diketahui.
5. **Celah data** — bagian yang belum bisa diisi dan apa yang dibutuhkan untuk mengisinya.
6. **Batas interpretasi** — satu kalimat: apa yang halaman ini **tidak** klaim.

Aturan bentuk: 4–8 butir, masing-masing satu baris, diawali label tebal. Bukan paragraf.

Contoh:

> - **Terverifikasi:** amar putusan dibaca dari salinan resmi (117 hlm), 14 Oktober 2026.
> - **Dilaporkan:** identitas penggugat dan dalilnya bersumber satu dokumen ringkasan kasus; belum dikonfirmasi pihak lain.
> - **Rumor:** isu akuisisi BBCA belum pernah dikonfirmasi BEI, OJK, atau BCA.
> - **Batas:** halaman ini tidak menyimpulkan ada pelanggaran hukum oleh pihak mana pun.

---

## 7. Yang tidak boleh dilakukan saat retrofit

- Menambah fakta baru tanpa sumber di bagian Sumber.
- Mengubah angka, tanggal, nomor perkara, atau nama.
- Menghapus peringatan editorial yang sudah ada (`risiko_editorial`, catatan verifikasi).
- Mengganti tabel menjadi daftar (atau sebaliknya) hanya demi keseragaman.
- Menautkan entitas yang halamannya tidak ada.
- Menulis "Kenapa penting buat Gen Z" dengan gaya *influencer*.
- Menyentuh frontmatter selain `updated` dan `last_updated`/`last_verified` (lihat 8).

## 8. Frontmatter saat retrofit

Boleh diubah: `updated`, `last_updated`, `last_verified`.
Tidak boleh diubah: `entity_id`, `entity_type`, `title`, `aliases`, `confidence`, `risiko_editorial`, `relasi`, `sumber`.
Jika tanggal verifikasi berubah, `last_verified` **hanya** boleh diisi jika isi halaman benar-benar diperiksa ulang terhadap sumbernya — bukan karena file disentuh.

---

## 9. Prosedur verifikasi (wajib sebelum commit)

```bash
# 1. struktur: tujuh bagian wajib ada dan berurutan
python3 tools/playbook_check.py content/...   # (lihat Bagian 10)

# 2. tautan internal tidak bertambah rusak
python3 tools/link_check.py --only <file>     # target: 0 rusak untuk halaman pilot

# 3. build bersih
bash build_wiki.sh

# 4. API/MCP sehat
curl -s -o /dev/null -w '%{http_code}\n' 'http://127.0.0.1:8000/search?q=prabowo&limit=1'   # 200
```

Kriteria lulus:

- [ ] Ketujuh heading wajib ada, urut, dan ejaannya sama.
- [ ] `## Kenapa penting buat Gen Z` berisi 3–6 kalimat, tanpa hype, tanpa klaim tanpa sumber.
- [ ] `## Fakta kunci` 4–6 butir, tiap butir punya angka/tanggal/nomor.
- [ ] Tidak ada angka yang muncul dalam dua versi berbeda tanpa penjelasan.
- [ ] `## Catatan presisi` menyebut status bukti dan batas interpretasi.
- [ ] `link_check.py` untuk halaman itu: 0 tautan rusak.
- [ ] Build sukses, jumlah halaman hasil build tidak turun.
- [ ] `git diff` hanya menyentuh halaman yang direncanakan.

---

## 10. Perkakas

| Berkas | Fungsi |
|---|---|
| `tools/link_check.py` | Resolusi seluruh `[[wikilink]]` terhadap `content/` (stem, `entity_id`, `title`, `aliases`). Keluaran berupa daftar tautan rusak per berkas. |
| `tools/playbook_check.py` | Validasi struktur tujuh bagian, jumlah kalimat bagian Gen Z, jumlah butir Fakta kunci, dan keberadaan Catatan presisi. |
| `build_wiki.sh` | Build Quartz + regenerasi `robots.txt`/`llms.txt`. |

`playbook_check.py` sengaja konservatif: ia menandai **struktur**, bukan selera. Peringatan kuning (mis. butir Fakta kunci 3) tidak memblokir commit, tetapi harus dijawab di laporan.

---

## 11. Rencana bertahap

### Fase 1 — Playbook + 5 halaman pilot (selesai pada 2026-10-20)

Halaman pilot dipilih agar mewakili tiga tipe halaman rujukan:

| Halaman | Tipe | Kenapa dipilih |
|---|---|---|
| `perang-ultra-modern-dan-geopolitik.md` | topik konseptual | punya kerangka teori + kronologi ekonomi; menantang pemisahan fakta/interpretasi |
| `peristiwa/sepak-terjang-haji-isam.md` | hub peristiwa panjang | 13 halaman dilipat ke satu hub; butuh ringkasan yang bisa dipindai |
| `peristiwa/soeharto-pahlawan-nasional.md` | peristiwa hukum sensitif | butuh batas interpretasi yang tegas (penganugerahan vs pelanggaran HAM) |
| `peristiwa/polemik-ijazah-gibran.md` | peristiwa hukum populer | trafik tinggi, penuh klaim dua pihak |
| `analisis/analisis-satgas-pkh-uang-vs-nilai.md` | analisis angka | kasus terbaik untuk aturan "kas vs valuasi" |

Keluaran Fase 1: dokumen ini, lima halaman lolos template, dua perkakas verifikasi.

### Fase 2 — 35 halaman berikutnya (belum dimulai, menunggu persetujuan)

- Urutan berdasarkan kriteria Bagian 2 (P1→P5).
- Kuota per putaran: 8–10 halaman, satu commit per halaman.
- Setiap putaran berakhir dengan laporan: halaman mana, temuan presisi apa, tautan rusak baru berapa (target 0).
- **Fase 2 tidak boleh dimulai sebelum Fase 1 disetujui.**

### Fase 3 — Penjagaan mutu

- `playbook_check.py` masuk ke pemeriksaan pra-build.
- Halaman baru wajib lahir dengan tujuh bagian (tambahkan ke template peristiwa & analisis).
- Audit kuartalan: halaman dengan `last_verified` lebih tua dari 12 bulan ditandai.

---

## 12. Riwayat

| Tanggal | Perubahan |
|---|---|
| 2026-10-20 | Versi 1.0 — struktur tujuh bagian, aturan Gen Z, aturan Catatan presisi, `link_check.py`, retrofit 5 halaman pilot. |
