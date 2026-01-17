# 配置文件
import os

# 共享文件夹路径 - 可以修改为您想要共享的文件夹路径
SHARED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared_files")

# 服务器配置
HOST = "0.0.0.0"  # 监听所有网络接口，允许内网访问
PORT = 10000

# 上传文件大小限制（字节），默认 100MB
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

# 创建共享文件夹（如果不存在）
os.makedirs(SHARED_FOLDER, exist_ok=True)

print(f"共享文件夹路径: {SHARED_FOLDER}")
print(f"访问地址: http://<本机IP>:10000")
