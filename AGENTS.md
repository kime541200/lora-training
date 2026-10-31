# lora-training

以 Docker（`train-lora:latest`）跑 kohya `sd-scripts` 訓練 SDXL LoRA。GPU：RTX 4060 Ti 16 GB。流程細節與模板在 `.agents/skills/train-lora/`，訓練、資料集、驗證相關工作先讀它的 `SKILL.md`。

- 訓練：`./train.sh sdxl_train_network.py train.toml`；所有指令經 `run.sh` 在容器內執行，快取留在專案目錄。
- 角色 trigger word 放在 caption 第一個 token，`train.toml` 的 `keep_tokens` 等於 trigger 數。
- `sd-scripts/` 是 git submodule（kohya-ss/sd-scripts），pointer 即版本。需要新功能或修正時直接 `git -C sd-scripts fetch && git -C sd-scripts checkout <ref>` 更新，再提交新 pointer；更新後以 `train.toml` 跑 smoke test（1 epoch）確認仍可訓練，通過才提交。
- 驗證用 ComfyUI；把 LoRA 複製進其 loras 目錄前，先問使用者。
