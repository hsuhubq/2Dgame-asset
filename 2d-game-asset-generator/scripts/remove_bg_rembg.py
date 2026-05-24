#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用rembg进行AI抠图的后处理脚本。"""

import sys
import os
import argparse
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def remove_background_rembg(input_path, output_path):
    """使用rembg进行AI抠图。"""
    try:
        from rembg import remove
        from PIL import Image
        
        # 加载图像
        input_image = Image.open(input_path)
        
        # 移除背景
        output_image = remove(input_image)
        
        # 保存结果
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        output_image.save(output_path, 'PNG')
        print(f"[成功] AI抠图完成: {output_path}")
        return True
        
    except ImportError:
        print("[错误] rembg库未安装")
        print("[提示] 请运行: pip install rembg")
        return False
    except Exception as e:
        print(f"[错误] 抠图失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='使用AI抠图移除背景')
    parser.add_argument('--input', required=True, help='输入图像路径')
    parser.add_argument('--output', required=True, help='输出图像路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[错误] 未找到输入文件: {args.input}")
        return
    
    remove_background_rembg(args.input, args.output)

if __name__ == '__main__':
    main()
