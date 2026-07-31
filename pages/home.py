"""
Home Page View
Landing hero banner, feature overview, and repository statistics.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_hero_section
from components.cards import render_repo_stats_cards, render_feature_cards

def render_home_page():
    render_hero_section()

    # Repository Statistics Section
    st.markdown("### 📊 Indexed Repository Footprint")
    st.markdown("<p style='color: #8b949e; font-size: 0.9rem; margin-top: -0.5rem;'>Live statistics from indexed FastAPI repository git graph & embeddings.</p>", unsafe_allow_html=True)
    
    with st.spinner("Fetching repository statistics..."):
        stats = api.get_repo_stats()
        render_repo_stats_cards(stats)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Features Section
    st.markdown("### ✨ Core Architectural Capabilities")
    render_feature_cards()

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Start CTA Box
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 2rem; border: 1px solid #58a6ff55;">
        <h3 style="margin: 0 0 0.5rem 0; color: #58a6ff; font-weight: 700;">Ready to Explore FastAPI's Design Decisions?</h3>
        <p style="color: #8b949e; max-width: 700px; margin: 0 auto 1.25rem auto;">
            Query the vector database over commits, pull requests, and core author reasoning with real-time NLI verification.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Launch Search Interface", use_container_width=True):
            st.session_state.selected_page = "Ask Repository"
            st.rerun()
