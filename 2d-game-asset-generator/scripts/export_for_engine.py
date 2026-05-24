#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""导出带有引擎特定元数据的素材。"""

import sys
import os
import json
import argparse
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def export_godot(asset_path, frame_size, animations):
    """生成Godot .tres资源文件。"""
    
    frame_w, frame_h = map(int, frame_size.split('x'))
    
    # 解析动画: "idle:0-3,walk:4-9"
    anim_data = {}
    if animations:
        for anim in animations.split(','):
            name, frames = anim.split(':')
            start, end = map(int, frames.split('-'))
            anim_data[name] = {'start': start, 'end': end}
    
    # 生成.tres文件
    tres_content = """[gd_resource type="SpriteFrames" format=3]

[resource]
animations = [
"""
    
    for anim_name, data in anim_data.items():
        tres_content += f'  {{\n    "name": "{anim_name}",\n    "speed": 10.0,\n    "loop": true,\n    "frames": [\n'
        for frame_idx in range(data['start'], data['end'] + 1):
            tres_content += f'      {{"frame": {frame_idx}, "duration": 1.0}},\n'
        tres_content += '    ]\n  },\n'
    
    tres_content += ']'
    
    return tres_content

def export_unity(asset_path, frame_size, animations):
    """生成Unity纹理图集JSON（标准格式）。"""
    
    frame_w, frame_h = map(int, frame_size.split('x'))
    
    # 解析动画
    sprites = []
    if animations:
        for anim in animations.split(','):
            name, frames = anim.split(':')
            start, end = map(int, frames.split('-'))
            
            for i in range(start, end + 1):
                sprites.append({
                    'name': f'{name}_{i - start}',
                    'rect': {'x': i * frame_w, 'y': 0, 'width': frame_w, 'height': frame_h},
                    'pivot': {'x': 0.5, 'y': 0.5}
                })
    
    # 生成Unity标准纹理图集JSON
    atlas = {
        'frames': {},
        'meta': {
            'image': Path(asset_path).name,
            'format': 'RGBA8888',
            'size': {'w': frame_w * len(sprites), 'h': frame_h},
            'scale': '1'
        }
    }
    
    for sprite in sprites:
        atlas['frames'][sprite['name']] = {
            'frame': sprite['rect'],
            'rotated': False,
            'trimmed': False,
            'spriteSourceSize': {'x': 0, 'y': 0, 'w': frame_w, 'h': frame_h},
            'sourceSize': {'w': frame_w, 'h': frame_h}
        }
    
    return json.dumps(atlas, indent=2, ensure_ascii=False)

def export_phaser(asset_path, frame_size, animations):
    """生成Phaser纹理图集JSON。"""
    
    frame_w, frame_h = map(int, frame_size.split('x'))
    
    atlas = {
        'frames': {},
        'meta': {
            'image': Path(asset_path).name,
            'format': 'RGBA8888',
            'size': {'w': 0, 'h': frame_h},
            'scale': '1'
        }
    }
    
    # 解析Phaser动画
    if animations:
        for anim in animations.split(','):
            name, frames = anim.split(':')
            start, end = map(int, frames.split('-'))
            
            for i in range(start, end + 1):
                frame_name = f'{name}_{i - start}'
                atlas['frames'][frame_name] = {
                    'frame': {'x': i * frame_w, 'y': 0, 'w': frame_w, 'h': frame_h},
                    'rotated': False,
                    'trimmed': False,
                    'spriteSourceSize': {'x': 0, 'y': 0, 'w': frame_w, 'h': frame_h},
                    'sourceSize': {'w': frame_w, 'h': frame_h}
                }
                
                atlas['meta']['size']['w'] = max(atlas['meta']['size']['w'], (i + 1) * frame_w)
    
    return json.dumps(atlas, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='为游戏引擎导出素材')
    parser.add_argument('--asset', required=True, help='素材文件路径')
    parser.add_argument('--engine', required=True, choices=['unity', 'godot', 'phaser'], help='目标引擎')
    parser.add_argument('--frame-size', required=True, help='帧尺寸（例如：64x64）')
    parser.add_argument('--animations', help='动画定义（例如：idle:0-3,walk:4-9）')
    parser.add_argument('--output', required=True, help='输出目录')
    
    args = parser.parse_args()
    
    print(f"[导出] 正在为 {args.engine.upper()} 导出...")
    
    # 生成元数据
    if args.engine == 'godot':
        content = export_godot(args.asset, args.frame_size, args.animations)
        ext = '.tres'
    elif args.engine == 'unity':
        content = export_unity(args.asset, args.frame_size, args.animations)
        ext = '.json'
    elif args.engine == 'phaser':
        content = export_phaser(args.asset, args.frame_size, args.animations)
        ext = '.json'
    
    # 保存元数据
    os.makedirs(args.output, exist_ok=True)
    asset_name = Path(args.asset).stem
    output_path = os.path.join(args.output, f'{asset_name}{ext}')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[成功] 元数据已保存: {output_path}")
    print(f"[提示] 将素材和元数据导入到你的 {args.engine.capitalize()} 项目中")

if __name__ == '__main__':
    main()
