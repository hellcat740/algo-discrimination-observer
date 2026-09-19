# 后端服务镜像：FastAPI + uvicorn
FROM python:3.12-slim

# 避免 .pyc 与输出缓冲，日志实时可见
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv

# 先装依赖，利用镜像层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝应用代码
COPY app ./app

EXPOSE 8000

# DATABASE_URL / API_KEY 由 docker-compose 注入
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
