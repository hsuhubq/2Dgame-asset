#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目管理脚本 - 支持批量生成和版本控制。"""

import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class ProjectManager:
    def __init__(self, project_dir=None):
        self.project_dir = Path(project_dir or os.getcwd())
        self.config_file = self.project_dir / 'project_config.json'
        self.assets_dir = self.project_dir / 'assets'
        
        # 默认配置
        self.config = {
            'name': 'untitled_project',
            'version': '1.0.0',
            'output_structure': {
                'sprites': 'assets/sprites',
                'tilesets': 'assets/tilesets',
                'ui': 'assets/ui',
                'icons': 'assets/icons',
                'backgrounds': 'assets/backgrounds',
                'effects': 'assets/effects'
            },
            'default_style': '16-bit',
            'default_size': '64x64'
        }
        
        # 加载或创建配置
        self.load_config()
    
    def load_config(self):
        """加载项目配置。"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                print(f"[配置] 已加载项目配置: {self.config_file}")
            except Exception as e:
                print(f"[警告] 配置加载失败: {e}")
                self.save_config()
        else:
            self.save_config()
    
    def save_config(self):
        """保存项目配置。"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"[配置] 已保存项目配置: {self.config_file}")
    
    def get_output_path(self, asset_type, filename):
        """根据素材类型获取输出路径。"""
        structure = self.config['output_structure']
        base_dir = structure.get(asset_type, 'assets')
        return Path(base_dir) / filename
    
    def create_project_structure(self):
        """创建项目目录结构。"""
        structure = self.config['output_structure']
        for dir_name in structure.values():
            (self.project_dir / dir_name).mkdir(parents=True, exist_ok=True)
        print(f"[项目] 已创建项目结构: {self.project_dir}")
    
    def backup(self):
        """备份当前项目。"""
        backup_dir = self.project_dir / 'backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制assets目录
        assets_src = self.project_dir / 'assets'
        if assets_src.exists():
            shutil.copytree(assets_src, backup_dir / 'assets')
        
        # 复制配置文件
        if self.config_file.exists():
            shutil.copy(self.config_file, backup_dir / 'project_config.json')
        
        print(f"[备份] 已创建备份: {backup_dir}")
        return backup_dir
    
    def list_assets(self):
        """列出所有生成的素材。"""
        structure = self.config['output_structure']
        print("\n[素材列表]")
        for asset_type, dir_path in structure.items():
            full_path = self.project_dir / dir_path
            if full_path.exists():
                files = list(full_path.glob('*.png'))
                print(f"  {asset_type}: {len(files)} 个文件")
                for f in files[:5]:  # 只显示前5个
                    print(f"    - {f.name}")
                if len(files) > 5:
                    print(f"    ... 还有 {len(files) - 5} 个文件")
        print()

def main():
    parser = argparse.ArgumentParser(description='项目管理工具')
    parser.add_argument('--init', action='store_true', help='初始化新项目')
    parser.add_argument('--backup', action='store_true', help='备份项目')
    parser.add_argument('--list', action='store_true', help='列出素材')
    parser.add_argument('--project-dir', default=None, help='项目目录')
    
    args = parser.parse_args()
    
    pm = ProjectManager(args.project_dir)
    
    if args.init:
        pm.create_project_structure()
    elif args.backup:
        pm.backup()
    elif args.list:
        pm.list_assets()
    else:
        pm.create_project_structure()

if __name__ == '__main__':
    import argparse
    main()
