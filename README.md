# lora-training：Docker 化 kohya `sd-scripts` LoRA 訓練與資料集處理工具

以 Docker 容器（`train-lora:latest`）封裝 [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) 與 WD14 自動打標／Caption 清理工具，支援在 Linux + NVIDIA GPU 環境下乾淨、可重現地面向 **SDXL / SD1.5 / Flux / SD3** 訓練角色或畫風 LoRA。

所有執行與 Hugging Face／PyTorch 快取皆隔離於容器與專案目錄內，不污染宿主機 Python 環境。

---

## 1. 快速建置環境

需求：Linux `x86_64`、NVIDIA GPU（建議 >= 12 GB VRAM）、Docker & NVIDIA Container Toolkit。

```bash
# 1. Clone 本專案（含 kohya sd-scripts submodule）
git clone --recurse-submodules https://github.com/kime541200/lora-training.git
cd lora-training

# 2. 建置訓練映像檔
docker build -t train-lora:latest .
```

準備底模與訓練圖片（皆已由 `.gitignore` 排除，不入版控）：
- 底模放入 `models/`（例如 `models/sd_xl_base_1.0.safetensors`）
- 原始訓練圖片放入 `images/<角色或專案名>/`

---

## 2. 標準訓練流程（以 SDXL 角色 LoRA 為例）

### 步驟一：建立資料集並執行 WD14 自動打標
使用內建的 `prep_dataset.py` 與 `run.sh` 在容器內完成裁切／整理與 WD14 Tagger 自動打標：

```bash
./run.sh python prep_dataset.py --help
# 將文字標籤中的角色固有外觀特徵移除、並將 trigger word 置於首位
./run.sh python fix_captions.py --help
```

### 步驟二：調整 `train.toml` 並啟動訓練
確認 [`train.toml`](train.toml) 中的 `pretrained_model_name_or_path`、`train_data_dir` 與 `output_name`，接著執行：

```bash
./train.sh sdxl_train_network.py train.toml
```

- 建議先以小步數（如 1 epoch / 100 steps）跑 smoke test 確認 Loss 收斂與顯存佔用正常，再進行完整訓練（例如 8 epochs，每 2 epochs 存檔）。
- 訓練完成的權重會輸出至 `output/*.safetensors`。
- 其他模型家族（SD1.5 / Flux / SD3）的訓練參數與注意事項請見 [`.agents/skills/train-lora/MODELS.md`](.agents/skills/train-lora/MODELS.md) 與 [`SKILL.md`](.agents/skills/train-lora/SKILL.md)。

---

## 3. 與 ComfyUI 及 AI Agent 生態系串接

訓練產出的 `output/*.safetensors` 可直接放入 ComfyUI 的 `models/loras/` 目錄進行驗證與生圖。歡迎搭配以下開源專案使用與參與貢獻：

| 專案 Repo | 角色與功能說明 |
| --- | --- |
| **[kime541200/comfyui-deploy](https://github.com/kime541200/comfyui-deploy)** | **Docker 化 ComfyUI 部署環境**：將產出的 LoRA 放入 `/data/comfyui/models/loras` 即可於容器內載入。 |
| **[kime541200/comfyui-agent](https://github.com/kime541200/comfyui-agent)** | **AI Agent 生圖工作區**：內建 `workflows/sdxl-lora.api.json` 模板，可讓 Agent 透過 [kime541200/comfy-mcp](https://github.com/kime541200/comfy-mcp) 自動載入 LoRA 出圖驗收。 |
| **[kime541200/ai-pose-gallery-zh](https://github.com/kime541200/ai-pose-gallery-zh)** | **AI 角色參考圖庫與合成台（4,345 張全中文索引）**：提供豐富的人像、服裝與姿勢參考，可作為訓練資料集生成素材或搭配 [kime541200/ai-pose-gallery-mcp](https://github.com/kime541200/ai-pose-gallery-mcp) 進行多圖角色合成。 |
