"""
AI Programming Tutor - Hugging Face Spaces Compatible Version
Optimized to avoid all permission errors and work reliably on HF Spaces
"""

import streamlit as st
import os
import tempfile

# Disable Streamlit telemetry and cache to avoid permission issues
os.environ['STREAMLIT_TELEMETRY_ENABLED'] = 'false'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

# Create temp directory for any cache needs
try:
    temp_dir = tempfile.mkdtemp()
    os.environ['STREAMLIT_CACHE_DIR'] = temp_dir
except:
    pass

# Configure page
st.set_page_config(
    page_title="AI Programming Tutor",
    page_icon="🤖",
    layout="wide"
)


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
        model_option = st.selectbox(
            "Choose Model:",
            ["Use Demo Mode", "Load Fine-tuned Model"],
            help="Demo mode works immediately, fine-tuned model requires setup"
        )

        if model_option == "Load Fine-tuned Model":
            st.info("🔧 Fine-tuned model requires Hugging Face Model Hub setup")
            st.info("📝 See README.md for setup instructions")

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
                # For now, use demo mode
                feedback = demo_feedback(code_input)

                # Display feedback in tabs
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "✅ Strengths", "❌ Weaknesses", "🚨 Issues",
                    "📈 Improvements", "🎓 Learning", "❓ Questions", "🔧 Code Fix"
                ])

                with tab1:
                    st.subheader("✅ Code Strengths")
                    for strength in feedback["strengths"]:
                        st.markdown(f"• {strength}")

                with tab2:
                    st.subheader("❌ Areas for Improvement")
                    for weakness in feedback["weaknesses"]:
                        st.markdown(f"• {weakness}")

                with tab3:
                    st.subheader("🚨 Issues to Address")
                    for issue in feedback["issues"]:
                        st.markdown(f"• {issue}")

                with tab4:
                    st.subheader("📈 Step-by-Step Improvements")
                    for i, improvement in enumerate(feedback["improvements"], 1):
                        st.markdown(f"{i}. {improvement}")

                with tab5:
                    st.subheader("🎓 Key Learning Points")
                    for point in feedback["learning_points"]:
                        st.markdown(f"• {point}")

                with tab6:
                    st.subheader("❓ Comprehension Questions")
                    for i, question in enumerate(feedback["comprehension_questions"], 1):
                        st.markdown(f"**Q{i}:** {question}")

                with tab7:
                    st.subheader("🔧 Improved Code")
                    st.code(feedback["code_fix"], language="python")

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
