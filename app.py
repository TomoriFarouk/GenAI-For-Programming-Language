"""
AI Programming Tutor - Hugging Face Spaces Deployment
Comprehensive Educational Feedback System
"""

import json
from fine import ProgrammingEducationAI, ComprehensiveFeedback
import streamlit as st
import torch
import os
import gc
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Environment setup for HF Spaces
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
os.environ["DATASETS_DISABLE_MULTIPROCESSING"] = "1"

# Clear CUDA cache if available
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    gc.collect()


def main():
    st.set_page_config(
        page_title="AI Programming Tutor",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🎓 AI Programming Tutor")
    st.subheader("Comprehensive Educational Feedback System")
    st.markdown("---")

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Model selection
        model_option = st.selectbox(
            "Choose Model:",
            ["Use Demo Mode", "Use Fine-tuned Model"],
            help="Demo mode works immediately. Fine-tuned model requires loading (5-10 minutes on HF Spaces)."
        )

        # Student level selection
        student_level = st.selectbox(
            "Student Level:",
            ["beginner", "intermediate", "advanced"],
            help="Adjusts feedback complexity and learning objectives"
        )

        # Memory info for HF Spaces
        if st.checkbox("Show System Info"):
            import psutil
            memory = psutil.virtual_memory()
            st.metric("Available RAM",
                      f"{memory.available / (1024**3):.1f} GB")
            st.metric("RAM Usage", f"{memory.percent}%")
            st.metric("CPU Cores", psutil.cpu_count())

        # HF Spaces specific instructions
        st.markdown("---")
        st.markdown("### 🚀 Hugging Face Spaces")
        st.info("""
        **Hardware**: 2 vCPU, 16GB RAM (FREE)
        
        **Recommendations**:
        - Use Demo Mode for quick testing
        - Fine-tuned model takes 5-10 minutes to load
        - 16GB RAM is sufficient for your model
        """)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Student Code Input")

        # Code input
        student_code = st.text_area(
            "Paste your Python code here:",
            height=300,
            placeholder="""# Example code to test:
def find_duplicates(numbers):
    x = []
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            if numbers[i] == numbers[j]:
                x.append(numbers[i])
    return x

# Test the function
result = find_duplicates([1, 2, 3, 2, 4, 5, 3])
print(result)""",
            help="Paste your Python code here for analysis"
        )

        # Generate feedback button
        if st.button("🎯 Generate Comprehensive Feedback", type="primary"):
            if not student_code.strip():
                st.warning("⚠️ Please enter some code first!")
            else:
                generate_feedback(student_code, student_level, model_option)

    with col2:
        st.header("📊 Feedback Results")

        if 'feedback' in st.session_state:
            display_feedback(st.session_state['feedback'])


def generate_feedback(code: str, student_level: str, model_option: str):
    """Generate comprehensive feedback using the AI tutor or demo mode"""
    with st.spinner("🤖 Analyzing your code..."):
        try:
            if model_option == "Use Fine-tuned Model":
                # Check if model is already loaded
                if 'ai_tutor' not in st.session_state:
                    with st.spinner("🚀 Loading fine-tuned model (this may take 5-10 minutes on HF Spaces)..."):
                        try:
                            # Use relative path for HF Spaces
                            model_path = "./model"  # Will be updated when model is uploaded
                            ai_tutor = ProgrammingEducationAI(model_path)
                            ai_tutor.load_model()
                            st.session_state['ai_tutor'] = ai_tutor
                            st.success(
                                "✅ Fine-tuned model loaded successfully!")
                        except Exception as e:
                            st.error(f"❌ Error loading model: {e}")
                            st.info("💡 Switching to demo mode...")
                            model_option = "Use Demo Mode"

                if 'ai_tutor' in st.session_state:
                    # Use fine-tuned model
                    feedback = st.session_state['ai_tutor'].generate_comprehensive_feedback(
                        code, student_level)
                    st.session_state['feedback'] = feedback
                    st.success("✅ Feedback generated using fine-tuned model!")
                else:
                    # Fallback to demo mode
                    feedback = create_demo_feedback(code, student_level)
                    st.session_state['feedback'] = feedback
                    st.success("✅ Demo feedback generated as fallback!")
            else:
                # Demo mode
                feedback = create_demo_feedback(code, student_level)
                st.session_state['feedback'] = feedback
                st.success("✅ Demo feedback generated!")
        except Exception as e:
            st.error(f"❌ Error generating feedback: {e}")
            # Fallback to demo mode
            feedback = create_demo_feedback(code, student_level)
            st.session_state['feedback'] = feedback
            st.success("✅ Demo feedback generated as fallback!")


def create_demo_feedback(code: str, student_level: str) -> ComprehensiveFeedback:
    """Create demo feedback for testing without model"""
    return ComprehensiveFeedback(
        code_snippet=code,
        student_level=student_level,
        strengths=[
            "Your code has a clear structure and logic",
            "You're using appropriate Python syntax",
            "The function name is descriptive"
        ],
        weaknesses=[
            "Variable names could be more descriptive",
            "Missing comments explaining the logic",
            "Could benefit from error handling"
        ],
        issues=[
            "Using generic variable names (x, i, j)",
            "No input validation",
            "Nested loops could be optimized"
        ],
        step_by_step_improvement=[
            "Step 1: Replace 'x' with 'duplicates' for better readability",
            "Step 2: Add comments explaining the nested loop logic",
            "Step 3: Consider using a set for O(n) time complexity",
            "Step 4: Add input validation for edge cases"
        ],
        learning_points=[
            "Good variable naming improves code readability and maintainability",
            "Comments help others (and yourself) understand complex logic",
            "Algorithm complexity matters - O(n²) vs O(n) can make a huge difference",
            "Always consider edge cases and input validation"
        ],
        review_summary="Your code works correctly but could be improved with better naming, comments, and optimization. The logic is sound for a beginner level.",
        comprehension_question="What is the time complexity of your current algorithm and how could you improve it?",
        comprehension_answer="The current algorithm has O(n²) time complexity due to nested loops. It could be improved to O(n) using a hash set.",
        explanation="Nested loops multiply their complexities. Using a set allows us to check for duplicates in O(1) time per element.",
        improved_code="""def find_duplicates(numbers):
    # Use a set for O(n) time complexity
    duplicates = []
    seen = set()
    
    for num in numbers:
        if num in seen:
            duplicates.append(num)
        else:
            seen.add(num)
    
    return duplicates

# Test the function
result = find_duplicates([1, 2, 3, 2, 4, 5, 3])
print(result)""",
        fix_explanation="The improved version uses a set to track seen numbers, reducing time complexity from O(n²) to O(n) and making the code more readable with better variable names.",
        difficulty_level=student_level,
        learning_objectives=["algorithm_complexity",
                             "code_readability", "best_practices"],
        estimated_time_to_improve="10-15 minutes"
    )


def display_feedback(feedback: ComprehensiveFeedback):
    """Display comprehensive feedback in a progressive learning flow"""

    # Initialize session state for tracking progress
    if 'quiz_completed' not in st.session_state:
        st.session_state['quiz_completed'] = False
    if 'current_step' not in st.session_state:
        st.session_state['current_step'] = 1

    # Progress indicator
    st.markdown("### 🎯 Learning Progress")
    progress_bar = st.progress(0)

    # Calculate progress based on current step
    if st.session_state['current_step'] == 1:
        progress_bar.progress(20)
    elif st.session_state['current_step'] == 2:
        progress_bar.progress(40)
    elif st.session_state['current_step'] == 3:
        progress_bar.progress(60)
    elif st.session_state['current_step'] == 4:
        progress_bar.progress(80)
    elif st.session_state['current_step'] == 5:
        progress_bar.progress(100)

    # Step 1: Analysis (Always available)
    if st.session_state['current_step'] >= 1:
        st.markdown("### 📊 Step 1: Code Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### ✅ Strengths")
            for i, strength in enumerate(feedback.strengths, 1):
                st.markdown(f"**{i}.** {strength}")

        with col2:
            st.markdown("#### ❌ Weaknesses")
            for i, weakness in enumerate(feedback.weaknesses, 1):
                st.markdown(f"**{i}.** {weakness}")

        with col3:
            st.markdown("#### ⚠️ Issues")
            for i, issue in enumerate(feedback.issues, 1):
                st.markdown(f"**{i}.** {issue}")

        st.markdown("#### 📋 Review Summary")
        st.info(feedback.review_summary)

        if st.session_state['current_step'] == 1:
            if st.button("✅ I understand the analysis - Continue to Step 2", type="primary"):
                st.session_state['current_step'] = 2
                st.rerun()

    # Step 2: Improvement Guide (Available after Step 1)
    if st.session_state['current_step'] >= 2:
        st.markdown("---")
        st.markdown("### 📝 Step 2: Improvement Guide")

        st.markdown("#### Step-by-Step Instructions")
        for i, step in enumerate(feedback.step_by_step_improvement, 1):
            st.markdown(f"**Step {i}:** {step}")

        st.markdown("---")
        st.markdown(
            f"**⏱️ Estimated time to improve:** {feedback.estimated_time_to_improve}")

        if st.session_state['current_step'] == 2:
            if st.button("✅ I understand the improvement steps - Continue to Step 3", type="primary"):
                st.session_state['current_step'] = 3
                st.rerun()

    # Step 3: Learning Points (Available after Step 2)
    if st.session_state['current_step'] >= 3:
        st.markdown("---")
        st.markdown("### 🎓 Step 3: Learning Points")

        st.markdown("#### Key Concepts to Understand")
        for i, point in enumerate(feedback.learning_points, 1):
            st.markdown(f"**{i}.** {point}")

        st.markdown("---")
        st.markdown("#### 🎯 Learning Objectives")
        for objective in feedback.learning_objectives:
            st.markdown(f"• {objective}")

        if st.session_state['current_step'] == 3:
            if st.button("✅ I understand the learning points - Continue to Step 4", type="primary"):
                st.session_state['current_step'] = 4
                st.rerun()

    # Step 4: Comprehension Quiz (Available after Step 3)
    if st.session_state['current_step'] >= 4:
        st.markdown("---")
        st.markdown("### ❓ Step 4: Comprehension Check")

        st.markdown(
            "**Before you see the solution, let's test your understanding:**")
        st.markdown(f"**Question:** {feedback.comprehension_question}")

        # Quiz interface
        user_answer = st.text_area(
            "Your answer:",
            placeholder="Type your answer here...",
            height=100,
            key="quiz_answer"
        )

        if st.button("Check My Answer", type="primary"):
            if user_answer.strip():
                st.markdown("**Correct Answer:**")
                st.success(feedback.comprehension_answer)
                st.markdown("**Explanation:**")
                st.info(feedback.explanation)

                if not st.session_state['quiz_completed']:
                    st.session_state['quiz_completed'] = True
                    st.session_state['current_step'] = 5
                    st.rerun()
            else:
                st.warning("Please provide an answer first!")

    # Step 5: Code Fix (Only available after completing quiz)
    if st.session_state['current_step'] >= 5 and st.session_state['quiz_completed']:
        st.markdown("---")
        st.markdown("### 🔧 Step 5: Improved Code Solution")

        st.markdown(
            "🎉 **Congratulations! You've completed the learning process. Here's the improved version:**")

        st.markdown("#### 🔧 Enhanced Version")
        st.code(feedback.improved_code, language="python")

        st.markdown("#### 💡 What Changed")
        st.info(feedback.fix_explanation)

        # Reset button for new analysis
        if st.button("🔄 Analyze New Code", type="secondary"):
            st.session_state['current_step'] = 1
            st.session_state['quiz_completed'] = False
            if 'feedback' in st.session_state:
                del st.session_state['feedback']
            st.rerun()

    # Display metadata
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Student Level", feedback.student_level.title())
    with col2:
        st.metric("Learning Objectives", len(feedback.learning_objectives))
    with col3:
        st.metric("Issues Found", len(feedback.issues))


if __name__ == "__main__":
    main()
