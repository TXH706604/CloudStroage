@echo off
chcp 65001 > nul
title 服务器状态检查

set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo %BLUE%========================================%RESET%
echo %BLUE%      服务器状态检查%RESET%
echo %BLUE%========================================%RESET%
echo.

:: 检查端口占用
netstat -ano | findstr ":10000" | findstr "LISTENING" >nul
if %errorlevel% neq 0 (
    echo %RED%状态: 未运行%RESET%
    echo.
    echo 服务器未启动，请运行 start.bat 启动服务器
    echo.
    pause
    exit /b 0
)

echo %GREEN%状态: 正在运行%RESET%
echo.

:: 显示详细信息
echo ========================================
echo 监听端口: 10000
echo ========================================
echo.
echo 占用该端口的进程:
echo.

:: 显示进程信息
for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr ":10000" ^| findstr "LISTENING"') do (
    echo 协议: %%a  本地地址: %%b  外部地址: %%c  状态: %%d  PID: %%e
)

echo.
echo 进程详情:
echo.
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":10000" ^| findstr "LISTENING"') do (
    tasklist /FI "PID eq %%a" /FO TABLE
)

echo.
echo ========================================
echo 测试连接
echo ========================================
echo.
echo 正在测试服务器响应...

:: 测试 API 连接
curl -s http://localhost:10000/api/config >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%✓ 服务器响应正常%RESET%
) else (
    echo %RED%✗ 服务器无响应%RESET%
)

echo.
echo ========================================
echo 快捷操作
echo ========================================
echo.
echo [1] 打开浏览器访问
echo [2] 重启服务器
echo [3] 停止服务器
echo [0] 退出
echo.

set /p choice="请选择操作 (0-3): "

if "%choice%"=="1" (
    start http://localhost:10000
    echo 已打开浏览器
)

if "%choice%"=="2" (
    call restart.bat
)

if "%choice%"=="3" (
    call stop.bat
)

echo.
pause
