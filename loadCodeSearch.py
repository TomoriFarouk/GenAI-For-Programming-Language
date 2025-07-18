import os
import json
from datasets import load_dataset

# List of supported languages
languages = ["python", "java", "javascript", "go", "php", "ruby"]

# Define directory structure
raw_dir = "data/raw_codesearchnet"
merged_file = "data/raw_codesearchnet/all_languages.jsonl"

# Ensure directories exist
os.makedirs(raw_dir, exist_ok=True)

# # Step 1: Download and save each language
# for lang in languages:
#     print(f"⏬ Downloading CodeSearchNet for: {lang}...")
#     dataset = load_dataset("code_search_net", name=lang,
#                            split="train", trust_remote_code=True)

#     lang_file = os.path.join(raw_dir, f"{lang}.jsonl")
#     with open(lang_file, "w", encoding="utf-8") as f:
#         for example in dataset:
#             f.write(json.dumps(example) + "\n")

#     print(f"✅ Saved {len(dataset)} examples to {lang_file}")

# Step 2: Merge all language files into one
print(f"🔁 Merging all language files into: {merged_file}")
with open(merged_file, "w", encoding="utf-8") as outfile:
    for lang in languages:
        lang_file = os.path.join(raw_dir, f"{lang}.jsonl")
        with open(lang_file, "r", encoding="utf-8") as infile:
            for line in infile:
                data = json.loads(line)
                data["language"] = lang  # Tag the language
                outfile.write(json.dumps(data) + "\n")

print("✅ Merge complete.")
