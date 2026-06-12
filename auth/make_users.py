import json, secrets, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from auth_app import hash_pw

# Nhân viên -> vai trò (username không dấu)
PEOPLE = [
    ("trung","ceo"), ("thanh","ceo"),
    ("thuan","ops"), ("quyen","ops"), ("mily","ops"),
    ("vuongngan","noi_ads"), ("duy","ngoai"),
    ("quynh","marketing"), ("maithi","marketing"),
]
# mật khẩu tạm dễ đọc (bỏ ký tự dễ nhầm)
AL="abcdefghjkmnpqrstuvwxyz"; NU="23456789"
def temp():
    import random
    r=random.SystemRandom()
    return "".join(r.choice(AL) for _ in range(4))+"-"+"".join(r.choice(NU) for _ in range(3))

users={}; plain={}
for name, role in PEOPLE:
    pw=temp(); plain[name]=pw
    users[name]={"role":role, "pw":hash_pw(pw)}

out=os.environ.get("OUT","users.json")
json.dump(users, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("== users.json đã tạo:", out, "==\n")
print(f"{'Tài khoản':12} {'Vai trò':14} {'Mật khẩu tạm'}")
print("-"*42)
for name, role in PEOPLE:
    print(f"{name:12} {role:14} {plain[name]}")
