---
title: "Panduan Paket Relevansi Anak Muda"
type: documentation
status: draft
lang: id
last_reviewed: 2026-10-20
---

# Paket Markdown: “Apa relevansinya dengan anak muda?”

Paket ini membantu LLM menyusun bagian **“Apa relevansinya dengan anak muda?”** pada halaman Wiki Ira Amalia. Tujuannya bukan membuat semua topik tampak relevan, melainkan menemukan hubungan yang konkret, spesifik, dan dapat ditelusuri ke bukti.

## Isi paket

- [`youth-relevance-map.md`](youth-relevance-map.md) — peta isu, kebutuhan, aspirasi, kelompok, mekanisme dampak, dan horizon waktu.
- [`youth-relevance-method.md`](youth-relevance-method.md) — prosedur analisis, standar bukti, dan aturan penulisan untuk LLM.
- [`youth-relevance-sources.md`](youth-relevance-sources.md) — daftar awal sumber rujukan dan aturan memperbaruinya.
- [`youth-relevance-test-cases.md`](youth-relevance-test-cases.md) — contoh uji agar LLM tidak menghasilkan relevansi tempelan.

## Cara pakai yang disarankan

1. Simpan ke repositori wiki atau repositori prompt yang terpisah.
2. Berikan `youth-relevance-method.md` dan `youth-relevance-map.md` kepada LLM saat membuat atau memperbarui halaman.
3. Gunakan `youth-relevance-sources.md` sebagai daftar awal sumber untuk riset lanjutan. Jangan menganggap daftar ini sebagai bukti lengkap untuk setiap klaim.
4. Jalankan contoh pada `youth-relevance-test-cases.md` sebagai uji kualitas sebelum menerapkan generator ke seluruh wiki.

## Prinsip utama

Peta ini **menghasilkan pertanyaan yang perlu diperiksa**, bukan jawaban faktual otomatis. Klaim dampak harus dibuktikan dari sumber yang relevan. Jika bukti tidak tersedia, LLM harus mempersempit klaim, menyebutkan ketidakpastian, atau tidak membuat klaim tersebut.

## Status

Ini adalah versi awal untuk diuji. Kategori, contoh, dan sumber perlu ditinjau secara berkala. Jangan menyalin angka statistik dari sumber lama ke halaman baru tanpa memeriksa tahun, populasi, metode, dan konteksnya.
