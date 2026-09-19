# -*- coding: utf-8 -*-
"""生成 PPT 用产品截图素材：插件三页（桩数据）+ 后端五页（真实服务）"""
import hashlib, json, os, shutil, socket, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(r"C:/Users/郭家锴/Documents/Kimi/Workspaces/算法歧视证据搜集插件")
WORK = ROOT / "shots_work"
PLUG = WORK / "plug"
OUT = ROOT / "shots"
OUT.mkdir(exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ---------- 1. 复制插件产物 ----------
if PLUG.exists():
    shutil.rmtree(PLUG)
for d in ["popup", "report", "options", "assets", "icons"]:
    src = ROOT / "dist" / d
    if src.exists():
        shutil.copytree(src, PLUG / d)

def patch(path, transform):
    p = Path(path)
    html = p.read_text(encoding="utf-8")
    p.write_text(transform(html), encoding="utf-8")

# ---------- 2. popup：去掉模块脚本，注入演示填充 ----------
POPUP_DEMO = """
<script>
window.addEventListener('DOMContentLoaded', function () {
  var s = document.getElementById('page-status');
  s.innerHTML = '<span class="badge ok">已识别</span> 淘宝 · 商品详情页';
  document.getElementById('consent-status').innerHTML = '<span class="badge ok">已授权</span>';
  var ck = document.getElementById('ck-auto'); ck.checked = true; ck.disabled = false;
  document.getElementById('auto-row').classList.remove('off');
  document.getElementById('endpoint-display').textContent = 'https://observer.example.com/api/observations';
  var cr = document.getElementById('conn-result');
  cr.style.display = 'block'; cr.style.color = '#166534';
  cr.textContent = '✅ 连接正常（延迟 86ms）';
  var lc = document.getElementById('last-card'); lc.hidden = false;
  document.getElementById('last-result').innerHTML =
    '<b>天猫</b> · 天猫国际自营全球超级店<br/>到手价 <b style="color:#4f46e5">¥3188.55</b>（原价 ¥3799）<br/>' +
    '<span class="muted">已上报 · observationId #1042 · 2 条清洗提示 · 发货地 嘉兴</span>';
  var col = document.getElementById('collect-result');
  col.style.display = 'block'; col.style.color = '#166534';
  col.textContent = '✅ 已自动采集本页观测数据';
});
</script>
"""
def popup_t(html):
    import re
    html = re.sub(r'<script type="module"[^>]*></script>', '', html)
    html = re.sub(r'<link rel="modulepreload"[^>]*>', '', html)
    return html.replace('</body>', POPUP_DEMO + '</body>')
patch(PLUG / "popup" / "popup.html", popup_t)

# ---------- 3. report：桩 chrome.storage，保留真实渲染 ----------
import random
random.seed(7)
plats = [("taobao", "淘宝"), ("tmall", "天猫"), ("jd", "京东"), ("pinduoduo", "拼多多")]
cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "西安"]
goods = ["Apple iPhone 16 Pro 256G", "华为 Mate 70 智能手机", "小米手环 9 NFC版", "美的变频空调 1.5匹",
         "戴森吹风机 HD16", "联想小新 Pro14 笔记本", "耐克 Air Zoom 跑鞋", "三只松鼠坚果礼盒",
         "茅台飞天 53度 500ml", "索尼 WH-1000XM5 耳机", "海尔对开门冰箱", "安踏羽绒服男款"]
obs = []
for i in range(46):
    p, _ = random.choice(plats)
    base = random.choice([99, 159, 299, 599, 1299, 2599, 3799, 5999])
    disc = random.choice([0, 0, 10, 20, 38, 50, 100, 300, 610])
    final = round(base - disc, 2)
    obs.append({
        "platform": p,
        "productName": random.choice(goods),
        "price": {"original": float(base), "final": final if disc else None, "display": float(base)},
        "network": {"city": random.choice(cities)},
        "uploadStatus": "success" if random.random() > 0.08 else "failed",
        "collectedAt": f"2026-09-{random.randint(10,18):02d}T{random.randint(8,22):02d}:{random.randint(10,59):02d}:00+08:00",
    })
STUB = """
<script>
window.chrome = { storage: { local: {
  get: function (key) { return Promise.resolve({ observations: %s }); },
  set: function () { return Promise.resolve(); }
}, onChanged: { addListener: function () {} } } };
</script>
""" % json.dumps(obs, ensure_ascii=False)
def report_t(html):
    return html.replace('<script type="module"', STUB + '<script type="module"')
patch(PLUG / "report" / "report.html", report_t)

# ---------- 4. options：去模块脚本，演示填充 ----------
OPTIONS_DEMO = """
<script>
window.addEventListener('DOMContentLoaded', function () {
  document.getElementById('ck-consent').checked = true;
  document.getElementById('ck-auto-collect').checked = true;
  document.getElementById('inp-endpoint').value = 'https://observer.example.com/api/observations';
  document.getElementById('inp-apikey').value = 'ing_76b1aafdb8aa410c73c28139';
  document.getElementById('ck-mask-shop').checked = true;
  document.getElementById('ck-mask-user').checked = true;
  document.getElementById('history-count').textContent = '本地留存 46 条观测记录（上限 500 条，溢出滚动删除）';
  document.getElementById('saved-hint').textContent = ' ✅ 已保存';
  document.getElementById('saved-hint').style.color = '#166534';
});
</script>
"""
patch(PLUG / "options" / "options.html", popup_t.__wrapped__ if hasattr(popup_t, "__wrapped__") else (lambda h: __import__("re").sub(r'<script type="module"[^>]*></script>', '', h).replace('</body>', OPTIONS_DEMO + '</body>')))

# ---------- 5. 截图工具 ----------
def edge_shot(url, out, w, h, budget=6000):
    prof = WORK / "edgeprof"
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--user-data-dir={prof}", f"--window-size={w},{h}",
           f"--virtual-time-budget={budget}", f"--screenshot={OUT / out}", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    ok = (OUT / out).exists()
    print(("OK " if ok else "FAIL ") + out)
    return ok

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

# ---------- 6. 起静态服务器截插件页 ----------
import http.server, functools, threading
port1 = free_port()
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(PLUG))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", port1), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base1 = f"http://127.0.0.1:{port1}"
time.sleep(0.5)
edge_shot(f"{base1}/popup/popup.html", "shot_popup.png", 380, 720)
edge_shot(f"{base1}/report/report.html", "shot_report.png", 1200, 1750)
edge_shot(f"{base1}/options/options.html", "shot_options.png", 1100, 980)
srv.shutdown()

# ---------- 7. 起真实后端截看板页 ----------
shutil.copy(ROOT / "backend" / "local_test.db", WORK / "obs_data.db")
env = dict(os.environ)
env["DATABASE_URL"] = "sqlite:///" + str(WORK / "obs_data.db").replace("\\", "/")
port2 = free_port()
proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.index:app", "--port", str(port2)],
                        cwd=str(ROOT / "deploy"), env=env,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
base2 = f"http://127.0.0.1:{port2}"
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(base2 + "/health", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    print("health:", urllib.request.urlopen(base2 + "/health", timeout=2).read()[:80])

    # 校验管理员密钥
    adm = "adm_0e606056c947a33fa94b9339"
    digest = "sha256:" + hashlib.sha256(adm.encode()).hexdigest()
    print("admin hash match:", digest.endswith("d2a3986bb1c79ac5edbc3d73a43b07570ffc92b9e8c9e83d568701b8b7672e6b") or digest == "sha256:d2a3986bb1c79ac5edbc3d73a43b07570ffc92b9e8c9e83d568701b8b7672e6b")
    req = urllib.request.Request(base2 + "/api/stats/summary", headers={"X-API-Key": adm})
    try:
        print("stats:", urllib.request.urlopen(req, timeout=3).read()[:120])
        good_key = adm
    except Exception as e:
        print("admin key fail:", e)
        good_key = "dev-key-123"

    static_dir = ROOT / "deploy" / "api" / "app" / "static"
    (static_dir / "_shotme.html").write_text(
        "<script>localStorage.setItem('obs_user_id','47cb0942-f5a6-45c4-961f-23627a9f43e1');location.replace('/me');</script>",
        encoding="utf-8")
    (static_dir / "_shotconsole.html").write_text(
        f"<script>localStorage.setItem('obs_api_key','{good_key}');location.replace('/console');</script>",
        encoding="utf-8")
    (static_dir / "_shotanalysis.html").write_text(
        f"<script>localStorage.setItem('obs_api_key','{good_key}');location.replace('/analysis');</script>",
        encoding="utf-8")
    try:
        edge_shot(f"{base2}/", "shot_landing.png", 1280, 860)
        edge_shot(f"{base2}/_shotme.html", "shot_me.png", 1280, 1450, 9000)
        edge_shot(f"{base2}/_shotconsole.html", "shot_console.png", 1440, 1900, 12000)
        edge_shot(f"{base2}/_shotanalysis.html", "shot_analysis.png", 1440, 1500, 12000)
        edge_shot(f"{base2}/download", "shot_download.png", 1280, 900)
    finally:
        for f in ["_shotme.html", "_shotconsole.html", "_shotanalysis.html"]:
            try:
                (static_dir / f).unlink()
            except FileNotFoundError:
                pass
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()
print("ALL DONE")
