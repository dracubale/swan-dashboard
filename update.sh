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

echo ">> [3/5] Cập nhật script pipeline (giữ nguyên data.json + dashboard.html sống)..."
if [ -n "$WEBDIR" ] && [ -d "$WEBDIR" ]; then
  for f in build_dashboard.py extract_v2.py revenue_sheet.py; do
    [ -f "$REPO/dashboard/$f" ] && cp "$REPO/dashboard/$f" "$WEBDIR/"
  done
fi

echo ">> [4/5] Build lại dashboard.html (front-end) từ build_dashboard.py..."
# An toàn: build ra thư mục TẠM (không đụng data.json thật), chỉ thay phần HTML.
if [ -n "$WEBDIR" ] && [ -f "$WEBDIR/build_dashboard.py" ] && [ -f "$WEBDIR/bundle.json" ]; then
  TMP=$(mktemp -d)
  if ( cd "$WEBDIR" && SWAN_OUTPUT_DIR="$TMP" SWAN_BUNDLE="$WEBDIR/bundle.json" python3 build_dashboard.py >/dev/null 2>&1 ) && [ -s "$TMP/swan_ceo_dashboard.html" ]; then
    cp "$TMP/swan_ceo_dashboard.html" "$WEBDIR/dashboard.html"
    echo ">>    dashboard.html đã build lại ($(wc -c < "$WEBDIR/dashboard.html") bytes)."
  else
    echo ">>    ⚠️ Build lại lỗi — giữ dashboard.html cũ. Chạy tay để xem lỗi:"
    echo ">>       cd $WEBDIR && SWAN_OUTPUT_DIR=. SWAN_BUNDLE=bundle.json python3 build_dashboard.py"
  fi
  rm -rf "$TMP"
else
  echo ">>    (Bỏ qua build lại: thiếu build_dashboard.py hoặc bundle.json trong $WEBDIR — sẽ áp dụng ở lần pipeline kế.)"
fi

echo ">> [5/5] Cài deps (nếu đổi) + restart..."
"$APP/venv/bin/pip" install -q -r "$APP/requirements.txt" || true
systemctl restart swan-auth
sleep 1
systemctl is-active swan-auth >/dev/null && echo ">> ✅ Xong. swan-auth đang chạy." || echo ">> ⚠️ swan-auth chưa chạy — xem: journalctl -u swan-auth -n 30"
