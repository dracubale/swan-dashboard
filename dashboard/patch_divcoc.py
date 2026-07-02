# -*- coding: utf-8 -*-
"""patch_divcoc.py — Bo sung coc realized (coc_add) vao DOANH THU THEO KHOA.

Van de: sau khi ghep coc->thuc hien, coc_add duoc cong vao gross MUC BILL
(headline toan clinic co coc), nhung doanh thu theo khoa doc line goc tu sheet
(_rl / allrbs) nen THIEU dung phan coc -> chenh dong het vao unclassified_rev.

Sua: bom coc_add (theo NHOM CHINH cua bill thuc hien) vao ca:
  (A) allrbs  -> divisions[].services & bang dich vu khop headline
  (B) _rl     -> divisions[].revenue, series_div, rev_by_service theo khoa

KHONG dung vao: completed (headline), linesub, gstats distributions (median/CV/p90).
Idempotent: chay lai khong nhan doi.
"""
import io, sys, os

PATH = sys.argv[1] if len(sys.argv) > 1 else 'extract_v2.py'
src = io.open(PATH, encoding='utf-8').read()

MARK = '# [divcoc]'
if MARK in src:
    print('Da patch roi (thay marker [divcoc]) — bo qua.'); sys.exit(0)

# ---- (A) cong coc realized vao allrbs (theo nhom chinh) ----
A_OLD = (
    "allrbs={}; dep_by_svc={}\n"
    "for s in series:\n"
    "    for g,v in s['rev_by_service'].items(): allrbs[g]=allrbs.get(g,0)+v\n"
    "    for g,v in s['deposit_by_service'].items(): dep_by_svc[g]=dep_by_svc.get(g,0)+v\n"
)
A_NEW = A_OLD + (
    "# [divcoc] coc ky nay da realized: cong vao DT nhom chinh cua bill thuc hien\n"
    "#          (khop headline & doanh thu khoa; khong dung linesub/gstats phan bo)\n"
    "for _,_r in B[(B['coc_add']>0)&(B['is_rev'])].iterrows():\n"
    "    _g=_r['primary']\n"
    "    if _g and DIVMAP.get(_g): allrbs[_g]=allrbs.get(_g,0)+int(round(_r['coc_add']*VND))\n"
)

# ---- (B) bom coc realized thanh line tong hop vao _rl (theo nhom chinh) ----
B_OLD = (
    "_rl=df[(df.billno.isin(_revbillnos))&(df.rev>0)&(df.g!='UNMAPPED')].copy()\n"
    "_rl['line_div']=_rl['g'].map(DIVMAP)\n"
    "_rl=_rl[_rl['line_div'].notna()]\n"
)
B_NEW = B_OLD + (
    "# [divcoc] coc realized khong nam tren line sheet nao -> bom line tong hop\n"
    "#          tren bill thuc hien (nhom chinh) de DT khoa & series_div khop headline\n"
    "_coc_lines=[]\n"
    "for _,_r in B[(B['coc_add']>0)&(B['is_rev'])].iterrows():\n"
    "    _g=_r['primary']; _dv=DIVMAP.get(_g) if _g else None\n"
    "    if _dv is None: continue\n"
    "    _coc_lines.append({'billno':_r['bill'],'date':_r['date'],'rev':float(_r['coc_add']),'g':_g,'line_div':_dv})\n"
    "if _coc_lines:\n"
    "    _rl=pd.concat([_rl,pd.DataFrame(_coc_lines)],ignore_index=True)\n"
)

for label, old in (('A(allrbs)', A_OLD), ('B(_rl)', B_OLD)):
    n = src.count(old)
    if n != 1:
        print('LOI: anchor %s xuat hien %d lan (can dung 1). Dung, khong sua.' % (label, n))
        sys.exit(2)

src = src.replace(A_OLD, A_NEW).replace(B_OLD, B_NEW)
io.open(PATH, 'w', encoding='utf-8').write(src)
print('OK: da patch %s (A: allrbs, B: _rl).' % PATH)
