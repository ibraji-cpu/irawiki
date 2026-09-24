#!/bin/bash
set -e
echo "=== Wiki Pull & Rebuild ==="
cd /home/ubuntu/irawiki
echo "[1/3] Pulling from GitHub..."
git pull origin main
echo "[2/3] Rebuilding Quartz..."
bash build_wiki.sh
echo "[3/3] Done! Wiki updated."
