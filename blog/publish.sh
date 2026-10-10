#!/bin/bash
set -e

echo "🚀 Memulai proses publish blog..."
cd /home/ubuntu/irawiki/blog

# 0. Generate ringkasan audio untuk artikel baru (belum punya audio)
echo "🎙️ Cek artikel baru untuk ringkasan audio..."
for md_file in $(find content/posts -maxdepth 2 -name "*.md" -not -name "_index.md" | sort); do
  echo "  → $md_file"
  python3 generate_audio_summary.py "$md_file" --update-frontmatter \
    || echo "  ⚠️ Gagal generate audio untuk $md_file, lanjut..."
done

# 1. Build web statis ke direktori Nginx
echo "⚙️  Menjalankan build Hugo..."
hugo --minify --cleanDestinationDir -d /var/www/blog

# 2. Simpan perubahan ke Git (hanya folder blog/, hindari submodule parent)
echo "📦 Menyimpan jejak perubahan ke Git..."
cd /home/ubuntu/irawiki
git add blog/

# Cek apakah ada perubahan sebelum commit
if ! git diff-index --quiet HEAD -- blog/; then
    git commit -m "Auto-publish artikel baru"
    echo "✅ Perubahan berhasil di-commit."
else
    echo "ℹ️ Tidak ada perubahan baru untuk di-commit."
fi

echo "🎉 Publish selesai! Website sudah diperbarui di https://blog.iraamalia.id"
