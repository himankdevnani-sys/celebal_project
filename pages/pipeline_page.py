"""
RAG Pipeline Visualization Page
Renders the step-by-step architectural workflow flow diagram for PatchContext.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_page_header
from components.pipeline import render_pipeline_visualization

def render_pipeline_page():
    render_page_header(
        title="RAG Pipeline Workflow",
        subtitle="End-to-end data pipeline diagram from repository ingestion to vector search, LLM generation, and NLI verification.",
        icon="⚡"
    )

    render_pipeline_visualization()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Active Pipeline Specs")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: 600;">VECTOR STORE</div>
            <div style="color: #58a6ff; font-weight: 700; font-size: 1.1rem;">FAISS FlatL2</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: 600;">RETRIEVER</div>
            <div style="color: #39d353; font-weight: 700; font-size: 1.1rem;">MMR (λ = 0.7)</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: 600;">EMBEDDING MODEL</div>
            <div style="color: #bc8cff; font-weight: 700; font-size: 1.1rem;">text-embedding-3-small</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: 600;">VERIFICATION GUARD</div>
            <div style="color: #d29922; font-weight: 700; font-size: 1.1rem;">NLI Entailment</div>
        </div>
        """, unsafe_allow_html=True)
