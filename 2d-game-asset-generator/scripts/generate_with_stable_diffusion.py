#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用Stable Diffusion API生成图像的示例实现。"""

import os
import sys
import json
import requests
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_with_stable_diffusion(prompt, size, output_path, count=1, api_key=None, model="stabilityai/stable-diffusion-xl-base-1.0"):
    """使用Stability AI Stable Diffusion API生成图像。"""
    
    # 获取API密钥
    api_key = api_key or os.environ.get('STABILITY_API_KEY')
    if not api_key:
        print("[错误] 未提供API密钥")
        print("[提示] 请设置STABILITY_API_KEY环境变量或传入api_key参数")
        return False
    
    # 尺寸映射
    size_map = {
        '32x32': (256, 256),
        '64x64': (256, 256),
        '128x128': (512, 512),
        '256x256': (1024, 1024),
        '512x512': (1024, 1024)
    }
    width, height = size_map.get(size, (1024, 1024))
    
    print(f"[Stable Diffusion] 生成 {count} 张图像...")
    print(f"[提示词] {prompt}")
    
    try:
        # 调用API
        response = requests.post(
            f"https://api.stability.ai/v1/generation/{model.replace('/', '-')}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "prompt": prompt,
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": count,
                "steps": 30
            }
        )
        
        if response.status_code != 200:
            print(f"[错误] API请求失败: {response.status_code}")
            print(f"[响应] {response.text}")
            return False
        
        data = response.json()
        
        # 创建输出目录
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 保存图像
        for idx, image_data in enumerate(data.get('artifacts', [])):
            # 生成文件名
            if count > 1:
                filename = f"{Path(output_path).stem}_{idx + 1}{Path(output_path).suffix}"
                output_file = os.path.join(output_dir, filename)
            else:
                output_file = output_path
            
            # 保存图像
            with open(output_file, 'wb') as f:
                f.write(bytes.fromhex(image_data['base64']))
            
            print(f"[成功] 保存到: {output_file}")
        
        # 保存元数据
        metadata = {
            'prompt': prompt,
            'size': size,
            'count': count,
            'output': output_path,
            'model': model,
            'timestamp': str(Path(output_path).stem)
        }
        
        metadata_path = str(Path(output_path).with_suffix('.json'))
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n[成功] 元数据已保存: {metadata_path}")
        return True
        
    except Exception as e:
        print(f"[错误] 生成失败: {e}")
        return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='使用Stable Diffusion生成图像')
    parser.add_argument('--prompt', required=True, help='提示词')
    parser.add_argument('--size', default='64x64', help='输出尺寸')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--count', type=int, default=1, help='生成数量')
    parser.add_argument('--api-key', help='Stability AI API密钥')
    parser.add_argument('--model', default='stabilityai/stable-diffusion-xl-base-1.0', help='模型名称')
    
    args = parser.parse_args()
    
    generate_with_stable_diffusion(
        prompt=args.prompt,
        size=args.size,
        output_path=args.output,
        count=args.count,
        api_key=args.api_key,
        model=args.model
    )
