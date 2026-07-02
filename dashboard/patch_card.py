# -*- coding: utf-8 -*-
"""Them 1 dong 'Khach moi den (thang)' vao the Khach (Noi) trong build_dashboard.py.
Hien khach_moi_den (unique, thang) tu DATA.llv.by_status; fallback dennew neu thieu.
Chi 1 dong, backup .bak. Khong doi du lieu -> deploy chi can update.sh.

Chay tu thu muc co build_dashboard.py:
    python patch_card.py
    python patch_card.py <duong_dan_build_dashboard.py>
"""
import sys, io

PATH = sys.argv[1] if len(sys.argv) > 1 else "build_dashboard.py"

OLD = ":row('Có DT',paying)+"
NEW = (":row('Khách mới đến (tháng)',"
       "((typeof DATA!=='undefined'&&DATA.llv&&DATA.llv.by_status)?"
       "DATA.llv.by_status.khach_moi_den:dennew))+"
       "row('Có DT',paying)+")

src = io.open(PATH, encoding="utf-8").read()
if OLD not in src:
    print("KHONG TIM THAY anchor. Co the da patch roi hoac file khac.")
    sys.exit(1)
if src.count(OLD) != 1:
    print("Anchor xuat hien %d lan (can dung 1). Dung." % src.count(OLD))
    sys.exit(1)
io.open(PATH + ".bak", "w", encoding="utf-8").write(src)
io.open(PATH, "w", encoding="utf-8").write(src.replace(OLD, NEW, 1))
print("OK: da them dong 'Khach moi den' vao the Khach |", PATH, "| backup .bak")
