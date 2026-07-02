# -*- coding: utf-8 -*-
"""Fix auth_app.py: giu block 'llv' khi serve data.json (them vao PAGE_KEYS overview).
Hien tai 'llv' bi xoa rong -> dashboard mat DATA.llv.by_status -> card 'Khach moi den'
roi ve fallback dennew. Them 'llv' -> card doc dung khach_moi_den (213). Backup .bak.

Chay tu thu muc co auth_app.py:
    python patch_auth.py
    python patch_auth.py <duong_dan_auth_app.py>
"""
import sys, io

PATH = sys.argv[1] if len(sys.argv) > 1 else "auth_app.py"

OLD = '"overview": ["series","series_div","divisions","newtk"],'
NEW = '"overview": ["series","series_div","divisions","newtk","llv"],'

src = io.open(PATH, encoding="utf-8").read()
if NEW in src:
    print("Da co 'llv' trong overview keys roi. Khong can sua.")
    sys.exit(0)
if OLD not in src:
    print("KHONG TIM THAY anchor PAGE_KEYS overview. Kiem tra lai file.")
    sys.exit(1)
if src.count(OLD) != 1:
    print("Anchor xuat hien %d lan (can 1). Dung." % src.count(OLD))
    sys.exit(1)
io.open(PATH + ".bak", "w", encoding="utf-8").write(src)
io.open(PATH, "w", encoding="utf-8").write(src.replace(OLD, NEW, 1))
print("OK: da them 'llv' vao overview keys |", PATH, "| backup .bak")
