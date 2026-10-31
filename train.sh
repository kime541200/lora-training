#!/bin/bash
# usage: ./train.sh <trainer.py> <config.toml>   e.g. ./train.sh sdxl_train_network.py train.toml
cd "$(dirname "$0")"; mkdir -p output
./run.sh accelerate launch --num_cpu_threads_per_process 4 "sd-scripts/${1:?trainer}" --config_file "/work/${2:?config}" 2>&1 | tee output/train.log
