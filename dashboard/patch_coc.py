# -*- coding: utf-8 -*-
# Vá lỗi GHÉP CỌC chết: khoá bill cọc là chuỗi ('3184') còn coc_link là số (2691.0)
# → 'coc_link in dep_amount' không bao giờ khớp → 0 ca ghép. Chuẩn hoá khoá bằng _bk().
# Chạy TRONG thư mục chứa extract_v2.py (repo Windows hoặc droplet). Idempotent.
import io, sys, os

PATH = 'extract_v2.py'
if not os.path.exists(PATH):
    sys.exit(f'Không thấy {PATH} trong thư mục hiện tại: {os.getcwd()}')

txt = io.open(PATH, encoding='utf-8').read()
nl = '\r\n' if '\r\n' in txt else '\n'

if 'def _bk(' in txt:
    print('Đã vá trước đó (thấy _bk). Bỏ qua.'); sys.exit(0)

bk = nl.join([
    "def _bk(x):                                  # chuan hoa khoa bill (BILLL str vs CỌC float)",
    "    try:",
    "        if pd.isna(x): return None",
    "        return str(int(float(x)))",
    "    except (ValueError, TypeError):",
    "        s = str(x).strip(); return s or None",
    "",
])

reps = [
    # 1) thêm _bk + chuẩn hoá khoá dep_amount
    ("dep_amount=B[B.is_deposit].set_index('bill')['gross'].to_dict()",
     bk + "dep_amount={_bk(k):v for k,v in B[B.is_deposit].set_index('bill')['gross'].to_dict().items()}"),
    # 2a) điều kiện ghép theo khoá chuẩn
    ("    if r['coc_link'] is not None and r['coc_link'] in dep_amount:",
     "    k=_bk(r['coc_link'])" + nl + "    if k is not None and k in dep_amount:"),
    # 2b) thân hàm dùng k
    ("        _realized.add(r['coc_link']); return float(dep_amount[r['coc_link']])",
     "        _realized.add(k); return float(dep_amount[k])"),
    # 3) gỡ bill cọc đã thực hiện — so khớp theo khoá chuẩn
    ("B.loc[B['bill'].isin(_realized),['is_deposit','is_rev','is_zero']]=False",
     "B.loc[B['bill'].apply(_bk).isin(_realized),['is_deposit','is_rev','is_zero']]=False"),
]

for old, new in reps:
    if old not in txt:
        sys.exit(f'KHÔNG khớp đoạn cần vá (file đã đổi?):\n  {old}')
    if txt.count(old) != 1:
        sys.exit(f'Đoạn xuất hiện {txt.count(old)} lần, cần đúng 1:\n  {old}')
    txt = txt.replace(old, new)

io.open(PATH, 'w', encoding='utf-8', newline='').write(txt)
print('✓ Đã vá extract_v2.py (4 chỗ): _bk + dep_amount + _coc_add + gỡ pipeline.')
print('  Kiểm tra cú pháp: python -m py_compile extract_v2.py')
print('  Sau đó: refresh_daily.sh (đổi pipeline, không chỉ render).')
