# -*- coding: utf-8 -*-
"""Doc Google Sheet BK Phau (lead pipeline Ngoai khoa) -> DataFrame sach.

- Tab goc = 'BK Phau' (cac tab 'Phau thuat' / 'Coc - Follow' chi la ban loc con).
- Dong tong (351.000.000) nam TREN header -> tu dong tim dong header chua 'Ngay hen'.
- Cot 'Doanh thu' o day = coc + phau tron lan -> KHONG dung lam doanh thu that;
  doanh thu chot that van lay tu revenue sheet (BCngay), join bang SDT chuan hoa.
- Tien o day la VND DAY DU ('3.000.000 ₫' = 3,000,000) -> KHONG nhan 1000 nhu revenue sheet.
"""
import os
import re
import datetime
import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.environ.get("SWAN_BKPHAU_ID", "198pRrBbdS1sEyrujlVKI6IKStCO3_KAOsnpIdVPvrr8")
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "/root/swan/swan-drive-bot.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
TAB_HINT = "bkph"   # normalize (bo dau cach, lower) -> chua chuoi nay


def _svc():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _find_tab(svc):
    meta = svc.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    titles = [s["properties"]["title"] for s in meta["sheets"]]
    for t in titles:
        if TAB_HINT in t.lower().replace(" ", ""):
            return t
    raise RuntimeError("Khong tim thay tab BK Phau. Tabs: %r" % titles)


def _vn_money(v):
    """'3.000.000 ₫' -> 3000000.0 (VND day du). o trong -> NaN."""
    s = str(v).strip()
    if s == "" or s.lower() == "nan":
        return np.nan
    s = re.sub(r"[^\d,.\-]", "", s)   # bo ₫, khoang trang, chu
    if s == "":
        return np.nan
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan


def _vn_date(v):
    """'27/05/2026' hoac '27/05' -> Timestamp. Thieu nam -> nam hien tai."""
    s = str(v).strip()
    m = re.match(r"^(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", s)
    if not m:
        return pd.NaT
    d, mo = int(m.group(1)), int(m.group(2))
    y = m.group(3)
    if y:
        y = int(y)
        if y < 100:
            y += 2000
    else:
        y = datetime.datetime.now().year
    try:
        return pd.Timestamp(year=y, month=mo, day=d)
    except ValueError:
        return pd.NaT


def norm_phone(v):
    """Chuan hoa SDT de join voi revenue sheet. Khong phai so -> ''."""
    s = re.sub(r"\D", "", str(v))   # chi giu chu so
    if not s:
        return ""
    if s.startswith("84"):
        s = "0" + s[2:]
    if not s.startswith("0"):
        s = "0" + s
    return s


def _stage(v):
    """Tinh trang -> stage chuan. Trong = 'booked'."""
    s = str(v).strip()
    if s == "" or s.lower() == "nan":
        return "booked"
    return s


def load_bkphau_df():
    """Tra ve DataFrame: giu nguyen cot goc + them cot dan xuat:
    _ngay_hen, _ngay_chot (datetime) | _doanhthu (VND) | _phone (chuan hoa) | _stage."""
    svc = _svc()
    tab = _find_tab(svc)
    resp = svc.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range="'" + tab + "'"
    ).execute()
    values = resp.get("values", [])
    if not values:
        raise RuntimeError("Sheet BK Phau rong")

    # tu dong dong header (dong chua 'Ngày hẹn'); dong tong nam phia tren se bi bo
    hidx = 0
    for i, row in enumerate(values[:6]):
        if any(str(c).strip() == "Ngày hẹn" for c in row):
            hidx = i
            break
    header = [str(h).strip() for h in values[hidx]]
    width = len(header)

    rows = []
    for r in values[hidx + 1:]:
        r = list(r) + [""] * (width - len(r))   # pad dong ngan
        rows.append(r[:width])                   # cat phan thua (note ngoai cot)
    df = pd.DataFrame(rows, columns=header)
    df = df.replace("", np.nan)
    df = df.dropna(how="all").reset_index(drop=True)   # bo dong trong hoan toan

    if "Ngày hẹn" in df.columns:
        df["_ngay_hen"] = df["Ngày hẹn"].apply(_vn_date)
    if "Ngày chốt" in df.columns:
        df["_ngay_chot"] = df["Ngày chốt"].apply(_vn_date)
    if "Doanh thu" in df.columns:
        df["_doanhthu"] = df["Doanh thu"].apply(_vn_money)
    if "SĐT" in df.columns:
        df["_phone"] = df["SĐT"].apply(norm_phone)
    if "Tình trạng" in df.columns:
        df["_stage"] = df["Tình trạng"].apply(_stage)

    return df


if __name__ == "__main__":
    df = load_bkphau_df()
    print("Shape:", df.shape)
    print("Cot:", list(df.columns))
    if "_stage" in df.columns:
        print("\n--- Tinh trang (stage) ---")
        print(df["_stage"].value_counts())
    if "_ngay_hen" in df.columns:
        print("\nNgay hen min -> max:", str(df["_ngay_hen"].min()), "->", str(df["_ngay_hen"].max()))
    if "Telesale" in df.columns:
        print("\n--- Telesale (sale Ngoai) ---")
        print(df["Telesale"].value_counts())
    if "_doanhthu" in df.columns:
        print("\nTong 'Doanh thu' BK (coc+phau, KHONG = DT that):",
              "{:,.0f}".format(df["_doanhthu"].fillna(0).sum()))
    if "_phone" in df.columns:
        print("So dong co SDT hop le:", int((df["_phone"].astype(str).str.len() >= 9).sum()), "/", len(df))
