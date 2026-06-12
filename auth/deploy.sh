#!/usr/bin/env bash
# Cài GĐ1 lên droplet. Chạy bằng root trên server.
#   sudo bash deploy.sh [/duong/dan/web]   (nếu bỏ trống sẽ tự dò theo data.json)
set -e
WEBDIR="${1:-}"
if [ -z "$WEBDIR" ]; then
  F=$(find /var/www /usr/share/nginx /srv /opt /home /root -name 'data.json' 2>/dev/null | head -1)
  WEBDIR=$(dirname "$F")
fi
echo ">> Thư mục web (chứa dashboard.html + data.json): $WEBDIR"
[ -f "$WEBDIR/dashboard.html" ] || { echo "!! Không thấy dashboard.html trong $WEBDIR — truyền đúng đường dẫn: sudo bash deploy.sh /duong/dan"; exit 1; }

for i in $(seq 1 30); do apt-get install -y python3-venv python3-pip >/dev/null 2>&1 && break; echo ">> apt ban, doi 6s"; sleep 6; done

mkdir -p /opt/swan-auth /etc/swan
cp auth_app.py make_users.py favicon-64.png favicon-180.png favicon.svg /opt/swan-auth/
python3 -m venv /opt/swan-auth/venv
/opt/swan-auth/venv/bin/pip install -q -r requirements.txt

# secret phiên (sinh ngẫu nhiên 1 lần)
[ -f /etc/swan/secret ] || openssl rand -hex 32 > /etc/swan/secret
chmod 600 /etc/swan/secret

# kho user: dùng file kèm theo (đã có mật khẩu tạm). Không ghi đè nếu đã tồn tại.
if [ ! -f /etc/swan/users.json ]; then
  cp users.json /etc/swan/users.json
  echo ">> Đã cài users.json (mật khẩu tạm theo bảng đã gửi)."
else
  echo ">> /etc/swan/users.json đã tồn tại — giữ nguyên."
fi
chmod 600 /etc/swan/users.json

sed "s#__WEBDIR__#$WEBDIR#g" swan-auth.service > /etc/systemd/system/swan-auth.service
systemctl daemon-reload
systemctl enable swan-auth >/dev/null 2>&1 || true
systemctl restart swan-auth
sleep 2
systemctl --no-pager -l status swan-auth | head -6
echo
echo ">> App đã chạy ở 127.0.0.1:8200. Giờ sửa nginx (xem nginx-swan.location) rồi: nginx -t && systemctl reload nginx"
