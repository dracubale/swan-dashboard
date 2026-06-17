# BÀN GIAO — Swan Clinic CEO Dashboard

Tài liệu này tóm tắt toàn bộ dự án để bắt đầu một phiên làm việc mới. Dán nội dung này vào đầu chat mới là đủ ngữ cảnh để tiếp tục.

## 1. Dự án là gì
Bảng điều khiển vận hành cho **Swan Clinic** (thẩm mỹ, HCMC), chủ sở hữu **Trung** (thương hiệu mẹ **Hydrasignal**). Báo cáo doanh thu, ad, sale, master, bán chéo… Có **đăng nhập + phân quyền** theo người.
- **Live:** `https://hydrasignal.com/swan`
- **Code (private):** `https://github.com/dracubale/swan-dashboard`
- **Server:** droplet DigitalOcean, IP `152.42.202.17` (SSH root)

## 2. Kiến trúc
- **Dashboard** = 1 file `dashboard.html` (vanilla JS) do `build_dashboard.py` sinh ra từ `bundle.json`/`data.json`. Pipeline chạy hằng ngày (~5:45 sáng).
- **Cổng đăng nhập** = app FastAPI `auth_app.py` đứng trước dashboard. Nginx proxy `/swan/` → `127.0.0.1:8200`. Đăng nhập theo người, **lọc dữ liệu theo vai trò ở server** (xóa rỗng key của trang/khoa bị cấm). Logo + favicon được **chèn lúc serve** (không nằm trong dashboard "trần").

## 3. Đường dẫn trên droplet
- App login: `/opt/swan-auth/` (service systemd `swan-auth`, chạy uvicorn 127.0.0.1:8200)
- Web/dashboard + pipeline: `/root/swan/swan-ceo-dashboard/dashboard/` (= `SWAN_WEB_DIR`, chứa `dashboard.html`, `data.json`, `bundle.json`, các `.py`)
- Tài khoản + secret: `/etc/swan/users.json`, `/etc/swan/secret`
- Bản clone để deploy: `/root/swan-dashboard/` (clone từ GitHub)

## 4. Quy trình deploy (đã thiết lập git-pull)
1. **Windows** (trong thư mục repo `swan-repo`):
   `git add . && git commit -m "..." && git push`
2. **Droplet** (SSH vào):
   `cd /root/swan-dashboard && bash update.sh`
   → `update.sh` kéo code, copy vào `/opt/swan-auth` + `SWAN_WEB_DIR` (KHÔNG đụng `users.json`/`data.json`), **build lại `dashboard.html`** (ra thư mục tạm rồi chỉ thay HTML), restart `swan-auth`.

Lưu ý: file nhạy cảm (`data.json`, `bundle.json`, `users.json`, secret) **không lên GitHub** (đã `.gitignore`).

## 5. Tài khoản & vai trò (9 user)
- `trung`, `thanh` → **ceo** (toàn bộ, gồm Bản tin CEO)
- `thuan`, `quyen`, `mily` → **ops** (tất cả trừ Bản tin)
- `vuongngan` → **noi_ads** (Nội khoa + toàn bộ Ads)
- `duy` → **ngoai** (chỉ Ngoại khoa)
- `quynh`, `maithi` → **marketing** (chỉ Tổng quan + Nền tảng)

Mật khẩu tạm ban đầu sinh bằng `make_users.py` (giữ riêng, không để trong repo). Reset: chạy lại `make_users.py` trên droplet hoặc dùng `/change-password`.

## 6. Đã xong
- Dashboard đầy đủ + đăng nhập/phân quyền (GĐ0/1/2: lọc Nội/Ngoại + ads theo khoa).
- Logo Swan ở sidebar + favicon (chữ H trắng, nền trong suốt) — chèn lúc serve.
- Code lên GitHub, deploy git-pull 1 lệnh.
- **% thay đổi (xanh tốt / đỏ xấu) cho từng metric ở các mốc Hôm nay · Hôm qua · 3 ngày · 7 ngày · 30 ngày** — đã đưa vào `build_dashboard.py` (bền qua mỗi lần build). "Hôm nay" luôn hiện (chưa có data thì `—`); "30 ngày" sẽ ra % khi data đủ ngày.

## 7. Còn lại / ý tưởng tiếp theo
- Sửa tận gốc hàm `dlabel` trong `build_dashboard.py` (chống null khi TikTok chưa sync — hiện mới vá ở bản phục vụ).
- Tách New/Tái khám theo khoa; cột BILL CỌC (liên kết cọc); hoàn thiện `series_div`.
- Email login (hiện chỉ username); logo brand cho Hydrasignal (trang mẹ).

## 8. Lệnh hay dùng
```bash
# deploy
cd /root/swan-dashboard && bash update.sh
# xem log app
journalctl -u swan-auth -n 40
# build lại dashboard thủ công (nếu cần)
cd /root/swan/swan-ceo-dashboard/dashboard && SWAN_OUTPUT_DIR=. SWAN_BUNDLE=bundle.json python3 build_dashboard.py && cp swan_ceo_dashboard.html dashboard.html
# kiểm tra file đã đúng bản
md5sum /opt/swan-auth/favicon-64.png   # bản hiện tại: 97dc09c58d9eede01ee7745304ff030c
```

## 9. Nguyên tắc đã chốt (để không làm sai lại)
- **CSKH Online** là chăm sóc khách cũ — KHÔNG đánh giá như sale chốt, loại khỏi mọi bảng/insight chốt deal.
- Bán chéo xếp hạng theo điểm tổng hợp (bills × √attach%), không dùng % attach thuần.
- Token GitHub đã dùng để clone trên droplet — nếu lộ thì **revoke + tạo mới**.
