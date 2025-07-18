import pandas as pd
import json
import numpy as np

# Use the path to your downloaded file
df = pd.read_parquet(r"C:\Users\farou\Downloads\0000.parquet")

# Show the first few rows and columns to inspect the structure
print(df.head())
print(df.columns)


def safe_json(val):
    # Convert numpy arrays to lists, or just to string if you prefer
    if isinstance(val, np.ndarray):
        return val.tolist()
    # Convert other non-serializable types to string
    try:
        json.dumps(val)
        return val
    except TypeError:
        return str(val)


output_path = "standardized_codereview.jsonl"

with open(output_path, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        # Try to extract language from meta_data if available, else default to "python"
        language = "python"
        meta_data = row.get("meta_data", None)
        if isinstance(meta_data, dict) and "language" in meta_data:
            language = meta_data["language"]
        item = {
            "language": language,
            "prompt": safe_json(row.get("prompt", "") or row.get("body", "")),
            "code": safe_json(row.get("response", "")),
            "feedback": safe_json(row.get("answer", ""))
        }
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"✅ Saved {len(df)} examples to {output_path}")
