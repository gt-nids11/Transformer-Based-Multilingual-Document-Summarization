import os
import streamlit as st
from utils import extract_text, detect_document_language, get_document_stats, validate_file
from summarizer import generate_summary

# Prevent library conflicts/crashes on Windows (Intel MKL/OMP)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Page configuration
st.set_page_config(
    page_title="Multilingual Document Summarizer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #0E1117;
        color: #E2E8F0;
    }
    
    /* Document/Workspace Containers */
    div[data-testid="stVerticalBlockBorder"] {
        background-color: #1A1D24 !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }
    div[data-testid="stVerticalBlockBorder"]:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(99, 179, 237, 0.15) !important;
        border-color: #3182CE !important;
    }
    
    /* Text styling overrides */
    h1, h2, h3, h4, h5, h6, label, p, span {
        color: #E2E8F0 !important;
    }
    
    /* File Uploader styling */
    [data-testid="stFileUploader"] {
        background-color: #12141C !important;
        border: 2px dashed #4A5568 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        transition: border-color 0.2s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #3182CE !important;
    }
    
    /* Drag-and-drop label legibility */
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] div {
        color: #F7FAFC !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
    }
    [data-testid="stFileUploader"] small {
        color: #A0AEC0 !important;
        font-weight: 500 !important;
    }
    
    /* Browse files button inside uploader */
    [data-testid="stFileUploader"] button {
        background-color: #2D3748 !important;
        color: #E2E8F0 !important;
        border: 1px solid #4A5568 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #3182CE !important;
        border-color: #63B3ED !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 12px rgba(49, 130, 206, 0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Primary buttons (Summarize button) */
    button[kind="primary"] {
        background-color: #3182CE !important;
        border: 1px solid #4299E1 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 6px rgba(49, 130, 206, 0.3) !important;
        transition: all 0.2s ease !important;
        border-radius: 6px !important;
    }
    button[kind="primary"]:hover {
        background-color: #2B6CB0 !important;
        border-color: #3182CE !important;
        box-shadow: 0 6px 12px rgba(49, 130, 206, 0.5) !important;
        transform: translateY(-1px);
    }
    
    /* Metric Card styling */
    .metric-card {
        background-color: #12141C;
        border-radius: 6px;
        padding: 12px;
        border-left: 4px solid #3182CE;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #63B3ED;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Summary container style */
    .summary-card {
        background-color: #12141C;
        border: 1px solid #2D3748;
        border-left: 5px solid #48BB78;
        border-radius: 6px;
        padding: 18px;
        margin-top: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
    }
</style>
""", unsafe_allow_html=True)

# 1. Header Section
st.markdown("<h1 style='text-align: center;'>📄 Transformer-Based Multilingual Document Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A0AEC0; font-size: 1.1rem; margin-bottom: 2rem;'>Upload documents and generate concise summaries in multiple languages using NLP and Transformers.</p>", unsafe_allow_html=True)

# 2. Upload Section
uploaded_file = st.file_uploader(
    "Choose a PDF/TXT document",
    type=["pdf", "txt"],
    help="We validate all files before running NLP processing."
)

if uploaded_file is not None:
    filename = uploaded_file.name
    
    # Validate file format
    if not validate_file(filename):
        st.error("❌ Unsupported file format. Please upload a PDF (.pdf) or TXT (.txt) file.")
    else:
        # Extract text with loading spinner
        with st.spinner("📄 Extracting text from document..."):
            try:
                raw_text = extract_text(uploaded_file, filename)
            except Exception as e:
                st.error(f"❌ Error extracting text from document: {e}")
                st.stop()
                
        # Validate content size
        if not raw_text.strip():
            st.error("⚠️ The uploaded document is empty or has no extractable text.")
        elif len(raw_text.split()) < 15:
            st.warning("⚠️ The document has very little text (less than 15 words). Please upload a more detailed document.")
        else:
            # Language Detection & Stats
            lang_code, lang_name = detect_document_language(raw_text)
            stats = get_document_stats(raw_text)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3. Document Information Card (Metric Grid)
            with st.container(border=True):
                st.markdown("### 📊 Document Information")
                m_col1, m_col2, m_col3 = st.columns(3)
                
                with m_col1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{lang_name}</div><div class="metric-label">Language</div></div>', unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["words"]:,}</div><div class="metric-label">Word Count</div></div>', unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{stats["characters"]:,}</div><div class="metric-label">Character Count</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 4. Original Text Preview
            with st.container(border=True):
                st.markdown("### 📖 Original Text Preview")
                preview_text = raw_text[:1000]
                if len(raw_text) > 1000:
                    preview_text += "\n\n... [Truncated for preview] ..."
                
                # Scrollable container using text_area
                st.text_area(
                    label="Showing first 1000 characters of the document:",
                    value=preview_text,
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 5. Summarization Trigger
            if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
                # Generates abstractive summary using cached mT5 model with load spinner
                with st.spinner("🧠 Generating abstractive summary using pre-trained mT5 model..."):
                    try:
                        summary = generate_summary(raw_text, num_beams=1)
                        
                        if not summary:
                            st.warning("⚠️ Could not generate summary. Check if the document has sufficient logical sentences.")
                        else:
                            # 6. Display Summary Card
                            st.markdown(f"""
                            <div class="summary-card">
                                <h3 style="color: #48BB78; margin-top: 0;">📝 Generated Summary</h3>
                                <p style="line-height: 1.6; color: #E2E8F0; font-size: 1.05rem;">{summary}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(f"❌ Summarization failed: {e}")
