---
name: 2d-game-asset-generator
description: 从文本描述或参数生成2D游戏素材，包括精灵、瓦片集、UI元素、背景和图标。当用户想要创建像素艺术精灵、角色动画、无缝瓦片地图、游戏UI组件、道具图标、背景场景或任何2D游戏视觉素材时使用此技能。支持多种美术风格（像素艺术、卡通、手绘）、游戏类型（RPG、平台跳跃、俯视角、解谜），并可导出Unity、Godot、Phaser等2D游戏引擎可用的素材。
---

# 2D游戏素材生成器

从自然语言描述生成可用于生产环境的2D游戏素材。此技能涵盖完整流程：提示词工程 → 图像生成 → 后处理 → 引擎就绪导出。

## 素材类型

| 类型 | 描述 | 常用尺寸 |
|------|------|--------------|
| **角色精灵** | 玩家、NPC、敌人及动画帧 | 32×32, 48×48, 64×64 |
| **精灵表** | 多帧动画条（待机/行走/攻击/受伤） | 256×64, 512×64, 1024×128 |
| **瓦片集** | 无缝地面、墙壁、装饰瓦片 | 每个瓦片16×16, 32×32 |
| **背景** | 视差层、场景背景 | 1920×1080, 2048×512 |
| **UI元素** | 按钮、面板、血条、图标 | 可变（支持9切片） |
| **道具图标** | 武器、药水、装备、收集品 | 16×16, 32×32, 64×64 |
| **特效精灵** | 爆炸、魔法、粒子 | 64×64, 128×128 |
| **道具/物体** | 宝箱、木桶、家具、装饰 | 32×32, 64×64 |

## 核心工作流程

### 步骤1 — 理解需求

从用户输入中识别：
- **素材类型**（精灵 / 瓦片集 / UI / 背景 / 图标 / 特效）
- **美术风格**（像素艺术 / 卡通 / 手绘 / 扁平 / 绘画风）
- **游戏类型**（RPG / 平台跳跃 / 俯视角 / 解谜 / 动作）
- **调色板**（暖色/冷色/暗色/亮色，或具体调色板名称）
- **目标引擎**（Unity / Godot / Phaser / GameMaker / 其他）
- **输出尺寸**（如未指定则使用上表中的标准尺寸）

如果用户提供的细节不足，询问：美术风格、素材类型和大致尺寸。不要问超过3个澄清问题。

### 步骤2 — 构建生成提示词

使用 `references/prompt-templates.md` 中的提示词模板。始终包含：
1. 素材类型关键词
2. 美术风格描述符
3. 主体描述（详细）
4. 技术约束（尺寸、透明背景、无文字）
5. 风格锁定（调色板、光照方向、轮廓样式）

**关键规则：**
- 对于精灵、图标和UI元素，始终指定 `透明背景`
- 始终指定 `无文字、无标签、无水印`
- 始终明确指定 `像素艺术` 或目标风格
- 锁定光照方向：`左上光源` 以保持一致性
- 对于精灵指定 `独立主体、居中构图`

### 步骤3 — 生成素材

使用图像生成脚本：`scripts/generate_asset.py`

```bash
python scripts/generate_asset.py \
  --type sprite \
  --prompt "pixel art warrior character, idle pose, blue armor, sword" \
  --style pixel-art \
  --size 64x64 \
  --output output/warrior_idle.png
```

批量生成（多个变体）：
```bash
python scripts/generate_asset.py \
  --type sprite \
  --prompt "pixel art warrior character, idle pose, blue armor, sword" \
  --style pixel-art \
  --size 64x64 \
  --count 4 \
  --output output/warrior_idle_batch/
```

### 步骤4 — 后处理

生成后，运行后处理以获得游戏就绪的输出：

```bash
# 移除背景并标准化尺寸
python scripts/post_process.py \
  --input output/warrior_idle.png \
  --size 64x64 \
  --remove-bg \
  --output output/warrior_idle_clean.png

# 从帧构建精灵表
python scripts/build_sprite_sheet.py \
  --frames-dir output/warrior_frames/ \
  --cols 4 \
  --rows 1 \
  --frame-size 64x64 \
  --output output/warrior_sheet.png
```

### 步骤5 — 引擎导出

为素材生成引擎元数据：

```bash
python scripts/export_for_engine.py \
  --asset output/warrior_sheet.png \
  --engine godot \
  --frame-size 64x64 \
  --animations "idle:0-3,walk:4-9,attack:10-15,hurt:16-18" \
  --output output/warrior_export/
```

## 美术风格指南

阅读 `references/art-styles.md` 获取详细的风格描述符和提示词修饰符：
- 像素艺术（8位、16位、32位）
- 卡通 / 矢量风格
- 手绘 / 素描
- 扁平设计
- 绘画风 / 水彩

## 提示词工程规则

阅读 `references/prompt-templates.md` 获取按素材类型分类的完整提示词模板。

**快速参考 — 始终包含的风格锁定：**
```
像素艺术风格，[尺寸]分辨率，透明背景，
左上光照，[轮廓样式]轮廓，有限调色板，
无文字，无水印，无背景场景，居中构图
```

## 质量检查清单

交付任何素材前，验证：
- [ ] 透明背景（主体后面无白色/彩色填充）
- [ ] 正确的像素尺寸（匹配请求的尺寸）
- [ ] 风格一致性（匹配美术风格描述符）
- [ ] 无文字、标签或水印
- [ ] 主体居中且正确取景
- [ ] 对于瓦片集：边缘无缝拼接（测试3×3网格）
- [ ] 对于精灵表：帧均匀间隔，尺寸相同
- [ ] 对于UI：9切片区域清晰定义

## 常见陷阱

- **风格不一致**：在一组素材中始终使用相同的风格描述符字符串
- **白色背景**：指定 `透明背景` 并使用PNG格式
- **模糊的像素艺术**：使用 `最近邻` 缩放，绝不使用双线性
- **比例漂移**：在一个请求中生成完整的动画条，而不是逐帧生成
- **错误的比例**：以512×512或更大尺寸生成，然后缩小到目标尺寸

## 引擎集成注意事项

- **Unity**：设置纹理类型 → 精灵，过滤模式 → 点（无过滤），所有精灵的PPU保持一致
- **Godot**：使用Sprite2D/AnimatedSprite2D，对像素艺术禁用纹理过滤，使用 `res://assets/` 文件夹结构
- **Phaser**：使用 `export_for_engine.py --engine phaser` 生成的纹理图集JSON（Phaser格式）
- **GameMaker**：导出为PNG条带，导入为精灵并设置帧尺寸

## 参考资料

- 按素材类型分类的提示词模板：`references/prompt-templates.md`
- 美术风格描述符：`references/art-styles.md`
- 引擎集成指南：`references/engine-integration.md`
- 调色板库：`references/palettes.md`
