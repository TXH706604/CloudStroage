#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内网云存储后端服务器
支持文件上传、下载、删除，实现跨设备文件共享
"""

import os
import json
import socket
import webbrowser
import base64
import re
from datetime import datetime
from urllib.parse import unquote
from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 确保 Flask 正确处理 UTF-8 编码
app.config['JSON_AS_ASCII'] = False  # JSON 返回时不转义中文

# 配置
CONFIG = {
    'UPLOAD_FOLDER': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared_files'),
    'MAX_FILE_SIZE': 500 * 1024 * 1024,  # 500MB
    'ALLOWED_EXTENSIONS': None  # None 表示允许所有文件类型
}

app.config['UPLOAD_FOLDER'] = CONFIG['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = CONFIG['MAX_FILE_SIZE']

# 确保上传文件夹存在
os.makedirs(CONFIG['UPLOAD_FOLDER'], exist_ok=True)

def safe_filename(filename):
    """安全的文件名处理，支持中文"""
    # 保留中文、字母、数字、下划线、连字符、点
    # 移除路径分隔符和其他危险字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip()
    # 移除开头和结尾的点和空格
    filename = filename.strip('. ')
    # 如果文件名为空，使用默认名称
    if not filename:
        filename = 'unnamed'
    return filename

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    # 如果 ALLOWED_EXTENSIONS 为 None，允许所有文件类型
    if CONFIG['ALLOWED_EXTENSIONS'] is None:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in CONFIG['ALLOWED_EXTENSIONS']

def get_file_size(size_bytes):
    """将字节数转换为可读格式"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_file_list():
    """获取文件列表"""
    files = []
    try:
        for item in os.listdir(CONFIG['UPLOAD_FOLDER']):
            item_path = os.path.join(CONFIG['UPLOAD_FOLDER'], item)
            if os.path.isfile(item_path):
                stat_info = os.stat(item_path)
                files.append({
                    'name': item,
                    'size': stat_info.st_size,
                    'size_display': get_file_size(stat_info.st_size),
                    'modified': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    except Exception as e:
        print(f"读取文件列表错误: {e}")
    return sorted(files, key=lambda x: x['name'])

@app.route('/')
def index():
    """主页 - 直接返回 HTML 文件"""
    try:
        # 直接读取并返回 index.html
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"无法加载页面: {str(e)}", 500

@app.route('/api/config')
def get_config():
    """获取服务器配置"""
    return jsonify({
        'success': True,
        'folder_path': CONFIG['UPLOAD_FOLDER'],
        'max_file_size': CONFIG['MAX_FILE_SIZE']
    })

@app.route('/api/files', methods=['GET'])
def list_files():
    """获取文件列表 API"""
    files = get_file_list()
    return jsonify({'success': True, 'files': files})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """文件上传 API"""
    print(f"[DEBUG] 收到上传请求")
    print(f"[DEBUG] request.files: {list(request.files.keys())}")
    
    if 'file' not in request.files:
        print("[DEBUG] 错误: 没有文件被上传")
        return jsonify({'success': False, 'message': '没有文件被上传'}), 400
    
    file = request.files['file']
    print(f"[DEBUG] 文件名: {file.filename}, 大小: {file.content_length if hasattr(file, 'content_length') else 'unknown'}")
    
    if file.filename == '':
        print("[DEBUG] 错误: 未选择文件")
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    # 检查文件类型是否允许
    if not allowed_file(file.filename):
        print(f"[DEBUG] 错误: 不支持的文件类型 - {file.filename}")
        return jsonify({'success': False, 'message': '不支持的文件类型'}), 400
    
    # 保存文件（使用支持中文的安全文件名处理）
    filename = safe_filename(file.filename)
    filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], filename)
    print(f"[DEBUG] 保存路径: {filepath}")
    
    # 处理重名文件
    counter = 1
    original_filename = filename
    while os.path.exists(filepath):
        name, ext = os.path.splitext(original_filename)
        filename = f"{name}_{counter}{ext}"
        filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], filename)
        counter += 1
    print(f"[DEBUG] 最终文件名: {filename}")
    
    try:
        file.save(filepath)
        print(f"[DEBUG] 文件保存成功: {filepath}")
        return jsonify({
            'success': True,
            'message': '文件上传成功',
            'filename': filename
        })
    except Exception as e:
        print(f"[DEBUG] 保存失败: {str(e)}")
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'}), 500

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """文件下载 API - 支持中文文件名"""
    try:
        # URL 解码文件名
        decoded_filename = unquote(filename)
        filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], decoded_filename)
        print(f"[DEBUG] 下载文件: {filepath}")
        
        if os.path.exists(filepath):
            # 使用原始文件名作为下载文件名
            return send_file(filepath, as_attachment=True, download_name=decoded_filename)
        return jsonify({'success': False, 'message': '文件不存在'}), 404
    except Exception as e:
        print(f"[DEBUG] 下载失败: {str(e)}")
        return jsonify({'success': False, 'message': f'下载失败: {str(e)}'}), 500

@app.route('/api/delete', methods=['DELETE'])
def delete_file():
    """文件删除 API - 支持中文文件名"""
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'success': False, 'message': '缺少文件名参数'}), 400
    
    # 直接使用文件名，不过滤中文（JSON 自动处理 UTF-8）
    filename = data['filename']
    filepath = os.path.join(CONFIG['UPLOAD_FOLDER'], filename)
    print(f"[DEBUG] 删除文件: {filepath}")
    print(f"[DEBUG] 文件名长度: {len(filename)}")
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '文件不存在'}), 404
    
    try:
        os.remove(filepath)
        return jsonify({'success': True, 'message': '文件删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}), 500

@app.route('/api/storage', methods=['GET'])
def get_storage_info():
    """获取存储信息"""
    total_size = 0
    file_count = 0
    try:
        for item in os.listdir(CONFIG['UPLOAD_FOLDER']):
            item_path = os.path.join(CONFIG['UPLOAD_FOLDER'], item)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
                file_count += 1
    except Exception as e:
        print(f"获取存储信息错误: {e}")
    
    return jsonify({
        'success': True,
        'total_size': total_size,
        'total_size_display': get_file_size(total_size),
        'file_count': file_count,
        'folder_path': CONFIG['UPLOAD_FOLDER']
    })

def get_local_ip():
    """获取本机局域网 IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    local_ip = get_local_ip()
    port = 10000
    
    print("\n" + "="*70)
    print("📁 内网云存储系统已启动")
    print("="*70)
    print(f"📍 本地访问:   http://localhost:{port}")
    print(f"🌐 局域网访问: http://{local_ip}:{port}")
    print(f"📂 共享目录:   {CONFIG['UPLOAD_FOLDER']}")
    print(f"📏 最大文件:   {get_file_size(CONFIG['MAX_FILE_SIZE'])}")
    print("="*70)
    print("\n✅ 所有连接到同一内网的设备都可以访问")
    print("⚠️  请确保防火墙允许端口 10000 的入站连接")
    print("\n按 Ctrl+C 停止服务器\n")

    # 自动打开浏览器
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass

    # 启动服务器
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
    except Exception as e:
        print(f"\n\n启动失败: {e}")
        print("提示: 端口 10000 可能被占用，请检查是否有其他程序正在使用该端口")

if __name__ == "__main__":
    main()
