#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""智能生成调度中心 - 自动选择最佳后端和流水线"""

import sys
import os
import json
import argparse
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 导入各个模块
try:
    from prompt_engineer import PromptEngineer
    from advanced_post_process import AdvancedPostProcessor
    from quality_control import QualityController, VariantSelector
except ImportError:
    print("[警告] 部分模块未找到，请确保所有脚本在同一目录")

class GenerationOrchestrator:
    """生成编排器"""
    
    def __init__(self, config_path='generation_config.json'):
        self.config = self.load_config(config_path)
        self.prompt_engineer = PromptEngineer()
        self.post_processor = AdvancedPostProcessor()
        self.quality_controller = QualityController()
        self.variant_selector = VariantSelector()
    
    def load_config(self, config_path):
        """加载配置"""
        
        default_config = {
            'backend': 'sd-local',  # sd-local, dalle, sd-api
            'model': 'pixel-art-xl',
            'quality_check': True,
            'auto_post_process': True,
            'generate_variants': False,
            'variant_count': 4,
            'post_process': {
                'pixelate': None,
                'palette': None,
                'remove_bg': True,
                'outline': False,
                'auto_crop': True
            }
        }
        
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def select_backend(self, backend=None):
        """选择生成后端"""
        
        backend = backend or self.config['backend']
        
        backends = {
            'sd-local': self._generate_sd_local,
            'dalle': self._generate_dalle,
            'sd-api': self._generate_sd_api
        }
        
        if backend not in backends:
            print(f"[警告] 未知后端: {backend}，使用sd-local")
            backend = 'sd-local'
        
        return backends[backend]
    
    def _generate_sd_local(self, prompt, negative_prompt, size, output_path, **kwargs):
        """本地Stable Diffusion生成"""
        
        try:
            from generate_with_sd_local import generate_with_local_sd
            
            return generate_with_local_sd(
                prompt=prompt,
                negative_prompt=negative_prompt,
                size=size,
                output_path=output_path,
                model=kwargs.get('model', self.config['model']),
                controlnet_image=kwargs.get('controlnet_image'),
                steps=kwargs.get('steps', 30),
                cfg_scale=kwargs.get('cfg_scale', 7.5),
                seed=kwargs.get('seed', -1)
            )
        except Exception as e:
            print(f"[错误] SD本地生成失败: {e}")
            return False
    
    def _generate_dalle(self, prompt, negative_prompt, size, output_path, **kwargs):
        """DALL-E生成"""
        
        try:
            from generate_with_dalle import generate_with_dalle
            
            # DALL-E不支持负面提示词，将其合并到主提示词
            full_prompt = f"{prompt}. Avoid: {negative_prompt}" if negative_prompt else prompt
            
            return generate_with_dalle(
                prompt=full_prompt,
                size=size,
                output_path=output_path,
                count=1,
                api_key=kwargs.get('api_key')
            )
        except Exception as e:
            print(f"[错误] DALL-E生成失败: {e}")
            return False
    
    def _generate_sd_api(self, prompt, negative_prompt, size, output_path, **kwargs):
        """Stable Diffusion API生成"""
        
        try:
            from generate_with_stable_diffusion import generate_with_stable_diffusion
            
            return generate_with_stable_diffusion(
                prompt=prompt,
                size=size,
                output_path=output_path,
                count=1,
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'stabilityai/stable-diffusion-xl-base-1.0')
            )
        except Exception as e:
            print(f"[错误] SD API生成失败: {e}")
            return False
    
    def generate(
        self,
        subject,
        asset_type='sprite',
        style_preset='chrono-trigger',
        art_style='pixel-art',
        action=None,
        details=None,
        size='512x512',
        output_path='output/generated.png',
        backend=None,
        use_template=True,
        **kwargs
    ):
        """完整生成流程"""
        
        print("\n" + "=" * 60)
        print("[生成编排器] 开始生成流程")
        print("=" * 60)
        
        # 0. 智能选择模板（如果是精灵类型）
        controlnet_image = kwargs.get('controlnet_image')
        if use_template and asset_type == 'sprite' and not controlnet_image:
            try:
                from template_selector import TemplateSelector
                selector = TemplateSelector()
                template_path = selector.select_template(subject, action)
                if template_path:
                    kwargs['controlnet_image'] = template_path
                    print(f"[模板] 已自动选择模板: {template_path}")
            except Exception as e:
                print(f"[警告] 模板选择失败: {e}")
        
        # 1. 构建提示词
        print("\n[步骤1] 构建提示词...")
        prompt, negative_prompt = self.prompt_engineer.build_prompt(
            subject=subject,
            asset_type=asset_type,
            style_preset=style_preset,
            art_style=art_style,
            action=action,
            details=details
        )
        
        print(f"[正面提示词] {prompt}")
        print(f"[负面提示词] {negative_prompt}")
        
        # 2. 选择后端并生成
        print("\n[步骤2] 生成图像...")
        generator = self.select_backend(backend)
        
        if self.config['generate_variants']:
            # 生成多个变体
            variant_paths = []
            for i in range(self.config['variant_count']):
                variant_path = output_path.replace('.png', f'_variant_{i}.png')
                kwargs['seed'] = i
                success = generator(prompt, negative_prompt, size, variant_path, **kwargs)
                if success:
                    variant_paths.append(variant_path)
            
            # 自动选择最佳
            if variant_paths:
                output_path, scores = self.variant_selector.auto_select_best(variant_paths)
        else:
            # 单次生成
            success = generator(prompt, negative_prompt, size, output_path, **kwargs)
            if not success:
                print("[失败] 图像生成失败")
                return None
        
        # 3. 后处理
        if self.config['auto_post_process']:
            print("\n[步骤3] 后处理...")
            processed_path = output_path.replace('.png', '_processed.png')
            
            self.post_processor.process_pipeline(
                input_path=output_path,
                output_path=processed_path,
                **self.config['post_process']
            )
            
            output_path = processed_path
        
        # 4. 质量检查
        if self.config['quality_check']:
            print("\n[步骤4] 质量检查...")
            result = self.quality_controller.evaluate(
                output_path,
                expected_size=size,
                asset_type=asset_type
            )
            
            if result['score'] < 40:
                print("[警告] 质量评分较低，建议重新生成")
        
        print("\n" + "=" * 60)
        print(f"[完成] 最终输出: {output_path}")
        print("=" * 60 + "\n")
        
        return output_path
    
    def generate_animation(
        self,
        subject,
        animation_type,
        frame_count,
        style_preset='chrono-trigger',
        size='64x64',
        output_dir='output/animation',
        **kwargs
    ):
        """生成动画序列"""
        
        print("\n[动画生成] 开始生成动画序列...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 构建动画提示词
        prompt, negative_prompt = self.prompt_engineer.build_animation_prompt(
            subject=subject,
            animation_type=animation_type,
            frame_count=frame_count,
            style_preset=style_preset
        )
        
        # 生成精灵表
        sheet_path = os.path.join(output_dir, f'{animation_type}_sheet.png')
        generator = self.select_backend()
        
        success = generator(
            prompt=prompt,
            negative_prompt=negative_prompt,
            size=f"{int(size.split('x')[0]) * frame_count}x{size.split('x')[1]}",
            output_path=sheet_path,
            **kwargs
        )
        
        if success:
            print(f"[成功] 动画精灵表已生成: {sheet_path}")
            return sheet_path
        else:
            print("[失败] 动画生成失败")
            return None

def main():
    parser = argparse.ArgumentParser(description='智能2D游戏素材生成器')
    
    # 基本参数
    parser.add_argument('--subject', required=True, help='主体描述（如：勇敢的骑士）')
    parser.add_argument('--type', default='sprite', 
                       choices=['sprite', 'tileset', 'ui', 'icon', 'background', 'effect'],
                       help='素材类型')
    parser.add_argument('--style', default='chrono-trigger',
                       choices=['chrono-trigger', 'celeste', 'hollow-knight', 'stardew-valley',
                               'undertale', 'shovel-knight', 'dead-cells', 'terraria'],
                       help='风格预设')
    parser.add_argument('--action', help='动作描述（如：挥剑攻击）')
    parser.add_argument('--details', help='额外细节（如：红色披风，金色盔甲）')
    parser.add_argument('--size', default='512x512', help='输出尺寸')
    parser.add_argument('--output', default='output/generated.png', help='输出路径')
    
    # 后端选择
    parser.add_argument('--backend', choices=['sd-local', 'dalle', 'sd-api'],
                       help='生成后端')
    parser.add_argument('--model', help='模型名称')
    
    # 高级选项
    parser.add_argument('--variants', action='store_true', help='生成多个变体')
    parser.add_argument('--controlnet', help='ControlNet控制图像路径')
    parser.add_argument('--no-template', action='store_true', help='禁用自动模板选择')
    parser.add_argument('--config', default='generation_config.json', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建编排器
    orchestrator = GenerationOrchestrator(args.config)
    
    # 如果指定了变体，更新配置
    if args.variants:
        orchestrator.config['generate_variants'] = True
    
    # 生成
    orchestrator.generate(
        subject=args.subject,
        asset_type=args.type,
        style_preset=args.style,
        action=args.action,
        details=args.details,
        size=args.size,
        output_path=args.output,
        backend=args.backend,
        model=args.model,
        controlnet_image=args.controlnet,
        use_template=not args.no_template
    )

if __name__ == '__main__':
    main()
