"""
Diagnostic App - Find out why the full model isn't working
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="Model Diagnostic",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Model Diagnostic Tool")
st.markdown("### Let's find out why your full model isn't working!")

# Diagnostic section
st.header("📊 System Diagnostics")

# Check 1: Python environment
st.subheader("1. Python Environment")
st.write(f"**Python Version:** {sys.version}")
st.write(f"**Working Directory:** {os.getcwd()}")

# Check 2: Required packages
st.subheader("2. Required Packages")
try:
    import streamlit
    st.success(f"✅ Streamlit: {streamlit.__version__}")
except ImportError as e:
    st.error(f"❌ Streamlit: {e}")

try:
    import torch
    st.success(f"✅ PyTorch: {torch.__version__}")
except ImportError as e:
    st.error(f"❌ PyTorch: {e}")

try:
    import transformers
    st.success(f"✅ Transformers: {transformers.__version__}")
except ImportError as e:
    st.error(f"❌ Transformers: {e}")

try:
    import accelerate
    st.success(f"✅ Accelerate: {accelerate.__version__}")
except ImportError as e:
    st.error(f"❌ Accelerate: {e}")

# Check 3: Fine-tuned model components
st.subheader("3. Fine-tuned Model Components")
try:
    from fine import ProgrammingEducationAI, ComprehensiveFeedback
    st.success("✅ Fine-tuned model components imported successfully")
    MODEL_AVAILABLE = True
except Exception as e:
    st.error(f"❌ Fine-tuned model components failed: {e}")
    MODEL_AVAILABLE = False

# Check 4: Environment variables
st.subheader("4. Environment Variables")
HF_TOKEN = os.getenv("HF_TOKEN", None)
if HF_TOKEN:
    st.success("✅ HF_TOKEN found")
    st.write(f"**Token starts with:** {HF_TOKEN[:10]}...")
else:
    st.warning("⚠️ HF_TOKEN not found")
    st.info("💡 Add HF_TOKEN to your environment variables or HF Spaces secrets")

# Check 5: Model path
st.subheader("5. Model Path Configuration")
model_path = "TomoriFarouk/codellama-7b-programming-education"
st.write(f"**Current model path:** {model_path}")
st.info("💡 Make sure this matches your actual model name on Hugging Face")

# Check 6: File structure
st.subheader("6. File Structure")
current_dir = os.getcwd()
st.write(f"**Current directory:** {current_dir}")

files = os.listdir(current_dir)
st.write("**Files in current directory:**")
for file in files:
    if file.endswith('.py'):
        st.write(f"  📄 {file}")

# Check 7: Fine.py file
st.subheader("7. Fine.py File Analysis")
fine_path = os.path.join(current_dir, "fine.py")
if os.path.exists(fine_path):
    st.success("✅ fine.py exists")
    file_size = os.path.getsize(fine_path)
    st.write(f"**File size:** {file_size:,} bytes")

    # Check if it has the required classes
    try:
        with open(fine_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "class ProgrammingEducationAI" in content:
                st.success("✅ ProgrammingEducationAI class found")
            else:
                st.error("❌ ProgrammingEducationAI class not found")

            if "class ComprehensiveFeedback" in content:
                st.success("✅ ComprehensiveFeedback class found")
            else:
                st.error("❌ ComprehensiveFeedback class not found")
    except Exception as e:
        st.error(f"❌ Error reading fine.py: {e}")
else:
    st.error("❌ fine.py not found")

# Check 8: Model files
st.subheader("8. Model Files")
models_dir = os.path.join(current_dir, "models")
if os.path.exists(models_dir):
    st.success("✅ models directory exists")
    model_files = os.listdir(models_dir)
    st.write("**Model files:**")
    for file in model_files:
        st.write(f"  📁 {file}")
else:
    st.warning("⚠️ models directory not found")

# Summary and recommendations
st.header("🎯 Summary & Recommendations")

if MODEL_AVAILABLE and HF_TOKEN:
    st.success("🎉 Everything looks good! Your model should work.")
    st.info("💡 Try using the full app now.")
elif not MODEL_AVAILABLE:
    st.error("❌ Fine-tuned model components are not available")
    st.markdown("""
    **Possible causes:**
    1. `fine.py` file is missing or corrupted
    2. Required dependencies are not installed
    3. Import error in `fine.py`
    
    **Solutions:**
    1. Make sure `fine.py` exists and is complete
    2. Install missing dependencies: `pip install torch transformers accelerate`
    3. Check for syntax errors in `fine.py`
    """)
elif not HF_TOKEN:
    st.warning("⚠️ HF_TOKEN is missing")
    st.markdown("""
    **To fix this:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token
    3. Add it to HF Spaces secrets as `HF_TOKEN`
    """)

# Test model loading
st.header("🧪 Test Model Loading")

if st.button("🚀 Test Model Loading"):
    if MODEL_AVAILABLE:
        with st.spinner("Testing model loading..."):
            try:
                model_path = "TomoriFarouk/codellama-7b-programming-education"
                ai_tutor = ProgrammingEducationAI(model_path)
                st.success("✅ Model class instantiated successfully")

                # Try to load the model
                try:
                    ai_tutor.load_model()
                    st.success("✅ Model loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Model loading failed: {e}")
                    st.info(
                        "💡 This usually means the model isn't uploaded to HF Model Hub yet")

            except Exception as e:
                st.error(f"❌ Model instantiation failed: {e}")
    else:
        st.error("❌ Cannot test - model components not available")

st.markdown("---")
st.info("💡 **Next Steps:** Fix the issues above, then try the main app again!")
