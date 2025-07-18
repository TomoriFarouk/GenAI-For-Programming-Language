import random

with open("merged_codefeedback_dataset.jsonl", "r", encoding="utf-8") as f:
    lines = f.readlines()

random.shuffle(lines)
split_idx = int(0.9 * len(lines))
train_lines = lines[:split_idx]
val_lines = lines[split_idx:]

with open("train.jsonl", "w", encoding="utf-8") as f:
    f.writelines(train_lines)
with open("val.jsonl", "w", encoding="utf-8") as f:
    f.writelines(val_lines)

print(f"Train: {len(train_lines)}, Validation: {len(val_lines)}")
