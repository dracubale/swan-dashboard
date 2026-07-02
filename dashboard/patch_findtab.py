# -*- coding: utf-8 -*-
"""patch_findtab.py - _find_tab ben vung: khong phan biet HOA/thuong + bo dau cach.
Nhan duoc 'BCngay- T06', 'BCNGAY - T07', 'BC ngay -T7',... cho moi thang.
Idempotent."""
import io, sys
PATH = sys.argv[1] if len(sys.argv) > 1 else 'revenue_sheet.py'
src = io.open(PATH, encoding='utf-8').read()
if '# [findtab2]' in src:
    print('Da patch roi ([findtab2]) - bo qua.'); sys.exit(0)

OLD = (
    "    mm = datetime.datetime.now().strftime(\"%m\")\n"
    "    for t in titles:\n"
    "        if t.startswith(\"BCng\") and (\"T\" + mm) in t:\n"
    "            return t\n"
)
NEW = (
    "    # [findtab2] khop khong phan biet hoa/thuong + bo dau cach: 'BCNGAY - T07' cung nhan\n"
    "    mm = datetime.datetime.now().strftime(\"%m\")\n"
    "    def _norm(x):\n"
    "        return \"\".join(str(x).lower().split())\n"
    "    wants = [\"t\" + mm, \"t\" + str(int(mm))]   # 'T07' va 'T7'\n"
    "    for t in titles:\n"
    "        n = _norm(t)\n"
    "        if n.startswith(\"bcng\") and any(w in n for w in wants):\n"
    "            return t\n"
)
if src.count(OLD) != 1:
    print('LOI: khong tim thay khoi _find_tab dung 1 lan (co %d). Dung.' % src.count(OLD)); sys.exit(2)
io.open(PATH, 'w', encoding='utf-8').write(src.replace(OLD, NEW))
print('OK: da patch %s (_find_tab ben vung).' % PATH)
