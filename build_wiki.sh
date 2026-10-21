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
node ./quartz/bootstrap-cli.mjs build

# SEO artifacts: robots.txt, llms.txt, llms-full.txt (regenerated every build)
python3 tools/build_seo.py

# Notifikasi update wiki -> blog/data/wiki_updates.json (jangan gagalkan deploy)
python3 tools/wiki_update_notify.py || echo "[!] wiki_update_notify gagal, notifikasi dilewati" >&2

echo "[✅] Selesai."
