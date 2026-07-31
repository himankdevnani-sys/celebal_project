"""
PatchContext Helper Utilities
Provides logging, formatting, score-to-color mapping, and UI utility functions.
"""
import logging
import datetime
from typing import Any, Dict

# Configure centralized logger
def setup_logger(name: str = "PatchContext") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

def format_date(date_str: str) -> str:
    """Formats an ISO date string to a human-readable format."""
    try:
        dt = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str

def get_similarity_color(score: float) -> str:
    """Returns a CSS color code based on similarity score."""
    if score >= 0.85:
        return "#3fb950"  # GitHub green
    elif score >= 0.70:
        return "#58a6ff"  # GitHub blue
    elif score >= 0.50:
        return "#d29922"  # GitHub yellow/amber
    else:
        return "#f85149"  # GitHub red

def get_score_badge_html(score: float, label: str = "Match") -> str:
    """Generates an HTML badge for similarity scores."""
    color = get_similarity_color(score)
    pct = int(score * 100)
    return f'<span style="background-color: {color}22; color: {color}; border: 1px solid {color}55; padding: 2px 8px; border-radius: 12px; font-size: 0.78rem; font-weight: 600;">{label}: {pct}%</span>'

def estimate_llm_cost(prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
    """Estimates LLM query cost based on token counts."""
    # Pricing per 1M tokens (e.g. GPT-4o-mini / Groq Llama 3.3 70b)
    input_rate = 0.15 / 1_000_000
    output_rate = 0.60 / 1_000_000
    return (prompt_tokens * input_rate) + (completion_tokens * output_rate)
