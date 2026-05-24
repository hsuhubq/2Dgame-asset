#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键安装和配置脚本"""

import sys
import os

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     2D游戏素材生成器 v2.0 - 一键安装                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

欢迎使用2D游戏素材生成器！

本脚本将自动完成以下操作：
1. 检查并安装Python依赖包
2. 下载AI模型（可选）
3. 生成角色骨架模板
4. 配置环境

准备开始安装吗？
""")
    
    choice = input("按Enter继续，或输入 'n' 取消: ").strip().lower()
    
    if choice == 'n':
        print("\n安装已取消")
        return
    
    # 运行工具管理器
    print("\n开始安装...\n")
    
    try:
        from scripts.tool_manager import ToolManager
        manager = ToolManager()
        manager.setup_environment()
    except Exception as e:
        print(f"\n[错误] 安装过程中出现错误: {e}")
        print("\n请尝试手动安装：")
        print("1. pip install -r requirements.txt")
        print("2. python scripts/tool_manager.py --setup")
        return
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     安装完成！                                                    ║
║                                                                  ║
║     快速开始：                                                    ║
║     python scripts/generate_asset.py ^                           ║
║       --subject "勇敢的骑士" ^                                    ║
║       --style chrono-trigger ^                                   ║
║       --output output/knight.png                                 ║
║                                                                  ║
║     查看更多示例：                                                ║
║     python examples_advanced.py                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

if __name__ == '__main__':
    main()
