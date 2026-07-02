# -*- coding: utf-8 -*-
"""Patch v2 extract_v2.py: New/TK theo NHAN loai khach (bo SDT-lan-dau + bo nap
thang truoc). Giu nguyen phan DOI/NO-SHOW theo SDT tai xuat. Backup .bak3.

Chay tu thu muc co extract_v2.py:
    python patch_llv_v2.py
    python patch_llv_v2.py <duong_dan_extract_v2.py>
"""
import sys, io

PATH = sys.argv[1] if len(sys.argv) > 1 else "extract_v2.py"

NEW_BLOCK = r'''# ===== LLV (booking / vận hành: đến / no-show / rớt theo ngày & theo sale) =====
# No-show vs DỜI tách theo SĐT tái xuất (KHÔNG dựa nhãn 'dời'): lịch lỡ mà SĐT có
# lịch ngày SAU = DỜI; không có = NO-SHOW. New/TK theo NHÃN loại khách (nhân viên
# đánh, khớp sheet doanh thu) -> KHÔNG dùng SĐT-lần-đầu cho phần này.
def _llv_key(ph, ten):
    p = re.sub(r'\D', '', str(ph or ''))
    if len(p) >= 9:
        return p
    t = sa(str(ten or '')).strip()
    return 'TEN:' + t if t else ''
def _llv_loai(v):
    s = sa(str(v or '')).strip()
    has_new = 'new' in s
    has_tk = ('tk' in s) or ('tai kham' in s)
    if has_new and not has_tk: return 'new'
    if has_tk: return 'tk'
    if 'cu' in s or s == 'kc' or 'vip' in s: return 'tk'
    return 'other'
def build_llv():
    try:
        import llv_sheet
        lv = llv_sheet.load_llv_df()
    except Exception as e:
        _warn.append('LLV: không đọc được sheet (%s)' % e)
        return None
    if lv is None or not len(lv): return None
    today_ts = pd.Timestamp(date.today())
    recs = []; later_days = {}; new_key = {}
    for _, r in lv.iterrows():
        hen = r['ngay_hen']; stt = r['status']
        if stt == 'noshow' and pd.notna(hen) and hen >= today_ts:
            stt = 'pending'
        k = _llv_key(r.get('phone'), r.get('ten'))
        loai = _llv_loai(r.get('loai_khach'))
        recs.append(dict(k=k, hen=hen, stt=stt, loai=loai,
                         sale=r.get('sale'), nguon=r.get('nguon')))
        if k and pd.notna(hen):
            later_days.setdefault(k, set()).add(hen.normalize())
        if k:                                  # khách MỚI theo NHÃN (1 dòng New -> cả khách New)
            new_key[k] = new_key.get(k, False) or (loai == 'new')
    def _empty():
        return {'booking':0,'den':0,'rot':0,'noshow':0,'doi':0,'pending':0,
                'den_new':0,'noshow_new':0,'booking_new':0,'booking_tk':0,'booking_src':{}}
    def _add(slot, stt, isnew):
        slot['booking'] += 1
        slot['booking_new' if isnew else 'booking_tk'] += 1
        if stt == 'arrived': slot['den'] += 1
        elif stt == 'rot':   slot['den'] += 1; slot['rot'] += 1
        elif stt == 'noshow':slot['noshow'] += 1
        elif stt == 'doi':   slot['doi'] += 1
        elif stt == 'pending':slot['pending'] += 1
        if isnew:
            if stt in ('arrived','rot'): slot['den_new'] += 1
            elif stt == 'noshow':        slot['noshow_new'] += 1
    def _book_src(raw):
        s = str(raw or '').strip().lower()
        if not s: return 'Khác'
        if s.startswith('tt') or 'tiktok' in s: return 'TikTok'
        if s.startswith('ig') or 'instagram' in s: return 'Instagram'
        if s.startswith('fb') or 'facebook' in s: return 'Facebook'
        if s.startswith('zl') or 'zalo' in s: return 'Zalo'
        if s.startswith('oa') or 'cskh' in s: return 'CSKH'
        return str(raw).strip()
    by_day = {}; by_sale = {}
    tot = {'arrived':0,'rot':0,'noshow':0,'doi':0,'pending':0}
    arr_keys = set(); ns_keys = set()
    for rc in recs:
        k, hen, stt = rc['k'], rc['hen'], rc['stt']
        isnew = new_key.get(k, False) if k else (rc['loai'] == 'new')
        if stt in ('noshow','doi') and pd.notna(hen) and k:
            nd = hen.normalize()
            has_later = any(d > nd for d in later_days.get(k, ()))
            stt = 'doi' if has_later else 'noshow'   # DỜI nếu có lịch sau, else NO-SHOW
        elif stt == 'doi':
            stt = 'noshow'                            # dời nhưng thiếu ngày/SĐT -> coi no-show
        tot[stt] = tot.get(stt, 0) + 1
        if pd.notna(hen):
            _slot = by_day.setdefault(hen.date().isoformat(), _empty())
            _add(_slot, stt, isnew)
            _bs = _book_src(rc['nguon'])
            _slot['booking_src'][_bs] = _slot['booking_src'].get(_bs, 0) + 1
        _add(by_sale.setdefault(rc['sale'] or '(trống)', _empty()), stt, isnew)
        if isnew and k:
            if stt in ('arrived','rot'): arr_keys.add(k)
            elif stt == 'noshow':        ns_keys.add(k)
    ns_keys -= arr_keys
    for s in by_sale.values():
        base = s['den'] + s['noshow']
        s['noshow_rate'] = round(s['noshow']/base, 3) if base else 0.0
    return dict(as_of=TODAY, total=int(len(lv)),
        by_status=dict(booking=int(len(lv)), den=tot['arrived']+tot['rot'], rot=tot['rot'],
            noshow=tot['noshow'], doi=tot['doi'], pending=tot['pending'],
            khach_moi_den=len(arr_keys), noshow_new=len(ns_keys)),
        by_day=by_day, by_sale=by_sale)
llv = build_llv()

# ===== ROT LLV (Nội khoa, dòng chảy theo ngày) vào series cho phễu vận hành =====
# Ngoại khoa KHÔNG dùng LLV: số lead nuôi là snapshot -> dashboard đọc thẳng block bkphau.
def _inject_funnel(series, series_div, llv):
    lday = (llv or {}).get('by_day', {}) or {}
    def _set_llv(rec):
        x = lday.get(rec['date'], {})
        rec['booking']=x.get('booking',0); rec['den']=x.get('den',0)
        rec['noshow']=x.get('noshow',0);   rec['rot']=x.get('rot',0); rec['doi']=x.get('doi',0)
        rec['den_new']=x.get('den_new',0); rec['noshow_new']=x.get('noshow_new',0)
        rec['booking_new']=x.get('booking_new',0); rec['booking_tk']=x.get('booking_tk',0)
        rec['booking_src']=x.get('booking_src',{})
    for rec in series_div.get('Nội khoa', []): _set_llv(rec)
    for rec in series:                         _set_llv(rec)
    for rec in series_div.get('Ngoại khoa', []):
        for k in ('booking','den','noshow','rot','doi','den_new','noshow_new','booking_new','booking_tk'): rec[k]=0
        rec['booking_src']={}
_inject_funnel(series, series_div, llv)'''

src = io.open(PATH, encoding="utf-8").read()
try:
    start = src.index("# ===== LLV (booking")
    end = src.index("\nbundle=dict(")
except ValueError as e:
    print("KHONG TIM THAY moc de patch:", e); sys.exit(1)
io.open(PATH + ".bak3", "w", encoding="utf-8").write(src)
io.open(PATH, "w", encoding="utf-8").write(src[:start] + NEW_BLOCK + src[end:])
print("OK: da patch v2", PATH, "| backup:", PATH + ".bak3")
