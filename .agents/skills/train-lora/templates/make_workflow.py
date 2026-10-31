"""Write ComfyUI API-format workflows (built-in nodes only) for testing an SDXL-family LoRA.
usage: python3 make_workflow.py <ckpt_name> <lora_name> <trigger+prompt> [seeds e.g. 1,2,3] [out_dir]
ckpt_name / lora_name are the names ComfyUI lists (subfolders included, e.g. Illustrious/x.safetensors).
Other families (Flux, SD3, ...) use different loader/sampler nodes: query the server's node list and adapt."""
import json, os, sys

ckpt, lora, prompt = sys.argv[1:4]
seeds = [int(s) for s in (sys.argv[4] if len(sys.argv) > 4 else "1,2,3").split(",")]
out = sys.argv[5] if len(sys.argv) > 5 else "workflows"
NEG = "lowres, bad anatomy, worst quality, low quality, text, watermark"
os.makedirs(out, exist_ok=True)
stem = os.path.splitext(os.path.basename(lora))[0]
for seed in seeds:
    wf = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "2": {"class_type": "LoraLoader", "inputs": {"model": ["1", 0], "clip": ["1", 1], "lora_name": lora, "strength_model": 1.0, "strength_clip": 1.0}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": NEG}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0], "seed": seed, "steps": 28, "cfg": 6.0, "sampler_name": "euler_ancestral", "scheduler": "normal", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": f"{stem}_s{seed}"}},
    }
    json.dump(wf, open(f"{out}/{stem}_s{seed}.json", "w"), indent=1)
print(f"{len(seeds)} workflows -> {out}")
