@echo off
chcp 65001 > nul
title 内网云存储系统

:: 颜色定义
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo %BLUE%========================================%RESET%
echo %BLUE%      内网云存储系统启动器%RESET%
echo %BLUE%========================================%RESET%
echo.

:: 检查 Python 是否安装
echo %YELLOW%[1/5] 检查 Python...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %RED%❌ 未检测到 Python！%RESET%
    echo.
    echo 请先安装 Python 3.6 或更高版本：
    echo https://www.python.org/downloads/
    echo.
    echo 安装时请务必勾选：
    echo %GREEN%☑ Add Python to PATH%RESET%
    echo.
    pause
    exit /b 1
)
echo %GREEN%✓ Python 已安装%RESET%
python --version
echo.

:: 检查 pip 是否可用
echo %YELLOW%[2/5] 检查 pip...%RESET%
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%❌ pip 不可用！%RESET%
    echo.
    echo 请重新安装 Python 并确保勾选 "Add Python to PATH"
    pause
    exit /b 1
)
echo %GREEN%✓ pip 可用%RESET%
python -m pip --version
echo.

:: 安装依赖
echo %YELLOW%[3/4] 检查并安装依赖...%RESET%
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo 正在安装 Flask...
    python -m pip install flask flask-cors --quiet
    if %errorlevel% neq 0 (
        echo %RED%❌ Flask 安装失败！%RESET%
        echo.
        echo 请手动运行以下命令：
        echo python -m pip install flask flask-cors
        pause
        exit /b 1
    )
    echo %GREEN%✓ Flask 安装完成%RESET%
) else (
    echo %GREEN%✓ Flask 已安装%RESET%
)
echo.

:: 创建共享文件夹
echo %YELLOW%[4/4] 准备共享文件夹...%RESET%
if not exist "shared_files" (
    mkdir "shared_files"
    echo %GREEN%✓ 共享文件夹已创建%RESET%
) else (
    echo %GREEN%✓ 共享文件夹已存在%RESET%
)
echo.

:: 检查端口占用
echo %YELLOW%[4/4] 检查端口 10000...%RESET%
netstat -ano | findstr ":10000" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo %RED%⚠ 警告：端口 10000 已被占用！%RESET%
    echo.
    echo 可能的原因：
    echo   - 服务器已经在运行
    echo   - 其他程序占用了该端口
    echo.
    set /p choice="是否继续启动？(Y/N): "
    if /i not "%choice%"=="Y" (
        echo 已取消启动
        pause
        exit /b 0
    )
) else (
    echo %GREEN%✓ 端口 10000 可用%RESET%
)
echo.

:: 启动服务器
echo %BLUE%========================================%RESET%
echo %GREEN%   所有检查完成，准备启动服务器%RESET%
echo %BLUE%========================================%RESET%
echo.
echo %YELLOW%提示：%RESET%
echo   - 服务器启动后会自动打开浏览器
echo   - 按 Ctrl+C 可停止服务器
echo   - 上传失败时请查看上方的调试信息
echo.
pause

echo.
echo %GREEN%🚀 正在启动服务器...%RESET%
echo.
python server.py

:: 如果服务器异常退出
echo.
echo %RED%服务器已停止%RESET%
echo.
pause
