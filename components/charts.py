"""
Plotly Dashboard Charts Component
Generates Plotly visualizations styled for GitHub dark theme.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from models.timeline import RAGEvaluationMetrics

# Dark theme palette
DARK_BG = "#0d1117"
CARD_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#c9d1d9"
ACCENT_BLUE = "#58a6ff"
ACCENT_GREEN = "#39d353"
ACCENT_PURPLE = "#bc8cff"
ACCENT_AMBER = "#d29922"

def render_ragas_radar_chart(metrics: RAGEvaluationMetrics):
    categories = ['Context Precision', 'Context Recall', 'Faithfulness', 'Answer Relevancy', 'RAGAs Overall']
    values = [
        metrics.context_precision,
        metrics.context_recall,
        metrics.faithfulness,
        metrics.answer_relevancy,
        metrics.ragas_score
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='PatchContext RAG',
        fillcolor='rgba(88, 166, 255, 0.25)',
        line=dict(color=ACCENT_BLUE, width=2)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.0], gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR)),
            angularaxis=dict(gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR, size=11)),
            bgcolor=CARD_BG
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        font=dict(color=TEXT_COLOR, family="Inter"),
        showlegend=False
    )
    return fig

def render_latency_breakdown_chart(metrics: RAGEvaluationMetrics):
    fig = go.Figure(data=[
        go.Bar(name='Retrieval (FAISS MMR)', x=['Latency (ms)'], y=[metrics.avg_retrieval_latency_ms], marker_color=ACCENT_GREEN),
        go.Bar(name='LLM Synthesis (Llama 3.3)', x=['Latency (ms)'], y=[metrics.avg_llm_latency_ms], marker_color=ACCENT_PURPLE)
    ])
    fig.update_layout(
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=CARD_BG,
        xaxis=dict(gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR), title="Time in Milliseconds"),
        legend=dict(font=dict(color=TEXT_COLOR), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=30),
        font=dict(color=TEXT_COLOR, family="Inter")
    )
    return fig

def render_benchmark_history_chart(history_list):
    df = pd.DataFrame(history_list)
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=df['version'], y=df['precision'], name='Precision', marker_color=ACCENT_BLUE))
    fig.add_trace(go.Bar(x=df['version'], y=df['recall'], name='Recall', marker_color=ACCENT_AMBER))
    fig.add_trace(go.Bar(x=df['version'], y=df['faithfulness'], name='Faithfulness', marker_color=ACCENT_GREEN))
    fig.add_trace(go.Bar(x=df['version'], y=df['ragas'], name='RAGAs Total', marker_color=ACCENT_PURPLE))

    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=CARD_BG,
        xaxis=dict(gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(gridcolor=BORDER_COLOR, tickfont=dict(color=TEXT_COLOR), range=[0, 1.0]),
        legend=dict(font=dict(color=TEXT_COLOR), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=30),
        font=dict(color=TEXT_COLOR, family="Inter")
    )
    return fig
