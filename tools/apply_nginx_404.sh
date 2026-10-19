#!/bin/bash
# Terapkan konfigurasi nginx anti-soft-404 untuk wiki.iraamalia.id.
# Idempoten: membackup konfigurasi lama, memasang yang baru, menguji, lalu reload.
set -euo pipefail

SRC="/home/ubuntu/irawiki/deploy/nginx-wiki.conf"
DST="/etc/nginx/sites-available/wiki.iraamalia.id"
STAMP=$(date +%Y%m%d-%H%M%S)

if [[ $EUID -ne 0 ]]; then
  echo "Harus root: sudo bash $0" >&2
  exit 1
fi

[[ -f "$SRC" ]] || { echo "Sumber tidak ada: $SRC" >&2; exit 1; }

if ! cmp -s "$SRC" "$DST"; then
  cp -a "$DST" "/etc/nginx/sites-available/wiki.iraamalia.id.bak-$STAMP"
  install -m 644 -o root -g root "$SRC" "$DST"
  echo "[+] Konfigurasi dipasang (backup: $DST.bak-$STAMP)"
else
  echo "[=] Konfigurasi sudah sama, tidak ada perubahan."
fi

nginx -t
systemctl reload nginx
echo "[✅] nginx reloaded"
