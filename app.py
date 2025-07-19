"""
Simplified AI Programming Tutor for Hugging Face Spaces
Optimized to avoid permission errors and work reliably on HF Spaces
"""

import streamlit as st
import os

# Try to import the fine-tuned model components
try:
    from fine import ProgrammingEducationAI, ComprehensiveFeedback
    MODEL_AVAILABLE = True
except Exception as e:
    MODEL_AVAILABLE = False

# Note: Using public model - no HF_TOKEN required
HF_TOKEN = None

st.title("🤖 AI Programming Tutor")
st.write("### Full AI Model Version - Shows Detailed Errors")

# Show model status
with st.sidebar:
    st.header("⚙️ Model Status")
    if MODEL_AVAILABLE:
        st.success("✅ Fine-tuned model available")
        st.success("🌐 Using public model - no authentication required")
        st.info(f"📁 Model path: FaroukTomori/codellama-7b-programming-education")
    else:
        st.error("❌ Fine-tuned model not available")
        st.error(f"🔍 Import error: {e}")
        st.info("💡 Check the import error above to fix the issue")

code = st.text_area("Enter your code:", height=200)

if st.button("Analyze with AI Model", type="primary"):
    if not code.strip():
        st.warning("Please enter some code!")
        return

    if not MODEL_AVAILABLE:
        st.error("❌ Cannot analyze - fine-tuned model components not available")
        st.error("🔍 Check the import error in the sidebar")
        return

    with st.spinner("🤖 Loading AI model..."):
        try:
            # Load the fine-tuned model
            model_path = "FaroukTomori/codellama-7b-programming-education"
            st.info(f"🔍 Attempting to load model from: {model_path}")

            ai_tutor = ProgrammingEducationAI(model_path)
            st.success("✅ Model class instantiated successfully")

            ai_tutor.load_model()
            st.success("✅ Model loaded successfully!")

            # Generate feedback
            feedback = ai_tutor.generate_comprehensive_feedback(
                code, "beginner")
            st.success("✅ AI feedback generated!")

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Strengths")
                for strength in feedback.strengths:
                    st.write(f"• {strength}")

            with col2:
                st.subheader("❌ Improvements")
                for weakness in feedback.weaknesses:
                    st.write(f"• {weakness}")

            st.subheader("🔧 Improved Code")
            st.code(feedback.improved_code, language="python")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.error("🔍 Full error details:")
            st.code(str(e), language="text")
            st.info("💡 Check the error above to understand what went wrong")
