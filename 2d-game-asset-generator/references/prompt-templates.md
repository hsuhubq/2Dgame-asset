# Prompt Templates for 2D Game Asset Generation

This file contains battle-tested prompt templates for each asset type. Copy and fill in the `[BRACKETS]`.

---

## Universal Style Lock String

Always append this to every prompt for consistency within a project:

```
pixel art style, [BIT_DEPTH]-bit aesthetic, [PALETTE_NAME] color palette, 
top-left light source, [OUTLINE] outline, no anti-aliasing, 
transparent background, no text, no watermarks, no background scenery,
centered composition, isolated subject
```

**BIT_DEPTH options**: `8` (NES/GB era), `16` (SNES/GBA era), `32` (modern pixel art)  
**OUTLINE options**: `single-pixel black`, `single-pixel dark`, `no`, `colored`  
**PALETTE_NAME options**: `warm earthy`, `cool fantasy`, `dark dungeon`, `bright arcade`, `pastel`, `monochrome`

---

## 1. Character Sprite (Single Frame)

### Template
```
Pixel art [CHARACTER_TYPE] character sprite, [POSE] pose, [FACING] facing direction,
[DESCRIPTION_OF_CHARACTER], [ARMOR/CLOTHING], [WEAPON/ACCESSORY],
[SIZE]x[SIZE] pixel art, transparent background, single-pixel black outline,
top-left light source, [PALETTE] color palette, no background, centered,
game sprite style, [BIT_DEPTH]-bit aesthetic, no text, no labels
```

### Examples
```
Pixel art warrior character sprite, idle pose, front-facing,
muscular build, blue steel plate armor, longsword in right hand,
64x64 pixel art, transparent background, single-pixel black outline,
top-left light source, cool steel color palette, no background, centered,
game sprite style, 16-bit aesthetic, no text, no labels
```

```
Pixel art female mage character sprite, casting pose, side-facing left,
slender build, purple robes with gold trim, magic staff, glowing orb,
48x48 pixel art, transparent background, single-pixel dark outline,
top-left light source, purple and gold color palette, no background, centered,
game sprite style, 16-bit aesthetic, no text, no labels
```

---

## 2. Character Sprite Sheet (Animation Strip)

### Template — Horizontal Strip
```
Pixel art [CHARACTER_TYPE] sprite sheet, [ANIMATION_NAME] animation,
[FRAME_COUNT] frames in a horizontal strip, [FACING] facing direction,
[CHARACTER_DESCRIPTION], [SIZE]x[SIZE] per frame, [TOTAL_WIDTH]x[SIZE] total,
each frame evenly spaced, same character proportions across all frames,
transparent background, single-pixel black outline, top-left light source,
[PALETTE] color palette, no background, no text, no labels, game sprite sheet
```

### Animation-Specific Examples

**Idle (4 frames)**
```
Pixel art knight sprite sheet, idle breathing animation,
4 frames in a horizontal strip, front-facing,
silver armor, shield and sword, 64x64 per frame, 256x64 total,
subtle chest rise and fall motion, slight weapon sway,
transparent background, single-pixel black outline, top-left light source,
cool metallic color palette, no background, no text, game sprite sheet
```

**Walk Cycle (6 frames)**
```
Pixel art adventurer sprite sheet, walk cycle animation,
6 frames in a horizontal strip, side-facing right,
green tunic, leather boots, backpack, 48x48 per frame, 288x48 total,
smooth walking motion with arm and leg swing,
transparent background, single-pixel black outline, top-left light source,
warm earthy color palette, no background, no text, game sprite sheet
```

**Attack (5 frames)**
```
Pixel art samurai sprite sheet, sword slash attack animation,
5 frames in a horizontal strip, side-facing right,
red kimono, katana, 64x64 per frame, 320x64 total,
wind-up, swing, follow-through motion sequence,
transparent background, single-pixel black outline, top-left light source,
red and black color palette, no background, no text, game sprite sheet
```

**Hurt/Death (3 frames)**
```
Pixel art goblin sprite sheet, hurt reaction animation,
3 frames in a horizontal strip, front-facing,
ragged clothes, club weapon, 32x32 per frame, 96x32 total,
recoil backward motion, flash of pain,
transparent background, single-pixel black outline, top-left light source,
green and brown color palette, no background, no text, game sprite sheet
```

---

## 3. Tileset

### Ground Tile (Seamless)
```
Pixel art seamless [TERRAIN_TYPE] ground tile, top-down view,
[SIZE]x[SIZE] pixels, tileable texture that repeats without visible seams,
[DESCRIPTION], [PALETTE] color palette, top-left light source,
no characters, no objects, no text, flat ground surface,
game tileset style, [BIT_DEPTH]-bit aesthetic, matte finish
```

**Examples:**
```
Pixel art seamless grass ground tile, top-down view,
32x32 pixels, tileable texture that repeats without visible seams,
lush green grass with subtle variation, small flowers occasionally,
warm green color palette, top-left light source,
no characters, no objects, no text, flat ground surface,
game tileset style, 16-bit aesthetic, matte finish
```

```
Pixel art seamless stone dungeon floor tile, top-down view,
32x32 pixels, tileable texture that repeats without visible seams,
cracked grey stone blocks with mortar lines, slight moss,
dark grey and brown color palette, top-left light source,
no characters, no objects, no text, flat ground surface,
game tileset style, 16-bit aesthetic, matte finish
```

### Wall Tile
```
Pixel art [MATERIAL] wall tile, [VIEW] view,
[SIZE]x[SIZE] pixels, clear impassable boundary appearance,
[DESCRIPTION], [PALETTE] color palette, top-left light source,
solid block shape, no transparency, no characters, no text,
game tileset style, [BIT_DEPTH]-bit aesthetic
```

### Tileset Sheet (Multiple Tiles)
```
Pixel art [THEME] tileset sheet, top-down RPG style,
[COLS]x[ROWS] grid of [SIZE]x[SIZE] tiles, [TOTAL_WIDTH]x[TOTAL_HEIGHT] total,
includes: ground tiles, wall tiles, corner pieces, transition tiles,
[PALETTE] color palette, consistent top-left lighting,
seamless edges between matching tiles, no text, no labels,
game tileset style, [BIT_DEPTH]-bit aesthetic
```

---

## 4. Background / Scene

### Parallax Layer
```
Pixel art [LAYER_TYPE] background layer, [SCENE_TYPE] scene,
[WIDTH]x[HEIGHT] pixels, horizontally tileable,
[DESCRIPTION], [TIME_OF_DAY] lighting, [PALETTE] color palette,
[LAYER_DEPTH] depth (far/mid/near), no characters, no UI elements,
game background style, [BIT_DEPTH]-bit aesthetic, [MOOD] atmosphere
```

**Examples:**
```
Pixel art sky background layer, fantasy forest scene,
1920x360 pixels, horizontally tileable,
gradient blue sky with fluffy white clouds, distant mountains silhouette,
golden hour lighting, warm blue and orange color palette,
far depth layer, no characters, no UI elements,
game background style, 16-bit aesthetic, peaceful atmosphere
```

```
Pixel art midground background layer, dark dungeon scene,
1920x360 pixels, horizontally tileable,
stone pillars, hanging torches with glow, cobwebs, distant archways,
dim torch lighting, dark grey and orange color palette,
mid depth layer, no characters, no UI elements,
game background style, 16-bit aesthetic, ominous atmosphere
```

---

## 5. UI Elements

### Button
```
Pixel art game UI button, [STYLE] style, [STATE] state,
[WIDTH]x[HEIGHT] pixels, [SHAPE] shape,
[MATERIAL/TEXTURE] appearance, [COLOR] color scheme,
9-slice compatible borders, no text, no labels,
game UI style, [BIT_DEPTH]-bit aesthetic, [THEME] theme
```

**Examples:**
```
Pixel art game UI button, medieval fantasy style, normal state,
128x32 pixels, rectangular shape with rounded corners,
carved stone appearance with gold trim, brown and gold color scheme,
9-slice compatible borders, no text, no labels,
game UI style, 16-bit aesthetic, RPG theme
```

### Panel / Window
```
Pixel art game UI panel, [STYLE] style,
[WIDTH]x[HEIGHT] pixels, [SHAPE] shape,
[MATERIAL] frame with [FILL] interior,
9-slice compatible, decorative corners, no text,
game UI style, [BIT_DEPTH]-bit aesthetic, [THEME] theme
```

### Health Bar / Progress Bar
```
Pixel art game UI health bar, [STYLE] style,
[WIDTH]x[HEIGHT] pixels, horizontal bar,
[COLOR] fill color, [BORDER_COLOR] border, [BACKGROUND_COLOR] empty background,
segmented or smooth fill, no text, no numbers,
game UI style, [BIT_DEPTH]-bit aesthetic
```

### HUD Icon
```
Pixel art game UI icon, [ICON_TYPE],
[SIZE]x[SIZE] pixels, [STYLE] style,
[DESCRIPTION], [COLOR] color scheme,
transparent background, clear silhouette readable at small size,
no text, no labels, game icon style, [BIT_DEPTH]-bit aesthetic
```

---

## 6. Item Icons

### Template
```
Pixel art game item icon, [ITEM_TYPE],
[SIZE]x[SIZE] pixels, [STYLE] style,
[DETAILED_DESCRIPTION], [MATERIAL], [COLOR_SCHEME],
transparent background, single-pixel [OUTLINE_COLOR] outline,
top-left light source, centered composition,
no text, no labels, game inventory icon style, [BIT_DEPTH]-bit aesthetic
```

### Examples
```
Pixel art game item icon, iron longsword,
32x32 pixels, RPG style,
straight double-edged blade, simple crossguard, wrapped leather grip,
grey iron metal with slight shine, silver and brown color scheme,
transparent background, single-pixel black outline,
top-left light source, centered composition,
no text, no labels, game inventory icon style, 16-bit aesthetic
```

```
Pixel art game item icon, health potion,
32x32 pixels, RPG style,
round glass bottle with cork stopper, glowing red liquid inside,
glass transparency effect, red and clear color scheme,
transparent background, single-pixel black outline,
top-left light source, centered composition,
no text, no labels, game inventory icon style, 16-bit aesthetic
```

---

## 7. Effect / Particle Sprites

### Template
```
Pixel art [EFFECT_TYPE] effect sprite sheet,
[FRAME_COUNT] frames in horizontal strip, [SIZE]x[SIZE] per frame,
[DESCRIPTION], [COLOR_SCHEME],
transparent background, no outline (or soft glow outline),
additive blend ready, bright saturated colors,
no text, no labels, game VFX sprite style, [BIT_DEPTH]-bit aesthetic
```

### Examples
```
Pixel art fire explosion effect sprite sheet,
8 frames in horizontal strip, 64x64 per frame,
expanding fireball with smoke, orange and yellow flames, dark smoke,
transparent background, no hard outline, soft glow effect,
additive blend ready, bright orange and yellow colors,
no text, no labels, game VFX sprite style, 16-bit aesthetic
```

```
Pixel art magic sparkle effect sprite sheet,
6 frames in horizontal strip, 32x32 per frame,
twinkling star burst with trailing particles, blue and white glow,
transparent background, soft glow outline,
additive blend ready, bright blue and white colors,
no text, no labels, game VFX sprite style, 16-bit aesthetic
```

---

## 8. Props and Objects

### Template
```
Pixel art [OBJECT_TYPE] game prop, top-down [OR side] view,
[SIZE]x[SIZE] pixels, [STYLE] style,
[DETAILED_DESCRIPTION], [MATERIAL], [COLOR_SCHEME],
transparent background, single-pixel [OUTLINE_COLOR] outline,
top-left light source, centered composition,
no text, no labels, game prop style, [BIT_DEPTH]-bit aesthetic
```

### Examples
```
Pixel art treasure chest game prop, 3/4 top-down view,
32x32 pixels, RPG style,
wooden chest with iron bands and gold lock, closed lid,
aged wood texture, brown and gold color scheme,
transparent background, single-pixel black outline,
top-left light source, centered composition,
no text, no labels, game prop style, 16-bit aesthetic
```

---

## Style Consistency Across Asset Sets

When generating multiple assets for the same game, use a **Style Lock String** — a fixed phrase appended to every prompt:

```
[GAME_NAME] game style, [BIT_DEPTH]-bit pixel art, [PALETTE_DESCRIPTION] palette,
top-left light source, single-pixel [OUTLINE_COLOR] outline,
[RESOLUTION] base resolution, [MOOD] atmosphere
```

**Example Style Lock:**
```
"Dungeon Quest" game style, 16-bit pixel art, warm earthy dungeon palette,
top-left light source, single-pixel black outline,
32x32 base resolution, dark fantasy atmosphere
```

Save this string and prepend it to every asset prompt in the project.
