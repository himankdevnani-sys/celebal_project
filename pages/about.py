"""
About & Project Overview Page
Explains PatchContext RAG system over FastAPI repository history and lists technologies.
Communicates strictly via services/api.py.
"""
import streamlit as st
from components.header import render_page_header

TECH_STACK = [
    ("FastAPI", "High-performance Python web framework (target indexed repository)", "#059669"),
    ("LangChain", "Orchestration layer for document loading, splitting, and prompt chaining", "#1d4ed8"),
    ("FAISS", "Facebook AI Similarity Search vector database indexing 84,500+ code chunks", "#7c3aed"),
    ("OpenAI Embeddings", "text-embedding-3-small generating 1536-dimensional dense vector embeddings", "#0284c7"),
    ("GPT-4o-mini / Groq Llama 3.3", "LLM reasoning engines synthesizing clear architectural answers", "#d97706"),
    ("MMR Retrieval", "Maximal Marginal Relevance algorithm balancing similarity with document diversity", "#dc2626"),
    ("Streamlit", "Modern, responsive pythonic web interface with custom dark theme styling", "#ff4b4b"),
    ("RAGAs", "Automated evaluation metrics framework scoring precision, recall, and faithfulness", "#0891b2"),
    ("NLI Verification", "Natural Language Inference guardrails enforcing zero ungrounded claim hallucinations", "#16a34a")
]

def render_about_page():
    render_page_header(
        title="About PatchContext",
        subtitle="Understand the architectural evolution and design history of FastAPI using RAG.",
        icon="ℹ"
    )

    st.markdown("""
    <div class="glass-card" style="padding: 1.75rem;">
        <h3 style="margin-top: 0; color: #58a6ff; font-weight: 700;">📌 Project Overview</h3>
        <p style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.6;">
            <strong>PatchContext</strong> is an AI-powered Retrieval-Augmented Generation (RAG) system built over the historical record of the 
            <a href="https://github.com/fastapi/fastapi" target="_blank" style="color: #58a6ff;">FastAPI repository</a>.
        </p>
        <p style="color: #8b949e; font-size: 0.9rem; line-height: 1.6;">
            Developers often ask why certain design decisions were made—such as why <code>APIRouter</code> was introduced, why async execution was structured in threadpools, or why <code>@app.on_event</code> was deprecated in favor of Starlette Lifespan context managers.
            PatchContext mines commit messages, pull request comments, issue threads, and core author reasoning to deliver verified, citation-backed answers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Technology Stack")

    cols = st.columns(3)
    for idx, (name, desc, color) in enumerate(TECH_STACK):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="glass-card" style="height: 150px; border-left: 3px solid {color};">
                <h4 style="margin: 0 0 0.4rem 0; color: #f0f6fc; font-size: 1rem;">{name}</h4>
                <p style="margin: 0; color: #8b949e; font-size: 0.83rem; line-height: 1.4;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #f0f6fc;">Open Source Repository Link</h4>
        <p style="color: #8b949e; font-size: 0.88rem; margin-bottom: 1rem;">
            Primary indexed resource: <code>https://github.com/fastapi/fastapi</code>
        </p>
        <a href="https://github.com/fastapi/fastapi" target="_blank" style="background-color: #238636; color: white; padding: 8px 18px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
            ⭐ Star FastAPI on GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)
