# 2D游戏素材生成器 v2.0

专业级AI驱动的2D游戏素材生成工具，支持高质量像素艺术、多风格预设、智能后处理和质量控制。

## 核心特性

### 🎯 智能模板系统（新）
- **自动角色识别** - 根据描述自动识别人型/四足动物/鸟类
- **骨架模板库** - 预设多种姿势模板（待机/行走/攻击/奔跑/飞行）
- **ControlNet集成** - 使用模板精确控制角色姿态
- **关键词智能匹配** - 支持中英文角色和动作识别

### 🛠️ 自动工具管理（新）
- **一键安装** - 自动检测和安装所有依赖
- **模型自动下载** - 从HuggingFace自动下载AI模型
- **环境配置** - 自动生成模板和配置文件
- **状态检查** - 随时查看工具安装状态

### 🎨 多后端支持
- **本地Stable Diffusion** - 使用pixel-art-xl等专业模型，完全可控
- **ControlNet集成** - 精确控制角色姿态和构图
- **DALL-E 3** - 快速原型设计
- **Stability AI API** - 云端高性能生成

### 🎯 智能提示词工程
- **8种经典游戏风格预设**
  - Chrono Trigger - 经典JRPG像素艺术
  - Celeste - 现代精致像素艺术
  - Hollow Knight - 手绘风格2D艺术
  - Stardew Valley - 温馨农场像素艺术
  - Undertale - 简约表现力像素艺术
  - Shovel Knight - NES复古像素艺术
  - Dead Cells - 流畅动作像素艺术
  - Terraria - 沙盒冒险像素艺术

- **自动负面提示词** - 防止模糊、3D、文字等不需要的元素
- **结构化提示词** - [主体] + [动作] + [风格] + [技术参数]
- **自定义风格预设** - 保存和复用你的风格配置

### 🔧 高级后处理流水线
- **像素化滤镜** - 将任何图像转换为像素艺术
- **调色板映射** - PICO-8、NES、Game Boy等经典调色板
- **AI抠图** - 使用rembg实现精准透明背景
- **自动轮廓** - 添加像素艺术风格轮廓
- **智能裁剪** - 自动移除多余透明区域
- **画布调整** - 精确控制最终尺寸

### ✅ 质量控制系统
- **自动评估** - 检查透明度、尺寸、颜色数量、边缘质量、居中对齐
- **变体生成** - 一次生成4个变体，自动选择最佳
- **批量检查** - 评估整个项目的所有素材
- **质量报告** - 生成详细的JSON格式报告

### 🎮 游戏引擎集成
- **Godot 4** - 生成标准.tres动画资源
- **Unity 2022+** - 标准纹理图集JSON
- **Phaser 3** - Texture Atlas格式

## 快速开始

### 0. 一键安装（推荐）

```bash
python setup.py
```

该命令将自动：
- 安装所有Python依赖
- 下载AI模型（可选）
- 生成角色骨架模板
- 配置环境

### 1. 手动安装依赖（可选）

```bash
# 基础依赖
pip install Pillow numpy scipy

# AI生成（选择一个）
pip install openai  # DALL-E
pip install diffusers transformers accelerate torch  # 本地SD

# 可选增强
pip install rembg  # AI抠图
```

### 2. 配置

编辑 `generation_config.json`:

```json
{
  "backend": "sd-local",
  "model": "pixel-art-xl",
  "quality_check": true,
  "auto_post_process": true
}
```

### 3. 生成你的第一个素材（自动使用模板）

```bash
python scripts/generate_asset.py ^
  --subject "勇敢的骑士" ^
  --type sprite ^
  --style chrono-trigger ^
  --action "持剑待机" ^
  --details "银色盔甲，红色披风" ^
  --size 64x64 ^
  --output output/knight.png
```

系统将自动：
1. 识别“骑士”为人型角色
2. 识别“待机”姿势
3. 选择合适的人型待机模板
4. 使用ControlNet控制姿态
5. 生成高质量像素艺术

## 完整工作流程

### 方案A: 快速生成（使用默认配置）

```bash
# 1. 生成角色
python scripts/generate_asset.py --subject "法师" --style celeste --output output/mage.png

# 2. 自动后处理和质量检查（已内置）
# 完成！
```

### 方案B: 专业工作流（完全控制）

```bash
# 1. 生成多个变体
python scripts/generate_asset.py ^
  --subject "战士" ^
  --style dead-cells ^
  --variants ^
  --output output/warrior.png

# 2. 手动后处理
python scripts/advanced_post_process.py ^
  --input output/warrior.png ^
  --output output/warrior_final.png ^
  --pixelate 4 ^
  --palette pico-8 ^
  --remove-bg ^
  --outline

# 3. 质量评估
python scripts/quality_control.py ^
  --input output/warrior_final.png ^
  --expected-size 64x64

# 4. 导出到引擎
python scripts/export_for_engine.py ^
  --asset output/warrior_final.png ^
  --engine godot ^
  --frame-size 64x64 ^
  --output exports/godot/
```

## 高级功能

### 使用ControlNet控制姿态

```bash
python scripts/generate_with_sd_local.py ^
  --prompt "像素艺术骑士，Chrono Trigger风格" ^
  --negative-prompt "blurry, 3d, realistic" ^
  --controlnet-image reference/pose.png ^
  --output output/knight_posed.png
```

### 创建自定义风格预设

```python
from prompt_engineer import PromptEngineer

engineer = PromptEngineer()

custom_style = {
    'style': '赛博朋克像素艺术',
    'technical': '霓虹色彩，高对比度，未来科技感',
    'palette': '蓝色+粉色+紫色霓虹',
    'negative_extra': ['natural', 'organic', 'medieval']
}

engineer.save_preset('cyberpunk', custom_style)
```

### 批量生成项目素材

```bash
# 初始化项目
python scripts/project_manager.py --init

# 批量生成
for action in idle walk attack hurt; do
  python scripts/generate_asset.py ^
    --subject "主角" ^
    --action $action ^
    --style celeste ^
    --output assets/sprites/hero_$action.png
done

# 批量质量检查
python scripts/quality_control.py --input assets/ --batch
```

## 调色板参考

| 调色板 | 颜色数 | 适用场景 |
|--------|--------|----------|
| pico-8 | 16色 | 复古游戏，限制挑战 |
| nes | 54色 | 8位复古风格 |
| gameboy | 4色 | 极简单色 |
| warm-dungeon | 5色 | 地牢探险 |
| cool-fantasy | 5色 | 奇幻冒险 |

## 风格预设对比

| 风格 | 特点 | 适合类型 |
|------|------|----------|
| chrono-trigger | 丰富色彩，细腻阴影 | JRPG |
| celeste | 高对比，鲜艳 | 平台跳跃 |
| hollow-knight | 手绘，梦幻 | 探索冒险 |
| stardew-valley | 温馨，柔和 | 模拟经营 |
| undertale | 简约，表现力强 | 叙事游戏 |
| shovel-knight | NES限制，复古 | 复古动作 |
| dead-cells | 流畅，高细节 | 动作Roguelike |
| terraria | 多彩，丰富 | 沙盒建造 |

## 性能优化

### 本地SD性能建议

```python
# generation_config.json
{
  "generation_params": {
    "steps": 20,  # 降低步数加快生成（质量略降）
    "cfg_scale": 7.0  # 降低CFG提高速度
  }
}
```

### GPU内存不足

```bash
# 使用较小的模型
--model pixel-art  # 而不是 pixel-art-xl

# 或降低分辨率后放大
--size 256x256  # 生成后用后处理放大
```

## 故障排查

### Q: 生成的图像不是像素艺术风格

A: 
1. 确保使用了像素艺术专用模型（pixel-art-xl）
2. 在风格预设中选择像素艺术风格
3. 启用后处理的像素化功能：`--pixelate 4`

### Q: 背景移除不干净

A:
```bash
# 安装rembg获得更好效果
pip install rembg

# 或手动调整后处理
python scripts/advanced_post_process.py --input image.png --remove-bg
```

### Q: 颜色太多，不像素艺术

A:
```bash
# 应用调色板限制
python scripts/advanced_post_process.py ^
  --input image.png ^
  --palette pico-8 ^
  --output image_limited.png
```

### Q: Windows编码错误

A: 所有脚本已修复编码问题，如仍有问题：
```bash
# 设置环境变量
set PYTHONIOENCODING=utf-8
```

## 项目结构

```
2d-game-asset-generator/
├── scripts/
│   ├── generate_asset.py              # 智能生成调度中心
│   ├── prompt_engineer.py             # 提示词工程系统
│   ├── generate_with_sd_local.py      # 本地SD生成
│   ├── generate_with_dalle.py         # DALL-E生成
│   ├── generate_with_stable_diffusion.py  # SD API生成
│   ├── advanced_post_process.py       # 高级后处理
│   ├── quality_control.py             # 质量控制
│   ├── build_sprite_sheet.py          # 精灵表构建
│   ├── export_for_engine.py           # 引擎导出
│   └── project_manager.py             # 项目管理
├── references/                         # 参考文档
├── generation_config.json              # 生成配置
├── examples_advanced.py                # 高级示例
└── README.md                           # 本文件
```

## 更新日志

### v2.0 (当前版本)
- ✅ 集成Stable Diffusion本地生成
- ✅ ControlNet姿态控制
- ✅ 8种经典游戏风格预设
- ✅ 智能提示词工程系统
- ✅ 高级后处理流水线（像素化、调色板、AI抠图）
- ✅ 质量控制和自动评估
- ✅ 变体生成和自动筛选
- ✅ 修复所有编码问题
- ✅ 完整的中文支持

### v1.0
- 基础生成功能
- 简单后处理
- 引擎导出

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- Stable Diffusion - 核心生成引擎
- rembg - AI抠图
- 各游戏风格灵感来源于相应的经典游戏


## 智能模板系统详解

### 自动角色识别

系统会自动识别以下角色类型：

**人型角色**
- 关键词：人、骑士、战士、法师、弓箭手、刺客、牧师、勇者、英雄、村民、商人、国王、王后、公主、王子、士兵、守卫、盗贼、巫师、术士、圣骑士、游侠
- 种族：人类、精灵、矮人、兽人、哥布林、巨魔

**四足动物**
- 关键词：狼、狗、猫、虎、狮、豹、熊、马、牛、羊、鹿、狐狸、兔子、松鼠、老鼠、猪、象、犀牛、四足、野兽、怪兽、龙、恐龙

**鸟类**
- 关键词：鸟、鹰、鸽、乌鸦、麻雀、燕子、鹦鹉、猫头鹰、凤凰、飞龙、翼龙

### 支持的姿势

- **idle** (待机) - 站立、静止
- **walk** (行走) - 走路、移动
- **run** (奔跑) - 跑步、冲刺
- **attack** (攻击) - 挥剑、战斗
- **jump** (跳跃) - 跳
- **fly** (飞行) - 飞

### 使用示例

```bash
# 示例1: 人型角色 - 自动使用人型待机模板
python scripts/generate_asset.py --subject "精灵弓箭手" --action "瞄准" --output output/elf.png

# 示例2: 四足动物 - 自动使用四足奔跑模板
python scripts/generate_asset.py --subject "凶猛的狼" --action "奔跑" --output output/wolf.png

# 示例3: 鸟类 - 自动使用鸟类飞行模板
python scripts/generate_asset.py --subject "雄鹰" --action "飞行" --output output/eagle.png

# 示例4: 禁用自动模板（使用自定义ControlNet图像）
python scripts/generate_asset.py --subject "战士" --no-template --controlnet my_pose.png --output output/warrior.png
```

### 手动生成模板

```bash
# 生成所有预设模板
python scripts/template_generator.py --type all

# 生成特定类型和姿势
python scripts/template_generator.py --type humanoid --pose attack --size 512x512
python scripts/template_generator.py --type quadruped --pose run --size 512x512
python scripts/template_generator.py --type bird --pose fly --size 512x512
```

## 工具管理系统

### 检查安装状态

```bash
python scripts/tool_manager.py --status
```

### 仅安装依赖

```bash
python scripts/tool_manager.py --install-deps
```

### 仅下载模型

```bash
python scripts/tool_manager.py --download-models
```

### 完整环境配置

```bash
python scripts/tool_manager.py --setup
```

## 模板系统工作原理

1. **用户输入** - 描述角色和动作
2. **智能识别** - 系统分析关键词，识别角色类型和姿势
3. **模板选择** - 自动选择匹配的骨架模板
4. **ControlNet应用** - 使用模板控制AI生成的姿态
5. **高质量输出** - 生成符合预期姿势的角色

### 优势

- **姿态准确** - 不再出现奇怪的肢体扭曲
- **风格一致** - 同一角色不同动作保持一致
- **效率提升** - 无需手动绘制骨架图
- **易于使用** - 完全自动化，无需额外操作

## 更新日志

### v2.1 (最新)
- ✅ 智能模板系统
- ✅ 自动角色类型识别
- ✅ 骨架模板生成器
- ✅ 工具自动下载和安装
- ✅ 一键环境配置
- ✅ 模板智能选择器

### v2.0
- ✅ 集成Stable Diffusion本地生成
- ✅ ControlNet姿态控制
- ✅ 8种经典游戏风格预设
- ✅ 智能提示词工程系统
- ✅ 高级后处理流水线
- ✅ 质量控制和自动评估
- ✅ 变体生成和自动筛选
- ✅ 修复所有编码问题
- ✅ 完整的中文支持
