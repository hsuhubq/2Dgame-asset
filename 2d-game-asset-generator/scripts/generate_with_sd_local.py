#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地Stable Diffusion集成 - 支持ControlNet和像素艺术专用模型"""

import sys
import os
import json
from pathlib import Path

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_with_local_sd(
    prompt, 
    negative_prompt,
    size, 
    output_path, 
    model="pixel-art-xl",
    controlnet_image=None,
    steps=30,
    cfg_scale=7.5,
    seed=-1
):
    """使用本地Stable Diffusion生成图像"""
    
    try:
        from diffusers import StableDiffusionPipeline, StableDiffusionControlNetPipeline, ControlNetModel
        import torch
        from PIL import Image
        
        print(f"[SD] 正在加载模型: {model}")
        
        # 解析尺寸
        width, height = map(int, size.split('x'))
        
        # 选择设备
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[设备] 使用: {device}")
        
        # 加载模型
        if controlnet_image:
            # 使用ControlNet模式
            print("[ControlNet] 启用姿态控制")
            controlnet = ControlNetModel.from_pretrained(
                "lllyasviel/control_v11p_sd15_openpose",
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                controlnet=controlnet,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None
            )
            
            # 加载控制图像
            control_image = Image.open(controlnet_image).convert("RGB")
            control_image = control_image.resize((width, height))
            
        else:
            # 标准模式
            model_map = {
                "pixel-art-xl": "nerijs/pixel-art-xl",
                "pixel-art": "kohbanye/pixel-art-style",
                "sd-1.5": "runwayml/stable-diffusion-v1-5",
                "sd-2.1": "stabilityai/stable-diffusion-2-1"
            }
            
            model_id = model_map.get(model, model)
            
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None
            )
        
        pipe = pipe.to(device)
        
        # 启用内存优化
        if device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()
        
        print(f"[生成] 开始生成...")
        print(f"[提示词] {prompt}")
        print(f"[负面提示词] {negative_prompt}")
        
        # 生成图像
        generator = torch.Generator(device=device)
        if seed != -1:
            generator = generator.manual_seed(seed)
        
        if controlnet_image:
            image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=control_image,
                num_inference_steps=steps,
                guidance_scale=cfg_scale,
                width=width,
                height=height,
                generator=generator
            ).images[0]
        else:
            image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=cfg_scale,
                width=width,
                height=height,
                generator=generator
            ).images[0]
        
        # 保存图像
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        image.save(output_path, 'PNG')
        print(f"[成功] 图像已保存: {output_path}")
        
        # 保存元数据
        metadata = {
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'model': model,
            'size': size,
            'steps': steps,
            'cfg_scale': cfg_scale,
            'seed': seed,
            'controlnet': controlnet_image is not None
        }
        
        metadata_path = str(Path(output_path).with_suffix('.json'))
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return True
        
    except ImportError:
        print("[错误] diffusers库未安装")
        print("[提示] 请运行: pip install diffusers transformers accelerate torch torchvision")
        return False
    except Exception as e:
        print(f"[错误] 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='使用本地Stable Diffusion生成图像')
    parser.add_argument('--prompt', required=True, help='正面提示词')
    parser.add_argument('--negative-prompt', default='', help='负面提示词')
    parser.add_argument('--size', default='512x512', help='输出尺寸')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--model', default='pixel-art-xl', help='模型名称')
    parser.add_argument('--controlnet-image', help='ControlNet控制图像路径')
    parser.add_argument('--steps', type=int, default=30, help='推理步数')
    parser.add_argument('--cfg-scale', type=float, default=7.5, help='CFG scale')
    parser.add_argument('--seed', type=int, default=-1, help='随机种子')
    
    args = parser.parse_args()
    
    generate_with_local_sd(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        size=args.size,
        output_path=args.output,
        model=args.model,
        controlnet_image=args.controlnet_image,
        steps=args.steps,
        cfg_scale=args.cfg_scale,
        seed=args.seed
    )

if __name__ == '__main__':
    main()
