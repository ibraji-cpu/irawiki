---
title: "[Nama Aktor]"
tags:
- individu
entity_type: individu
entity_id: "[slug-aktor]"

nama_lengkap: "[Nama lengkap]"
nama_alias:
- "[Alias jika ada]"

jabatan_aktif:
- "[Jabatan aktif + periode]"

jabatan_historis:
- "[Jabatan sebelumnya + periode]"

partai: "[Partai / independen / tidak diketahui]"
basis_daerah:
- "[Daerah]"

latar_militer: "[ya/tidak/tidak diketahui]"

afiliasi_bisnis:
- "[[Perusahaan/Entitas Bisnis]]"

afiliasi_ormas:
- "[[Organisasi]]"

afiliasi_keagamaan:
- "[Agama/afiliasi jika memang tercantum dalam sumber]"

dinasti_politik:
- "[Relasi keluarga/kerabat yang terdokumentasi]"

kepemilikan_konsesi:
- "[Konsesi yang terdokumentasi]"

kebijakan_didukung:
- "[Kebijakan yang secara eksplisit didukung]"

kebijakan_ditolak:
- "[Kebijakan yang secara eksplisit ditolak]"

isu_konsisten:
- "[Isu yang konsisten terkait aktor]"

catatan_kontroversial:
- "[Kontroversi yang terdokumentasi + sumber/atribusi bila relevan]"

member_of:
- "[[Organisasi/Lembaga]]"

leader_of:
- "[[Organisasi/Perusahaan]]"

pengaruh_media: "[rendah/sedang/tinggi/tidak diketahui]"
status_hukum: "[bersih/bermasalah/tidak diketahui]"

risiko_editorial: "[rendah/sedang/tinggi]"
confidence: 5
last_updated: "[YYYY-MM-DD]"
last_verified: "[YYYY-MM-DD]"

relasi:
  - tipe: memimpin                    # vocabulary: mengangkat, memecat, menggantikan, memimpin, berkoalisi_dengan, berkonflik_dengan, mendukung, mengkritik, terlibat_dalam, memicu, bagian_dari
    target: aktor/[slug-target]       # format: entity_type/entity_id
    tanggal: "[YYYY-MM-DD]"           # opsional
    sumber: "[Sumber wajib, mis. Kompas, 21 Okt 2024]"
    catatan: "[opsional]"
  - tipe: berkonflik_dengan
    target: aktor/[slug-target-2]
    sumber: "[Sumber wajib]"
---

# [Nama Aktor]

## Jabatan Aktif

- [Jabatan aktif terbaru]
- [Jabatan aktif lainnya]

## Riwayat Jabatan

- [Jabatan sebelumnya]

## Afiliasi Bisnis

- [[Perusahaan/Entitas Bisnis]]

## Afiliasi Organisasi

- [[Organisasi/Lembaga]]

## Perkembangan Terakhir

### [YYYY-MM-DD]

- [Perubahan atau perkembangan terbaru]
- [[Peristiwa terkait]]

## Relasi Terstruktur

- [tipe] → [target]: [sumber] ([tanggal]) — [catatan]
- [Contoh: memimpin → aktor/budi-gunawan: "Kompas, 21 Okt 2024" — Menetapkan sebagai ketua pelaksana.]

## Catatan

- [Informasi tambahan yang relevan dan bersumber]

## Sumber
- [Sumber]
