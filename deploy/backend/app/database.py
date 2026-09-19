"""
数据库连接配置。

- DATABASE_URL 从环境变量读取，默认指向 docker-compose 启动的 PostgreSQL。
- 兼容 SQLite（本地无 Docker 时兜底测试用）：sqlite URL 自动加 check_same_thread=False。
- UUID 在模型层用 String(36) 存储，保证 PostgreSQL 与 SQLite 行为一致。
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://obs:obs@localhost:5432/observations",
)

# SQLite 需要关闭同线程检查；PostgreSQL 不需要任何额外参数
_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI 依赖：每请求一个会话，结束自动关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
