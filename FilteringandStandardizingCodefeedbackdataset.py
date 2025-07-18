import json
from datasets import load_dataset

dataset = load_dataset("m-a-p/Code-Feedback", split="train")
target_languages = ["python", "ruby", "java"]


def detect_language(messages):
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
print(f"Saved filth richer feedback.")
standardized = []
for ex in filtered_examples:
    user_msgs = [m['content'] for m in ex['messages'] if m['role'] == 'user']
    assistant_msgs = [m['content']
                      for m in ex['messages'] if m['role'] == 'assistant']
    if user_msgs and assistant_msgs:
        prompt = user_msgs[0]
        code = assistant_msgs[0]
        feedback = " ".join(assistant_msgs[1:]) if len(
            assistant_msgs) > 1 else ""
        fix = ""

        # Print examples where the assistant's message looks like code
        if any(keyword in code for keyword in ["def ", "class ", "import ", "{", ";", "function ", "public ", "private "]):
            print("Example with code in assistant's message:")
            print(ex)

        standardized.append({
            "language": ex["language"],
            "prompt": prompt,
            "code": code,
            "feedback": feedback,
            "fix": fix
        })

with open("standardized_codefeedback_rich.jsonl", "w", encoding="utf-8") as f:
    for item in standardized:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Saved {len(standardized)} examples with richer feedback.")
