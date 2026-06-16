import pandas as pd, unicodedata, json, re, statistics as st, numpy as np
from datetime import date
def sa(s):
    s=unicodedata.normalize('NFKD',str(s));return ''.join(c for c in s if not unicodedata.combining(c)).lower()
GROUPS={"Tiêm":["tiem","filler","botox","meso","injection"],"Máy":["danh may","may","laser","hifu","thermage","ulthe","ipl","rf"],
"Căng chỉ":["cang chi","thread","lifting"],"Mũi":["mui","nose","rhino"],"Ngực":["nguc","breast","v1"],
"Mí/Mắt":["mi","mat","eye","blepharo"],"Mông":["mong","buttock"],"Hút mỡ":["hut mo","lipo"],
"Phẫu mông":["phau mong"]}
# Tag dịch vụ ở đầu tên ad theo quy ước (vd "(tiêm) abc", "(v1) ..."=ngực). Ưu tiên tag trong ( ) hoặc [ ].
def classify(name):
    if name is None or str(name).strip()=='' or str(name)=='nan': return 'UNMAPPED'
    m=re.match(r'\s*[\(\[]([^\)\]]+)[\)\]]',str(name)); base=sa(m.group(1)) if m else sa(name)
    best=(0,'UNMAPPED')
    for g,kws in GROUPS.items():
        for kw in kws:
            if kw in base and len(kw)>best[0]: best=(len(kw),g)
    return best[1]
DIVMAP={'Tiêm':'Nội khoa','Máy':'Nội khoa','Căng chỉ':'Nội khoa','Mông':'Nội khoa',
        'Mũi':'Ngoại khoa','Ngực':'Ngoại khoa','Mí/Mắt':'Ngoại khoa','Hút mỡ':'Ngoại khoa','Phẫu mông':'Ngoại khoa'}
DIV_GROUPS={'Nội khoa':['Tiêm','Máy','Căng chỉ','Mông'],'Ngoại khoa':['Mũi','Ngực','Mí/Mắt','Hút mỡ','Phẫu mông']}
def _divof(g): return DIVMAP.get(g)
VND=1000
# ===== DATA POOL: thư mục cấu hình qua SWAN_INPUT_DIR (mặc định = thư mục upload) =====
# Khám phá file ĐỘNG theo mẫu tên → thêm account/ file mới chỉ cần đặt tên đúng tiền tố,
# KHÔNG cần sửa code. File hằng ngày có đuôi ngày khác nhau vẫn nhận đúng (lấy bản mới nhất).
import os, glob as _glob
INPUT_DIR=os.environ.get('SWAN_INPUT_DIR','/mnt/user-data/uploads')
def _pick(pattern):                       # 1 file mới nhất khớp mẫu
    fs=sorted(_glob.glob(os.path.join(INPUT_DIR,pattern)),key=os.path.getmtime,reverse=True)
    if not fs: raise FileNotFoundError(f'Không thấy file khớp mẫu "{pattern}" trong {INPUT_DIR}')
    return fs[0]
def _latest_per_account(*patterns):       # gom mọi file, nhóm theo account (Swan<số>), lấy bản mới nhất/account
    seen={}
    for pat in patterns:
        for f in _glob.glob(os.path.join(INPUT_DIR,pat)):
            m=re.search(r'swan\s*\d+',sa(os.path.basename(f)))
            key=m.group(0).replace(' ','') if m else os.path.basename(f).lower()
            if key not in seen or os.path.getmtime(f)>os.path.getmtime(seen[key]): seen[key]=f
    return sorted(seen.values())
# Doanh thu đọc TRỰC TIẾP từ Google Sheet (live) — không qua file xls (xem load_revenue_df bên dưới)
# Meta: tự khám phá MỌI account theo tiền tố tên — NoiKhoa*=Nội, NgoaiKhoa*=Ngoại
META_FILES=[(f,'Nội khoa') for f in _latest_per_account('NoiKhoa*.xlsx')] + \
           [(f,'Ngoại khoa') for f in _latest_per_account('NgoaiKhoa*.xlsx')]
# Meta optional: chưa có file NoiKhoa*/NgoaiKhoa*.xlsx → chạy rỗng (spend Meta = 0)
_tk=sorted(_glob.glob(os.path.join(INPUT_DIR,'Tiktok_Ads*.xlsx')),key=os.path.getmtime,reverse=True)
TKFILE=_tk[0] if _tk else None            # TikTok optional: chưa có → chạy rỗng (spend TikTok = 0)
TK_DIV='Nội khoa'
TODAY=date.today().isoformat()

from revenue_sheet import load_revenue_df
df=load_revenue_df()   # đọc trực tiếp Google Sheet (live) → DataFrame y như pd.read_excel cũ
df=df.iloc[1:].copy()
df['NGÀY']=pd.to_datetime(df['NGÀY'],errors='coerce').ffill()
df['date']=df['NGÀY'].dt.strftime('%Y-%m-%d')
REVMAX=str(df['date'].dropna().max())   # ngày doanh thu mới nhất — căn ad data về đúng kỳ
df['is_cust']=pd.to_numeric(df['Tính khách?'],errors='coerce')==1
df['rev']=pd.to_numeric(df['GIÁ TRỊ BILL'],errors='coerce').fillna(0.0)
df['billno']=df['BILLL'].ffill()
df['coc']=df['NGƯỜI THỰC HIỆN'].astype(str).apply(lambda v:'coc' in sa(v))
df['coc_link']=pd.to_numeric(df['CỌC'],errors='coerce')   # bill cọc trước đó (ghép cọc→thực hiện)
df['is_phau']=df['SALE'].astype(str).apply(lambda v:'phau' in sa(v))  # sale chuyển phẫu = ngoại khoa
df['g']=df['DỊCH VỤ'].apply(classify)
df['hasK']=df['DỊCH VỤ'].notna() & (df['DỊCH VỤ'].astype(str).str.strip()!='')

bills=[]
for bid,grp in df.groupby('billno'):
    e1=grp[grp.is_cust]; n_e1=len(e1); has_cust=n_e1>=1
    gross=grp['rev'].sum(); e1_coc=bool(e1['coc'].any()) if has_cust else False
    has_dep_line=bool(grp['coc'].any())
    is_deposit=has_cust and e1_coc
    is_zero=has_cust and (not is_deposit) and gross==0
    is_rev=has_cust and (not is_deposit) and gross>0
    cl=grp['coc_link'].dropna(); coc_link=int(cl.iloc[0]) if len(cl) else None
    is_phau=bool(grp['is_phau'].any())
    sgroups=set(grp[(grp.hasK)&(grp.g!='UNMAPPED')]['g'])
    paid=set(grp[(grp.rev>0)&(grp.g!='UNMAPPED')]['g'])
    prby=grp[(grp.rev>0)&(grp.g!='UNMAPPED')].groupby('g')['rev'].sum()
    primary=prby.idxmax() if len(prby) else None
    ctype=sale=master=None; dt=grp['date'].iloc[0]
    if has_cust:
        r=e1.iloc[0]; ctype=str(r['LOẠI KHÁCH']).strip().upper() if pd.notna(r['LOẠI KHÁCH']) else None
        sale=r['SALE'] if pd.notna(r['SALE']) else None; master=r['MASTER'] if pd.notna(r['MASTER']) else None
    bills.append(dict(bill=bid,date=dt,n_e1=n_e1,has_cust=has_cust,ctype=ctype,sale=sale,master=master,
        gross=gross,is_deposit=is_deposit,is_zero=is_zero,is_rev=is_rev,mixed=bool(is_rev and has_dep_line),
        coc_link=coc_link,is_phau=is_phau,sgroups=sgroups,paid=paid,distinct=len(sgroups),primary=primary))
B=pd.DataFrame(bills)

# ===== Ghép cọc→thực hiện: cộng giá trị cọc kỳ này vào bill thực hiện; tách ca prepaid khỏi bill 0đ =====
dep_amount=B[B.is_deposit].set_index('bill')['gross'].to_dict()   # bill cọc -> giá trị cọc (nghìn)
_realized=set()
def _coc_add(r):
    if r['coc_link'] is not None and r['coc_link'] in dep_amount:
        _realized.add(r['coc_link']); return float(dep_amount[r['coc_link']])
    return 0.0
B['coc_add']=B.apply(_coc_add,axis=1)
B['gross']=B['gross']+B['coc_add']                                # bill thực hiện gánh full giá trị (gồm cọc kỳ này)
# ca thực hiện từ cọc kỳ TRƯỚC (không có bill cọc trong file) & còn 0đ → không phải bill 0đ thật
B['coc_done']=B['coc_link'].notna() & (~B['is_deposit']) & (B['gross']==0)
B.loc[B['coc_done'],'is_zero']=False
# bill thực hiện có cọc kỳ này (gross_eff>0) → là bill khách có DT
m_cocrev=B['coc_link'].notna() & (~B['is_deposit']) & (B['gross']>0) & B['has_cust']
B.loc[m_cocrev,'is_rev']=True; B.loc[m_cocrev,'is_zero']=False
# bill cọc đã được thực hiện trong kỳ → chuyển khỏi pipeline (giá trị đã sang bill thực hiện)
B.loc[B['bill'].isin(_realized),['is_deposit','is_rev','is_zero']]=False
# division mỗi bill: ngoại nếu sale phẫu hoặc dịch vụ chính thuộc ngoại; còn lại theo dịch vụ
def _billdiv(r):
    if r['is_phau']: return 'Ngoại khoa'
    return _divof(r['primary'])
B['division']=B.apply(_billdiv,axis=1)

def _div_for(g,accdiv): d=DIVMAP.get(g); return d if d else accdiv   # UNMAPPED ad → theo division của account
def meta():
    if not META_FILES: return {},{},{},{},{},0.0,None
    daily={}; msv={}; spv={}; spd_div={}; msd_div={}; tot=0.0; unmt=0.0; latest=None
    for path,accdiv in META_FILES:
        mf=pd.read_excel(path,sheet_name='Formatted Report',header=2).rename(columns=lambda c:str(c).strip())
        mf['Day']=mf['Day'].ffill()
        ads=mf[(mf['Ad name'].notna())&(mf['Ad name']!='All')].copy(); ads['g']=ads['Ad name'].apply(classify)
        ads['d']=pd.to_datetime(ads['Day'],errors='coerce').dt.strftime('%Y-%m-%d'); ads=ads[ads['d']<=REVMAX]
        ads['sp']=pd.to_numeric(ads['Amount spent (VND)'],errors='coerce').fillna(0.0)
        ads['ms']=pd.to_numeric(ads['New messaging contacts'],errors='coerce').fillna(0.0)
        for d,v in ads.groupby('d')['sp'].sum().items(): daily.setdefault(d,{'spend':0.0,'msg':0.0})['spend']+=float(v)
        for d,v in ads.groupby('d')['ms'].sum().items(): daily.setdefault(d,{'spend':0.0,'msg':0.0})['msg']+=float(v)
        for (d,g),v in ads.groupby(['d','g'])['ms'].sum().items():
            if v>0: msv.setdefault(d,{}); msv[d][g]=msv[d].get(g,0)+int(round(v)); msd_div.setdefault(d,{}); msd_div[d][_div_for(g,accdiv)]=msd_div[d].get(_div_for(g,accdiv),0)+v
        for (d,g),v in ads.groupby(['d','g'])['sp'].sum().items():
            spd_div.setdefault(d,{}); spd_div[d][_div_for(g,accdiv)]=spd_div[d].get(_div_for(g,accdiv),0)+float(v)
        for g,v in ads.groupby('g')['sp'].sum().items(): spv[g]=spv.get(g,0)+float(v)
        tot+=float(ads['sp'].sum()); unmt+=float(ads[ads.g=='UNMAPPED']['sp'].sum())
    return daily,msv,spv,spd_div,msd_div,(unmt/max(1e-9,tot)*100),(max(daily) if daily else None)
def tiktok():
    if TKFILE is None: return {},{},{},{},{},0.0,None
    tf=pd.read_excel(TKFILE,sheet_name='Sheet1').rename(columns=lambda c:str(c).strip())
    tf=tf[~tf['By Day'].astype(str).str.contains('Total',na=False)]; tf=tf[tf['Ad name'].notna()]
    tf['Cost']=pd.to_numeric(tf['Cost'],errors='coerce').fillna(0)
    tf['msg']=pd.to_numeric(tf['Conversations (TikTok direct message)'],errors='coerce').fillna(0)
    tf['g']=tf['Ad name'].apply(classify); tf['d']=tf['By Day'].astype(str); tf=tf[tf['d']<=REVMAX]
    daily={}; msv={}; spv={}; spd_div={}; msd_div={}
    for d,sub in tf.groupby('d'): daily[d]={'spend':float(sub['Cost'].sum()),'msg':float(sub['msg'].sum())}
    for (d,g),v in tf.groupby(['d','g'])['msg'].sum().items():
        if v>0: msv.setdefault(d,{}); msv[d][g]=msv[d].get(g,0)+int(round(v)); msd_div.setdefault(d,{}); msd_div[d][_div_for(g,TK_DIV)]=msd_div[d].get(_div_for(g,TK_DIV),0)+v
    for (d,g),v in tf.groupby(['d','g'])['Cost'].sum().items():
        spd_div.setdefault(d,{}); spd_div[d][_div_for(g,TK_DIV)]=spd_div[d].get(_div_for(g,TK_DIV),0)+float(v)
    for g,v in tf.groupby('g')['Cost'].sum().items(): spv[g]=spv.get(g,0)+float(v)
    tot=float(tf['Cost'].sum()); unmapped=float(tf[tf.g=='UNMAPPED']['Cost'].sum())/max(1e-9,tot)*100
    return daily,msv,spv,spd_div,msd_div,unmapped,(max(daily) if daily else None)
md,mms,mspv,mspd,mmsd,m_unmap,m_latest=meta(); td,tms,tspv,tspd,tmsd,t_unmap,t_latest=tiktok()
def spend_div_day(d,division): return mspd.get(d,{}).get(division,0)+tspd.get(d,{}).get(division,0)
def msg_div_day(d,division): return mmsd.get(d,{}).get(division,0)+tmsd.get(d,{}).get(division,0)

days=sorted(df['date'].dropna().unique())
def dayrec(d):
    bb=B[B.date==d]; sub=df[df.date==d]
    rev_bills=bb[bb.is_rev]; dep_bills=bb[bb.is_deposit]
    revenue=rev_bills['gross'].sum()*VND; deposit=dep_bills['gross'].sum()*VND
    revbillnos=set(rev_bills['bill']); rsub=sub[(sub.billno.isin(revbillnos))&(sub.rev>0)&(sub.g!='UNMAPPED')]
    rbs={g:round(v*VND) for g,v in rsub.groupby('g')['rev'].sum().items() if v}
    dep_svc={}
    for _,r in dep_bills.iterrows():
        gset=list(r['sgroups']) if r['sgroups'] else ['(chưa rõ DV)']
        for g in gset: dep_svc[g]=dep_svc.get(g,0)+round(r['gross']*VND/len(gset))
    pv=[round(x*VND) for x in rev_bills['gross'].tolist()]
    xs=rev_bills[rev_bills['distinct']>=2]; ms={}
    for src in (mms.get(d,{}),tms.get(d,{})):
        for g,v in src.items(): ms[g]=ms.get(g,0)+v
    sp=md.get(d,{}).get('spend',0)+td.get(d,{}).get('spend',0)
    return dict(date=d,gross=(revenue+deposit),operating=revenue,revenue=revenue,deposit=deposit,cash_in=revenue+deposit,
        customers=int(bb.has_cust.sum()),paying=int(bb.is_rev.sum()),coc=int(bb.is_deposit.sum()),zero=int(bb.is_zero.sum()),
        new=int(((bb.is_rev)&(bb.ctype=='NEW')).sum()),tk=int(((bb.is_rev)&(bb.ctype=='TK')).sum()),
        median_bill=float(st.median(pv)) if pv else 0.0,mean_bill=float(st.mean(pv)) if pv else 0.0,
        bill_values=pv,rev_by_service=rbs,deposit_by_service={k:int(v) for k,v in dep_svc.items()},
        bills_total=int(bb.is_rev.sum()),bills_multi=int(len(xs)),crosssell_rev=int(round(xs['gross'].sum()*VND)),
        meta_spend=md.get(d,{}).get('spend',0),tk_spend=td.get(d,{}).get('spend',0),spend=sp,
        meta_msg=md.get(d,{}).get('msg',0),tk_msg=td.get(d,{}).get('msg',0),msg_by_service=ms,
        roas=round(revenue/sp,1) if sp else 0)
series=[dayrec(d) for d in days]

revB=B[B.is_rev]; coc_billnos=set(B[B.is_deposit]['bill'])|set(_realized)
linesub=df[(df.rev>0)&(~df.billno.isin(coc_billnos))&(df.g!='UNMAPPED')]
allrbs={}; dep_by_svc={}
for s in series:
    for g,v in s['rev_by_service'].items(): allrbs[g]=allrbs.get(g,0)+v
    for g,v in s['deposit_by_service'].items(): dep_by_svc[g]=dep_by_svc.get(g,0)+v
def gstats(g):
    sel=linesub[linesub.g==g]; v=np.array(sorted(sel['rev'].tolist(),reverse=True)); n=len(v)
    bset=revB[revB.paid.apply(lambda p:g in p)]; n_bills=len(bset)
    base=dict(cust_with=int(n_bills),rev_with=round(float(bset['gross'].sum()*VND)),
        svc_attach=round(float((bset['distinct']>=2).mean()*100)) if n_bills else 0)
    if n_bills>0:
        cg=np.array(sorted((bset['gross'].astype(float)*VND).tolist(),reverse=True))
        cmean=cg.mean(); ccv=float(cg.std(ddof=1)/cmean*100) if (n_bills>1 and cmean) else 0.0
        ck=max(1,round(n_bills*0.2)); cshare=float(cg[:ck].sum()/cg.sum()*100) if cg.sum() else 0.0
        base.update(cust_median=round(float(np.median(cg))),cust_p90=round(float(np.percentile(cg,90))),
            cust_cv=round(ccv),cust_top_share=round(cshare),cust_top_bills=int(ck))
    if n==0: return base
    mean=v.mean(); cv=float(v.std(ddof=1)/mean*100) if (n>1 and mean) else 0.0
    k=max(1,round(n*0.2)); share=float(v[:k].sum()/v.sum()*100) if v.sum() else 0.0
    base.update(lines=int(n),median=round(float(np.median(v))*VND),p90=round(float(np.percentile(v,90))*VND),
        cv=round(cv),top_bills=int(k),top_share=round(share))
    return base
services=[]
for g in sorted(set(list(allrbs.keys())+list(dep_by_svc.keys())),key=lambda g:-(allrbs.get(g,0))):
    rec={'group':g,'revenue':int(allrbs.get(g,0)),'deposit':int(dep_by_svc.get(g,0)),'division':DIVMAP.get(g)}; rec.update(gstats(g)); services.append(rec)

xsB=revB[revB['distinct']>=2]; nonxs=revB[revB['distinct']<2]; completed=revB['gross'].sum()*VND
aov_xs=float(xsB['gross'].mean()*VND) if len(xsB) else 0; aov_non=float(nonxs['gross'].mean()*VND) if len(nonxs) else 0
crosssell=dict(rev_customers=int(len(revB)),xsell_bills=int(len(xsB)),
    attach_rate=round(len(xsB)/len(revB)*100,1) if len(revB) else 0,
    xsell_revenue=int(round(xsB['gross'].sum()*VND)),xsell_share=round(xsB['gross'].sum()*VND/completed*100,1) if completed else 0,
    aov_xsell=round(aov_xs),aov_nonxsell=round(aov_non),uplift=round((aov_xs/aov_non-1)*100,1) if aov_non else 0,
    avg_groups=round(revB['distinct'].sum()/len(revB),2) if len(revB) else 0)

def seg(ct):
    sb=B[B.ctype==ct]; rev=sb[sb.is_rev]; pv=[x*VND for x in rev['gross']]; xs=rev[rev['distinct']>=2]
    return dict(customers=int(sb.has_cust.sum()),revenue=int(round(rev['gross'].sum()*VND)),coc=int(sb.is_deposit.sum()),
        zero=int(sb.is_zero.sum()),paying=int(len(rev)),aov=round(st.mean(pv)) if pv else 0,
        median=round(st.median(pv)) if pv else 0,attach=round(len(xs)/len(rev)*100,1) if len(rev) else 0)
newtk={'New':seg('NEW'),'TK':seg('TK')}

# ============ Master / Sale via shared agent stats + Value Index ============
GA=(revB.groupby('primary')['gross'].mean()*VND).to_dict()   # expected AOV by primary group
def pctl(a,q): return float(np.percentile(a,q)) if a else 0
def agent_stats(grp):
    rev=grp[grp.is_rev]; pv=[x*VND for x in rev['gross']]; xs=rev[rev['distinct']>=2]; nx=rev[rev['distinct']<2]
    pvx=[x*VND for x in xs['gross']]; pvn=[x*VND for x in nx['gross']]
    completed=float(rev['gross'].sum()*VND); deposit=float(grp[grp.is_deposit]['gross'].sum()*VND)
    exp=float(sum(GA.get(p,0) for p in rev['primary'] if p is not None))
    mix={}
    for _,r in rev.iterrows():
        if r['primary']: mix[r['primary']]=mix.get(r['primary'],0)+r['gross']*VND
    mix={k:int(round(v)) for k,v in sorted(mix.items(),key=lambda x:-x[1])}
    n=len(grp); nr=len(rev)
    pv_days=[int((rev['date']==d).sum()) for d in days]   # khách DT mỗi ngày (ngày 0 vẫn tính)
    _mpd=sum(pv_days)/len(pv_days) if pv_days else 0
    _pcv=round(st.pstdev(pv_days)/_mpd*100) if (_mpd>0 and len(pv_days)>1) else None
    return dict(customers=int(n),paying=int(nr),coc=int(grp.is_deposit.sum()),zero=int(grp.is_zero.sum()),
        paying_per_day=round(_mpd,2),paying_cv=_pcv,
        revenue=int(round(completed)),deposit=int(round(deposit)),cash_in=int(round(completed+deposit)),
        aov=round(st.mean(pv)) if pv else 0,median=round(st.median(pv)) if pv else 0,p90=round(pctl(pv,90)),
        attach=round(len(xs)/nr*100,1) if nr else 0,conv=round(nr/n*100,1) if n else 0,
        paid_rate=round(nr/n*100,1) if n else 0,
        monetized_rate=round((nr+grp.is_deposit.sum())/n*100,1) if n else 0,
        zero_pct=round(grp.is_zero.sum()/n*100,1) if n else 0,
        deposit_rate=round(grp.is_deposit.sum()/n*100,1) if n else 0,
        xsell=int(len(xs)),aov_xsell=round(st.mean(pvx)) if pvx else 0,aov_nonxsell=round(st.mean(pvn)) if pvn else 0,
        uplift=round((st.mean(pvx)/st.mean(pvn)-1)*100,1) if (pvx and pvn and st.mean(pvn)) else 0,
        new=int((grp.ctype=='NEW').sum()),tk=int((grp.ctype=='TK').sum()),
        new_paid=int(((rev.ctype=='NEW')).sum()),tk_paid=int(((rev.ctype=='TK')).sum()),
        tk_paid_rev=int(round(rev[rev.ctype=='TK']['gross'].sum()*VND)),
        new_paid_rev=int(round(rev[rev.ctype=='NEW']['gross'].sum()*VND)),
        expected=int(round(exp)),value_index=round(completed/exp,2) if exp else None,mix=mix)

CHAN={'thucskh','truc tiep','phau'}
def parse_sale(s):
    if not s or str(s)=='nan': return None
    toks=[t.strip() for t in re.split(r'[,/]',str(s)) if t.strip()]
    persons=[t for t in toks if sa(t) not in CHAN]
    if persons: return persons[-1].upper().strip()
    t=sa(toks[0]) if toks else ''
    return 'CSKH Online' if 'thucskh' in t else ('Trực tiếp' if 'truc tiep' in t else (toks[0].strip().upper() if toks else None))
B['sale_key']=B['sale'].apply(parse_sale)
B['master_key']=B['master'].apply(lambda s: str(s).strip().upper() if (s and str(s)!='nan') else None)
sales=[]
for name,grp in B[(B.has_cust)&(B.sale_key.notna())].groupby('sale_key'):
    d=agent_stats(grp); d['name']=name; sales.append(d)
sales.sort(key=lambda x:-x['revenue'])
masters=[]
for name,grp in B[(B.has_cust)&(B.master_key.notna())].groupby('master_key'):
    d=agent_stats(grp); d['name']=name; masters.append(d)
masters.sort(key=lambda x:-x['revenue'])

# ============ cross-sell: medians + pair matrix + opportunity ============
crosssell['median_xsell']=int(round(st.median([x*VND for x in xsB['gross']]))) if len(xsB) else 0
crosssell['median_nonxsell']=int(round(st.median([x*VND for x in nonxs['gross']]))) if len(nonxs) else 0
pairs={}
for _,r in xsB.iterrows():
    main=r['primary']
    if not main: continue
    for other in r['sgroups']:
        if other==main: continue
        key=(main,other); p=pairs.setdefault(key,{'bills':0,'rev':0.0})
        p['bills']+=1; p['rev']+=r['gross']*VND
pair_list=sorted([{'main':k[0],'attach':k[1],'bills':v['bills'],'revenue':int(round(v['rev']))}
    for k,v in pairs.items()],key=lambda x:-x['revenue'])
# opportunity per primary group
opp=[]
for g in sorted(set(revB['primary'].dropna())):
    sub=revB[revB['primary']==g]; n=len(sub); xsub=sub[sub['distinct']>=2]; nsub=sub[sub['distinct']<2]
    aovx=float(xsub['gross'].mean()*VND) if len(xsub) else 0; aovn=float(nsub['gross'].mean()*VND) if len(nsub) else 0
    cur=len(xsub)/n*100 if n else 0; gap=(aovx-aovn) if (aovx>0 and aovn>0) else 0
    opp.append(dict(group=g,customers=int(n),attach=round(cur,1),aov_non=round(aovn),aov_x=round(aovx),
        has_pair=bool(len(xsub) and len(nsub)),
        uplift=round((aovx/aovn-1)*100,1) if (aovx>0 and aovn>0) else None,
        plus5=int(round(n*0.05*gap)),plus10=int(round(n*0.10*gap)),plus15=int(round(n*0.15*gap))))
opp.sort(key=lambda x:-x['customers'])
crosssell['pairs']=pair_list; crosssell['opportunity']=opp

def ad_table(fname,sheet,header,namecol,daycol,spendcol,leadcol,convcol,imprcol,reachcol,clickcol,platname,accdiv,is_total=False):
    df_=pd.read_excel(fname,sheet_name=sheet,header=header).rename(columns=lambda c:str(c).strip())
    if is_total: df_=df_[~df_[daycol].astype(str).str.contains('Total',na=False)]
    ads=df_[(df_[namecol].notna())&(df_[namecol]!='All')].copy()
    num=lambda col: pd.to_numeric(ads[col],errors='coerce').fillna(0) if col and col in ads else 0
    ads['_spend']=num(spendcol); ads['_lead']=num(leadcol); ads['_conv']=num(convcol)
    ads['_impr']=num(imprcol); ads['_reach']=num(reachcol); ads['_click']=num(clickcol) if clickcol else 0
    ads['g']=ads[namecol].apply(classify)
    rows=[]
    for name,gg in ads.groupby(namecol):
        sp=float(gg['_spend'].sum()); ld=float(gg['_lead'].sum()); cv=float(gg['_conv'].sum())
        im=float(gg['_impr'].sum()); rc=float(gg['_reach'].sum()); ck=float(gg['_click'].sum())
        g0=gg['g'].iloc[0]
        rows.append(dict(name=str(name),platform=platname,g=g0,div=_div_for(g0,accdiv),spend=sp,lead=ld,conv=cv,impr=im,reach=rc,click=ck))
    return rows
m_ads=[]
for _p,_accdiv in META_FILES: m_ads+=ad_table(_p,'Formatted Report',2,'Ad name','Day','Amount spent (VND)','New messaging contacts','Messaging conversations started','Impressions','Reach',None,'Meta',_accdiv)
t_ads=ad_table(TKFILE,'Sheet1',0,'Ad name','By Day','Cost','Leads (TikTok direct message)','Conversations (TikTok direct message)','Impressions','Reach','Clicks (destination)','TikTok',TK_DIV,is_total=True) if TKFILE else []

def plat_totals(ads,name,has_click):
    sp=sum(a['spend'] for a in ads); ld=sum(a['lead'] for a in ads); cv=sum(a['conv'] for a in ads)
    im=sum(a['impr'] for a in ads); rc=sum(a['reach'] for a in ads); ck=sum(a['click'] for a in ads)
    mix={}; 
    for a in ads:
        if a['g']!='UNMAPPED': mx=mix.setdefault(a['g'],{'spend':0,'lead':0,'conv':0}); mx['spend']+=a['spend']; mx['lead']+=a['lead']; mx['conv']+=a['conv']
    by_service=[{'group':g,'spend':round(v['spend']),'lead':int(round(v['lead'])),'conv':int(round(v['conv'])),
        'cpl':round(v['spend']/v['lead']) if v['lead'] else None} for g,v in sorted(mix.items(),key=lambda x:-x[1]['spend'])]
    unmap=sum(a['spend'] for a in ads if a['g']=='UNMAPPED')/max(1e-9,sp)*100
    return dict(name=name,spend=round(sp),new_lead=int(round(ld)),conv=int(round(cv)),
        impr=int(round(im)),reach=int(round(rc)),
        cpl_lead=round(sp/ld) if ld else None,cpl_conv=round(sp/cv) if cv else None,
        cpm=round(sp/im*1000) if im else None,freq=round(im/rc,2) if rc else None,
        ctr=round(ck/im*100,2) if (has_click and im) else None,cpc=round(sp/ck) if (has_click and ck) else None,
        spend_by_service=by_service,unmapped_pct=round(unmap,1),
        spend_by_service_dict={g:round(v['spend']) for g,v in mix.items()})
plat={'meta':plat_totals(m_ads,'Meta',False),'tiktok':plat_totals(t_ads,'TikTok',True)}
# Platform tách theo division (lọc ad theo div) — cho trang Nền tảng khi lọc Nội/Ngoại
platform_div={}
for dv in ['Nội khoa','Ngoại khoa']:
    platform_div[dv]={'meta':plat_totals([a for a in m_ads if a['div']==dv],'Meta',False),
                      'tiktok':plat_totals([a for a in t_ads if a['div']==dv],'TikTok',True)}

# combined ad-level table with status
all_ads=[a for a in (m_ads+t_ads) if a['spend']>0 or a['lead']>0]
tot_spend=sum(a['spend'] for a in all_ads); tot_lead=sum(a['lead'] for a in all_ads)
bench=tot_spend/tot_lead if tot_lead else 0
MIN_SPEND=3_000_000
def status(a):
    cpl=a['spend']/a['lead'] if a['lead'] else None
    freq=a['impr']/a['reach'] if a['reach'] else 0
    if a['spend']>=MIN_SPEND and (a['lead']==0 or (cpl and cpl>bench*1.5)): return 'Cut'
    if a['lead']>=3 and cpl and cpl<bench*0.8: return 'Scale'
    if freq>=3 or (cpl and cpl>bench*1.2): return 'Watch'
    if a['spend']<MIN_SPEND: return 'Hold'
    return 'Giữ'
adrows=[]
for a in all_ads:
    cpl=round(a['spend']/a['lead']) if a['lead'] else None
    adrows.append(dict(name=a['name'][:42],platform=a['platform'],group=a['g'],div=a.get('div'),spend=round(a['spend']),
        lead=int(round(a['lead'])),conv=int(round(a['conv'])),cpl=cpl,
        freq=round(a['impr']/a['reach'],2) if a['reach'] else None,status=status(a)))
adrows.sort(key=lambda x:-x['spend'])
# winner concentration: top 20% ads by lead -> % of leads
ads_by_lead=sorted([a['lead'] for a in all_ads],reverse=True); kk=max(1,round(len(ads_by_lead)*0.2))
winner_pct=round(sum(ads_by_lead[:kk])/max(1e-9,sum(ads_by_lead))*100) if ads_by_lead else 0
waste=round(sum(a['spend'] for a in all_ads if (a['lead']==0) or (a['lead'] and a['spend']/a['lead']>bench*2)))
platform_extra=dict(ads=adrows,benchmark_cpl=round(bench),winner_pct=winner_pct,winner_n=kk,n_ads=len(all_ads),
    waste_spend=waste,total_spend=round(tot_spend),total_lead=int(round(tot_lead)))

spend_svc={}
for p in (plat['meta'],plat['tiktok']):
    for g,v in p['spend_by_service_dict'].items(): spend_svc[g]=spend_svc.get(g,0)+v
for p in plat.values(): p.pop('spend_by_service_dict',None)
for dv in platform_div.values():
    for p in dv.values(): p.pop('spend_by_service_dict',None)
msg_svc={}
for src in (mms,tms):
    for d,gd in src.items():
        for g,v in gd.items(): msg_svc[g]=msg_svc.get(g,0)+v
for s in services:
    sp=spend_svc.get(s['group'],0); s['ad_spend']=round(sp); s['proxy_roas']=round(s['revenue']/sp,1) if sp else None
    s['ad_msg']=int(round(msg_svc.get(s['group'],0)))


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
TARGET_MONTH={'Nội khoa':12_000_000_000,'Ngoại khoa':3_000_000_000}
# Ad theo division: cộng từ 4 account Meta (2 nội + 2 ngoại) + TikTok, tag theo dịch vụ ở tên ad
DIV_AD={dv:float(sum(spend_div_day(d,dv) for d in days)) for dv in ['Nội khoa','Ngoại khoa']}
DIV_MSG={dv:float(sum(msg_div_day(d,dv) for d in days)) for dv in ['Nội khoa','Ngoại khoa']}
_y,_m=int(TODAY[:4]),int(TODAY[5:7]); month_days=calendar.monthrange(_y,_m)[1]
days_elapsed=len([d for d in days if d[:7]==TODAY[:7]]) or len(days)
divisions=[]
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
        customers=int(len(parts)),aov=int(round(st.mean(pv))) if pv else 0,median=int(round(st.median(pv))) if pv else 0,
        p90=int(round(pctl(pv,90))) if pv else 0,bill_values=[int(round(x)) for x in pv],services=svc,coc_done=coc_done_n,
        ad_spend=int(round(ad)),ad_msg=int(round(DIV_MSG[dname])),roas=round(rev/ad,1) if ad else None,
        target_month=int(tgt),projected_month=int(round(proj)),
        pct_target=round(rev/tgt*100,1) if tgt else 0,pct_projected=round(proj/tgt*100,1) if tgt else 0))
_div_rev=sum(d['revenue'] for d in divisions)
_cocdone_cross=int((B['coc_done']).sum())
divblock=dict(month_days=month_days,days_elapsed=days_elapsed,items=divisions,
    unclassified_rev=int(round(completed-_div_rev)),
    note_ad='Ad đã tách theo 4 account Meta (2 nội + 2 ngoại) + TikTok, gắn tag dịch vụ ở tên ad',
    note_pipeline=(f'{_cocdone_cross} ca thực hiện từ cọc kỳ trước (giá trị cọc nằm ở file tháng trước, doanh thu kỳ này chưa gồm phần cọc đó)' if _cocdone_cross else 'Đã ghép cọc→thực hiện qua cột CỌC'))

# Team chia riêng: master ngoại = Tiên & Vương; sale chuyển phẫu (tên có "phẫu") = ngoại
NGOAI_MASTERS={'tien','vuong'}
for d in masters: d['division']='Ngoại khoa' if sa(d['name']) in NGOAI_MASTERS else 'Nội khoa'
def _domdiv(grp):
    vc=grp[grp.is_rev]['division'].dropna()
    return vc.mode().iloc[0] if len(vc) else None
_sdiv={n:_domdiv(g) for n,g in B[(B.has_cust)&(B.sale_key.notna())].groupby('sale_key')}
for d in sales: d['division']=('Ngoại khoa' if 'phau' in sa(d['name']) else _sdiv.get(d['name']))

# Stats theo từng division: ai chốt bill mảng nào hiện đúng ở mảng đó (vd ca ngoại khoa đã chốt)
def agents_for(keycol,div):
    out=[]
    for name,grp in B[(B.has_cust)&(B[keycol].notna())&(B.division==div)].groupby(keycol):
        d=agent_stats(grp); d['name']=name; d['division']=div; out.append(d)
    out.sort(key=lambda x:-x['revenue']); return out
sales_div={dv:agents_for('sale_key',dv) for dv in ['Nội khoa','Ngoại khoa']}
masters_div={dv:agents_for('master_key',dv) for dv in ['Nội khoa','Ngoại khoa']}

# cross-sell tính riêng từng division (attach/pairs/opportunity nội bộ division)
def crosssell_for(rb):
    xs=rb[rb['distinct']>=2]; nx=rb[rb['distinct']<2]; comp=rb['gross'].sum()*VND
    axs=float(xs['gross'].mean()*VND) if len(xs) else 0; anx=float(nx['gross'].mean()*VND) if len(nx) else 0
    cs=dict(rev_customers=int(len(rb)),xsell_bills=int(len(xs)),
        attach_rate=round(len(xs)/len(rb)*100,1) if len(rb) else 0,
        xsell_revenue=int(round(xs['gross'].sum()*VND)),xsell_share=round(xs['gross'].sum()*VND/comp*100,1) if comp else 0,
        aov_xsell=round(axs),aov_nonxsell=round(anx),uplift=round((axs/anx-1)*100,1) if anx else 0,
        avg_groups=round(rb['distinct'].sum()/len(rb),2) if len(rb) else 0,
        median_xsell=int(round(st.median([x*VND for x in xs['gross']]))) if len(xs) else 0,
        median_nonxsell=int(round(st.median([x*VND for x in nx['gross']]))) if len(nx) else 0)
    prs={}
    for _,r in xs.iterrows():
        main=r['primary']
        if not main: continue
        for other in r['sgroups']:
            if other==main: continue
            k=(main,other); pp=prs.setdefault(k,{'bills':0,'rev':0.0}); pp['bills']+=1; pp['rev']+=r['gross']*VND
    cs['pairs']=sorted([{'main':k[0],'attach':k[1],'bills':v['bills'],'revenue':int(round(v['rev']))} for k,v in prs.items()],key=lambda x:-x['revenue'])
    opp=[]
    for g in sorted(set(rb['primary'].dropna())):
        sub=rb[rb['primary']==g]; n=len(sub); xsub=sub[sub['distinct']>=2]; nsub=sub[sub['distinct']<2]
        aovx=float(xsub['gross'].mean()*VND) if len(xsub) else 0; aovn=float(nsub['gross'].mean()*VND) if len(nsub) else 0
        cur=len(xsub)/n*100 if n else 0; gap=(aovx-aovn) if (aovx>0 and aovn>0) else 0
        opp.append(dict(group=g,customers=int(n),attach=round(cur,1),aov_non=round(aovn),aov_x=round(aovx),
            has_pair=bool(len(xsub) and len(nsub)),
            uplift=round((aovx/aovn-1)*100,1) if (aovx>0 and aovn>0) else None,
            plus5=int(round(n*0.05*gap)),plus10=int(round(n*0.10*gap)),plus15=int(round(n*0.15*gap))))
    cs['opportunity']=sorted(opp,key=lambda x:-x['customers'])
    return cs
crosssell_div={d:crosssell_for(revB[revB['division']==d]) for d in ['Nội khoa','Ngoại khoa']}

# per-division daily series (cho overview lọc theo division)
def dayrec_div(d,division):
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
        roas=round(revenue/(msp+tsp),1) if (msp+tsp) else 0)
series_div={dv:[dayrec_div(d,dv) for d in days] for dv in ['Nội khoa','Ngoại khoa']}

dq=dict(bills_no_e1=int((B.n_e1==0).sum()),bills_multi_e1=int((B.n_e1>1).sum()),mixed_bills=int(B.mixed.sum()),
    rev_unmapped_pct=round(float(df[(df.rev>0)&(df.g=='UNMAPPED')]['rev'].sum()/max(1e-9,df[df.rev>0]['rev'].sum())*100),1),
    meta_unmapped_pct=round(m_unmap,1),tk_unmapped_pct=round(t_unmap,1),
    latest_revenue=days[-1],latest_meta=m_latest,latest_tiktok=t_latest,today=TODAY,
    generated_at=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'))

allpv=[v for s in series for v in s['bill_values']]
dep_total=B[B.is_deposit]['gross'].sum()*VND
bundle=dict(period=dict(start=days[0],end=days[-1],n_days=len(days)),today=days[-1],system_today=TODAY,
    week_median_bill=float(st.median(allpv)) if allpv else 0,week_mean_bill=float(st.mean(allpv)) if allpv else 0,
    totals=dict(revenue_completed=int(round(completed)),deposit=int(round(dep_total)),cash_in=int(round(completed+dep_total))),
    series=series,services=services,crosssell=crosssell,newtk=newtk,platform=plat,platform_div=platform_div,platform_extra=platform_extra,dataquality=dq,sales=sales,masters=masters,sales_div=sales_div,masters_div=masters_div,divisions=divblock,crosssell_div=crosssell_div,series_div=series_div)
json.dump(bundle,open('bundle.json','w'),ensure_ascii=False)

print('=== VALIDATION ===')
print('Khách:',int(B.has_cust.sum()),'= rev',int(B.is_rev.sum()),'/ cọc',int(B.is_deposit.sum()),'/ 0đ',int(B.is_zero.sum()),'| mixed(flag)',int(B.mixed.sum()))
print('Hoàn tất %.0fk | Cọc %.0fk | Cash-in %.0fk'%(completed/1e3,dep_total/1e3,(completed+dep_total)/1e3))
print('Pie completed:',{s['group']:round(s['revenue']/1e6) for s in services if s['revenue']>0})
print('Pipeline cọc:',{s['group']:round(s['deposit']/1e6,1) for s in services if s.get('deposit',0)>0})
print('Cross-sell:',crosssell)
print('New/TK:',{k:{'cust':v['customers'],'rev':round(v['revenue']/1e6),'aov':round(v['aov']/1e6,1),'attach':v['attach']} for k,v in newtk.items()})
print('DQ:',dq)
