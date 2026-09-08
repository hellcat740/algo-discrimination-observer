"""
API Key 鉴权。

- 数据接口一律要求 X-API-Key 请求头；admin 页面的数据 API 额外兼容
  ?api_key= 查询参数，方便浏览器直接访问。
- /health 与 /admin 不鉴权（在 main.py 中不挂载本依赖）。
- 密钥从 API_KEY 环境变量读取，默认 dev-key-123（仅本地开发用）。
"""
import os
from typing import Optional

from fastapi import Header, HTTPException, Query, status

API_KEY = os.environ.get("API_KEY", "dev-key-123")


async def require_api_key(
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    api_key: Optional[str] = Query(default=None, description="浏览器兼容：与 X-API-Key 等价"),
):
    """校验 API Key；header 优先，query 参数兜底。"""
    provided = x_api_key or api_key
    if not provided:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少 API Key：请提供 X-API-Key 请求头（或 ?api_key= 参数）",
        )
    if provided != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key 无效",
        )
    return provided
