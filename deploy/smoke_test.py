# -*- coding: utf-8 -*-
"""Vercel 部署树冒烟测试：按真实路由/字段覆盖关键路径。"""
import os
import sys
import tempfile

DEPLOY_API = os.path.abspath(os.path.join(os.path.dirname(__file__), "deploy", "api"))
sys.path.insert(0, DEPLOY_API)

_tmp = tempfile.mkdtemp(prefix="observer-smoke-")
os.chdir(_tmp)
os.environ["VERCEL"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp, "obs.db")

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

_client = TestClient(app)  # 抛异常，便于定位 500
_client.__enter__()      # 触发 startup 建表（等价 uvicorn 启动）
client = _client

ADMIN_KEY = "adm_0e606056c947a33fa94b9339"
INGEST_KEY = "ing_76b1aafdb8aa410c73c28139"
USER_ID = "11111111-2222-3333-4444-555555555555"

results = []
def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    if not cond:
        print("FAIL " + name + "  " + str(extra)[:200])
    else:
        print("PASS " + name)

r = client.get("/health")
check("GET /health", r.status_code == 200 and r.json().get("db") == "up", r.text)

for path in ["/", "/me", "/admin-login", "/download", "/console", "/admin", "/analysis"]:
    r = client.get(path)
    check(f"GET {path}", r.status_code == 200 and len(r.text) > 100, f"{r.status_code}")

r = client.get("/download/plugin.zip")
check("GET /download/plugin.zip", r.status_code == 200 and len(r.content) > 1000, f"{r.status_code} {len(r.content)}B")

r = client.post("/api/auth/admin", json={"key": "wrong-key"})
check("POST /api/auth/admin 错误密钥 401", r.status_code == 401, f"{r.status_code} {r.text[:100]}")
r = client.post("/api/auth/admin", json={"key": ADMIN_KEY})
check("POST /api/auth/admin 正确密钥", r.status_code == 200, f"{r.status_code} {r.text[:100]}")

r = client.get("/api/stats/summary", headers={"X-API-Key": ADMIN_KEY})
check("GET /api/stats/summary 管理员", r.status_code == 200, f"{r.status_code} {r.text[:200]}")
r = client.get("/api/stats/summary", headers={"X-API-Key": "bad"})
check("GET /api/stats/summary 无密钥 401", r.status_code in (401, 403), f"{r.status_code}")

payload = {
    "platform_code": "taobao", "source_type": "extension",
    "product_id": "smoke-001", "product_name": "冒烟测试商品",
    "product_url": "https://item.taobao.com/test",
    "display_price_cents": 9900, "currency": "CNY",
    "anonymous_id": USER_ID, "is_login": True,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SmokeTest/1.0",
}
r = client.post("/api/observations", json=payload, headers={"X-API-Key": INGEST_KEY})
check("POST /api/observations 上报", r.status_code in (200, 201), f"{r.status_code} {r.text[:200]}")
r = client.post("/api/observations", json=payload, headers={"X-API-Key": "bad"})
check("POST /api/observations 错误密钥 401", r.status_code in (401, 403), f"{r.status_code}")

r = client.post("/api/my/login", headers={"X-User-Id": USER_ID})
check("POST /api/my/login 一键登录", r.status_code == 200, f"{r.status_code} {r.text[:150]}")
r = client.get("/api/my/stats", headers={"X-User-Id": USER_ID})
check("GET /api/my/stats 用户统计", r.status_code == 200 and r.json().get("total") == 1, f"{r.status_code} {r.text[:200]}")
r = client.get("/api/my/observations", headers={"X-User-Id": USER_ID})
check("GET /api/my/observations 用户数据", r.status_code == 200 and r.json().get("total") == 1, f"{r.status_code} {r.text[:200]}")

# ---- 管理员用户管理 API ----
r = client.get("/api/admin/users", headers={"X-API-Key": ADMIN_KEY})
check("GET /api/admin/users 管理员列表", r.status_code == 200 and any(
    u.get("anonymous_id") == USER_ID and u.get("observation_count") == 1 for u in r.json()),
    f"{r.status_code} {r.text[:200]}")
r = client.get("/api/admin/users", headers={"X-API-Key": "bad"})
check("GET /api/admin/users 错误密钥 401/403", r.status_code in (401, 403), f"{r.status_code}")
r = client.delete(f"/api/admin/users/{USER_ID}", headers={"X-API-Key": ADMIN_KEY})
check("DELETE /api/admin/users/{id} 删除用户", r.status_code == 200
      and r.json().get("deleted_observations") == 1 and r.json().get("deleted_user") is True,
      f"{r.status_code} {r.text[:200]}")
r = client.get("/api/my/observations", headers={"X-User-Id": USER_ID})
check("删除后该用户观测清空", r.status_code == 200 and r.json().get("total") == 0, f"{r.status_code} {r.text[:200]}")
r = client.delete(f"/api/admin/users/{USER_ID}", headers={"X-API-Key": ADMIN_KEY})
check("DELETE /api/admin/users/{id} 不存在 404", r.status_code == 404, f"{r.status_code}")

failed = [n for n, ok in results if not ok]
print(f"\n=== {len(results) - len(failed)}/{len(results)} 通过 ===")
if failed:
    sys.exit(1)
