# -*- coding: utf-8 -*-
"""
数据通路端到端测试：真实启动两个 HTTP 服务（公网服务器 + 本地后端）。

链路：
  插件/手工 → 本地后端(8322) → /api/local/sync/push → 服务器(8321)
  分析 → 本地后端 /api/local/analysis/pull → 服务器 /api/pool/* → 合并判别分析
       → keep=false 删除 / keep=true 留存(origin='pulled')

运行：deploy/backend/.venv/Scripts/python.exe deploy/test_pipeline.py
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "repo", "backend"))
VENV_PYTHON = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", ".venv", "Scripts", "python.exe"))

SERVER_PORT = 8321
LOCAL_PORT = 8322
SERVER = f"http://127.0.0.1:{SERVER_PORT}"
LOCAL = f"http://127.0.0.1:{LOCAL_PORT}"

ADMIN_KEY = "adm_0e606056c947a33fa94b9339"
INGEST_KEY = "ing_76b1aafdb8aa410c73c28139"
USER_LOCAL = "aaaaaaaa-0000-0000-0000-000000000001"   # 本地后端用户
USER_OTHER = "bbbbbbbb-0000-0000-0000-000000000002"   # 服务器上另一用户
PRODUCT_ID = "pipeline-test-001"

procs = []
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:200] if extra and not cond else ""))


def req(method, url, headers=None, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method,
                               headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"raw": body[:200]}


def wait_ready(url, proc, timeout=40):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            raise RuntimeError(f"服务进程提前退出：{url}")
        try:
            s, _ = req("GET", url + "/health")
            if s == 200:
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"服务启动超时：{url}")


def start_service(name, port, db_name, extra_env):
    env = os.environ.copy()
    env.update({
        "DATABASE_URL": f"sqlite:///{os.path.join(tmp, db_name)}",
        "VERCEL": "",  # 不用 /tmp 兜底，显式 DATABASE_URL
        **extra_env,
    })
    env.pop("VERCEL", None)
    logf = open(os.path.join(tmp, f"{name}.log"), "w", encoding="utf-8")
    p = subprocess.Popen(
        [VENV_PYTHON, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=BACKEND_DIR, env=env, stdout=logf, stderr=subprocess.STDOUT,
    )
    procs.append(p)
    wait_ready(f"http://127.0.0.1:{port}", p)
    print(f"  [启动] {name} :{port}")


tmp = tempfile.mkdtemp(prefix="observer-pipeline-")

try:
    # ---- 启动双服务 ----
    start_service("server", SERVER_PORT, "server.db", {})
    start_service("local", LOCAL_PORT, "local.db", {
        "SYNC_SERVER_URL": SERVER,
        "SYNC_USER_ID": USER_LOCAL,
        "SYNC_INTERVAL_SEC": "30",
    })

    # ---- 1. 插件向本地后端上报一条观测（公网直报同口径） ----
    obs_payload = {
        "platform_code": "taobao", "product_id": PRODUCT_ID,
        "product_name": "数据通路测试商品", "product_url": "https://item.taobao.com/pipe-test",
        "display_price_cents": 9900, "currency": "CNY",
        "anonymous_id": USER_LOCAL, "is_login": True, "user_agent": "pipeline-test/1.0",
    }
    s, d = req("POST", LOCAL + "/api/observations", {"X-API-Key": INGEST_KEY}, obs_payload)
    check("1.本地后端接收插件上报", s == 201, f"{s} {d}")

    # ---- 2. 本地后端上行到服务器（幂等） ----
    s, d = req("POST", LOCAL + "/api/local/sync/push")
    check("2a.上行 push 成功", s == 200 and d.get("pushed") == 1, f"{s} {d}")
    first_push = d
    s, d = req("POST", LOCAL + "/api/local/sync/push")
    check("2b.再次 push 幂等(无待同步)", s == 200 and d.get("pushed") == 0, f"{s} {d}")
    s, d = req("GET", SERVER + "/api/observations?page_size=50", {"X-API-Key": ADMIN_KEY})
    server_has = any(o["product_id"] == PRODUCT_ID and o.get("user_ref") == USER_LOCAL
                     for o in d.get("items", []))
    check("2c.服务器已收到且归属正确", s == 200 and server_has, f"{s} total={d.get('total')}")

    # ---- 3. 另一用户同步同商品不同价的数据到服务器 ----
    other_rows = [
        {"observation_id": "cccccccc-0000-0000-0000-0000000000%02d" % i,
         "platform_code": "taobao", "product_id": PRODUCT_ID,
         "product_name": "数据通路测试商品", "product_url": "https://item.taobao.com/pipe-test",
         "display_price_cents": 12900 + i * 100, "currency": "CNY",
         "is_login": False, "user_agent": "pipeline-test/1.0",
         "fetch_ts": "2026-09-19T02:00:0%d+00:00" % i}
        for i in range(1, 4)
    ]
    s, d = req("POST", SERVER + "/api/pool/sync", {"X-User-Id": USER_OTHER}, {"items": other_rows})
    check("3a.池同步(他用户)成功", s == 200 and d.get("inserted") == 3, f"{s} {d}")
    s, d = req("POST", SERVER + "/api/pool/sync", {"X-User-Id": USER_OTHER}, {"items": other_rows})
    check("3b.池同步幂等(重复上传跳过)", s == 200 and d.get("inserted") == 0 and d.get("skipped") == 3, f"{s} {d}")
    bad = [dict(other_rows[0], observation_id="dddddddd-0000-0000-0000-000000000099", platform_code="darkweb")]
    s, d = req("POST", SERVER + "/api/pool/sync", {"X-User-Id": USER_OTHER}, {"items": bad})
    check("3c.池同步拒绝非法平台", s == 200 and d.get("rejected") == 1, f"{s} {d}")

    # ---- 4. 按商品拉取（假名化） ----
    s, d = req("GET", SERVER + f"/api/pool/observations?product_id={PRODUCT_ID}&limit=100", {"X-User-Id": USER_LOCAL})
    items = d.get("items", [])
    pseudonyms = {it.get("user_pseudonym") for it in items}
    check("4a.拉取全池数据(≥4条)", s == 200 and len(items) >= 4, f"{s} n={len(items)}")
    check("4b.user_ref 已假名化", all(it.get("user_pseudonym") and not str(it.get("user_pseudonym")).startswith(("aaaa", "bbbb")) for it in items), "")
    check("4c.两用户假名不同", len(pseudonyms) >= 2, str(pseudonyms))
    s, d = req("GET", SERVER + f"/api/pool/products?keyword={PRODUCT_ID}", {"X-User-Id": USER_LOCAL})
    check("4d.商品发现", s == 200 and any(p["product_id"] == PRODUCT_ID for p in d.get("products", [])), f"{s} {d}")
    s, d = req("GET", SERVER + "/api/pool/observations", {"X-User-Id": USER_LOCAL})
    check("4e.无条件拉取被拒(422)", s == 422, f"{s}")

    # ---- 5. 本地分析拉取：keep=false 不留存 ----
    s, d = req("POST", LOCAL + "/api/local/analysis/pull",
               {"Content-Type": "application/json"},  # X-User-Id 由 SYNC_USER_ID 提供
               {"product_id": PRODUCT_ID, "keep": False})
    check("5a.拉取比对分析完成", s == 200 and "analysis" in d, f"{s} {str(d)[:200]}")
    check("5b.拉取数量正确(池内4条=自己1+他人3,新插入3)", d.get("pulled") == 4 and d.get("inserted") == 3, str(d)[:300])
    check("5c.keep=false 未留存", d.get("kept") is False, "")
    an = d.get("analysis", {})
    check("5d.分析结果含用户对", isinstance(an, dict) and ("user_a" in an or "reason_code" in an), str(an)[:200])
    s, d = req("GET", LOCAL + "/api/local/sync/status")
    check("5e.本地无 pulled 留存", s == 200 and d.get("pulled_kept") == 0, f"{s} {d}")

    # ---- 6. keep=true 留存 ----
    s, d = req("POST", LOCAL + "/api/local/analysis/pull", {},
               {"product_id": PRODUCT_ID, "keep": True})
    check("6a.keep=true 留存", s == 200 and d.get("kept") is True and d.get("inserted") == 3, str(d)[:300])
    s, d = req("GET", LOCAL + "/api/local/sync/status")
    check("6b.本地 pulled 留存=3", s == 200 and d.get("pulled_kept") == 3, f"{s} {d}")
    # 留存后可从本地控制台口径查询（管理员视角本地库）
    s, d = req("GET", LOCAL + f"/api/observations?product_id={PRODUCT_ID}&page_size=50", {"X-API-Key": ADMIN_KEY})
    origins = {o.get("origin") for o in d.get("items", [])}
    check("6c.本地库含 local+pulled 两种来源", "pulled" in origins and "local" in origins, str(origins))

    # ---- 7. 管理员能力：新增记录（控制台「新增记录」走的接口） ----
    manual = dict(obs_payload, product_id="manual-add-001", display_price_cents=5000,
                  source_type="manual")
    s, d = req("POST", SERVER + "/api/observations", {"X-API-Key": ADMIN_KEY}, manual)
    check("7a.管理员密钥可新增记录", s == 201, f"{s} {d}")
    s, d = req("POST", SERVER + "/api/observations", {"X-API-Key": "bad-key"}, manual)
    check("7b.非法密钥仍被拒", s in (401, 403), f"{s}")
    s, d = req("GET", SERVER + "/api/stats/summary", {"X-API-Key": ADMIN_KEY})
    check("7c.管理员统计正常", s == 200 and d.get("total", 0) >= 5, f"{s} total={d.get('total')}")

    # ---- 8. 管理员用户管理 API（服务器端） ----
    s, d = req("GET", SERVER + "/api/admin/users", {"X-API-Key": ADMIN_KEY})
    anon_ids = [u.get("anonymous_id") for u in d] if isinstance(d, list) else []
    check("8a.服务器端管理员列出用户(含上行来的 USER_LOCAL)", s == 200 and USER_LOCAL in anon_ids, f"{s} {str(d)[:200]}")
    s, d = req("GET", SERVER + "/api/admin/users", {"X-API-Key": "bad-key"})
    check("8b.用户列表错误密钥被拒", s in (401, 403), f"{s}")
    s, d = req("DELETE", SERVER + f"/api/admin/users/{USER_OTHER}", {"X-API-Key": ADMIN_KEY})
    check("8c.删除服务器测试用户及其观测", s == 200 and d.get("deleted_user") is True and d.get("deleted_observations") == 3, f"{s} {d}")
    s, d = req("GET", SERVER + f"/api/observations?product_id={PRODUCT_ID}&page_size=50", {"X-API-Key": ADMIN_KEY})
    remaining = [o for o in d.get("items", []) if o.get("user_ref") == USER_OTHER]
    check("8d.被删用户观测已从服务器消失", s == 200 and not remaining, f"{s} {str(d)[:200]}")
    s, d = req("DELETE", SERVER + f"/api/admin/users/{USER_OTHER}", {"X-API-Key": ADMIN_KEY})
    check("8e.重复删除不存在用户 404", s == 404, f"{s}")

finally:
    for p in procs:
        p.terminate()
    for p in procs:
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()

failed = [n for n, ok in results if not ok]
print(f"\n=== {len(results) - len(failed)}/{len(results)} 通过 ===")
if failed:
    print("失败项：", failed)
    for name in ("server.log", "local.log"):
        path = os.path.join(tmp, name)
        if os.path.exists(path):
            print(f"--- {name} 尾部 ---")
            print(open(path, encoding="utf-8", errors="replace").read()[-2000:])
    sys.exit(1)
