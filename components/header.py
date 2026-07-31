"""
Header UI Component
Renders styled page headers, hero sections, and badge titles.
"""
import streamlit as st

def render_hero_section():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">PatchContext</div>
        <div class="hero-subtitle">
            Understand why <strong>FastAPI</strong> evolved the way it did using Retrieval-Augmented Generation (RAG) over commit logs, PR discussions, and issue history.
        </div>
        <div style="margin-top: 1.25rem;">
            <span class="badge badge-commit">🔍 Commit History Search</span>
            <span class="badge badge-pr">🔀 PR Discussion Explorer</span>
            <span class="badge badge-issue">💬 Issue Reasoning</span>
            <span class="badge badge-verified">🛡️ Hallucination Detection</span>
            <span class="badge badge-tech">📈 Repository Timeline</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str, icon: str = "⚡"):
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem; border-bottom: 1px solid #30363d; padding-bottom: 1rem;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700; color: #f0f6fc; display: flex; align-items: center; gap: 10px;">
            <span>{icon}</span> <span>{title}</span>
        </h1>
        <p style="margin: 0.35rem 0 0 0; color: #8b949e; font-size: 0.95rem;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
