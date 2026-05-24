# 2D游戏素材生成器

一个完整的2D游戏素材生成工具链，支持从文本描述生成精灵、瓦片集、UI元素、背景和图标。

## 功能特性

### 🎨 素材类型支持
- **角色精灵** - 玩家、NPC、敌人角色
- **精灵表** - 多帧动画序列
- **瓦片集** - 无缝地图瓦片
- **背景** - 场景背景和视差层
- **UI元素** - 按钮、面板、血条
- **道具图标** - 武器、药水、装备
- **特效精灵** - 爆炸、魔法、粒子效果

### 🛠️ 完整工作流程
1. **提示词工程** - 智能构建生成提示词
2. **图像生成** - 支持多种生成后端
3. **后处理** - 像素化、调色板匹配、AI抠图
4. **质量控制** - 自动评估生成质量
5. **引擎导出** - 支持Unity、Godot等游戏引擎

### 🎯 美术风格预设
- **经典像素艺术** - Chrono Trigger风格
- **现代像素艺术** - Celeste风格
- **手绘风格** - Hollow Knight风格
- **温馨像素** - Stardew Valley风格
- **简约风格** - Undertale风格
- **复古风格** - Shovel Knight风格
- **动作风格** - Dead Cells风格
- **沙盒风格** - Terraria风格

## 快速开始

### 1. 安装依赖
```bash
# 使用改进的安装脚本（推荐）
python install_deps.py

# 或使用原始安装脚本
python setup.py
```

### 2. 生成测试素材
```bash
# 生成骑士角色精灵
python scripts/generate_asset.py --subject "勇敢的骑士" --style chrono-trigger --output output/knight.png

# 生成草地瓦片
python scripts/generate_asset.py --subject "草地地面" --type tileset --style stardew-valley --output output/grass_tile.png

# 生成UI按钮
python scripts/generate_asset.py --subject "中世纪按钮" --type ui --style shovel-knight --output output/button.png
```

### 3. 后处理
```bash
# 移除背景并调整尺寸
python scripts/advanced_post_process.py --input output/knight.png --output output/knight_processed.png --remove-bg --auto-crop

# 应用像素艺术调色板
python scripts/advanced_post_process.py --input output/knight.png --output output/knight_pixel.png --pixelate 4 --palette pico-8
```

## 详细使用

### 生成编排器
```bash
python scripts/generate_asset.py --help
```

主要参数：
- `--subject` - 主体描述（必需）
- `--type` - 素材类型（sprite/tileset/ui/icon/background/effect）
- `--style` - 风格预设
- `--size` - 输出尺寸（如64x64）
- `--output` - 输出文件路径
- `--backend` - 生成后端（mock/sd-local/dalle/sd-api）

### 后处理流水线
```bash
python scripts/advanced_post_process.py --help
```

后处理功能：
- `--remove-bg` - 移除背景
- `--pixelate` - 像素化大小
- `--palette` - 调色板名称
- `--outline` - 添加轮廓
- `--auto-crop` - 自动裁剪透明边缘
- `--target-size` - 目标画布尺寸

### 质量控制
```bash
python scripts/quality_control.py --input output/knight.png --expected-size 64x64
```

质量检查项目：
- 透明度检查
- 尺寸验证
- 颜色数量限制
- 边缘清晰度
- 主体居中

## 项目结构

```
2d-game-asset-generator/
├── scripts/                    # 核心脚本
│   ├── generate_asset.py      # 生成编排器
│   ├── prompt_engineer.py     # 提示词工程
│   ├── advanced_post_process.py # 后处理
│   ├── quality_control.py     # 质量控制
│   ├── mock_backend.py        # 模拟后端
│   └── ...其他脚本
├── references/                # 参考资料
│   ├── art-styles.md         # 美术风格指南
│   ├── prompt-templates.md   # 提示词模板
│   ├── palettes.md           # 调色板库
│   └── engine-integration.md # 引擎集成
├── config_simple.json        # 简化配置文件
├── generation_config.json    # 完整配置文件
├── requirements.txt          # Python依赖
├── install_deps.py          # 改进的依赖安装
├── setup.py                 # 一键安装脚本
└── QUICK_START.md          # 快速开始指南
```

## 配置说明

### 后端选择
项目支持多种生成后端：

1. **模拟后端**（默认）
   - 无需AI API密钥
   - 生成简单的测试图像
   - 用于了解工作流程

2. **自定义后端集成**
   - 可集成任何图像生成API
   - 支持自定义生成函数
   - 详见代码注释

### 配置文件
- `config_simple.json` - 简化配置（推荐）
- `generation_config.json` - 完整配置（含详细说明）

## 开发指南

### 添加新的风格预设
1. 编辑 `scripts/prompt_engineer.py` 中的 `STYLE_PRESETS` 字典
2. 添加新的风格描述和技术参数
3. 更新 `references/art-styles.md` 文档

### 扩展后处理功能
1. 在 `scripts/advanced_post_process.py` 中添加新的处理方法
2. 更新 `AdvancedPostProcessor` 类
3. 添加相应的命令行参数

### 集成新的生成后端
1. 在 `scripts/generate_asset.py` 中添加新的生成函数
2. 更新 `select_backend` 方法
3. 创建对应的生成脚本

## 常见问题

### Q: 安装依赖时超时怎么办？
A: 使用 `install_deps.py` 脚本，它支持重试机制和国内镜像源。

### Q: Windows中文显示乱码？
A: 已修复编码问题，如果仍有问题，请确保系统区域设置为中文。

### Q: 如何生成动画序列？
A: 使用 `generate_animation` 方法或查看 `examples_advanced.py`。

### Q: 如何导出到游戏引擎？
A: 使用 `scripts/export_for_engine.py` 脚本，支持Unity、Godot等引擎。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 支持

- 查看 `examples.py` 了解完整工作流程
- 查看 `references/` 文件夹获取详细指南
- 查看 `QUICK_START.md` 获取快速开始说明
