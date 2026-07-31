"""
AI Answer Focus View Page
Dedicated view for reading synthesized AI architectural answers, inline citations, and ground truth references.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_page_header
from components.cards import render_citations

def render_ai_answer_page():
    render_page_header(
        title="AI Answer Engine",
        subtitle="Synthesized architectural reasoning grounded in FastAPI repository evidence.",
        icon="🧠"
    )

    query = st.session_state.get("current_query", "Why was APIRouter introduced?")

    if "rag_answer" not in st.session_state or not st.session_state.rag_answer:
        st.info("No active query answer found. Generating response for default architectural query...")
        ans = api.ask_repository(query)
        st.session_state.rag_answer = ans
    else:
        ans = st.session_state.rag_answer

    # Query Badge
    st.markdown(f"""
    <div style="background: rgba(22, 27, 34, 0.8); border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin-bottom: 1.5rem;">
        <span style="color: #8b949e; font-size: 0.85rem;">Target Question:</span>
        <strong style="color: #58a6ff; margin-left: 6px; font-size: 1.05rem;">"{ans.query}"</strong>
    </div>
    """, unsafe_allow_html=True)

    # Synthesized Answer Card
    st.markdown("""
    <div class="glass-card" style="padding: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 0.75rem; margin-bottom: 1rem;">
            <div style="font-weight: 700; color: #58a6ff; font-size: 1.2rem;">
                🧠 Synthesized Answer
            </div>
            <div style="font-size: 0.8rem; color: #8b949e;">
                Model: <span style="color: #bc8cff; font-weight: 600;">{ans.model_name}</span>
            </div>
        </div>
    """.format(ans=ans), unsafe_allow_html=True)

    st.markdown(ans.markdown_answer)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Citations
    render_citations(ans.citations)

    # Copy Raw Markdown Section
    with st.expander("📋 View & Copy Raw Markdown"):
        st.code(ans.markdown_answer, language="markdown")
