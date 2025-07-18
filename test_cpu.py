"""
Lightweight test script for CPU-only environment
"""

import os
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Environment setup
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DATASETS_DISABLE_MULTIPROCESSING"] = "1"


def test_environment():
    """Test the environment setup"""
    print("=== Environment Test ===")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"GPU count: {torch.cuda.device_count()}")

    # Test system memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"System RAM: {memory.total / (1024**3):.1f}GB total")
        print(f"Available RAM: {memory.available / (1024**3):.1f}GB")
    except ImportError:
        print("psutil not available")

    # Test transformers import
    try:
        from transformers import AutoTokenizer
        print("✓ Transformers library available")
    except ImportError as e:
        print(f"✗ Transformers import failed: {e}")
        return False

    return True


def test_model_loading():
    """Test loading a small model first"""
    print("\n=== Model Loading Test ===")

    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM

        # Try loading a small model first
        print("Testing with a small model...")
        model_name = "microsoft/DialoGPT-small"  # Very small model for testing

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )

        print("✓ Small model loaded successfully")

        # Test generation
        print("Testing generation...")
        inputs = tokenizer("Hello, how are you?", return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=10,
                temperature=0.7,
                do_sample=True
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ Generation test passed: {response}")

        return True

    except Exception as e:
        print(f"✗ Model loading test failed: {e}")
        return False


def main():
    """Main test function"""
    print("Testing CPU-only environment for fine-tuned model...")

    # Test environment
    if not test_environment():
        print("Environment test failed!")
        return

    # Test model loading
    if not test_model_loading():
        print("Model loading test failed!")
        return

    print("\n=== All Tests Passed! ===")
    print("Your environment is ready for the fine-tuned model.")
    print("Note: Loading the full 7B model on CPU will take much longer.")
    print("Consider using a smaller model or cloud GPU for production use.")


if __name__ == "__main__":
    main()
