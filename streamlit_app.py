"""
AI Programming Tutor - Full Version with Fine-tuned Model Support
Works on Hugging Face Spaces with fallback to demo mode
"""

import streamlit as st
import os

# Configure page
st.set_page_config(
    page_title="AI Programming Tutor",
    page_icon="🤖",
    layout="wide"
)

# Try to import the fine-tuned model components
try:
    from fine import ProgrammingEducationAI, ComprehensiveFeedback
    MODEL_AVAILABLE = True
except Exception as e:
    MODEL_AVAILABLE = False

# Note: Using public model - no HF_TOKEN required
HF_TOKEN = None  # Set to None for public model


def demo_feedback(code_input):
    """Provide demo feedback when model is not available"""
    return {
        "strengths": [
            "Good code structure and formatting",
            "Clear variable naming",
            "Appropriate use of comments"
        ],
        "weaknesses": [
            "Could benefit from more error handling",
            "Consider adding input validation",
            "Documentation could be more comprehensive"
        ],
        "issues": [
            "Missing edge case handling",
            "No input validation present"
        ],
        "improvements": [
            "Add try-catch blocks for error handling",
            "Implement input validation",
            "Add comprehensive documentation"
        ],
        "learning_points": [
            "Error handling is crucial for robust code",
            "Input validation prevents unexpected behavior",
            "Good documentation helps with code maintenance"
        ],
        "comprehension_questions": [
            "What happens if the user enters invalid input?",
            "How would you handle exceptions in this code?",
            "What are the benefits of input validation?"
        ],
        "code_fix": f"# Improved version of your code:\n{code_input}\n\n# Add error handling and validation here"
    }


def main():
    st.title("🤖 AI Programming Tutor")
    st.markdown("### Enhancing Programming Education with Generative AI")

    # Sidebar for model selection
    with st.sidebar:
        st.header("⚙️ Settings")

        if MODEL_AVAILABLE:
            model_option = st.selectbox(
                "Choose Model:",
                ["Use Demo Mode", "Use Fine-tuned Model"],
                help="Demo mode works immediately. Fine-tuned model requires loading."
            )
        else:
            model_option = "Use Demo Mode"
            st.warning("⚠️ Fine-tuned model not available - using demo mode")
            st.info(
                "💡 To enable AI model: Make sure your model is uploaded to HF Model Hub as public")

        student_level = st.selectbox(
            "Student Level:",
            ["beginner", "intermediate", "advanced"],
            help="Adjusts feedback complexity"
        )

        st.markdown("---")
        st.markdown("### 📚 About")
        st.markdown("""
        This AI tutor provides structured feedback on programming code:
        
        - **Strengths**: What you did well
        - **Weaknesses**: Areas for improvement
        - **Issues**: Problems to fix
        - **Improvements**: Step-by-step guidance
        - **Learning Points**: Key concepts to understand
        - **Questions**: Test your comprehension
        - **Code Fix**: Improved version
        """)

        # Show model status
        if MODEL_AVAILABLE:
            st.success("✅ Fine-tuned model available")
            st.success("🌐 Using public model - no authentication required")
        else:
            st.error("❌ Fine-tuned model not available")

    # Main content
    st.markdown("---")

    # Code input
    code_input = st.text_area(
        "📝 Enter your code here:",
        height=200,
        placeholder="def hello_world():\n    print('Hello, World!')\n    return 'success'",
        help="Paste your Python code here for analysis"
    )

    if st.button("🚀 Analyze Code", type="primary"):
        if not code_input.strip():
            st.warning("⚠️ Please enter some code to analyze")
            return

        with st.spinner("🤖 Analyzing your code..."):
            try:
                if model_option == "Use Fine-tuned Model" and MODEL_AVAILABLE:
                    # Check if model is already loaded
                    if 'ai_tutor' not in st.session_state:
                        with st.spinner("🚀 Loading fine-tuned model (this may take 5-10 minutes on HF Spaces)..."):
                            try:
                                # Use Hugging Face Model Hub
                                # Replace with your actual model name
                                model_path = "FaroukTomori/codellama-7b-programming-education"

                                # Using public model - no authentication required
                                st.info(
                                    "🌐 Using public model - no authentication required")

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
                            code_input, student_level)
                        st.success(
                            "✅ Feedback generated using fine-tuned model!")
                    else:
                        # Fallback to demo mode
                        feedback = demo_feedback(code_input)
                        st.success("✅ Demo feedback generated as fallback!")
                else:
                    # Demo mode
                    feedback = demo_feedback(code_input)
                    st.success("✅ Demo feedback generated!")

                # Display feedback in tabs
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "✅ Strengths", "❌ Weaknesses", "🚨 Issues",
                    "📈 Improvements", "🎓 Learning", "❓ Questions", "🔧 Code Fix"
                ])

                with tab1:
                    st.subheader("✅ Code Strengths")
                    if isinstance(feedback, dict):
                        for strength in feedback["strengths"]:
                            st.markdown(f"• {strength}")
                    else:
                        for strength in feedback.strengths:
                            st.markdown(f"• {strength}")

                with tab2:
                    st.subheader("❌ Areas for Improvement")
                    if isinstance(feedback, dict):
                        for weakness in feedback["weaknesses"]:
                            st.markdown(f"• {weakness}")
                    else:
                        for weakness in feedback.weaknesses:
                            st.markdown(f"• {weakness}")

                with tab3:
                    st.subheader("🚨 Issues to Address")
                    if isinstance(feedback, dict):
                        for issue in feedback["issues"]:
                            st.markdown(f"• {issue}")
                    else:
                        for issue in feedback.issues:
                            st.markdown(f"• {issue}")

                with tab4:
                    st.subheader("📈 Step-by-Step Improvements")
                    if isinstance(feedback, dict):
                        for i, improvement in enumerate(feedback["improvements"], 1):
                            st.markdown(f"{i}. {improvement}")
                    else:
                        for i, step in enumerate(feedback.step_by_step_improvement, 1):
                            st.markdown(f"**Step {i}:** {step}")

                with tab5:
                    st.subheader("🎓 Key Learning Points")
                    if isinstance(feedback, dict):
                        for point in feedback["learning_points"]:
                            st.markdown(f"• {point}")
                    else:
                        for point in feedback.learning_points:
                            st.markdown(f"• {point}")

                with tab6:
                    st.subheader("❓ Comprehension Questions")
                    if isinstance(feedback, dict):
                        for i, question in enumerate(feedback["comprehension_questions"], 1):
                            st.markdown(f"**Q{i}:** {question}")
                    else:
                        st.markdown(
                            f"**Question:** {feedback.comprehension_question}")
                        st.markdown(
                            f"**Answer:** {feedback.comprehension_answer}")
                        st.markdown(f"**Explanation:** {feedback.explanation}")

                with tab7:
                    st.subheader("🔧 Improved Code")
                    if isinstance(feedback, dict):
                        st.code(feedback["code_fix"], language="python")
                    else:
                        st.code(feedback.improved_code, language="python")
                        st.markdown("**What Changed:**")
                        st.info(feedback.fix_explanation)

                st.success(
                    "✅ Analysis complete! Review each tab for comprehensive feedback.")

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                st.info("💡 Try using demo mode or check your code input")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application error: {e}")
        st.info("💡 Please refresh the page and try again")
