"""
Evaluation Dashboard Page
Displays RAGAs metrics, token costs, latency breakdowns, and historical benchmark charts using Plotly.
Communicates strictly via services/api.py.
"""
import streamlit as st
from services.api import api
from components.header import render_page_header
from components.charts import (
    render_ragas_radar_chart,
    render_latency_breakdown_chart,
    render_benchmark_history_chart
)
from utils.helpers import estimate_llm_cost

def render_evaluation_page():
    render_page_header(
        title="Evaluation Dashboard",
        subtitle="Comprehensive RAGAs metrics, latency profiling, token tracking, and system benchmark comparisons.",
        icon="📊"
    )

    metrics = api.get_evaluation_metrics()

    # RAGAs Score Metric Cards
    cols = st.columns(5)
    score_items = [
        ("Context Precision", f"{metrics.context_precision*100:.1f}%", "#58a6ff"),
        ("Context Recall", f"{metrics.context_recall*100:.1f}%", "#d29922"),
        ("Faithfulness", f"{metrics.faithfulness*100:.1f}%", "#39d353"),
        ("Answer Relevancy", f"{metrics.answer_relevancy*100:.1f}%", "#bc8cff"),
        ("RAGAs Overall Score", f"{metrics.ragas_score*100:.1f}%", "#f778ba")
    ]

    for idx, (label, val, color) in enumerate(score_items):
        with cols[idx]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color: {color}; font-size: 1.8rem;">{val}</div>
                <div class="stat-lbl" style="font-size: 0.75rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Plotly Charts Section
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 🎯 RAGAs Performance Profile (Radar)")
        fig_radar = render_ragas_radar_chart(metrics)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_chart2:
        st.markdown("#### ⏱️ Latency Breakdown (ms)")
        fig_latency = render_latency_breakdown_chart(metrics)
        st.plotly_chart(fig_latency, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Token & Cost Metrics Panel
    st.markdown("### 💰 Token Usage & Cost Efficiency Metrics")
    
    tcol1, tcol2, tcol3, tcol4 = st.columns(4)
    with tcol1:
        st.metric("Avg Prompt Tokens", f"{metrics.avg_prompt_tokens:,}")
    with tcol2:
        st.metric("Avg Completion Tokens", f"{metrics.avg_completion_tokens:,}")
    with tcol3:
        st.metric("Total Tokens / Query", f"{metrics.avg_prompt_tokens + metrics.avg_completion_tokens:,}")
    with tcol4:
        st.metric("Est Cost / Query", f"${metrics.total_cost_usd:.5f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Historical Benchmark Comparison Bar Chart
    st.markdown("### 📈 Version Benchmark Progression (Naive vs MMR vs PatchContext NLI)")
    fig_bench = render_benchmark_history_chart(metrics.historical_benchmark)
    st.plotly_chart(fig_bench, use_container_width=True)
