#!/bin/bash
set -e
echo "=== Wiki Pull & Rebuild ==="
cd /home/ubuntu/irawiki
echo "[1/3] Pulling from GitHub..."
# Aman dari pohon kerja yang sedang di branch lain: `git pull origin main` akan
# me-merge main ke branch aktif dan bisa konflik, sehingga build tidak pernah jalan.
git fetch origin main
git checkout main
git reset --hard origin/main
echo "[2/3] Rebuilding Quartz..."
bash build_wiki.sh
echo "[3/3] Done! Wiki updated."
