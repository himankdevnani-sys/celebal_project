"""
PatchContext Custom CSS Stylesheet
GitHub Dark Mode, Glassmorphism Cards, Typography, and Sleek Animations
"""
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Dark Theme Overrides */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }

    /* Custom Glassmorphic Card */
    .glass-card {
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        border-color: #58a6ff55;
        box-shadow: 0 12px 40px 0 rgba(88, 166, 255, 0.1);
        transform: translateY(-2px);
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(13, 17, 23, 0.95) 0%, rgba(22, 27, 34, 0.95) 50%, rgba(33, 38, 45, 0.95) 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(88, 166, 255, 0.08) 0%, transparent 60%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 50%, #39d353 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #8b949e;
        font-weight: 400;
        max-width: 800px;
        line-height: 1.6;
    }

    /* Stat Cards */
    .stat-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .stat-card:hover {
        border-color: #58a6ff;
    }
    .stat-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        font-family: 'JetBrains Mono', monospace;
    }
    .stat-lbl {
        font-size: 0.85rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
        font-weight: 600;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-commit {
        background-color: rgba(57, 211, 83, 0.15);
        color: #39d353;
        border: 1px solid rgba(57, 211, 83, 0.3);
    }
    .badge-pr {
        background-color: rgba(188, 140, 255, 0.15);
        color: #bc8cff;
        border: 1px solid rgba(188, 140, 255, 0.3);
    }
    .badge-issue {
        background-color: rgba(210, 153, 34, 0.15);
        color: #d29922;
        border: 1px solid rgba(210, 153, 34, 0.3);
    }
    .badge-verified {
        background-color: rgba(46, 160, 67, 0.2);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.5);
    }
    .badge-tech {
        background-color: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }

    /* Code Block styling */
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #161b22 !important;
        border-radius: 6px;
    }

    /* Timeline styling */
    .timeline-node {
        position: relative;
        padding-left: 2rem;
        border-left: 2px solid #30363d;
        margin-bottom: 1.5rem;
    }
    .timeline-node::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #58a6ff;
        border: 2px solid #0d1117;
    }

    /* Streamlit Sidebar custom styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
    }
    
    /* Streamlit Buttons styling */
    div.stButton > button {
        background-color: #238636;
        color: #ffffff;
        font-weight: 600;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #2ea043;
        border-color: #3fb950;
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #8b949e;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d !important;
        color: #58a6ff !important;
    }
    </style>
    """, unsafe_allow_html=True)
