@echo off
chcp 936 >nul
setlocal

rem ============================================================
rem  算法歧视众包观测 · 本地后端一键启动
rem  用法：双击本文件。首次运行会自动创建虚拟环境并安装依赖。
rem ============================================================

cd /d "%~dp0backend"
if errorlevel 1 (
  echo 【错误】未找到 backend 目录，请确认本脚本位于项目根目录。
  pause
  exit /b 1
)

rem ---------- 1. 虚拟环境自检与自动修复 ----------
if not exist ".venv\Scripts\python.exe" (
  echo 首次运行，正在创建虚拟环境...
  where python >nul 2>&1
  if not errorlevel 1 (
    python -m venv .venv
  )
  if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>&1
    if not errorlevel 1 (
      echo 系统 python 不可用，尝试 py 启动器...
      py -3 -m venv .venv
    )
  )
  if not exist ".venv\Scripts\python.exe" (
    echo 【错误】未找到可用的 Python。请先安装 Python 3.10 及以上版本，
    echo        安装时勾选 Add to PATH（官网 python.org 或微软商店均可）。
    pause
    exit /b 1
  )
  echo 虚拟环境创建完成，正在安装依赖（首次较慢，请耐心等待）...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  if errorlevel 1 (
    echo 【错误】依赖安装失败，请检查网络后重试。
    pause
    exit /b 1
  )
  echo 依赖安装完成。
) else (
  rem 虚拟环境已存在：检查关键依赖是否齐全，缺失则自动补装
  ".venv\Scripts\python.exe" -c "import fastapi, uvicorn, pandas, statsmodels" >nul 2>&1
  if errorlevel 1 (
    echo 检测到依赖缺失，正在自动补装...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
      echo 【错误】依赖安装失败，请检查网络后重试。
      pause
      exit /b 1
    )
  )
)

rem ---------- 2. 数据库连接 ----------
rem 默认使用本地 SQLite 文件，开箱即用。
rem 装了 Docker / PostgreSQL 后，改成下面这行即可（去掉前面 rem 并注释掉 sqlite 行）：
rem set "DATABASE_URL=postgresql+psycopg2://obs:obs@localhost:5432/observations"
set "DATABASE_URL=sqlite:///./local_test.db"

rem ---------- 3. 端口检测：已在运行则不重复启动 ----------
netstat -ano | findstr /C:":8000 " | findstr /C:"LISTENING" >nul
if not errorlevel 1 (
  echo 服务已在运行（8000 端口已被监听），不重复启动。
  start "" "http://localhost:8000/"
  exit /b 0
)

rem ---------- 4. 启动后端（新窗口运行，主窗口不阻塞） ----------
echo 正在启动后端服务...
start "算法歧视观测后端" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

rem ---------- 5. 等待服务就绪（最长 30 秒，用 ping 做延时，兼容 stdin 重定向场景） ----------
set /a TRIES=0
:wait_health
set /a TRIES+=1
if %TRIES% GTR 10 goto :health_timeout
where curl >nul 2>&1
if not errorlevel 1 (
  curl -s -m 2 http://127.0.0.1:8000/health 2>nul | findstr /C:"ok" >nul
) else (
  powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 2).Content } catch { '' }" | findstr /C:"ok" >nul
)
if not errorlevel 1 goto :health_ok
echo 等待服务就绪，第 %TRIES% 次尝试...
"%SystemRoot%\System32\ping.exe" -n 4 127.0.0.1 >nul
goto :wait_health

:health_timeout
echo 【错误】等待 30 秒后服务仍未就绪，请到【算法歧视观测后端】窗口查看报错。
pause
exit /b 1

:health_ok
echo.
echo ============================================================
echo  服务已启动，本窗口可关闭；
echo  后端运行在【算法歧视观测后端】窗口，关闭该窗口即停止服务。
echo ============================================================
start "" "http://localhost:8000/"
exit /b 0
