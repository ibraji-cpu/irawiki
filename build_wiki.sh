#!/bin/bash
set -e

echo "[*] Build Quartz..."
cd /home/ubuntu/irawiki
node ./quartz/bootstrap-cli.mjs build

echo "[✅] Selesai."
