"""
DocVerify AI - Streamlit Dashboard
Beautiful UI for document verification.
"""

import streamlit as st
import requests

# --- Config ---
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DocVerify AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for beautiful styling ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
        border-right: 1px solid #e94560;
    }

    /* Headers */
    h1, h2, h3 {
        color: #e94560 !important;
        font-weight: 700 !important;
    }

    /* Cards */
    .css-1r6slb0, .stContainer {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(233,69,96,0.2) 0%, rgba(15,52,96,0.3) 100%);
        border: 1px solid rgba(233,69,96,0.3);
        border-radius: 12px;
        padding: 15px;
    }

    [data-testid="stMetricValue"] {
        color: #e94560 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #eee !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(233,69,96,0.4);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.05);
        border: 2px dashed rgba(233,69,96,0.5);
        border-radius: 15px;
        padding: 20px;
    }

    /* Success/Error/Warning boxes */
    .stSuccess {
        background: linear-gradient(90deg, rgba(0,200,117,0.2) 0%, rgba(0,150,87,0.1) 100%);
        border-left: 4px solid #00c875;
        border-radius: 8px;
    }

    .stError {
        background: linear-gradient(90deg, rgba(233,69,96,0.2) 0%, rgba(200,50,80,0.1) 100%);
        border-left: 4px solid #e94560;
        border-radius: 8px;
    }

    .stWarning {
        background: linear-gradient(90deg, rgba(255,190,11,0.2) 0%, rgba(200,150,0,0.1) 100%);
        border-left: 4px solid #ffbe0b;
        border-radius: 8px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #eee;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e94560 0%, #ff6b6b 100%);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }

    /* Text colors */
    p, span, label {
        color: #eee !important;
    }

    /* Divider */
    hr {
        border-color: rgba(233,69,96,0.3);
    }

    /* Custom card class */
    .result-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(233,69,96,0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }

    .field-item {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        border-left: 3px solid #e94560;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("# 🛡️ DocVerify AI")
    st.markdown("---")

    # Animated status indicator
    try:
        health = requests.get(f"{API_URL}/health", timeout=2).json()
        if health.get("processor_initialized"):
            st.markdown("""
                <div style="background: linear-gradient(90deg, #00c875, #00a65a);
                            padding: 12px 20px; border-radius: 25px; text-align: center;">
                    <span style="color: white; font-weight: 600;">🟢 System Online</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Initializing...")
    except:
        st.markdown("""
            <div style="background: linear-gradient(90deg, #e94560, #c73e54);
                        padding: 12px 20px; border-radius: 25px; text-align: center;">
                <span style="color: white; font-weight: 600;">🔴 Offline</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Supported Documents")
    docs = ["Aadhaar Card", "PAN Card", "Voter ID", "Driving License", "Passport", "Birth Certificate"]
    for doc in docs:
        st.markdown(f"<div style='padding: 5px 10px; margin: 3px 0; background: rgba(233,69,96,0.1); border-radius: 5px; font-size: 14px;'>✓ {doc}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌐 Languages")
    st.markdown("English • Hindi • Tamil • Telugu")

# --- Main Content ---
st.markdown("""
    <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">
        🛡️ DocVerify AI
    </h1>
    <p style="text-align: center; color: #aaa; font-size: 1.1rem; margin-top: 5px;">
        AI-Powered Document Verification for Indian Government IDs
    </p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Verify Document", "📋 History", "📊 Analytics"])

# ============================================
# TAB 1: Verification
# ============================================
with tab1:
    uploaded_file = st.file_uploader(
        "Drop your document here or click to browse",
        type=["png", "jpg", "jpeg", "pdf", "tiff"],
        help="Supported: Aadhaar, PAN, Voter ID, DL, Passport, Birth Certificate"
    )

    if uploaded_file:
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 📄 Document Preview")
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, use_container_width=True)
            else:
                st.info(f"📄 **{uploaded_file.name}**")

        with col2:
            st.markdown("### ✨ Verification Results")

            if st.button("🚀 Verify Now", use_container_width=True):

                # Progress animation
                progress = st.progress(0, text="Initializing...")

                try:
                    progress.progress(20, text="📤 Uploading document...")
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                    progress.progress(40, text="🔍 Running OCR...")
                    resp = requests.post(f"{API_URL}/api/v1/verify", files=files, timeout=60)

                    progress.progress(80, text="✅ Validating fields...")

                    if resp.status_code == 200:
                        result = resp.json()
                        progress.progress(100, text="Done!")
                        progress.empty()

                        # Status Card
                        is_valid = result.get("validation", {}).get("is_valid", False)
                        status = result.get("status", "unknown")

                        if status == "success" and is_valid:
                            st.markdown("""
                                <div style="background: linear-gradient(90deg, #00c875, #00a65a);
                                            padding: 20px; border-radius: 12px; text-align: center; margin: 15px 0;">
                                    <span style="font-size: 2rem;">✅</span><br>
                                    <span style="color: white; font-size: 1.3rem; font-weight: 700;">Document Verified</span>
                                </div>
                            """, unsafe_allow_html=True)
                        elif status == "success":
                            st.markdown("""
                                <div style="background: linear-gradient(90deg, #ffbe0b, #e09f00);
                                            padding: 20px; border-radius: 12px; text-align: center; margin: 15px 0;">
                                    <span style="font-size: 2rem;">⚠️</span><br>
                                    <span style="color: white; font-size: 1.3rem; font-weight: 700;">Validation Issues</span>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Processing Failed")

                        # Metrics
                        m1, m2 = st.columns(2)
                        doc_type = result.get("document_type", "unknown").replace("_", " ").title()
                        confidence = result.get("confidence", 0)
                        m1.metric("📄 Document Type", doc_type)
                        m2.metric("🎯 Confidence", f"{confidence:.0%}")

                        # Extracted Fields
                        fields = result.get("extracted_fields", {})
                        if fields:
                            st.markdown("#### 📝 Extracted Information")
                            for k, v in fields.items():
                                label = k.replace("_", " ").title()
                                st.markdown(f"""
                                    <div class="field-item">
                                        <strong>{label}:</strong> {v}
                                    </div>
                                """, unsafe_allow_html=True)

                        # Validation Errors
                        errors = result.get("validation", {}).get("errors", {})
                        if errors:
                            st.markdown("#### ❌ Validation Errors")
                            for field, err in errors.items():
                                st.error(f"**{field}**: {err}")

                        # Raw Response
                        with st.expander("🔧 View Raw API Response"):
                            st.json(result)
                    else:
                        progress.empty()
                        st.error(f"API Error: {resp.text}")

                except requests.exceptions.ConnectionError:
                    progress.empty()
                    st.error("🔌 Cannot connect to API. Is the server running?")
                except Exception as e:
                    progress.empty()
                    st.error(f"Error: {e}")
    else:
        # Empty state
        st.markdown("""
            <div style="text-align: center; padding: 60px 20px;
                        background: rgba(255,255,255,0.02); border-radius: 20px;
                        border: 2px dashed rgba(233,69,96,0.3);">
                <span style="font-size: 4rem;">📄</span><br><br>
                <span style="color: #aaa; font-size: 1.2rem;">
                    Upload a document to get started
                </span><br>
                <span style="color: #666; font-size: 0.9rem;">
                    Supports Aadhaar, PAN, Voter ID, and more
                </span>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: History
# ============================================
with tab2:
    st.markdown("### 📋 Recent Documents")

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    try:
        resp = requests.get(f"{API_URL}/api/v1/documents?limit=10", timeout=5)
        if resp.status_code == 200:
            docs = resp.json().get("documents", [])

            if docs:
                for doc in docs:
                    status = doc.get("status", "pending")
                    status_color = "#00c875" if status == "verified" else "#ffbe0b" if status == "uploaded" else "#e94560"

                    st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 15px 20px;
                                    border-radius: 10px; margin: 10px 0; display: flex;
                                    justify-content: space-between; align-items: center;
                                    border-left: 4px solid {status_color};">
                            <div>
                                <strong style="color: #eee;">{doc.get("file_name", "Unknown")}</strong><br>
                                <small style="color: #888;">{doc.get("uploaded_at", "")[:19]}</small>
                            </div>
                            <div style="background: {status_color}; padding: 5px 15px;
                                        border-radius: 20px; color: white; font-size: 0.85rem;">
                                {status.upper()}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No documents uploaded yet")
        else:
            st.warning("Could not load documents")
    except:
        st.warning("API not available")

# ============================================
# TAB 3: Analytics
# ============================================
with tab3:
    st.markdown("### 📊 Verification Analytics")

    try:
        resp = requests.get(f"{API_URL}/api/v1/analytics/summary", timeout=5)

        if resp.status_code == 200:
            stats = resp.json()

            # Big metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📄 Documents", stats.get("total_documents", 0))
            c2.metric("🔍 Verifications", stats.get("total_verifications", 0))
            c3.metric("✅ Successful", stats.get("verified_successfully", 0))

            rate = stats.get("success_rate", 0)
            c4.metric("📈 Success Rate", f"{rate:.0%}")

            st.markdown("---")

            # By document type
            by_type = stats.get("by_document_type", {})
            if by_type:
                st.markdown("#### 📋 By Document Type")
                cols = st.columns(len(by_type) if len(by_type) <= 4 else 4)
                for i, (doc_type, count) in enumerate(by_type.items()):
                    with cols[i % 4]:
                        label = doc_type.replace("_", " ").title()
                        st.metric(label, count)
            else:
                st.info("No verification data yet. Start verifying documents!")
        else:
            st.info("No analytics data available")
    except:
        st.warning("API not available")

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        <strong style="color: #e94560;">DocVerify AI</strong> © 2025<br>
        Powered by PaddleOCR • Gemini • FastAPI
    </div>
""", unsafe_allow_html=True)
