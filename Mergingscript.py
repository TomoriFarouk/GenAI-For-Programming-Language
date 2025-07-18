import json
from datasets import load_dataset


input_files = [
    "standardized_codefeedback_rich.jsonl",
    "standardized_codereview.jsonl"
    # Add more files here if needed
]
output_file = "merged_codefeedback_dataset.jsonl"

with open(output_file, "w", encoding="utf-8") as outfile:
    for fname in input_files:
        with open(fname, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)

print(f"✅ Merged {len(input_files)} files into {output_file}")
