#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增强的提示词工程系统 - 支持风格预设和负面提示词"""

import sys
import json
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 负面提示词库
NEGATIVE_PROMPTS = {
    'pixel-art': [
        'blurry', 'anti-aliased', '3d', 'realistic', 'photorealistic',
        'text', 'watermark', 'signature', 'low quality', 'deformed',
        'ugly', 'bad anatomy', 'extra limbs', 'poorly drawn',
        'smooth', 'gradient', 'soft edges', 'dithering artifacts'
    ],
    'cartoon': [
        'realistic', 'photorealistic', '3d render', 'blurry',
        'text', 'watermark', 'low quality', 'deformed', 'ugly'
    ],
    'hand-drawn': [
        'digital', '3d', 'photorealistic', 'blurry',
        'text', 'watermark', 'low quality', 'deformed'
    ]
}

# 风格预设库
STYLE_PRESETS = {
    # 经典像素艺术风格
    'chrono-trigger': {
        'style': '16位JRPG像素艺术，Chrono Trigger风格',
        'technical': '清晰的轮廓，丰富的色彩渐变，细腻的阴影，SNES美学',
        'palette': '16-32色调色板',
        'negative_extra': ['modern', 'minimalist', 'flat colors']
    },
    'celeste': {
        'style': '现代像素艺术，Celeste风格',
        'technical': '高对比度，鲜艳色彩，清晰轮廓，动态姿态',
        'palette': '明亮饱和色彩',
        'negative_extra': ['dull', 'washed out', 'low contrast']
    },
    'hollow-knight': {
        'style': '手绘风格2D艺术，Hollow Knight风格',
        'technical': '细腻线条，柔和阴影，梦幻氛围，高细节',
        'palette': '深色调为主，局部亮色点缀',
        'negative_extra': ['bright', 'colorful', 'pixel art']
    },
    'stardew-valley': {
        'style': '温馨像素艺术，Stardew Valley风格',
        'technical': '柔和色彩，圆润造型，友好氛围',
        'palette': '柔和暖色调',
        'negative_extra': ['dark', 'gritty', 'realistic']
    },
    'undertale': {
        'style': '简约像素艺术，Undertale风格',
        'technical': '极简设计，黑白为主，强烈表现力',
        'palette': '黑白+少量强调色',
        'negative_extra': ['complex', 'detailed', 'realistic']
    },
    'shovel-knight': {
        'style': 'NES风格像素艺术，Shovel Knight风格',
        'technical': '8位美学，有限调色板，清晰轮廓',
        'palette': 'NES调色板限制',
        'negative_extra': ['modern', 'smooth', 'high resolution']
    },
    'dead-cells': {
        'style': '现代像素艺术，Dead Cells风格',
        'technical': '流畅动画，高细节，动态光影',
        'palette': '深色背景+鲜艳角色',
        'negative_extra': ['static', 'simple', 'flat']
    },
    'terraria': {
        'style': '沙盒像素艺术，Terraria风格',
        'technical': '丰富细节，多层次，清晰可读',
        'palette': '鲜艳多彩',
        'negative_extra': ['minimalist', 'simple', 'monochrome']
    }
}

# 素材类型特定提示词
ASSET_TYPE_PROMPTS = {
    'sprite': {
        'composition': '居中构图，完整角色，清晰轮廓',
        'background': '透明背景，无环境元素',
        'technical': '游戏精灵，可平铺使用'
    },
    'tileset': {
        'composition': '俯视视角，无缝边缘，可重复平铺',
        'background': '纯色或透明背景',
        'technical': '地图瓦片，边缘完美对接'
    },
    'ui': {
        'composition': '扁平设计，清晰图标，易识别',
        'background': '透明背景，9切片兼容',
        'technical': 'UI元素，可缩放'
    },
    'icon': {
        'composition': '居中，简洁，高辨识度',
        'background': '透明背景',
        'technical': '小尺寸清晰可读'
    },
    'background': {
        'composition': '横向构图，层次分明',
        'background': '完整场景',
        'technical': '视差滚动兼容'
    },
    'effect': {
        'composition': '动态效果，爆发感',
        'background': '透明背景',
        'technical': '特效动画帧，可叠加'
    }
}

class PromptEngineer:
    """提示词工程师"""
    
    def __init__(self):
        self.negative_prompts = NEGATIVE_PROMPTS
        self.style_presets = STYLE_PRESETS
        self.asset_type_prompts = ASSET_TYPE_PROMPTS
    
    def build_prompt(
        self,
        subject,
        asset_type='sprite',
        style_preset='chrono-trigger',
        art_style='pixel-art',
        action=None,
        details=None,
        custom_style=None
    ):
        """构建结构化提示词"""
        
        # 获取风格预设
        preset = self.style_presets.get(style_preset, {})
        
        # 获取素材类型提示词
        type_prompt = self.asset_type_prompts.get(asset_type, {})
        
        # 构建主提示词
        prompt_parts = []
        
        # 1. 主体描述
        prompt_parts.append(subject)
        
        # 2. 动作/姿态
        if action:
            prompt_parts.append(action)
        
        # 3. 风格描述
        if custom_style:
            prompt_parts.append(custom_style)
        elif preset:
            prompt_parts.append(preset.get('style', ''))
            prompt_parts.append(preset.get('technical', ''))
        
        # 4. 技术参数
        prompt_parts.append(type_prompt.get('composition', ''))
        prompt_parts.append(type_prompt.get('background', ''))
        prompt_parts.append(type_prompt.get('technical', ''))
        
        # 5. 额外细节
        if details:
            prompt_parts.append(details)
        
        # 6. 调色板
        if preset and 'palette' in preset:
            prompt_parts.append(preset['palette'])
        
        # 组合提示词
        positive_prompt = '，'.join([p for p in prompt_parts if p])
        
        # 构建负面提示词
        negative_parts = self.negative_prompts.get(art_style, [])
        
        # 添加风格特定的负面提示词
        if preset and 'negative_extra' in preset:
            negative_parts.extend(preset['negative_extra'])
        
        negative_prompt = ', '.join(negative_parts)
        
        return positive_prompt, negative_prompt
    
    def build_animation_prompt(
        self,
        subject,
        animation_type,
        frame_count,
        style_preset='chrono-trigger',
        art_style='pixel-art'
    ):
        """构建动画序列提示词"""
        
        animation_descriptions = {
            'idle': '待机动画，轻微呼吸动作，自然站立',
            'walk': '行走动画，流畅步伐，手臂摆动',
            'run': '奔跑动画，快速移动，动态姿态',
            'attack': '攻击动画，力量爆发，武器挥舞',
            'hurt': '受伤动画，后退反应，痛苦表情',
            'jump': '跳跃动画，腾空姿态，落地缓冲',
            'cast': '施法动画，魔法聚集，能量释放'
        }
        
        anim_desc = animation_descriptions.get(animation_type, animation_type)
        
        prompt, negative = self.build_prompt(
            subject=subject,
            asset_type='sprite',
            style_preset=style_preset,
            art_style=art_style,
            action=anim_desc,
            details=f'{frame_count}帧动画序列，水平排列，帧间流畅过渡'
        )
        
        return prompt, negative
    
    def save_preset(self, name, preset_data, filepath='custom_presets.json'):
        """保存自定义风格预设"""
        
        presets_file = Path(filepath)
        
        if presets_file.exists():
            with open(presets_file, 'r', encoding='utf-8') as f:
                presets = json.load(f)
        else:
            presets = {}
        
        presets[name] = preset_data
        
        with open(presets_file, 'w', encoding='utf-8') as f:
            json.dump(presets, f, indent=2, ensure_ascii=False)
        
        print(f"[保存] 风格预设已保存: {name}")
    
    def load_custom_presets(self, filepath='custom_presets.json'):
        """加载自定义风格预设"""
        
        presets_file = Path(filepath)
        
        if presets_file.exists():
            with open(presets_file, 'r', encoding='utf-8') as f:
                custom_presets = json.load(f)
                self.style_presets.update(custom_presets)
                print(f"[加载] 已加载 {len(custom_presets)} 个自定义预设")

def main():
    """测试提示词工程"""
    
    engineer = PromptEngineer()
    
    # 测试1: 角色精灵
    print("\n=== 测试1: 角色精灵 ===")
    prompt, negative = engineer.build_prompt(
        subject="勇敢的骑士",
        asset_type="sprite",
        style_preset="chrono-trigger",
        action="持剑待机姿势",
        details="银色盔甲，红色披风"
    )
    print(f"正面提示词:\n{prompt}\n")
    print(f"负面提示词:\n{negative}\n")
    
    # 测试2: 动画序列
    print("\n=== 测试2: 动画序列 ===")
    prompt, negative = engineer.build_animation_prompt(
        subject="法师角色",
        animation_type="cast",
        frame_count=6,
        style_preset="celeste"
    )
    print(f"正面提示词:\n{prompt}\n")
    print(f"负面提示词:\n{negative}\n")
    
    # 测试3: 地图瓦片
    print("\n=== 测试3: 地图瓦片 ===")
    prompt, negative = engineer.build_prompt(
        subject="草地地面",
        asset_type="tileset",
        style_preset="stardew-valley",
        details="鲜花点缀，自然纹理"
    )
    print(f"正面提示词:\n{prompt}\n")
    print(f"负面提示词:\n{negative}\n")

if __name__ == '__main__':
    main()
