"""
Generative AI for Enhancing Programming Education
================================================

This project implements a fine-tuned CodeLlama-7B model to provide structured,
educational code feedback for programming students.

Problem Statement:
- High dropout rates in programming education
- Inefficient feedback loops
- Lack of personalized learning
- Limited instructor bandwidth
- Current AI tools prioritize productivity over learning

Solution:
- Fine-tuned CodeLlama-7B for educational feedback
- Structured, actionable code reviews
- Beginner-friendly explanations
- Personalized adaptation based on skill level
- Educational focus with ethical safeguards

Author: [Your Name]
Date: [Current Date]
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import gc
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# --- Critical Environment Setup (Must be before imports) ---
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DATASETS_DISABLE_MULTIPROCESSING"] = "1"

# Clear any existing CUDA cache (only if CUDA is available)
if torch.cuda.is_available():
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128,garbage_collection_threshold:0.6"
    torch.cuda.empty_cache()
    gc.collect()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clear_cuda_cache():
    """Clear CUDA cache and run garbage collection"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    gc.collect()


def get_system_memory():
    """Get system memory information"""
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(
            f"System RAM: {memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB used ({memory.percent:.1f}%)")
    except Exception as e:
        print(f"Could not get system memory info: {e}")


def get_gpu_memory():
    """Get GPU memory information (if available)"""
    if torch.cuda.is_available():
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total', '--format=csv,nounits,noheader'],
                                    capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                used, total = map(int, line.split(', '))
                print(
                    f"GPU {i}: {used}MB / {total}MB used ({used/total*100:.1f}%)")
        except Exception as e:
            print(f"Could not get GPU memory info: {e}")
    else:
        print("No GPU available - using CPU only")


@dataclass
class CodeFeedback:
    """Data structure for storing code feedback"""
    code_snippet: str
    feedback_type: str  # 'syntax', 'logic', 'optimization', 'style', 'explanation'
    feedback_message: str
    suggested_improvement: Optional[str] = None
    difficulty_level: str = 'beginner'  # 'beginner', 'intermediate', 'advanced'
    learning_objectives: List[str] = None


@dataclass
class ComprehensiveFeedback:
    """Comprehensive feedback structure with all educational components"""
    code_snippet: str
    student_level: str

    # Analysis
    strengths: List[str]
    weaknesses: List[str]
    issues: List[str]

    # Educational content
    step_by_step_improvement: List[str]
    learning_points: List[str]
    review_summary: str

    # Interactive elements
    comprehension_question: str
    comprehension_answer: str
    explanation: str

    # Code fixes
    improved_code: str
    fix_explanation: str

    # Metadata
    difficulty_level: str
    learning_objectives: List[str]
    estimated_time_to_improve: str


class ProgrammingEducationAI:
    """
    Main class for the fine-tuned CodeLlama model for programming education
    """

    def __init__(self, model_path: str = "./model"):
        """
        Initialize the fine-tuned model and tokenizer

        Args:
            model_path: Path to your fine-tuned CodeLlama-7B model
        """
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.feedback_templates = self._load_feedback_templates()
        self.code_review_prompt_template = self._load_code_review_prompt()
        self.code_feedback_prompt_template = self._load_code_feedback_prompt()
        self.comprehensive_feedback_prompt = self._load_comprehensive_feedback_prompt()
        self.comprehension_question_prompt = self._load_comprehension_question_prompt()
        self.code_fix_prompt = self._load_code_fix_prompt()

    def _load_code_review_prompt(self) -> str:
        """Load the code review prompt template used during fine-tuning"""
        return """You are an expert programming tutor. Review the following student code and provide educational feedback.

Student Code:
{code}

Student Level: {level}

Please provide:
1. Syntax errors (if any)
2. Logic errors (if any)
3. Style improvements
4. Optimization suggestions
5. Educational explanations

Feedback:"""

    def _load_code_feedback_prompt(self) -> str:
        """Load the code feedback prompt template used during fine-tuning"""
        return """You are a helpful programming tutor. The student has written this code:

{code}

Student Level: {level}

Provide constructive, educational feedback that helps the student learn. Focus on:
- What they did well
- What can be improved
- Why the improvement matters
- How to implement the improvement

Feedback:"""

    def _load_feedback_templates(self) -> Dict[str, str]:
        """Load predefined feedback templates for different scenarios"""
        return {
            "syntax_error": "I notice there's a syntax issue in your code. {error_description}. "
            "Here's what's happening: {explanation}. "
            "Try this correction: {suggestion}",

            "logic_error": "Your code has a logical issue. {problem_description}. "
            "The problem is: {explanation}. "
            "Consider this approach: {suggestion}",

            "optimization": "Your code works, but we can make it more efficient! "
                           "Current complexity: {current_complexity}. "
                           "Optimized version: {optimized_complexity}. "
                           "Here's how: {explanation}",

            "style_improvement": "Great work! Here's a style tip: {tip}. "
            "This makes your code more readable and maintainable.",

            "concept_explanation": "Let me explain this concept: {concept}. "
            "In simple terms: {simple_explanation}. "
            "Example: {example}"
        }

    def load_model(self):
        """Load the fine-tuned model and tokenizer using optimized settings"""
        try:
            logger.info(f"Loading fine-tuned model from {self.model_path}")

            # Load tokenizer with proper settings
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                use_fast=True,
                padding_side="right"
            )

            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

            logger.info(
                f"Tokenizer loaded - Vocab size: {len(self.tokenizer)}")

            # Load model optimized for HF Spaces (16GB RAM, 2 vCPU)
            print("Loading model optimized for HF Spaces (16GB RAM, 2 vCPU)...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float32,
                device_map=None,  # Force CPU for HF Spaces
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                offload_folder="offload"  # Offload to disk if needed
            )
            # Enable gradient checkpointing for memory savings
            self.model.gradient_checkpointing_enable()

            logger.info("Fine-tuned model loaded successfully")
            logger.info(f"Model loaded on devices: {self.model.hf_device_map}")

        except Exception as e:
            logger.error(f"Error loading fine-tuned model: {e}")
            raise

    def generate_code_review(self, code: str, student_level: str = "beginner") -> str:
        """
        Generate code review using the fine-tuned model

        Args:
            code: Student's code to review
            student_level: Student's skill level

        Returns:
            Generated code review feedback
        """
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model() first.")

        # Format the prompt using the template from fine-tuning
        prompt = self.code_review_prompt_template.format(
            code=code,
            level=student_level
        )

        # Tokenize input
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048)

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the generated part (after the prompt)
        generated_text = response[len(prompt):].strip()

        return generated_text

    def generate_educational_feedback(self, code: str, student_level: str = "beginner") -> str:
        """
        Generate educational feedback using the fine-tuned model

        Args:
            code: Student's code to provide feedback on
            student_level: Student's skill level

        Returns:
            Generated educational feedback
        """
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model() first.")

        # Format the prompt using the template from fine-tuning
        prompt = self.code_feedback_prompt_template.format(
            code=code,
            level=student_level
        )

        # Tokenize input
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048)

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the generated part (after the prompt)
        generated_text = response[len(prompt):].strip()

        return generated_text

    def analyze_student_code(self, code: str, student_level: str = "beginner") -> List[CodeFeedback]:
        """
        Analyze student code and provide educational feedback using the fine-tuned model

        Args:
            code: The student's code to analyze
            student_level: Student's skill level ('beginner', 'intermediate', 'advanced')

        Returns:
            List of CodeFeedback objects
        """
        feedback_list = []

        # Use fine-tuned model for comprehensive code review
        try:
            code_review = self.generate_code_review(code, student_level)
            educational_feedback = self.generate_educational_feedback(
                code, student_level)

            # Create structured feedback from model output
            feedback_list.append(CodeFeedback(
                code_snippet=code,
                feedback_type="comprehensive_review",
                feedback_message=code_review,
                difficulty_level=student_level,
                learning_objectives=["code_analysis", "best_practices"]
            ))

            feedback_list.append(CodeFeedback(
                code_snippet=code,
                feedback_type="educational_guidance",
                feedback_message=educational_feedback,
                difficulty_level=student_level,
                learning_objectives=["learning", "improvement"]
            ))

        except Exception as e:
            logger.warning(
                f"Fine-tuned model failed, falling back to rule-based analysis: {e}")
            # Fallback to rule-based analysis if model fails
            feedback_list = self._fallback_analysis(code, student_level)

        return feedback_list

    def _fallback_analysis(self, code: str, student_level: str) -> List[CodeFeedback]:
        """Fallback analysis using rule-based methods if fine-tuned model fails"""
        feedback_list = []

        # Analyze syntax
        syntax_feedback = self._check_syntax(code, student_level)
        if syntax_feedback:
            feedback_list.append(syntax_feedback)

        # Analyze logic and structure
        logic_feedback = self._check_logic(code, student_level)
        if logic_feedback:
            feedback_list.extend(logic_feedback)

        # Check for optimization opportunities
        optimization_feedback = self._check_optimization(code, student_level)
        if optimization_feedback:
            feedback_list.append(optimization_feedback)

        # Provide style suggestions
        style_feedback = self._check_style(code, student_level)
        if style_feedback:
            feedback_list.append(style_feedback)

        return feedback_list

    def _check_syntax(self, code: str, student_level: str) -> Optional[CodeFeedback]:
        """Check for syntax errors and provide educational feedback"""
        # This would integrate with the fine-tuned model
        # For now, using basic pattern matching as placeholder

        common_syntax_errors = {
            r"print\s*\([^)]*\)\s*$": "Remember to add a colon after print statements in some contexts",
            r"if\s+[^:]+$": "Don't forget the colon after your if condition",
            r"for\s+[^:]+$": "Don't forget the colon after your for loop",
        }

        for pattern, message in common_syntax_errors.items():
            if re.search(pattern, code):
                return CodeFeedback(
                    code_snippet=code,
                    feedback_type="syntax",
                    feedback_message=message,
                    difficulty_level=student_level,
                    learning_objectives=["syntax", "basic_python"]
                )

        return None

    def _check_logic(self, code: str, student_level: str) -> List[CodeFeedback]:
        """Check for logical errors and provide educational feedback"""
        feedback_list = []

        # Check for infinite loops
        if "while True:" in code and "break" not in code:
            feedback_list.append(CodeFeedback(
                code_snippet=code,
                feedback_type="logic",
                feedback_message="This while loop will run forever! Make sure to include a break statement or condition to exit the loop.",
                difficulty_level=student_level,
                learning_objectives=["control_flow", "loops"]
            ))

        # Check for unused variables
        # This is a simplified check - the actual model would be more sophisticated
        if "x = " in code and "x" not in code.replace("x = ", ""):
            feedback_list.append(CodeFeedback(
                code_snippet=code,
                feedback_type="logic",
                feedback_message="You created variable 'x' but didn't use it. Consider removing unused variables to keep your code clean.",
                difficulty_level=student_level,
                learning_objectives=["variables", "code_cleanliness"]
            ))

        return feedback_list

    def _check_optimization(self, code: str, student_level: str) -> Optional[CodeFeedback]:
        """Check for optimization opportunities"""
        # Check for nested loops that could be optimized
        if code.count("for") > 1 and code.count("in range") > 1:
            return CodeFeedback(
                code_snippet=code,
                feedback_type="optimization",
                feedback_message="You have nested loops here. Consider if you can optimize this to O(n) instead of O(n²).",
                suggested_improvement="Use a hashmap or set to reduce complexity",
                difficulty_level=student_level,
                learning_objectives=["algorithms",
                                     "complexity", "optimization"]
            )

        return None

    def _check_style(self, code: str, student_level: str) -> Optional[CodeFeedback]:
        """Check for style improvements"""
        # Check for meaningful variable names
        if "x" in code or "y" in code or "z" in code:
            return CodeFeedback(
                code_snippet=code,
                feedback_type="style",
                feedback_message="Consider using more descriptive variable names instead of x, y, z. This makes your code easier to understand.",
                difficulty_level=student_level,
                learning_objectives=["naming_conventions", "readability"]
            )

        return None

    def generate_explanation(self, concept: str, student_level: str) -> str:
        """
        Generate explanations for programming concepts based on student level

        Args:
            concept: The concept to explain
            student_level: Student's skill level

        Returns:
            Explanation tailored to the student's level
        """
        explanations = {
            "variables": {
                "beginner": "Variables are like labeled boxes where you store information. Think of 'name = \"John\"' as putting \"John\" in a box labeled 'name'.",
                "intermediate": "Variables are memory locations that store data. They have a name, type, and value. Python is dynamically typed, so the type is inferred.",
                "advanced": "Variables in Python are references to objects in memory. They're dynamically typed and use reference counting for memory management."
            },
            "loops": {
                "beginner": "Loops repeat code multiple times. 'for' loops are great when you know how many times to repeat, 'while' loops when you don't.",
                "intermediate": "Loops control program flow. 'for' iterates over sequences, 'while' continues until a condition is False. Consider time complexity.",
                "advanced": "Loops are fundamental control structures. Python's 'for' is actually a foreach loop. Consider iterator patterns and generator expressions."
            }
        }

        return explanations.get(concept, {}).get(student_level, f"Explanation for {concept} at {student_level} level")

    def _load_comprehensive_feedback_prompt(self) -> str:
        """Load the comprehensive feedback prompt template"""
        return """You are an expert programming tutor. Provide comprehensive educational feedback for the following student code.

Student Code:
{code}

Student Level: {level}

Please provide a detailed analysis in the following JSON format:

{{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2", "weakness3"],
    "issues": ["issue1", "issue2", "issue3"],
    "step_by_step_improvement": [
        "Step 1: Description of first improvement",
        "Step 2: Description of second improvement",
        "Step 3: Description of third improvement"
    ],
    "learning_points": [
        "Learning point 1: What the student should understand",
        "Learning point 2: Key concept to grasp",
        "Learning point 3: Best practice to follow"
    ],
    "review_summary": "A comprehensive review of the code highlighting key areas for improvement",
    "learning_objectives": ["objective1", "objective2", "objective3"],
    "estimated_time_to_improve": "5-10 minutes"
}}

Focus on educational value and constructive feedback that helps the student learn and improve."""

    def _load_comprehension_question_prompt(self) -> str:
        """Load the comprehension question generation prompt"""
        return """Based on the learning points and improvements discussed, generate a comprehension question to test the student's understanding.

Learning Points: {learning_points}
Code Issues: {issues}
Student Level: {level}

Generate a question that tests understanding of the key concepts discussed. The question should be appropriate for the student's level.

Format your response as JSON:
{{
    "question": "Your comprehension question here",
    "answer": "The correct answer",
    "explanation": "Detailed explanation of why this answer is correct"
}}

Make the question challenging but fair for the student's level."""

    def _load_code_fix_prompt(self) -> str:
        """Load the code fix generation prompt"""
        return """You are an expert programming tutor. Based on the analysis and learning points, provide an improved version of the student's code.

Original Code:
{code}

Issues Identified: {issues}
Learning Points: {learning_points}
Student Level: {level}

Provide an improved version of the code that addresses the issues while maintaining educational value. Include comments to explain the improvements.

Format your response as JSON:
{{
    "improved_code": "The improved code with comments",
    "fix_explanation": "Detailed explanation of what was changed and why"
}}

Focus on educational improvements that help the student understand better practices."""

    def adapt_feedback_complexity(self, feedback: CodeFeedback, student_level: str) -> CodeFeedback:
        """
        Adapt feedback complexity based on student level

        Args:
            feedback: Original feedback
            student_level: Student's skill level

        Returns:
            Adapted feedback
        """
        if student_level == "beginner":
            # Simplify language and add more examples
            feedback.feedback_message = feedback.feedback_message.replace(
                "O(n²)", "quadratic time (slower)"
            ).replace(
                "O(n)", "linear time (faster)"
            )
        elif student_level == "advanced":
            # Add more technical details
            if "optimization" in feedback.feedback_type:
                feedback.feedback_message += " Consider the space-time tradeoff and cache locality."

        return feedback

    def generate_comprehensive_feedback(self, code: str, student_level: str = "beginner") -> ComprehensiveFeedback:
        """
        Generate comprehensive educational feedback with all components

        Args:
            code: Student's code to analyze
            student_level: Student's skill level

        Returns:
            ComprehensiveFeedback object with all educational components
        """
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model() first.")

        try:
            # Step 1: Generate comprehensive analysis
            comprehensive_analysis = self._generate_comprehensive_analysis(
                code, student_level)

            # Step 2: Generate comprehension question
            comprehension_data = self._generate_comprehension_question(
                comprehensive_analysis["learning_points"],
                comprehensive_analysis["issues"],
                student_level
            )

            # Step 3: Generate improved code
            code_fix_data = self._generate_code_fix(
                code,
                comprehensive_analysis["issues"],
                comprehensive_analysis["learning_points"],
                student_level
            )

            # Create comprehensive feedback object
            return ComprehensiveFeedback(
                code_snippet=code,
                student_level=student_level,
                strengths=comprehensive_analysis["strengths"],
                weaknesses=comprehensive_analysis["weaknesses"],
                issues=comprehensive_analysis["issues"],
                step_by_step_improvement=comprehensive_analysis["step_by_step_improvement"],
                learning_points=comprehensive_analysis["learning_points"],
                review_summary=comprehensive_analysis["review_summary"],
                comprehension_question=comprehension_data["question"],
                comprehension_answer=comprehension_data["answer"],
                explanation=comprehension_data["explanation"],
                improved_code=code_fix_data["improved_code"],
                fix_explanation=code_fix_data["fix_explanation"],
                difficulty_level=student_level,
                learning_objectives=comprehensive_analysis["learning_objectives"],
                estimated_time_to_improve=comprehensive_analysis["estimated_time_to_improve"]
            )

        except Exception as e:
            logger.error(f"Error generating comprehensive feedback: {e}")
            # Return a basic comprehensive feedback if model fails
            return self._create_fallback_comprehensive_feedback(code, student_level)

    def _generate_comprehensive_analysis(self, code: str, student_level: str) -> Dict:
        """Generate comprehensive analysis using the fine-tuned model"""
        prompt = self.comprehensive_feedback_prompt.format(
            code=code,
            level=student_level
        )

        response = self._generate_model_response(prompt)

        try:
            # Try to parse JSON response
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback")
            return self._create_fallback_analysis(code, student_level)

    def _generate_comprehension_question(self, learning_points: List[str], issues: List[str], student_level: str) -> Dict:
        """Generate comprehension question using the fine-tuned model"""
        prompt = self.comprehension_question_prompt.format(
            learning_points=", ".join(learning_points),
            issues=", ".join(issues),
            level=student_level
        )

        response = self._generate_model_response(prompt)

        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(
                "Failed to parse comprehension question JSON, using fallback")
            return {
                "question": "What is the main concept you learned from this code review?",
                "answer": "The main concept is understanding code structure and best practices.",
                "explanation": "This question tests your understanding of the key learning points discussed."
            }

    def _generate_code_fix(self, code: str, issues: List[str], learning_points: List[str], student_level: str) -> Dict:
        """Generate improved code using the fine-tuned model"""
        prompt = self.code_fix_prompt.format(
            code=code,
            issues=", ".join(issues),
            learning_points=", ".join(learning_points),
            level=student_level
        )

        response = self._generate_model_response(prompt)

        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse code fix JSON, using fallback")
            return {
                "improved_code": "# Improved version of your code\n# Add comments and improvements here",
                "fix_explanation": "This is a fallback improved version. The model should provide specific improvements."
            }

    def _generate_model_response(self, prompt: str) -> str:
        """Generate response from the fine-tuned model"""
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048)

        # Move to CPU if no GPU available
        if not torch.cuda.is_available():
            inputs = {k: v.cpu() for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()

    def _create_fallback_analysis(self, code: str, student_level: str) -> Dict:
        """Create fallback analysis when model fails"""
        return {
            "strengths": ["Your code has a clear structure", "You're using appropriate data types"],
            "weaknesses": ["Could improve variable naming", "Consider adding comments"],
            "issues": ["Basic syntax and style issues"],
            "step_by_step_improvement": [
                "Step 1: Add descriptive variable names",
                "Step 2: Include comments explaining your logic",
                "Step 3: Consider code optimization"
            ],
            "learning_points": [
                "Good variable naming improves code readability",
                "Comments help others understand your code",
                "Always consider efficiency in your solutions"
            ],
            "review_summary": "Your code works but could be improved with better practices.",
            "learning_objectives": ["code_quality", "best_practices", "readability"],
            "estimated_time_to_improve": "10-15 minutes"
        }

    def _create_fallback_comprehensive_feedback(self, code: str, student_level: str) -> ComprehensiveFeedback:
        """Create fallback comprehensive feedback when model fails"""
        fallback_analysis = self._create_fallback_analysis(code, student_level)

        return ComprehensiveFeedback(
            code_snippet=code,
            student_level=student_level,
            strengths=fallback_analysis["strengths"],
            weaknesses=fallback_analysis["weaknesses"],
            issues=fallback_analysis["issues"],
            step_by_step_improvement=fallback_analysis["step_by_step_improvement"],
            learning_points=fallback_analysis["learning_points"],
            review_summary=fallback_analysis["review_summary"],
            comprehension_question="What is the importance of good variable naming in programming?",
            comprehension_answer="Good variable naming makes code more readable and maintainable.",
            explanation="Descriptive variable names help other developers (and yourself) understand what the code does.",
            improved_code="# Improved version\n# Add your improvements here",
            fix_explanation="This is a fallback version. The model should provide specific improvements.",
            difficulty_level=student_level,
            learning_objectives=fallback_analysis["learning_objectives"],
            estimated_time_to_improve=fallback_analysis["estimated_time_to_improve"]
        )


def main():
    """Main function to demonstrate the system with fine-tuned model"""
    print("Generative AI for Programming Education")
    print("Using Fine-tuned CodeLlama-7B Model")
    print("=" * 50)

    # System information
    print(f"Available GPUs: {torch.cuda.device_count()}")
    if torch.cuda.is_available():
        print("GPU Memory before loading:")
        get_gpu_memory()
    else:
        print("System Memory before loading:")
        get_system_memory()

    # Initialize the system with your fine-tuned model path
    # Update this path to point to your actual fine-tuned model
    model_path = r"C:\Users\farou\OneDrive - Aston University\finetunning"
    ai_tutor = ProgrammingEducationAI(model_path)

    try:
        # Load the fine-tuned model
        print("Loading fine-tuned model...")
        ai_tutor.load_model()
        print("✓ Model loaded successfully!")

        # Clear cache after loading
        clear_cuda_cache()
        if torch.cuda.is_available():
            print("GPU Memory after loading:")
            get_gpu_memory()
        else:
            print("System Memory after loading:")
            get_system_memory()

        # Example student code for testing
        student_code = """
def find_duplicates(numbers):
    x = []
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            if numbers[i] == numbers[j]:
                x.append(numbers[i])
    return x

# Test the function
result = find_duplicates([1, 2, 3, 2, 4, 5, 3])
print(result)
"""

        print(f"\nAnalyzing student code:\n{student_code}")

        # Get feedback using fine-tuned model
        feedback_list = ai_tutor.analyze_student_code(student_code, "beginner")

        print("\n" + "="*50)
        print("FINE-TUNED MODEL FEEDBACK:")
        print("="*50)

        for i, feedback in enumerate(feedback_list, 1):
            print(f"\n{i}. {feedback.feedback_type.upper()}:")
            print(f"   {feedback.feedback_message}")
            if feedback.suggested_improvement:
                print(f"   Suggestion: {feedback.suggested_improvement}")
            print(
                f"   Learning objectives: {', '.join(feedback.learning_objectives)}")

        # Demonstrate direct model calls
        print("\n" + "="*50)
        print("DIRECT MODEL GENERATION:")
        print("="*50)

        # Code review
        print("\n1. CODE REVIEW:")
        code_review = ai_tutor.generate_code_review(student_code, "beginner")
        print(code_review)

        # Educational feedback
        print("\n2. EDUCATIONAL FEEDBACK:")
        educational_feedback = ai_tutor.generate_educational_feedback(
            student_code, "beginner")
        print(educational_feedback)

        # Demonstrate comprehensive feedback system
        print("\n" + "="*50)
        print("COMPREHENSIVE EDUCATIONAL FEEDBACK SYSTEM:")
        print("="*50)

        comprehensive_feedback = ai_tutor.generate_comprehensive_feedback(
            student_code, "beginner")

        # Display comprehensive feedback
        print("\n📊 CODE ANALYSIS:")
        print("="*30)

        print("\n✅ STRENGTHS:")
        for i, strength in enumerate(comprehensive_feedback.strengths, 1):
            print(f"   {i}. {strength}")

        print("\n❌ WEAKNESSES:")
        for i, weakness in enumerate(comprehensive_feedback.weaknesses, 1):
            print(f"   {i}. {weakness}")

        print("\n⚠️ ISSUES:")
        for i, issue in enumerate(comprehensive_feedback.issues, 1):
            print(f"   {i}. {issue}")

        print("\n📝 STEP-BY-STEP IMPROVEMENT GUIDE:")
        print("="*40)
        for i, step in enumerate(comprehensive_feedback.step_by_step_improvement, 1):
            print(f"   Step {i}: {step}")

        print("\n🎓 LEARNING POINTS:")
        print("="*25)
        for i, point in enumerate(comprehensive_feedback.learning_points, 1):
            print(f"   {i}. {point}")

        print("\n📋 REVIEW SUMMARY:")
        print("="*20)
        print(f"   {comprehensive_feedback.review_summary}")

        print("\n❓ COMPREHENSION QUESTION:")
        print("="*30)
        print(f"   Question: {comprehensive_feedback.comprehension_question}")
        print(f"   Answer: {comprehensive_feedback.comprehension_answer}")
        print(f"   Explanation: {comprehensive_feedback.explanation}")

        print("\n🔧 IMPROVED CODE:")
        print("="*20)
        print(comprehensive_feedback.improved_code)

        print("\n💡 FIX EXPLANATION:")
        print("="*20)
        print(f"   {comprehensive_feedback.fix_explanation}")

        print("\n📊 METADATA:")
        print("="*15)
        print(f"   Student Level: {comprehensive_feedback.student_level}")
        print(
            f"   Learning Objectives: {', '.join(comprehensive_feedback.learning_objectives)}")
        print(
            f"   Estimated Time to Improve: {comprehensive_feedback.estimated_time_to_improve}")

    except Exception as e:
        print(f"Error: {e}")
        print(
            "Make sure to update the model_path variable to point to your fine-tuned model.")


if __name__ == "__main__":
    main()
