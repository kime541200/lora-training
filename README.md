# lora-training

以 Docker 跑 kohya `sd-scripts` 訓練 SDXL LoRA。

## 重建環境

```bash
git clone https://github.com/kohya-ss/sd-scripts sd-scripts
git -C sd-scripts checkout 11d8cedd0c67b93a10f8b2d75f43554f6f12c794   # 已驗證可訓練的 commit
sed -i '/^-e \.$/d' sd-scripts/requirements.txt                        # 本地唯一改動：移除 `-e .`
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
