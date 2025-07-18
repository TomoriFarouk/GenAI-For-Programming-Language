# from huggingface_hub import snapshot_download

# snapshot_download(
#     repo_id="codellama/CodeLlama-7b-hf",
#     local_dir="models/CodeLLaMA-7b",
#     resume_download=True
# )

from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "models/CodeLLaMA-7b"  # replace with actual unzipped folder

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

print("✅ Model and tokenizer loaded successfully.")
