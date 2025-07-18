"""
Configuration file for the Generative AI Programming Education project
"""

import os
from pathlib import Path

# Model Configuration
MODEL_CONFIG = {
    # Path to your fine-tuned CodeLlama-7B model
    # Hugging Face Model Hub
    "model_path": "TomoriFarouk/codellama-7b-programming-education",

    # Model generation parameters
    "max_new_tokens": 512,
    "temperature": 0.7,
    "do_sample": True,
    "top_p": 0.9,
    "top_k": 50,

    # Input processing
    "max_input_length": 2048,
    "truncation": True,

    # Device configuration
    "device_map": "auto",
    "torch_dtype": "float16",
    "trust_remote_code": True
}

# Dataset Configuration (for reference)
DATASET_CONFIG = {
    "code_review_dataset": "path/to/your/code_review_dataset",
    "code_feedback_dataset": "path/to/your/code_feedback_dataset",
    "training_data_format": "json",  # or "csv", "txt"
}

# Educational Levels
STUDENT_LEVELS = {
    "beginner": {
        "description": "Students new to programming",
        "feedback_style": "explanatory",
        "include_basics": True,
        "complexity_threshold": "low"
    },
    "intermediate": {
        "description": "Students with basic programming knowledge",
        "feedback_style": "balanced",
        "include_basics": False,
        "complexity_threshold": "medium"
    },
    "advanced": {
        "description": "Students with strong programming background",
        "feedback_style": "technical",
        "include_basics": False,
        "complexity_threshold": "high"
    }
}

# Feedback Types
FEEDBACK_TYPES = [
    "syntax",
    "logic",
    "optimization",
    "style",
    "explanation",
    "comprehensive_review",
    "educational_guidance"
]

# Learning Objectives
LEARNING_OBJECTIVES = [
    "syntax",
    "basic_python",
    "control_flow",
    "loops",
    "variables",
    "code_cleanliness",
    "algorithms",
    "complexity",
    "optimization",
    "naming_conventions",
    "readability",
    "code_analysis",
    "best_practices",
    "learning",
    "improvement"
]

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "programming_education_ai.log"
}

# Ethical Safeguards
ETHICAL_CONFIG = {
    "prevent_over_reliance": True,
    "encourage_learning": True,
    "provide_explanations": True,
    "suggest_alternatives": True,
    "promote_best_practices": True
}


def get_model_path():
    """Get the model path from environment variable or config"""
    return os.getenv("FINETUNED_MODEL_PATH", MODEL_CONFIG["model_path"])


def validate_config():
    """Validate the configuration settings"""
    model_path = get_model_path()
    if not os.path.exists(model_path):
        print(f"Warning: Model path does not exist: {model_path}")
        print("Please update the model_path in config.py or set FINETUNED_MODEL_PATH environment variable")
        return False
    return True


if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"Model path: {get_model_path()}")
    print(f"Student levels: {list(STUDENT_LEVELS.keys())}")
    print(f"Feedback types: {FEEDBACK_TYPES}")
    validate_config()
