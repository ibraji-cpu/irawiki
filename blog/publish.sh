#!/bin/bash
set -e

echo "🚀 Memulai proses publish blog..."
cd /home/ubuntu/irawiki/blog

# 1. Build web statis ke direktori Nginx
echo "⚙️  Menjalankan build Hugo..."
hugo --minify --cleanDestinationDir -d /var/www/blog

# 2. Simpan perubahan ke Git
echo "📦 Menyimpan jejak perubahan ke Git..."
git add -A

# Cek apakah ada perubahan sebelum commit
if ! git diff-index --quiet HEAD; then
    git commit -m "Auto-publish artikel baru"
    echo "✅ Perubahan berhasil di-commit."
else
    echo "ℹ️ Tidak ada perubahan baru untuk di-commit."
fi

echo "🎉 Publish selesai! Website sudah diperbarui di https://blog.iraamalia.id"
