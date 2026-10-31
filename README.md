# lora-training

以 Docker 跑 kohya `sd-scripts` 訓練 LoRA（SD1.5 / SDXL / Flux / SD3 等）。SDXL 是已驗證流程；其他家族見 `.agents/skills/train-lora/MODELS.md`。

## 重建環境

```bash
git clone --recurse-submodules git@github.com:kime541200/lora-training.git
docker build -t train-lora:latest .
```

另需自行放入（皆不入版控）：`models/sd_xl_base_1.0.safetensors`、`images/`（訓練圖）。

## 使用

- 資料集：`prep_dataset.py`、`fix_captions.py`（用法見檔頭 docstring）
- 訓練：`./train.sh sdxl_train_network.py train.toml`
- 輸出：`output/*.safetensors`

## 目前實驗：ohwxgirl 角色 LoRA

- 10 張虛構寫實女性圖；trigger `ohwxgirl`；底模 SDXL 1.0 base。
- 資料集 `dataset/20_ohwxgirl`（20 repeats），WD14 tagging 後以 `fix_captions.py` 清理（trigger 置首，移除固定外觀 tag）。
- smoke test 通過（100 steps，約 3.5 min）；正式訓練 8 epochs（約 800 steps，約 1 h），每 2 epoch 存檔。
