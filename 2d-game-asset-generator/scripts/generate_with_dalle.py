#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用OpenAI DALL-E API生成图像的示例实现。"""

import os
import sys
import json
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_with_dalle(prompt, size, output_path, count=1, api_key=None):
    """使用OpenAI DALL-E API生成图像。"""
    
    try:
        from openai import OpenAI
    except ImportError:
        print("[错误] openai库未安装")
        print("[提示] 请运行: pip install openai")
        return False
    
    # 获取API密钥
    api_key = api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("[错误] 未提供API密钥")
        print("[提示] 请设置OPENAI_API_KEY环境变量或传入api_key参数")
        return False
    
    # 初始化客户端
    client = OpenAI(api_key=api_key)
    
    # 尺寸映射
    size_map = {
        '32x32': '256x256',
        '64x64': '256x256',
        '128x128': '512x512',
        '256x256': '1024x1024',
        '512x512': '1024x1024'
    }
    dalle_size = size_map.get(size, '1024x1024')
    
    print(f"[DALL-E] 生成 {count} 张图像...")
    print(f"[提示词] {prompt}")
    
    try:
        # 生成图像
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=dalle_size,
            quality="standard",
            n=count
        )
        
        # 创建输出目录
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 保存图像
        for idx, image_data in enumerate(response.data):
            # 生成文件名
            if count > 1:
                filename = f"{Path(output_path).stem}_{idx + 1}{Path(output_path).suffix}"
                output_file = os.path.join(output_dir, filename)
            else:
                output_file = output_path
            
            # 下载并保存图像
            image_url = image_data.url
            print(f"[下载] 图像 {idx + 1}/{count}: {image_url}")
            
            # 下载图像
            import requests
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            with open(output_file, 'wb') as f:
                f.write(image_response.content)
            
            print(f"[成功] 保存到: {output_file}")
        
        # 保存元数据
        metadata = {
            'prompt': prompt,
            'size': size,
            'count': count,
            'output': output_path,
            'model': 'dall-e-3',
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
    parser = argparse.ArgumentParser(description='使用DALL-E生成图像')
    parser.add_argument('--prompt', required=True, help='提示词')
    parser.add_argument('--size', default='64x64', help='输出尺寸')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--count', type=int, default=1, help='生成数量')
    parser.add_argument('--api-key', help='OpenAI API密钥')
    
    args = parser.parse_args()
    
    generate_with_dalle(
        prompt=args.prompt,
        size=args.size,
        output_path=args.output,
        count=args.count,
        api_key=args.api_key
    )
