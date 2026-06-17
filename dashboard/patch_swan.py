#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vá extract_v2.py: tính doanh thu khoa theo TỪNG DÒNG dịch vụ (sửa lỗi 1 bill nhiều DV
# bị gán trọn về 1 khoa), và tách "Phẫu mông" sang Ngoại khoa.
import io, os, sys, py_compile

PATH = sys.argv[1] if len(sys.argv) > 1 else "extract_v2.py"
src = io.open(PATH, encoding="utf-8").read()

if "Phẫu mông" in src and "_div_billvals" in src:
    print("File có vẻ ĐÃ vá rồi (thấy 'Phẫu mông' + '_div_billvals'). Dừng."); sys.exit(0)

edits = []

# 1) GROUPS: thêm nhóm "Phẫu mông"
edits.append((
'"Mí/Mắt":["mi","mat","eye","blepharo"],"Mông":["mong","buttock"],"Hút mỡ":["hut mo","lipo"]}',
'"Mí/Mắt":["mi","mat","eye","blepharo"],"Mông":["mong","buttock"],"Hút mỡ":["hut mo","lipo"],\n"Phẫu mông":["phau mong"]}'
))

# 2) DIVMAP: Phẫu mông -> Ngoại
edits.append((
"'Mũi':'Ngoại khoa','Ngực':'Ngoại khoa','Mí/Mắt':'Ngoại khoa','Hút mỡ':'Ngoại khoa'}",
"'Mũi':'Ngoại khoa','Ngực':'Ngoại khoa','Mí/Mắt':'Ngoại khoa','Hút mỡ':'Ngoại khoa','Phẫu mông':'Ngoại khoa'}"
))

# 3) DIV_GROUPS: thêm Phẫu mông vào Ngoại
edits.append((
"DIV_GROUPS={'Nội khoa':['Tiêm','Máy','Căng chỉ','Mông'],'Ngoại khoa':['Mũi','Ngực','Mí/Mắt','Hút mỡ']}",
"DIV_GROUPS={'Nội khoa':['Tiêm','Máy','Căng chỉ','Mông'],'Ngoại khoa':['Mũi','Ngực','Mí/Mắt','Hút mỡ','Phẫu mông']}"
))

# 4) Chèn cấu trúc tách-theo-dòng ngay trước khối DIVISION split
edits.append((
"\n# ============ DIVISION split: Nội khoa vs Ngoại khoa ============\nimport calendar\n",
"""
# ===== Doanh thu tách khoa ở mức DÒNG (1 bill nhiều DV -> mỗi dòng về đúng khoa của nó) =====
# Sửa lỗi: trước đây cả bill bị gán 1 khoa (do sale chứa 'phẫu' hoặc dịch vụ chính khác khoa),
# làm phình DT khoa này & thiếu DT khoa kia. Giờ chia DT theo từng dòng dịch vụ.
from collections import defaultdict as _dd
_revbillnos=set(revB['bill'])
_rl=df[(df.billno.isin(_revbillnos))&(df.rev>0)&(df.g!='UNMAPPED')].copy()
_rl['line_div']=_rl['g'].map(DIVMAP)
_rl=_rl[_rl['line_div'].notna()]
bill2div=_dd(dict)                                    # bill -> {khoa: rev(nghin)}
for (bno,dv),v in _rl.groupby(['billno','line_div'])['rev'].sum().items():
    bill2div[bno][dv]=float(v)
def _div_billvals(dname):                             # list phan DT thuoc khoa nay theo tung bill (nghin)
    return [vals[dname] for vals in bill2div.values() if dname in vals]

# ============ DIVISION split: Nội khoa vs Ngoại khoa ============
import calendar
"""
))

# 5) Khối divisions: tính revenue/khách/bill_values theo DÒNG
edits.append((
"""divisions=[]
for dname in ['Nội khoa','Ngoại khoa']:
    sub=revB[revB['division']==dname]
    pv=sorted([x*VND for x in sub['gross']]); rev=float(sub['gross'].sum()*VND)
    depdiv=0.0
    for _,r in B[B.is_deposit].iterrows():
        ds={DIVMAP.get(x) for x in (r['sgroups'] or [])}; ds={x for x in ds if x}
        if r['is_phau']: ds={'Ngoại khoa'}
        if not ds: continue
        if dname in ds: depdiv+=r['gross']*VND/len(ds)
    coc_done_n=int(((B['division']==dname)&(B['coc_done'])).sum())
    svc=sorted([{'group':g,'revenue':int(allrbs.get(g,0))} for g in DIV_GROUPS[dname] if allrbs.get(g,0)>0],key=lambda x:-x['revenue'])
    tgt=TARGET_MONTH[dname]; proj=rev/days_elapsed*month_days if days_elapsed else 0; ad=DIV_AD[dname]
    divisions.append(dict(name=dname,groups=DIV_GROUPS[dname],revenue=int(round(rev)),deposit=int(round(depdiv)),
        customers=int(len(sub)),aov=int(round(st.mean(pv))) if pv else 0,median=int(round(st.median(pv))) if pv else 0,""",
"""divisions=[]
for dname in ['Nội khoa','Ngoại khoa']:
    parts=_div_billvals(dname)                        # moi phan = DT khoa nay trong 1 bill (line-level)
    pv=sorted([p*VND for p in parts]); rev=float(sum(parts)*VND)
    depdiv=0.0
    for _,r in B[B.is_deposit].iterrows():
        ds={DIVMAP.get(x) for x in (r['sgroups'] or [])}; ds={x for x in ds if x}
        if not ds: continue
        if dname in ds: depdiv+=r['gross']*VND/len(ds)
    coc_done_n=int(((B['division']==dname)&(B['coc_done'])).sum())
    svc=sorted([{'group':g,'revenue':int(allrbs.get(g,0))} for g in DIV_GROUPS[dname] if allrbs.get(g,0)>0],key=lambda x:-x['revenue'])
    tgt=TARGET_MONTH[dname]; proj=rev/days_elapsed*month_days if days_elapsed else 0; ad=DIV_AD[dname]
    divisions.append(dict(name=dname,groups=DIV_GROUPS[dname],revenue=int(round(rev)),deposit=int(round(depdiv)),
        customers=int(len(parts)),aov=int(round(st.mean(pv))) if pv else 0,median=int(round(st.median(pv))) if pv else 0,"""
))

# 6) dayrec_div: tính theo DÒNG
edits.append((
"""def dayrec_div(d,division):
    bb=B[(B.date==d)&(B.division==division)]
    rev_bills=bb[bb.is_rev]; dep_bills=bb[bb.is_deposit]
    revenue=rev_bills['gross'].sum()*VND; deposit=dep_bills['gross'].sum()*VND
    pv=[round(x*VND) for x in rev_bills['gross'].tolist()]; xs=rev_bills[rev_bills['distinct']>=2]
    revbillnos=set(rev_bills['bill']); rsub=df[(df.date==d)&(df.billno.isin(revbillnos))&(df.rev>0)&(df.g!='UNMAPPED')]
    rbs={g:round(v*VND) for g,v in rsub.groupby('g')['rev'].sum().items() if v and DIVMAP.get(g)==division}
    ms={};
    for src in (mms.get(d,{}),tms.get(d,{})):
        for g,v in src.items():
            if DIVMAP.get(g)==division: ms[g]=ms.get(g,0)+v
    mmsg=msg_div_day(d,division)
    msp=spend_div_day(d,division); tsp=0   # spend_div_day đã gộp cả Meta+TikTok
    return dict(date=d,gross=(revenue+deposit),operating=revenue,revenue=revenue,deposit=deposit,cash_in=revenue+deposit,
        customers=int(bb.has_cust.sum()),paying=int(bb.is_rev.sum()),coc=int(bb.is_deposit.sum()),zero=int(bb.is_zero.sum()),
        new=int(((bb.is_rev)&(bb.ctype=='NEW')).sum()),tk=int(((bb.is_rev)&(bb.ctype=='TK')).sum()),
        median_bill=float(st.median(pv)) if pv else 0.0,mean_bill=float(st.mean(pv)) if pv else 0.0,
        bill_values=pv,rev_by_service=rbs,deposit_by_service={},
        bills_total=int(bb.is_rev.sum()),bills_multi=int(len(xs)),crosssell_rev=int(round(xs['gross'].sum()*VND)),
        meta_spend=msp,tk_spend=tsp,spend=msp+tsp,meta_msg=int(mmsg),tk_msg=0,msg_by_service=ms,
        roas=round(revenue/(msp+tsp),1) if (msp+tsp) else 0)""",
"""def dayrec_div(d,division):
    _ld=_rl[(_rl.date==d)&(_rl.line_div==division)]              # dong DT thuoc khoa nay trong ngay
    perbill=_ld.groupby('billno')['rev'].sum()                  # phan DT khoa nay theo tung bill
    dbills=set(perbill.index)
    bb=B[(B.date==d)&(B.bill.isin(dbills))]
    revenue=float(perbill.sum())*VND
    pv=[round(float(x)*VND) for x in perbill.tolist()]
    rbs={g:round(v*VND) for g,v in _ld.groupby('g')['rev'].sum().items() if v}
    _ng=_ld.groupby('billno')['g'].nunique(); xs_bills=set(_ng[_ng>=2].index)
    ms={}
    for src in (mms.get(d,{}),tms.get(d,{})):
        for g,v in src.items():
            if DIVMAP.get(g)==division: ms[g]=ms.get(g,0)+v
    mmsg=msg_div_day(d,division)
    msp=spend_div_day(d,division); tsp=0   # spend_div_day da gop ca Meta+TikTok
    npay=len(dbills)
    return dict(date=d,gross=revenue,operating=revenue,revenue=revenue,deposit=0,cash_in=revenue,
        customers=npay,paying=npay,coc=0,zero=0,
        new=int(((bb.is_rev)&(bb.ctype=='NEW')).sum()),tk=int(((bb.is_rev)&(bb.ctype=='TK')).sum()),
        median_bill=float(st.median(pv)) if pv else 0.0,mean_bill=float(st.mean(pv)) if pv else 0.0,
        bill_values=pv,rev_by_service=rbs,deposit_by_service={},
        bills_total=npay,bills_multi=int(len(xs_bills)),crosssell_rev=int(round(_ld[_ld.billno.isin(xs_bills)]['rev'].sum()*VND)),
        meta_spend=msp,tk_spend=tsp,spend=msp+tsp,meta_msg=int(mmsg),tk_msg=0,msg_by_service=ms,
        roas=round(revenue/(msp+tsp),1) if (msp+tsp) else 0)"""
))

# --- ap dung, kiem tra khop chinh xac 1 lan ---
out = src
for i,(old,new) in enumerate(edits,1):
    c = out.count(old)
    if c != 1:
        print("LOI o thay doi #%d: tim thay %d lan (can dung 1). KHONG ghi file." % (i,c)); sys.exit(1)
    out = out.replace(old,new)

bak = PATH + ".bak"
io.open(bak,"w",encoding="utf-8").write(src)
io.open(PATH,"w",encoding="utf-8").write(out)
try:
    py_compile.compile(PATH, doraise=True)
except Exception as e:
    print("Cu phap LOI sau khi va -> khoi phuc ban goc:", e)
    io.open(PATH,"w",encoding="utf-8").write(src); sys.exit(1)
print("OK: da va xong 6 thay doi. Ban goc luu o", bak)
