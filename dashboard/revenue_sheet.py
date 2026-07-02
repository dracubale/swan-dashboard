# -*- coding: utf-8 -*-
"""Doc doanh thu TRUC TIEP tu Google Sheet (live), tra ve DataFrame giong het
pd.read_excel(MNG.xlsx, sheet_name='BCngay- T06', header=0).rename(strip)
-> de ghep thang vao extract_v2 (thay cho buoc doc xls)."""
import os
import re
import datetime
import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ.get("SWAN_SPREADSHEET_ID", "1eWXLcT0UY9ny9VbJsOu73tja8sFzAucWNoFYC1oiCv8")
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "/root/swan/swan-drive-bot.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# cac cot tien dinh dang VN ("35.000,000") -> can chuyen sang so
MONEY_COLS = ["GIÁ TRỊ BILL", "CHUYỂN KHOẢN", "THẺ", "TIỀN  MẶT", "TIỀN MẶT", "CỌC"]


def _svc():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _find_tab(svc):
    meta = svc.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    titles = [s["properties"]["title"] for s in meta["sheets"]]
    # [findtab2] khop khong phan biet hoa/thuong + bo dau cach: 'BCNGAY - T07' cung nhan
    mm = datetime.datetime.now().strftime("%m")
    def _norm(x):
        return "".join(str(x).lower().split())
    wants = ["t" + mm, "t" + str(int(mm))]   # 'T07' va 'T7'
    for t in titles:
        n = _norm(t)
        if n.startswith("bcng") and any(w in n for w in wants):
            return t
    raise RuntimeError("Khong tim thay tab BCngay thang hien tai. Tabs: %r" % titles)


def _vn_num(v):
    s = str(v).strip()
    if s == "" or s.lower() == "nan":
        return np.nan
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan


def _vn_date(v):
    s = str(v).strip()
    m = re.match(r"^(\d{1,2})/(\d{1,2})", s)
    if not m:
        return pd.NaT
    d, mo = int(m.group(1)), int(m.group(2))
    try:
        return pd.Timestamp(year=datetime.datetime.now().year, month=mo, day=d)
    except ValueError:
        return pd.NaT


def load_revenue_df():
    """Tra ve DataFrame y het pd.read_excel(...).rename(strip): cot da strip,
    o trong = NaN, NGAY = datetime, cot tien = so. Dong 0 = dong tong ket (extract_v2 se .iloc[1:])."""
    svc = _svc()
    tab = _find_tab(svc)
    resp = svc.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range="'" + tab + "'"
    ).execute()
    values = resp.get("values", [])
    if not values:
        raise RuntimeError("Sheet rong")
    header = [str(h).strip() for h in values[0]]
    width = len(header)
    rows = []
    for r in values[1:]:
        r = list(r) + [""] * (width - len(r))   # pad dong ngan
        rows.append(r[:width])
    df = pd.DataFrame(rows, columns=header)
    df = df.replace("", np.nan)                  # o trong -> NaN (giong pd.read_excel)
    if "NGÀY" in df.columns:
        df["NGÀY"] = df["NGÀY"].apply(_vn_date)
    for c in MONEY_COLS:
        if c in df.columns:
            df[c] = df[c].apply(_vn_num)
    return df


if __name__ == "__main__":
    df = load_revenue_df()
    print("Shape:", df.shape)
    print("So cot:", len(df.columns))
    d = df.iloc[1:].copy()                       # bo dong tong ket, giong extract_v2
    d["NGÀY"] = pd.to_datetime(d["NGÀY"], errors="coerce").ffill()
    print("Ngay min -> max:", str(d["NGÀY"].min()), "->", str(d["NGÀY"].max()))
    rev = pd.to_numeric(d["GIÁ TRỊ BILL"], errors="coerce").fillna(0.0).sum()
    cust = int((pd.to_numeric(d["Tính khách?"], errors="coerce") == 1).sum())
    print("Doanh thu (sum GIA TRI BILL):", "{:,.0f}".format(rev), "| muc tieu 4,304,240")
    print("So khach (Tinh khach=1):", cust, "| muc tieu 180")
