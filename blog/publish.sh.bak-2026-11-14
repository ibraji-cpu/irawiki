#!/bin/bash
set -e

# google-genai + dotenv TIDAK ada di venv, hanya di site-packages ini.
# Tanpa ini: ModuleNotFoundError di generate_audio_summary.py -> step audio mati senyap.
export PYTHONPATH=/home/ubuntu/.local/lib/python3.14/site-packages
# ffmpeg dipakai TTS (PCM -> MP3)
export PATH=/home/ubuntu/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin:$PATH

echo "🚀 Memulai proses publish blog..."
cd /home/ubuntu/irawiki/blog

# 0. Generate ringkasan audio untuk artikel baru (belum punya audio)
echo "🎙️ Cek artikel baru untuk ringkasan audio..."
AUDIO_FAILED=()
for md_file in $(find content/posts -maxdepth 2 -name "*.md" -not -name "_index.md" | sort); do
  echo "  → $md_file"
  if ! /home/ubuntu/irawiki_venv/bin/python3 generate_audio_summary.py "$md_file" --update-frontmatter; then
    echo "  ⚠️ Gagal generate audio untuk $md_file, lanjut..."
    AUDIO_FAILED+=("$md_file")
  fi
done
if [ ${#AUDIO_FAILED[@]} -gt 0 ]; then
  echo "⚠️  ${#AUDIO_FAILED[@]} artikel gagal dapat ringkasan audio (cek log di atas):"
  printf '   - %s\n' "${AUDIO_FAILED[@]}"
fi

# 1. Generate llms.txt artikel terbaru
echo "🤖 Generate llms.txt untuk AI search & context..."
python3 generate_blog_llms.py || echo "⚠️ Gagal generate llms.txt, lanjut..."

# 2. Build web statis ke direktori Nginx
echo "⚙️  Menjalankan build Hugo..."
hugo --minify --cleanDestinationDir -d /var/www/blog

# 3. Simpan perubahan ke Git (hanya folder blog/, hindari submodule parent)
echo "📦 Menyimpan jejak perubahan ke Git..."
cd /home/ubuntu/irawiki
git add blog/

# Cek apakah ada perubahan sebelum commit
if ! git diff-index --quiet HEAD -- blog/; then
    git commit -m "Auto-publish artikel baru [skip ci]"
    git push origin main
    echo "✅ Perubahan berhasil di-commit & push."
else
    echo "ℹ️ Tidak ada perubahan baru untuk di-commit."
fi

echo "🎉 Publish selesai! Website sudah diperbarui di https://blog.iraamalia.id"
