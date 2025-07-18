import pandas as pd
import os
import json

input_dir = r"C:\Users\farou\data\raw_codesearchnet"
lang = "java"  # Change as needed

file_path = os.path.join(input_dir, f"{lang}.jsonl")

# Load the JSONL file
df = pd.read_json(file_path, lines=True)


output_file = f"standardized_codesearchnet_{lang}.jsonl"

with open(output_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        item = {
            "language": row.get("language", lang),
            "prompt": row.get("func_documentation_string", ""),
            "code": row.get("func_code_string", ""),
            "feedback": "",
            "fix": ""
        }
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"✅ Saved {len(df)} examples to {output_file}")
