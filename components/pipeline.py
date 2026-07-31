"""
RAG Pipeline Visualization Component
Renders an interactive step-by-step workflow flow diagram for PatchContext RAG processing.
"""
import streamlit as st

PIPELINE_STEPS = [
    {
        "step": 1,
        "title": "GitHub Repository",
        "icon": "📦",
        "description": "FastAPI Git commit logs, PR threads, issue comments, and discussion markdown parsed via GitPython API.",
        "badge": "Source Data",
        "color": "#58a6ff"
    },
    {
        "step": 2,
        "title": "Document Chunking",
        "icon": "✂️",
        "description": "Recursive character splitting with code-aware boundary detection (chunk size 512, overlap 64).",
        "badge": "LangChain Splitter",
        "color": "#bc8cff"
    },
    {
        "step": 3,
        "title": "Dense Embeddings",
        "icon": "🧠",
        "description": "Vectorization using OpenAI `text-embedding-3-small` producing 1536-dimensional embeddings.",
        "badge": "OpenAI Embeddings",
        "color": "#39d353"
    },
    {
        "step": 4,
        "title": "Vector DB Index",
        "icon": "⚡",
        "description": "FAISS (Facebook AI Similarity Search) index housing 84,500+ pre-calculated repository vectors.",
        "badge": "FAISS Engine",
        "color": "#f778ba"
    },
    {
        "step": 5,
        "title": "MMR Retrieval",
        "icon": "🎯",
        "description": "Maximal Marginal Relevance (MMR λ=0.7) balancing similarity with retrieval diversity across PRs & Commits.",
        "badge": "Retriever (Top-5)",
        "color": "#d29922"
    },
    {
        "step": 6,
        "title": "Context Assembly",
        "icon": "📑",
        "description": "Concatenation of raw diffs, issue comments, and metadata into structured prompt context window.",
        "badge": "Context Window",
        "color": "#79c0ff"
    },
    {
        "step": 7,
        "title": "LLM Synthesis",
        "icon": "🤖",
        "description": "GPT-4o-mini / Llama-3.3-70b synthesis of architectural reasoning with strict ground truth constraints.",
        "badge": "Groq / OpenAI",
        "color": "#bc8cff"
    },
    {
        "step": 8,
        "title": "NLI Verification",
        "icon": "🛡️",
        "description": "Natural Language Inference cross-verification enforcing zero unsupported claims before display.",
        "badge": "Hallucination Guard",
        "color": "#39d353"
    },
    {
        "step": 9,
        "title": "Final Answer & Citations",
        "icon": "✨",
        "description": "Rich markdown explanation with clickable GitHub commit SHAs and PR issue citations.",
        "badge": "Verified Answer",
        "color": "#58a6ff"
    }
]

def render_pipeline_visualization():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <p style="color: #8b949e; font-size: 0.95rem;">
            End-to-end data processing workflow powering PatchContext Retrieval-Augmented Generation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, step in enumerate(PIPELINE_STEPS):
        col_idx = idx % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div class="glass-card" style="position: relative; padding: 1.25rem; margin-bottom: 1rem; border-left: 4px solid {step['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem;">{step['icon']}</span>
                    <span style="background: {step['color']}22; color: {step['color']}; border: 1px solid {step['color']}55; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">
                        Step {step['step']} • {step['badge']}
                    </span>
                </div>
                <h4 style="margin: 0 0 0.3rem 0; color: #f0f6fc; font-size: 1rem;">{step['title']}</h4>
                <p style="margin: 0; color: #8b949e; font-size: 0.82rem; line-height: 1.4;">{step['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            if idx < len(PIPELINE_STEPS) - 1 and (idx + 1) % 3 != 0:
                st.markdown("<div style='text-align: center; color: #30363d; font-size: 1.2rem; margin: -0.5rem 0;'>⬇️</div>", unsafe_allow_html=True)
