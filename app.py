"""
PatchContext Streamlit Main Entry Point
Modular multi-page router with GitHub Dark Theme and Glassmorphism styling.
"""
import streamlit as st

# Configure page layout and title before any other Streamlit commands
st.set_page_config(
    page_title="PatchContext • Understand FastAPI Evolution",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom CSS styling
from styles.custom_css import inject_custom_css
inject_custom_css()

# Import navigation sidebar component
from components.sidebar import render_sidebar

# Import page modules
from pages.home import render_home_page
from pages.ask_repository import render_ask_repository_page
from pages.retrieved_evidence import render_retrieved_evidence_page
from pages.ai_answer import render_ai_answer_page
from pages.verification import render_verification_page
from pages.timeline_page import render_timeline_page
from pages.pipeline_page import render_pipeline_page
from pages.evaluation import render_evaluation_page
from pages.settings import render_settings_page
from pages.about import render_about_page

# Initialize session state defaults
if "current_query" not in st.session_state:
    st.session_state.current_query = "Why was dependency injection implemented this way?"
if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = None

def main():
    selected_page = render_sidebar()

    # Router logic
    if selected_page == "Home":
        render_home_page()
    elif selected_page == "Ask Repository":
        render_ask_repository_page()
    elif selected_page == "Retrieved Evidence":
        render_retrieved_evidence_page()
    elif selected_page == "AI Answer":
        render_ai_answer_page()
    elif selected_page == "Verification":
        render_verification_page()
    elif selected_page == "Repository Timeline":
        render_timeline_page()
    elif selected_page == "RAG Pipeline":
        render_pipeline_page()
    elif selected_page == "Evaluation Dashboard":
        render_evaluation_page()
    elif selected_page == "Settings":
        render_settings_page()
    elif selected_page == "About":
        render_about_page()

if __name__ == "__main__":
    main()
