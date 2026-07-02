# -*- coding: utf-8 -*-
# Sửa dayrec_div: gross theo khoa phải = doanh thu thuần + cọc (gồm cọc),
# đồng bộ với dayrec overview. Hiện đang gross=revenue → tooltip "Tổng (gồm cọc)" sai.
# Đây là thay đổi PIPELINE → sau khi vá phải refresh_daily (extract+build). Idempotent.
import io, sys, os
PATH = 'extract_v2.py'
if not os.path.exists(PATH):
    sys.exit(f'Không thấy {PATH} trong: {os.getcwd()}')
txt = io.open(PATH, encoding='utf-8').read()

old = "return dict(date=d,gross=revenue,operating=revenue,revenue=revenue,deposit=int(round(_depv)),cash_in=revenue+_depv,"
new = "return dict(date=d,gross=revenue+_depv,operating=revenue,revenue=revenue,deposit=int(round(_depv)),cash_in=revenue+_depv,"

if "gross=revenue+_depv,operating=revenue" in txt:
    print('Đã vá trước đó. Bỏ qua.'); sys.exit(0)
if old not in txt:
    sys.exit('KHÔNG khớp dòng return của dayrec_div (file đã đổi?).')
if txt.count(old) != 1:
    sys.exit(f'Đoạn xuất hiện {txt.count(old)} lần, cần 1.')

txt = txt.replace(old, new)
io.open(PATH, 'w', encoding='utf-8', newline='').write(txt)
print('✓ Đã vá dayrec_div: gross theo khoa = doanh thu thuần + cọc.')
print('  Đây là đổi pipeline → chạy refresh_daily.sh (extract + build), không chỉ render.')
