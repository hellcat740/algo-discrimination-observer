@echo off
chcp 936 >nul
setlocal

rem ============================================================
rem  算法歧视众包观测 · 停止本地后端服务
rem  原理：找到监听 8000 端口的进程并结束。
rem ============================================================

set "FOUND="
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /C:":8000 " ^| findstr /C:"LISTENING"') do (
  set "FOUND=1"
  echo 正在停止进程 PID %%P ...
  taskkill /F /PID %%P >nul 2>&1
)

if defined FOUND (
  echo 本地服务已停止，8000 端口已释放。
) else (
  echo 未发现监听 8000 端口的服务，无需停止。
)
pause
