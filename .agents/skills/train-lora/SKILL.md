---
name: train-lora
description: Train a LoRA for an image-generation model (SDXL/Illustrious/Pony, SD1.5, Flux, SD3, Lumina, others) from a folder of images, in Docker with kohya sd-scripts. Use when the user wants a character, style, or concept LoRA, or asks which base model to use.
---

# Train LoRA

The user is a non-technical **client**: they bring images and a wish; you are the engineer. Every decision you can make, make, and state it in one plain sentence. The user acts only at a **handoff**: something that needs their hands (a download behind a login, a long job).

Work from the project folder (it holds `images/`). Everything you install or produce stays inside it; ask before writing anywhere else.

## Steps

### 1. Brief

Read the folder first: count and look at the images, read existing `AGENTS.md`, `models/`, `train-lora:latest` image, GPU (`nvidia-smi`). Then settle with the user, in plain language, only what you cannot infer:

- **Subject**: character / style / concept, and the trigger word (propose one: a rare coined token).
- **Base model**: if the user names one, check it in [MODELS.md](MODELS.md) against their VRAM. If not, recommend one from the user's intent (look they want, anime vs. realistic) and VRAM, with one sentence of reasoning, and let them veto.
- **Where it will be used** (ComfyUI, A1111, other): decides the checkpoint to verify with.

**Done when:** subject, trigger word, base model, trainer script, and verification tool are each named, and the plan fits the VRAM.

### 2. Scaffold

Copy what is missing from [templates/](templates) into the project: `Dockerfile`, `requirements.docker.txt`, `run.sh`, `train.sh`, the prep/caption scripts, and the toml matching the trainer. Clone `kohya-ss/sd-scripts` into `sd-scripts/` at the latest commit (`--depth 1`), then drop `-e .` from its `requirements.txt`. If a later update breaks the templates, fix the template in this skill; `git checkout` an older commit only to unblock the current run. Small missing packages go to `.pylibs` (`pip install --target /work/.pylibs`), keeping the image unchanged.

Record the project's specifics (paths, base model, trigger word, commands, the sd-scripts commit that trained successfully) in the project `AGENTS.md`, since the next session starts cold.

### 3. Handoff: setup

Hand the user one message listing exactly what only they can do, each as a paste-ready command: `docker build -t train-lora:latest .` (slow), and the base-model download (see MODELS.md for the repo, and the command shape that works through Docker). Then stop and wait.

**Done when:** `docker image inspect train-lora:latest` succeeds and the base model file exists at the path the toml names.

### 4. Dataset

1. Prep images (`templates/prep_dataset.py`) into `dataset/<repeats>_<name>/`. Repeats ≈ 200–400 / image count for a small set, so one epoch is 200–400 steps' worth of exposure.
2. Caption with the tagger or captioner the trainer family expects (MODELS.md). For anime-style models that is WD14 tags; for natural-language models, sentences.
3. Clean captions (`templates/fix_captions.py`): trigger words first, then remove tags that restate the trigger or that you want baked into the character instead of promptable (see [LESSONS.md](LESSONS.md)).
4. Read ten captions at random.

**Done when:** every image has a caption, the trigger leads each one, and `keep_tokens` in the toml equals the number of trigger words.

### 5. Config

Fill the toml from MODELS.md's recommended settings for the family, estimate VRAM and time, and write two `sample_prompts.txt` lines that use the trigger word. Set `max_train_epochs = 1` for the first run.

**Done when:** every `<PLACEHOLDER>` is replaced, each path in the toml exists, and the toml's keys all appear in the family's guide under `sd-scripts/docs/`.

### 6. Handoff: training

A training run is long, so the user starts it. Run in two rounds, each three lines: the command (`./train.sh <trainer> train.toml`), the expected duration, and that the GPU must be free.

1. **Smoke test**: one epoch. When the user reports back, check `output/train.log` for a finished run, a falling loss, and a sample image; then restore the real epoch count.
2. **Full run**: wait for the user's report.

Stop after each message; leave launching and waiting to the user.

### 7. Verify

When the user reports completion, check `output/train.log` for the loss and final file, then generate test images against the user's actual tool (for ComfyUI: `templates/make_workflow.py`, with the checkpoint and LoRA names the server lists; the LoRA goes into its loras folder, so ask first) with the trigger word plus 2–3 varied prompts and a fixed seed sweep. Compare saved epoch checkpoints when a later one looks overcooked (ignores the prompt, burnt colours) or undercooked (no likeness).

Ask before copying a LoRA outside the project. Report back with one picture-based verdict, and the single next knob if it is unsatisfying (see LESSONS.md).

**Done when:** at least one prompt without the dataset's pose has been generated and judged against the training images, and the user has the path of the file to use.
