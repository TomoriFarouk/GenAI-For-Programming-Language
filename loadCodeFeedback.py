from datasets import load_dataset
import json
import os

# Load the dataset
dataset = load_dataset("m-a-p/Code-Feedback", split="train")

# Define target languages
target_languages = {"python", "ruby", "java"}

# Filter for the target languages
filtered = dataset.filter(lambda x: x.get(
    "language", "").lower() in target_languages)

# Print a few examples to verify
for i in range(3):
    print(f"Example {i+1}:")
    print("Language:", filtered[i]["language"])
    print("Code:", filtered[i]["code"][:200], "...")
    print("Feedback:", filtered[i]["feedback"][:200], "...")
    print("-" * 40)

# Output directory
output_dir = "data/codefeedback"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "codefeedback_formatted.jsonl")
count = 0

with open(output_path, "w", encoding="utf-8") as f:
    for item in filtered:
        f.write(json.dumps(item) + "\n")

print(f"✅ Saved {len(filtered)} {output_path}")
