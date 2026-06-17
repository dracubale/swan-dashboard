# -*- coding: utf-8 -*-
"""Do cau truc Google Sheet BK Phau: liet ke tab, header va vai dong mau.
Dung: python bk_inspect.py "<URL hoac ID cua sheet BK Phau>"
"""
import sys
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA = "/root/swan/swan-drive-bot.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

arg = sys.argv[1] if len(sys.argv) > 1 else ""
want_tab = sys.argv[2] if len(sys.argv) > 2 else ""   # tuy chon: ten tab muon doc
m = re.search(r"/spreadsheets/d/([A-Za-z0-9_-]+)", arg)
SID = m.group(1) if m else arg.strip()   # cho phep dan thang URL hoac ID
if not SID:
    print("Thieu URL/ID. Dung: python bk_inspect.py \"<URL>\" [ten_tab]")
    sys.exit(1)
print("SPREADSHEET_ID:", SID)

creds = service_account.Credentials.from_service_account_file(SA, scopes=SCOPES)
svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
meta = svc.spreadsheets().get(spreadsheetId=SID).execute()
titles = [s["properties"]["title"] for s in meta["sheets"]]
print("TABS:", titles)


def norm(s):
    return s.lower().replace(" ", "")


tab = None
if want_tab:   # uu tien tab nguoi dung chi dinh (khop gan dung)
    for t in titles:
        if norm(want_tab) in norm(t):
            tab = t
            break
    if tab is None:
        print("!! Khong thay tab khop %r, doc tab dau tien." % want_tab)
if tab is None:
    for t in titles:
        if "bkph" in norm(t):
            tab = t
            break
if tab is None:
    tab = titles[0]
print("DUNG TAB:", repr(tab))

v = svc.spreadsheets().values().get(
    spreadsheetId=SID, range="'" + tab + "'"
).execute().get("values", [])
print("SO DONG:", len(v))
if v:
    print("--- HEADER ---")
    for i, h in enumerate(v[0]):
        print("  [%d] %r" % (i, h))
    print("--- 5 DONG MAU ---")
    for i, r in enumerate(v[1:6], 1):
        print("ROW%d:" % i, r)
