#!/bin/bash
# usage: ./run.sh <command...>  (runs inside the train-lora container, all caches kept in project dir)
cd "$(dirname "$0")"
docker run --rm --gpus all --ipc=host -u $(id -u):$(id -g) -v "$PWD:/work" \
  -e USER=$(id -un) -e LOGNAME=$(id -un) -e TORCHINDUCTOR_CACHE_DIR=/work/.home/inductor -e HF_HOME=/work/.hf -e HOME=/work/.home -e PYTHONPATH=/work/sd-scripts:/work/.pylibs \
  -e TRITON_CACHE_DIR=/work/.home/triton train-lora:latest "$@"
