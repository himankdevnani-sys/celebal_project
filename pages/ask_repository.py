"""
Ask Repository Search Page
Main interactive query engine executing real vector search & RAG with Debug Mode Tracing.
Communicates strictly via services/api.py.
"""
import streamlit as st
import time
from services.api import api
from components.header import render_page_header
from components.cards import render_evidence_card, render_verification_panel, render_citations

def render_ask_repository_page():
    render_page_header(
        title="Ask Repository",
        subtitle="Semantic RAG query engine exploring FastAPI commit history, PRs, and architectural decisions.",
        icon="💬"
    )

    sample_queries = api.get_sample_queries()

    # Preset Clickable Example Question Pills
    st.markdown("<div style='font-size: 0.85rem; font-weight: 600; color: #8b949e; margin-bottom: 6px;'>TRY PRESET QUESTIONS:</div>", unsafe_allow_html=True)
    
    col_pills = st.columns(len(sample_queries))
    selected_preset = None
    for idx, sq in enumerate(sample_queries):
        with col_pills[idx]:
            if st.button(sq["question"], key=f"btn_sq_{idx}", use_container_width=True):
                selected_preset = sq["question"]

    # Search Bar Input
    default_query = selected_preset or st.session_state.get("current_query", "What is FastAPI dependency injection?")
    
    query_input = st.text_input(
        "Enter your architectural question:",
        value=default_query,
        placeholder="What is FastAPI dependency injection?",
        key="search_input_field"
    )

    col1, col2 = st.columns([3, 1])
    with col2:
        search_clicked = st.button("⚡ Ask PatchContext", type="primary", use_container_width=True)

    if search_clicked or selected_preset:
        st.session_state.current_query = query_input
        
        # Step-by-step Visual Progress Flow
        st.markdown("<br>", unsafe_allow_html=True)
        progress_placeholder = st.empty()
        
        flow_steps = [
            ("🔍 Question Received & Expanded", 15),
            ("📂 Query Embedding & BM25 Keyword Search", 35),
            ("⚡ FAISS Vector Search (768-dim BAAI/bge-base-en)", 55),
            ("📊 CrossEncoder Reranking (ms-marco-MiniLM)", 75),
            ("🛡️ NLI Hallucination Verification", 90),
            ("🧠 Finalizing AI Answer & Citations", 100)
        ]

        with progress_placeholder.container():
            pbar = st.progress(0)
            status_text = st.empty()
            for text, val in flow_steps:
                status_text.markdown(f"<span style='color: #58a6ff; font-weight: 600;'>{text}...</span>", unsafe_allow_html=True)
                pbar.progress(val)
                time.sleep(0.06)
        
        progress_placeholder.empty()

        with st.spinner("Executing real RAG pipeline & vector search..."):
            rag_answer = api.ask_repository(query_input)
            st.session_state.rag_answer = rag_answer

    # Display Answer & Results if present in session state
    if "rag_answer" in st.session_state and st.session_state.rag_answer:
        ans = st.session_state.rag_answer
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")

        # Real Measured Latency & Token Metrics
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            st.metric("Total Latency", f"{ans.total_latency_ms:.1f} ms")
        with mcol2:
            st.metric("Retrieval Latency", f"{ans.retrieval_latency_ms:.1f} ms")
        with mcol3:
            st.metric("Total Tokens", f"{ans.prompt_tokens + ans.completion_tokens}")
        with mcol4:
            st.metric("Model Engine", ans.model_name)

        # Verification Guard Panel with Real Calculated Scores
        render_verification_panel(ans.verification)

        # AI Answer Glassmorphism Card
        st.markdown("""
        <div style="background: rgba(22, 27, 34, 0.9); border: 1px solid #58a6ff55; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <h2 style="margin: 0 0 1rem 0; color: #58a6ff; font-weight: 700; font-size: 1.4rem; display: flex; align-items: center; gap: 8px;">
                <span>🧠</span> <span>AI Architectural Answer</span>
            </h2>
        """, unsafe_allow_html=True)
        
        st.markdown(ans.markdown_answer)
        st.markdown("</div>", unsafe_allow_html=True)

        # Citations Section
        render_citations(ans.citations)

        st.markdown("<br>", unsafe_allow_html=True)

        # Phase 7: Debug Mode Expander Panel
        if ans.debug_info:
            with st.expander("🛠️ Debug Mode: Real RAG Pipeline Trace & FAISS Scores"):
                dbg = ans.debug_info
                st.markdown(f"**User Query:** `{dbg.user_query}`")
                st.markdown(f"**Expanded Query:** `{dbg.expanded_query}`")
                st.markdown(f"**Embedding Model:** `{dbg.embedding_model}` (Dimension: {dbg.embedding_dim})")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown("**FAISS Raw Vector Search Hits:**")
                    for idx, hit in enumerate(dbg.faiss_raw_hits):
                        st.markdown(f"{idx+1}. **{hit['id']}** ({hit['title']}) — Cosine Score: `{hit['score']}`")

                with col_d2:
                    st.markdown("**CrossEncoder Reranked Hits:**")
                    for idx, hit in enumerate(dbg.reranked_hits):
                        st.markdown(f"{idx+1}. **{hit['id']}** ({hit['title']}) — Rerank Probability: `{hit['score']}`")

                st.markdown("**Exact LLM Prompt Context Sent to Model:**")
                st.code(dbg.llm_prompt_context, language="text")

        # Expandable Retrieved Evidence Cards Section
        st.markdown(f"### 📚 Retrieved Context Evidence ({len(ans.evidences)} Real Chunks)")
        for idx, ev in enumerate(ans.evidences):
            render_evidence_card(ev, idx)
