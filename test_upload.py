#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件上传功能
"""

import requests
import os

# 测试上传
def test_upload():
    url = "http://localhost:10000/api/upload"
    
    # 创建一个测试文件
    test_file_path = "test_upload.txt"
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("这是一个测试文件\n")
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': f}
            print(f"正在上传 {test_file_path} 到 {url}...")
            response = requests.post(url, files=files)
            
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ 上传成功!")
                else:
                    print(f"❌ 上传失败: {data.get('message')}")
            else:
                print(f"❌ 服务器返回错误: {response.status_code}")
                
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print("已清理测试文件")

if __name__ == "__main__":
    print("="*50)
    print("测试文件上传功能")
    print("="*50)
    print()
    print("请确保服务器正在运行 (python server.py)")
    print()
    
    try:
        test_upload()
    except KeyboardInterrupt:
        print("\n测试已取消")
