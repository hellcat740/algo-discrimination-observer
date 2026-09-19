"""Vercel 无服务器入口：把 api/ 加入 sys.path 后暴露 ASGI app。

构建阶段由 scripts/bootstrap.py 从 GitHub 仓库拉取完整后端代码到 api/ 下。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app  # noqa: E402,F401
except ImportError as exc:  # 构建拉取失败时给出可诊断信息
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/health")
    def _bootstrap_error():
        return {"status": "bootstrap_error", "detail": str(exc)}
