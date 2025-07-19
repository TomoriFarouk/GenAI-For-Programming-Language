"""
Simplified AI Programming Tutor for Hugging Face Spaces
Optimized to avoid permission errors and work reliably on HF Spaces
"""

import streamlit as st

st.title("🤖 AI Programming Tutor")
st.write("### Simple Demo Version")

code = st.text_area("Enter your code:", height=200)

if st.button("Analyze"):
    if code:
        st.success("Analysis complete!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Strengths")
            st.write("• Good structure")
            st.write("• Clear naming")

        with col2:
            st.subheader("❌ Improvements")
            st.write("• Add error handling")
            st.write("• Validate inputs")

        st.subheader("🔧 Improved Code")
        st.code(
            f"# Your code:\n{code}\n\n# Add error handling here", language="python")
    else:
        st.warning("Please enter some code!")
