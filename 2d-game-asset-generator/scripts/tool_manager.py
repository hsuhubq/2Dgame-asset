#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工具自动下载和安装系统"""

import sys
import os
import subprocess
import json
from pathlib import Path
import urllib.request
import zipfile
import tarfile

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools_dir = Path('tools')
        self.tools_dir.mkdir(exist_ok=True)
        self.config_file = self.tools_dir / 'tools_config.json'
        self.load_config()
    
    def load_config(self):
        """加载工具配置"""
        
        default_config = {
            'models': {
                'pixel-art-xl': {
                    'type': 'huggingface',
                    'repo': 'nerijs/pixel-art-xl',
                    'installed': False
                },
                'controlnet-openpose': {
                    'type': 'huggingface',
                    'repo': 'lllyasviel/control_v11p_sd15_openpose',
                    'installed': False
                }
            },
            'dependencies': {
                'diffusers': {
                    'type': 'pip',
                    'package': 'diffusers>=0.25.0',
                    'installed': False
                },
                'transformers': {
                    'type': 'pip',
                    'package': 'transformers>=4.35.0',
                    'installed': False
                },
                'torch': {
                    'type': 'pip',
                    'package': 'torch>=2.0.0',
                    'installed': False
                },
                'rembg': {
                    'type': 'pip',
                    'package': 'rembg>=2.0.50',
                    'installed': False
                },
                'openai': {
                    'type': 'pip',
                    'package': 'openai>=1.0.0',
                    'installed': False
                }
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """保存工具配置"""
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def check_dependency(self, package_name):
        """检查依赖是否已安装"""
        
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    
    def install_pip_package(self, package_spec):
        """安装pip包"""
        
        print(f"[安装] 正在安装: {package_spec}")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package_spec
            ])
            print(f"[成功] {package_spec} 安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[错误] 安装失败: {e}")
            return False
    
    def download_huggingface_model(self, repo_id):
        """下载HuggingFace模型"""
        
        print(f"[下载] 正在下载模型: {repo_id}")
        print("[提示] 首次下载可能需要较长时间...")
        
        try:
            from huggingface_hub import snapshot_download
            
            model_path = snapshot_download(
                repo_id=repo_id,
                cache_dir=str(self.tools_dir / 'models')
            )
            
            print(f"[成功] 模型已下载到: {model_path}")
            return True
        except ImportError:
            print("[错误] huggingface_hub未安装")
            print("[提示] 正在安装huggingface_hub...")
            if self.install_pip_package('huggingface_hub'):
                return self.download_huggingface_model(repo_id)
            return False
        except Exception as e:
            print(f"[错误] 下载失败: {e}")
            return False
    
    def install_all_dependencies(self):
        """安装所有依赖"""
        
        print("\n[依赖检查] 开始检查和安装依赖...")
        print("=" * 60)
        
        for name, info in self.config['dependencies'].items():
            if info['type'] == 'pip':
                package_spec = info['package']
                package_name = package_spec.split('>=')[0].split('==')[0]
                
                print(f"\n[检查] {name}...")
                
                if self.check_dependency(package_name):
                    print(f"[已安装] {name}")
                    info['installed'] = True
                else:
                    print(f"[未安装] {name}")
                    if self.install_pip_package(package_spec):
                        info['installed'] = True
        
        self.save_config()
        print("\n" + "=" * 60)
        print("[完成] 依赖检查完成")
    
    def download_all_models(self):
        """下载所有模型"""
        
        print("\n[模型下载] 开始下载模型...")
        print("=" * 60)
        
        for name, info in self.config['models'].items():
            if info['type'] == 'huggingface':
                print(f"\n[模型] {name}...")
                
                if info.get('installed'):
                    print(f"[已下载] {name}")
                else:
                    if self.download_huggingface_model(info['repo']):
                        info['installed'] = True
        
        self.save_config()
        print("\n" + "=" * 60)
        print("[完成] 模型下载完成")
    
    def setup_environment(self):
        """设置完整环境"""
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     2D游戏素材生成器 - 环境自动配置                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
        # 1. 安装依赖
        self.install_all_dependencies()
        
        # 2. 下载模型
        print("\n[询问] 是否下载AI模型？（模型较大，首次下载需要时间）")
        print("  1. 是 - 下载所有模型（推荐，获得最佳效果）")
        print("  2. 否 - 跳过模型下载（可使用DALL-E API）")
        
        choice = input("\n请选择 [1/2]: ").strip()
        
        if choice == '1':
            self.download_all_models()
        else:
            print("[跳过] 模型下载已跳过")
        
        # 3. 生成模板
        print("\n[模板] 正在生成角色骨架模板...")
        try:
            from template_generator import TemplateGenerator
            generator = TemplateGenerator()
            generator.generate_all_templates()
        except Exception as e:
            print(f"[警告] 模板生成失败: {e}")
        
        # 4. 完成
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     环境配置完成！                                                ║
║                                                                  ║
║     现在可以开始生成素材了：                                      ║
║     python scripts/generate_asset.py --subject "骑士" ...        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    def check_status(self):
        """检查工具状态"""
        
        print("\n[状态检查]")
        print("=" * 60)
        
        print("\n依赖包:")
        for name, info in self.config['dependencies'].items():
            status = "[已安装]" if info.get('installed') else "[未安装]"
            print(f"  {status} {name}")
        
        print("\nAI模型:")
        for name, info in self.config['models'].items():
            status = "[已下载]" if info.get('installed') else "[未下载]"
            print(f"  {status} {name}")
        
        print("\n" + "=" * 60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='工具管理器')
    parser.add_argument('--setup', action='store_true', help='完整环境配置')
    parser.add_argument('--install-deps', action='store_true', help='仅安装依赖')
    parser.add_argument('--download-models', action='store_true', help='仅下载模型')
    parser.add_argument('--status', action='store_true', help='检查状态')
    
    args = parser.parse_args()
    
    manager = ToolManager()
    
    if args.setup:
        manager.setup_environment()
    elif args.install_deps:
        manager.install_all_dependencies()
    elif args.download_models:
        manager.download_all_models()
    elif args.status:
        manager.check_status()
    else:
        print("请使用 --setup 进行完整环境配置")
        print("或使用 --help 查看所有选项")

if __name__ == '__main__':
    main()
