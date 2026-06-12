# Swan Clinic — CEO Dashboard + Cổng phân quyền

Bảng điều khiển vận hành cho Swan Clinic (Hydrasignal). Gồm 2 phần:

## `dashboard/` — Pipeline dựng dashboard
- `extract_v2.py`, `revenue_sheet.py` — trích & chuẩn hóa dữ liệu (Google Sheets doanh thu, Meta/TikTok Ads) → `data.json`.
- `build_dashboard.py` — dựng `dashboard.html` (1 file, vanilla JS): tổng quan, dịch vụ, nền tảng (Meta vs TikTok), sale, master, bán chéo, bản tin CEO.
- `dashboard.html` ở đây đã **xóa số liệu nhúng** (chỉ còn khung giao diện).

## `auth/` — Cổng đăng nhập + phân quyền (FastAPI)
Đặt trước dashboard tĩnh: đăng nhập theo người, lọc dữ liệu theo vai trò **ở server** (xóa rỗng key của trang/khoa bị cấm).
- `auth_app.py` — app chính (login, session, `/data.json` đã lọc, favicon).
- Vai trò: CEO · QL vận hành · QL Nội/Ngoại khoa · QL Ads · QL Marketing.
- `make_users.py` — sinh kho tài khoản + mật khẩu tạm.
- `deploy.sh`, `swan-auth.service`, `nginx-swan.location` — cài đặt trên VPS.

## Cài đặt nhanh (VPS Ubuntu)
```bash
cd auth
python3 make_users.py            # sinh users.json (mật khẩu tạm)
sudo bash deploy.sh /duong/dan/web
# sửa nginx theo nginx-swan.location, rồi: nginx -t && systemctl reload nginx
```

## ⚠️ Bảo mật
- **Không commit**: `data.json`, `bundle.json` (doanh thu thật), `auth/users.json` (hash mật khẩu), `secret`, file Excel/CSV nguồn. Đã đưa vào `.gitignore`.
- Khuyến nghị đặt repo ở chế độ **Private**.
