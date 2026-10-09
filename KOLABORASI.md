# KOLABORASI.md — Ruang Kerja Bersama Agen

> Wajib dibaca agen baru sebelum berkontribusi.

## Aturan Utama

1. **Hanya Ibrahim yang merge ke `main`** — tidak ada agen yang boleh merge sendiri.
2. Satu PR = satu unit kerja.
3. Branch berumur pendek: kerja → PR → merge → hapus.

## Struktur Repo

```
wiki/content/       ← isi wiki (Markdown + frontmatter)
blog/posts/         ← artikel Ira Amalia (Markdown + frontmatter)
draf/               ← area kerja agen, tidak ikut terbit
```

## Konvensi Branch

Nama: `<agen>/<topik-singkat>`

Contoh:
- `teknisi/stub-achmad-taufik`
- `hermes/fix-deploy-wiki`
- `konten/carousel-satu-data`

## Alur Kerja

1. Buat branch dari `main`
2. Kerjakan, push
3. Buka PR (draft) → tandai *ready for review* setelah siap
4. Ibrahim review via GitHub Mobile → approve & merge
5. Merge → otomatis terbit (GitHub Actions → build → deploy)

## Prefix Judul PR

- `[wiki]` — perubahan di `wiki/content/`
- `[blog]` — perubahan di `blog/posts/`
- `[draf]` — perubahan di `draf/`

## Checklist PR

- [ ] Wiki: setiap klaim faktual ada sumbernya
- [ ] Wiki: tuduhan memakai kata "diduga"; tersangka ≠ vonis
- [ ] Wiki: tanpa opini (opini hanya untuk blog)
- [ ] Blog: suara Ira Amalia; disclaimer AI tetap ada
- [ ] Frontmatter lengkap & valid
- [ ] Tidak ada konflik dengan `main` terbaru

## Deploy Otomatis

Setiap merge ke `main` memicu GitHub Actions:
- **Wiki**: `git pull` → `build_wiki.sh` → `wiki.iraamalia.id`
- **Blog**: `git pull` → `publish.sh` → `blog.iraamalia.id`

## Peran Agen

| Agen | Peran |
|---|---|
| teknisi (Muse) | Enrichment wiki, draf riset, render aset |
| Hermes | Tooling, wiring deploy, voiceover, posting sosmed |
| konten | Diskusi + draf teks bersama Ibrahim |
| Agen baru | Baca file ini, ikuti konvensi di atas |
