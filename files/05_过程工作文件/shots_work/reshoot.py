# -*- coding: utf-8 -*-
"""看板页截图：打默认密钥补丁 + 自动运行分析，截完恢复原文件"""
import os, shutil, socket, sqlite3, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(r"C:/Users/郭家锴/Documents/Kimi/Workspaces/算法歧视证据搜集插件")
WORK = ROOT / "shots_work"; OUT = ROOT / "shots"; BAK = WORK / "backup"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
KEY = "adm_0e606056c947a33fa94b9339"
UID = "7d65eb9b-2f1a-4557-9237-ae86b14a84a0"
STATIC = ROOT / "deploy" / "api" / "app" / "static"

def edge(url, out, w, h, budget=15000):
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--user-data-dir={WORK/'edgeprof'}", f"--window-size={w},{h}",
           f"--virtual-time-budget={budget}", f"--screenshot={OUT/out}", url]
    subprocess.run(cmd, capture_output=True, timeout=180)
    print(("OK " if (OUT/out).exists() else "FAIL ") + out)

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

# 1) 数据库副本：把 demo-user-old-1 的 39 条记录划归真实 UUID 用户
shutil.copy(ROOT / "backend" / "local_test.db", WORK / "obs_data.db")
db = sqlite3.connect(WORK / "obs_data.db")
db.execute("UPDATE observations SET user_ref=? WHERE user_ref='demo-user-old-1'", (UID,))
db.execute("UPDATE users SET observation_count=(SELECT count(*) FROM observations WHERE user_ref=?) WHERE anonymous_id=?", (UID, UID))
db.commit(); db.close()

# 2) 备份并补丁静态页
BAK.mkdir(exist_ok=True)
for f in ["index.html", "me.html", "analysis.html", "admin.html"]:
    shutil.copy(STATIC / f, BAK / f)

def patch_file(name, subs, append=""):
    p = STATIC / name
    t = p.read_text(encoding="utf-8")
    for old, new in subs:
        assert old in t, f"{name}: pattern not found: {old[:50]}"
        t = t.replace(old, new, 1)
    if append:
        t = t.replace("</body>", append + "</body>")
    p.write_text(t, encoding="utf-8")

keysub = ("localStorage.getItem('obs_api_key') || ''",
          f"localStorage.getItem('obs_api_key') || '{KEY}'")
patch_file("index.html", [keysub],
           "<script>window.addEventListener('load',function(){setTimeout(function(){try{ovRunPlatform()}catch(e){}},600);});</script>")
patch_file("analysis.html", [keysub],
           "<script>window.addEventListener('load',function(){setTimeout(async function(){try{await loadProducts();var sel=document.getElementById('productSelect');if(sel.options.length){sel.selectedIndex=0;await runAnalysis();await runPlatformAnalysis();}}catch(e){}},600);});</script>")
patch_file("admin.html", [keysub])
patch_file("me.html", [("var uid = localStorage.getItem(KEY);",
                        f"var uid = localStorage.getItem(KEY) || '{UID}';")])

# 3) 起服务截图
env = dict(os.environ); env["DATABASE_URL"] = "sqlite:///" + str(WORK / "obs_data.db").replace("\\", "/")
port = free_port(); base = f"http://127.0.0.1:{port}"
proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.index:app", "--port", str(port)],
                        cwd=str(ROOT / "deploy"), env=env,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(base + "/health", timeout=1); break
        except Exception:
            time.sleep(0.5)
    edge(base + "/me", "shot_me.png", 1280, 1450)
    edge(base + "/console", "shot_console.png", 1440, 2400, 20000)
    edge(base + "/analysis", "shot_analysis.png", 1440, 2300, 25000)
    edge(base + "/admin", "shot_admin.png", 1440, 1500)
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()
    for f in ["index.html", "me.html", "analysis.html", "admin.html"]:
        shutil.copy(BAK / f, STATIC / f)
    print("restored originals")
print("DONE")
