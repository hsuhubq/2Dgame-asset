#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对生成的素材进行后处理，使其游戏就绪。"""

import sys
import os
import argparse
from PIL import Image

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def remove_background(image):
    """使用AI抠图移除背景（需要rembg库）。"""
    try:
        from rembg import remove
        return remove(image)
    except ImportError:
        # 如果rembg不可用，使用简单的阈值方法作为后备
        print("[警告] rembg库未安装，使用简单背景移除（可能效果不佳）")
        print("[提示] 请运行: pip install rembg")
        return remove_background_simple(image)

def remove_background_simple(image):
    """简单的背景移除（仅适用于白色背景）。"""
    img = image.convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # 将白色（和接近白色）的像素改为透明
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img

def resize_nearest_neighbor(image, target_size):
    """使用最近邻缩放（无模糊）适用于像素艺术。"""
    width, height = map(int, target_size.split('x'))
    return image.resize((width, height), Image.NEAREST)

def main():
    parser = argparse.ArgumentParser(description='后处理游戏素材')
    parser.add_argument('--input', required=True, help='输入图像路径')
    parser.add_argument('--output', required=True, help='输出图像路径')
    parser.add_argument('--size', help='目标尺寸（例如：64x64）')
    parser.add_argument('--remove-bg', action='store_true', help='移除白色背景')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[错误] 未找到输入文件: {args.input}")
        return
    
    print(f"[处理] 正在处理: {args.input}")
    
    # 加载图像
    img = Image.open(args.input)
    
    # 如果需要则移除背景
    if args.remove_bg:
        print("[背景] 正在移除背景...")
        img = remove_background(img)
    
    # 如果需要则调整尺寸
    if args.size:
        print(f"[尺寸] 正在调整尺寸到 {args.size}...")
        img = resize_nearest_neighbor(img, args.size)
    
    # 保存
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    img.save(args.output, 'PNG')
    
    print(f"[成功] 已保存到: {args.output}")

if __name__ == '__main__':
    main()
