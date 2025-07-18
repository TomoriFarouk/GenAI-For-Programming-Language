from datasets import load_dataset

dataset = load_dataset("m-a-p/Code-Feedback", split="train")

target_languages = ["python", "ruby", "java"]


def detect_language(messages):
    # Look for language keywords in the user's prompt
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"].lower()
            for lang in target_languages:
                if lang in content:
                    return lang
    return None


filtered_examples = []
for example in dataset:
    lang = detect_language(example["messages"])
    if lang:
        filtered_examples.append({
            "id": example["id"],
            "language": lang,
            "messages": example["messages"]
        })

print(f"Found {len(filtered_examples)} examples with target languages.")

# Print a few examples to verify
for ex in filtered_examples[:3]:
    print(f"ID: {ex['id']}, Language: {ex['language']}")
    print("User prompt:", [m['content']
          for m in ex['messages'] if m['role'] == 'user'][0][:200])
    print("Assistant response:", [
          m['content'] for m in ex['messages'] if m['role'] == 'assistant'][0][:200])
    print("-" * 40)
