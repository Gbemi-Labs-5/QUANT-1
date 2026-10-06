#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
MODEL_NAME="Qwen/Qwen2.5-0.5B-Instruct"

"$PYTHON_BIN" -m pip install --quiet "transformers>=4.46" "sentencepiece" "accelerate" "tqdm"

"$PYTHON_BIN" - <<'PY'
import os
import time

os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
print(f"loading model: {model_name}")
start = time.time()
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True)
model.eval()

prompt = "Classify this news as macro or irrelevant: The ECB kept rates unchanged at 3.75% and signaled a gradual path for future easing."
inputs = tokenizer(prompt, return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=32, do_sample=False)
answer = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(f"benchmark_seconds={time.time() - start:.2f}")
print(answer)
PY

echo "Local AI installation and smoke test complete."
