#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整使用示例 - 展示所有新功能"""

import sys
import os

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def example_basic_generation():
    """示例1: 基础生成"""
    print_section("示例1: 基础角色精灵生成")
    
    cmd = """python scripts/generate_asset.py ^
  --subject "勇敢的骑士" ^
  --type sprite ^
  --style chrono-trigger ^
  --action "持剑待机姿势" ^
  --details "银色盔甲，红色披风，金色剑柄" ^
  --size 64x64 ^
  --output output/knight_idle.png"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 使用Chrono Trigger风格生成一个骑士角色")

def example_with_variants():
    """示例2: 生成多个变体并自动选择最佳"""
    print_section("示例2: 生成变体并自动筛选")
    
    cmd = """python scripts/generate_asset.py ^
  --subject "神秘法师" ^
  --type sprite ^
  --style celeste ^
  --action "施法姿势" ^
  --details "紫色长袍，发光法杖，魔法光环" ^
  --size 64x64 ^
  --variants ^
  --output output/mage_cast.png"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 生成4个变体，系统自动评分并选择最佳结果")

def example_tileset():
    """示例3: 地图瓦片生成"""
    print_section("示例3: 地图瓦片生成")
    
    cmd = """python scripts/generate_asset.py ^
  --subject "草地地面" ^
  --type tileset ^
  --style stardew-valley ^
  --details "鲜花点缀，自然纹理，可无缝平铺" ^
  --size 32x32 ^
  --output output/grass_tile.png"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 生成可无缝平铺的草地瓦片")

def example_post_processing():
    """示例4: 高级后处理"""
    print_section("示例4: 高级后处理流水线")
    
    cmd = """python scripts/advanced_post_process.py ^
  --input output/knight_idle.png ^
  --output output/knight_processed.png ^
  --pixelate 4 ^
  --palette pico-8 ^
  --remove-bg ^
  --outline ^
  --auto-crop ^
  --target-size 64x64"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 像素化、应用PICO-8调色板、AI抠图、添加轮廓")

def example_quality_check():
    """示例5: 质量检查"""
    print_section("示例5: 质量评估")
    
    cmd = """python scripts/quality_control.py ^
  --input output/knight_processed.png ^
  --expected-size 64x64 ^
  --asset-type sprite"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 检查透明度、尺寸、颜色数量、边缘质量、居中对齐")

def example_batch_quality():
    """示例6: 批量质量检查"""
    print_section("示例6: 批量质量评估")
    
    cmd = """python scripts/quality_control.py ^
  --input output/ ^
  --batch ^
  --report quality_report.json"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 评估整个目录的所有素材，生成质量报告")

def example_animation():
    """示例7: 动画序列生成"""
    print_section("示例7: 角色动画生成")
    
    # 首先生成精灵表
    cmd1 = """python scripts/generate_asset.py ^
  --subject "战士角色" ^
  --type sprite ^
  --style dead-cells ^
  --action "攻击动画，6帧序列" ^
  --size 384x64 ^
  --output output/warrior_attack_sheet.png"""
    
    print("步骤1: 生成精灵表")
    print(cmd1)
    
    # 然后导出到引擎
    cmd2 = """python scripts/export_for_engine.py ^
  --asset output/warrior_attack_sheet.png ^
  --engine godot ^
  --frame-size 64x64 ^
  --animations "attack:0-5" ^
  --output output/godot_export/"""
    
    print("\n步骤2: 导出到Godot")
    print(cmd2)
    print("\n说明: 生成6帧攻击动画并导出为Godot可用格式")

def example_controlnet():
    """示例8: 使用ControlNet精确控制姿态"""
    print_section("示例8: ControlNet姿态控制")
    
    cmd = """python scripts/generate_with_sd_local.py ^
  --prompt "像素艺术战士角色，Chrono Trigger风格，蓝色盔甲" ^
  --negative-prompt "blurry, 3d, realistic, text" ^
  --size 512x512 ^
  --controlnet-image reference/pose_skeleton.png ^
  --output output/warrior_controlled.png"""
    
    print("命令:")
    print(cmd)
    print("\n说明: 使用骨架图精确控制角色姿态")

def example_custom_style():
    """示例9: 自定义风格预设"""
    print_section("示例9: 创建和使用自定义风格")
    
    code = """from prompt_engineer import PromptEngineer

engineer = PromptEngineer()

# 创建自定义风格预设
custom_style = {
    'style': '暗黑哥特像素艺术',
    'technical': '高对比度，深色调，细腻阴影，神秘氛围',
    'palette': '黑色+深紫+血红',
    'negative_extra': ['bright', 'colorful', 'cheerful']
}

engineer.save_preset('dark-gothic', custom_style)

# 使用自定义风格
prompt, negative = engineer.build_prompt(
    subject="吸血鬼伯爵",
    style_preset="dark-gothic",
    action="展开蝙蝠翅膀"
)

print(f"提示词: {prompt}")
"""
    
    print("Python代码:")
    print(code)
    print("\n说明: 创建自定义风格预设并使用")

def example_project_workflow():
    """示例10: 完整项目工作流"""
    print_section("示例10: 完整游戏项目工作流")
    
    print("步骤1: 初始化项目")
    print("python scripts/project_manager.py --init\n")
    
    print("步骤2: 生成主角精灵（多个动作）")
    actions = ['idle', 'walk', 'attack', 'hurt']
    for action in actions:
        print(f"python scripts/generate_asset.py --subject 主角 --action {action} --style celeste --output assets/sprites/hero_{action}.png")
    print()
    
    print("步骤3: 生成地图瓦片")
    print("python scripts/generate_asset.py --subject 草地 --type tileset --output assets/tilesets/grass.png")
    print("python scripts/generate_asset.py --subject 石头地面 --type tileset --output assets/tilesets/stone.png\n")
    
    print("步骤4: 生成UI元素")
    print("python scripts/generate_asset.py --subject 生命值图标 --type icon --output assets/ui/health_icon.png\n")
    
    print("步骤5: 批量质量检查")
    print("python scripts/quality_control.py --input assets/ --batch --report project_quality.json\n")
    
    print("步骤6: 导出到游戏引擎")
    print("python scripts/export_for_engine.py --asset assets/sprites/hero_walk.png --engine unity --output exports/unity/\n")
    
    print("步骤7: 项目备份")
    print("python scripts/project_manager.py --backup\n")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     2D游戏素材生成器 - 完整使用示例                              ║
║     高质量AI驱动的游戏素材生成工具                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    print("本示例展示了所有主要功能的使用方法\n")
    print("注意: 以下命令为演示，实际使用前请确保已安装所有依赖")
    
    example_basic_generation()
    example_with_variants()
    example_tileset()
    example_post_processing()
    example_quality_check()
    example_batch_quality()
    example_animation()
    example_controlnet()
    example_custom_style()
    example_project_workflow()
    
    print("\n" + "=" * 70)
    print("  更多信息请查看 README.md 和各脚本的 --help 选项")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
