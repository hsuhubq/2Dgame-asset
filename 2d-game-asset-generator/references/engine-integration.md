# 游戏引擎集成指南

如何将生成的素材导入各主流2D游戏引擎。

---

## Unity

### 导入精灵

1. 将PNG文件拖入 `Assets/Sprites/` 文件夹
2. 选中素材，在Inspector中设置：
   - **Texture Type**: Sprite (2D and UI)
   - **Sprite Mode**: Single（单帧）或 Multiple（精灵表）
   - **Pixels Per Unit**: 根据你的游戏设置（通常32或64）
   - **Filter Mode**: Point (no filter) - 像素艺术必须！
   - **Compression**: None

### 精灵表设置

1. Sprite Mode 选择 Multiple
2. 点击 Sprite Editor
3. 使用 Slice 工具：
   - Grid By Cell Size
   - 输入单帧尺寸（如64x64）
4. 命名每个精灵（idle_0, idle_1等）

### 动画

1. 选中精灵表中的所有帧
2. 拖到Hierarchy中的GameObject上
3. Unity会自动创建Animator和Animation Clip
4. 在Animation窗口调整帧率（通常10-12 FPS）

---

## Godot

### 导入精灵

1. 将PNG文件复制到 `res://assets/sprites/`
2. Godot会自动导入
3. 对于像素艺术，创建 `.import` 文件或在导入设置中：
   - **Filter**: Off（关闭过滤）
   - **Mipmaps**: Off

### 使用Sprite2D

```gdscript
extends Sprite2D

func _ready():
    texture = load("res://assets/sprites/character.png")
    # 关闭纹理过滤（像素艺术）
    texture_filter = TEXTURE_FILTER_NEAREST
```

### 使用AnimatedSprite2D

1. 创建 AnimatedSprite2D 节点
2. 创建 SpriteFrames 资源
3. 添加动画（idle, walk, attack等）
4. 为每个动画添加帧
5. 设置FPS（通常10）

```gdscript
extends AnimatedSprite2D

func _ready():
    play("idle")
    
func _process(delta):
    if Input.is_action_pressed("ui_right"):
        play("walk")
    else:
        play("idle")
```

### 使用导出脚本

```bash
python scripts/export_for_engine.py \
  --asset output/warrior_sheet.png \
  --engine godot \
  --frame-size 64x64 \
  --animations "idle:0-3,walk:4-9,attack:10-15" \
  --output output/godot_export/
```

生成的 `.tres` 文件可直接在Godot中使用。

---

## Phaser 3

### 加载精灵表

```javascript
class GameScene extends Phaser.Scene {
    preload() {
        // 加载精灵表和JSON
        this.load.atlas(
            'character',
            'assets/character.png',
            'assets/character.json'
        );
    }
    
    create() {
        // 创建精灵
        const player = this.add.sprite(400, 300, 'character');
        
        // 创建动画
        this.anims.create({
            key: 'idle',
            frames: this.anims.generateFrameNames('character', {
                prefix: 'idle_',
                start: 0,
                end: 3
            }),
            frameRate: 10,
            repeat: -1
        });
        
        this.anims.create({
            key: 'walk',
            frames: this.anims.generateFrameNames('character', {
                prefix: 'walk_',
                start: 0,
                end: 5
            }),
            frameRate: 10,
            repeat: -1
        });
        
        player.play('idle');
    }
}
```

### 使用导出脚本

```bash
python scripts/export_for_engine.py \
  --asset output/warrior_sheet.png \
  --engine phaser \
  --frame-size 64x64 \
  --animations "idle:0-3,walk:4-9,attack:10-15" \
  --output output/phaser_export/
```

---

## GameMaker Studio 2

### 导入精灵

1. 右键 Sprites 文件夹 → Create Sprite
2. Import Strip Image
3. 设置：
   - **Number of frames**: 帧数
   - **Frames per row**: 每行帧数
   - **Image speed**: 动画速度（通常10-12）
   - **Separate Texture Page**: 勾选（性能优化）

### 像素艺术设置

在 Sprite 属性中：
- 取消勾选 **Separate Texture Page** 下的 **Interpolate**
- 在 Game Options → Graphics 中设置 **Interpolate colors between pixels**: Off

---

## Construct 3

### 导入精灵

1. 右键 Project → Import files
2. 选择PNG文件
3. 在Animation Editor中：
   - 点击 Import frames → Import sprite strip
   - 设置列数和行数
   - 设置帧率（通常10）

### 像素艺术设置

在 Project Properties 中：
- **Sampling**: Nearest（像素艺术必须）
- **Pixel rounding**: On

---

## 通用最佳实践

### 文件组织

```
assets/
├── sprites/
│   ├── characters/
│   │   ├── player_idle.png
│   │   ├── player_walk.png
│   │   └── player_attack.png
│   ├── enemies/
│   ├── items/
│   └── effects/
├── tilesets/
│   ├── dungeon.png
│   └── forest.png
├── ui/
│   ├── buttons/
│   └── panels/
└── backgrounds/
    ├── sky.png
    └── mountains.png
```

### 命名规范

- 使用小写和下划线：`player_idle.png`
- 包含尺寸信息：`icon_32x32.png`
- 动画帧编号：`walk_00.png`, `walk_01.png`
- 变体标记：`sword_iron.png`, `sword_steel.png`

### 性能优化

1. **纹理图集**：将多个小图合并成一张大图
2. **2的幂次尺寸**：64x64, 128x128, 256x256（GPU友好）
3. **压缩**：非像素艺术可使用PNG压缩工具
4. **透明度**：只在需要时使用RGBA，否则用RGB

### 像素艺术特殊注意

- **必须关闭纹理过滤**（Nearest/Point采样）
- **必须关闭抗锯齿**
- **像素对齐**：坐标使用整数，避免半像素偏移
- **统一PPU**：同一游戏中所有精灵使用相同的Pixels Per Unit

---

## 故障排查

### 问题：精灵模糊

**原因**：纹理过滤开启  
**解决**：设置为 Point/Nearest 采样

### 问题：动画不流畅

**原因**：帧率不匹配  
**解决**：统一使用10-12 FPS

### 问题：精灵边缘有白边

**原因**：背景未正确移除  
**解决**：使用 `post_process.py --remove-bg`

### 问题：精灵尺寸不一致

**原因**：生成时未锁定尺寸  
**解决**：使用 `post_process.py --size 64x64` 统一调整
