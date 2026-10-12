#!/bin/bash
set -e

# concurrency-safe: non-blocking flock — skip if another build holds the lock
exec 200>/tmp/irawiki-build.lock
if ! flock -n 200; then
  echo "[!] Build already running (flock /tmp/irawiki-build.lock busy), skipping." >&2
  exit 0
fi

echo "[*] Build Quartz..."
cd /home/ubuntu/irawiki
python3 update_index.py
node ./quartz/bootstrap-cli.mjs build

echo "[✅] Selesai."
