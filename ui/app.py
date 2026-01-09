import streamlit as st
import requests
import json
import time

# --- Config ---
API_URL = "http://localhost:8000"
APP_TITLE = "DocVerify AI"
APP_ICON = "🔍"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title(f"{APP_ICON} {APP_TITLE}")
st.sidebar.markdown("---")
st.sidebar.info("AI-Powered Document Verification Platform")

# Health Check Indicator
try:
    health = requests.get(f"{API_URL}/health", timeout=2).json()
    st.sidebar.success(f"System Online ({health.get('agents', {}).keys()})")
except Exception:
    st.sidebar.error("System Offline")

# --- Main Layout ---
st.title(f"{APP_ICON} Document Verification")
st.markdown("Upload a document (**Aadhaar, PAN, etc.**) to verify its authenticity.")

# File Uploader
uploaded_file = st.file_uploader("Choose a document...", type=["pdf", "png", "jpg", "jpeg", "tiff"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Preview")
        # Display image preview if image
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption="Preview", use_container_width=True)
        else:
            st.info(f"PDF Document: {uploaded_file.name}")
            
    with col2:
        st.subheader("Verification")
        if st.button("Verify Document", type="primary"):
            with st.status("Processing Document...", expanded=True) as status:
                st.write("📤 Uploading...")
                
                try:
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    st.write("🤖 Agents Analyzing...")
                    response = requests.post(f"{API_URL}/api/v1/verify", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        status.update(label="Verification Complete!", state="complete", expanded=False)
                        st.success("Analysis Successful")
                        
                        # Display Results
                        st.json(result)
                        
                        # Mock Visuals
                        mock_data = result.get("mock_result", {})
                        st.metric("Document Type", mock_data.get("document_type", "Unknown"))
                        
                    else:
                        status.update(label="Verification Failed", state="error")
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    status.update(label="Connection Error", state="error")
                    st.error(f"Failed to connect to API: {e}")

else:
    st.info("👆 Upload a file to get started.")

# Footer
st.markdown("---")
st.caption("© 2025 DocVerify AI - Powered by Gemini & Ollama")
