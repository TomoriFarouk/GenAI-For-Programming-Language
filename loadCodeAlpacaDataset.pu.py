from datasets import load_dataset
import os
import json

# Load CodeAlpaca dataset
dataset = load_dataset("sahil2801/CodeAlpaca-20k", split="train")

# Output directory
output_dir = "data/raw_codesearchnet"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "codealpaca.jsonl")

# Save as JSONL
with open(output_path, "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(json.dumps(item) + "\n")

print(f"✅ Saved {len(dataset)} CodeAlpaca examples to {output_path}")
