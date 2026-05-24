#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""智能模板选择器 - 自动识别角色类型并选择合适的骨架模板"""

import sys
import re
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class TemplateSelector:
    """模板选择器"""
    
    def __init__(self):
        self.templates_dir = Path('templates')
        
        # 定义关键词映射
        self.humanoid_keywords = [
            '人', '骑士', '战士', '法师', '弓箭手', '刺客', '牧师',
            '勇者', '英雄', '村民', '商人', '国王', '王后', '公主', '王子',
            '士兵', '守卫', '盗贼', '巫师', '术士', '圣骑士', '游侠',
            '人类', '精灵', '矮人', '兽人', '哥布林', '巨魔',
            'knight', 'warrior', 'mage', 'archer', 'assassin', 'priest',
            'hero', 'villager', 'merchant', 'king', 'queen', 'soldier'
        ]
        
        self.quadruped_keywords = [
            '狼', '狗', '猫', '虎', '狮', '豹', '熊', '马', '牛', '羊',
            '鹿', '狐狸', '兔子', '松鼠', '老鼠', '猪', '象', '犀牛',
            '四足', '野兽', '怪兽', '龙', '恐龙',
            'wolf', 'dog', 'cat', 'tiger', 'lion', 'bear', 'horse',
            'deer', 'fox', 'rabbit', 'beast', 'monster', 'dragon'
        ]
        
        self.bird_keywords = [
            '鸟', '鹰', '鸽', '乌鸦', '麻雀', '燕子', '鹦鹉', '猫头鹰',
            '凤凰', '飞龙', '翼龙', '飞行',
            'bird', 'eagle', 'crow', 'sparrow', 'owl', 'phoenix', 'flying'
        ]
        
        # 姿势关键词
        self.pose_keywords = {
            'idle': ['待机', '站立', '静止', 'idle', 'stand', 'standing'],
            'walk': ['行走', '走路', '移动', 'walk', 'walking', 'move'],
            'run': ['奔跑', '跑步', '冲刺', 'run', 'running', 'sprint'],
            'attack': ['攻击', '挥剑', '战斗', 'attack', 'attacking', 'fight'],
            'jump': ['跳跃', '跳', 'jump', 'jumping', 'leap'],
            'fly': ['飞行', '飞', 'fly', 'flying', 'flight']
        }
    
    def detect_character_type(self, description):
        """检测角色类型"""
        
        description_lower = description.lower()
        
        # 检查人型
        for keyword in self.humanoid_keywords:
            if keyword in description_lower:
                return 'humanoid'
        
        # 检查鸟类
        for keyword in self.bird_keywords:
            if keyword in description_lower:
                return 'bird'
        
        # 检查四足动物
        for keyword in self.quadruped_keywords:
            if keyword in description_lower:
                return 'quadruped'
        
        # 默认返回人型
        return 'humanoid'
    
    def detect_pose(self, description):
        """检测姿势"""
        
        description_lower = description.lower()
        
        for pose, keywords in self.pose_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return pose
        
        # 默认返回待机
        return 'idle'
    
    def select_template(self, subject, action=None):
        """选择合适的模板"""
        
        # 合并描述
        full_description = subject
        if action:
            full_description += ' ' + action
        
        # 检测类型和姿势
        char_type = self.detect_character_type(full_description)
        pose = self.detect_pose(full_description)
        
        # 调整姿势（某些类型不支持某些姿势）
        if char_type == 'bird' and pose not in ['idle', 'fly']:
            pose = 'fly' if any(k in full_description.lower() for k in ['飞', 'fly']) else 'idle'
        
        if char_type == 'quadruped' and pose == 'walk':
            pose = 'run'
        
        print(f"[模板选择] 角色类型: {char_type}, 姿势: {pose}")
        
        # 查找模板文件
        template_pattern = f"{char_type}_{pose}_*.png"
        templates = list(self.templates_dir.glob(template_pattern))
        
        if templates:
            template_path = str(templates[0])
            print(f"[模板] 使用: {template_path}")
            return template_path
        else:
            print(f"[警告] 未找到模板: {template_pattern}")
            print("[提示] 运行 python scripts/template_generator.py --type all 生成模板")
            return None
    
    def get_template_info(self, subject, action=None):
        """获取模板信息（不实际选择文件）"""
        
        full_description = subject
        if action:
            full_description += ' ' + action
        
        char_type = self.detect_character_type(full_description)
        pose = self.detect_pose(full_description)
        
        return {
            'type': char_type,
            'pose': pose,
            'description': full_description
        }

def main():
    """测试模板选择器"""
    
    selector = TemplateSelector()
    
    test_cases = [
        ("勇敢的骑士", "持剑待机"),
        ("神秘法师", "施法攻击"),
        ("凶猛的狼", "奔跑"),
        ("可爱的猫", "行走"),
        ("雄鹰", "飞行"),
        ("小鸟", "站立"),
        ("战士", "跳跃攻击"),
        ("精灵弓箭手", "瞄准"),
        ("巨龙", "飞行喷火"),
    ]
    
    print("\n[测试] 模板选择器测试")
    print("=" * 60)
    
    for subject, action in test_cases:
        print(f"\n主体: {subject}")
        print(f"动作: {action}")
        
        info = selector.get_template_info(subject, action)
        print(f"  -> 类型: {info['type']}, 姿势: {info['pose']}")
        
        template = selector.select_template(subject, action)
        if template:
            print(f"  -> 模板: {template}")
        else:
            print(f"  -> 需要生成模板")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
