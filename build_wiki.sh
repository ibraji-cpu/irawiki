#!/bin/bash
set -e

echo "[*] Build Quartz..."
cd /home/ubuntu/irawiki
python3 update_index.py
node ./quartz/bootstrap-cli.mjs build

echo "[✅] Selesai."
