#!/usr/bin/env bash
# Deploy 1 lệnh trên droplet: kéo code mới từ GitHub -> cập nhật app -> restart.
# Chạy:  cd /root/swan-dashboard && ./update.sh
# KHÔNG đụng tới users.json / data.json / secret (file nhạy cảm chỉ có trên server).
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
APP=/opt/swan-auth
WEBDIR=$(grep -oP '(?<=SWAN_WEB_DIR=)\S+' /etc/systemd/system/swan-auth.service | head -1)

echo ">> [1/4] Kéo code mới từ GitHub..."
git -C "$REPO" pull --ff-only

echo ">> [2/4] Cập nhật app login (giữ nguyên users.json)..."
for f in auth_app.py make_users.py requirements.txt favicon-64.png favicon-180.png favicon.svg swan-logo.png; do
  [ -f "$REPO/auth/$f" ] && cp "$REPO/auth/$f" "$APP/"
done

echo ">> [3/4] Cập nhật script pipeline (giữ nguyên data.json + dashboard.html sống)..."
if [ -n "$WEBDIR" ] && [ -d "$WEBDIR" ]; then
  for f in build_dashboard.py extract_v2.py revenue_sheet.py; do
    [ -f "$REPO/dashboard/$f" ] && cp "$REPO/dashboard/$f" "$WEBDIR/"
  done
fi

echo ">> [4/4] Cài deps (nếu đổi) + restart..."
"$APP/venv/bin/pip" install -q -r "$APP/requirements.txt" || true
systemctl restart swan-auth
sleep 1
systemctl is-active swan-auth >/dev/null && echo ">> ✅ Xong. swan-auth đang chạy." || echo ">> ⚠️ swan-auth chưa chạy — xem: journalctl -u swan-auth -n 30"
