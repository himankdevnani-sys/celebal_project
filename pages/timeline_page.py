"""
Repository History Timeline Page
Chronological visual timeline of FastAPI architectural evolution.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_page_header
from components.timeline import render_timeline

def render_timeline_page():
    render_page_header(
        title="Repository Timeline",
        subtitle="Chronological audit trail of FastAPI design decisions from issue proposal to pull request, merge, and release.",
        icon="📈"
    )

    with st.spinner("Loading repository timeline..."):
        events = api.get_timeline()

    # Timeline stats bar
    cols = st.columns(4)
    with cols[0]:
        st.metric("Timeline Milestone Events", f"{len(events)}")
    with cols[1]:
        st.metric("Primary Author", "tiangolo")
    with cols[2]:
        st.metric("Repository Target", "fastapi/fastapi")
    with cols[3]:
        st.metric("Timeframe", "2019 - Present")

    st.markdown("<br>", unsafe_allow_html=True)

    render_timeline(events)
