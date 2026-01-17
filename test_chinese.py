#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文文件名支持
"""

import requests
import os

def test_chinese_filename():
    """测试中文文件名上传"""
    url = "http://localhost:10000/api/upload"
    
    # 创建一个中文文件名的测试文件
    test_files = [
        "测试文件.txt",
        "中文文档.docx",
        "图片测试.jpg",
        "数据文件_2024.xlsx",
        "程序代码.py",
        "视频文件.mp4",
        "压缩包.zip",
        "特殊字符@#$%.txt"
    ]
    
    print("="*50)
    print("测试中文文件名支持")
    print("="*50)
    print()
    
    for filename in test_files:
        print(f"正在测试: {filename}")
        
        # 创建测试文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"这是测试文件：{filename}\n")
        
        try:
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"  ✅ 上传成功 - 保存为: {data.get('filename')}")
                    else:
                        print(f"  ❌ 上传失败: {data.get('message')}")
                else:
                    print(f"  ❌ 服务器错误: {response.status_code}")
                    
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
        
        # 清理测试文件
        if os.path.exists(filename):
            os.remove(filename)
        
        print()
    
    print("="*50)
    print("测试完成")
    print("="*50)
    print()
    print("提示:")
    print("  - 请确保服务器正在运行")
    print("  - 检查 shared_files 文件夹中的文件")

if __name__ == "__main__":
    try:
        test_chinese_filename()
    except KeyboardInterrupt:
        print("\n测试已取消")
