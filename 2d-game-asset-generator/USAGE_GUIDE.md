# 2D游戏素材生成器 - 完整使用指南

## 目录
1. [快速开始](#快速开始)
2. [智能模板系统](#智能模板系统)
3. [高级功能](#高级功能)
4. [完整项目工作流](#完整项目工作流)
5. [故障排查](#故障排查)

---

## 快速开始

### 第一步：安装

```bash
# 方法1: 一键安装（推荐）
python setup.py

# 方法2: 手动安装
pip install -r requirements.txt
python scripts/tool_manager.py --setup
```

### 第二步：生成第一个角色

```bash
python scripts/generate_asset.py ^
  --subject "勇敢的骑士" ^
  --style chrono-trigger ^
  --output output/knight.png
```

就这么简单！系统会自动：
- 识别"骑士"为人型角色
- 选择合适的骨架模板
- 应用Chrono Trigger风格
- 生成高质量像素艺术

---

## 智能模板系统

### 它是如何工作的？

```
用户输入 → 关键词识别 → 模板选择 → ControlNet → 高质量输出
```

### 示例1：人型角色

```bash
# 输入
python scripts/generate_asset.py ^
  --subject "精灵法师" ^
  --action "施法" ^
  --output output/elf_mage.png

# 系统自动：
# 1. 识别"精灵"+"法师" = 人型角色
# 2. 识别"施法" = 攻击姿势
# 3. 选择 humanoid_attack 模板
# 4. 生成符合姿势的角色
```

### 示例2：四足动物

```bash
# 输入
python scripts/generate_asset.py ^
  --subject "凶猛的狼" ^
  --action "奔跑" ^
  --output output/wolf.png

# 系统自动：
# 1. 识别"狼" = 四足动物
# 2. 识别"奔跑" = run姿势
# 3. 选择 quadruped_run 模板
# 4. 生成奔跑的狼
```

### 示例3：鸟类

```bash
# 输入
python scripts/generate_asset.py ^
  --subject "雄鹰" ^
  --action "飞行" ^
  --output output/eagle.png

# 系统自动：
# 1. 识别"鹰" = 鸟类
# 2. 识别"飞行" = fly姿势
# 3. 选择 bird_fly 模板
# 4. 生成展翅飞翔的鹰
```

---

## 高级功能

### 功能1：生成多个变体并自动选择最佳

```bash
python scripts/generate_asset.py ^
  --subject "神秘法师" ^
  --style celeste ^
  --variants ^
  --output output/mage.png
```

系统会：
1. 生成4个不同的变体
2. 对每个变体进行质量评分
3. 自动选择得分最高的
4. 保存最佳结果

### 功能2：自定义后处理

```bash
# 生成原始图像
python scripts/generate_asset.py ^
  --subject "战士" ^
  --output output/warrior_raw.png

# 应用高级后处理
python scripts/advanced_post_process.py ^
  --input output/warrior_raw.png ^
  --output output/warrior_final.png ^
  --pixelate 4 ^
  --palette pico-8 ^
  --remove-bg ^
  --outline ^
  --auto-crop
```

### 功能3：质量评估

```bash
# 单个文件评估
python scripts/quality_control.py ^
  --input output/warrior_final.png ^
  --expected-size 64x64 ^
  --asset-type sprite

# 批量评估
python scripts/quality_control.py ^
  --input output/ ^
  --batch ^
  --report quality_report.json
```

### 功能4：手动指定模板

```bash
# 先生成自定义模板
python scripts/template_generator.py ^
  --type humanoid ^
  --pose jump ^
  --size 512x512

# 使用自定义模板
python scripts/generate_asset.py ^
  --subject "忍者" ^
  --controlnet templates/humanoid_jump_512x512.png ^
  --output output/ninja.png
```

---

## 完整项目工作流

### 场景：制作一个RPG游戏的角色素材

#### 步骤1：初始化项目

```bash
python scripts/project_manager.py --init
```

这会创建标准目录结构：
```
assets/
├── sprites/
├── tilesets/
├── ui/
├── icons/
├── backgrounds/
└── effects/
```

#### 步骤2：生成主角的所有动作

```bash
# 待机
python scripts/generate_asset.py ^
  --subject "主角战士" ^
  --action "待机" ^
  --style celeste ^
  --size 64x64 ^
  --output assets/sprites/hero_idle.png

# 行走
python scripts/generate_asset.py ^
  --subject "主角战士" ^
  --action "行走" ^
  --style celeste ^
  --size 64x64 ^
  --output assets/sprites/hero_walk.png

# 攻击
python scripts/generate_asset.py ^
  --subject "主角战士" ^
  --action "挥剑攻击" ^
  --style celeste ^
  --size 64x64 ^
  --output assets/sprites/hero_attack.png

# 受伤
python scripts/generate_asset.py ^
  --subject "主角战士" ^
  --action "受伤后退" ^
  --style celeste ^
  --size 64x64 ^
  --output assets/sprites/hero_hurt.png
```

#### 步骤3：生成敌人

```bash
# 哥布林
python scripts/generate_asset.py ^
  --subject "绿色哥布林" ^
  --action "持棍待机" ^
  --style celeste ^
  --size 48x48 ^
  --output assets/sprites/goblin_idle.png

# 骷髅战士
python scripts/generate_asset.py ^
  --subject "骷髅战士" ^
  --action "挥剑" ^
  --style celeste ^
  --size 64x64 ^
  --output assets/sprites/skeleton_attack.png
```

#### 步骤4：生成地图瓦片

```bash
# 草地
python scripts/generate_asset.py ^
  --subject "草地地面" ^
  --type tileset ^
  --style stardew-valley ^
  --size 32x32 ^
  --output assets/tilesets/grass.png

# 石头地面
python scripts/generate_asset.py ^
  --subject "石头地面" ^
  --type tileset ^
  --style stardew-valley ^
  --size 32x32 ^
  --output assets/tilesets/stone.png
```

#### 步骤5：生成UI元素

```bash
# 生命值图标
python scripts/generate_asset.py ^
  --subject "红色心形生命值图标" ^
  --type icon ^
  --size 32x32 ^
  --output assets/ui/health_icon.png

# 魔法值图标
python scripts/generate_asset.py ^
  --subject "蓝色水滴魔法值图标" ^
  --type icon ^
  --size 32x32 ^
  --output assets/ui/mana_icon.png
```

#### 步骤6：批量质量检查

```bash
python scripts/quality_control.py ^
  --input assets/ ^
  --batch ^
  --report project_quality_report.json
```

#### 步骤7：导出到游戏引擎

```bash
# 导出到Godot
python scripts/export_for_engine.py ^
  --asset assets/sprites/hero_walk.png ^
  --engine godot ^
  --frame-size 64x64 ^
  --animations "walk:0-5" ^
  --output exports/godot/

# 导出到Unity
python scripts/export_for_engine.py ^
  --asset assets/sprites/hero_attack.png ^
  --engine unity ^
  --frame-size 64x64 ^
  --animations "attack:0-7" ^
  --output exports/unity/
```

#### 步骤8：项目备份

```bash
python scripts/project_manager.py --backup
```

---

## 故障排查

### 问题1：模板未找到

```
[警告] 未找到模板: humanoid_idle_*.png
```

**解决方案：**
```bash
# 生成所有模板
python scripts/template_generator.py --type all
```

### 问题2：依赖未安装

```
[错误] diffusers库未安装
```

**解决方案：**
```bash
# 自动安装所有依赖
python scripts/tool_manager.py --install-deps
```

### 问题3：模型未下载

```
[错误] 模型未找到
```

**解决方案：**
```bash
# 下载所有模型
python scripts/tool_manager.py --download-models
```

### 问题4：生成的图像不是像素艺术

**解决方案：**
```bash
# 方法1: 使用像素艺术专用模型
python scripts/generate_asset.py --model pixel-art-xl ...

# 方法2: 应用像素化后处理
python scripts/advanced_post_process.py ^
  --input image.png ^
  --pixelate 4 ^
  --palette pico-8 ^
  --output image_pixel.png
```

### 问题5：角色姿势不对

**解决方案：**
```bash
# 方法1: 使用更明确的动作描述
--action "双手高举挥剑向下劈砍"

# 方法2: 手动指定模板
--controlnet templates/humanoid_attack_512x512.png

# 方法3: 禁用自动模板，使用自定义ControlNet图像
--no-template --controlnet my_custom_pose.png
```

### 问题6：Windows编码错误

**解决方案：**
所有脚本已修复编码问题。如仍有问题：
```bash
set PYTHONIOENCODING=utf-8
python scripts/generate_asset.py ...
```

---

## 性能优化建议

### GPU内存不足

```json
// generation_config.json
{
  "model": "pixel-art",  // 使用较小模型
  "generation_params": {
    "steps": 20,  // 减少步数
    "cfg_scale": 7.0
  }
}
```

### 加快生成速度

1. 使用较小的模型
2. 减少推理步数（20-25步）
3. 降低生成分辨率，后期放大
4. 禁用变体生成

---

## 总结

这个工具现在已经是一个完整的专业级2D游戏素材生成系统：

✅ **智能化** - 自动识别角色类型和姿势
✅ **高质量** - 使用专业AI模型和ControlNet
✅ **易用性** - 一键安装，自动配置
✅ **灵活性** - 支持多种风格和自定义
✅ **完整性** - 从生成到导出的完整流程

开始创作你的游戏素材吧！
