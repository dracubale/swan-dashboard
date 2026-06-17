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
# vi tri cot (0-based)
C_SALE, C_NGUON, C_LOAI, C_NGAYCHOT = 0, 1, 2, 3
C_TEN, C_SDT, C_SL, C_DV = 4, 5, 6, 7
C_NGAYHEN, C_TRANGTHAI, C_NHAC = 12, 14, 15


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

    width = 16
    rows = []
    cur_day = pd.NaT   # ngay tu dong ngan gan nhat (de ffill khi cot 12 trong)
    for r in values[1:]:               # values[0] = header
        r = list(r) + [""] * (width - len(r))
        r = r[:width]
        if _is_separator(r):
            cur_day = _vn_date(r[C_SALE], year)
            continue
        ten = (r[C_TEN] or "").strip()
        sdt = (r[C_SDT] or "").strip()
        if not ten and not sdt:
            continue                    # dong trong
        hen = _vn_date(r[C_NGAYHEN], year)
        if pd.isna(hen):
            hen = cur_day               # ffill tu dong ngan ngay
        rows.append(dict(
            sale=map_sale(r[C_SALE]),
            nguon=(r[C_NGUON] or "").strip() or None,
            loai_khach=(r[C_LOAI] or "").strip() or None,
            ngay_chot=_vn_date(r[C_NGAYCHOT], year),
            ten=ten or None,
            phone=norm_phone(r[C_SDT]),
            sl=(r[C_SL] or "").strip() or None,
            dich_vu=(r[C_DV] or "").strip() or None,
            ngay_hen=hen,
            trang_thai_raw=(r[C_TRANGTHAI] or "").strip() or None,
            nhac_lich=(r[C_NHAC] or "").strip() or None,
            status=parse_status(r[C_TRANGTHAI], r[C_NHAC]),
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
