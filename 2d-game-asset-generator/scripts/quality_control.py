#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""质量控制与评估系统"""

import sys
import os
import numpy as np
from PIL import Image
from pathlib import Path
import json

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class QualityController:
    """质量控制器"""
    
    def __init__(self):
        self.checks = []
        self.scores = {}
    
    def check_transparency(self, image):
        """检查透明度"""
        
        if image.mode != 'RGBA':
            return {
                'passed': False,
                'score': 0,
                'message': '图像不包含alpha通道'
            }
        
        alpha = np.array(image.split()[3])
        transparent_pixels = np.sum(alpha == 0)
        total_pixels = alpha.size
        transparency_ratio = transparent_pixels / total_pixels
        
        # 对于精灵，应该有一定比例的透明像素
        if transparency_ratio > 0.1:
            return {
                'passed': True,
                'score': 100,
                'message': f'透明度正常 ({transparency_ratio:.1%})'
            }
        else:
            return {
                'passed': False,
                'score': 50,
                'message': f'透明度过低 ({transparency_ratio:.1%})'
            }
    
    def check_size(self, image, expected_size):
        """检查尺寸"""
        
        if not expected_size:
            return {'passed': True, 'score': 100, 'message': '未指定尺寸要求'}
        
        width, height = map(int, expected_size.split('x'))
        
        if image.size == (width, height):
            return {
                'passed': True,
                'score': 100,
                'message': f'尺寸正确 ({width}x{height})'
            }
        else:
            return {
                'passed': False,
                'score': 0,
                'message': f'尺寸不匹配: 期望{width}x{height}, 实际{image.width}x{image.height}'
            }
    
    def check_color_count(self, image, max_colors=256):
        """检查颜色数量"""
        
        if image.mode == 'RGBA':
            rgb_image = image.convert('RGB')
        else:
            rgb_image = image
        
        colors = rgb_image.getcolors(maxcolors=100000)
        
        if colors is None:
            color_count = 100000
        else:
            color_count = len(colors)
        
        if color_count <= max_colors:
            return {
                'passed': True,
                'score': 100,
                'message': f'颜色数量合理 ({color_count}色)'
            }
        else:
            return {
                'passed': False,
                'score': 50,
                'message': f'颜色过多 ({color_count}色，建议<{max_colors})'
            }
    
    def check_edge_quality(self, image):
        """检查边缘质量（检测模糊）"""
        
        if image.mode == 'RGBA':
            rgb_image = image.convert('RGB')
        else:
            rgb_image = image
        
        img_array = np.array(rgb_image)
        
        # 计算拉普拉斯方差（边缘清晰度）
        from scipy import ndimage
        laplacian = ndimage.laplace(img_array.mean(axis=2))
        variance = laplacian.var()
        
        # 方差越大，边缘越清晰
        if variance > 100:
            score = 100
            message = f'边缘清晰 (方差: {variance:.1f})'
            passed = True
        elif variance > 50:
            score = 70
            message = f'边缘一般 (方差: {variance:.1f})'
            passed = True
        else:
            score = 30
            message = f'边缘模糊 (方差: {variance:.1f})'
            passed = False
        
        return {'passed': passed, 'score': score, 'message': message}
    
    def check_centering(self, image):
        """检查主体居中"""
        
        if image.mode != 'RGBA':
            return {'passed': True, 'score': 100, 'message': '无alpha通道，跳过居中检查'}
        
        alpha = np.array(image.split()[3])
        
        # 找到非透明区域的中心
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)
        
        if not rows.any() or not cols.any():
            return {'passed': False, 'score': 0, 'message': '图像完全透明'}
        
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        content_center_y = (rmin + rmax) / 2
        content_center_x = (cmin + cmax) / 2
        
        image_center_y = image.height / 2
        image_center_x = image.width / 2
        
        # 计算偏移
        offset_y = abs(content_center_y - image_center_y) / image.height
        offset_x = abs(content_center_x - image_center_x) / image.width
        
        max_offset = max(offset_y, offset_x)
        
        if max_offset < 0.1:
            return {
                'passed': True,
                'score': 100,
                'message': f'主体居中 (偏移: {max_offset:.1%})'
            }
        elif max_offset < 0.2:
            return {
                'passed': True,
                'score': 70,
                'message': f'主体基本居中 (偏移: {max_offset:.1%})'
            }
        else:
            return {
                'passed': False,
                'score': 30,
                'message': f'主体偏离中心 (偏移: {max_offset:.1%})'
            }
    
    def evaluate(self, image_path, expected_size=None, asset_type='sprite'):
        """综合评估"""
        
        print(f"\n[质量评估] {image_path}")
        print("=" * 60)
        
        image = Image.open(image_path)
        
        results = {}
        total_score = 0
        check_count = 0
        
        # 执行各项检查
        checks = [
            ('透明度', self.check_transparency(image)),
            ('尺寸', self.check_size(image, expected_size)),
            ('颜色数量', self.check_color_count(image)),
            ('边缘质量', self.check_edge_quality(image)),
        ]
        
        if asset_type == 'sprite':
            checks.append(('居中对齐', self.check_centering(image)))
        
        for name, result in checks:
            results[name] = result
            total_score += result['score']
            check_count += 1
            
            status = "[通过]" if result['passed'] else "[失败]"
            print(f"{status} {name}: {result['message']} (得分: {result['score']})")
        
        # 计算总分
        average_score = total_score / check_count if check_count > 0 else 0
        
        print("=" * 60)
        print(f"[总分] {average_score:.1f}/100")
        
        if average_score >= 80:
            grade = "优秀"
        elif average_score >= 60:
            grade = "良好"
        elif average_score >= 40:
            grade = "及格"
        else:
            grade = "不及格"
        
        print(f"[评级] {grade}\n")
        
        return {
            'score': average_score,
            'grade': grade,
            'checks': results
        }
    
    def batch_evaluate(self, image_dir, output_report='quality_report.json'):
        """批量评估"""
        
        image_dir = Path(image_dir)
        results = {}
        
        for image_file in image_dir.glob('*.png'):
            result = self.evaluate(str(image_file))
            results[image_file.name] = result
        
        # 保存报告
        with open(output_report, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[报告] 已保存到: {output_report}")
        
        return results

class VariantSelector:
    """变体筛选器"""
    
    def __init__(self):
        self.qc = QualityController()
    
    def generate_variants(self, generator_func, count=4):
        """生成多个变体"""
        
        variants = []
        
        for i in range(count):
            print(f"\n[变体 {i+1}/{count}] 生成中...")
            variant = generator_func(seed=i)
            variants.append(variant)
        
        return variants
    
    def auto_select_best(self, variant_paths):
        """自动选择最佳变体"""
        
        print("\n[自动筛选] 评估所有变体...")
        
        scores = []
        
        for path in variant_paths:
            result = self.qc.evaluate(path)
            scores.append((path, result['score']))
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        best_path, best_score = scores[0]
        
        print(f"\n[最佳] {best_path} (得分: {best_score:.1f})")
        
        return best_path, scores

def main():
    import argparse
    parser = argparse.ArgumentParser(description='质量控制与评估')
    parser.add_argument('--input', required=True, help='输入图像或目录')
    parser.add_argument('--expected-size', help='期望尺寸（如64x64）')
    parser.add_argument('--asset-type', default='sprite', help='素材类型')
    parser.add_argument('--batch', action='store_true', help='批量模式')
    parser.add_argument('--report', default='quality_report.json', help='报告输出路径')
    
    args = parser.parse_args()
    
    qc = QualityController()
    
    if args.batch:
        qc.batch_evaluate(args.input, args.report)
    else:
        qc.evaluate(args.input, args.expected_size, args.asset_type)

if __name__ == '__main__':
    main()
