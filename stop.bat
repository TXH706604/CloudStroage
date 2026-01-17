@echo off
chcp 65001 > nul
title 停止云存储服务器

set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "RESET=[0m"

echo.
echo ========================================
echo      停止内网云存储服务器
echo ========================================
echo.

:: 查找占用端口的进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":10000" ^| findstr "LISTENING"') do (
    set PID=%%a
)

if "%PID%"=="" (
    echo %GREEN%✓ 服务器未运行%RESET%
    echo.
    pause
    exit /b 0
)

echo %YELLOW%发现运行中的服务器 (PID: %PID%)%RESET%
echo.

:: 显示进程信息
tasklist /FI "PID eq %PID%" /FO TABLE

echo.
set /p choice="确定要停止服务器吗？(Y/N): "
if /i not "%choice%"=="Y" (
    echo 已取消操作
    pause
    exit /b 0
)

:: 停止进程
echo.
echo %YELLOW%正在停止服务器...%RESET%
taskkill /F /PID %PID% >nul 2>&1

if %errorlevel% equ 0 (
    echo %GREEN%✓ 服务器已停止 (PID: %PID%)%RESET%
) else (
    echo %RED%❌ 停止失败，可能需要管理员权限%RESET%
    echo.
    echo 提示：请以管理员身份运行此脚本
)

echo.
pause
