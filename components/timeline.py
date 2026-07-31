"""
Repository Timeline Component
Renders an interactive, visual chronological timeline of repository events.
"""
import streamlit as st
from typing import List
from models.timeline import TimelineEvent
from utils.helpers import format_date

STAGE_COLORS = {
    "Issue Created": "#d29922",
    "Discussion": "#58a6ff",
    "Pull Request": "#bc8cff",
    "Code Review": "#f778ba",
    "Merge": "#238636",
    "Bug Fix": "#da3633",
    "Release": "#39d353"
}

def render_timeline(events: List[TimelineEvent]):
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <p style="color: #8b949e; font-size: 0.9rem;">
            Chronological progression from original developer issue creation down to code review, merge, and official release tag.
        </p>
    </div>
    """, unsafe_allow_html=True)

    for idx, ev in enumerate(events):
        color = STAGE_COLORS.get(ev.stage, "#58a6ff")
        
        st.markdown(f"""
        <div class="timeline-node">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.1rem;">{ev.icon}</span>
                    <span style="background: {color}22; color: {color}; border: 1px solid {color}55; padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700;">
                        {ev.stage.upper()}
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; color: #58a6ff; font-weight: 600; font-size: 0.88rem;">
                        {ev.reference_id}
                    </span>
                </div>
                <span style="color: #8b949e; font-size: 0.8rem;">
                    📅 {format_date(ev.date)} • 👤 <strong>{ev.author}</strong>
                </span>
            </div>
            <h4 style="margin: 0.2rem 0; color: #f0f6fc; font-size: 1rem;">{ev.title}</h4>
            <p style="margin: 0; color: #8b949e; font-size: 0.86rem; line-height: 1.5;">{ev.description}</p>
            <div style="margin-top: 0.4rem; font-size: 0.78rem;">
                <a href="{ev.url}" target="_blank" style="color: #58a6ff; text-decoration: none;">🔗 Open GitHub Event Link</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
