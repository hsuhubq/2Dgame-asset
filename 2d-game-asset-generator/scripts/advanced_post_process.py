#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""高级后处理流水线 - 像素化、调色板匹配、AI抠图"""

import sys
import os
import numpy as np
from PIL import Image
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 预定义调色板
PALETTES = {
    'pico-8': [
        (0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81),
        (171, 82, 54), (95, 87, 79), (194, 195, 199), (255, 241, 232),
        (255, 0, 77), (255, 163, 0), (255, 236, 39), (0, 228, 54),
        (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170)
    ],
    'nes': [
        (124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
        (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
        (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
        (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (188, 188, 188), (0, 120, 248), (0, 88, 248), (104, 68, 252),
        (216, 0, 204), (228, 0, 88), (248, 56, 0), (228, 92, 16),
        (172, 124, 0), (0, 184, 0), (0, 168, 0), (0, 168, 68),
        (0, 136, 136), (0, 0, 0), (0, 0, 0), (0, 0, 0),
        (248, 248, 248), (60, 188, 252), (104, 136, 252), (152, 120, 248),
        (248, 120, 248), (248, 88, 152), (248, 120, 88), (252, 160, 68),
        (248, 184, 0), (184, 248, 24), (88, 216, 84), (88, 248, 152),
        (0, 232, 216), (120, 120, 120), (0, 0, 0), (0, 0, 0),
        (252, 252, 252), (164, 228, 252), (184, 184, 248), (216, 184, 248),
        (248, 184, 248), (248, 164, 192), (240, 208, 176), (252, 224, 168),
        (248, 216, 120), (216, 248, 120), (184, 248, 184), (184, 248, 216),
        (0, 252, 252), (248, 216, 248), (0, 0, 0), (0, 0, 0)
    ],
    'gameboy': [
        (15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)
    ],
    'warm-dungeon': [
        (44, 24, 16), (92, 51, 23), (139, 105, 20), (200, 168, 75), (232, 213, 163)
    ],
    'cool-fantasy': [
        (26, 58, 26), (45, 90, 39), (74, 140, 63), (123, 198, 122), (184, 230, 176)
    ]
}

class AdvancedPostProcessor:
    """高级后处理器"""
    
    def __init__(self):
        pass
    
    def pixelate(self, image, pixel_size=4, color_depth=32):
        """像素化处理"""
        
        print(f"[像素化] 像素大小: {pixel_size}x{pixel_size}, 色深: {color_depth}")
        
        # 缩小图像
        small_size = (image.width // pixel_size, image.height // pixel_size)
        small_img = image.resize(small_size, Image.NEAREST)
        
        # 颜色量化
        if color_depth < 256:
            small_img = small_img.quantize(colors=color_depth, method=2)
            small_img = small_img.convert('RGB')
        
        # 放大回原尺寸
        pixelated = small_img.resize(image.size, Image.NEAREST)
        
        return pixelated
    
    def apply_palette(self, image, palette_name='pico-8'):
        """应用调色板映射"""
        
        if palette_name not in PALETTES:
            print(f"[警告] 未知调色板: {palette_name}")
            return image
        
        print(f"[调色板] 应用: {palette_name}")
        
        palette = PALETTES[palette_name]
        img_array = np.array(image.convert('RGB'))
        
        # 创建输出数组
        output = np.zeros_like(img_array)
        
        # 对每个像素找到最接近的调色板颜色
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                pixel = img_array[i, j]
                
                # 计算与调色板中每个颜色的距离
                distances = [
                    np.sqrt(np.sum((pixel - np.array(color)) ** 2))
                    for color in palette
                ]
                
                # 选择最近的颜色
                closest_idx = np.argmin(distances)
                output[i, j] = palette[closest_idx]
        
        return Image.fromarray(output.astype('uint8'))
    
    def remove_background_ai(self, image):
        """AI抠图"""
        
        try:
            from rembg import remove
            print("[AI抠图] 使用rembg")
            return remove(image)
        except ImportError:
            print("[警告] rembg未安装，使用简单方法")
            return self.remove_background_simple(image)
    
    def remove_background_simple(self, image, threshold=240):
        """简单背景移除"""
        
        print(f"[背景移除] 阈值: {threshold}")
        
        img = image.convert("RGBA")
        data = np.array(img)
        
        # 检测白色背景
        white_mask = (data[:, :, 0] > threshold) & \
                     (data[:, :, 1] > threshold) & \
                     (data[:, :, 2] > threshold)
        
        # 设置为透明
        data[white_mask, 3] = 0
        
        return Image.fromarray(data)
    
    def add_outline(self, image, outline_color=(0, 0, 0), thickness=1):
        """添加轮廓"""
        
        print(f"[轮廓] 颜色: {outline_color}, 粗细: {thickness}")
        
        img_array = np.array(image.convert('RGBA'))
        alpha = img_array[:, :, 3]
        
        # 创建轮廓mask
        from scipy import ndimage
        
        # 膨胀alpha通道
        dilated = ndimage.binary_dilation(alpha > 0, iterations=thickness)
        
        # 轮廓 = 膨胀 - 原始
        outline_mask = dilated & (alpha == 0)
        
        # 应用轮廓颜色
        img_array[outline_mask] = list(outline_color) + [255]
        
        return Image.fromarray(img_array)
    
    def auto_crop(self, image, padding=2):
        """自动裁剪透明边缘"""
        
        print(f"[裁剪] 边距: {padding}px")
        
        img_array = np.array(image.convert('RGBA'))
        alpha = img_array[:, :, 3]
        
        # 找到非透明区域
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        
        if not rows.any() or not cols.any():
            return image
        
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        # 添加边距
        rmin = max(0, rmin - padding)
        rmax = min(img_array.shape[0], rmax + padding + 1)
        cmin = max(0, cmin - padding)
        cmax = min(img_array.shape[1], cmax + padding + 1)
        
        cropped = img_array[rmin:rmax, cmin:cmax]
        
        return Image.fromarray(cropped)
    
    def resize_canvas(self, image, target_size, center=True):
        """调整画布大小（保持内容）"""
        
        print(f"[画布] 目标尺寸: {target_size}")
        
        width, height = map(int, target_size.split('x'))
        
        # 创建新画布
        canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # 计算粘贴位置
        if center:
            x = (width - image.width) // 2
            y = (height - image.height) // 2
        else:
            x, y = 0, 0
        
        canvas.paste(image, (x, y), image if image.mode == 'RGBA' else None)
        
        return canvas
    
    def process_pipeline(
        self,
        input_path,
        output_path,
        pixelate_size=None,
        palette=None,
        remove_bg=False,
        add_outline_flag=False,
        auto_crop_flag=False,
        target_size=None
    ):
        """完整处理流水线"""
        
        print(f"\n[流水线] 开始处理: {input_path}")
        
        # 加载图像
        image = Image.open(input_path)
        
        # 1. 移除背景
        if remove_bg:
            image = self.remove_background_ai(image)
        
        # 2. 像素化
        if pixelate_size:
            image = self.pixelate(image, pixel_size=pixelate_size)
        
        # 3. 应用调色板
        if palette:
            # 保存alpha通道
            if image.mode == 'RGBA':
                alpha = image.split()[3]
                image = self.apply_palette(image, palette)
                image.putalpha(alpha)
            else:
                image = self.apply_palette(image, palette)
        
        # 4. 自动裁剪
        if auto_crop_flag:
            image = self.auto_crop(image)
        
        # 5. 添加轮廓
        if add_outline_flag:
            image = self.add_outline(image)
        
        # 6. 调整画布
        if target_size:
            image = self.resize_canvas(image, target_size)
        
        # 保存
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        image.save(output_path, 'PNG')
        print(f"[完成] 已保存: {output_path}\n")
        
        return image

def main():
    import argparse
    parser = argparse.ArgumentParser(description='高级后处理流水线')
    parser.add_argument('--input', required=True, help='输入图像路径')
    parser.add_argument('--output', required=True, help='输出图像路径')
    parser.add_argument('--pixelate', type=int, help='像素化大小')
    parser.add_argument('--palette', choices=list(PALETTES.keys()), help='调色板名称')
    parser.add_argument('--remove-bg', action='store_true', help='移除背景')
    parser.add_argument('--outline', action='store_true', help='添加轮廓')
    parser.add_argument('--auto-crop', action='store_true', help='自动裁剪')
    parser.add_argument('--target-size', help='目标画布尺寸（如64x64）')
    
    args = parser.parse_args()
    
    processor = AdvancedPostProcessor()
    processor.process_pipeline(
        input_path=args.input,
        output_path=args.output,
        pixelate_size=args.pixelate,
        palette=args.palette,
        remove_bg=args.remove_bg,
        add_outline_flag=args.outline,
        auto_crop_flag=args.auto_crop,
        target_size=args.target_size
    )

if __name__ == '__main__':
    main()
