"""
Web Interface for Generative AI Programming Education System
"""

import streamlit as st
import sys
import os
from fine import ProgrammingEducationAI, ComprehensiveFeedback
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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

        # Model path input
        model_path = st.text_input(
            "Fine-tuned Model Path",
            value="path/to/your/finetuned/codellama-7b-model",
            help="Enter the path to your fine-tuned CodeLlama-7B model"
        )

        # Student level selection
        student_level = st.selectbox(
            "Student Level",
            ["beginner", "intermediate", "advanced"],
            index=0,
            help="Select the student's skill level for personalized feedback"
        )

        # Load model button
        load_model = st.button("🚀 Load Model", type="primary")

        if load_model:
            with st.spinner("Loading fine-tuned model..."):
                try:
                    # Initialize AI tutor
                    ai_tutor = ProgrammingEducationAI(model_path)
                    ai_tutor.load_model()
                    st.session_state['ai_tutor'] = ai_tutor
                    st.success("✅ Model loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Error loading model: {e}")
                    st.info(
                        "💡 Make sure to update the model path to point to your actual fine-tuned model.")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Student Code")

        # Code input
        student_code = st.text_area(
            "Enter your code here:",
            height=400,
            placeholder="""def find_duplicates(numbers):
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
        if st.button("🎯 Generate Comprehensive Feedback", type="primary", disabled='ai_tutor' not in st.session_state):
            if not student_code.strip():
                st.warning("⚠️ Please enter some code first!")
            elif 'ai_tutor' not in st.session_state:
                st.warning("⚠️ Please load the model first!")
            else:
                generate_feedback(student_code, student_level)

    with col2:
        st.header("📊 Feedback Results")

        if 'feedback' in st.session_state:
            display_feedback(st.session_state['feedback'])


def generate_feedback(code: str, student_level: str):
    """Generate comprehensive feedback using the AI tutor"""
    with st.spinner("🤖 Analyzing your code..."):
        try:
            ai_tutor = st.session_state['ai_tutor']
            feedback = ai_tutor.generate_comprehensive_feedback(
                code, student_level)
            st.session_state['feedback'] = feedback
            st.success("✅ Feedback generated successfully!")
        except Exception as e:
            st.error(f"❌ Error generating feedback: {e}")


def display_feedback(feedback: ComprehensiveFeedback):
    """Display comprehensive feedback in an organized way"""

    # Create tabs for different feedback sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analysis",
        "📝 Improvement Guide",
        "🎓 Learning",
        "❓ Quiz",
        "🔧 Code Fix"
    ])

    with tab1:
        st.subheader("Code Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### ✅ Strengths")
            for i, strength in enumerate(feedback.strengths, 1):
                st.markdown(f"**{i}.** {strength}")

        with col2:
            st.markdown("### ❌ Weaknesses")
            for i, weakness in enumerate(feedback.weaknesses, 1):
                st.markdown(f"**{i}.** {weakness}")

        with col3:
            st.markdown("### ⚠️ Issues")
            for i, issue in enumerate(feedback.issues, 1):
                st.markdown(f"**{i}.** {issue}")

        st.markdown("### 📋 Review Summary")
        st.info(feedback.review_summary)

    with tab2:
        st.subheader("Step-by-Step Improvement Guide")

        for i, step in enumerate(feedback.step_by_step_improvement, 1):
            st.markdown(f"**Step {i}:** {step}")

        st.markdown("---")
        st.markdown(
            f"**⏱️ Estimated time to improve:** {feedback.estimated_time_to_improve}")

    with tab3:
        st.subheader("Learning Points")

        for i, point in enumerate(feedback.learning_points, 1):
            st.markdown(f"**{i}.** {point}")

        st.markdown("---")
        st.markdown("### 🎯 Learning Objectives")
        for objective in feedback.learning_objectives:
            st.markdown(f"• {objective}")

    with tab4:
        st.subheader("Comprehension Check")

        st.markdown(f"**Question:** {feedback.comprehension_question}")

        # Create a quiz interface
        user_answer = st.text_area(
            "Your answer:",
            placeholder="Type your answer here...",
            height=100
        )

        if st.button("Check Answer"):
            if user_answer.strip():
                st.markdown("**Correct Answer:**")
                st.success(feedback.comprehension_answer)
                st.markdown("**Explanation:**")
                st.info(feedback.explanation)
            else:
                st.warning("Please provide an answer first!")

    with tab5:
        st.subheader("Improved Code")

        st.markdown("### 🔧 Enhanced Version")
        st.code(feedback.improved_code, language="python")

        st.markdown("### 💡 What Changed")
        st.info(feedback.fix_explanation)

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
