#!/bin/bash
# Watcher pantauan konten: branch konten/pantauan-* -> branch kerja hermes/pantauan-*
# -> Pull Request ke main. Deploy Quartz + indexer HANYA setelah user merge PR.
# Dijalankan tiap hari 06:00 WIB oleh cron Hermes (job pantauan-watcher).
set -uo pipefail

REPO=/home/ubuntu/irawiki
LOG=/home/ubuntu/irawiki/logs/pantau-konten.log
PY=/usr/bin/python3

mkdir -p "$(dirname "$LOG")"

exec 9>/tmp/pantau-konten.lock
if ! flock -n 9; then
  echo "$(date '+%F %T') [skip] watcher lain sedang jalan" >>"$LOG"
  exit 0
fi

cd "$REPO" || exit 1
# Jalankan watcher. Jika ada laporan, cetak ke stdout (diteruskan ke telegram/cron) dan log.
REPORT=$($PY tools/pantau_konten_watcher.py "$@")
rc=$?

if [ -n "$REPORT" ]; then
  echo "$REPORT"
  echo "=== $(date '+%F %T %Z') (rc=$rc) ===" >>"$LOG"
  echo "$REPORT" >>"$LOG"
fi

exit $rc
