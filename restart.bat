@echo off
chcp 65001 > nul
title 重启云存储服务器

set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo %BLUE%========================================%RESET%
echo %BLUE%      重启内网云存储服务器%RESET%
echo %BLUE%========================================%RESET%
echo.

echo %YELLOW%正在停止服务器...%RESET%

:: 查找并停止占用端口的进程
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":10000" 2^>nul ^| findstr "LISTENING" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo %GREEN%✓ 服务器已停止%RESET%
echo.

echo %YELLOW%正在启动服务器...%RESET%
echo.

:: 启动新服务器
call start.bat
