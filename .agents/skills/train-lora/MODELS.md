# Base models and trainers

Trainer scripts live in `sd-scripts/` (cloned in step 2). Each family's guide ships with the clone at `sd-scripts/docs/<trainer>.md` (shared options: `train_network.md`, `config_README-en.md`); it matches the cloned code, so it overrides the settings below. **Read that guide before filling a toml for a family other than SDXL**: the settings below are a starting point, and the guide is the source for required flags (text encoders, VAE paths, precision).

## Choosing

| User intent | Recommend | Trainer | Min VRAM (LoRA, 1024px) |
| --- | --- | --- | --- |
| Anime / illustration character or style, best tag control | Illustrious-XL (or Pony / NoobAI, same family) | `sdxl_train_network.py` | ~10 GB (verified, 16 GB card) |
| Realistic photo, broad ecosystem | an SDXL photo checkpoint | `sdxl_train_network.py` | ~10 GB |
| Lowest hardware, oldest ecosystem | SD 1.5 | `train_network.py` | ~6–8 GB |
| Best prompt adherence, natural language, text in image | Flux.1 dev | `flux_train_network.py` | high; needs fp8/block swap on 16 GB (`sd-scripts/docs/block_swap.md`) |
| Other newer families | SD3 / Lumina / HunyuanImage / Anima / MOSS | `sd3_`, `lumina_`, `hunyuan_image_`, `anima_`, `moss_image_` `train_network.py` | see `sd-scripts/docs/<family>_train_network.md` |

Match the base model to what the user will generate with: a LoRA only works on its own family (an SDXL LoRA does nothing on Flux). Within a family, train on a plain base release (e.g. Illustrious-XL v1.0) and verify on close relatives; this worked for Illustrious v1.0 → v1.1.

Caption style follows the family: SDXL anime lines (Illustrious, Pony, NoobAI) want WD14 tags; SD1.5 anime the same; Flux, SD3 and the other T5/LLM-encoder families want natural-language sentences.

## Downloading

The user runs downloads (login/licence gates). Offer a paste-ready command that runs through the project image so nothing is installed on the host, e.g.:

```
docker run --rm -v "$PWD/models:/m" -e HF_HOME=/m/.hf train-lora:latest \
  hf download <repo> <file> --local-dir /m
```

Gated repos (Flux, SD3) need the user to accept the licence on the model page and pass `-e HF_TOKEN=...` themselves.

## SDXL recipe (verified)

`templates/train-sdxl.toml` is a character LoRA that trained cleanly: dim 16 / alpha 8, AdamW8bit lr 1e-4, UNet only, bf16, batch 2, 1024 px with bucketing, `cosine_with_restarts`, 10 epochs over 38 images × 10 repeats (~70 min on RTX 4060 Ti 16 GB, ~10 GB VRAM), checkpoint and sample image every 2 epochs. Scale the epochs with image count so total steps stay near 700–1000.

Tagger: `finetune/tag_images_by_wd14_tagger.py --onnx --repo_id SmilingWolf/wd-swinv2-tagger-v3 --model_dir /work/models/wd14 --batch_size 4 --thresh 0.35 --caption_extension .txt --remove_underscore <dataset dir>` via `./run.sh python sd-scripts/...`. The model downloads on first run, so a network-restricted run needs the user to fetch it.
