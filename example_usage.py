"""
Example Usage of the Comprehensive Educational Feedback System
"""

from fine import ProgrammingEducationAI
import json


def main():
    print("🎓 Comprehensive Educational Feedback System")
    print("=" * 60)

    # Initialize the system
    # Update this path to your actual fine-tuned model
    model_path = r"C:\Users\farou\OneDrive - Aston University\finetunning"
    ai_tutor = ProgrammingEducationAI(model_path)

    try:
        # Load the model
        print("Loading fine-tuned model...")
        ai_tutor.load_model()
        print("✅ Model loaded successfully!")

        # Example 1: Beginner student code
        print("\n" + "="*60)
        print("EXAMPLE 1: BEGINNER STUDENT")
        print("="*60)

        beginner_code = """
def find_duplicates(numbers):
    x = []
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            if numbers[i] == numbers[j]:
                x.append(numbers[i])
    return x

result = find_duplicates([1, 2, 3, 2, 4, 5, 3])
print(result)
"""

        print("Student Code:")
        print(beginner_code)

        feedback = ai_tutor.generate_comprehensive_feedback(
            beginner_code, "beginner")
        display_comprehensive_feedback(feedback)

        # Example 2: Intermediate student code
        print("\n" + "="*60)
        print("EXAMPLE 2: INTERMEDIATE STUDENT")
        print("="*60)

        intermediate_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 10 Fibonacci numbers
for i in range(10):
    print(fibonacci(i))
"""

        print("Student Code:")
        print(intermediate_code)

        feedback = ai_tutor.generate_comprehensive_feedback(
            intermediate_code, "intermediate")
        display_comprehensive_feedback(feedback)

        # Example 3: Advanced student code
        print("\n" + "="*60)
        print("EXAMPLE 3: ADVANCED STUDENT")
        print("="*60)

        advanced_code = """
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def process(self):
        result = []
        for item in self.data:
            if item > 0:
                result.append(item * 2)
        return result

processor = DataProcessor([1, -2, 3, -4, 5])
output = processor.process()
print(output)
"""

        print("Student Code:")
        print(advanced_code)

        feedback = ai_tutor.generate_comprehensive_feedback(
            advanced_code, "advanced")
        display_comprehensive_feedback(feedback)

    except Exception as e:
        print(f"❌ Error: {e}")
        print(
            "💡 Make sure to update the model_path to point to your actual fine-tuned model.")


def display_comprehensive_feedback(feedback):
    """Display comprehensive feedback in a formatted way"""

    print("\n📊 COMPREHENSIVE FEEDBACK")
    print("-" * 40)

    # Analysis
    print("\n✅ STRENGTHS:")
    for i, strength in enumerate(feedback.strengths, 1):
        print(f"   {i}. {strength}")

    print("\n❌ WEAKNESSES:")
    for i, weakness in enumerate(feedback.weaknesses, 1):
        print(f"   {i}. {weakness}")

    print("\n⚠️ ISSUES:")
    for i, issue in enumerate(feedback.issues, 1):
        print(f"   {i}. {issue}")

    # Educational content
    print("\n📝 STEP-BY-STEP IMPROVEMENT:")
    for i, step in enumerate(feedback.step_by_step_improvement, 1):
        print(f"   Step {i}: {step}")

    print("\n🎓 LEARNING POINTS:")
    for i, point in enumerate(feedback.learning_points, 1):
        print(f"   {i}. {point}")

    print(f"\n📋 REVIEW SUMMARY:")
    print(f"   {feedback.review_summary}")

    # Interactive elements
    print(f"\n❓ COMPREHENSION QUESTION:")
    print(f"   Q: {feedback.comprehension_question}")
    print(f"   A: {feedback.comprehension_answer}")
    print(f"   Explanation: {feedback.explanation}")

    # Code fixes
    print(f"\n🔧 IMPROVED CODE:")
    print(feedback.improved_code)

    print(f"\n💡 FIX EXPLANATION:")
    print(f"   {feedback.fix_explanation}")

    # Metadata
    print(f"\n📊 METADATA:")
    print(f"   Student Level: {feedback.student_level}")
    print(f"   Learning Objectives: {', '.join(feedback.learning_objectives)}")
    print(
        f"   Estimated Time to Improve: {feedback.estimated_time_to_improve}")


def save_feedback_to_json(feedback, filename):
    """Save feedback to JSON file for later analysis"""
    feedback_dict = {
        "code_snippet": feedback.code_snippet,
        "student_level": feedback.student_level,
        "strengths": feedback.strengths,
        "weaknesses": feedback.weaknesses,
        "issues": feedback.issues,
        "step_by_step_improvement": feedback.step_by_step_improvement,
        "learning_points": feedback.learning_points,
        "review_summary": feedback.review_summary,
        "comprehension_question": feedback.comprehension_question,
        "comprehension_answer": feedback.comprehension_answer,
        "explanation": feedback.explanation,
        "improved_code": feedback.improved_code,
        "fix_explanation": feedback.fix_explanation,
        "learning_objectives": feedback.learning_objectives,
        "estimated_time_to_improve": feedback.estimated_time_to_improve
    }

    with open(filename, 'w') as f:
        json.dump(feedback_dict, f, indent=2)

    print(f"💾 Feedback saved to {filename}")


if __name__ == "__main__":
    main()
