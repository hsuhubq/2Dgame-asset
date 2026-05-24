# Art Style Reference Guide

Detailed style descriptors and prompt modifiers for each art style supported by the 2D game asset generator.

---

## 1. Pixel Art Styles

### 8-bit (NES / Game Boy Era)
- **Resolution**: 16×16 or 32×32 sprites
- **Colors**: 4–16 colors per sprite, very limited palette
- **Characteristics**: Hard edges, no anti-aliasing, chunky pixels, minimal shading
- **Prompt modifiers**: `8-bit pixel art, NES style, 4-color palette, chunky pixels, hard edges, no anti-aliasing, retro game aesthetic`
- **Best for**: Retro games, jam games, nostalgic aesthetics

### 16-bit (SNES / Mega Drive Era)
- **Resolution**: 32×32 or 48×48 sprites
- **Colors**: 16–32 colors per sprite
- **Characteristics**: More detail, subtle shading, dithering for gradients, defined outlines
- **Prompt modifiers**: `16-bit pixel art, SNES style, 16-color palette, subtle dithering, defined black outline, classic RPG aesthetic`
- **Best for**: RPGs, platformers, action games — the most versatile style

### 32-bit / Modern Pixel Art
- **Resolution**: 48×48 to 128×128 sprites
- **Colors**: 32–64 colors, rich palettes
- **Characteristics**: Detailed shading, hue shifting, anti-aliased outlines, painterly feel
- **Prompt modifiers**: `modern pixel art, 32-bit style, rich color palette, hue-shifted shading, detailed pixel clusters, indie game aesthetic`
- **Best for**: Modern indie games, detailed characters, high-quality assets

### Isometric Pixel Art
- **View**: 2:1 isometric projection (26.565° angle)
- **Characteristics**: Consistent 2:1 diamond grid, top/left/right face shading
- **Prompt modifiers**: `isometric pixel art, 2:1 isometric view, top-down 45-degree angle, three-face shading (top bright, left medium, right dark), isometric game tile`
- **Best for**: Strategy games, city builders, RPGs with isometric view

---

## 2. Cartoon / Vector-Style

### Flat Cartoon
- **Characteristics**: Bold outlines, flat colors, minimal shading, simple shapes
- **Prompt modifiers**: `flat cartoon style, bold black outline, flat colors, no gradients, simple shapes, mobile game aesthetic, bright saturated colors`
- **Best for**: Mobile games, casual games, children's games

### Rounded Cartoon
- **Characteristics**: Soft rounded shapes, gradient shading, friendly aesthetic
- **Prompt modifiers**: `rounded cartoon style, soft edges, gradient shading, friendly character design, pastel colors, cute game aesthetic`
- **Best for**: Casual games, puzzle games, family-friendly titles

### Comic Book Style
- **Characteristics**: Strong outlines, cel shading, dynamic poses, high contrast
- **Prompt modifiers**: `comic book style, strong black outline, cel shading, high contrast, dynamic composition, action game aesthetic`
- **Best for**: Action games, superhero games, beat-em-ups

---

## 3. Hand-Drawn / Sketch

### Pencil Sketch
- **Characteristics**: Visible pencil strokes, rough edges, organic feel
- **Prompt modifiers**: `hand-drawn pencil sketch style, visible pencil strokes, rough organic edges, sketch aesthetic, indie game art`
- **Best for**: Puzzle games, narrative games, artistic indie titles

### Ink & Watercolor
- **Characteristics**: Ink outlines with watercolor fills, soft color bleeding
- **Prompt modifiers**: `ink and watercolor style, black ink outline, soft watercolor fill, color bleeding effect, painterly game aesthetic`
- **Best for**: Story-driven games, atmospheric titles, artistic games

---

## 4. Flat Design

### Material Design Game Style
- **Characteristics**: Clean geometric shapes, flat colors, subtle shadows, minimal detail
- **Prompt modifiers**: `flat design style, geometric shapes, flat colors, subtle drop shadow, minimal detail, clean modern aesthetic, mobile UI game`
- **Best for**: Puzzle games, hyper-casual games, UI-heavy games

---

## 5. Painterly

### Digital Painting
- **Characteristics**: Brush strokes visible, rich textures, painterly shading
- **Prompt modifiers**: `digital painting style, visible brush strokes, rich texture, painterly shading, detailed illustration, RPG concept art style`
- **Best for**: Backgrounds, cutscenes, high-detail environments

---

## Style Comparison Quick Reference

| Style | Detail Level | Colors | Best Asset Types | Performance Cost |
|-------|-------------|--------|-----------------|-----------------|
| 8-bit pixel art | Low | 4–16 | Sprites, tiles | Very low |
| 16-bit pixel art | Medium | 16–32 | All types | Low |
| Modern pixel art | High | 32–64 | Characters, UI | Low-Medium |
| Isometric pixel | Medium-High | 16–32 | Tiles, props | Low |
| Flat cartoon | Low-Medium | 8–24 | UI, mobile | Very low |
| Rounded cartoon | Medium | 16–32 | Characters | Low |
| Hand-drawn | High | Variable | Backgrounds | Medium |
| Painterly | Very High | Full | Backgrounds | High |

---

## Palette Families

### Fantasy RPG Palettes
- **Warm Dungeon**: `#2C1810, #5C3317, #8B6914, #C8A84B, #E8D5A3` — torchlit stone
- **Forest Green**: `#1A3A1A, #2D5A27, #4A8C3F, #7BC67A, #B8E6B0` — outdoor nature
- **Magic Purple**: `#1A0A2E, #3D1A6E, #7B3FA0, #B87FD4, #E8C8F0` — arcane magic

### Sci-Fi Palettes
- **Neon Cyber**: `#0A0A1A, #1A1A3E, #0066FF, #00FFCC, #FF0066` — cyberpunk
- **Space Dark**: `#050510, #0A0A2A, #1A1A4A, #4A4A8A, #8A8ACA` — deep space

### Casual / Mobile Palettes
- **Bright Arcade**: `#FF4444, #FF8800, #FFDD00, #44BB44, #4488FF` — vibrant primary
- **Pastel Soft**: `#FFB3BA, #FFDFBA, #FFFFBA, #BAFFC9, #BAE1FF` — gentle pastel

### Retro Palettes
- **NES**: 54-color NES hardware palette — authentic 8-bit
- **Game Boy**: `#0F380F, #306230, #8BAC0F, #9BBC0F` — classic green LCD
- **CGA**: `#000000, #555555, #AAAAAA, #FFFFFF, #FF5555, #55FFFF` — PC retro
