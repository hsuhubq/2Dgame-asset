#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从单独的帧构建精灵表。"""

import sys
import os
import re
import argparse
from PIL import Image
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def natural_sort_key(filename):
    """自然排序键，正确处理frame_1.png和frame_10.png的顺序。"""
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', str(filename))]

def build_sprite_sheet(frames_dir, cols, rows, frame_size, output_path):
    """将单独的帧组合成精灵表。"""
    
    # 获取所有PNG文件并使用自然排序
    frames = sorted(Path(frames_dir).glob('*.png'), key=natural_sort_key)
    
    if not frames:
        print(f"[错误] 在 {frames_dir} 中未找到PNG文件")
        return
    
    print(f"[帧] 找到 {len(frames)} 帧")
    
    # 解析帧尺寸
    frame_w, frame_h = map(int, frame_size.split('x'))
    
    # 计算精灵表尺寸
    sheet_w = frame_w * cols
    sheet_h = frame_h * rows
    
    # 创建空白精灵表
    sprite_sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0))
    
    # 粘贴帧
    for idx, frame_path in enumerate(frames[:cols * rows]):
        frame = Image.open(frame_path).convert('RGBA')
        
        # 如需要则调整尺寸
        if frame.size != (frame_w, frame_h):
            frame = frame.resize((frame_w, frame_h), Image.NEAREST)
        
        # 计算位置
        col = idx % cols
        row = idx // cols
        x = col * frame_w
        y = row * frame_h
        
        sprite_sheet.paste(frame, (x, y))
        print(f"  [帧 {idx + 1}] {frame_path.name} -> ({x}, {y})")
    
    # 保存
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    sprite_sheet.save(output_path, 'PNG')
    
    print(f"\n[成功] 精灵表已保存: {output_path}")
    print(f"[尺寸] {sheet_w}x{sheet_h} ({cols}x{rows} 网格)")

def main():
    parser = argparse.ArgumentParser(description='从帧构建精灵表')
    parser.add_argument('--frames-dir', required=True, help='帧图像所在目录')
    parser.add_argument('--cols', type=int, required=True, help='列数')
    parser.add_argument('--rows', type=int, required=True, help='行数')
    parser.add_argument('--frame-size', required=True, help='每帧尺寸（例如：64x64）')
    parser.add_argument('--output', required=True, help='输出精灵表路径')
    
    args = parser.parse_args()
    
    build_sprite_sheet(args.frames_dir, args.cols, args.rows, args.frame_size, args.output)

if __name__ == '__main__':
    main()
