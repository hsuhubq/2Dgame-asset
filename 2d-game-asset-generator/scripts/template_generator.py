#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模板系统 - 提供各类角色骨架模板用于ControlNet"""

import sys
import os
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class TemplateGenerator:
    """模板生成器"""
    
    def __init__(self):
        self.templates_dir = Path('templates')
        self.templates_dir.mkdir(exist_ok=True)
    
    def create_humanoid_template(self, pose='idle', size=(512, 512)):
        """创建人型模板"""
        
        width, height = size
        image = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(image)
        
        # 定义人体比例（基于8头身）
        head_height = height // 8
        
        if pose == 'idle':
            # 待机姿势
            # 头部
            head_center = (width // 2, head_height)
            draw.ellipse([
                head_center[0] - head_height//2, head_center[1] - head_height//2,
                head_center[0] + head_height//2, head_center[1] + head_height//2
            ], fill='black')
            
            # 躯干
            torso_top = head_height * 2
            torso_bottom = head_height * 5
            torso_width = head_height * 2
            draw.rectangle([
                width//2 - torso_width//2, torso_top,
                width//2 + torso_width//2, torso_bottom
            ], fill='black')
            
            # 左臂
            draw.line([
                width//2 - torso_width//2, torso_top + head_height//2,
                width//2 - torso_width, torso_bottom - head_height
            ], fill='black', width=head_height//3)
            
            # 右臂
            draw.line([
                width//2 + torso_width//2, torso_top + head_height//2,
                width//2 + torso_width, torso_bottom - head_height
            ], fill='black', width=head_height//3)
            
            # 左腿
            draw.line([
                width//2 - torso_width//4, torso_bottom,
                width//2 - torso_width//2, height - head_height
            ], fill='black', width=head_height//3)
            
            # 右腿
            draw.line([
                width//2 + torso_width//4, torso_bottom,
                width//2 + torso_width//2, height - head_height
            ], fill='black', width=head_height//3)
        
        elif pose == 'walk':
            # 行走姿势
            head_center = (width // 2, head_height)
            draw.ellipse([
                head_center[0] - head_height//2, head_center[1] - head_height//2,
                head_center[0] + head_height//2, head_center[1] + head_height//2
            ], fill='black')
            
            torso_top = head_height * 2
            torso_bottom = head_height * 5
            torso_width = head_height * 2
            draw.rectangle([
                width//2 - torso_width//2, torso_top,
                width//2 + torso_width//2, torso_bottom
            ], fill='black')
            
            # 左臂向前
            draw.line([
                width//2 - torso_width//2, torso_top + head_height//2,
                width//2 - torso_width//4, torso_bottom + head_height
            ], fill='black', width=head_height//3)
            
            # 右臂向后
            draw.line([
                width//2 + torso_width//2, torso_top + head_height//2,
                width//2 + torso_width, torso_bottom - head_height//2
            ], fill='black', width=head_height//3)
            
            # 左腿向后
            draw.line([
                width//2 - torso_width//4, torso_bottom,
                width//2 - torso_width, height - head_height
            ], fill='black', width=head_height//3)
            
            # 右腿向前
            draw.line([
                width//2 + torso_width//4, torso_bottom,
                width//2 + torso_width//4, height - head_height//2
            ], fill='black', width=head_height//3)
        
        elif pose == 'attack':
            # 攻击姿势
            head_center = (width // 2 - head_height, head_height)
            draw.ellipse([
                head_center[0] - head_height//2, head_center[1] - head_height//2,
                head_center[0] + head_height//2, head_center[1] + head_height//2
            ], fill='black')
            
            torso_top = head_height * 2
            torso_bottom = head_height * 5
            torso_width = head_height * 2
            draw.rectangle([
                width//2 - torso_width, torso_top,
                width//2, torso_bottom
            ], fill='black')
            
            # 右臂向前挥舞
            draw.line([
                width//2, torso_top + head_height//2,
                width//2 + torso_width * 2, torso_top
            ], fill='black', width=head_height//3)
            
            # 左臂向后
            draw.line([
                width//2 - torso_width, torso_top + head_height//2,
                width//2 - torso_width * 2, torso_bottom
            ], fill='black', width=head_height//3)
            
            # 腿部
            draw.line([
                width//2 - torso_width//2, torso_bottom,
                width//2 - torso_width, height - head_height
            ], fill='black', width=head_height//3)
            
            draw.line([
                width//2 - torso_width//4, torso_bottom,
                width//2, height - head_height
            ], fill='black', width=head_height//3)
        
        return image
    
    def create_quadruped_template(self, pose='idle', size=(512, 512)):
        """创建四足动物模板"""
        
        width, height = size
        image = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(image)
        
        body_height = height // 3
        body_width = width // 2
        
        if pose == 'idle':
            # 头部
            head_size = body_height // 2
            head_x = width // 4
            head_y = height // 3
            draw.ellipse([
                head_x - head_size//2, head_y - head_size//2,
                head_x + head_size//2, head_y + head_size//2
            ], fill='black')
            
            # 身体
            body_x = width // 2
            body_y = height // 2
            draw.ellipse([
                body_x - body_width//2, body_y - body_height//2,
                body_x + body_width//2, body_y + body_height//2
            ], fill='black')
            
            # 前左腿
            draw.line([
                body_x - body_width//3, body_y + body_height//2,
                body_x - body_width//3, height - body_height//4
            ], fill='black', width=head_size//4)
            
            # 前右腿
            draw.line([
                body_x - body_width//6, body_y + body_height//2,
                body_x - body_width//6, height - body_height//4
            ], fill='black', width=head_size//4)
            
            # 后左腿
            draw.line([
                body_x + body_width//6, body_y + body_height//2,
                body_x + body_width//6, height - body_height//4
            ], fill='black', width=head_size//4)
            
            # 后右腿
            draw.line([
                body_x + body_width//3, body_y + body_height//2,
                body_x + body_width//3, height - body_height//4
            ], fill='black', width=head_size//4)
            
            # 尾巴
            draw.line([
                body_x + body_width//2, body_y,
                body_x + body_width, body_y - body_height//2
            ], fill='black', width=head_size//4)
        
        elif pose == 'run':
            # 奔跑姿势
            head_size = body_height // 2
            head_x = width // 4
            head_y = height // 3 - body_height//4
            draw.ellipse([
                head_x - head_size//2, head_y - head_size//2,
                head_x + head_size//2, head_y + head_size//2
            ], fill='black')
            
            # 身体（倾斜）
            body_x = width // 2
            body_y = height // 2 - body_height//4
            draw.ellipse([
                body_x - body_width//2, body_y - body_height//2,
                body_x + body_width//2, body_y + body_height//2
            ], fill='black')
            
            # 前腿伸展
            draw.line([
                body_x - body_width//3, body_y + body_height//2,
                body_x - body_width//2, height - body_height//2
            ], fill='black', width=head_size//4)
            
            draw.line([
                body_x - body_width//6, body_y + body_height//2,
                body_x, height - body_height//4
            ], fill='black', width=head_size//4)
            
            # 后腿收缩
            draw.line([
                body_x + body_width//6, body_y + body_height//2,
                body_x + body_width//4, body_y + body_height
            ], fill='black', width=head_size//4)
            
            draw.line([
                body_x + body_width//3, body_y + body_height//2,
                body_x + body_width//2, body_y + body_height
            ], fill='black', width=head_size//4)
            
            # 尾巴向后
            draw.line([
                body_x + body_width//2, body_y,
                body_x + body_width + body_width//2, body_y
            ], fill='black', width=head_size//4)
        
        return image
    
    def create_bird_template(self, pose='idle', size=(512, 512)):
        """创建鸟类模板"""
        
        width, height = size
        image = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(image)
        
        body_size = height // 3
        
        if pose == 'idle':
            # 头部
            head_x = width // 2
            head_y = height // 3
            head_size = body_size // 2
            draw.ellipse([
                head_x - head_size//2, head_y - head_size//2,
                head_x + head_size//2, head_y + head_size//2
            ], fill='black')
            
            # 身体
            body_x = width // 2
            body_y = height // 2
            draw.ellipse([
                body_x - body_size//2, body_y - body_size//3,
                body_x + body_size//2, body_y + body_size//2
            ], fill='black')
            
            # 翅膀（收起）
            draw.arc([
                body_x - body_size, body_y - body_size//2,
                body_x + body_size, body_y + body_size//2
            ], start=180, end=360, fill='black', width=head_size//4)
            
            # 腿
            draw.line([
                body_x - body_size//4, body_y + body_size//2,
                body_x - body_size//4, height - body_size//4
            ], fill='black', width=head_size//6)
            
            draw.line([
                body_x + body_size//4, body_y + body_size//2,
                body_x + body_size//4, height - body_size//4
            ], fill='black', width=head_size//6)
        
        elif pose == 'fly':
            # 飞行姿势
            head_x = width // 2
            head_y = height // 3
            head_size = body_size // 2
            draw.ellipse([
                head_x - head_size//2, head_y - head_size//2,
                head_x + head_size//2, head_y + head_size//2
            ], fill='black')
            
            # 身体
            body_x = width // 2
            body_y = height // 2
            draw.ellipse([
                body_x - body_size//2, body_y - body_size//3,
                body_x + body_size//2, body_y + body_size//2
            ], fill='black')
            
            # 翅膀（展开）
            # 左翅
            draw.line([
                body_x, body_y,
                body_x - body_size * 2, body_y - body_size//2
            ], fill='black', width=head_size//3)
            
            # 右翅
            draw.line([
                body_x, body_y,
                body_x + body_size * 2, body_y - body_size//2
            ], fill='black', width=head_size//3)
            
            # 尾羽
            draw.line([
                body_x, body_y + body_size//2,
                body_x, body_y + body_size * 2
            ], fill='black', width=head_size//4)
        
        return image
    
    def save_template(self, template_type, pose, size=(512, 512)):
        """保存模板"""
        
        if template_type == 'humanoid':
            image = self.create_humanoid_template(pose, size)
        elif template_type == 'quadruped':
            image = self.create_quadruped_template(pose, size)
        elif template_type == 'bird':
            image = self.create_bird_template(pose, size)
        else:
            print(f"[错误] 未知模板类型: {template_type}")
            return None
        
        filename = f"{template_type}_{pose}_{size[0]}x{size[1]}.png"
        filepath = self.templates_dir / filename
        
        image.save(filepath)
        print(f"[保存] 模板已保存: {filepath}")
        
        return str(filepath)
    
    def generate_all_templates(self):
        """生成所有预设模板"""
        
        print("[生成] 正在生成所有模板...")
        
        templates = [
            ('humanoid', 'idle'),
            ('humanoid', 'walk'),
            ('humanoid', 'attack'),
            ('quadruped', 'idle'),
            ('quadruped', 'run'),
            ('bird', 'idle'),
            ('bird', 'fly')
        ]
        
        for template_type, pose in templates:
            self.save_template(template_type, pose)
        
        print(f"[完成] 已生成 {len(templates)} 个模板")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='生成角色骨架模板')
    parser.add_argument('--type', required=True, 
                       choices=['humanoid', 'quadruped', 'bird', 'all'],
                       help='模板类型')
    parser.add_argument('--pose', default='idle',
                       help='姿势（idle/walk/attack/run/fly）')
    parser.add_argument('--size', default='512x512',
                       help='尺寸')
    
    args = parser.parse_args()
    
    generator = TemplateGenerator()
    
    if args.type == 'all':
        generator.generate_all_templates()
    else:
        width, height = map(int, args.size.split('x'))
        generator.save_template(args.type, args.pose, (width, height))

if __name__ == '__main__':
    main()
