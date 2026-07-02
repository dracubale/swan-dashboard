# -*- coding: utf-8 -*-
"""patch_updatesh.py - update.sh copy them llv_sheet.py + bkphau_sheet.py vao WEBDIR.
Truoc day chi copy 3 file -> sua llv_sheet/bkphau_sheet khong tu len droplet. Idempotent."""
import io, sys
PATH = sys.argv[1] if len(sys.argv) > 1 else 'update.sh'
src = io.open(PATH, encoding='utf-8').read()
OLD = "for f in build_dashboard.py extract_v2.py revenue_sheet.py; do"
NEW = "for f in build_dashboard.py extract_v2.py revenue_sheet.py llv_sheet.py bkphau_sheet.py; do"
if NEW in src:
    print('Da patch roi - bo qua.'); sys.exit(0)
if src.count(OLD) != 1:
    print('LOI: khong thay dong copy dung 1 lan (co %d). Dung.' % src.count(OLD)); sys.exit(2)
io.open(PATH, 'w', encoding='utf-8').write(src.replace(OLD, NEW))
print('OK: update.sh gio copy them llv_sheet.py + bkphau_sheet.py.')
