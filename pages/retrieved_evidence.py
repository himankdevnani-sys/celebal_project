"""
Retrieved Evidence Explorer Page
Deep dive into vector search evidence items, similarity scores, git diffs, and GitHub references.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_page_header
from components.cards import render_evidence_card

def render_retrieved_evidence_page():
    render_page_header(
        title="Retrieved Evidence",
        subtitle="Explore raw commits, pull request discussions, and issue history retrieved by MMR vector search.",
        icon="📚"
    )

    query = st.session_state.get("current_query", "Why was APIRouter introduced?")

    st.markdown(f"""
    <div style="background: rgba(22, 27, 34, 0.8); border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; margin-bottom: 1.5rem;">
        <span style="color: #8b949e; font-size: 0.85rem;">Active Query Context:</span>
        <strong style="color: #58a6ff; margin-left: 6px;">"{query}"</strong>
    </div>
    """, unsafe_allow_html=True)

    # Filter Controls
    col1, col2 = st.columns([2, 2])
    with col1:
        type_filter = st.multiselect(
            "Filter Evidence Type:",
            options=["Commit", "Pull Request", "Issue", "Discussion"],
            default=["Commit", "Pull Request", "Issue"]
        )
    with col2:
        sort_order = st.selectbox(
            "Sort By:",
            options=["Similarity Score (High to Low)", "Date (Newest First)", "Confidence Score"]
        )

    # Fetch Evidence via APIService
    evidences = api.get_evidence(query)

    # Filter
    if type_filter:
        evidences = [e for e in evidences if e.type in type_filter]

    # Sort
    if "Similarity" in sort_order:
        evidences.sort(key=lambda x: x.similarity_score, reverse=True)
    elif "Date" in sort_order:
        evidences.sort(key=lambda x: x.date, reverse=True)
    elif "Confidence" in sort_order:
        evidences.sort(key=lambda x: x.confidence_score, reverse=True)

    st.markdown(f"#### Showing {len(evidences)} Evidence Documents")

    if not evidences:
        st.info("No evidence documents match your selected filters. Try broadening the filter selection.")
        return

    for idx, ev in enumerate(evidences):
        render_evidence_card(ev, idx)
