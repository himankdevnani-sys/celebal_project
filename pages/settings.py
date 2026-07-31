"""
Settings & System Configuration Page
Allows runtime tuning of LLMs, vector search parameters, top-k, MMR lambda, and backend options.
Communicates strictly via services/api.py.
"""
import streamlit as st
from utils.config import config
from components.header import render_page_header

def render_settings_page():
    render_page_header(
        title="Settings & RAG Configuration",
        subtitle="Dynamically update retrieval thresholds, LLM engines, vector search parameters, and backend mode.",
        icon="⚙"
    )

    st.markdown("### 🔌 Backend Mode & Connection Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        use_mock_toggle = st.toggle(
            "Use Mock Service Mode (Standalone Frontend)",
            value=config.USE_MOCK,
            help="When enabled, PatchContext uses built-in realistic mock data. When disabled, calls live FastAPI backend endpoints."
        )
    with col2:
        backend_url_input = st.text_input(
            "Backend REST API URL",
            value=config.BACKEND_URL,
            placeholder="http://localhost:8000"
        )

    st.markdown("---")
    st.markdown("### 🤖 LLM & Embedding Engine Selection")

    col3, col4 = st.columns(2)
    with col3:
        llm_model = st.selectbox(
            "LLM Generation Model",
            options=["llama-3.3-70b-versatile", "gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"],
            index=0
        )
    with col4:
        embedding_model = st.selectbox(
            "Embedding Model",
            options=["text-embedding-3-small", "text-embedding-3-large", "bge-large-en-v1.5"],
            index=0
        )

    st.markdown("---")
    st.markdown("### 🎯 Vector Retrieval Parameters")

    col5, col6, col7 = st.columns(3)
    with col5:
        top_k = st.slider("Top-K Retrieved Documents", min_value=1, max_value=20, value=config.TOP_K)
    with col6:
        similarity_threshold = st.slider("Similarity Threshold Score", min_value=0.0, max_value=1.0, value=config.SIMILARITY_THRESHOLD, step=0.05)
    with col7:
        mmr_lambda = st.slider("MMR Diversity Lambda (λ)", min_value=0.0, max_value=1.0, value=config.MMR_LAMBDA, step=0.05)

    col8, col9, col10 = st.columns(3)
    with col8:
        temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.0, value=config.TEMPERATURE, step=0.05)
    with col9:
        chunk_size = st.number_input("Document Chunk Size", min_value=128, max_value=2048, value=config.CHUNK_SIZE, step=64)
    with col10:
        chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=512, value=config.CHUNK_OVERLAP, step=16)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 Save Configuration Changes", type="primary"):
        config.USE_MOCK = use_mock_toggle
        config.BACKEND_URL = backend_url_input
        config.MODEL_NAME = llm_model
        config.EMBEDDING_MODEL = embedding_model
        config.TOP_K = top_k
        config.SIMILARITY_THRESHOLD = similarity_threshold
        config.MMR_LAMBDA = mmr_lambda
        config.TEMPERATURE = temperature
        config.CHUNK_SIZE = chunk_size
        config.CHUNK_OVERLAP = chunk_overlap

        st.success("✅ Settings updated successfully! All active RAG queries will use the updated configuration.")
        st.rerun()
