#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速开始示例 - 演示完整的素材生成流程"""

import os
import subprocess

def run_command(cmd, description):
    """运行命令并显示描述"""
    print(f"\n{'='*60}")
    print(f"[示例] {description}")
    print(f"{'='*60}")
    print(f"命令: {cmd}\n")
    
    # 这里只是演示，实际使用时取消注释下面的代码
    # result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # print(result.stdout)
    # if result.returncode != 0:
    #     print(f"错误: {result.stderr}")
    #     return False
    # return True
    
    print("[成功] (演示模式 - 实际使用时会执行命令)\n")
    return True

def main():
    print("""
============================================================
     2D游戏素材生成器 - 快速开始示例                      
============================================================

本脚本演示完整的素材生成工作流程：
1. 生成角色精灵
2. 后处理（去背景）
3. 构建精灵表
4. 导出到游戏引擎

注意：需要先集成图像生成API才能实际生成图像
""")
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/warrior_frames", exist_ok=True)
    
    # 示例1：生成单个角色精灵
    run_command(
        'python scripts/generate_asset.py --type sprite --prompt "像素艺术战士角色，待机姿势，蓝色盔甲，剑" --style 16-bit --size 64x64 --output output/warrior_idle.png',
        "示例1：生成战士角色（待机姿势）"
    )
    
    # 示例2：生成地图瓦片
    run_command(
        'python scripts/generate_asset.py --type tileset --prompt "无缝草地瓦片" --style 16-bit --size 32x32 --output output/grass_tile.png',
        "示例2：生成草地瓦片"
    )
    
    # 示例3：生成UI按钮
    run_command(
        'python scripts/generate_asset.py --type ui --prompt "中世纪奇幻按钮，石头带金边" --style 16-bit --size 128x32 --output output/button.png',
        "示例3：生成UI按钮"
    )
    
    # 示例4：生成道具图标
    run_command(
        'python scripts/generate_asset.py --type icon --prompt "生命药水，玻璃瓶中的红色液体" --style 16-bit --size 32x32 --output output/health_potion.png',
        "示例4：生成生命药水图标"
    )
    
    # 示例5：后处理
    run_command(
        'python scripts/post_process.py --input output/warrior_idle.png --output output/warrior_idle_clean.png --size 64x64 --remove-bg',
        "示例5：后处理 - 去除背景并调整尺寸"
    )
    
    # 示例6：构建精灵表（假设已有多帧）
    run_command(
        'python scripts/build_sprite_sheet.py --frames-dir output/warrior_frames/ --cols 4 --rows 1 --frame-size 64x64 --output output/warrior_sheet.png',
        "示例6：构建精灵表（4帧动画）"
    )
    
    # 示例7：导出到Godot
    run_command(
        'python scripts/export_for_engine.py --asset output/warrior_sheet.png --engine godot --frame-size 64x64 --animations "idle:0-3" --output output/godot_export/',
        "示例7：导出到Godot引擎"
    )
    
    # 示例8：导出到Unity
    run_command(
        'python scripts/export_for_engine.py --asset output/warrior_sheet.png --engine unity --frame-size 64x64 --animations "idle:0-3" --output output/unity_export/',
        "示例8：导出到Unity引擎"
    )
    
    print(f"\n{'='*60}")
    print("[完成] 示例演示完成！")
    print("="*60)
    print("""
下一步：
1. 在 generate_asset.py 中集成图像生成API
2. 运行上述命令生成实际素材
3. 查看 references/ 文件夹了解更多提示词技巧
4. 查看 README.md 了解完整使用指南

支持的图像生成API：
- OpenAI DALL-E
- Stability AI (Stable Diffusion)
- 本地Stable Diffusion
- Midjourney (非官方API)
""")

if __name__ == '__main__':
    main()
