"""
AI Programming Tutor - Full Version with Fine-tuned Model Support
Works on Hugging Face Spaces with fallback to demo mode
Version: 2.0 - No Demo Fallback, Shows Detailed Errors
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


# Demo feedback function removed - app now shows actual errors instead of falling back to demo


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

            # Show current model path
            st.info(f"📁 Model path: FaroukTomori/codellama-7b-programming-education")

            # Show if model is loaded in session
            if 'ai_tutor' in st.session_state:
                st.success("✅ Model loaded in session")
            else:
                st.info("⏳ Model not loaded yet - will load when you analyze code")
        else:
            st.error("❌ Fine-tuned model not available")
            st.error("🔍 Check the import error above to fix the issue")

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

                                st.info(
                                    f"🔍 Attempting to load model from: {model_path}")

                                ai_tutor = ProgrammingEducationAI(model_path)
                                st.success(
                                    "✅ Model class instantiated successfully")

                                ai_tutor.load_model()
                                st.session_state['ai_tutor'] = ai_tutor
                                st.success(
                                    "✅ Fine-tuned model loaded successfully!")
                            except Exception as e:
                                st.error(f"❌ Error loading model: {e}")
                                st.error("🔍 Full error details:")
                                st.code(str(e), language="text")
                                st.info(
                                    "💡 Check the error above to fix the model loading issue")
                                return  # Stop here and show the error

                    if 'ai_tutor' in st.session_state:
                        # Use fine-tuned model
                        try:
                            feedback = st.session_state['ai_tutor'].generate_comprehensive_feedback(
                                code_input, student_level)
                            st.success(
                                "✅ Feedback generated using fine-tuned model!")
                        except Exception as e:
                            st.error(f"❌ Error generating feedback: {e}")
                            st.error("🔍 Full error details:")
                            st.code(str(e), language="text")
                            st.info(
                                "💡 Check the error above to fix the feedback generation issue")
                            return
                    else:
                        # Model failed to load - show error instead of falling back
                        st.error(
                            "❌ Model failed to load - cannot generate feedback")
                        st.info("💡 Fix the model loading error above first")
                        return
                else:
                    # Model not available or not selected - show error
                    if not MODEL_AVAILABLE:
                        st.error("❌ Fine-tuned model components not available")
                        st.error("🔍 Check the import error in the sidebar")
                        return
                    else:
                        st.error(
                            "❌ Please select 'Use Fine-tuned Model' to analyze with AI")
                        st.info("💡 The model is available but not selected")
                        return

                # Display AI feedback in tabs
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "✅ Strengths", "❌ Weaknesses", "🚨 Issues",
                    "📈 Improvements", "🎓 Learning", "❓ Questions", "🔧 Code Fix"
                ])

                with tab1:
                    st.subheader("✅ Code Strengths")
                    for strength in feedback.strengths:
                        st.markdown(f"• {strength}")

                with tab2:
                    st.subheader("❌ Areas for Improvement")
                    for weakness in feedback.weaknesses:
                        st.markdown(f"• {weakness}")

                with tab3:
                    st.subheader("🚨 Issues to Address")
                    for issue in feedback.issues:
                        st.markdown(f"• {issue}")

                with tab4:
                    st.subheader("📈 Step-by-Step Improvements")
                    for i, step in enumerate(feedback.step_by_step_improvement, 1):
                        st.markdown(f"**Step {i}:** {step}")

                with tab5:
                    st.subheader("🎓 Key Learning Points")
                    for point in feedback.learning_points:
                        st.markdown(f"• {point}")

                with tab6:
                    st.subheader("❓ Comprehension Questions")
                    st.markdown(
                        f"**Question:** {feedback.comprehension_question}")
                    st.markdown(f"**Answer:** {feedback.comprehension_answer}")
                    st.markdown(f"**Explanation:** {feedback.explanation}")

                with tab7:
                    st.subheader("🔧 Improved Code")
                    st.code(feedback.improved_code, language="python")
                    st.markdown("**What Changed:**")
                    st.info(feedback.fix_explanation)

                st.success(
                    "✅ Analysis complete! Review each tab for comprehensive feedback.")

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                st.error("🔍 Full error details:")
                st.code(str(e), language="text")
                st.info("💡 Check the error above to understand what went wrong")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application error: {e}")
        st.info("💡 Please refresh the page and try again")
