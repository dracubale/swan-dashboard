# -*- coding: utf-8 -*-
"""Doc Google Sheet LLV (lich lam viec / booking) -> DataFrame 1 dong = 1 lich hen.

- Tu dong tim tab thang hien tai: 'LLV T<thang>/<nam>' (vd 'LLV T6/2026').
- Bo dong ngan ngay ('THU 2 - 1/6/2026...') va dong trong; chi giu dong co Ten/SDT.
- Map cot theo VI TRI (header lech o dau):
  0=sale | 1=nguon | 2=loai khach | 3=ngay chot | 4=ten | 5=sdt | 6=SL |
  7=dich vu | 8=DV thuc hien | 9=note | 10=bill | 11=gio | 12=NGAY HEN |
  13=e kip | 14=TRANG THAI | 15=nhac lich
- Trang thai (text, cot O): 'x'=den | chua 'rot'=den+rot | trong+ 'doi'(nhac lich)=doi lich | trong=no-show.
"""
import os
import re
import datetime
import unicodedata
import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ.get("SWAN_LLV_ID", "1hbkMufVmjTnq4hCvvvsOVslGX-gC1iTnEQuctA_pfdA")
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "/root/swan/swan-drive-bot.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# gom ten sale ve chuan (key = ten da bo dau cau + bo dau tieng Viet + lower)
CANON = {
    "yn": "YN", "ynhi": "YN", "ynhii": "YN",
    "miao": "Linh", "linh": "Linh",
    "mai": "Mai", "maii": "Mai",
    "mai thi": "Mai Thi", "maithi": "Mai Thi",   # team MKT/KOL, KHONG phai sale Mai
    "thu": "CSKH", "cskh": "CSKH",
    "chau": "Bảo Châu", "bao chau": "Bảo Châu",
    "bich linh": "Bích Linh",
    "hoang ly": "Hoàng Ly",
    "tram": "Trâm",
    "ha": "Hà",
    "vy": "Vy",   # sale cu da nghi
}
# vi tri cot MAC DINH (0-based) - chi dung khi khong do duoc theo ten header
C_SALE, C_NGUON, C_LOAI, C_NGAYCHOT = 1, 2, 3, 4
C_TEN, C_SDT, C_SL, C_DV = 5, 6, 7, 8
C_NGAYHEN, C_TRANGTHAI, C_NHAC = 13, 15, 16

# [llvcols] Do cot theo TEN header -> ben vung khi sheet them/bot/xe dich cot.
def _hn(h):
    h = unicodedata.normalize('NFKD', str(h))
    h = ''.join(c for c in h if not unicodedata.combining(c))
    return ' '.join(h.lower().split())   # gom moi khoang trang (\n \xa0...) ve 1 space
def _find_cols(header):
    H = [_hn(h) for h in header]
    def find(*keys):
        for i, h in enumerate(H):
            if h and any(k in h for k in keys):
                return i
        return None
    c = {}
    c['nguon']     = find('nguon')
    c['loai']      = find('loai khach', 'loai')
    c['ngaychot']  = find('ngay chot', 'chot')
    c['ten']       = find('ho va ten', 'ho ten', 'ten')
    c['sdt']       = find('dien thoai', 'so dt', 'sdt')
    c['sl']        = find('sl khach', 'sl')
    c['dv']        = find('dich vu')          # 'DICH VU' dau tien
    c['thoigian']  = find('thoi gian')
    c['master']    = find('bac si', 'master', 'ktv')
    c['trangthai'] = find('trang thai', 'tinh trang')
    c['nhac']      = find('nhac lich', 'nhac')
    # 2 cot header TRONG -> suy theo hang xom co ten:
    c['sale']    = (c['nguon'] - 1) if c['nguon'] else C_SALE   # cot ngay truoc NGUON
    if c['master'] is not None:     c['ngayhen'] = c['master'] - 1   # cot ngay truoc BAC SI-MASTER
    elif c['thoigian'] is not None: c['ngayhen'] = c['thoigian'] + 1
    else:                           c['ngayhen'] = C_NGAYHEN
    # fallback mac dinh neu thieu ten
    _fb = {'sale':C_SALE,'nguon':C_NGUON,'loai':C_LOAI,'ngaychot':C_NGAYCHOT,'ten':C_TEN,
           'sdt':C_SDT,'sl':C_SL,'dv':C_DV,'ngayhen':C_NGAYHEN,'trangthai':C_TRANGTHAI,'nhac':C_NHAC}
    for k, v in _fb.items():
        if c.get(k) is None: c[k] = v
    return c


def _norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def _svc():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _find_tab(svc, month=None, year=None):
    now = datetime.datetime.now()
    m = month or now.month
    meta = svc.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    titles = [s["properties"]["title"] for s in meta["sheets"]]
    want = "llvt%d/" % m
    for t in titles:
        if want in _norm(t).replace(" ", ""):
            return t
    raise RuntimeError("Khong tim thay tab 'LLV T%d/...'. Tabs: %r" % (m, titles))


def _vn_date(v, year=None):
    s = str(v).strip()
    m = re.search(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", s)
    if not m:
        return pd.NaT
    d, mo = int(m.group(1)), int(m.group(2))
    y = m.group(3)
    if y:
        y = int(y)
        if y < 100:
            y += 2000
    else:
        y = year or datetime.datetime.now().year
    try:
        return pd.Timestamp(year=y, month=mo, day=d)
    except ValueError:
        return pd.NaT


def norm_phone(v):
    s = re.sub(r"\D", "", str(v))
    if not s:
        return ""
    if s.startswith("84"):
        s = "0" + s[2:]
    if not s.startswith("0"):
        s = "0" + s
    return s


def _canon_one(tok):
    t = re.sub(r"[^\w\s]", "", tok).strip()   # bo dau cau (vd 'YN.')
    return CANON.get(_norm(t), t.strip() or None)


def map_sale(raw):
    """Cot sale co the nhieu ten (xuong dong, '/', '+'). Gom chuan, bo CSKH, lay sale that."""
    parts = re.split(r"[\n/+]+", str(raw))
    names = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        c = _canon_one(p)
        if c:
            names.append(c)
    sales = [n for n in names if _norm(n) != "cskh"]
    if sales:
        return sales[0]
    return names[0] if names else None


def parse_status(tt, nhac):
    """-> 'arrived' | 'rot' | 'doi' | 'noshow'."""
    t = _norm(tt)
    if "rot" in t:            # 'rot' / 'x / rot'
        return "rot"          # co den nhung tu van rot
    if t.startswith("x"):
        return "arrived"      # co den
    n = _norm(nhac)
    if "doi" in n:
        return "doi"          # doi lich (khong tinh no-show)
    return "noshow"           # trong = khong den


def _is_separator(row):
    """Dong ngan ngay: co 'THU'/'CN' o cot 0 va khong co ten/sdt."""
    c0 = _norm(row[C_SALE]) if len(row) > C_SALE else ""
    ten = row[C_TEN].strip() if len(row) > C_TEN and row[C_TEN] else ""
    sdt = row[C_SDT].strip() if len(row) > C_SDT and row[C_SDT] else ""
    if ten or sdt:
        return False
    return c0.startswith("thu") or c0.startswith("cn") or ("/" in c0 and any(ch.isdigit() for ch in c0))


def load_llv_df(month=None, year=None):
    svc = _svc()
    tab = _find_tab(svc, month, year)
    resp = svc.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range="'" + tab + "'"
    ).execute()
    values = resp.get("values", [])
    if not values:
        raise RuntimeError("Tab LLV rong: %s" % tab)

    # [llvcols] do cot theo ten header cua CHINH tab nay
    C = _find_cols(values[0])
    width = max(len(values[0]), max(C.values()) + 1, 18)
    rows = []
    cur_day = pd.NaT   # ngay tu dong gan nhat (ffill khi 1 dong thieu ngay hen)
    for r in values[1:]:               # values[0] = header
        r = list(r) + [""] * (width - len(r))
        r = r[:width]
        ten = (r[C['ten']] or "").strip()
        sdt = (r[C['sdt']] or "").strip()
        if not ten and not sdt:
            d = _vn_date(r[C['ngayhen']], year)   # dong ngan/trong: cap nhat ngay neu co
            if pd.notna(d): cur_day = d
            continue                              # dong trong
        hen = _vn_date(r[C['ngayhen']], year)
        if pd.isna(hen):
            hen = cur_day               # ffill tu dong gan nhat
        rows.append(dict(
            sale=map_sale(r[C['sale']]),
            nguon=(r[C['nguon']] or "").strip() or None,
            loai_khach=(r[C['loai']] or "").strip() or None,
            ngay_chot=_vn_date(r[C['ngaychot']], year),
            ten=ten or None,
            phone=norm_phone(r[C['sdt']]),
            sl=(r[C['sl']] or "").strip() or None,
            dich_vu=(r[C['dv']] or "").strip() or None,
            ngay_hen=hen,
            trang_thai_raw=(r[C['trangthai']] or "").strip() or None,
            nhac_lich=(r[C['nhac']] or "").strip() or None,
            status=parse_status(r[C['trangthai']], r[C['nhac']]),
        ))
    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = load_llv_df()
    print("Tab thang hien tai | so lich hen:", len(df))
    if not len(df):
        raise SystemExit
    print("\n--- status ---")
    print(df["status"].value_counts())
    print("\nNgay hen min -> max:", str(df["ngay_hen"].min()), "->", str(df["ngay_hen"].max()))
    print("\n--- nguon ---")
    print(df["nguon"].value_counts(dropna=False).head(10))
    print("\n--- theo sale (no-show & rot) ---")
    piv = df.pivot_table(index="sale", columns="status", aggfunc="size", fill_value=0)
    cols = [c for c in ["arrived", "rot", "noshow", "doi"] if c in piv.columns]
    piv["total"] = piv[cols].sum(axis=1)
    print(piv[cols + ["total"]].sort_values("total", ascending=False))
    print("\nSo dong co SDT hop le:", int((df["phone"].astype(str).str.len() >= 9).sum()), "/", len(df))
