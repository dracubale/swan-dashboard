import json, datetime

import os as _os0
bundle = json.load(open(_os0.environ.get('SWAN_BUNDLE','bundle.json'), encoding='utf-8'))
DATA_JSON = json.dumps(bundle, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<script>(function(){try{var t=localStorage.getItem('swan-theme');if(!t)t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';if(t==='dark')document.documentElement.setAttribute('data-theme','dark');}catch(e){}})();</script>
<title>Swan Clinic — Bảng điều khiển CEO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  color-scheme:light;
  --paper:#F7F4EC; --paper-2:#FFFEFA; --ink:#1B1A16; --ink-soft:#5C594E;
  --line:#E3DDCF; --jade:#0F7B74; --jade-2:#2BA39B; --gold:#B6802A;
  --rose:#A8443A; --shadow:0 1px 2px rgba(27,26,22,.04),0 8px 24px rgba(27,26,22,.06);
  --tint:#F0EEE5; --tint2:#EFEADC; --accent-soft:#E3F1EF; --accent-soft-bd:#CDE2D9; --muted:#9A927E;
  --gold-soft:#F6E8CF; --rose-soft:#F3DCD8;
  --pos:#12955A; --warn:#CF9412; --neg:#D93A2C;
}
[data-theme="dark"]{
  --paper:#0F1513; --paper-2:#17201D; --ink:#E9EFEC; --ink-soft:#9CA7A2;
  --line:#283330; --jade:#3FB8AE; --jade-2:#5BC9BF; --gold:#D6A552; --rose:#E58C80;
  --tint:#1C2622; --tint2:#202A26; --accent-soft:#143230; --accent-soft-bd:#2A524C; --muted:#828D88;
  --gold-soft:#33291A; --rose-soft:#36231F;
  --pos:#34D08A; --warn:#ECB347; --neg:#F76B5C;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 28px rgba(0,0,0,.4); color-scheme:dark;
}
[data-theme="dark"] .side{background:#0B2422}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:'Inter',sans-serif;
  font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased;line-height:1.5}
.app{display:grid;grid-template-columns:248px 1fr;min-height:100vh}
/* sidebar */
.side{background:#0E423E;color:#E7EFEC;padding:28px 18px;position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;gap:6px}
.brand{font-family:'Inter',sans-serif;font-size:25px;font-weight:700;letter-spacing:-.01em;line-height:1.05;margin-bottom:2px}
.brand small{display:block;font-family:'Inter';font-weight:600;font-size:10px;letter-spacing:.22em;
  text-transform:uppercase;color:#A29A86;margin-top:8px}
.nav{margin-top:26px;display:flex;flex-direction:column;gap:3px}
.nav button{all:unset;cursor:pointer;display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:10px;
  font-weight:600;font-size:14px;color:#C7C1B0;transition:.18s}
.nav button .vi{color:inherit}.nav button .en{font-size:10.5px;color:#7E7765;letter-spacing:.04em}
.nav button svg{width:18px;height:18px;flex-shrink:0;opacity:.85}
.nav button.active svg{opacity:1}
.nav button:hover{background:#26241E;color:#fff}
.nav button.active{background:var(--jade);color:#fff}
.nav button.active .en{color:#A9D5C8}
.nav .dot{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.6}
.side-foot{margin-top:auto;font-size:11px;color:#827B69;line-height:1.6;border-top:1px solid #322F28;padding-top:16px}
.side-foot b{color:#C7C1B0;font-weight:600}
/* main */
.main{padding:34px 44px 60px;max-width:1360px;min-width:0}
.topbar{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:30px;flex-wrap:wrap;gap:16px}
.topbar h1{font-family:'Inter',sans-serif;font-weight:600;font-size:33px;letter-spacing:-.02em}
.topbar .sub{color:var(--ink-soft);font-size:13.5px;margin-top:4px}
.pill{display:inline-flex;align-items:center;gap:8px;background:var(--accent-soft);color:var(--jade);
  font-weight:700;font-size:12.5px;padding:8px 14px;border-radius:999px;border:1px solid var(--accent-soft-bd)}
.pill .led{width:8px;height:8px;border-radius:50%;background:var(--jade-2);box-shadow:0 0 0 3px #BFE6E1}
.topbar-right{display:flex;align-items:center;gap:10px}
.themebtn{all:unset;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:10px;border:1px solid var(--line);background:var(--paper-2);color:var(--ink-soft);box-shadow:var(--shadow);transition:.18s}
.themebtn:hover{color:var(--jade);border-color:var(--accent-soft-bd)}
.themebtn svg{width:18px;height:18px}
.themebtn .sun{display:none}.themebtn .moon{display:block}
[data-theme="dark"] .themebtn .moon{display:none}[data-theme="dark"] .themebtn .sun{display:block}
.page{display:none;animation:fade .4s ease}
.page.active{display:block}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
/* kpi */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px}
.kpi{background:var(--paper-2);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.kpi .lab{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.kpi .lab .en{display:block;font-size:9.5px;letter-spacing:.08em;color:var(--muted);font-weight:600;margin-top:2px}
.kpi .val{font-family:'Inter',sans-serif;font-size:33px;font-weight:600;margin-top:12px;letter-spacing:-.02em;line-height:1}
.kpi .val .u{font-size:16px;color:var(--ink-soft);font-family:'Inter';font-weight:700;margin-left:3px}
.kpi .meta{font-size:12px;color:var(--ink-soft);margin-top:8px}
.kpi.accent{background:var(--jade);color:#fff;border-color:var(--jade)}
.kpi.accent .lab,.kpi.accent .meta{color:#BFE0D6}.kpi.accent .lab .en{color:#8FBFB1}
.kpi.accent .val .u{color:#BFE0D6}
.kpi-sm{grid-template-columns:repeat(4,1fr)}
.kpi-sm .kpi{padding:16px}.kpi-sm .val{font-size:25px}
/* card */
.card{background:var(--paper-2);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:var(--shadow);margin-top:18px}
.card h2{font-family:'Inter',sans-serif;font-weight:600;font-size:20px;letter-spacing:-.01em}
.card .h-en{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:2px;margin-bottom:18px}
.grid2{display:grid;grid-template-columns:1.55fr 1fr;gap:18px}
/* chart */
.chart{width:100%}
.bars{display:flex;align-items:flex-end;gap:14px;height:200px;padding-top:10px}
.bar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:7px;height:100%;justify-content:flex-end}
.bar-wrap{width:100%;display:flex;justify-content:center;align-items:flex-end;gap:4px;height:100%}
.bar{width:46%;border-radius:6px 6px 2px 2px;background:linear-gradient(180deg,var(--jade-2),var(--jade));position:relative;transition:.6s cubic-bezier(.2,.8,.2,1)}
.bar.spend{background:linear-gradient(180deg,#D9B36A,var(--gold));width:30%}
.bar .roas{position:absolute;top:-20px;left:50%;transform:translateX(-50%);font-size:10.5px;font-weight:700;color:var(--jade);white-space:nowrap}
.bar-x{font-size:11px;color:var(--ink-soft);font-weight:600}
.bar-x b{display:block;color:var(--ink);font-size:12px}
.legend{display:flex;gap:20px;margin-top:8px;font-size:12px;color:var(--ink-soft);font-weight:600}
.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px}
/* hbars */
.hbar{display:flex;align-items:center;gap:12px;margin:11px 0}
.hbar .nm{width:96px;font-weight:700;font-size:13px;flex-shrink:0}
.hbar .track{flex:1;height:26px;background:var(--tint2);border-radius:7px;overflow:hidden;position:relative}
.hbar .fill{height:100%;border-radius:7px;background:linear-gradient(90deg,var(--jade),var(--jade-2));
  display:flex;align-items:center;justify-content:flex-end;padding-right:9px;color:#fff;font-weight:700;font-size:12px;transition:.7s cubic-bezier(.2,.8,.2,1)}
.hbar .vv{width:78px;text-align:right;font-weight:700;font-size:13px;color:var(--ink)}
/* table */
table{width:100%;border-collapse:collapse;margin-top:6px;font-size:13.5px}
th{text-align:left;padding:11px 12px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-soft);border-bottom:2px solid var(--line);font-weight:700}
td{padding:12px;border-bottom:1px solid var(--line);font-weight:600;text-align:left}
tr:last-child td{border-bottom:none}
.tag{display:inline-block;padding:3px 9px;border-radius:6px;font-size:11.5px;font-weight:700}
.tag.good{background:var(--accent-soft);color:var(--jade)}.tag.warn{background:var(--gold-soft);color:var(--gold)}
.tag.bad{background:var(--rose-soft);color:var(--rose)}.tag.na{background:var(--tint);color:var(--muted)}
/* platform */
.statusb{padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800;white-space:nowrap}
.s-Scale{background:rgba(18,149,90,.14);color:var(--pos)}.s-Cut{background:rgba(217,58,44,.14);color:var(--neg)}
.s-Watch{background:rgba(207,148,18,.16);color:var(--warn)}.s-Hold{background:var(--tint2);color:var(--ink-soft)}.s-Giữ{background:var(--accent-soft);color:var(--jade-2)}
.plat{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.platc{border:1px solid var(--line);border-radius:16px;padding:22px;background:var(--paper-2)}
.platc .ph{display:flex;align-items:center;gap:10px;font-weight:800;font-size:16px}
.platc .ph .ic{width:30px;height:30px;border-radius:8px;display:grid;place-items:center;color:#fff;font-weight:800;font-size:13px}
.platc .row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--line);font-size:14px}
.platc .row:last-child{border:none}.platc .row b{font-weight:800}
.donut{width:150px;height:150px;border-radius:50%;margin:6px auto}
/* memo */
.memo{font-size:14.5px;line-height:1.72}
.memo h3{font-family:'Inter',sans-serif;font-size:17px;margin:20px 0 8px;color:var(--jade);font-weight:600}
.memo h3:first-child{margin-top:0}
.memo ul,ul.memo{margin:0 0 4px 2px;list-style:none;padding-left:0}
.memo li{padding:5px 0 5px 22px;position:relative}
.memo li:before{content:'';position:absolute;left:4px;top:13px;width:6px;height:6px;border-radius:50%;background:var(--gold)}
.memo .act{padding:5px 0 5px 22px;position:relative}
.memo .act:before{content:'→';position:absolute;left:2px;top:5px;color:var(--jade);font-weight:800}
.memo .head{background:var(--tint);border-left:3px solid var(--jade);padding:14px 18px;border-radius:0 10px 10px 0;font-size:13.5px;line-height:1.7}
.dpos{color:var(--pos);font-weight:800}.dneg{color:var(--neg);font-weight:800}.dwarn{color:var(--warn);font-weight:800}.dmut{color:var(--ink-soft)}
.seemore{background:none;border:none;color:var(--jade);font-weight:700;font-size:12.5px;cursor:pointer;padding:0;font-family:inherit}
.seemore:hover{text-decoration:underline}
.cardhd{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.tier{font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);margin-bottom:4px}
.alertbox{display:flex;gap:10px;align-items:flex-start;padding:10px 14px;border-radius:10px;margin-bottom:8px;font-size:13.5px;font-weight:600}
.alertbox.red{background:rgba(217,58,44,.10);color:var(--neg)}.alertbox.amber{background:rgba(207,148,18,.13);color:var(--warn)}.alertbox.ok{background:rgba(18,149,90,.12);color:var(--pos)}
.actrow{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--line)}
.actrow:last-child{border:none}.actrow .pr{font-weight:800;font-size:11px;padding:3px 8px;border-radius:6px;white-space:nowrap}
.pr.P1{background:rgba(217,58,44,.14);color:var(--neg)}.pr.P2{background:rgba(207,148,18,.16);color:var(--warn)}
.note{font-size:12.5px;color:var(--ink-soft);background:var(--tint);border-radius:10px;padding:12px 15px;margin-top:16px;line-height:1.6}
.note b{color:var(--ink)}
/* svg combo chart */
.combo{width:100%;height:auto;display:block;margin-top:6px}
.combo text.roas{font:700 11px Inter;fill:var(--jade);text-anchor:middle}
.combo text.xl{font:700 12px Inter;fill:var(--ink);text-anchor:middle}
.combo text.xs{font:600 11px Inter;fill:var(--ink-soft);text-anchor:middle}
.combo text.ml{font:700 10px Inter;fill:var(--rose);text-anchor:middle}
.combo text.ax{font:600 10px Inter;fill:var(--muted)}
.kpi .per{font-size:11px;font-weight:700;color:var(--muted);font-family:'Inter';margin-left:6px;letter-spacing:.04em}
.kpi.accent .per{color:#8FBFB1}
.chg{font-size:10px;font-weight:800;margin-left:5px;font-family:'Inter';letter-spacing:.01em;white-space:nowrap}
.chg-up{color:#1A9956}
.chg-down{color:#D64545}
.chg-neu{color:var(--muted)}
.kpi.accent .chg-up{color:#7FE3B0}.kpi.accent .chg-down{color:#F2A6A6}.kpi.accent .chg-neu{color:#8FBFB1}
.kpis.six{grid-template-columns:repeat(6,1fr);gap:12px}
.kpis.six .kpi{padding:15px}
.kpis.six .val{font-size:26px}
.kpis.six .lab{font-size:10px}
.kpis.six .lab .en{font-size:8.8px}
.kpis.six .meta{font-size:11px}
.sub3{margin-top:10px;display:flex;flex-direction:column;gap:3px;font-size:11px;color:var(--ink-soft);line-height:1.35}
.sub3 span b{color:var(--ink);font-weight:700}
.kpi.accent .sub3{color:#BFE0D6}.kpi.accent .sub3 span b{color:#fff}
.ranges{display:flex;gap:7px;flex-wrap:wrap;margin:2px 0 4px}
.ranges button{all:unset;cursor:pointer;font-size:12.5px;font-weight:700;color:var(--ink-soft);
  padding:6px 13px;border-radius:999px;border:1px solid var(--line);transition:.15s}
.ranges button:hover{border-color:var(--jade-2);color:var(--jade)}
.ranges button.on{background:var(--jade);color:#fff;border-color:var(--jade)}
.custom{display:flex;align-items:center;gap:8px;margin:4px 0 6px;font-size:13px;color:var(--ink-soft)}
.custom input{font-family:'Inter';font-size:13px;padding:6px 9px;border:1px solid var(--line);border-radius:8px;background:var(--paper-2);color:var(--ink)}
.custom button{all:unset;cursor:pointer;background:var(--jade);color:#fff;font-weight:700;font-size:12.5px;padding:7px 14px;border-radius:8px}
.combo .hit{transition:.12s}
.tip{position:fixed;z-index:50;display:none;background:#15201D;color:#EDE9DD;border:1px solid rgba(255,255,255,.09);border-radius:12px;
  padding:13px 15px;box-shadow:0 10px 30px rgba(0,0,0,.28);pointer-events:none;min-width:188px;font-size:12.5px}
.tip .tt-d{font-family:'Inter',sans-serif;font-weight:600;font-size:15px;margin-bottom:8px;color:#fff}
.tip .tt-r{display:flex;justify-content:space-between;gap:18px;padding:3px 0}
.tip .tt-r span{color:#A29A86}.tip .tt-r b{font-weight:700;color:#fff}
.tip .tt-r.hl b{color:#A9D5C8}
/* 3-gate funnel */
.gates{display:flex;align-items:stretch;gap:10px;margin-top:16px}
.gates .gate{flex:1;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:17px}
.ghead{display:flex;gap:10px;align-items:flex-start;margin-bottom:13px}
.gnum{width:29px;height:29px;border-radius:9px;display:grid;place-items:center;color:#fff;font-weight:800;font-size:14px;flex-shrink:0}
.ghead b{font-size:14px;font-weight:800;display:block;line-height:1.18}
.ghead i{font-style:normal;font-size:11px;color:var(--ink-soft);display:block;margin-top:3px}
.gbig{font-family:'Inter',sans-serif;font-size:29px;font-weight:600;letter-spacing:-.02em;line-height:1;margin-bottom:11px}
.gbig span{font-family:'Inter';font-size:12.5px;color:var(--ink-soft);font-weight:700;margin-left:5px}
.grow{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-top:1px solid var(--line);font-size:12.5px}
.grow span{color:var(--ink-soft)}.grow b{font-weight:700;text-align:right;white-space:nowrap}
.gsplit{font-size:11px;color:var(--ink-soft);margin-top:7px;line-height:1.5}
.gby{font-size:11px;color:var(--ink-soft);margin-top:7px;line-height:1.55}
.gby b{color:var(--ink);font-weight:700}
.garrow{display:flex;align-items:center;font-size:20px;color:#C7BFA8;font-weight:700}
.fnl{display:grid;column-gap:14px;row-gap:18px;margin-top:16px;align-items:stretch}
.fcard{background:var(--paper);border:1px solid var(--accent-soft-bd);box-shadow:0 0 0 3px var(--accent-soft);border-radius:16px;padding:16px 17px;display:flex;flex-direction:column;grid-row:1}
.fcard.lead{border-color:var(--gold);box-shadow:0 0 0 3px var(--gold-soft)}
.fch{display:flex;align-items:center;gap:11px;margin-bottom:13px}
.ficon{width:38px;height:38px;border-radius:11px;background:var(--accent-soft);display:grid;place-items:center;flex-shrink:0;color:var(--jade)}
.ficon svg{width:20px;height:20px}
.fcard.lead .ficon{background:var(--gold-soft);color:var(--gold)}
.fch .ft{min-width:0}
.fch .fnm{font-size:14.5px;font-weight:800;line-height:1.12}
.fch .fsub{font-size:11px;color:var(--ink-soft);margin-top:2px;line-height:1.25}
.fbig{font-family:'Inter',sans-serif;font-size:33px;font-weight:600;letter-spacing:-.02em;line-height:1}
.fbig small{font-size:12px;font-weight:700;color:var(--ink-soft);margin-left:5px}
.frows{margin-top:12px;display:flex;flex-direction:column}
.fm{display:flex;justify-content:space-between;gap:10px;padding:6px 0;font-size:12.5px;border-top:1px solid var(--line)}
.fm .fl{color:var(--ink-soft)} .fm .fv{font-weight:700;text-align:right;white-space:nowrap}
.fm.coc .fv{color:var(--gold)}
.fsub2{display:flex;align-items:center;gap:7px;font-size:9.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--gold);margin-top:10px;padding-top:8px;border-top:1px solid var(--line)}
.fsub2::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--gold);flex-shrink:0}
.fby{font-size:11px;color:var(--ink-soft);margin-top:11px;line-height:1.6}
.fby b{color:var(--ink);font-weight:700}
.fwait{font-size:10px;font-style:italic;color:var(--muted);margin-top:11px;padding-top:9px;border-top:1px dashed var(--line)}
.fchip{grid-row:2;justify-self:center;display:flex;flex-direction:column;align-items:center;gap:5px;max-width:235px;text-align:center;position:relative;z-index:1}
.fline{align-self:start;margin-top:42px;display:flex;align-items:center;z-index:0;pointer-events:none;opacity:.7}
.fdot{width:7px;height:7px;border-radius:50%;background:var(--accent-soft-bd);flex-shrink:0;margin-right:-1px}
.fbar{flex:1;height:3px;border-radius:3px;background:linear-gradient(90deg,transparent,var(--accent-soft-bd) 14%,var(--jade-2) 92%)}
.fhd{width:0;height:0;border-top:7px solid transparent;border-bottom:7px solid transparent;border-left:11px solid var(--jade-2);margin-left:-1px}
.fchip .carr{font-size:18px;font-weight:800;line-height:1}
.fpill{display:flex;align-items:center;gap:11px;background:var(--paper-2);border:1px solid var(--gold);border-radius:13px;padding:9px 14px;box-shadow:0 0 0 3px var(--gold-soft)}
.fpill .cnum{width:25px;height:25px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:800;font-size:12.5px;flex-shrink:0}
.fpill .cbox{text-align:left;min-width:0}
.fpill .cv{font-family:'Inter',sans-serif;font-size:18px;font-weight:700;line-height:1;letter-spacing:-.01em}
.fpill .cl{font-size:8.5px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-soft);margin-top:3px}
.ffml{font-size:10px;font-style:italic;color:var(--muted)}
.fdrop{font-size:9.5px;font-weight:800}
.finfo{flex:0 0 auto;width:16px;height:16px;border-radius:50%;border:1px solid var(--line);color:var(--muted);font:italic 700 10px/14px Georgia,serif;display:flex;align-items:center;justify-content:center;cursor:help;position:relative;margin-left:2px}
.ftip{display:none;position:absolute;bottom:135%;left:50%;transform:translateX(-50%);width:240px;background:var(--paper-2);border:1px solid var(--line);border-radius:9px;padding:9px 11px;font-size:11px;font-style:normal;font-weight:500;line-height:1.6;color:var(--ink);text-align:left;white-space:normal;z-index:60;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.finfo:hover .ftip,.finfo:focus .ftip{display:block}
.fdrop.ns{color:var(--rose)} .fdrop.rot{color:var(--gold)}
.fstar{font-size:8.5px;font-weight:800;color:var(--gold);letter-spacing:.05em;text-transform:uppercase}
@media(max-width:760px){.fnl{display:flex!important;flex-direction:column;grid-template-columns:none!important}.fcard,.fchip{grid-column:auto!important;grid-row:auto!important;justify-self:stretch}.fchip{max-width:none;flex-direction:row;flex-wrap:wrap;justify-content:flex-start;gap:9px}.fchip .carr{transform:rotate(90deg)}.fline{display:none}}
#chartBox{margin-top:14px}
/* pie / donut */
.piewrap{display:flex;gap:28px;align-items:center;flex-wrap:wrap;margin-top:6px}
.svcpies{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}
.svcpie-main{flex:2;min-width:300px}
.svcpie-side{flex:1;min-width:210px;border-left:1px solid var(--line);padding-left:24px}
.piewrap.small{flex-direction:column;align-items:center;gap:12px}
.piewrap.small .pie{max-width:170px}
.piewrap.small .pie svg{width:160px;height:160px}
.piewrap.small .pielegend{width:100%}
@media(max-width:760px){.svcpie-side{border-left:none;border-top:1px solid var(--line);padding-left:0;padding-top:18px;margin-top:4px}}
.pie svg{width:300px;height:300px}
.pie .slice{cursor:pointer;transition:opacity .12s}
.pie .slice:hover{opacity:.82}
.pielegend{flex:1;min-width:240px;display:flex;flex-direction:column;gap:9px}
.pli{display:flex;align-items:center;gap:10px;font-size:13.5px}
.pli .sw{width:13px;height:13px;border-radius:4px;flex-shrink:0}
.pli .pnm{font-weight:700;min-width:74px}
.pli .pval{color:var(--ink-soft);margin-left:auto;font-variant-numeric:tabular-nums}
.pli .ppct{font-weight:800;min-width:42px;text-align:right;font-variant-numeric:tabular-nums}
.svctbl td .mini{color:var(--ink-soft);font-size:11px}
.cvtag{font-weight:700;padding:2px 8px;border-radius:999px;font-size:11.5px}
.spark{display:block;width:100%;cursor:help}
.kspark{height:28px;margin-top:11px}
.tspark{height:20px;width:82px}
.sparkline{fill:none;stroke:var(--jade);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.sparkfill{fill:var(--jade);opacity:.08;stroke:none}
.spark.spk-pos .sparkline{stroke:var(--pos)}.spark.spk-pos .sparkfill{fill:var(--pos)}
.spark.spk-neg .sparkline{stroke:var(--neg)}.spark.spk-neg .sparkfill{fill:var(--neg)}
.spark.spk-neu .sparkline{stroke:var(--ink-soft)}.spark.spk-neu .sparkfill{fill:var(--ink-soft)}
.kpi.accent .sparkline{stroke:#fff}.kpi.accent .sparkfill{fill:#fff;opacity:.2}
.sparkna{color:var(--muted);font-size:11px}
.pctsub{font-size:11px;color:var(--muted);font-weight:400}
#sales table td{white-space:nowrap}
.lbgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px;margin-bottom:18px}
.lbgrid.lb4{grid-template-columns:repeat(4,1fr)}
@media(max-width:1100px){.lbgrid.lb4{grid-template-columns:repeat(2,1fr)}}
@media(max-width:820px){.lbgrid,.lbgrid.lb4{grid-template-columns:1fr}}
.lb{background:var(--paper-2);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:var(--shadow);cursor:pointer;transition:border-color .15s,transform .1s,box-shadow .15s}
.lb:hover{border-color:var(--jade-2);transform:translateY(-2px);box-shadow:0 6px 20px rgba(27,26,22,.10)}
.lb-h{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:1px}
.lb-t{font-weight:700;font-size:14.5px;color:var(--ink)}
.lb-x{font-size:11px;color:var(--jade-2);white-space:nowrap;font-weight:600}
.lb-sub{font-size:11px;color:var(--muted);margin-bottom:9px}
.lbrow{display:flex;align-items:center;gap:10px;padding:5px 0;font-size:13px;border-top:1px solid var(--line)}
.lbrow:first-of-type{border-top:none}
.lbrank{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;background:var(--tint);color:var(--ink-soft);flex-shrink:0}
.lbrank.g{background:#F4C84A;color:#5a4500}.lbrank.s{background:#C9D2D8;color:#33414a}.lbrank.b{background:#E0A878;color:#5a3210}
.lbnm{flex:1;font-weight:600;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lbval{font-weight:700;color:var(--ink);white-space:nowrap;font-size:12.5px}
.ihead{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 10px}
.insights{display:flex;flex-direction:column;gap:10px}
.insight{background:var(--paper);border:1px solid var(--line);border-left-width:4px;border-radius:11px;padding:12px 15px}
.insight.s3{border-left-color:var(--neg)}.insight.s2{border-left-color:var(--warn)}.insight.s1{border-left-color:var(--jade-2)}
.insight .it{font-weight:700;font-size:14.5px;margin-bottom:7px;color:var(--ink);display:flex;align-items:center;gap:9px}
.insight .sevdot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.insight.s3 .sevdot{background:var(--neg)}.insight.s2 .sevdot{background:var(--warn)}.insight.s1 .sevdot{background:var(--jade-2)}
.insight .row{font-size:13px;color:var(--ink-soft);margin:3px 0;display:flex;gap:8px;line-height:1.5}
.insight .row span:last-child{flex:1}.insight .row b{color:var(--ink)}
.insight .k{color:var(--muted);min-width:78px;flex-shrink:0}
td.mtd{font-weight:700;color:var(--ink)}
.cvtag.cg{background:rgba(18,149,90,.14);color:var(--pos)}
.cvtag.cm{background:rgba(207,148,18,.16);color:var(--warn)}
.cvtag.cb{background:rgba(217,58,44,.14);color:var(--neg)}
.rev3{display:flex;gap:14px;flex-wrap:wrap}
.rev3 .rc{flex:1;min-width:160px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.rev3 .rc .l{font-size:11.5px;color:var(--ink-soft);font-weight:700;letter-spacing:.03em;text-transform:uppercase}
.rev3 .rc .v{font-family:'Inter',sans-serif;font-size:25px;font-weight:600;margin-top:6px}
.rev3 .rc .s{font-size:11.5px;color:var(--ink-soft);margin-top:4px}
.rev3 .rc.done{background:var(--accent-soft);border-color:var(--jade-2)}
/* division */
.dvgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}
@media(max-width:820px){.dvgrid{grid-template-columns:1fr}}
.dvcard{background:var(--paper-2);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:var(--shadow);overflow:hidden}
.dvcard.noi{border-top:3px solid var(--jade)}.dvcard.ngoai{border-top:3px solid var(--gold)}
.dv-h{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.dv-name{font-family:'Inter',sans-serif;font-weight:600;font-size:21px;letter-spacing:-.01em}
.dv-grp{font-size:11.5px;color:var(--muted);margin-top:3px}
.dv-share{font-size:12px;font-weight:700;color:var(--ink-soft);background:var(--tint);padding:5px 11px;border-radius:999px;white-space:nowrap}
.dv-hero{margin:16px 0 4px}
.dv-pct{font-family:'Inter',sans-serif;font-size:40px;font-weight:600;line-height:1}
.dv-pct small{font-size:15px;color:var(--ink-soft);font-weight:600}
.dv-tcap{font-size:12.5px;color:var(--ink-soft);margin-top:5px}
.dv-track{height:14px;background:var(--tint2);border-radius:8px;overflow:hidden;margin-top:12px}
.dv-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,var(--jade),var(--jade-2));transition:.7s cubic-bezier(.2,.8,.2,1)}
.dvcard.ngoai .dv-fill{background:linear-gradient(90deg,#d8b15a,var(--gold))}
.dv-proj{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:13px;color:var(--ink-soft);flex-wrap:wrap}
.dv-pill{font-weight:700;font-size:11.5px;padding:3px 9px;border-radius:999px}
.dv-pill.ok{background:rgba(18,149,90,.14);color:var(--pos)}.dv-pill.behind{background:rgba(207,148,18,.16);color:var(--warn)}.dv-pill.bad{background:rgba(217,58,44,.14);color:var(--neg)}
.dv-metrics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-top:18px}
.dv-m{background:var(--paper-2);padding:12px 14px}
.dv-m .l{font-size:10.5px;color:var(--muted);font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.dv-m .v{font-family:'Inter',sans-serif;font-size:18px;font-weight:600;margin-top:3px}
.dv-svc{margin-top:16px}
.dv-svc .sr{display:flex;align-items:center;gap:10px;margin:7px 0;font-size:12.5px}
.dv-svc .sn{width:74px;color:var(--ink-soft);font-weight:600;flex-shrink:0}
.dv-svc .st{flex:1;height:9px;background:var(--tint2);border-radius:5px;overflow:hidden}
.dv-svc .sf{height:100%;background:var(--jade-2);border-radius:5px}
.dvcard.ngoai .dv-svc .sf{background:var(--gold)}
.dv-svc .sv{width:56px;text-align:right;font-weight:700;font-size:12px}
.dv-bar{display:flex;height:22px;border-radius:7px;overflow:hidden;margin-top:14px}
.dv-bar .seg.n{background:linear-gradient(90deg,var(--jade),var(--jade-2))}.dv-bar .seg.g{background:linear-gradient(90deg,#d8b15a,var(--gold))}
.dv-leg{display:flex;gap:22px;margin-top:10px;font-size:13px;color:var(--ink-soft);flex-wrap:wrap}
.dv-leg i.d{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:middle}
.dv-leg i.d.n{background:var(--jade)}.dv-leg i.d.g{background:var(--gold)}
.dvtag{font-size:9.5px;font-weight:700;padding:1px 6px;border-radius:999px;margin-left:7px;vertical-align:middle;letter-spacing:.03em}
.dvtag.noi{background:rgba(15,123,116,.13);color:var(--jade)}
.dvtag.ngoai{background:rgba(182,128,42,.16);color:var(--gold)}
.divbar{display:flex;align-items:center;gap:8px;margin:-4px 0 2px;flex-wrap:wrap}
.divbar-lbl{font-size:11.5px;color:var(--muted);font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-right:2px}
.divbar button{font-family:'Inter',sans-serif;font-size:13px;font-weight:600;cursor:pointer;color:var(--ink-soft);background:var(--paper-2);padding:6px 15px;border-radius:999px;border:1px solid var(--line);transition:.15s}
.divbar button:hover{border-color:var(--jade-2)}
.divbar button.on{background:var(--jade);color:#fff;border-color:var(--jade)}
.divbar button.on[data-d="Ngoại khoa"]{background:var(--gold);border-color:var(--gold)}
.dshead{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:14px}
.dslink{cursor:pointer;color:var(--jade-2);font-weight:600;font-size:12.5px;white-space:nowrap}
.dsrows{display:flex;flex-direction:column;gap:12px}
.dsr-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:5px;font-size:13px;flex-wrap:wrap}
.dslab{font-weight:700}.dslab.n{color:var(--jade)}.dslab.g{color:var(--gold)}
.dsval{font-weight:700;font-size:13px}
.dstrack{height:10px;background:var(--tint2);border-radius:6px;overflow:hidden}
.dsfill{height:100%;border-radius:6px}.dsfill.n{background:linear-gradient(90deg,var(--jade),var(--jade-2))}.dsfill.g{background:linear-gradient(90deg,#d8b15a,var(--gold))}
.dvbar2{display:flex;height:16px;border-radius:6px;overflow:hidden;margin-top:16px}
.dvbar2 .seg.n{background:linear-gradient(90deg,var(--jade),var(--jade-2))}.dvbar2 .seg.g{background:linear-gradient(90deg,#d8b15a,var(--gold))}
.dsleg{display:flex;gap:20px;margin-top:9px;font-size:12.5px;color:var(--ink-soft);flex-wrap:wrap}
.dsleg i.d{display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:6px;vertical-align:middle}
.dsleg i.d.n{background:var(--jade)}.dsleg i.d.g{background:var(--gold)}
.dqbar{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.dqchip{font-size:11.5px;padding:5px 11px;border-radius:999px;font-weight:600;background:var(--tint);color:var(--ink-soft)}
.dqchip.warn{background:var(--gold-soft);color:var(--warn)}.dqchip.ok{background:rgba(18,149,90,.12);color:var(--pos)}
.ntk{display:flex;gap:14px;flex-wrap:wrap}
.ntk .nc{flex:1;min-width:220px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.ntk .nc h4{font-size:14px;font-weight:800;margin-bottom:10px}
.ntk .nc .r{display:flex;justify-content:space-between;padding:4px 0;font-size:12.5px;border-top:1px solid var(--line)}
.ntk .nc .r span{color:var(--ink-soft)}.ntk .nc .r b{font-weight:700}
.src{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.src span{font-size:11.5px;background:var(--tint);color:var(--ink-soft);padding:6px 11px;border-radius:7px;font-weight:600}
.src span b{color:var(--jade)}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%}
.grid2>*,.plat>*{min-width:0}
@media(max-width:880px){
  .app{grid-template-columns:1fr;align-content:start;min-height:0}
  .side{position:static;height:auto;flex-direction:column;padding:16px}
  .brand{font-size:21px}
  .nav{flex-direction:row;flex-wrap:wrap;gap:6px;margin-top:12px}
  .nav button{padding:8px 11px;font-size:12.5px;gap:7px}
  .nav button .en,.nav .dot{display:none}
  .side-foot{display:none}
  .main{padding:18px 14px 48px;max-width:100%}
  .topbar{margin-bottom:18px;gap:10px}
  .topbar h1{font-size:23px}
  .pill{font-size:11px;padding:7px 11px}
  .card{padding:15px}
  .card h2{font-size:17px}
  .kpis,.kpi-sm,.kpis.six{grid-template-columns:repeat(2,1fr)!important;gap:10px}
  .kpi{padding:14px}.kpi .val,.kpis.six .val{font-size:23px}
  .grid2,.plat{grid-template-columns:1fr!important}
  .rev3,.ntk{flex-direction:column}
  .gates{flex-direction:column}.garrow{transform:rotate(90deg);align-self:center;margin:2px 0}
  .bars{gap:5px;height:165px}
  .card svg{max-width:100%;height:auto}
  .tscroll table{white-space:nowrap}
  .tscroll table th,.tscroll table td{padding:9px 10px}
}
@media(max-width:520px){
  .kpis{grid-template-columns:1fr!important}
  .ranges button{font-size:11.5px;padding:5px 9px}
}
</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand">Swan Clinic<small>Bảng điều khiển CEO</small></div>
    <nav class="nav" id="nav">
      <button data-p="overview" class="active"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg><span class="vi">Tổng quan</span></button>
      <button data-p="division"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><rect x="3" y="6" width="6" height="12" rx="1"/><rect x="15" y="9" width="6" height="9" rx="1"/></svg><span class="vi">Nội / Ngoại</span></button>
      <button data-p="service"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.7 4.6L18 9l-4.3 1.4L12 15l-1.7-4.6L6 9l4.3-1.4z"/><path d="M18.5 14.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8L16 16.3l1.8-.7z"/></svg><span class="vi">Dịch vụ</span></button>
      <button data-p="platform"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 16-6v14L3 13z"/><path d="M8 13v4a2 2 0 0 0 4 0v-1"/></svg><span class="vi">Nền tảng</span></button>
      <button data-p="sales"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg><span class="vi">Sale</span></button>
      <button data-p="master"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3H3v2a4 4 0 0 0 8 0V3h-1"/><path d="M7 11v3a6 6 0 0 0 12 0v-2"/><circle cx="19" cy="10" r="2"/></svg><span class="vi">Master</span></button>
      <button data-p="cross"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M6 9v3a6 6 0 0 0 6 6h3"/><path d="M15 12l3-3-3-3"/></svg><span class="vi">Bán chéo</span></button>
      <button data-p="memo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8M16 17H8M10 9H8"/></svg><span class="vi">Bản tin CEO</span></button>
    </nav>
    <div class="side-foot">
      Nguồn dữ liệu tự động:<br>
      <b>Google Drive</b> — doanh thu<br>
      <b>Meta Ads API</b> — quảng cáo<br>
      <b>TikTok Ads API</b> — quảng cáo<br><br>
      Cập nhật mỗi ngày <b>trước 6:00</b>.
    </div>
  </aside>
  <main class="main">
    <div class="topbar">
      <div>
        <h1 id="ptitle">Tổng quan vận hành</h1>
        <div class="sub" id="psub"></div>
      </div>
      <div class="topbar-right">
        <div class="pill" id="statuspill"><span class="led"></span> Đang tải…</div>
        <button class="themebtn" id="themebtn" onclick="toggleTheme()" title="Đổi giao diện Sáng / Tối" aria-label="Đổi giao diện">
          <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
        </button>
      </div>
    </div>

    <div class="divbar" id="divbar" style="display:none">
      <span class="divbar-lbl">Lọc division</span>
      <button data-d="all" class="on" onclick="setDiv('all')">Tất cả</button>
      <button data-d="Nội khoa" onclick="setDiv('Nội khoa')">Nội khoa</button>
      <button data-d="Ngoại khoa" onclick="setDiv('Ngoại khoa')">Ngoại khoa</button>
    </div>

    <section class="page active" id="overview"></section>
    <section class="page" id="division"></section>
    <section class="page" id="service"></section>
    <section class="page" id="platform"></section>
    <section class="page" id="sales"></section>
    <section class="page" id="master"></section>
    <section class="page" id="cross"></section>
    <section class="page" id="memo"></section>
  </main>
</div>
<div id="tip" class="tip"></div>

<script>
/* In production the daily 5:45 job overwrites data.json; the dashboard would
   fetch('data.json'). For this standalone preview the real parsed week is embedded. */
let DATA = __DATA__;   // embedded = fallback cho bản xem trước; production sẽ fetch data.json

const sum=(a,f)=>a.reduce((s,x)=>s+f(x),0);
let S,wk,TODAY_DATE,LATEST_DATA,STALE,COMPLETE,TODAYREC,BASE,YDAY,_INS;
function deriveGlobals(){
  _INS=null;
  S=DATA.series;
  wk={rev:sum(S,s=>s.operating),gross:sum(S,s=>s.gross),spend:sum(S,s=>s.spend),
    meta:sum(S,s=>s.meta_spend),tk:sum(S,s=>s.tk_spend),cust:sum(S,s=>s.customers),
    paying:sum(S,s=>s.paying),coc:sum(S,s=>s.coc),zero:sum(S,s=>s.zero),
    msg:sum(S,s=>s.meta_msg+s.tk_msg),metamsg:sum(S,s=>s.meta_msg),tkmsg:sum(S,s=>s.tk_msg)};
  wk.roas=wk.rev/wk.spend; wk.cpl=wk.spend/wk.msg; wk.aov=wk.rev/wk.paying;
  TODAY_DATE=DATA.system_today||DATA.today||S[S.length-1].date;  // hôm nay = ngày hệ thống
  LATEST_DATA=S[S.length-1].date;
  const _yest=new Date(new Date(TODAY_DATE+'T00:00:00').getTime()-86400000).toISOString().slice(0,10);
  STALE=LATEST_DATA<_yest;                         // chỉ "cũ" khi thiếu cả ngày hôm qua (DT trễ 1 ngày là bình thường)
  COMPLETE=S.filter(s=>s.date<TODAY_DATE);        // ngày đã chốt (loại hôm nay)
  TODAYREC=S.find(s=>s.date===TODAY_DATE)||null;  // hôm nay (chưa đủ ngày)
  BASE=COMPLETE.length?COMPLETE:S;                // fallback nếu chưa có ngày chốt
  YDAY=BASE[BASE.length-1];                       // hôm qua = ngày chốt gần nhất
}
deriveGlobals();
const MO=YDAY.date.slice(0,7);
let _SDIV=null;
function seriesDivFallback(){
  if(_SDIV) return _SDIV;
  const out={'Nội khoa':[],'Ngoại khoa':[]};
  DATA.series.forEach(s=>{
    const rbs=s.rev_by_service||{}; let ngRev=0;
    for(const g in rbs){if(DIVMAP_JS[g]==='Ngoại khoa')ngRev+=rbs[g];}
    const rev=s.revenue||0; ngRev=Math.min(ngRev,rev);
    const ngSh=rev?ngRev/rev:0, noiSh=1-ngSh;
    const mk=(dv,sh,noi)=>{
      const rbd={}; for(const g in rbs){if(DIVMAP_JS[g]===dv)rbd[g]=rbs[g];}
      const bv=s.bill_values||[], k=Math.round(bv.length*sh);
      const bvd=noi?bv.slice(0,k||(rev*sh>0?1:0)):bv.slice(Math.max(0,bv.length-k));
      const r=Math.round(rev*sh);
      return {date:s.date,revenue:r,operating:r,gross:Math.round((s.gross||rev)*sh),
        deposit:Math.round((s.deposit||0)*sh),cash_in:Math.round((s.cash_in||rev)*sh),
        customers:Math.round((s.customers||0)*sh),paying:Math.round((s.paying||0)*sh),
        coc:Math.round((s.coc||0)*sh),zero:Math.round((s.zero||0)*sh),
        new:Math.round((s.new||0)*sh),tk:Math.round((s.tk||0)*sh),
        bill_values:bvd,rev_by_service:rbd,deposit_by_service:{},
        bills_total:Math.round((s.bills_total||0)*sh),bills_multi:Math.round((s.bills_multi||0)*sh),
        crosssell_rev:Math.round((s.crosssell_rev||0)*sh),
        meta_spend:noi?(s.meta_spend||0):0,tk_spend:noi?(s.tk_spend||0):0,spend:noi?(s.spend||0):0,
        meta_msg:noi?(s.meta_msg||0):0,tk_msg:noi?(s.tk_msg||0):0,msg_by_service:noi?(s.msg_by_service||{}):{},
        roas:(noi&&s.spend)?+(r/s.spend).toFixed(1):0};
    };
    out['Nội khoa'].push(mk('Nội khoa',noiSh,true));
    out['Ngoại khoa'].push(mk('Ngoại khoa',ngSh,false));
  });
  // Hiệu chỉnh tổng mỗi mảng khớp với khối divisions (bill-level) để mọi card trên overview nhất quán
  ['Nội khoa','Ngoại khoa'].forEach(dv=>{
    const item=((DATA.divisions&&DATA.divisions.items)||[]).find(x=>x.name===dv); if(!item)return;
    const sR=out[dv].reduce((a,s)=>a+s.revenue,0)||1, sD=out[dv].reduce((a,s)=>a+s.deposit,0)||1, sC=out[dv].reduce((a,s)=>a+s.customers,0)||1;
    const rr=(item.revenue||0)/sR, dr=(item.deposit||0)/sD, cr=(item.customers||0)/sC;
    out[dv].forEach(s=>{
      s.revenue=Math.round(s.revenue*rr); s.operating=s.revenue; s.gross=Math.round(s.gross*rr); s.crosssell_rev=Math.round(s.crosssell_rev*rr);
      s.deposit=Math.round(s.deposit*dr); s.cash_in=s.revenue+s.deposit;
      s.customers=Math.round(s.customers*cr); s.paying=Math.round(s.paying*cr); s.coc=Math.round(s.coc*cr); s.zero=Math.round(s.zero*cr);
      s.new=Math.round(s.new*cr); s.tk=Math.round(s.tk*cr); s.bills_total=Math.round(s.bills_total*cr); s.bills_multi=Math.round(s.bills_multi*cr);
      s.bill_values=(s.bill_values||[]).map(v=>Math.round(v*rr)); s.roas=s.spend?+(s.revenue/s.spend).toFixed(1):0;
    });
  });
  _SDIV=out; return out;
}
function activeSeries(){
  if(window.__page==='overview'&&DIVFILTER!=='all'){
    const sd=(DATA.series_div&&DATA.series_div[DIVFILTER])||seriesDivFallback()[DIVFILTER];
    if(sd&&sd.length) return sd;
  }
  return DATA.series;
}
function winSlice(key,f,t){
  const SS=activeSeries();
  const today=SS.find(s=>s.date===TODAY_DATE)||null;
  const comp=SS.filter(s=>s.date<TODAY_DATE), base=comp.length?comp:SS;
  if(key==='today')return today?[today]:[];
  if(key==='y')return base.length?[base[base.length-1]]:[];
  if(key==='mtd')return base.filter(s=>s.date.slice(0,7)===MO);
  if(key==='custom')return SS.filter(s=>s.date>=f && s.date<=t);
  const n={d3:3,d7:7,d15:15,d30:30}[key]||7; return n>=base.length?base.slice():base.slice(-n);
}
function mergeDict(arr,field){const o={};arr.forEach(s=>{const d=s[field]||{};for(const k in d)o[k]=(o[k]||0)+d[k];});return o;}
function poolVals(arr){let v=[];arr.forEach(s=>v=v.concat(s.bill_values||[]));return v;}
function median(a){if(!a.length)return 0;const b=[...a].sort((x,y)=>x-y),m=b.length>>1;return b.length%2?b[m]:(b[m-1]+b[m])/2;}
function mean(a){return a.length?a.reduce((s,x)=>s+x,0)/a.length:0;}

function vnd(n){ // smart Vietnamese money
  if(n>=1e9) return (n/1e9).toFixed(2).replace('.',',')+' <span class="u">tỷ</span>';
  if(n>=1e6) return Math.round(n/1e6).toLocaleString('vi-VN')+' <span class="u">tr</span>';
  return Math.round(n/1e3).toLocaleString('vi-VN')+' <span class="u">k</span>';
}
function tr(n){return Math.round(n/1e6).toLocaleString('vi-VN')+' tr';}
function tr1(n){return (n/1e6).toFixed(1).replace('.',',')+' tr';}
let PIEC=[];
function buildPieStatic(rows,total,label){
  PIEC=rows.map(s=>({group:s.group,val:s.val,pct:(s.val/total*100).toFixed(1)}));
  const cx=150,cy=150,r=132,ri=78; let a=-Math.PI/2,slices='';
  rows.forEach((s,i)=>{const a1=a+(s.val/total)*Math.PI*2;
    slices+=`<path class="slice" d="${arcPath(cx,cy,r,ri,a,a1-0.004)}" fill="${PIECOL[i%PIECOL.length]}" onmousemove="showPieTipC(event,${i})" onmouseleave="hideTip()" onclick="showPieTipC(event,${i})"></path>`; a=a1;});
  return `<svg viewBox="0 0 300 300">${slices}
    <text x="150" y="143" text-anchor="middle" style="font-family:'Inter',sans-serif;font-size:25px;font-weight:600;fill:var(--ink)">${tyS(total)}</text>
    <text x="150" y="166" text-anchor="middle" style="font-size:10px;fill:var(--ink-soft);letter-spacing:.04em">${label}</text></svg>`;
}
function showPieTipC(e,i){
  const s=PIEC[i]; if(!s)return; const t=document.getElementById('tip');
  t.innerHTML=`<div class="tt-d">${s.group}</div>
    <div class="tt-r hl"><span>Cọc</span><b>${tr(s.val)}</b></div>
    <div class="tt-r"><span>Tỉ trọng</span><b>${s.pct}%</b></div>`;
  t.style.display='block';
  t.style.left=Math.min(e.clientX+16,window.innerWidth-210)+'px';
  t.style.top=Math.min(e.clientY+16,window.innerHeight-200)+'px';
}
function cvtag(cv){if(cv==null)return '<span style="color:var(--muted)">—</span>';const k=cv>=110?'cb':cv>=60?'cm':'cg';const l=cv>=110?'Dao động':cv>=60?'Khá đều':'Ổn định';return `<span class="cvtag ${k}">${l} · ${cv}%</span>`;}
function vitag(v){if(v==null)return '<span style="color:var(--muted)">—</span>';return `<span class="cvtag ${v>=1.1?'cg':v<0.9?'cb':'cm'}">${v.toFixed(2)}</span>`;}
function viText(v){return v==null?'—':(v>=1.1?'Khai thác tốt hơn mặt bằng':v<0.9?'Dưới kỳ vọng · nên coaching':'Bình thường');}
function xsScore(a){return (a.xsell||0)*Math.sqrt(a.attach||0);}  // điểm bán chéo = số bill × √(attach%)
function miniLB(title,sub,items,targetId){
  const md=i=>i===0?'g':i===1?'s':i===2?'b':'';
  return `<div class="lb" onclick="document.getElementById('${targetId}').scrollIntoView({behavior:'smooth',block:'start'})">
    <div class="lb-h"><div class="lb-t">${title}</div><div class="lb-x">Xem chi tiết ↓</div></div>
    <div class="lb-sub">${sub}</div>
    ${items.map((it,i)=>`<div class="lbrow"><span class="lbrank ${md(i)}">${i+1}</span><span class="lbnm">${it.name}</span><span class="lbval">${it.disp}</span></div>`).join('')||'<div class="lb-sub">Chưa có dữ liệu</div>'}
  </div>`;
}
function k(n){return Math.round(n/1e3).toLocaleString('vi-VN')+'k';}
const dlabel=d=>{const[_,m,day]=d.split('-');return day+'/'+m;};
const DIVMAP_JS={'Tiêm':'Nội khoa','Máy':'Nội khoa','Căng chỉ':'Nội khoa','Mông':'Nội khoa','Mũi':'Ngoại khoa','Ngực':'Ngoại khoa','Mí/Mắt':'Ngoại khoa','Hút mỡ':'Ngoại khoa'};
let DIVFILTER='all';
const DIVPAGES=['overview','service','sales','master','cross','platform'];
function inDiv(d){return DIVFILTER==='all'||d===DIVFILTER;}
function dvchipG(g){const d=DIVMAP_JS[g];if(!d)return '';const ng=d.includes('Ngoại');return `<span class="dvtag ${ng?'ngoai':'noi'}">${ng?'Ngoại':'Nội'}</span>`;}
function setDiv(d){DIVFILTER=d;show(window.__page||'overview');}
function divEmpty(){return `<div class="card"><h2>${DIVFILTER} — chưa đủ dữ liệu trong kỳ</h2><div class="note" style="margin-top:8px">Division này mới triển khai hoặc phần lớn doanh thu còn ở cọc (chưa ghép cọc→thực hiện). Số sẽ đầy đủ sau file cập nhật có cột BILL CỌC.</div></div>`;}
const titles={overview:['Tổng quan vận hành','Bức tranh một màn hình cho buổi sáng'],
  division:['Nội khoa vs Ngoại khoa','Hai cỗ máy doanh thu — tiến độ so với target tháng'],
  service:['Hiệu suất dịch vụ','Dịch vụ nào đáng để rót ngân sách'],
  platform:['Meta vs TikTok','So sánh hiệu quả hai nền tảng'],
  sales:['Hiệu suất Sale','Doanh thu & chất lượng theo nhân viên'],
  master:['Hiệu suất Master','Năng lực khai thác giá trị khách tại clinic'],
  cross:['Bán chéo','Khách mua thêm dịch vụ thứ hai'],
  memo:['Bản tin CEO hằng ngày','Số liệu nói gì & nên làm gì hôm nay']};

/* ---------- OVERVIEW ---------- */
const agg=(arr,f)=>arr.reduce((s,x)=>s+f(x),0);
function metric(arr,key){
  const op=agg(arr,s=>s.operating),sp=agg(arr,s=>s.spend),pay=agg(arr,s=>s.paying),coc=agg(arr,s=>s.coc);
  if(key==='rev')return op; if(key==='spend')return sp;
  if(key==='roas')return sp?op/sp:0; if(key==='paying')return pay;
  if(key==='cac')return (pay+coc)?sp/(pay+coc):0; if(key==='adds')return op?sp/op*100:0;
}
const tyS=v=>v>=1e9?(v/1e9).toFixed(2).replace('.',',')+' tỷ':Math.round(v/1e6).toLocaleString('vi-VN')+' tr';
const trd=n=>(n/1e6).toFixed(1).replace('.',',')+' tr';
const fmtM={rev:tyS,spend:tyS,roas:v=>v.toFixed(1)+'x',paying:v=>Math.round(v),
  cac:v=>trd(v),adds:v=>v.toFixed(1)+'%'};
const addUnit={rev:1,spend:1,paying:1};
const CARDS=[
 {k:'rev',vi:'Doanh thu',en:'Bill khách · không gồm cọc',g:1},
 {k:'spend',vi:'Chi phí quảng cáo',en:'Meta + TikTok',g:0},
 {k:'roas',vi:'ROAS',en:'Doanh thu ÷ chi ad',g:1},
 {k:'paying',vi:'Khách có doanh thu',en:'Khách trả tiền · chưa gồm cọc',g:1},
 {k:'cac',vi:'Chi phí ad / khách',en:'Chi ad ÷ (khách DT+cọc)',g:-1},
 {k:'adds',vi:'Chi phí ad / DS',en:'Chi ad ÷ doanh thu',g:-1},
];

// ----- % thay đổi so kỳ liền trước (xanh tốt / đỏ xấu theo hướng g) -----
const SUMKEYS=new Set(['rev','spend','paying']);  // chỉ số dạng tổng -> chuẩn hoá theo ngày khi so kỳ
function _chgChip(cur,prev,g){
  if(prev===0||!isFinite(cur)||!isFinite(prev))return '';
  const p=(cur-prev)/Math.abs(prev)*100; if(!isFinite(p))return '';
  if(Math.abs(p)<0.5)return '<span class="chg chg-neu">→0%</span>';
  const up=p>0, arrow=up?'▲':'▼';
  const good = g>0?up : g<0?!up : null;          // g=0: trung tính
  const cls = good===null?'chg-neu':(good?'chg-up':'chg-down');
  return `<span class="chg ${cls}">${arrow}${Math.abs(p).toFixed(0)}%</span>`;
}
function chg(curA,prevA,key,g){
  if(!curA.length||!prevA.length)return '<span class="chg chg-neu">—</span>';
  let cur=metric(curA,key),prev=metric(prevA,key);
  if(SUMKEYS.has(key)){cur/=curA.length;prev/=prevA.length;}
  return _chgChip(cur,prev,g)||'<span class="chg chg-neu">—</span>';
}
function chgF(curA,prevA,fn,g,isSum){
  if(!curA.length||!prevA.length)return '<span class="chg chg-neu">—</span>';
  let cur=fn(curA),prev=fn(prevA);
  if(isSum){cur/=curA.length;prev/=prevA.length;}
  return _chgChip(cur,prev,g)||'<span class="chg chg-neu">—</span>';
}

const fullDate=d=>{const[y,m,dd]=d.split('-');return dd+'/'+m+'/'+y;};

// ---- interactive chart (global so range buttons can re-render) ----
let VIEW=winSlice('mtd');
function buildChartSVG(arr){
  if(!arr||!arr.length)return '<div style="padding:40px;text-align:center;color:var(--ink-soft)">Chưa có dữ liệu cho khung thời gian này.</div>';
  const W=940,H=360,L=48,Rg=54,T=30,B=58, pw=W-L-Rg, ph=H-T-B;
  const maxRev=Math.max(...arr.map(s=>s.gross))*1.06;
  const maxMed=Math.max(...arr.map(s=>s.median_bill))*1.18;
  const gw=pw/arr.length;
  let bars='',hits='',pts=[],med='',grid='';
  for(let g=0;g<=4;g++){const v=maxRev*g/4,y=T+ph-(v/maxRev*ph);
    grid+=`<line x1=${L} y1=${y} x2=${L+pw} y2=${y} stroke="var(--tint)" stroke-width="1"/>`;
    grid+=`<text x=${L-8} y=${y+3} text-anchor="end" class="ax">${(v/1e6).toFixed(0)}</text>`;}
  for(let g=0;g<=3;g++){const v=maxMed*g/3,y=T+ph-(v/maxMed*ph);
    grid+=`<text x=${L+pw+8} y=${y+3} class="ax" fill="var(--rose)">${(v/1e6).toFixed(0)}</text>`;}
  arr.forEach((s,i)=>{
    const cx=L+(i+0.5)*gw;
    const opH=s.operating/maxRev*ph,cocH=s.deposit/maxRev*ph,spH=s.spend/maxRev*ph;
    const bw=Math.min(26,gw*0.42), rx=cx-bw-1, sx=cx+3, sw=Math.min(16,gw*0.26);
    const opY=T+ph-opH, cocY=opY-cocH;
    bars+=`<rect x=${rx} y=${opY} width=${bw} height=${opH} rx=4 fill="url(#gj)"></rect>`;
    if(cocH>1.5)bars+=`<rect x=${rx} y=${cocY} width=${bw} height=${cocH} rx=3 fill="#A9CFC5"></rect>`;
    bars+=`<rect x=${sx} y=${T+ph-spH} width=${sw} height=${spH} rx=3 fill="url(#gg)"></rect>`;
    bars+=`<text x=${cx-bw/2} y=${cocY-8} class="roas">${s.roas}x</text>`;
    bars+=`<text x=${cx} y=${H-30} class="xl">${(s.gross/1e6).toFixed(0)}tr</text>`;
    bars+=`<text x=${cx} y=${H-14} class="xs">${dlabel(s.date)}</text>`;
    const my=T+ph-(s.median_bill/maxMed*ph); pts.push(`${cx},${my.toFixed(1)}`);
    med+=`<circle cx=${cx} cy=${my} r="3.6" fill="var(--rose)" stroke="#fff" stroke-width="1.4"></circle>`;
    hits+=`<rect class="hit" x=${L+i*gw} y=${T} width=${gw} height=${ph} fill="transparent" style="cursor:pointer" onmousemove="showTip(event,${i})" onmouseleave="hideTip()" onclick="showTip(event,${i})"></rect>`;
  });
  const poly=`<polyline points="${pts.join(' ')}" fill="none" stroke="var(--rose)" stroke-width="2.4" stroke-linejoin="round"></polyline>`;
  return `<svg class="combo" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">
    <defs><linearGradient id="gj" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--jade-2)"></stop><stop offset="1" stop-color="var(--jade)"></stop></linearGradient>
    <linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9B36A"></stop><stop offset="1" stop-color="var(--gold)"></stop></linearGradient></defs>
    <text x=${L-8} y=${T-12} text-anchor="end" class="ax">tr</text>
    <text x=${L+pw+8} y=${T-12} class="ax" fill="var(--rose)">tr</text>
    ${grid}${bars}${poly}${med}${hits}</svg>`;
}
function renderChart(){const b=document.getElementById('chartBox');if(b)b.innerHTML=buildChartSVG(VIEW);}
function selectRange(key,btn){
  VIEW=winSlice(key);
  document.querySelectorAll('#chartRanges button').forEach(x=>x.classList.remove('on'));
  if(btn)btn.classList.add('on');
  document.getElementById('customBox').style.display='none';
  renderChart(); hideTip();
}
function toggleCustom(btn){
  document.querySelectorAll('#chartRanges button').forEach(x=>x.classList.remove('on'));
  if(btn)btn.classList.add('on');
  const c=document.getElementById('customBox'); c.style.display=c.style.display==='none'?'flex':'none';
}
function applyCustom(){
  const f=document.getElementById('cFrom').value, t=document.getElementById('cTo').value;
  VIEW=winSlice('custom',f,t); if(!VIEW.length)VIEW=winSlice('mtd');
  renderChart(); hideTip();
}
function showTip(e,i){
  const s=VIEW[i]; if(!s)return; const t=document.getElementById('tip');
  const msg=s.meta_msg+s.tk_msg;
  t.innerHTML=`<div class="tt-d">${fullDate(s.date)}</div>
    <div class="tt-r hl"><span>Doanh thu thuần</span><b>${tr(s.operating)}</b></div>
    <div class="tt-r"><span>Doanh thu cọc</span><b>${tr(s.deposit)}</b></div>
    <div class="tt-r"><span>Tổng (gồm cọc)</span><b>${tr(s.gross)}</b></div>
    <div class="tt-r"><span>Chi quảng cáo</span><b>${tr(s.spend)}</b></div>
    <div class="tt-r"><span>ROAS</span><b>${s.roas}x</b></div>
    <div class="tt-r"><span>Bill trung vị</span><b>${tr(s.median_bill)}</b></div>
    <div class="tt-r"><span>Khách có DT</span><b>${s.paying}</b></div>
    <div class="tt-r"><span>Tin nhắn</span><b>${msg}</b></div>`;
  t.style.display='block';
  t.style.left=Math.min(e.clientX+16, window.innerWidth-210)+'px';
  t.style.top=Math.min(e.clientY+16, window.innerHeight-260)+'px';
}
function hideTip(){const t=document.getElementById('tip');if(t)t.style.display='none';}
function toggleTheme(){const dark=document.documentElement.getAttribute('data-theme')==='dark';const t=dark?'light':'dark';if(t==='dark')document.documentElement.setAttribute('data-theme','dark');else document.documentElement.removeAttribute('data-theme');try{localStorage.setItem('swan-theme',t)}catch(e){}}
function sparkTip(e,el){const t=document.getElementById('tip');if(!t)return;const raw=el.getAttribute('data-tip')||'';if(!raw){hideTip();return;}const parts=raw.replace('Xu hướng ','').split(' · ');t.innerHTML=`<div class="tt-d" style="font-size:13.5px;margin-bottom:6px">Xu hướng theo ngày</div><div class="tt-r"><span>Khoảng</span><b>${parts[0]||''}</b></div><div class="tt-r"><span>Dữ liệu</span><b>${parts[1]||''}</b></div>`;t.style.display='block';t.style.left=Math.min(e.clientX+16, window.innerWidth-210)+'px';t.style.top=Math.min(e.clientY+16, window.innerHeight-110)+'px';}
function heat(v,mn,mx){if(v==null||!isFinite(v)||mx<=mn)return '';const t=Math.max(0,Math.min(1,(v-mn)/(mx-mn)));return ` style="background:rgba(18,149,90,${(t*0.20).toFixed(3)})"`;}
function heatR(v,mn,mx){if(v==null||!isFinite(v)||mx<=mn)return '';const t=Math.max(0,Math.min(1,(mx-v)/(mx-mn)));return ` style="background:rgba(18,149,90,${(t*0.20).toFixed(3)})"`;}
function spark(vals,cls,g,title){
  vals=(vals||[]).filter(v=>v!=null&&isFinite(v));
  if(vals.length<3) return '<span class="sparkna">—</span>';
  const n=vals.length,mn=Math.min(...vals),mx=Math.max(...vals),rng=(mx-mn)||1,W=200,H=30,p=3,iw=W-2*p,ih=H-2*p;
  const P=vals.map((v,i)=>[p+(i/(n-1))*iw, p+ih-((v-mn)/rng)*ih]);
  const line=P.map((q,i)=>(i?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1)).join(' ');
  const area='M'+P[0][0].toFixed(1)+' '+(H-p)+' '+P.map(q=>'L'+q[0].toFixed(1)+' '+q[1].toFixed(1)).join(' ')+' L'+P[n-1][0].toFixed(1)+' '+(H-p)+' Z';
  let mod='spk-neu';
  if(g){const h=Math.max(2,Math.floor(n/3));const a=vals.slice(0,h).reduce((x,y)=>x+y,0)/h;const b=vals.slice(-h).reduce((x,y)=>x+y,0)/h;const ch=(b-a)/(Math.abs(a)||1);const tr=ch>0.04?1:ch<-0.04?-1:0;if(tr)mod=(tr*g>0)?'spk-pos':'spk-neg';}
  const tip=(title||'').replace(/"/g,'&quot;');
  return `<svg class="spark ${cls||''} ${mod}" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" data-tip="${tip}" onmousemove="sparkTip(event,this)" onmouseleave="hideTip()" onclick="sparkTip(event,this)"><rect x="0" y="0" width="${W}" height="${H}" fill="#000" fill-opacity="0" style="pointer-events:all"/><path d="${area}" class="sparkfill"/><path d="${line}" class="sparkline" vector-effect="non-scaling-stroke"/></svg>`;
}
document.addEventListener('click',e=>{if(!e.target.closest('.hit,.slice,.spark,#tip'))hideTip();},true);

let GVIEW=winSlice('mtd');
function gatesDivNote(){
  if(DIVFILTER==='all') return '';
  const isng=DIVFILTER==='Ngoại khoa';
  return `<div class="note" style="margin-bottom:12px">Đang lọc <b>${DIVFILTER}</b> — phễu tính trên ${isng?'2 account Meta ngoại khoa (Swan3, Swan4)':'2 account Meta nội khoa (Swan2, Swan5) + TikTok'}; chi phí ad tách theo tag dịch vụ ở tên ad.</div>`;
}
// gatesNgoai (placeholder ad-chưa-nạp) đã bỏ — ngoại khoa giờ có account ad + series riêng, dùng gatesInner.
function divProgress(){
  const D=DATA.divisions; if(!D||!D.items||!D.items.length) return '';
  const items=D.items;
  let seg, ng=false;
  if(DIVFILTER==='all'){
    const rev=items.reduce((a,d)=>a+d.revenue,0), tgt=items.reduce((a,d)=>a+d.target_month,0);
    const proj=D.days_elapsed?rev/D.days_elapsed*D.month_days:0;
    seg={name:'Toàn clinic',revenue:rev,target_month:tgt,pct_target:tgt?+(rev/tgt*100).toFixed(1):0,projected_month:Math.round(proj),pct_projected:tgt?+(proj/tgt*100).toFixed(1):0};
  } else {
    seg=items.find(d=>d.name===DIVFILTER)||items[0]; ng=seg.name.includes('Ngoại');
  }
  const pj=seg.pct_projected, pill=pj>=100?'ok':pj>=80?'behind':'bad', pjlab=pj>=100?'Đúng/vượt nhịp':pj>=80?'Hơi chậm nhịp':'Chậm nhịp';
  return `<div class="card" style="padding:18px 22px">
    <div class="dshead"><h2 style="font-size:17px;margin:0">Tiến độ target tháng${DIVFILTER==='all'?'':' · '+seg.name}</h2><span class="dslink" onclick="show('division')">So sánh 2 mảng →</span></div>
    <div class="dsr-h"><span class="dslab ${ng?'g':'n'}">${seg.name}</span>
      <span class="dsval">${seg.pct_target}% <span style="color:var(--muted);font-weight:500">· ${tyS(seg.revenue)}/${tyS(seg.target_month)} · đã qua ${D.days_elapsed}/${D.month_days} ngày</span></span></div>
    <div class="dstrack"><div class="dsfill ${ng?'g':'n'}" style="width:${Math.min(100,seg.pct_target)}%"></div></div>
    <div class="dv-proj" style="margin-top:11px"><span class="dv-pill ${pill}">${pjlab}</span><span>Dự phóng cuối tháng: <b style="color:var(--ink)">${tyS(seg.projected_month)}</b> (${seg.pct_projected}% target)</span></div>
  </div>`;
}
const FICON={
 ad:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>',
 msg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
 lead:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/></svg>',
 bk:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
 exam:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
 cust:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
 rev:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'
};
function gatesInner(arr){
  const isng=DIVFILTER==='Ngoại khoa';
  const spend=agg(arr,s=>s.spend),meta=agg(arr,s=>s.meta_spend),tk=agg(arr,s=>s.tk_spend);
  const metamsg=agg(arr,s=>s.meta_msg),tkmsg=agg(arr,s=>s.tk_msg),msg=metamsg+tkmsg;
  const msgnew=agg(arr,s=>s.msg_new||0),msgconv=agg(arr,s=>s.msg_conv||0);
  const _BK=(typeof DATA!=='undefined'&&DATA.bkphau)?DATA.bkphau:null;
  const booking=agg(arr,s=>s.booking||0),arrived=agg(arr,s=>s.den||0);
  const noshow=agg(arr,s=>s.noshow||0),rot=agg(arr,s=>s.rot||0),cocxa=agg(arr,s=>s.cocxa||0),doi=agg(arr,s=>s.doi||0);
  const due=arrived+noshow, pending=Math.max(0,booking-arrived-noshow-doi);
  const bnew=agg(arr,s=>s.booking_new||0),btk=agg(arr,s=>s.booking_tk||0),bmulti=agg(arr,s=>s.booking_multi||0);
  const ltbook=arr.length?(arr.reduce((x,s)=>x+(s.book_lead||0),0)/arr.length):0;
  const paying=agg(arr,s=>s.paying),coc=agg(arr,s=>s.coc),zero=agg(arr,s=>s.zero),cust=agg(arr,s=>s.customers);
  const chot=paying+coc;
  const cnew=agg(arr,s=>s.new||0),dennew=agg(arr,s=>s.den_new||0);
  const cocnew=agg(arr,s=>s.coc_new||0);
  const rotNew=Math.max(0,dennew-cnew-cocnew), chiTK=Math.max(0,arrived-paying-coc-rotNew);
  const rev=agg(arr,s=>s.operating),dep=agg(arr,s=>s.deposit),xrev=agg(arr,s=>s.crosssell_rev||0);
  const bt=agg(arr,s=>s.bills_total||0),bm=agg(arr,s=>s.bills_multi||0),attach=bt?bm/bt*100:0;
  const vals=poolVals(arr),med=median(vals),mn=mean(vals);
  const revnew=agg(arr,s=>s.rev_new||0),revtk=agg(arr,s=>s.rev_tk||0);
  const lead=(isng&&_BK)?(_BK.n_nuoi||0):agg(arr,s=>s.lead_nuoi||0),leadval=(isng&&_BK)?(_BK.pipeline_value||0):agg(arr,s=>s.lead_value||0),leadrisk=(isng&&_BK)?(_BK.n_at_risk||0):agg(arr,s=>s.lead_risk||0);
  const ldays=(isng&&_BK)?(_BK.days_pending_avg||0):(arr.length?(arr.reduce((x,s)=>x+(s.lead_days||0),0)/arr.length):0);
  const bkTotal=(isng&&_BK)?(_BK.total_leads||0):0, nkham=(isng&&_BK)?(_BK.n_kham||0):0, ncoc=(isng&&_BK)?(_BK.n_coc||0):0, nphau=(isng&&_BK)?(_BK.n_phau||0):0, ntvr=(isng&&_BK)?(_BK.n_tuvanrot||0):0;
  const cocReached=ncoc+nphau, chuaKham=Math.max(0,bkTotal-nkham);
  const ndays=arr.length||1, adDays=arr.filter(s=>(s.spend||0)>0).length;
  const pct=(n,d)=>d?(n/d*100):0;
  const MS=(typeof activeSeries==='function'&&typeof TODAY_DATE!=='undefined'&&TODAY_DATE)?activeSeries().filter(s=>s.date.slice(0,7)===TODAY_DATE.slice(0,7)):arr;
  const monthSpend=agg(MS,s=>s.spend);
  const adsvcStr=Object.entries(mergeDict(arr,'spend_by_service')).sort((a,b)=>b[1]-a[1]).map(([g,v])=>`${g} ${tyS(v)}`).join(' · ')||'—';
  const msStr=Object.entries(mergeDict(arr,'msg_by_service')).sort((a,b)=>b[1]-a[1]).map(([g,v])=>`${g} ${v}`).join(' · ')||'—';
  const svc=Object.entries(mergeDict(arr,'rev_by_service')).sort((a,b)=>b[1]-a[1]).map(([g,v])=>`${g} ${tyS(v)}`).join(' · ')||'—';
  const bsStr=Object.entries(mergeDict(arr,'booking_src')).sort((a,b)=>b[1]-a[1]).map(([g,v])=>`${g} ${v}`).join(' · ')||'—';
  const leadsvcStr=((isng&&_BK&&_BK.by_service)?Object.entries(_BK.by_service):Object.entries(mergeDict(arr,'lead_by_service'))).sort((a,b)=>b[1]-a[1]).map(([g,v])=>`${g} ${v}`).join(' · ')||'—';
  const row=(l,v,c)=>`<div class="fm${c?' coc':''}"><span class="fl">${l}</span><span class="fv">${v}</span></div>`;
  const sub2=(t)=>`<div class="fsub2">${t}</div>`;
  const cardHTML=(c)=>`<div class="fcard${c.cls||''}"><div class="fch"><span class="ficon">${FICON[c.ic]}</span><div class="ft"><div class="fnm">${c.name}</div><div class="fsub">${c.sub}</div></div></div><div class="fbig">${c.big}${c.unit?`<small>${c.unit}</small>`:''}</div><div class="frows">${c.rows||''}</div>${c.by?`<div class="fby">${c.by}</div>`:''}${c.wait?`<div class="fwait">${c.wait}</div>`:''}</div>`;
  const QC={ic:'ad',name:'Quảng cáo',sub:'Tổng chi Meta + TikTok',big:tyS(spend),
    rows:row('Meta',`${tyS(meta)} (${pct(meta,spend).toFixed(0)}%)`)+row('TikTok',`${tyS(tk)} (${pct(tk,spend).toFixed(0)}%)`)+row('Chi ad / ngày',trd(spend/ndays))+row('Tổng chi tháng',tyS(monthSpend)),
    by:`Chi ad theo DV: <b>${adsvcStr}</b>`};
  const TN={ic:'msg',name:'Tin nhắn',sub:'Tin nhắn Meta + TikTok',big:msg.toLocaleString('vi-VN'),unit:'tin',
    rows:row('Meta (CPL)',`${metamsg} · ${metamsg?k(meta/metamsg):'—'}`)+row('TikTok (CPL)',`${tkmsg} · ${tkmsg?k(tk/tkmsg):'—'}`)+(msgnew?row('Tin nhắn mới',msgnew.toLocaleString('vi-VN')):'')+(msgconv?row('Tổng hội thoại',msgconv.toLocaleString('vi-VN')):''),
    by:`Tin nhắn theo DV: <b>${msStr}</b>`};
  const KHACH={ic:'cust',name:'Khách',cls:' key',sub:'Khách đến phòng khám',big:arrived.toLocaleString('vi-VN'),unit:'khách',
    rows:(isng?row('Khách có DT',paying)+row('Khách chỉ TK',zero)+row('Đến không làm',rot)+row('Chi ad / khách đến',arrived?trd(spend/arrived):'—')+row('Chi ad / khách có DT + cọc',chot?trd(spend/chot):'—'):row('Có DT',paying)+row('Chỉ TK',chiTK)+row('Khách rớt (mới)',rotNew)+row('Chi ad / khách đến',arrived?trd(spend/arrived):'—')+row('Chi ad / khách có DT',paying?trd(spend/paying):'—'))+sub2('Chờ thực hiện · cọc')+row('Đã cọc',`${coc} khách · ${tr(dep)}`,1)};
  const DT={ic:'rev',name:'Doanh thu',sub:'Doanh thu đã làm',big:tyS(rev),
    rows:row('ROAS · Chi/DS',`${spend?(rev/spend).toFixed(1):'—'}x · ${rev?pct(spend,rev).toFixed(1):'—'}%`)+row('AOV · trung vị',`${tr(mn)} · ${tr(med)}`)+row('Bán chéo · DT bill bán chéo',`${attach.toFixed(1)}% · ${tr(xrev)}`)+row('DT New / Tái khám',`${tr(revnew)} / ${tr(revtk)}`),
    by:`DT theo DV: <b>${svc}</b>`};
  let cards=[],chips=[];
  cards.push(QC,TN);
  chips.push({v:`${msg?k(spend/msg):'—'}`,l:'CPL / tin nhắn',f:'= chi ad ÷ tin nhắn',tip:`chi ad ${tyS(spend)} ÷ ${msg.toLocaleString('vi-VN')} tin nhắn = ${msg?k(spend/msg):'—'}`});
  if(!isng){
    const LICH={ic:'bk',name:'Lịch hẹn',cls:' key',sub:'Lịch từ mọi nguồn',big:booking.toLocaleString('vi-VN'),unit:'lịch',
      rows:((bnew||btk)?row('Mới / Tái khám',`${bnew} / ${btk}`):'')+row('Dời lịch',doi)+(pending?row('Chưa tới hạn',pending):'')+(cocxa?row('Cọc xa (online)',cocxa):'')+(bmulti?row('Khách đi kèm (>1)',bmulti):'')+(ltbook?row('Lead time đặt→hẹn',`${ltbook.toFixed(1)} ngày`):'')+row('Chi ad / lịch hẹn',booking?trd(spend/booking):'—'),
      by:`Booking theo nguồn: <b>${bsStr}</b>`};
    cards.push(LICH,KHACH,DT);
    chips.push({v:`${pct(booking,msg).toFixed(1)}%`,l:'tin nhắn → lịch hẹn',f:'= lịch hẹn ÷ tin nhắn',tip:`${booking} lịch hẹn ÷ ${msg.toLocaleString('vi-VN')} tin nhắn = ${pct(booking,msg).toFixed(1)}%`});
    chips.push({v:`${pct(arrived,due).toFixed(0)}%`,l:'lịch hẹn → đến khám',f:'= đến khám ÷ lịch đã tới hạn',tip:`đến khám ${arrived} ÷ đã tới hạn ${due} = ${pct(arrived,due).toFixed(1)}%<br>đã tới hạn ${due} = lịch hẹn ${booking} − dời ${doi} − chưa tới hạn ${pending}<br>no-show ${noshow} (${pct(noshow,due).toFixed(1)}%)`,drop:'ns',dropt:`−${noshow} no-show (${pct(noshow,due).toFixed(1)}%)`});
    chips.push({v:`${pct(cnew,dennew).toFixed(0)}%`,l:'đến khám → chốt (khách mới)',f:'= chốt mới ÷ đến khám mới',tip:`chốt mới ${cnew} ÷ đến khám mới ${dennew} = ${pct(cnew,dennew).toFixed(1)}%<br>đến khám mới ${dennew} = chốt ${cnew} + rớt ${rotNew} + cọc ${cocnew}`,drop:'rot',dropt:`đến khám mới ${dennew}/${arrived} · ${rotNew} rớt · ${cocnew} cọc`});
  } else {
    const LEAD={ic:'lead',name:'Lead',cls:' lead',sub:'Đang quản lý · nhu cầu thật',big:bkTotal?bkTotal.toLocaleString('vi-VN'):'\u2014',unit:'lead',
      rows:row('Giá kỳ vọng (pipeline)',leadval?tyS(leadval):'\u2014')+row('Lead nguy cơ (treo lâu)',leadrisk||'\u2014')+row('Ngày treo TB',ldays?`${ldays.toFixed(0)} ngày`:'\u2014')+row('Chưa chốt lịch khám',chuaKham),
      by:`Lead theo DV: <b>${leadsvcStr}</b>`};
    const KHAM={ic:'exam',name:'Khám',cls:' key',sub:'Đã đến khám · có master',big:nkham?nkham.toLocaleString('vi-VN'):'\u2014',unit:'khách',
      rows:row('Tư vấn rớt (chăm lại)',ntvr)+row('Tỉ lệ lead \u2192 khám',bkTotal?pct(nkham,bkTotal).toFixed(0)+'%':'\u2014')};
    const COC={ic:'cust',name:'Cọc',cls:' key',sub:'Đã chốt cọc',big:cocReached?cocReached.toLocaleString('vi-VN'):'\u2014',unit:'khách',
      rows:row('Đang chờ mổ',ncoc)+row('Đã lên bàn mổ',nphau)};
    const PHAU={ic:'rev',name:'Phẫu · DT',sub:'Đã mổ · doanh thu',big:nphau?nphau.toLocaleString('vi-VN'):'\u2014',unit:'ca',
      rows:row('Doanh thu đã làm',tyS(rev))+row('ROAS · Chi/DS',`${spend?(rev/spend).toFixed(1):'\u2014'}x · ${rev?pct(spend,rev).toFixed(1):'\u2014'}%`)+row('AOV · trung vị',`${tr(mn)} · ${tr(med)}`),
      by:`DT theo DV: <b>${svc}</b>`};
    cards.push(LEAD,KHAM,COC,PHAU);
    chips.push({v:`${msg?pct(bkTotal,msg).toFixed(1)+'%':'\u2014'}`,l:'tin nhắn \u2192 lead',f:'= lead ÷ tin nhắn (snapshot)',tip:`lead ${bkTotal} ÷ ${msg.toLocaleString('vi-VN')} tin nhắn = ${msg?pct(bkTotal,msg).toFixed(1):'—'}%<br>lead là snapshot (không theo khung thời gian)`});
    chips.push({v:`${bkTotal?pct(nkham,bkTotal).toFixed(0)+'%':'\u2014'}`,l:'lead \u2192 khám',f:'= khám ÷ lead',tip:`khám ${nkham} ÷ lead ${bkTotal} = ${bkTotal?pct(nkham,bkTotal).toFixed(1):'—'}%<br>chưa chốt lịch khám ${chuaKham}`,drop:'ns',dropt:`\u2212${chuaKham} chưa chốt lịch khám`});
    chips.push({v:`${nkham?pct(cocReached,nkham).toFixed(0)+'%':'\u2014'}`,l:'khám \u2192 cọc',f:'= cọc ÷ khám',tip:`cọc ${cocReached} ÷ khám ${nkham} = ${nkham?pct(cocReached,nkham).toFixed(1):'—'}%<br>tư vấn rớt ${ntvr}`,drop:'rot',dropt:`\u2212${ntvr} tư vấn rớt`});
    chips.push({v:`${cocReached?pct(nphau,cocReached).toFixed(0)+'%':'\u2014'}`,l:'cọc \u2192 phẫu',f:'= phẫu ÷ cọc',tip:`phẫu ${nphau} ÷ cọc ${cocReached} = ${cocReached?pct(nphau,cocReached).toFixed(1):'—'}%`});
  }
  const N=cards.length, COL=['var(--gold)','var(--jade)','var(--rose)'];
  let H=`<div class="fnl" style="grid-template-columns:repeat(${N},minmax(0,1fr))">`;
  H+=`<div class="fline" style="grid-column:1/-1;grid-row:2"><span class="fdot"></span><span class="fbar"></span><span class="fhd"></span></div>`;
  cards.forEach((c,i)=>{
    H+=cardHTML(c).replace('<div class="fcard',`<div style="grid-column:${i+1};grid-row:1" class="fcard`);
    if(i<N-1){
      const ch=chips[i],col=COL[i%3];
      H+=`<div class="fchip" style="grid-column:${i+1}/span 2;grid-row:2"><span class="carr" style="color:${col}">↑</span><div class="fpill"><span class="cnum" style="background:${col}">${i+1}</span><div class="cbox"><div class="cv">${ch.v}</div><div class="cl">${ch.l}</div></div>${ch.tip?`<span class="finfo" tabindex="0">i<span class="ftip">${ch.tip}</span></span>`:''}</div></div>`;
    }
  });
  H+='</div>';
  H+=`<div class="note" style="margin-top:18px"><b>Đọc nhanh:</b> ${isng?`Ngoại khoa (nguồn BK Phẫu): ${bkTotal} lead \u2192 ${nkham} đã khám (rơi ${chuaKham} chưa chốt lịch khám) \u2192 ${cocReached} cọc (rơi ${ntvr} tư vấn rớt) \u2192 ${nphau} phẫu.`:`${msg.toLocaleString('vi-VN')} tin nhắn → ${booking} lịch hẹn → ${arrived} đến khám (rơi ${noshow} no-show ${pct(noshow,due).toFixed(1)}%) → ${chot} khách chốt (rơi ${rotNew} khách mới rớt).`} ${isng?'Nguồn BK Phẫu (snapshot); ad & tin nhắn Meta/TikTok.':'Booking/no-show/rớt từ LLV; ad & tin nhắn Meta/TikTok.'}</div>`;
  return H;
}
function renderGates(){const b=document.getElementById('gateBox');if(!b)return;b.innerHTML=gatesDivNote()+gatesInner(GVIEW);}
function selectGateRange(key,btn){
  GVIEW=winSlice(key);
  document.querySelectorAll('#gateRanges button').forEach(x=>x.classList.remove('on'));
  if(btn)btn.classList.add('on');
  document.getElementById('gateCustom').style.display='none';
  renderGates();
}
function toggleGateCustom(btn){
  document.querySelectorAll('#gateRanges button').forEach(x=>x.classList.remove('on'));
  if(btn)btn.classList.add('on');
  const c=document.getElementById('gateCustom'); c.style.display=c.style.display==='none'?'flex':'none';
}
function applyGateCustom(){
  const f=document.getElementById('gFrom').value,t=document.getElementById('gTo').value;
  GVIEW=winSlice('custom',f,t); if(!GVIEW.length)GVIEW=winSlice('mtd'); renderGates();
}

function dqChips(){
  const q=DATA.dataquality||{}; const c=[];
  const w=t=>`<span class="dqchip warn">⚠ ${t}</span>`, ok=t=>`<span class="dqchip ok">✓ ${t}</span>`;
  if(q.bills_no_e1) c.push(w(q.bills_no_e1+' bill thiếu dòng E=1'));
  if(q.bills_multi_e1) c.push(w(q.bills_multi_e1+' bill có >1 dòng E=1'));
  if(q.mixed_bills) c.push(w(q.mixed_bills+' bill vừa có DT vừa có cọc'));
  c.push((q.rev_unmapped_pct>2?w:ok)('Map doanh thu→DV '+(100-(q.rev_unmapped_pct||0)).toFixed(0)+'%'));
  if((q.meta_unmapped_pct>2)||(q.tk_unmapped_pct>2)) c.push(w('Quảng cáo còn chưa map DV'));
  c.push(ok('Mới nhất: DT '+fmtDate(q.latest_revenue)+' · Meta '+fmtDate(q.latest_meta)+' · TikTok '+fmtDate(q.latest_tiktok)));
  return '<div class="dqbar">'+c.join('')+'</div>';
}
function newtkCard(){
  const nt=DATA.newtk; if(!nt)return '';
  const card=(name,o,accent)=>`<div class="nc">
    <h4>${name}<span style="font-weight:500;color:var(--ink-soft);font-size:12px"> · ${o.customers} khách</span></h4>
    <div class="r"><span>Doanh thu hoàn tất</span><b>${tyS(o.revenue)}</b></div>
    <div class="r"><span>AOV · trung vị</span><b>${tr(o.aov)} · ${tr(o.median)}</b></div>
    <div class="r"><span>Khách trả tiền / cọc / 0đ</span><b>${o.paying} · ${o.coc} · ${o.zero}</b></div>
    <div class="r"><span>Tỉ lệ bán chéo</span><b>${o.attach}%</b></div></div>`;
  return `<div class="card"><h2>New vs Tái khám (toàn kỳ)</h2><div class="h-en">Khách mới phản ánh acquisition · TK phản ánh retention</div>
    <div class="ntk">${card('New (khách mới)',nt.New)}${card('TK (tái khám)',nt.TK)}</div></div>`;
}
function overview(){
  const dd=dlabel(YDAY.date);
  const AS=activeSeries();
  const MTD=winSlice('mtd'), L7=winSlice('d7'), L30=winSlice('d30'), Y=winSlice('y'), L3=winSlice('d3');
  const COMP=AS.filter(s=>s.date<TODAY_DATE);                 // các ngày đã chốt
  const Yp = COMP.length>=2?[COMP[COMP.length-2]]:[];          // hôm trước hôm qua
  const L7p = COMP.slice(-14,-7);                              // 7 ngày liền trước
  const L3p = COMP.slice(-6,-3);                               // 3 ngày liền trước
  const L30p = COMP.slice(-60,-30);                            // 30 ngày liền trước
  const MONTH=AS.filter(s=>s.date.slice(0,7)===TODAY_DATE.slice(0,7));  // tháng đến hiện tại (gồm hôm nay)
  const _td=winSlice('today'); const TODAYV=_td.length?_td:null;
  const spk=AS.filter(s=>s.date<TODAY_DATE).slice(-30);
  const sd=d=>d.slice(8,10)+'/'+d.slice(5,7);
  const spkLbl=spk.length?`Xu hướng ${sd(spk[0].date)}–${sd(spk[spk.length-1].date)} · ${spk.length} ngày đã chốt`:'';
  const kpis=CARDS.map(c=>{
    const f=fmtM[c.k], suf=addUnit[c.k]?'<span class="per">/tháng</span>':'';
    return `<div class="kpi${c.accent?' accent':''}"><div class="lab">${c.vi}<span class="en">${c.en}</span></div>
      <div class="val">${f(metric(MONTH,c.k))}${suf}</div>
      ${spark(spk.map(d=>metric([d],c.k)),'kspark',c.g,spkLbl)}
      <div class="sub3">
        <span>Hôm nay: <b>${TODAYV?f(metric(TODAYV,c.k)):'—'}</b></span>
        <span>Hôm qua: <b>${f(metric(Y,c.k))}</b>${chg(Y,Yp,c.k,c.g)}</span>
        <span>3 ngày: <b>${f(metric(L3,c.k))}</b>${chg(L3,L3p,c.k,c.g)}</span>
        <span>7 ngày: <b>${f(metric(L7,c.k))}</b>${chg(L7,L7p,c.k,c.g)}</span>
        <span>30 ngày: <b>${f(metric(L30,c.k))}</b>${chg(L30,L30p,c.k,c.g)}</span>
      </div></div>`;}).join('');
  const dmin=S[0].date, dmax=S[S.length-1].date;
  const bm=MONTH, bt=TODAYV, by=winSlice('y'),b3=winSlice('d3'),b7=winSlice('d7'),b30=winSlice('d30');
  const mMsg=a=>agg(a,s=>s.meta_msg+s.tk_msg);
  const mConv=a=>{const m=mMsg(a);return m?(agg(a,s=>s.paying+s.coc)/m*100):0;};
  const mMed=a=>median(poolVals(a)), mMean=a=>mean(poolVals(a));
  const bcard=(vi,en,fn,fmt,g,isSum)=>`<div class="kpi"><div class="lab">${vi}<span class="en">${en}</span></div>
    <div class="val">${fmt(fn(bm))}<span class="per">/tháng</span></div>
    ${spark(spk.map(d=>fn([d])),'kspark',g,spkLbl)}
    <div class="sub3"><span>Hôm nay: <b>${bt?fmt(fn(bt)):'—'}</b></span><span>Hôm qua: <b>${fmt(fn(by))}</b>${chgF(by,Yp,fn,g,isSum)}</span><span>3 ngày: <b>${fmt(fn(b3))}</b>${chgF(b3,L3p,fn,g,isSum)}</span><span>7 ngày: <b>${fmt(fn(b7))}</b>${chgF(b7,L7p,fn,g,isSum)}</span><span>30 ngày: <b>${fmt(fn(b30))}</b>${chgF(b30,L30p,fn,g,isSum)}</span></div></div>`;
  return `
  ${insightCards('overview')}
  <div class="card" style="padding:20px 22px">
    <h2>Phễu vận hành</h2><div class="h-en">Quảng cáo → Tin nhắn → Lịch hẹn → Khách → Doanh thu · chọn khung thời gian</div>
    <div class="ranges" id="gateRanges">
      <button class="on" onclick="selectGateRange('mtd',this)">Tháng này</button>
      <button onclick="selectGateRange('today',this)">Hôm nay</button>
      <button onclick="selectGateRange('y',this)">Hôm qua</button>
      <button onclick="selectGateRange('d3',this)">3 ngày</button>
      <button onclick="selectGateRange('d7',this)">7 ngày</button>
      <button onclick="selectGateRange('d15',this)">15 ngày</button>
      <button onclick="selectGateRange('d30',this)">30 ngày</button>
      <button onclick="toggleGateCustom(this)">Tùy chỉnh</button>
    </div>
    <div class="custom" id="gateCustom" style="display:none">
      <input type="date" id="gFrom" min="${dmin}" max="${dmax}" value="${dmin}"><span>→</span>
      <input type="date" id="gTo" min="${dmin}" max="${dmax}" value="${dmax}">
      <button onclick="applyGateCustom()">Áp dụng</button>
    </div>
    <div id="gateBox"></div>
  </div>
  <div class="card"><h2>Trạng thái doanh thu (tháng này)</h2><div class="h-en">Tách rõ doanh thu hoàn tất · cọc/pipeline · tổng cash-in</div>
    <div class="rev3">
      <div class="rc done"><div class="l">Doanh thu hoàn tất</div><div class="val" style="font-family:'Inter',sans-serif;font-size:25px;font-weight:600;margin-top:6px">${tyS(agg(MONTH,s=>s.revenue))}</div><div class="s">Dịch vụ đã thực hiện, có doanh thu thật</div></div>
      <div class="rc"><div class="l">Cọc / pipeline</div><div class="val" style="font-family:'Inter',sans-serif;font-size:25px;font-weight:600;margin-top:6px">${tr(agg(MONTH,s=>s.deposit))}</div><div class="s">Tiền đặt trước cho dịch vụ tương lai</div></div>
      <div class="rc"><div class="l">Tổng cash-in</div><div class="val" style="font-family:'Inter',sans-serif;font-size:25px;font-weight:600;margin-top:6px">${tyS(agg(MONTH,s=>s.cash_in))}</div><div class="s">Hoàn tất + cọc = tiền thực thu trong kỳ</div></div>
    </div>
    ${dqChips()}
  </div>
  ${divProgress()}
  ${DIVFILTER!=='all'?`<div class="card" style="padding:14px 18px"><div class="note" style="margin:0">Đang lọc <b>${DIVFILTER}</b>: mọi số (KPI, biểu đồ, phễu, target) đã theo division — doanh thu từ bills, chi phí ad & tin nhắn tách theo ${DIVFILTER==='Ngoại khoa'?'2 account Meta ngoại khoa (Swan3, Swan4)':'2 account Meta nội khoa (Swan2, Swan5) + TikTok'} qua tag dịch vụ ở tên ad.</div></div>`:''}
  <div class="kpis six" style="margin-top:22px">${kpis}</div>
  <div class="card">
    <h2>Doanh thu & hiệu quả theo ngày</h2><div class="h-en">Di chuột / chạm vào từng ngày để xem chi tiết · chọn khung thời gian</div>
    <div class="ranges" id="chartRanges">
      <button class="on" onclick="selectRange('mtd',this)">Tháng này</button>
      <button onclick="selectRange('today',this)">Hôm nay</button>
      <button onclick="selectRange('y',this)">Hôm qua</button>
      <button onclick="selectRange('d3',this)">3 ngày</button>
      <button onclick="selectRange('d7',this)">7 ngày</button>
      <button onclick="selectRange('d15',this)">15 ngày</button>
      <button onclick="selectRange('d30',this)">30 ngày</button>
      <button onclick="toggleCustom(this)">Tùy chỉnh</button>
    </div>
    <div class="custom" id="customBox" style="display:none">
      <input type="date" id="cFrom" min="${dmin}" max="${dmax}" value="${dmin}">
      <span>→</span>
      <input type="date" id="cTo" min="${dmin}" max="${dmax}" value="${dmax}">
      <button onclick="applyCustom()">Áp dụng</button>
    </div>
    <div id="chartBox"></div>
    <div class="legend">
      <span><i style="background:var(--jade)"></i>Doanh thu thuần</span>
      <span><i style="background:#A9CFC5"></i>Doanh thu cọc</span>
      <span><i style="background:var(--gold)"></i>Chi quảng cáo</span>
      <span style="color:var(--rose)"><i style="background:var(--rose)"></i>Bill trung vị (trục phải)</span>
      <span style="color:var(--jade)">▲ ROAS mỗi ngày</span></div>
  </div>
  <div class="kpis kpi-sm" style="margin-top:18px">
    ${bcard('Bill trung vị','Giá trị giữa của bill khách',mMed,tr,1,false)}
    ${bcard('Bill trung bình','Doanh thu ÷ khách có DT',mMean,tr,1,false)}
    ${bcard('Tin nhắn','Meta + TikTok',mMsg,v=>Math.round(v).toLocaleString('vi-VN'),1,true)}
    ${bcard('Tỉ lệ chuyển đổi','Msg → khách (DT+cọc)',mConv,v=>v.toFixed(1)+'%',1,false)}
  </div>
  ${DIVFILTER==='all'?newtkCard():''}
  <div class="card"><div class="src">
    <span>Nguồn: <b>MNG…BAOCAONGAY</b> · sheet BCngày- T06</span>
    <span><b>Meta</b> Trung-Swan2 Daily Report</span>
    <span><b>TikTok</b> Báo cáo ngày</span>
    <span>Cập nhật: tự động mỗi 5:45</span></div></div>`;
}

/* ---------- SERVICE ---------- */
const PIECOL=['#0F7B74','#B6802A','#A8443A','#2BA39B','#D9B36A','#7A9B94','#C77B5C','#5A7D74'];
let PIE=[];
function arcPath(cx,cy,r,ri,a0,a1){
  const pt=(rr,a)=>[cx+rr*Math.cos(a),cy+rr*Math.sin(a)];
  const large=(a1-a0)>Math.PI?1:0;
  const [x0,y0]=pt(r,a0),[x1,y1]=pt(r,a1),[x2,y2]=pt(ri,a1),[x3,y3]=pt(ri,a0);
  return `M${x0.toFixed(1)} ${y0.toFixed(1)} A${r} ${r} 0 ${large} 1 ${x1.toFixed(1)} ${y1.toFixed(1)} L${x2.toFixed(1)} ${y2.toFixed(1)} A${ri} ${ri} 0 ${large} 0 ${x3.toFixed(1)} ${y3.toFixed(1)} Z`;
}
function buildPie(rows,total){
  const cx=150,cy=150,r=132,ri=78; let a=-Math.PI/2,slices='';
  rows.forEach((s,i)=>{
    const a1=a+(s.revenue/total)*Math.PI*2;
    slices+=`<path class="slice" d="${arcPath(cx,cy,r,ri,a,a1-0.004)}" fill="${PIECOL[i%PIECOL.length]}" onmousemove="showPieTip(event,${i})" onmouseleave="hideTip()" onclick="showPieTip(event,${i})"></path>`;
    a=a1;
  });
  return `<svg viewBox="0 0 300 300">${slices}
    <text x="150" y="143" text-anchor="middle" style="font-family:'Inter',sans-serif;font-size:27px;font-weight:600;fill:var(--ink)">${tyS(total)}</text>
    <text x="150" y="166" text-anchor="middle" style="font-size:11px;fill:var(--ink-soft);letter-spacing:.04em">DOANH THU</text></svg>`;
}
function showPieTip(e,i){
  const s=PIE[i]; if(!s)return; const t=document.getElementById('tip');
  t.innerHTML=`<div class="tt-d">${s.group}</div>
    <div class="tt-r hl"><span>Doanh thu</span><b>${tr(s.revenue)}</b></div>
    <div class="tt-r"><span>Tỉ trọng</span><b>${s.pct}%</b></div>
    <div class="tt-r"><span>Số dòng DV</span><b>${s.lines||'—'}</b></div>
    <div class="tt-r"><span>Bill trung vị</span><b>${tr(s.median||0)}</b></div>`;
  t.style.display='block';
  t.style.left=Math.min(e.clientX+16,window.innerWidth-210)+'px';
  t.style.top=Math.min(e.clientY+16,window.innerHeight-200)+'px';
}
function service(){
  const rows=DATA.services.filter(s=>s.revenue>0&&inDiv(s.division));
  if(!rows.length&&!DATA.services.some(s=>(s.ad_spend>0||s.revenue>0)&&inDiv(s.division))) return divEmpty();
  const total=rows.reduce((a,s)=>a+s.revenue,0)||1;
  const pipe=DATA.services.filter(s=>(s.deposit||0)>0&&inDiv(s.division));
  const pipeTotal=pipe.reduce((a,s)=>a+s.deposit,0);
  PIE=rows.map(s=>({group:s.group,revenue:s.revenue,pct:(s.revenue/total*100).toFixed(1),lines:s.lines,median:s.median}));
  const legend=rows.map((s,i)=>`<div class="pli"><span class="sw" style="background:${PIECOL[i%PIECOL.length]}"></span>
    <span class="pnm">${s.group}</span><span class="pval">${tr(s.revenue)}</span><span class="ppct">${(s.revenue/total*100).toFixed(1)}%</span></div>`).join('');
  const pipeLegend=pipe.map((s,i)=>`<div class="pli"><span class="sw" style="background:${PIECOL[i%PIECOL.length]}"></span><span class="pnm">${s.group}</span><span class="pval">${tr(s.deposit)}</span><span class="ppct">${(s.deposit/pipeTotal*100).toFixed(0)}%</span></div>`).join('');
  const dash='<span style="color:var(--ink-soft)">—</span>';
  const dvchip=s=>s.division?`<span class="dvtag ${s.division.includes('Ngoại')?'ngoai':'noi'}">${s.division.includes('Ngoại')?'Ngoại':'Nội'}</span>`:'';
  const svRv=rows.map(s=>s.revenue),svRvMn=Math.min(...svRv),svRvMx=Math.max(...svRv);
  const lineTbl=rows.map(s=>{const has=s.lines!=null;return `<tr>
      <td><b>${s.group}</b>${dvchip(s)}</td><td>${has?s.lines:dash}</td><td${heat(s.revenue,svRvMn,svRvMx)}>${tr(s.revenue)}</td>
      <td>${has?tr(s.median):dash}</td><td>${has?tr(s.p90):dash}</td><td>${has?cvtag(s.cv):dash}</td>
      <td>${has?`${s.top_bills} · <b>${s.top_share}%</b>`:dash}</td></tr>`;}).join('');
  const bw=DATA.services.filter(s=>(s.cust_with||0)>0&&inDiv(s.division));
  const bwRv=bw.map(s=>s.rev_with),bwMn=Math.min(...bwRv),bwMx=Math.max(...bwRv);
  const billTbl=bw.map(s=>{const has=s.cust_median!=null;return `<tr>
      <td><b>${s.group}</b>${dvchip(s)}</td><td>${s.cust_with}</td><td${heat(s.rev_with,bwMn,bwMx)}>${tr(s.rev_with)}</td>
      <td>${has?tr(s.cust_median):dash}</td><td>${has?tr(s.cust_p90):dash}</td><td>${has?cvtag(s.cust_cv):dash}</td>
      <td>${has?`${s.cust_top_bills} \u00B7 <b>${s.cust_top_share}%</b>`:dash}</td><td>${s.svc_attach}%</td></tr>`;}).join('');
  const roasTag=r=>r==null?dash:`<span class="cvtag ${r>=8?'cg':r>=4?'cm':'cb'}">${r}x</span>`;
  const fsvc=DATA.services.filter(s=>(s.revenue>0||s.ad_spend>0)&&inDiv(s.division)).sort((a,b)=>b.revenue-a.revenue);
  const cplOf=s=>s.ad_msg>0?s.ad_spend/s.ad_msg:null, convOf=s=>s.ad_msg>0?s.cust_with/s.ad_msg*100:null, addtOf=s=>(s.ad_spend>0&&s.revenue>0)?s.ad_spend/s.revenue*100:null;
  const _ar=f=>fsvc.map(f).filter(x=>x!=null&&isFinite(x)&&x>0), lo=a=>a.length?Math.min(...a):0, hi=a=>a.length?Math.max(...a):1;
  const Hmsg=_ar(s=>s.ad_msg),Hcpl=_ar(cplOf),Hconv=_ar(convOf),Hrev=_ar(s=>s.revenue),Haddt=_ar(addtOf);
  const TS=fsvc.reduce((a,s)=>a+(s.ad_spend||0),0),TM=fsvc.reduce((a,s)=>a+(s.ad_msg||0),0),TK=fsvc.reduce((a,s)=>a+(s.cust_with||0),0),TRV=fsvc.reduce((a,s)=>a+(s.revenue||0),0);
  const ps=(v,t)=>t?` <span class="pctsub">(${Math.round(v/t*100)}%)</span>`:'';
  const funnelRows=fsvc.map(s=>{
    const cpl=cplOf(s),conv=convOf(s),cac=(s.ad_spend>0&&s.cust_with>0)?s.ad_spend/s.cust_with:null,addt=addtOf(s);
    return `<tr><td><b>${s.group}</b>${dvchip(s)}</td>
      <td>${s.ad_spend?tr(s.ad_spend)+ps(s.ad_spend,TS):dash}</td>
      <td${s.ad_msg?heat(s.ad_msg,lo(Hmsg),hi(Hmsg)):''}>${s.ad_msg?s.ad_msg+ps(s.ad_msg,TM):dash}</td>
      <td${cpl!=null?heatR(cpl,lo(Hcpl),hi(Hcpl)):''}>${cpl!=null?Math.round(cpl/1e3).toLocaleString('vi-VN')+'k':dash}</td>
      <td${conv!=null?heat(conv,lo(Hconv),hi(Hconv)):''}>${conv!=null?conv.toFixed(1)+'%':dash}</td>
      <td>${s.cust_with?s.cust_with+ps(s.cust_with,TK):dash}</td>
      <td>${cac!=null?tr1(cac):dash}</td>
      <td${heat(s.revenue,lo(Hrev),hi(Hrev))}><b>${tr(s.revenue)}</b>${ps(s.revenue,TRV)}</td>
      <td${addt!=null?heatR(addt,lo(Haddt),hi(Haddt)):''}>${addt!=null?addt.toFixed(1)+'%':dash}</td>
      <td>${roasTag(s.proxy_roas)}</td></tr>`;}).join('');
  const funnelCard=`<div class="card svctbl"><h2>Hiệu suất theo dịch vụ — 3 cổng</h2><div class="h-en">Quảng cáo → Tin nhắn → Khách → Doanh số · ROI từng dịch vụ</div>
    <table><thead><tr><th>Dịch vụ</th><th>Chi quảng cáo</th><th>Tin nhắn</th><th>CPL/tin nhắn</th><th>TN→Khách</th><th>Khách có DT</th><th>Chi ad/khách</th><th>Doanh thu</th><th>Ad/DT</th><th>ROAS (proxy)</th></tr></thead><tbody>${funnelRows}</tbody></table>
    <div class="note" style="margin-top:12px"><b>3 cổng:</b> \u2460 Quảng cáo→Tin nhắn (Chi \u00B7 Tin nhắn \u00B7 CPL) \u00B7 \u2461 Tin nhắn→Khách (TN→Khách \u00B7 Khách \u00B7 Chi ad/khách) \u00B7 \u2462 Khách→Doanh số (Doanh thu \u00B7 Ad/DT \u00B7 ROAS). <b>TN→Khách</b> = khách có DT \u00F7 tin nhắn; <b>Ad/DT</b> = chi quảng cáo \u00F7 doanh thu (càng thấp càng tốt). <b>Lưu ý:</b> Chi &amp; Tin nhắn lấy từ báo cáo ad (gán dịch vụ qua [TÊN DV] trong tên chiến dịch); Khách &amp; Doanh thu lấy từ sheet doanh thu. ROAS là <b>proxy theo nhóm</b> (chưa nối từng khách với ad — vài khách đến từ giới thiệu/tự nhiên) \u2014 ROAS thật cần nguồn lead/SĐT. Dịch vụ không chạy ad ghi \u201C—\u201D ở cột chi/tin nhắn.</div></div>`;
  return `
  ${insightCards('service')}
  ${DIVFILTER!=='all'?`<div class="card" style="padding:14px 18px"><div class="note" style="margin:0">Đang lọc <b>${DIVFILTER}</b> — đây là góc nhìn theo <b>dòng dịch vụ</b> (mọi dòng thuộc nhóm của division). Có thể lệch nhẹ với doanh thu division ở tab <b>Nội / Ngoại</b> (tính theo <b>bill chính</b>: cả bill thuộc về division của dịch vụ chính). Sẽ thống nhất sau khi chốt định nghĩa với file cập nhật.</div></div>`:''}
  <div class="card"><div class="svcpies">
    <div class="svcpie-main"><h2>Doanh thu hoàn tất theo dịch vụ</h2><div class="h-en">Chỉ doanh thu thật (loại cọc) · di chuột vào từng phần để xem chi tiết</div>
      <div class="piewrap"><div class="pie">${buildPie(rows,total)}</div><div class="pielegend">${legend}</div></div></div>
    ${pipe.length?`<div class="svcpie-side"><h2 style="font-size:15px">Cọc / pipeline</h2><div class="h-en">Đặt trước cho DV tương lai · ${tr(pipeTotal)}</div>
      <div class="piewrap small"><div class="pie">${buildPieStatic(pipe.map(s=>({group:s.group,val:s.deposit})),pipeTotal,'CỌC')}</div><div class="pielegend">${pipeLegend}</div></div></div>`:''}
  </div></div>
  ${funnelCard}
  <div class="card svctbl"><h2>Phân phối theo lượt dịch vụ</h2><div class="h-en">Mỗi lượt = một lần một dịch vụ được thực hiện & tính tiền (một khách có thể có nhiều lượt)</div>
   <table><thead><tr><th>Dịch vụ</th><th>Số lượt có doanh thu</th><th>Doanh thu</th><th>Trung vị</th><th>P90</th><th>Độ ổn định (CV)</th><th>Top 20%</th></tr></thead>
   <tbody>${lineTbl}</tbody></table>
   <div class="note" style="margin-top:12px"><b>Cách đọc:</b> <b>Số lượt có doanh thu</b> = số lần dịch vụ này được làm và thu tiền (loại lần miễn phí 0đ và cọc). <b>Trung vị</b> = giá trị giữa của mỗi lần làm dịch vụ; <b>P90</b> = ngưỡng 10% lượt đắt nhất. <b>CV</b> = độ phân tán giá trị (≥140% rất lệch). <b>Top 20%</b> = 20% lượt giá trị cao nhất gánh bao nhiêu % doanh thu của dịch vụ.</div>
  </div>
  <div class="card svctbl"><h2>Phân tích theo khách</h2><div class="h-en">Đơn vị là khách (mỗi khách tính 1 lần dù làm nhiều dịch vụ) — khác với “lượt dịch vụ” ở trên</div>
   <table><thead><tr><th>Dịch vụ</th><th>Số khách dùng DV này</th><th>Doanh thu nhóm khách đó</th><th>Trung vị/khách</th><th>P90</th><th>Độ ổn định (CV)</th><th>Top 20%</th><th>Mua kèm DV khác</th></tr></thead>
   <tbody>${billTbl}</tbody></table>
   <div class="note" style="margin-top:12px;color:var(--ink-soft)"><b>Trung vị/khách · P90 · CV · Top 20%</b> tính trên <b>tổng giá trị mỗi khách</b> dùng dịch vụ này (gồm cả dịch vụ mua kèm) — khác bảng trên (tính theo từng lượt dịch vụ). <b>Mua kèm DV khác</b> = % khách dùng DV này có làm thêm nhóm khác cùng lần đến.</div>
  </div>`;
}

/* ---------- PLATFORM ---------- */
function platform(){
  const _pd=(DIVFILTER==='all')?DATA.platform:((DATA.platform_div&&DATA.platform_div[DIVFILTER])||DATA.platform);
  const dnote=DIVFILTER!=='all'?`<div class="card" style="padding:14px 18px"><div class="note" style="margin:0">Đang lọc <b>${DIVFILTER}</b> — số dưới đây chỉ gồm ad của mảng này (${DIVFILTER==='Ngoại khoa'?'2 account Meta Swan3 + Swan4, <b>không chạy TikTok</b> nên cột TikTok = 0':'2 account Meta Swan2 + Swan5 + TikTok'}), tách theo tag dịch vụ ở tên ad.</div></div>`:'';
  const m=_pd.meta, t=_pd.tiktok, pe=DATA.platform_extra;
  const totSpend=(m.spend+t.spend)||1, totLead=(m.new_lead+t.new_lead)||1;
  const kk=v=>v==null?'\u2014':k(v);
  const pct=(a,b)=>b?Math.round(a/b*100)+'%':'\u2014';
  const cmp=(lab,mv,tv)=>`<tr><td>${lab}</td><td>${mv}</td><td>${tv}</td></tr>`;
  const block1=`<div class="card svctbl"><h2>Meta vs TikTok \u2014 tổng quan</h2><div class="h-en">Nền tảng nào mua nhu cầu rẻ hơn (tách rõ hội thoại vs lead mới)</div>
    <table><thead><tr><th>Chỉ số</th><th>Meta</th><th>TikTok</th></tr></thead><tbody>
      ${cmp('Chi phí',tr(m.spend),tr(t.spend))}
      ${cmp('% ngân sách',pct(m.spend,totSpend),pct(t.spend,totSpend))}
      ${cmp('Hội thoại (conversations)',m.conv.toLocaleString('vi-VN'),t.conv.toLocaleString('vi-VN'))}
      ${cmp('Lead mới (new leads)',m.new_lead.toLocaleString('vi-VN'),t.new_lead.toLocaleString('vi-VN'))}
      ${cmp('CPL theo hội thoại',kk(m.cpl_conv),kk(t.cpl_conv))}
      ${cmp('CPL theo lead mới',kk(m.cpl_lead),kk(t.cpl_lead))}
      ${cmp('CPM',kk(m.cpm),kk(t.cpm))}
      ${cmp('CTR',m.ctr!=null?m.ctr+'%':'\u2014 (không có click)',t.ctr!=null?t.ctr+'%':'\u2014')}
      ${cmp('Frequency',m.freq??'\u2014',t.freq??'\u2014')}
    </tbody></table>
    <div class="note" style="margin-top:12px"><b>Lưu ý:</b> Meta \u201Clead mới\u201D = New messaging contacts; TikTok \u201Clead mới\u201D = Leads (DM). Đừng cộng \u201Cnew contacts\u201D của Meta với \u201Cconversations\u201D của TikTok \u2014 hai khái niệm khác nhau. TikTok rẻ hơn ở <b>hội thoại</b> nhưng đắt hơn ở <b>lead mới</b>.</div></div>`;
  // Block 2: platform x service
  const px=[];
  const psvc=(p,ads)=>ads.forEach(s=>px.push({plat:p,...s}));
  psvc('Meta',m.spend_by_service); psvc('TikTok',t.spend_by_service);
  const totLeadSvc=px.reduce((a,s)=>a+s.lead,0)||1, totSpendSvc=px.reduce((a,s)=>a+s.spend,0)||1;
  const pxTbl=px.sort((a,b)=>b.spend-a.spend).map(s=>`<tr><td><b>${s.plat}</b></td><td>${s.group}${dvchipG(s.group)}</td><td>${tr(s.spend)}</td>
    <td>${s.lead}</td><td>${s.cpl?k(s.cpl):'\u2014'}</td><td>${pct(s.spend,totSpendSvc)}</td><td>${pct(s.lead,totLeadSvc)}</td></tr>`).join('');
  const block2=`<div class="card svctbl"><h2>Nền tảng \u00D7 Dịch vụ</h2><div class="h-en">Mỗi nền tảng đang mạnh ở dịch vụ nào</div>
    <table><thead><tr><th>Nền tảng</th><th>Dịch vụ</th><th>Spend</th><th>Lead mới</th><th>CPL</th><th>% spend</th><th>% lead</th></tr></thead><tbody>${pxTbl}</tbody></table></div>`;
  // Block 3: creative / ad table
  const sb=s=>`<span class="statusb s-${s}">${s}</span>`;
  const adTbl=pe.ads.filter(a=>DIVFILTER==='all'||a.div===DIVFILTER).slice(0,22).map(a=>`<tr><td title="${a.name}">${a.name}</td><td>${a.platform}</td><td>${a.group}${dvchipG(a.group)}</td>
    <td>${tr(a.spend)}</td><td>${a.lead}</td><td>${a.cpl?k(a.cpl):'\u2014'}</td><td>${a.freq??'\u2014'}</td><td>${sb(a.status)}</td></tr>`).join('');
  const block3=`<div class="card svctbl"><h2>Hiệu quả từng quảng cáo</h2><div class="h-en">Gợi ý hành động theo CPL & frequency \u00B7 benchmark CPL ${k(pe.benchmark_cpl)} \u00B7 ${pe.n_ads} ads</div>
    <div class="dqbar" style="margin-top:0;margin-bottom:6px">
      <span class="dqchip">Top 20% ads tạo <b>${pe.winner_pct}%</b> lead</span>
      <span class="dqchip warn">Spend lãng phí ~<b>${tr(pe.waste_spend)}</b> (ad không/ít ra lead)</span></div>
    <table><thead><tr><th>Quảng cáo</th><th>Nền tảng</th><th>DV</th><th>Spend</th><th>Lead</th><th>CPL</th><th>Freq</th><th>Trạng thái</th></tr></thead><tbody>${adTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Scale</b>: đủ lead, CPL rẻ hơn benchmark \u00B7 <b>Giữ</b>: ổn \u00B7 <b>Watch</b>: CPL cao hơn benchmark hoặc frequency cao (creative mệt) \u00B7 <b>Hold</b>: mới chạy, chưa đủ data \u00B7 <b>Cut</b>: spend lớn nhưng không/ít ra lead. Hiện top 22 ad theo chi phí.</div></div>`;
  // Block 4: proxy roas
  const proxy=DATA.services.filter(s=>s.ad_spend>0&&inDiv(s.division)).map(s=>`<tr><td><b>${s.group}</b>${dvchipG(s.group)}</td><td>${tr(s.revenue)}</td><td>${tr(s.ad_spend)}</td><td><b>${s.proxy_roas}x</b></td></tr>`).join('');
  const block4=`<div class="card svctbl"><h2>Proxy ROAS theo dịch vụ</h2><div class="h-en">Doanh thu hoàn tất của DV \u00F7 chi quảng cáo của DV (gộp 2 nền tảng)</div>
    <table><thead><tr><th>Dịch vụ</th><th>Doanh thu hoàn tất</th><th>Chi quảng cáo</th><th>Proxy ROAS</th></tr></thead><tbody>${proxy}</tbody></table>
    <div class="note" style="margin-top:12px"><b>\u26A0 Đây là PROXY, chưa phải ROAS thật.</b> Chỉ ghép quảng cáo với doanh thu theo <b>nhóm dịch vụ</b>, không khớp theo từng khách \u2014 là tương quan, không phải attribution. Để có ROAS nền tảng thật cần thêm: nguồn lead (Meta/TikTok), campaign/ad id, hoặc SĐT khách để khớp lead với bill. Đừng scale ngân sách chỉ dựa vào proxy.</div></div>`;
  return insightCards('platform')+dnote+block1+block2+block3+block4;
}

function salesList(){return DIVFILTER==='all'?DATA.sales:((DATA.sales_div&&DATA.sales_div[DIVFILTER])||[]);}
/* ---------- SALES ---------- */
function sales(){
  const rows=salesList();
  if(!rows.length) return divEmpty();
  const byRev=[...rows].sort((a,b)=>b.revenue-a.revenue);
  const byQual=[...rows].filter(s=>s.paying>0||s.customers>=3).sort((a,b)=>b.paid_rate-a.paid_rate);
  const byX=[...rows].filter(s=>s.xsell>0).sort((a,b)=>xsScore(b)-xsScore(a));
  const mdays=S.filter(s=>s.date.slice(0,7)===TODAY_DATE.slice(0,7)).length||S.length;
  const perDay=s=>(s.paying/mdays).toFixed(1);
  const stab=s=>((s.paying/mdays)<1||s.paying_cv==null)?'<span style="color:var(--muted)">\u2014</span>':cvtag(s.paying_cv);
  const svj=v=>v==null?'<span style="color:var(--muted)">\u2014</span>':`<span style="color:${v>=1.1?'var(--pos)':v<0.9?'var(--neg)':'var(--warn)'}">${v>=1.1?'Giá trị cao':v<0.9?'Dưới kỳ vọng':'Bình thường'} \u00B7 ${v.toFixed(2)}</span>`;
  const pdv=byRev.map(s=>+perDay(s)),pdMn=Math.min(...pdv),pdMx=Math.max(...pdv);
  const rvv=byRev.map(s=>s.revenue),rvMn=Math.min(...rvv),rvMx=Math.max(...rvv);
  const isCloser=s=>!/CSKH|ONLINE|TRỰC TIẾP|TRUC TIEP/i.test(s.name||'');
  const lbR=miniLB('Top doanh thu','Doanh thu hoàn tất toàn kỳ',byRev.filter(isCloser).map(s=>({name:s.name,disp:tr(s.revenue)})),'s-rev');
  const lbP=miniLB('Top khách DT/ngày','Năng suất chốt mỗi ngày',[...rows].filter(isCloser).sort((a,b)=>(b.paying/mdays)-(a.paying/mdays)).map(s=>({name:s.name,disp:perDay(s)})),'s-rev');
  const lbX=miniLB('Top bán chéo','Số bill \u00D7 \u221Aattach',byX.filter(isCloser).map(s=>({name:s.name,disp:`${s.xsell} bill \u00B7 ${s.attach}%`})),'s-xsell');
  const revTbl=byRev.map(s=>`<tr><td><b>${s.name}</b></td><td>${s.customers}</td><td${heat(+perDay(s),pdMn,pdMx)}><b>${perDay(s)}</b></td><td>${stab(s)}</td><td${heat(s.revenue,rvMn,rvMx)}>${tr(s.revenue)}</td>
    <td>${tr(s.cash_in)}</td><td>${s.median?tr(s.median):'\u2014'}</td><td>${s.new}/${s.tk}</td><td>${/CSKH|ONLINE|TRỰC TIẾP|TRUC TIEP/i.test(s.name||'')?'<span style="color:var(--muted)">— CSKH</span>':svj(s.value_index)}</td></tr>`).join('');
  const qualTbl=byQual.map(s=>`<tr><td><b>${s.name}</b></td><td>${s.paid_rate}%</td><td>${s.monetized_rate}%</td><td>${s.deposit_rate}%</td><td>${s.zero_pct}%</td><td>${s.new_paid}/${s.tk_paid}</td></tr>`).join('');
  const xTbl=byX.map(s=>`<tr><td><b>${s.name}</b></td><td>${s.paying}</td><td>${s.xsell}</td><td>${s.attach}%</td><td><b>${xsScore(s).toFixed(1)}</b></td><td>${s.aov_xsell?tr(s.aov_xsell):'\u2014'}</td><td>${s.uplift?'+'+s.uplift+'%':'\u2014'}</td></tr>`).join('');
  return `
  ${insightCards('sales')}
  <div class="lbgrid">${lbR}${lbP}${lbX}</div>
  <div class="card svctbl" id="s-rev"><h2>Ranking doanh thu</h2><div class="h-en">Ai mang về nhiều tiền nhất (toàn kỳ)</div>
    <table><thead><tr><th>Sale</th><th>Khách</th><th>Khách DT/ngày</th><th>Độ ổn định (CV)</th><th>DT hoàn tất</th><th>Cash-in</th><th>Trung vị</th><th>New/TK</th><th>Đánh giá</th></tr></thead><tbody>${revTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Khách DT/ngày</b> = số khách có doanh thu của sale đó \u00F7 ${mdays} ngày trong tháng (mọi sale đi làm mỗi ngày nên ngày 0 khách vẫn tính) — năng suất chốt khách trung bình mỗi ngày. <b>Ổn định</b> = độ dao động khách DT giữa các ngày (CV): càng thấp càng đều và dễ đoán, không phụ thuộc vài ngày bùng phát. <span style="color:var(--jade)">&lt;60% ổn định</span> \u00B7 <span style="color:var(--gold)">60\u2013110% khá đều</span> \u00B7 <span style="color:var(--rose)">&gt;110% dao động</span>. <b>Đánh giá</b> = chỉ số giá trị khách (giống Chỉ số DT kỳ vọng của master): doanh thu thực tế so với kỳ vọng theo nhóm dịch vụ khách mua \u2014 &ge;1.1 khách giá trị cao hơn mặt bằng, &lt;0.9 dưới kỳ vọng.</div></div>
  <div class="card svctbl"><h2>Ranking chất lượng chuyển đổi</h2><div class="h-en">Ai chốt khéo \u2014 tách khỏi lợi thế được chia khách dễ</div>
    <table><thead><tr><th>Sale</th><th>% trả tiền</th><th>% có giá trị TM</th><th>% đặt cọc</th><th>% khách 0đ</th><th>New/TK chốt</th></tr></thead><tbody>${qualTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>% trả tiền</b> = khách tạo doanh thu / tổng khách. <b>% có giá trị TM</b> = (khách DT + cọc) / tổng khách. <b>New/TK chốt</b> = số khách mới / tái khám đã trả tiền. Doanh thu cao chưa chắc chốt giỏi \u2014 có thể do được chia khách giá trị cao.</div></div>
  <div class="card svctbl" id="s-xsell"><h2>Ranking bán chéo</h2><div class="h-en">Ai gợi mở khách mua thêm dịch vụ tốt nhất \u2014 xếp theo điểm (số bill \u00D7 \u221Aattach)</div>
    <table><thead><tr><th>Sale</th><th>Khách DT</th><th>Bill bán chéo</th><th>Attach</th><th>Điểm</th><th>AOV bán chéo</th><th>Uplift</th></tr></thead><tbody>${xTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Điểm bán chéo = số bill bán chéo \u00D7 \u221A(tỉ lệ attach %)</b> \u2014 ưu tiên người tạo <b>nhiều bill</b> bán chéo, vẫn thưởng tỉ lệ cao. Vì vậy 6 bill @ 20% (YN) xếp trên 1 bill @ 33% (HÀ).</div></div>
  <div class="card"><div class="note" style="margin:0"><b>Quy ước gán Sale:</b> mỗi bill gán cho người trực tiếp chốt (loại nhãn kênh THƯCSKH/TRỰC TIẾP); bill chỉ có kênh online ghi là \u201CCSKH Online\u201D. Tổng doanh thu = đúng doanh thu hoàn tất, không đếm trùng. <b>CSKH Online</b> là vai trò chăm sóc khách cũ quay lại (không phải telesale chốt), nên được <b>loại khỏi phần insight/đánh giá chốt</b> — tạm thời cho đến khi vai trò thay đổi. <b>Lưu ý New/TK:</b> đây là loại lượt khám ở mức bill, không phải phân định khách mới vs khách cũ của riêng sale (mỗi sale đều chăm cả khách mới lẫn khách cũ). <b>Để có phễu đầy đủ</b> (lead \u2192 booking \u2192 show-up \u2192 chốt) cần thêm dữ liệu phân bổ lead từ CRM/Messenger.</div></div>`;
}

function master(){
  const ms=DATA.masters.filter(m=>inDiv(m.division));
  if(!ms.length) return divEmpty();
  const byRev=[...ms].sort((a,b)=>b.revenue-a.revenue);
  const mRv=byRev.map(m=>m.revenue),mRvMn=Math.min(...mRv),mRvMx=Math.max(...mRv);
  const byVI=[...ms].filter(m=>m.value_index!=null&&m.paying>=2).sort((a,b)=>b.value_index-a.value_index);
  const byXs=[...ms].filter(m=>m.xsell>0).sort((a,b)=>xsScore(b)-xsScore(a));
  const revTbl=byRev.map(m=>`<tr><td><b>${m.name}</b></td><td>${m.customers}</td><td>${m.paying>=5?cvtag(m.paying_cv):'<span style="color:var(--muted)">\u2014</span>'}</td><td${heat(m.revenue,mRvMn,mRvMx)}>${tr(m.revenue)}</td><td>${m.coc?tr(m.deposit):'\u2014'}</td><td>${m.aov?tr(m.aov):'\u2014'}</td><td>${m.median?tr(m.median):'\u2014'}</td><td>${m.p90?tr(m.p90):'\u2014'}</td><td>${m.new}/${m.tk}</td></tr>`).join('');
  const viTbl=byVI.map(m=>`<tr><td><b>${m.name}</b></td><td>${m.paying}</td><td>${tr(m.revenue)}</td><td>${tr(m.expected)}</td><td>${vitag(m.value_index)}</td><td>${m.value_index>=1.1?'Khai thác tốt hơn mặt bằng':m.value_index<0.9?'Dưới kỳ vọng \u00B7 nên coaching':'Bình thường'}</td></tr>`).join('');
  const attTbl=byXs.map(m=>`<tr><td><b>${m.name}</b></td><td>${m.paying}</td><td>${m.xsell}</td><td>${m.attach}%</td><td><b>${xsScore(m).toFixed(1)}</b></td><td>${m.aov_xsell?tr(m.aov_xsell):'\u2014'}</td><td>${m.uplift?'+'+m.uplift+'%':'\u2014'}</td></tr>`).join('');
  // TK→DT (logic độc lập): master đã biến khách thăm khám/tái khám (0đ) thành bao nhiêu doanh số mới
  const byTK=[...ms].filter(m=>m.tk>=1).sort((a,b)=>(b.tk_paid_rev||0)-(a.tk_paid_rev||0));
  const tkRate=m=>{const r=Math.round(m.tk_paid/m.tk*100),c=r>=60?'cg':r>=40?'cm':'cb';
    return m.tk>=3?`<span class="cvtag ${c}">${r}%</span>`:`<span style="color:var(--muted)">${r}% \u00B7 ít mẫu</span>`;};
  const tkTbl=byTK.map(m=>{const share=m.revenue?Math.round((m.tk_paid_rev||0)/m.revenue*100):0;
    return `<tr><td><b>${m.name}</b></td><td>${m.tk}</td><td>${m.tk_paid}</td><td>${tkRate(m)}</td><td><b>${m.tk_paid_rev?tr(m.tk_paid_rev):'\u2014'}</b></td><td>${m.tk_paid_rev?share+'%':'\u2014'}</td></tr>`;}).join('');
  const lbR=miniLB('Top doanh thu','Doanh thu hoàn tất toàn kỳ',byRev.map(m=>({name:m.name,disp:tr(m.revenue)})),'m-rev');
  const lbT=miniLB('Top chuyển TK→DT','Doanh số mới từ khách thăm khám',byTK.filter(m=>m.tk_paid_rev>0).map(m=>({name:m.name,disp:tr(m.tk_paid_rev)})),'m-tk');
  const lbV=miniLB('Top chỉ số DT kỳ vọng','DT thực tế \u00F7 kỳ vọng',byVI.map(m=>({name:m.name,disp:m.value_index.toFixed(2)})),'m-vi');
  const lbX=miniLB('Top bán chéo','Số bill \u00D7 \u221Aattach',byXs.map(m=>({name:m.name,disp:`${m.xsell} bill \u00B7 ${m.attach}%`})),'m-xsell');
  const mix=ms.filter(m=>Object.keys(m.mix).length).map(m=>{const tot=Object.values(m.mix).reduce((a,b)=>a+b,0)||1;
    return `<div class="nc"><h4>${m.name}<span style="font-weight:500;color:var(--ink-soft);font-size:12px"> \u00B7 ${tr(m.revenue)}</span></h4>${Object.entries(m.mix).slice(0,4).map(([g,v])=>`<div class="r"><span>${g}${dvchipG(g)}</span><b>${(v/tot*100).toFixed(0)}%</b></div>`).join('')}</div>`;}).join('');
  const warn=ms.filter(m=>(m.paying>=3&&m.value_index!=null&&m.value_index<0.9)||(m.tk>=3&&m.tk_paid/m.tk<0.4)).map(m=>{
    const bits=[]; if(m.value_index!=null&&m.value_index<0.9)bits.push('Chỉ số DT kỳ vọng '+m.value_index); if(m.tk>=3&&m.tk_paid/m.tk<0.4)bits.push('chuyển TK→DT '+Math.round(m.tk_paid/m.tk*100)+'%');
    return `<span class="dqchip warn">\u26A0 ${m.name}: ${bits.join(' \u00B7 ')}</span>`;}).join('');
  return `
  ${insightCards('master')}
  <div class="lbgrid lb4">${lbR}${lbT}${lbV}${lbX}</div>
  <div class="card svctbl" id="m-rev"><h2>Ranking doanh thu</h2><div class="h-en">Ai tạo doanh thu thật nhiều nhất tại clinic</div>
    <table><thead><tr><th>Master</th><th>Khách</th><th>Độ ổn định (CV)</th><th>DT hoàn tất</th><th>Cọc</th><th>AOV</th><th>Trung vị</th><th>P90</th><th>New/TK</th></tr></thead><tbody>${revTbl}</tbody></table></div>
  <div class="card svctbl" id="m-tk"><h2>Ranking chuyển TK→DT</h2><div class="h-en">Master biến lượt thăm khám/tái khám (khách 0đ) thành doanh số mới \u2014 chỉ số độc lập, xếp theo doanh số mới sinh ra</div>
    <table><thead><tr><th>Master</th><th>Khách TK</th><th>Đã chốt DT</th><th>Tỉ lệ chuyển</th><th>Doanh số mới từ TK</th><th>% trong DT master</th></tr></thead><tbody>${tkTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Chuyển TK→DT</b> đo riêng khả năng biến khách <b>thăm khám/tái khám (TK)</b> \u2014 vốn đến với 0đ \u2014 thành doanh thu. <b>Tỉ lệ chuyển</b> = số TK chốt DT \u00F7 tổng TK được giao. <b>Doanh số mới từ TK</b> = tổng doanh thu các bill TK mà master này chốt được, chính là phần tiền mới sinh ra từ việc chăm &amp; tư vấn khách 0đ. <b>% trong DT master</b> = doanh số mới từ TK \u00F7 tổng DT của master (đóng góp của mảng chuyển khám vào doanh thu chung). Chỉ số này <b>độc lập, KHÔNG nằm trong</b> Chỉ số DT kỳ vọng (vốn chỉ tính trên khách đã có DT). <span style="color:var(--ink-soft)">Lưu ý: khách 0đ chưa chốt là chăm sóc khách cũ, KHÔNG tính là xấu \u2014 đây là chỉ số cơ hội, không phải chỉ số phạt.</span> <span style="color:var(--muted)">(TK &lt;3 = ít mẫu, tỉ lệ chỉ để tham khảo)</span></div></div>
  <div class="card svctbl" id="m-vi"><h2>Ranking chỉ số DT kỳ vọng</h2><div class="h-en">Doanh thu thực tế \u00F7 doanh thu kỳ vọng theo loại khách được giao \u2014 công bằng hơn doanh thu thô</div>
    <table><thead><tr><th>Master</th><th>Khách DT</th><th>DT thực tế</th><th>DT kỳ vọng</th><th>Chỉ số DT kỳ vọng</th><th>Đánh giá</th></tr></thead><tbody>${viTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Chỉ số DT kỳ vọng</b> = DT thực tế \u00F7 DT kỳ vọng (kỳ vọng = cộng AOV trung bình toàn clinic của nhóm dịch vụ mỗi khách master đó nhận). <b style="color:var(--jade)">\u22651,1</b> khai thác tốt hơn mặt bằng \u00B7 <b style="color:var(--gold)">0,9\u20131,1</b> bình thường \u00B7 <b style="color:var(--rose)">&lt;0,9</b> dưới kỳ vọng, nên coaching. Giúp đánh giá công bằng vì master nhận nhiều khách giá trị cao tự nhiên doanh thu sẽ cao.<br><br><b>Tỉ lệ chuyển TK\u2192DT</b> đã tách thành bảng riêng ở trên (chỉ số <b>độc lập</b>, KHÔNG nằm trong công thức này): Chỉ số DT kỳ vọng chỉ tính trên khách <b>đã có</b> doanh thu, còn chuyển TK\u2192DT đo khả năng biến lượt thăm khám/tái khám (0đ) thành doanh thu mới. Hai chỉ số bổ sung nhau.</div></div>
  <div class="card svctbl" id="m-xsell"><h2>Ranking bán chéo</h2><div class="h-en">Master nào khai thác thêm dịch vụ tốt nhất \u2014 xếp theo điểm (số bill \u00D7 \u221Aattach)</div>
    <table><thead><tr><th>Master</th><th>Khách DT</th><th>Bill bán chéo</th><th>Attach</th><th>Điểm</th><th>AOV bán chéo</th><th>Uplift</th></tr></thead><tbody>${attTbl}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Điểm bán chéo = số bill bán chéo \u00D7 \u221A(tỉ lệ attach %)</b> \u2014 ưu tiên người tạo <b>nhiều bill</b> bán chéo (giá trị thực mang lại), vẫn thưởng tỉ lệ attach cao. Vì vậy 5 bill @ attach vừa xếp trên 1 bill @ attach cao.</div></div>
  <div class="card"><h2>Cơ cấu dịch vụ theo master</h2><div class="h-en">Master mạnh dịch vụ nào (theo doanh thu hoàn tất)</div><div class="ntk">${mix}</div></div>
  ${warn?`<div class="card"><h2>Cảnh báo cần chú ý</h2><div class="dqbar">${warn}</div><div class="note" style="margin-top:10px;color:var(--ink-soft)">Master có Chỉ số DT kỳ vọng thấp hoặc tỉ lệ chuyển khám→DT thấp \u2014 nên xem cách tư vấn để biến lượt thăm khám/tái khám thành doanh thu & đẩy bán chéo. Lưu ý: khách 0đ (tái khám/thăm khám) là chăm sóc khách cũ, KHÔNG tính là xấu.</div></div>`:''}`;
}

/* ---------- CROSS-SELL ---------- */
function cross(){
  const x=(DIVFILTER==='all')?DATA.crosssell:((DATA.crosssell_div&&DATA.crosssell_div[DIVFILTER])||DATA.crosssell);
  if(DIVFILTER!=='all'&&(!x||!x.rev_customers)) return divEmpty();
  const r=x.attach_rate; const deg=r/100*360;
  const card=(lab,en,val)=>`<div class="kpi"><div class="lab">${lab}<span class="en">${en}</span></div><div class="val">${val}</div></div>`;
  const rc=(l,v,s,done)=>`<div class="rc${done?' done':''}"><div class="l">${l}</div><div class="v">${v}</div><div class="s">${s}</div></div>`;
  const pairTbl=x.pairs.map(p=>`<tr><td><b>${p.main}</b>${dvchipG(p.main)}</td><td>${p.attach}${dvchipG(p.attach)}</td><td>${p.bills}</td><td>${tr(p.revenue)}</td></tr>`).join('')||'<tr><td colspan="4" style="color:var(--ink-soft)">Chưa có cặp bán chéo</td></tr>';
  const attRow=s=>`<tr><td><b>${s.name}</b></td><td>${s.paying}</td><td>${s.xsell}</td><td>${s.attach}%</td><td>${s.aov_xsell?tr(s.aov_xsell):'\u2014'}</td><td>${s.aov_nonxsell?tr(s.aov_nonxsell):'\u2014'}</td><td>${s.uplift?'+'+s.uplift+'%':'\u2014'}</td></tr>`;
  const saleAtt=salesList().filter(s=>s.paying>0).sort((a,b)=>b.attach-a.attach).map(attRow).join('')||'<tr><td colspan="7" style="color:var(--ink-soft)">—</td></tr>';
  const mastAtt=DATA.masters.filter(s=>s.paying>0&&inDiv(s.division)).sort((a,b)=>b.attach-a.attach).map(attRow).join('')||'<tr><td colspan="7" style="color:var(--ink-soft)">—</td></tr>';
  const opp=x.opportunity.filter(o=>o.customers>=2).map(o=>`<tr><td><b>${o.group}</b>${dvchipG(o.group)}</td><td>${o.customers}</td><td>${o.attach}%</td><td>${o.aov_non?tr(o.aov_non):'\u2014'}</td><td>${o.aov_x?tr(o.aov_x):'\u2014'}</td><td>${o.uplift!=null?'+'+o.uplift+'%':'\u2014'}</td><td>${o.plus5?'+'+tr(o.plus5):'\u2014'}</td><td>${o.plus10?'+'+tr(o.plus10):'\u2014'}</td><td>${o.plus15?'+'+tr(o.plus15):'\u2014'}</td></tr>`).join('');
  return `
  ${insightCards('cross')}
  <div class="card"><div class="grid2" style="align-items:center">
    <div><h2>Tỉ lệ bán chéo</h2><div class="h-en">Bill có \u22652 nhóm dịch vụ / khách có doanh thu</div>
      <div class="donut" style="background:conic-gradient(var(--jade) 0 ${deg}deg,var(--tint2) ${deg}deg 360deg);position:relative">
        <div style="position:absolute;inset:26px;background:var(--paper-2);border-radius:50%;display:grid;place-items:center">
          <div style="text-align:center"><div style="font-family:Inter;font-size:30px;font-weight:600;color:var(--jade)">${r}%</div>
          <div style="font-size:11px;color:var(--ink-soft);font-weight:600">${x.xsell_bills}/${x.rev_customers} khách</div></div></div></div>
    </div>
    <div class="kpis kpi-sm" style="grid-template-columns:1fr 1fr;margin:0">
      ${card('Số bill bán chéo','Cross-sell bills',x.xsell_bills)}
      ${card('Nhóm DV / khách','Avg service groups',x.avg_groups)}
      ${card('AOV bill bán chéo','AOV cross-sell',tr(x.aov_xsell))}
      ${card('AOV không bán chéo','AOV single',tr(x.aov_nonxsell))}
    </div>
  </div></div>
  <div class="card"><h2>Giá trị của bán chéo</h2><div class="h-en">Khách mua nhiều nhóm dịch vụ đóng góp doanh thu lớn hơn nhiều</div>
    <div class="rev3">
      ${rc('DT từ bill bán chéo',tyS(x.xsell_revenue),'Chiếm '+x.xsell_share+'% doanh thu hoàn tất',true)}
      ${rc('Uplift AOV','+'+x.uplift+'%','Trung vị: '+tr(x.median_xsell)+' vs '+tr(x.median_nonxsell))}
      ${rc('Số khách bán chéo',x.xsell_bills,'trên '+x.rev_customers+' khách có doanh thu')}
    </div>
    <div class="note" style="margin-top:14px"><b>Lưu ý cách đo:</b> \u201CDT từ bill bán chéo\u201D = tổng doanh thu các bill có \u22652 nhóm dịch vụ \u2014 KHÔNG phải \u201Cdoanh thu tăng thêm nhờ bán kèm\u201D. Phần tăng thêm chưa đo được vì dịch vụ phụ đang nhập 0đ; cần nhập giá trị thật từng dịch vụ để đo chính xác.</div>
  </div>
  <div class="card svctbl"><h2>Cặp dịch vụ bán chéo</h2><div class="h-en">Dịch vụ chính (giá trị lớn nhất trong bill) \u2192 dịch vụ làm kèm</div>
    <table><thead><tr><th>Dịch vụ chính</th><th>Bán kèm</th><th>Số bill</th><th>Doanh thu của bill</th></tr></thead><tbody>${pairTbl}</tbody></table>
    <div class="note" style="margin-top:12px;color:var(--ink-soft)">Cặp <b>Tiêm \u2194 Máy</b> đang là combo mạnh nhất \u2014 nên xây script/combo ưu đãi quanh cặp này.</div></div>
  <div class="grid2" style="grid-template-columns:1fr 1fr">
    <div class="card svctbl"><h2>Bán chéo theo Sale</h2><div class="h-en">Ai gợi mở bán thêm tốt</div>
      <table><thead><tr><th>Sale</th><th>Khách DT</th><th>Bill BC</th><th>Attach</th><th>AOV BC</th><th>AOV thường</th><th>Uplift</th></tr></thead><tbody>${saleAtt}</tbody></table></div>
    <div class="card svctbl"><h2>Bán chéo theo Master</h2><div class="h-en">Ai khai thác tại clinic tốt</div>
      <table><thead><tr><th>Master</th><th>Khách DT</th><th>Bill BC</th><th>Attach</th><th>AOV BC</th><th>AOV thường</th><th>Uplift</th></tr></thead><tbody>${mastAtt}</tbody></table></div>
  </div>
  <div class="card svctbl"><h2>Cơ hội doanh thu từ bán chéo</h2><div class="h-en">Doanh thu tăng thêm ước tính nếu nâng attach rate \u2014 không cần mua thêm lead</div>
    <table><thead><tr><th>Dịch vụ chính</th><th>Khách</th><th>Attach hiện tại</th><th>AOV thường</th><th>AOV bán chéo</th><th>Uplift</th><th>+5 điểm %</th><th>+10 điểm %</th><th>+15 điểm %</th></tr></thead><tbody>${opp}</tbody></table>
    <div class="note" style="margin-top:12px"><b>Cách tính:</b> Doanh thu tăng thêm = số khách dịch vụ chính \u00D7 mức tăng attach \u00D7 (AOV bán chéo \u2212 AOV thường). Ví dụ chỉ cần nâng attach <b>Tiêm</b> thêm vài điểm % đã tạo doanh thu lớn hơn việc cố mua thêm lead mới.</div></div>`;
}

/* ---------- MEMO ---------- */
/* ---------- INSIGHT ENGINE (Layer 2) ---------- */
function getInsights(){ if(_INS===null||_INS===undefined) _INS=buildInsights(); return _INS; }
const scr=i=>i.sev*1e12+(i.impact||0);
function dvchipD(d){if(!d)return '<span class="dvtag" style="background:var(--tint);color:var(--ink-soft)">Chung</span>';const ng=String(d).includes('Ngoại');return `<span class="dvtag ${ng?'ngoai':'noi'}">${ng?'Ngoại':'Nội'}</span>`;}
function insightCards(page,max){
  const useDiv=DIVPAGES.includes(page)&&DIVFILTER!=='all'&&page!=='overview';
  const list=getInsights().filter(i=>i.page===page&&(!useDiv||!i.division||i.division===DIVFILTER)).sort((a,b)=>scr(b)-scr(a)).slice(0,max||3);
  const head=useDiv?`Insight &amp; hành động đề xuất \u2014 ${DIVFILTER}`:'Insight &amp; hành động đề xuất';
  if(!list.length) return useDiv?`<div class="card"><div class="ihead">${head}</div><div class="note" style="margin-top:6px">Chưa có insight riêng cho ${DIVFILTER} trong kỳ này.</div></div>`:'';
  return `<div class="card"><div class="ihead">${head}</div><div class="insights">`+
    list.map(i=>`<div class="insight s${i.sev}"><div class="it"><span class="sevdot"></span><span style="flex:1">${i.title}</span>${dvchipD(i.division)}</div>
      <div class="row"><span class="k">Bằng chứng</span><span>${i.ev}</span></div>
      <div class="row"><span class="k">Hành động</span><span><b>${i.act}</b></span></div>
      <div class="row"><span class="k">Phụ trách</span><span>${i.owner}</span></div>
      <div class="row"><span class="k">Tác động</span><span>${i.exp}</span></div></div>`).join('')+`</div></div>`;
}
function buildInsights(){
  const comp=COMPLETE, S=DATA.series, ins=[];
  if(comp.length<2) return ins;
  const sum=(a,f)=>a.reduce((s,x)=>s+f(x),0);
  const yday=comp[comp.length-1], base=comp.slice(Math.max(0,comp.length-8),comp.length-1);
  const dOf=(y,b)=>b?(y-b)/b:0, pcf=d=>(d>=0?'+':'')+Math.round(d*100)+'%';
  const roasOf=a=>{const sp=sum(a,s=>s.spend);return sp?sum(a,s=>s.revenue)/sp:0;};
  const cplOf=a=>{const m=sum(a,s=>s.meta_msg+s.tk_msg);return m?sum(a,s=>s.spend)/m:0;};
  const convOf=a=>{const m=sum(a,s=>s.meta_msg+s.tk_msg);return m?sum(a,s=>s.paying+s.coc)/m*100:0;};
  const aovOf=a=>{const p=sum(a,s=>s.paying);return p?sum(a,s=>s.revenue)/p:0;};
  const add=o=>ins.push(o);

  // A. Operating bottleneck (overview) — weakest gate vs nền 7 ngày
  const dCpl=dOf(cplOf([yday]),cplOf(base)), dConv=dOf(convOf([yday]),convOf(base)), dAov=dOf(aovOf([yday]),aovOf(base));
  const gates=[
    {bad:Math.max(0,dCpl),title:'Cửa 1 (Quảng cáo→Tin nhắn) yếu: CPL tăng',ev:`CPL hôm qua ${pcf(dCpl)} so với nền 7 ngày`,act:'Soát creative/targeting ad CPL cao, tạm dừng ad kém',owner:'Ads team',exp:'Hạ CPL về nền → nhiều lead hơn cùng ngân sách'},
    {bad:Math.max(0,-dConv),title:'Cửa 2 (Tin nhắn→Khách) yếu: tỉ lệ chốt giảm',ev:`Tỉ lệ chuyển đổi ${pcf(dConv)} so với nền`,act:'Nghe lại booking/cuộc gọi hôm qua, soát script & tốc độ phản hồi',owner:'Sale lead',exp:'Khôi phục tỉ lệ chốt về nền → nhiều khách hơn cùng lượng tin nhắn'},
    {bad:Math.max(0,-dAov),title:'Cửa 3 (Khách→Giá trị) yếu: AOV giảm',ev:`AOV hôm qua ${pcf(dAov)} so với nền`,act:'Đẩy bán chéo & gói combo khi khách đến',owner:'Master/Clinic lead',exp:'Nâng AOV về nền → doanh thu mỗi khách cao hơn'},
  ].sort((a,b)=>b.bad-a.bad);
  if(gates[0].bad>=0.15){const g=gates[0]; add({page:'overview',sev:g.bad>=0.3?3:2,impact:0,title:g.title,ev:g.ev,act:g.act,owner:g.owner,exp:g.exp});}

  // B. Ads waste (platform)
  const px=DATA.platform_extra;
  if(px.waste_spend>10e6) add({page:'platform',sev:px.waste_spend>30e6?3:2,impact:px.waste_spend,
    title:'Quảng cáo lãng phí cần cắt',ev:`~${tr(px.waste_spend)} đổ vào ad ít/không ra lead (trên ${px.n_ads} ad)`,
    act:'Cắt/đổi ad trạng thái Cut, dồn ngân sách sang ad đang ra lead rẻ',owner:'Ads team',
    exp:`Tiết kiệm tới ~${tr(px.waste_spend)} hoặc tái phân bổ để tăng lead`});

  // C. Ad scale hypothesis (platform) — đánh dấu giả thuyết, không auto-scale
  const topSvc=DATA.services.filter(s=>s.ad_spend>0&&s.revenue>0).sort((a,b)=>b.revenue-a.revenue)[0];
  if(topSvc) add({page:'platform',sev:1,impact:0,title:`Cân nhắc tăng nhẹ ngân sách ${topSvc.group} (giả thuyết)`,
    ev:`${topSvc.group} doanh thu cao nhất, proxy-ROAS ${topSvc.proxy_roas}x`,
    act:`Thử tăng nhẹ ngân sách ${topSvc.group} và ĐO bằng lead/khách thực — không scale mạnh chỉ theo proxy`,
    owner:'Ads team',exp:'Có thể tăng lead nếu proxy đúng (cần kiểm chứng bằng nguồn lead thật)'});

  // D. Sale — dao động mạnh / chốt thấp (loại CSKH & nhãn kênh: không phải telesale chốt)
  const mdays=S.filter(s=>s.date.slice(0,7)===TODAY_DATE.slice(0,7)).length||S.length;
  const isCloser=s=>{const n=(s.name||'').toUpperCase();return !(n.includes('CSKH')||n.includes('TRỰC TIẾP')||n.includes('TRUC TIEP')||n.includes('ONLINE'));};
  const volat=DATA.sales.filter(s=>isCloser(s)&&(s.paying/mdays)>=1&&s.paying_cv!=null&&s.paying_cv>100).sort((a,b)=>b.paying_cv-a.paying_cv)[0];
  if(volat) add({page:'sales',sev:2,impact:0,division:volat.division,title:`Khách DT của ${volat.name} dao động mạnh`,
    ev:`CV ${volat.paying_cv}% — phụ thuộc vài ngày bùng phát`,act:`Ổn định lịch chốt/chia khách đều hơn cho ${volat.name}`,
    owner:'Sale lead',exp:'Doanh thu đều và dễ đoán hơn'});
  const loPaid=DATA.sales.filter(s=>isCloser(s)&&s.customers>=10).sort((a,b)=>a.paid_rate-b.paid_rate)[0];
  if(loPaid&&loPaid.paid_rate<55) add({page:'sales',sev:2,impact:0,division:loPaid.division,title:`${loPaid.name} chốt ra tiền thấp`,
    ev:`% trả tiền ${loPaid.paid_rate}% trên ${loPaid.customers} khách`,act:`Coaching kỹ năng chốt cho ${loPaid.name}`,
    owner:'Sale lead',exp:'Nâng % trả tiền → thêm khách có doanh thu từ cùng lượng khách'});

  // E. Master TK→DT (trọng tâm)
  const MA=DATA.masters;
  const tp=sum(MA,m=>m.tk_paid||0), tt=sum(MA,m=>m.tk||0), tkClinic=tt?tp/tt:0, clinicAov=aovOf(comp)||0;
  MA.filter(m=>m.tk>=3&&(m.tk_paid/m.tk)<0.4).sort((a,b)=>(a.tk_paid/a.tk)-(b.tk_paid/b.tk)).slice(0,2).forEach(m=>{
    const rate=m.tk_paid/m.tk, gain=Math.max(0,(tkClinic-rate)*m.tk), imp=Math.round(gain*(m.aov||clinicAov));
    add({page:'master',sev:rate<0.2?3:2,impact:imp,division:m.division,title:`${m.name}: chuyển thăm khám→DT thấp`,
      ev:`Chỉ ${m.tk_paid}/${m.tk} khách thăm khám/tái khám thành doanh thu (${Math.round(rate*100)}%)`,
      act:`Huấn luyện ${m.name} tư vấn nhu cầu & đề xuất dịch vụ cho khách tái khám`,owner:'Master/Clinic lead',
      exp:`Nếu đạt mức TB clinic (${Math.round(tkClinic*100)}%) → +~${Math.round(gain)} khách ≈ +${tr(imp)} (giả định AOV như hiện tại)`});
  });

  // F. Master Chỉ số DT kỳ vọng dưới kỳ vọng
  const wM=MA.filter(m=>m.paying>=3&&m.value_index!=null&&m.value_index<0.9).sort((a,b)=>a.value_index-b.value_index)[0];
  if(wM){const gap=Math.max(0,(wM.expected||0)-(wM.revenue||0));
    add({page:'master',sev:2,impact:gap,division:wM.division,title:`${wM.name}: khai thác giá trị dưới kỳ vọng`,
      ev:`Chỉ số DT kỳ vọng ${wM.value_index} (DT ${tr(wM.revenue)} vs kỳ vọng ${tr(wM.expected)})`,
      act:`Coaching ${wM.name} nâng giá trị khai thác (gói cao hơn, bán chéo)`,owner:'Master/Clinic lead',
      exp:`Đưa Chỉ số DT kỳ vọng về ~1.0 ≈ +${tr(gap)} doanh thu`});}

  // G. Cross-sell opportunity
  const opp=(DATA.crosssell.opportunity||[]).filter(o=>o.customers>=5&&o.has_pair).sort((a,b)=>b.plus10-a.plus10)[0];
  if(opp) add({page:'cross',sev:2,impact:opp.plus10,division:DIVMAP_JS[opp.group],title:`Cơ hội bán chéo lớn ở nhóm ${opp.group}`,
    ev:`Attach hiện ${opp.attach}% · ${opp.customers} khách`,act:`Đẩy script/combo bán chéo cho khách ${opp.group}`,
    owner:'Sale / Master',exp:`Attach +10đ% ≈ +${tr(opp.plus10)} doanh thu (giả định mỗi khách thêm ~1 nhóm dịch vụ)`});

  // H. Service concentration
  const totRev=sum(DATA.services,s=>s.revenue)||1;
  const svcTop=DATA.services.filter(s=>s.group!=='(chưa rõ DV)'&&s.revenue>0).sort((a,b)=>b.revenue-a.revenue)[0];
  if(svcTop&&svcTop.top_share>=60) add({page:'service',sev:1,impact:0,division:DIVMAP_JS[svcTop.group],
    title:`Doanh thu ${svcTop.group} tập trung vào số ít ca lớn`,
    ev:`${svcTop.group} = ${Math.round(svcTop.revenue/totRev*100)}% doanh thu, Top20% ca chiếm ${svcTop.top_share}%`,
    act:`Theo dõi rủi ro phụ thuộc; mở rộng tệp khách nhóm ${svcTop.group}`,owner:'CEO',
    exp:'Giảm rủi ro doanh thu phụ thuộc vài ca lớn'});

  // I. BÁO ĐỘNG ĐỎ division: chi quảng cáo ≥ doanh thu (ROAS thấp) + chậm xa nhịp target
  const DV=DATA.divisions;
  if(DV&&DV.items){const pace=DV.month_days?DV.days_elapsed/DV.month_days*100:0;
    DV.items.forEach(d=>{
      const hasAd=d.ad_spend>0, roas=hasAd?d.revenue/d.ad_spend:null;
      const adOverRev=hasAd&&d.revenue>0&&roas<1.2;
      const behind=d.pct_projected!=null&&d.pct_projected<pace*0.6;   // dự phóng < 60% nhịp đáng lẽ phải đạt
      if(adOverRev&&behind){
        add({page:'overview',sev:3,impact:Math.max(0,d.ad_spend-d.revenue),division:d.name,
          title:`${d.name}: chi quảng cáo vượt doanh thu, chậm xa target tháng`,
          ev:`Ad ${tr(d.ad_spend)} ${roas<1?'>':'≈'} DT ${tr(d.revenue)} (ROAS ${roas.toFixed(1)}x) · mới ${d.pct_target}% target ${tyS(d.target_month)}, dự phóng cuối tháng chỉ ${d.pct_projected}% trong khi đã qua ${Math.round(pace)}% số ngày`,
          act:`Soát từng ad ${d.name}: cắt ad không/ít ra ca, xem lại định giá & tỉ lệ chốt ca; cân nhắc giảm ngân sách tới khi ROAS>1 — đang lỗ ad ~${tr(Math.max(0,d.ad_spend-d.revenue))} kỳ này`,
          owner:'CEO + Ads',exp:`Chặn lỗ quảng cáo và kéo ${d.name} về nhịp target ${tyS(d.target_month)}`});
      }
    });
  }

  return ins;
}

function memo(){
  const comp=COMPLETE;
  if(comp.length<2) return '<div class="card"><div class="note">Chưa đủ dữ liệu (cần ít nhất 2 ngày đã chốt) để tạo bản tin.</div></div>';
  const yday=comp[comp.length-1], prev=comp[comp.length-2];
  const base=comp.slice(Math.max(0,comp.length-8),comp.length-1);
  const base3=comp.slice(Math.max(0,comp.length-4),comp.length-1);
  const M=winSlice('mtd');
  const sum=(a,f)=>a.reduce((s,x)=>s+f(x),0), avg=(a,f)=>a.length?sum(a,f)/a.length:0;
  const baseAvg=f=>avg(base,f), baseAvg3=f=>avg(base3,f);
  const roasOf=a=>{const sp=sum(a,s=>s.spend);return sp?sum(a,s=>s.revenue)/sp:0;};
  const cplOf=a=>{const m=sum(a,s=>s.meta_msg+s.tk_msg);return m?sum(a,s=>s.spend)/m:0;};
  const aovOf=a=>{const p=sum(a,s=>s.paying);return p?sum(a,s=>s.revenue)/p:0;};
  const attachOf=a=>{const b=sum(a,s=>s.bills_total);return b?sum(a,s=>s.bills_multi)/b*100:0;};
  const adrevOf=a=>{const r=sum(a,s=>s.revenue);return r?sum(a,s=>s.spend)/r*100:0;};
  const zeroOf=a=>{const c=sum(a,s=>s.customers);return c?sum(a,s=>s.zero)/c*100:0;};
  const medOf=a=>{const v=a.flatMap(s=>s.bill_values||[]);return v.length?median(v):0;};
  const dOf=(y,b)=>b?(y-b)/b:0;
  const pc=d=>(d>=0?'+':'')+Math.round(d*100)+'%';
  const dcls=(g,d)=>{if(g===0||!isFinite(d)||d===0)return 'dmut';const f=g>0?d:-d;return f>=0.05?'dpos':(f<=-0.2?'dneg':'dwarn');};
  const ds=(g,d)=>`<span class="${dcls(g,d)}">${pc(d)}</span>`;

  // ---- deltas ----
  const dRev=dOf(yday.revenue,baseAvg(s=>s.revenue)), dSpend=dOf(yday.spend,baseAvg(s=>s.spend));
  const dRoas=dOf(roasOf([yday]),roasOf(base)), dCpl=dOf(cplOf([yday]),cplOf(base));
  const dZero=dOf(zeroOf([yday]),zeroOf(base)), dAtt=dOf(attachOf([yday]),attachOf(base)), dMed=dOf(medOf([yday]),medOf(base));

  // ---- what changed ----
  const changes=[]; const addc=(l,d,g,m)=>{if(isFinite(d)&&Math.abs(d)>=0.15)changes.push({l,d,g,m});};
  addc('Doanh thu hoàn tất',dRev,1,dRev>0?'Doanh thu hôm qua cao hơn nền 7 ngày':'Doanh thu hụt so với nền 7 ngày');
  DATA.services.filter(s=>s.revenue>0).forEach(s=>{const bv=baseAvg(d=>d.rev_by_service[s.group]||0);const dd=dOf(yday.rev_by_service[s.group]||0,bv);if(bv>20e6)addc('Doanh thu '+s.group,dd,1,(dd>0?s.group+' tăng mạnh':s.group+' giảm')+' so với nền');});
  addc('CPL',dCpl,-1,dCpl>0?'Chi phí mỗi lead tăng — soát ads/creative':'CPL giảm — quảng cáo hiệu quả hơn');
  addc('Tỉ lệ khách 0đ',dZero,0,dZero>0?'0đ tăng — kiểm tra (tái khám tăng hay chốt yếu?)':'0đ giảm');
  addc('Attach rate',dAtt,1,dAtt>0?'Bán chéo tốt hơn nền':'Bán chéo hôm qua kém hơn nền');
  addc('Median bill',dMed,1,dMed>0?'Bill điển hình lớn hơn':'Bill nhỏ hơn — doanh thu có thể đến từ volume');
  changes.sort((a,b)=>Math.abs(b.d)-Math.abs(a.d)); const top=changes.slice(0,5);

  // ---- alerts ----
  const al=[]; const dq=DATA.dataquality;
  // Báo động cấp tháng theo division: chi ad ≥ doanh thu + chậm xa nhịp target
  const DVm=DATA.divisions;
  if(DVm&&DVm.items){const pace=DVm.month_days?DVm.days_elapsed/DVm.month_days*100:0;
    DVm.items.forEach(d=>{const roas=d.ad_spend>0?d.revenue/d.ad_spend:null;
      if(roas!=null&&roas<1.2&&d.revenue>0&&d.pct_projected!=null&&d.pct_projected<pace*0.6)
        al.push(['red',`${d.name}: chi quảng cáo ${tr(d.ad_spend)} ${roas<1?'vượt':'≈'} doanh thu ${tr(d.revenue)} (ROAS ${roas.toFixed(1)}x) — mới ${d.pct_target}% target ${tyS(d.target_month)} dù đã qua ${Math.round(pace)}% tháng. Báo động đỏ: soát từng ad & định giá/tỉ lệ chốt ca, cân nhắc giảm ngân sách tới khi ROAS>1.`]);
    });
  }
  if(dRev<-0.20)al.push(['red','Doanh thu hôm qua thấp hơn nền 7 ngày '+pc(dRev)]);
  if(dSpend>0.15&&dRev<dSpend)al.push(['amber','Chi ads tăng '+pc(dSpend)+' nhưng doanh thu '+pc(dRev)+' — hiệu quả giảm']);
  if(dCpl>0.25)al.push(['amber','CPL tăng '+pc(dCpl)+' so với nền 7 ngày']);
  if(dRoas<-0.25)al.push(['red','ROAS giảm '+pc(dRoas)+' so với nền 7 ngày']);
  if(dZero>0.30)al.push(['amber','Tỉ lệ khách 0đ tăng '+pc(dZero)+' — kiểm tra (tái khám tăng hay khâu chốt yếu?)']);
  if(dAtt<-0.20)al.push(['amber','Attach rate giảm '+pc(dAtt)+' — bán chéo yếu']);
  if(STALE)al.push(['red','Dữ liệu chưa cập nhật tới hôm nay (mới nhất '+dlabel(LATEST_DATA)+')']);
  if(dq.meta_unmapped_pct>12||dq.tk_unmapped_pct>12||dq.rev_unmapped_pct>12)al.push(['amber','Tỉ lệ chưa map dịch vụ cao — kiểm tra đặt tên QC / cột dịch vụ']);

  // ---- actions ----
  // action queue = top 3-5 insight toàn dashboard, xếp theo mức độ × tác động
  const acts=getInsights().slice().sort((a,b)=>scr(b)-scr(a)).slice(0,5);
  const topSvc=DATA.services.filter(s=>s.ad_spend>0&&s.revenue>0).sort((a,b)=>b.revenue-a.revenue)[0];

  // ---- exec summary ----
  const pos=top.find(c=>(c.g>0?c.d>0:c.d<0)), neg=top.find(c=>(c.g>0?c.d<0:c.d>0));
  const exec=`Hôm qua (${dlabel(yday.date)}) doanh thu hoàn tất <b>${tr(yday.revenue)}</b> (${ds(1,dRev)} so với nền 7 ngày), chi ads <b>${tr(yday.spend)}</b>, ROAS <b>${roasOf([yday]).toFixed(1)}x</b>, ${yday.paying} khách có doanh thu. `
    +(pos?`Điểm tích cực: ${pos.l.toLowerCase()} ${pc(pos.d)}. `:'')+(neg?`Điểm cần chú ý: ${neg.l.toLowerCase()} ${pc(neg.d)}. `:'')
    +(acts.length?`Hôm nay nên: ${acts[0].act.toLowerCase()}${acts[1]?'; '+acts[1].act.toLowerCase():''}.`:'');

  // ---- BLOCKS ----
  const link=(p,t)=>`<button class="seemore" onclick="show('${p}')">${t} →</button>`;
  // data status
  const allLatest=[dq.latest_revenue,dq.latest_meta,dq.latest_tiktok].sort()[0];
  const dataStatus=(allLatest>=yday.date)?['ok','Complete — đủ dữ liệu cho hôm qua']:(STALE?['red','Partial — một nguồn chưa cập nhật']:['amber','Partial']);
  const header=`<div class="card"><div class="cardhd"><h2>Bản tin cho ngày ${dlabel(DATA.system_today)}/${DATA.system_today.slice(0,4)}</h2>
    <span class="dqchip ${dataStatus[0]==='ok'?'ok':'warn'}">${dataStatus[1]}</span></div>
    <div class="dqbar" style="margin-top:6px">
      <span class="dqchip">Doanh thu: ${dlabel(dq.latest_revenue)}</span><span class="dqchip">Meta: ${dlabel(dq.latest_meta)}</span>
      <span class="dqchip">TikTok: ${dlabel(dq.latest_tiktok)}</span><span class="dqchip">Tạo lúc: ${dq.generated_at}</span></div></div>`;
  const execCard=`<div class="card memo"><div class="tier">Đọc nhanh 30 giây</div><h3 style="margin-top:0">Tóm tắt điều hành</h3><div class="head">${exec}</div></div>`;
  const alertCard=`<div class="card"><div class="tier">Cảnh báo</div><h2 style="margin-bottom:10px">Cảnh báo & bất thường</h2>${al.length?al.map(a=>`<div class="alertbox ${a[0]}">⚠ ${a[1]}</div>`).join(''):'<div class="alertbox ok">✓ Không có cảnh báo bất thường so với nền 7 ngày.</div>'}</div>`;
  const actCard=`<div class="card"><div class="tier">Việc hôm nay</div><h2 style="margin-bottom:2px">Danh sách hành động hôm nay</h2><div class="h-en" style="margin-bottom:10px">Top ${acts.length} việc ưu tiên tổng hợp từ insight các trang · là giả thuyết cần kiểm chứng, không tự động thực thi</div>
    ${acts.map(a=>{const pr=a.sev>=3?'P1':'P2';return `<div class="actrow"><span class="pr ${pr}">${pr}</span><div><b>${a.act}</b> <span style="color:var(--ink-soft)">· ${a.owner}</span><div style="font-size:12.5px;color:var(--ink-soft);margin-top:2px">${a.ev} → ${a.exp}</div></div></div>`;}).join('')||'<div class="note" style="margin:0">Không có hành động ưu tiên — duy trì vận hành hiện tại.</div>'}</div>`;

  // business pulse
  const spd=COMPLETE.slice(-30);
  const sd2=d=>d.slice(8,10)+'/'+d.slice(5,7);
  const spdLbl=spd.length?`Xu hướng ${sd2(spd[0].date)}–${sd2(spd[spd.length-1].date)} · ${spd.length} ngày đã chốt`:'';
  const pulse=[
    {k:'Doanh thu hoàn tất',g:1,f:tr,y:yday.revenue,p:prev.revenue,b:baseAvg(s=>s.revenue),b3:baseAvg3(s=>s.revenue),m:sum(M,s=>s.revenue),sf:s=>s.revenue},
    {k:'Tiền cọc / pipeline',g:0,f:tr,y:yday.deposit,p:prev.deposit,b:baseAvg(s=>s.deposit),b3:baseAvg3(s=>s.deposit),m:sum(M,s=>s.deposit),sf:s=>s.deposit},
    {k:'Cash-in',g:1,f:tr,y:yday.cash_in,p:prev.cash_in,b:baseAvg(s=>s.cash_in),b3:baseAvg3(s=>s.cash_in),m:sum(M,s=>s.cash_in),sf:s=>s.cash_in},
    {k:'Chi ads',g:0,f:tr,y:yday.spend,p:prev.spend,b:baseAvg(s=>s.spend),b3:baseAvg3(s=>s.spend),m:sum(M,s=>s.spend),sf:s=>s.spend},
    {k:'ROAS doanh thu thật',g:1,f:x=>x.toFixed(1)+'x',y:roasOf([yday]),p:roasOf([prev]),b:roasOf(base),b3:roasOf(base3),m:roasOf(M),sf:s=>roasOf([s])},
    {k:'Ad cost / revenue',g:-1,f:x=>x.toFixed(0)+'%',y:adrevOf([yday]),p:adrevOf([prev]),b:adrevOf(base),b3:adrevOf(base3),m:adrevOf(M),sf:s=>adrevOf([s])},
    {k:'Tin nhắn / lead',g:1,f:x=>Math.round(x),y:yday.meta_msg+yday.tk_msg,p:prev.meta_msg+prev.tk_msg,b:baseAvg(s=>s.meta_msg+s.tk_msg),b3:baseAvg3(s=>s.meta_msg+s.tk_msg),m:sum(M,s=>s.meta_msg+s.tk_msg),sf:s=>s.meta_msg+s.tk_msg},
    {k:'CPL',g:-1,f:k,y:cplOf([yday]),p:cplOf([prev]),b:cplOf(base),b3:cplOf(base3),m:cplOf(M),sf:s=>cplOf([s])},
    {k:'Khách có doanh thu',g:1,f:x=>Math.round(x),y:yday.paying,p:prev.paying,b:baseAvg(s=>s.paying),b3:baseAvg3(s=>s.paying),m:sum(M,s=>s.paying),sf:s=>s.paying},
    {k:'Khách cọc',g:0,f:x=>Math.round(x),y:yday.coc,p:prev.coc,b:baseAvg(s=>s.coc),b3:baseAvg3(s=>s.coc),m:sum(M,s=>s.coc),sf:s=>s.coc},
    {k:'Khách 0đ',g:0,f:x=>Math.round(x),y:yday.zero,p:prev.zero,b:baseAvg(s=>s.zero),b3:baseAvg3(s=>s.zero),m:sum(M,s=>s.zero),sf:s=>s.zero},
    {k:'AOV',g:1,f:tr,y:aovOf([yday]),p:aovOf([prev]),b:aovOf(base),b3:aovOf(base3),m:aovOf(M),sf:s=>aovOf([s])},
    {k:'Median bill',g:1,f:tr,y:medOf([yday]),p:medOf([prev]),b:medOf(base),b3:medOf(base3),m:medOf(M),sf:s=>medOf([s])},
    {k:'Attach rate',g:1,f:x=>x.toFixed(1)+'%',y:attachOf([yday]),p:attachOf([prev]),b:attachOf(base),b3:attachOf(base3),m:attachOf(M),sf:s=>attachOf([s])},
  ];
  const pulseTbl=pulse.map(r=>`<tr><td>${r.k}</td><td>${r.f(r.y)}</td><td>${r.p?ds(r.g,dOf(r.y,r.p)):'—'}</td><td>${r.b3?ds(r.g,dOf(r.y,r.b3)):'—'}</td><td>${r.b?ds(r.g,dOf(r.y,r.b)):'—'}</td><td class="mtd"><b>${r.f(r.m)}</b></td><td>${spark(spd.map(r.sf),'tspark',r.g,spdLbl)}</td></tr>`).join('');
  const pulseCard=`<div class="card svctbl"><div class="tier">Đọc trong 3 phút</div><h2>Nhịp tim kinh doanh</h2><div class="h-en">Hôm qua so với hôm trước · nền 7 ngày · cả tháng</div>
    <table><thead><tr><th>Chỉ số</th><th>Hôm qua</th><th>vs hôm trước</th><th>vs 3 ngày</th><th>vs 7 ngày</th><th>MTD</th><th>Xu hướng</th></tr></thead><tbody>${pulseTbl}</tbody></table>
    <div class="note" style="margin-top:10px;color:var(--ink-soft)"><span class="dpos">Xanh</span> tốt hơn nền · <span class="dwarn">vàng</span> lệch nhẹ · <span class="dneg">đỏ</span> lệch mạnh. So với nền 7 ngày đáng tin hơn so với hôm trước (đỡ nhiễu).</div></div>`;

  // what changed
  const chgCard=`<div class="card"><h2>Thay đổi đáng kể hôm qua</h2><div class="h-en">Tự động phát hiện các thay đổi lớn nhất so với nền 7 ngày</div>
    ${top.length?top.map(c=>`<div class="actrow"><span class="${dcls(c.g,c.d)}" style="min-width:54px;font-size:15px">${pc(c.d)}</span><div><b>${c.l}</b><div style="font-size:12.5px;color:var(--ink-soft)">${c.m}</div></div></div>`).join(''):'<div class="note" style="margin:0">Không có thay đổi đáng kể (mọi chỉ số dao động trong khoảng bình thường).</div>'}</div>`;

  // ads memo
  const m_=DATA.platform.meta,t_=DATA.platform_extra,tk=DATA.platform.tiktok;
  const yMsg=yday.meta_msg+yday.tk_msg;
  const adsCard=`<div class="card svctbl"><div class="cardhd"><h2>Quảng cáo & nền tảng</h2>${link('platform','Trang Nền tảng')}</div><div class="h-en">Hôm qua · và khuyến nghị ngân sách</div>
    <table><thead><tr><th>Chỉ số</th><th>Meta</th><th>TikTok</th></tr></thead><tbody>
      <tr><td>Chi (hôm qua)</td><td>${tr(yday.meta_spend)}</td><td>${tr(yday.tk_spend)}</td></tr>
      <tr><td>Tin nhắn (hôm qua)</td><td>${yday.meta_msg}</td><td>${yday.tk_msg}</td></tr>
      <tr><td>CPL lead mới (kỳ)</td><td>${m_.cpl_lead?k(m_.cpl_lead):'—'}</td><td>${tk.cpl_lead?k(tk.cpl_lead):'—'}</td></tr>
      <tr><td>Dịch vụ mạnh nhất</td><td>${m_.spend_by_service[0]?m_.spend_by_service[0].group:'—'}</td><td>${tk.spend_by_service[0]?tk.spend_by_service[0].group:'—'}</td></tr>
    </tbody></table>
    <div class="note" style="margin-top:10px"><b>Khuyến nghị:</b> ${topSvc?'Giữ ngân sách <b>'+topSvc.group+'</b> (proxy-ROAS '+topSvc.proxy_roas+'x). ':''}Top 20% ad tạo ${t_.winner_pct}% lead; spend lãng phí ~${tr(t_.waste_spend)} cần cắt. CPL ${dCpl>0.1?'<span class="dneg">đang tăng '+pc(dCpl)+'</span> — theo dõi creative':'ổn định so với nền'}.</div></div>`;

  // revenue/service memo
  const svcRows=DATA.services.map(s=>{const y=yday.rev_by_service[s.group]||0;const yd=yday.deposit_by_service[s.group]||0;const bv=baseAvg(d=>d.rev_by_service[s.group]||0);
    const pipeOnly=s.revenue===0&&(s.deposit||0)>0;
    return `<tr><td><b>${s.group}</b></td><td>${pipeOnly?'<span class="dmut">cọc</span>':tr(y)}</td><td>${yd?tr(yd):'—'}</td><td>${bv?ds(1,dOf(y,bv)):'—'}</td><td>${pipeOnly?'Chỉ pipeline (cọc), chưa phải DT thật':(y>=bv?'Trên nền':'Dưới nền')}</td></tr>`;}).join('');
  const svcCard=`<div class="card svctbl"><div class="cardhd"><h2>Doanh thu theo dịch vụ (hôm qua)</h2>${link('service','Trang Dịch vụ')}</div><div class="h-en">Tách doanh thu hoàn tất vs cọc/pipeline</div>
    <table><thead><tr><th>Dịch vụ</th><th>DT hoàn tất</th><th>Cọc</th><th>vs 7 ngày</th><th>Nhận xét</th></tr></thead><tbody>${svcRows}</tbody></table></div>`;

  // people memo
  const S=DATA.sales.filter(s=>s.customers>=2&&!/CSKH|ONLINE|TRỰC TIẾP|TRUC TIEP/i.test(s.name||'')), MA=DATA.masters.filter(m=>m.customers>=2);
  const by=(arr,f)=>arr.slice().sort((a,b)=>f(b)-f(a))[0];
  const topSaleRev=by(S,s=>s.revenue),topSalePaid=by(S,s=>s.paid_rate),topSaleAtt=by(S,s=>s.attach),hiZeroSale=by(S,s=>s.zero_pct),hiCocSale=by(S,s=>s.coc);
  const mdays=DATA.series.filter(d=>d.date.slice(0,7)===TODAY_DATE.slice(0,7)).length||DATA.series.length;
  const topSalePD=by(S,s=>s.paying); const pdv=s=>(s.paying/mdays).toFixed(1);
  const topMastVI=by(MA.filter(m=>m.value_index!=null),m=>m.value_index),loMastVI=MA.filter(m=>m.value_index!=null).slice().sort((a,b)=>a.value_index-b.value_index)[0],topMastAtt=by(MA,m=>m.attach),hiZeroMast=by(MA,m=>m.zero_pct);
  const stS=S.filter(s=>s.paying_cv!=null&&(s.paying/mdays)>=1).slice().sort((a,b)=>a.paying_cv-b.paying_cv);
  const mostStable=stS[0], leastStable=stS[stS.length-1];
  const tkM=MA.filter(m=>m.tk>=3).map(m=>({m,r:m.tk_paid/m.tk})).sort((a,b)=>b.r-a.r);
  const bestTK=tkM[0], worstTK=tkM[tkM.length-1];
  const peopleCard=`<div class="grid2" style="grid-template-columns:1fr 1fr">
    <div class="card"><div class="cardhd"><h2>Sale nổi bật</h2>${link('sales','Trang Sale')}</div>
      <ul class="memo" style="margin-top:4px">
        <li style="font-weight:700"><span style="color:var(--jade)">★ Năng suất khách DT/ngày:</span> ${topSalePD.name} — ${pdv(topSalePD)} khách/ngày</li>
        ${mostStable?`<li>Ổn định nhất (đều mỗi ngày): <b>${mostStable.name}</b> (CV ${mostStable.paying_cv}%)</li>`:''}
        ${leastStable&&leastStable!==mostStable&&leastStable.paying_cv>100?`<li>Cần xem (dao động mạnh): <b>${leastStable.name}</b> (CV ${leastStable.paying_cv}%)</li>`:''}
        <li>Doanh thu cao nhất: <b>${topSaleRev.name}</b> (${tr(topSaleRev.revenue)})</li>
        <li>Chốt tốt nhất: <b>${topSalePaid.name}</b> (% trả tiền ${topSalePaid.paid_rate}%)</li>
        <li>Bán chéo tốt: <b>${topSaleAtt.name}</b> (attach ${topSaleAtt.attach}%)</li>
        <li>Nhiều cọc cần follow-up: <b>${hiCocSale.name}</b> (${hiCocSale.coc} cọc)</li>
      </ul></div>
    <div class="card"><div class="cardhd"><h2>Master nổi bật</h2>${link('master','Trang Master')}</div>
      <ul class="memo" style="margin-top:4px">
        <li>Chỉ số DT kỳ vọng cao: <b>${topMastVI.name}</b> (${topMastVI.value_index})</li>
        ${bestTK?`<li>Chuyển khám→DT tốt: <b>${bestTK.m.name}</b> (${Math.round(bestTK.r*100)}% · ${bestTK.m.tk_paid}/${bestTK.m.tk})</li>`:''}
        ${worstTK&&worstTK!==bestTK&&worstTK.r<0.4?`<li>Cần chú ý (chuyển khám→DT thấp): <b>${worstTK.m.name}</b> (${Math.round(worstTK.r*100)}% · ${worstTK.m.tk_paid}/${worstTK.m.tk})</li>`:''}
        <li>Bán chéo tốt: <b>${topMastAtt.name}</b> (attach ${topMastAtt.attach}%)</li>
        ${loMastVI&&loMastVI.value_index<0.9?`<li>Cần coaching (Chỉ số DT kỳ vọng): <b>${loMastVI.name}</b> (${loMastVI.value_index})</li>`:''}
      </ul></div></div>`;

  // cross-sell memo
  const x=DATA.crosssell, bestPair=(x.pairs||[])[0];
  const xCard=`<div class="card svctbl"><div class="cardhd"><h2>Bán chéo</h2>${link('cross','Trang Bán chéo')}</div><div class="h-en">Hôm qua có khai thác thêm giá trị khách không</div>
    <table><thead><tr><th>Chỉ số</th><th>Hôm qua / kỳ</th><th>vs 7 ngày</th></tr></thead><tbody>
      <tr><td>Attach rate</td><td>${attachOf([yday]).toFixed(1)}%</td><td>${ds(1,dAtt)}</td></tr>
      <tr><td>Số bill bán chéo (hôm qua)</td><td>${yday.bills_multi}</td><td>—</td></tr>
      <tr><td>AOV bill bán chéo (kỳ)</td><td>${tr(x.aov_xsell)}</td><td>—</td></tr>
      <tr><td>AOV bill thường (kỳ)</td><td>${tr(x.aov_nonxsell)}</td><td>—</td></tr>
      <tr><td>Uplift</td><td>+${x.uplift}%</td><td>—</td></tr>
    </tbody></table>
    <div class="note" style="margin-top:10px">${bestPair?'Cặp mạnh nhất kỳ này: <b>'+bestPair.main+' + '+bestPair.attach+'</b> ('+bestPair.bills+' bill). ':''}${dAtt<-0.1?'Attach hôm qua dưới nền — nên đẩy script bán chéo.':'Bán chéo vẫn có tác dụng (uplift +'+x.uplift+'%) — duy trì nhắc đội ngũ.'}</div></div>`;

  return header+execCard+alertCard+actCard+pulseCard+chgCard+adsCard+svcCard+peopleCard+xCard;
}

const R={overview,division,service,platform,sales,master,cross,memo};
function division(){
  const D=DATA.divisions;
  if(!D||!D.items||!D.items.length) return '<div class="card"><h2>Chưa có dữ liệu division</h2><div class="note" style="margin-top:8px">Cần phân loại dịch vụ theo division trong pipeline.</div></div>';
  const items=D.items;
  const totRev=items.reduce((a,d)=>a+d.revenue,0)+(D.unclassified_rev||0)||1;
  const card=d=>{
    const isN=d.name.includes('Ngoại'); const cls=isN?'ngoai':'noi';
    const share=Math.round(d.revenue/totRev*100);
    const pj=d.pct_projected, pill=pj>=100?'ok':pj>=80?'behind':'bad', pjlab=pj>=100?'Đúng/vượt nhịp':pj>=80?'Hơi chậm nhịp':'Chậm nhịp';
    const m=(l,v)=>`<div class="dv-m"><div class="l">${l}</div><div class="v">${v}</div></div>`;
    const maxsvc=Math.max(1,...d.services.map(s=>s.revenue));
    const svc=d.services.length?d.services.map(s=>`<div class="sr"><span class="sn">${s.group}</span><span class="st"><span class="sf" style="width:${Math.round(s.revenue/maxsvc*100)}%"></span></span><span class="sv">${tr(s.revenue)}</span></div>`).join(''):'<div class="dv-tcap">Chưa có doanh thu hoàn tất nhóm này trong kỳ — phần lớn còn nằm ở cọc, sẽ hiện khi ghép cọc→thực hiện.</div>';
    return `<div class="dvcard ${cls}">
      <div class="dv-h"><div><div class="dv-name">${d.name}</div><div class="dv-grp">${d.groups.join(' \u00B7 ')}</div></div><div class="dv-share">${share}% tổng DT</div></div>
      <div class="dv-hero"><div class="dv-pct">${d.pct_target}%<small> target tháng</small></div>
        <div class="dv-tcap">${tyS(d.revenue)} / ${tyS(d.target_month)} \u00B7 đã qua ${D.days_elapsed}/${D.month_days} ngày</div>
        <div class="dv-track"><div class="dv-fill fill" style="width:${Math.min(100,d.pct_target)}%"></div></div>
        <div class="dv-proj"><span class="dv-pill ${pill}">${pjlab}</span><span>Dự phóng cuối tháng: <b style="color:var(--ink)">${tyS(d.projected_month)}</b> (${d.pct_projected}% target)</span></div></div>
      <div class="dv-metrics">${m('Khách',d.customers)}${m('AOV',d.aov?tr(d.aov):'\u2014')}${m('Trung vị',d.median?tr(d.median):'\u2014')}${m('P90',d.p90?tr(d.p90):'\u2014')}${m('Cọc/pipeline',d.deposit?tr(d.deposit):'\u2014')}${m('Ad \u00B7 ROAS',d.ad_spend?`${tr(d.ad_spend)} \u00B7 ${d.roas}x`:'0 \u00B7 \u2014')}</div>
      <div class="dv-svc"><div class="dv-grp" style="margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;font-weight:700">Doanh thu theo nhóm</div>${svc}</div></div>`;
  };
  const noi=items.find(d=>!d.name.includes('Ngoại'))||items[0];
  const ng=items.find(d=>d.name.includes('Ngoại'))||items[1]||{revenue:0};
  const base=(noi.revenue+ng.revenue)||1; const noiPct=Math.round(noi.revenue/base*100);
  return `
  <div class="card" style="padding:20px 22px">
    <h2>Đóng góp doanh thu theo division (tháng này)</h2><div class="h-en">Nội khoa vs Ngoại khoa \u2014 theo doanh thu hoàn tất đã chốt</div>
    <div class="dv-bar"><div class="seg n" style="width:${noiPct}%"></div><div class="seg g" style="width:${100-noiPct}%"></div></div>
    <div class="dv-leg"><span><i class="d n"></i>Nội khoa <b>${noiPct}%</b> \u00B7 ${tyS(noi.revenue)}</span><span><i class="d g"></i>Ngoại khoa <b>${100-noiPct}%</b> \u00B7 ${tyS(ng.revenue)}</span></div>
    <div class="note" style="margin-top:12px">${[D.note_ad,D.note_pipeline].filter(Boolean).join(' \u00B7 ')}</div>
  </div>
  <div class="dvgrid">${items.map(card).join('')}</div>`;
}
function show(p){
  window.__page=p;
  document.querySelectorAll('.nav button').forEach(b=>b.classList.toggle('active',b.dataset.p===p));
  const db=document.getElementById('divbar'); if(db){db.style.display=DIVPAGES.includes(p)?'flex':'none';
    db.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.d===DIVFILTER));}
  document.querySelectorAll('.page').forEach(s=>s.classList.remove('active'));
  const el=document.getElementById(p); el.innerHTML=R[p](); el.classList.add('active');
  document.getElementById('ptitle').textContent=titles[p][0];
  document.getElementById('psub').textContent=titles[p][1];
  hideTip();
  if(p==='overview'){ VIEW=winSlice('mtd'); GVIEW=winSlice('mtd'); if(!GVIEW.length)GVIEW=winSlice('mtd'); renderChart(); renderGates(); }
  // animate bars
  requestAnimationFrame(()=>document.querySelectorAll('.bar,.fill').forEach(b=>{
    const h=b.style.height,w=b.style.width;
    if(h){b.style.height='0';requestAnimationFrame(()=>b.style.height=h);}
    if(w){const ww=w;b.style.width='0';requestAnimationFrame(()=>b.style.width=ww);}
  }));
}
document.getElementById('nav').addEventListener('click',e=>{const b=e.target.closest('button');if(b)show(b.dataset.p);});
function fmtDate(d){if(!d)return '—';const[y,m,dd]=d.split('-');return dd+'/'+m;}
function updateStatus(){
  const el=document.getElementById('statuspill'); if(!el)return;
  const dq=DATA.dataquality||{};
  const t=new Date().toLocaleTimeString('vi-VN');
  if(STALE){
    el.style.background='var(--rose-soft)'; el.style.color='var(--rose)';
    el.querySelector('.led').style.background='var(--rose)';
    el.childNodes[1].nodeValue=' Dữ liệu chưa tới hôm nay — mới nhất '+fmtDate(LATEST_DATA)+' · kiểm tra '+t;
  } else {
    el.style.background=''; el.style.color=''; el.querySelector('.led').style.background='';
    el.childNodes[1].nodeValue=' Dữ liệu tới '+fmtDate(LATEST_DATA)+' · cập nhật '+(dq.generated_at||'')+' · kiểm tra '+t;
  }
}
// Tự refresh: thử nạp data.json mỗi 45s; nếu pipeline ghi dữ liệu mới (generated_at đổi) thì cập nhật + vẽ lại.
// Bản xem trước chạy bằng file:// sẽ fetch lỗi → giữ nguyên dữ liệu nhúng sẵn.
function refreshData(){
  fetch('data.json?t='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():null).then(j=>{
    if(j&&j.dataquality&&j.dataquality.generated_at!==(DATA.dataquality||{}).generated_at){
      DATA=j; deriveGlobals(); show(window.__page||'overview'); updateStatus();
    } else { updateStatus(); }
  }).catch(()=>{});
}
show('overview');
updateStatus();
refreshData();
setInterval(refreshData,45000);
</script>
</body>
</html>'''

html = HTML.replace('__DATA__', DATA_JSON)
html = html.replace('<table>', '<div class="tscroll"><table>').replace('</table>', '</table></div>')
import os as _os
_outdir = _os.environ.get('SWAN_OUTPUT_DIR', '/mnt/user-data/outputs')
_os.makedirs(_outdir, exist_ok=True)
open(_os.path.join(_outdir,'swan_ceo_dashboard.html'),'w',encoding='utf-8').write(html)
# Ghi kèm data.json để dashboard tự refresh (fetch mỗi 45s) mà không cần build lại HTML
open(_os.path.join(_outdir,'data.json'),'w',encoding='utf-8').write(DATA_JSON)
print('dashboard written:', len(html), 'bytes ->', _outdir)
