"""
Swan Clinic dashboard — cổng đăng nhập + phân quyền theo trang (GĐ1).

Đặt trước dashboard tĩnh. nginx proxy /swan/ -> app này (127.0.0.1:8200).
- Phục vụ dashboard.html (đã chèn lớp ẩn trang theo vai trò)
- /data.json trả bundle ĐÃ LỌC theo vai trò (xóa rỗng key của trang bị cấm => không rò rỉ kể cả tải thẳng)
- Login bằng session ký (cookie), mỗi nhân viên 1 tài khoản
- Đổi mật khẩu khi đã đăng nhập

GĐ2 (sau): lọc theo chiều dữ liệu Nội/Ngoại + ads theo account — đã chừa sẵn móc `data_scope`.
"""
import os, json, hmac, hashlib, secrets, copy, base64
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse, Response
from starlette.middleware.sessions import SessionMiddleware

_APPDIR = Path(__file__).resolve().parent
def _load_fav(name):
    p = _APPDIR / name
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""
FAV64  = _load_fav("favicon-64.png")
FAV180 = _load_fav("favicon-180.png")
FAV_SVG = _load_fav("favicon.svg")     # SVG tự đổi màu theo nền (đen ở nền sáng, trắng ở nền tối)
def _fav_tags():
    t = ""
    if FAV_SVG: t += '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,%s">' % FAV_SVG
    if FAV64:   t += '<link rel="icon" type="image/png" sizes="64x64" href="data:image/png;base64,%s">' % FAV64
    if FAV180:  t += '<link rel="apple-touch-icon" href="data:image/png;base64,%s">' % FAV180
    return t
FAV_TAGS = _fav_tags()

# ----------------------------------------------------------------------------
# Cấu hình (đổi qua biến môi trường khi deploy)
# ----------------------------------------------------------------------------
WEB_DIR   = Path(os.environ.get("SWAN_WEB_DIR", "/var/www/swan"))      # nơi pipeline ghi data.json + dashboard.html
DASH_FILE = Path(os.environ.get("SWAN_DASH", str(WEB_DIR / "dashboard.html")))
BUNDLE    = Path(os.environ.get("SWAN_BUNDLE", str(WEB_DIR / "data.json")))
USERS_FILE= Path(os.environ.get("SWAN_USERS", "/etc/swan/users.json"))
SECRET_FILE=Path(os.environ.get("SWAN_SECRET", "/etc/swan/secret"))

def _secret():
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text().strip()
    return os.environ.get("SWAN_SESSION_SECRET", "dev-secret-change-me")

# ----------------------------------------------------------------------------
# Vai trò -> trang được xem (data-p trong dashboard)
# ----------------------------------------------------------------------------
ALL_PAGES = ["overview","division","service","platform","sales","master","cross","memo"]
ROLE_PAGES = {
    "ceo":       ALL_PAGES,                                                  # Trung, Thanh
    "ops":       ["overview","division","service","platform","sales","master","cross"],  # vận hành / CFO / nhân sự
    "noi":       ["overview","division","service","platform","sales","master","cross"],  # QL nội khoa  (GĐ2: data Nội)
    "ngoai":     ["overview","division","service","platform","sales","master","cross"],  # QL ngoại khoa(GĐ2: data Ngoại)
    "noi_ads":   ["overview","division","service","platform","sales","master","cross"],  # Vương Ngân (GĐ2: Nội + full ads)
    "ads":       ["platform"],                                              # QL ads
    "marketing": ["overview","platform"],                                   # QL marketing
}
ROLE_LABEL = {
    "ceo":"CEO","ops":"Quản lý vận hành","noi":"QL Nội khoa","ngoai":"QL Ngoại khoa",
    "noi_ads":"QL Nội khoa + Ads","ads":"QL Ads","marketing":"QL Marketing",
}
# GĐ2 — chiều dữ liệu mỗi vai trò (đã chừa sẵn, GĐ1 chưa áp dụng)
DATA_SCOPE = {  # division=None => toàn bộ; ads='full' => xem mọi quảng cáo dù division bị giới hạn
    "ceo":{"division":None,"ads":"full"}, "ops":{"division":None,"ads":"full"},
    "noi":{"division":"Nội khoa","ads":"div"}, "ngoai":{"division":"Ngoại khoa","ads":"div"},
    "noi_ads":{"division":"Nội khoa","ads":"full"},
    "ads":{"division":None,"ads":"full"}, "marketing":{"division":None,"ads":"full"},
}

# Trang -> các DATA key trang đó cần. Key của trang BỊ CẤM sẽ bị xóa rỗng ở server.
PAGE_KEYS = {
    "overview": ["series","series_div","divisions","newtk"],
    "division": ["series_div","divisions"],
    "service":  ["services"],
    "platform": ["platform","platform_div","platform_extra","services"],
    "sales":    ["sales","sales_div"],
    "master":   ["masters","masters_div"],
    "cross":    ["crosssell","crosssell_div","services","divisions"],
    "memo":     [],  # sinh tại client từ dữ liệu chung; chỉ CEO thấy nav/section
}
# Luôn giữ: cần cho deriveGlobals + thanh trạng thái (series phải khác rỗng)
ALWAYS_KEEP = ["period","today","system_today","week_median_bill","week_mean_bill",
               "totals","dataquality","series"]

# ----------------------------------------------------------------------------
# Mật khẩu (pbkdf2, stdlib — không cần lib ngoài)
# ----------------------------------------------------------------------------
def hash_pw(pw, salt=None):
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 200_000)
    return salt + "$" + dk.hex()

def verify_pw(pw, stored):
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(hash_pw(pw, salt), stored)

def load_users():
    return json.loads(USERS_FILE.read_text(encoding="utf-8")) if USERS_FILE.exists() else {}

def save_users(u):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(u, ensure_ascii=False, indent=2), encoding="utf-8")

# ----------------------------------------------------------------------------
# Lọc bundle theo vai trò
# ----------------------------------------------------------------------------
def _redact_div_item(it):
    """Giữ tên + target (mục tiêu, không nhạy cảm), về 0 các số tài chính của khoa kia."""
    red = dict(it)
    for k in ("revenue","deposit","customers","aov","median","p90","ad_spend","ad_msg",
              "roas","projected_month","pct_target","pct_projected","coc_done"):
        if k in red:
            red[k] = 0
    red["bill_values"] = []
    red["services"] = []
    return red

def _slice_ads(pe, div):
    """Lọc bảng quảng cáo theo khoa + tính lại các chỉ số tổng cho khớp."""
    ads = [a for a in pe.get("ads", []) if a.get("div") == div and (a.get("spend") or 0) > 0]
    total_spend = sum(a.get("spend", 0) for a in ads)
    total_lead = sum((a.get("lead") or 0) for a in ads)
    cpls = sorted(a["cpl"] for a in ads if a.get("cpl"))
    bench = cpls[len(cpls)//2] if cpls else pe.get("benchmark_cpl")
    n = len(ads)
    topn = max(1, int(round(n * 0.2)))
    by_lead = sorted(ads, key=lambda a: (a.get("lead") or 0), reverse=True)[:topn]
    win_lead = sum((a.get("lead") or 0) for a in by_lead)
    winner_pct = round(win_lead / total_lead * 100) if total_lead else 0
    waste = sum(a.get("spend", 0) for a in ads if not (a.get("lead") or 0))
    out = dict(pe)
    out.update({"ads": ads, "n_ads": n, "benchmark_cpl": bench, "winner_pct": winner_pct,
                "winner_n": topn, "waste_spend": waste, "total_spend": total_spend,
                "total_lead": total_lead})
    return out

def apply_scope(out, role):
    """GĐ2: cắt theo chiều dữ liệu (Nội/Ngoại) + ads theo khoa."""
    sc = DATA_SCOPE.get(role, {"division": None, "ads": "full"})
    div, ads = sc.get("division"), sc.get("ads", "full")
    if div:
        sd = out.get("series_div") or {}
        if isinstance(sd, dict) and div in sd:
            out["series"] = sd[div]; out["series_div"] = {div: sd[div]}
        for base, dkey in (("sales","sales_div"), ("masters","masters_div")):
            dv = out.get(dkey) or {}
            if isinstance(dv, dict):
                out[base] = dv.get(div, []); out[dkey] = {div: dv.get(div, [])}
        cdv = out.get("crosssell_div") or {}
        if isinstance(cdv, dict) and div in cdv:
            out["crosssell"] = cdv[div]; out["crosssell_div"] = {div: cdv[div]}
        if isinstance(out.get("services"), list):
            out["services"] = [s for s in out["services"] if s.get("division") == div]
        if "newtk" in out:
            out["newtk"] = None        # New/TK chưa tách theo khoa -> ẩn thẻ
        D = out.get("divisions")
        if isinstance(D, dict) and isinstance(D.get("items"), list):
            D = dict(D)
            D["items"] = [it if it.get("name") == div else _redact_div_item(it) for it in D["items"]]
            out["divisions"] = D
    if ads == "div" and div:
        pdv = out.get("platform_div") or {}
        if isinstance(pdv, dict) and div in pdv:
            out["platform"] = pdv[div]; out["platform_div"] = {div: pdv[div]}
        if isinstance(out.get("platform_extra"), dict):
            out["platform_extra"] = _slice_ads(out["platform_extra"], div)
    return out

def filter_bundle(role):
    raw = json.loads(BUNDLE.read_text(encoding="utf-8"))
    pages = ROLE_PAGES.get(role, [])
    keep = set(ALWAYS_KEEP)
    for p in pages:
        keep.update(PAGE_KEYS.get(p, []))
    out = {}
    for k, v in raw.items():
        if k in keep:
            out[k] = v
        else:                       # trang bị cấm -> xóa rỗng đúng kiểu để không vỡ derive
            out[k] = [] if isinstance(v, list) else ({} if isinstance(v, dict) else v)
    return apply_scope(out, role)   # GĐ2: lọc tiếp theo khoa

# ----------------------------------------------------------------------------
# Chèn lớp phân quyền vào dashboard (ẩn nav + section, đổi trang mặc định, nút đăng xuất)
# ----------------------------------------------------------------------------
import re as _re
_EMBED = _re.compile(r"let DATA = \{.*?\};(\s*//\s*embedded)", _re.DOTALL)

def render_dashboard(user, role):
    html = DASH_FILE.read_text(encoding="utf-8")
    # Vá phòng thủ: dlabel() gốc vỡ khi gặp field ngày null (vd latest_tiktok=null lúc TikTok chưa sync).
    html = html.replace(
        "const dlabel=d=>{const[_,m,day]=d.split('-');return day+'/'+m;};",
        "const dlabel=d=>{if(!d)return '—';const[_,m,day]=String(d).split('-');return day+'/'+m;};")
    pages = ROLE_PAGES.get(role, [])
    landing = pages[0] if pages else "overview"
    # QUAN TRỌNG: thay DATA nhúng sẵn (fallback) bằng bundle đã lọc, nếu không xem source là lộ hết.
    filtered = json.dumps(filter_bundle(role), ensure_ascii=False).replace("</", "<\\/")
    html, n = _EMBED.subn("let DATA = " + filtered + r";\1", html, count=1)
    if n == 0:  # không tìm thấy khối nhúng -> chặn an toàn, không serve dữ liệu thừa
        html = html.replace("let DATA =", "let DATA = {} || ", 1)
    cfg = {"pages": pages, "user": user, "role": role,
           "label": ROLE_LABEL.get(role, role), "landing": landing,
           "div": DATA_SCOPE.get(role, {}).get("division")}
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    # favicon Hydrasignal (SVG tự đổi màu + PNG fallback)
    fav = FAV_TAGS
    # 1) định nghĩa __SWAN SỚM (trong <head>) để dashboard khởi động đúng trang mặc định
    head_inject = fav + "<script>window.__SWAN=%s;</script>" % cfg_json
    if "</head>" in html:
        html = html.replace("</head>", head_inject + "\n</head>", 1)
    else:
        html = head_inject + html
    # 2) dashboard tự gọi show('overview') khi load -> đổi sang trang mặc định của vai trò
    boot_old = "show('overview');"
    i = html.rfind(boot_old)
    if i != -1:
        html = html[:i] + "show((window.__SWAN&&window.__SWAN.landing)||'overview');" + html[i+len(boot_old):]
    # 3) lớp ẩn nav/section + khóa điều hướng + chip người dùng (cuối <body>)
    inject = """
<script>
(function(){
  var S=window.__SWAN, allow=new Set(S.pages);
  function gate(){
    document.querySelectorAll('.nav button[data-p]').forEach(function(b){
      if(!allow.has(b.dataset.p)) b.style.display='none';
    });
    document.querySelectorAll('.page').forEach(function(s){
      if(!allow.has(s.id)){ s.classList.remove('active'); s.innerHTML=''; }
    });
    if(S.div){ var st=document.createElement('style'); st.textContent='#divbar{display:none!important}'; document.head.appendChild(st); }
    var tr=document.querySelector('.topbar-right');
    if(tr && !document.getElementById('swan-userchip')){
      var d=document.createElement('div'); d.id='swan-userchip';
      d.style.cssText='display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--ink-soft)';
      d.innerHTML='<span><b>'+S.user+'</b> · '+S.label+'</span>'+
        '<a href="change-password" style="color:var(--jade);text-decoration:none">Đổi MK</a>'+
        '<a href="logout" style="color:#b4513f;text-decoration:none">Đăng xuất</a>';
      tr.appendChild(d);
    }
  }
  if(typeof window.show==='function' && !window.__swanWrapped){
    var orig=window.show; window.__swanWrapped=true;
    window.show=function(p){ if(!allow.has(p)) p=S.landing; return orig(p); };
  }
  function boot(){ gate(); if(window.show) window.show(S.landing); }
  if(document.readyState!=='loading') setTimeout(boot,0);
  else document.addEventListener('DOMContentLoaded',function(){setTimeout(boot,0);});
})();
</script>
"""
    if "</body>" in html:
        html = html.replace("</body>", inject + "\n</body>", 1)
    else:
        html += inject
    return html

LOGIN_HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Swan Clinic — Đăng nhập</title>
<style>
body{margin:0;font-family:system-ui,'Segoe UI',sans-serif;background:#1d1b16;color:#efe9db;
display:flex;min-height:100vh;align-items:center;justify-content:center}
.box{background:#26241e;padding:34px 30px;border-radius:16px;width:300px;box-shadow:0 12px 40px rgba(0,0,0,.4)}
h1{font-size:21px;margin:0 0 2px}.sub{font-size:11px;letter-spacing:.2em;color:#a99;margin-bottom:22px}
label{font-size:12px;color:#bbb;display:block;margin:12px 0 5px}
input{width:100%;box-sizing:border-box;padding:11px 12px;border-radius:9px;border:1px solid #3a372e;
background:#1d1b16;color:#fff;font-size:14px}
button{margin-top:20px;width:100%;padding:12px;border:0;border-radius:9px;background:#2f6f5e;color:#fff;
font-size:14px;font-weight:600;cursor:pointer}button:hover{background:#357c69}
.err{background:#3a2420;color:#e7a99b;font-size:12.5px;padding:9px 11px;border-radius:8px;margin-bottom:14px}
</style></head><body><form class="box" method="post" action="login">
<h1>Swan Clinic</h1><div class="sub">BẢNG ĐIỀU KHIỂN</div>
{ERR}
<label>Tài khoản</label><input name="username" autofocus autocomplete="username">
<label>Mật khẩu</label><input name="password" type="password" autocomplete="current-password">
<button>Đăng nhập</button></form></body></html>"""

CHPW_HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Đổi mật khẩu</title>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#1d1b16;color:#efe9db;display:flex;
min-height:100vh;align-items:center;justify-content:center}.box{background:#26241e;padding:32px;border-radius:16px;width:300px}
h1{font-size:19px;margin:0 0 18px}label{font-size:12px;color:#bbb;display:block;margin:12px 0 5px}
input{width:100%;box-sizing:border-box;padding:11px;border-radius:9px;border:1px solid #3a372e;background:#1d1b16;color:#fff}
button{margin-top:18px;width:100%;padding:12px;border:0;border-radius:9px;background:#2f6f5e;color:#fff;font-weight:600;cursor:pointer}
.msg{font-size:12.5px;padding:9px 11px;border-radius:8px;margin-bottom:12px}.ok{background:#23362c;color:#9bd5bd}
.err{background:#3a2420;color:#e7a99b}a{color:#7fb8a6;font-size:12.5px;display:inline-block;margin-top:14px}
</style></head><body><form class="box" method="post" action="change-password">
<h1>Đổi mật khẩu</h1>{MSG}
<label>Mật khẩu hiện tại</label><input name="old" type="password">
<label>Mật khẩu mới</label><input name="new1" type="password">
<label>Nhập lại mật khẩu mới</label><input name="new2" type="password">
<button>Cập nhật</button><a href=".">← Về bảng điều khiển</a></form></body></html>"""

# gắn favicon vào trang login + đổi mật khẩu
LOGIN_HTML = LOGIN_HTML.replace("</head>", FAV_TAGS + "</head>")
CHPW_HTML  = CHPW_HTML.replace("</head>", FAV_TAGS + "</head>")

# ----------------------------------------------------------------------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=_secret(), session_cookie="swan_sess",
                   https_only=True, same_site="lax", max_age=60*60*12)

def current(request):
    u = request.session.get("user"); r = request.session.get("role")
    return (u, r) if u and r in ROLE_PAGES else (None, None)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    u, r = current(request)
    if not u:
        return RedirectResponse("login", status_code=302)
    return HTMLResponse(render_dashboard(u, r))

@app.get("/data.json")
def data(request: Request):
    u, r = current(request)
    if not u:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    return JSONResponse(filter_bundle(r))

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    if current(request)[0]:
        return RedirectResponse(".", status_code=302)
    return HTMLResponse(LOGIN_HTML.replace("{ERR}", ""))

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users(); rec = users.get(username.strip().lower())
    if rec and verify_pw(password, rec["pw"]):
        request.session.update({"user": username.strip().lower(), "role": rec["role"]})
        return RedirectResponse(".", status_code=302)
    err = '<div class="err">Sai tài khoản hoặc mật khẩu.</div>'
    return HTMLResponse(LOGIN_HTML.replace("{ERR}", err), status_code=401)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("login", status_code=302)

@app.get("/change-password", response_class=HTMLResponse)
def chpw_get(request: Request):
    if not current(request)[0]:
        return RedirectResponse("login", status_code=302)
    return HTMLResponse(CHPW_HTML.replace("{MSG}", ""))

@app.post("/change-password", response_class=HTMLResponse)
def chpw_post(request: Request, old: str = Form(...), new1: str = Form(...), new2: str = Form(...)):
    u, r = current(request)
    if not u:
        return RedirectResponse("login", status_code=302)
    users = load_users(); rec = users.get(u)
    def page(cls, txt):
        return HTMLResponse(CHPW_HTML.replace("{MSG}", f'<div class="msg {cls}">{txt}</div>'))
    if not rec or not verify_pw(old, rec["pw"]):
        return page("err", "Mật khẩu hiện tại không đúng.")
    if len(new1) < 6:
        return page("err", "Mật khẩu mới cần ≥ 6 ký tự.")
    if new1 != new2:
        return page("err", "Hai ô mật khẩu mới không khớp.")
    rec["pw"] = hash_pw(new1); users[u] = rec; save_users(users)
    return page("ok", "Đã đổi mật khẩu.")

@app.get("/favicon.svg")
def favicon_svg():
    p = _APPDIR / "favicon.svg"
    if p.exists():
        return Response(p.read_bytes(), media_type="image/svg+xml")
    return Response(status_code=404)

@app.get("/favicon.ico")
def favicon():
    p = _APPDIR / "favicon-64.png"
    if p.exists():
        return Response(p.read_bytes(), media_type="image/png")
    return Response(status_code=404)

@app.get("/healthz")
def healthz():
    return PlainTextResponse("ok")
