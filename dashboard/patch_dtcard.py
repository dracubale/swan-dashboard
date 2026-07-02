# -*- coding: utf-8 -*-
# Đổi headline card "Doanh thu" (gatesInner) sang GỒM CỌC (cash-in = đã làm + cọc).
# Giữ ROAS/Chi-DS trên doanh thu THẬT (rev=operating); thêm dòng tách "Đã làm · Cọc".
# Chỉ đổi render → deploy bằng update.sh, KHÔNG cần refresh_daily. Idempotent.
import io, sys, os
PATH = 'build_dashboard.py'
if not os.path.exists(PATH):
    sys.exit(f'Không thấy {PATH} trong: {os.getcwd()}')
txt = io.open(PATH, encoding='utf-8').read()

old_dt = "const DT={ic:'rev',name:'Doanh thu',sub:'Doanh thu đã làm',big:tyS(rev),\n"
old_rows = "    rows:row('ROAS · Chi/DS',`${spend?(rev/spend).toFixed(1):'—'}x · ${rev?pct(spend,rev).toFixed(1):'—'}%`)+row('AOV · trung vị',"

if "sub:'Gồm cọc (cash-in)'" in txt:
    print('Đã vá trước đó. Bỏ qua.'); sys.exit(0)

# tìm linh hoạt theo CRLF/LF
import re
m = re.search(r"const DT=\{ic:'rev',name:'Doanh thu',sub:'Doanh thu đã làm',big:tyS\(rev\),", txt)
if not m:
    sys.exit('KHÔNG khớp dòng khai báo card DT (file đã đổi?).')
txt = txt.replace(
    "const DT={ic:'rev',name:'Doanh thu',sub:'Doanh thu đã làm',big:tyS(rev),",
    "const DT={ic:'rev',name:'Doanh thu',sub:'Gồm cọc (cash-in)',big:tyS(rev+dep),")

# chèn dòng tách "Đã làm · Cọc" vào đầu rows
anchor = "rows:row('ROAS · Chi/DS',"
if anchor not in txt:
    sys.exit('KHÔNG khớp anchor rows của card DT.')
if txt.count(anchor) != 1:
    sys.exit(f'anchor xuất hiện {txt.count(anchor)} lần, cần 1.')
txt = txt.replace(anchor, "rows:row('Đã làm · Cọc',`${tr(rev)} · ${tr(dep)}`)+row('ROAS · Chi/DS',", 1)

io.open(PATH, 'w', encoding='utf-8', newline='').write(txt)
print('✓ Đã vá build_dashboard.py: headline Doanh thu = GỒM CỌC; thêm dòng "Đã làm · Cọc".')
print('  Deploy: update.sh (render-only, không cần refresh_daily).')
