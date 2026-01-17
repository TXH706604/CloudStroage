#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "${BLUE}========================================${NC}"
echo "${BLUE}      内网云存储系统启动器${NC}"
echo "${BLUE}========================================${NC}"
echo ""

# 检查 Python 是否安装
echo "${YELLOW}[1/5] 检查 Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "${RED}❌ 未检测到 Python3！${NC}"
    echo ""
    echo 请先安装 Python 3.6 或更高版本：
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  - macOS: brew install python3"
    echo ""
    exit 1
fi
echo "${GREEN}✓ Python 已安装${NC}"
python3 --version
echo ""

# 检查 pip 是否可用
echo "${YELLOW}[2/5] 检查 pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo "${RED}❌ pip3 不可用！${NC}"
    echo ""
    echo 请安装 pip3：
    echo "  - Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  - CentOS/RHEL: sudo yum install python3-pip"
    echo "  - macOS: brew install python3"
    echo ""
    exit 1
fi
echo "${GREEN}✓ pip3 可用${NC}"
pip3 --version
echo ""

# 安装依赖
echo "${YELLOW}[3/4] 检查并安装依赖...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo ""
    echo 正在安装 Flask...
    pip3 install flask flask-cors -q
    if [ $? -ne 0 ]; then
        echo "${RED}❌ Flask 安装失败！${NC}"
        echo ""
        echo 请手动运行以下命令：
        echo "  pip3 install flask flask-cors"
        exit 1
    fi
    echo "${GREEN}✓ Flask 安装完成${NC}"
else
    echo "${GREEN}✓ Flask 已安装${NC}"
fi
echo ""

# 创建共享文件夹
echo "${YELLOW}[4/4] 准备共享文件夹...${NC}"
if [ ! -d "shared_files" ]; then
    mkdir -p "shared_files"
    echo "${GREEN}✓ 共享文件夹已创建${NC}"
else
    echo "${GREEN}✓ 共享文件夹已存在${NC}"
fi
echo ""

# 检查端口占用
echo "${YELLOW}[4/4] 检查端口 10000...${NC}"
if lsof -Pi :10000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "${RED}⚠ 警告：端口 10000 已被占用！${NC}"
    echo ""
    echo 可能的原因：
    echo "  - 服务器已经在运行"
    echo "  - 其他程序占用了该端口"
    echo ""
    read -p "是否继续启动？(Y/N): " choice
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        echo "已取消启动"
        exit 0
    fi
else
    echo "${GREEN}✓ 端口 10000 可用${NC}"
fi
echo ""

# 启动服务器
echo "${BLUE}========================================${NC}"
echo "${GREEN}   所有检查完成，准备启动服务器${NC}"
echo "${BLUE}========================================${NC}"
echo ""
echo "${YELLOW}提示：${NC}"
echo "  - 服务器启动后会自动打开浏览器"
echo "  - 按 Ctrl+C 可停止服务器"
echo "  - 上传失败时请查看上方的调试信息"
echo ""
read -p "按回车键继续..."

echo ""
echo "${GREEN}🚀 正在启动服务器...${NC}"
echo ""
python3 server.py

# 如果服务器异常退出
echo ""
echo "${RED}服务器已停止${NC}"
echo ""
