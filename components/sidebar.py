"""
Sidebar Navigation & Status Component
Renders the left navigation menu and system status indicators.
"""
import streamlit as st
from utils.config import config
from services.api import api

PAGE_OPTIONS = [
    ("🏠 Home", "Home"),
    ("💬 Ask Repository", "Ask Repository"),
    ("📚 Retrieved Evidence", "Retrieved Evidence"),
    ("🧠 AI Answer", "AI Answer"),
    ("🛡 Verification", "Verification"),
    ("📈 Repository Timeline", "Repository Timeline"),
    ("⚡ RAG Pipeline", "RAG Pipeline"),
    ("📊 Evaluation Dashboard", "Evaluation Dashboard"),
    ("⚙ Settings", "Settings"),
    ("ℹ About", "About")
]

def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 0.5rem;">
            <h2 style="margin: 0; color: #58a6ff; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.02em;">
                ⚡ PatchContext
            </h2>
            <p style="font-size: 0.75rem; color: #8b949e; margin-top: 4px; font-style: italic;">
                "Understand why FastAPI evolved the way it did."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Radio Buttons
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = "Home"

        page_labels = [p[0] for p in PAGE_OPTIONS]
        # Find index of current selected page
        current_index = 0
        for idx, (label, key) in enumerate(PAGE_OPTIONS):
            if key == st.session_state.selected_page:
                current_index = idx
                break

        selected_label = st.radio(
            "Navigation",
            options=page_labels,
            index=current_index,
            label_visibility="collapsed"
        )
        
        # Update session state
        for label, key in PAGE_OPTIONS:
            if label == selected_label:
                st.session_state.selected_page = key

        st.markdown("---")
        
        # System & Backend Status Panel
        st.markdown("""
        <div style="font-size: 0.8rem; font-weight: 600; color: #8b949e; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">
            System Status
        </div>
        """, unsafe_allow_html=True)

        mode_badge = '<span class="badge badge-tech">MOCK MODE</span>' if config.USE_MOCK else '<span class="badge badge-verified">LIVE BACKEND</span>'
        
        st.markdown(f"""
        <div style="background: rgba(22, 27, 34, 0.9); border: 1px solid #30363d; border-radius: 8px; padding: 10px; font-size: 0.78rem;">
            <div style="margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #c9d1d9;">Engine:</span>
                {mode_badge}
            </div>
            <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                <span style="color: #c9d1d9;">Target Repo:</span>
                <span style="color: #58a6ff; font-weight: 600;">fastapi/fastapi</span>
            </div>
            <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                <span style="color: #c9d1d9;">Vector Store:</span>
                <span style="color: #39d353; font-weight: 600;">FAISS (84.5k)</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #c9d1d9;">LLM:</span>
                <span style="color: #bc8cff; font-weight: 600;">Llama 3.3 70B</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("PatchContext v1.0.0 • Designed for FastAPI Insights")

    return st.session_state.selected_page
