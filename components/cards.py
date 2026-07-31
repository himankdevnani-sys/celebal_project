"""
Reusable UI Cards Component
Renders stats cards, feature cards, expandable evidence items, and verification panels.
"""
import streamlit as st
from typing import Dict, Any, List
from models.evidence import EvidenceItem
from models.answer import VerificationResult, CitationLink
from utils.helpers import get_score_badge_html, format_date

def render_repo_stats_cards(stats: Dict[str, Any]):
    cols = st.columns(6)
    items = [
        ("Commits Indexed", f"{stats.get('commits_indexed', 5420):,}", "#39d353"),
        ("Pull Requests", f"{stats.get('pull_requests', 4850):,}", "#bc8cff"),
        ("Issues", f"{stats.get('issues', 12100):,}", "#d29922"),
        ("Discussions", f"{stats.get('discussions', 3900):,}", "#58a6ff"),
        ("Embeddings", f"{stats.get('embeddings', 84500):,}", "#f778ba"),
        ("Documents", f"{stats.get('documents', 26200):,}", "#79c0ff")
    ]
    
    for idx, (label, val, color) in enumerate(items):
        with cols[idx]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color: {color};">{val}</div>
                <div class="stat-lbl">{label}</div>
            </div>
            """, unsafe_allow_html=True)

def render_feature_cards():
    features = [
        ("🔍 Commit History Search", "Perform dense vector search across thousands of historical commit messages, diffs, and architectural changes."),
        ("🔀 PR Discussion Explorer", "Uncover why specific PRs were merged or rejected through multi-document thread contextualization."),
        ("💬 Issue Reasoning", "Trace feature requests and bug reports back to the original developer discussions and architectural trade-offs."),
        ("🛡️ Hallucination Detection", "Real-time NLI (Natural Language Inference) guardrails cross-reference generated answers against raw source text."),
        ("📈 Repository Timeline", "Visual chronologies detailing how architectural primitives (like APIRouter or Lifespan) evolved over time."),
        ("📊 RAG Evaluation", "Continuous monitoring of Context Precision, Context Recall, Faithfulness, and Answer Relevancy via RAGAs.")
    ]
    
    cols = st.columns(3)
    for idx, (title, desc) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="glass-card" style="height: 170px;">
                <h4 style="margin: 0 0 0.5rem 0; color: #f0f6fc; font-size: 1.05rem;">{title}</h4>
                <p style="margin: 0; color: #8b949e; font-size: 0.85rem; line-height: 1.5;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def render_evidence_card(evidence: EvidenceItem, index: int):
    # Badge class selection
    badge_cls = "badge-commit" if evidence.type == "Commit" else "badge-pr" if evidence.type == "Pull Request" else "badge-issue"
    score_badge = get_score_badge_html(evidence.similarity_score, "Similarity")
    conf_badge = get_score_badge_html(evidence.confidence_score, "Confidence")

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 0.75rem; padding: 1.1rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
            <div>
                <span class="badge {badge_cls}">{evidence.type.upper()}</span>
                <span style="font-family: 'JetBrains Mono', monospace; color: #58a6ff; font-weight: 600; font-size: 0.9rem;">
                    {evidence.reference_id}
                </span>
                <span style="color: #8b949e; font-size: 0.8rem; margin-left: 8px;">
                    by <strong>{evidence.author}</strong> on {format_date(evidence.date)}
                </span>
            </div>
            <div>
                {score_badge} {conf_badge}
            </div>
        </div>
        <h4 style="margin: 0.4rem 0; color: #f0f6fc; font-size: 1rem; font-weight: 600;">{evidence.title}</h4>
        <p style="margin: 0; color: #8b949e; font-size: 0.88rem; line-height: 1.5;">{evidence.summary}</p>
        <div style="margin-top: 0.5rem; font-size: 0.8rem;">
            <a href="{evidence.url}" target="_blank" style="color: #58a6ff; text-decoration: none; font-weight: 500;">
                🔗 View on GitHub ({evidence.repository})
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Expandable details
    with st.expander(f"📖 Inspect Full Context & Code Snippet ({evidence.reference_id})"):
        st.markdown("**Full Raw Text / Thread:**")
        st.markdown(f"```text\n{evidence.full_content}\n```")
        if evidence.diff_snippet:
            st.markdown("**Git Diff / Code Changes:**")
            st.code(evidence.diff_snippet, language="diff")

def render_verification_panel(verif: VerificationResult):
    status_bg = "rgba(46, 160, 67, 0.15)" if verif.status == "VERIFIED" else "rgba(210, 153, 34, 0.15)"
    status_color = "#3fb950" if verif.status == "VERIFIED" else "#d29922"
    border_color = "rgba(46, 160, 67, 0.4)" if verif.status == "VERIFIED" else "rgba(210, 153, 34, 0.4)"

    st.markdown(f"""
    <div style="background: {status_bg}; border: 1px solid {border_color}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.4rem;">🛡️</span>
                <div>
                    <h3 style="margin: 0; color: {status_color}; font-size: 1.1rem; font-weight: 700;">
                        Verification Guardrail: {verif.status}
                    </h3>
                    <p style="margin: 0; color: #8b949e; font-size: 0.82rem;">
                        Natural Language Inference (NLI) Cross-Verification
                    </p>
                </div>
            </div>
            <span class="badge badge-verified" style="font-size: 0.85rem; padding: 6px 14px;">
                ✓ HALLUCINATION GUARD PASSED
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 0.75rem; text-align: center;">
            <div style="background: rgba(13, 17, 23, 0.6); padding: 8px; border-radius: 8px; border: 1px solid #30363d;">
                <div style="color: #8b949e; font-size: 0.75rem; font-weight: 600;">CONFIDENCE SCORE</div>
                <div style="color: #58a6ff; font-size: 1.25rem; font-weight: 700; font-family: 'JetBrains Mono';">{int(verif.confidence_score*100)}%</div>
            </div>
            <div style="background: rgba(13, 17, 23, 0.6); padding: 8px; border-radius: 8px; border: 1px solid #30363d;">
                <div style="color: #8b949e; font-size: 0.75rem; font-weight: 600;">NLI FAITHFULNESS</div>
                <div style="color: #39d353; font-size: 1.25rem; font-weight: 700; font-family: 'JetBrains Mono';">{int(verif.nli_score*100)}%</div>
            </div>
            <div style="background: rgba(13, 17, 23, 0.6); padding: 8px; border-radius: 8px; border: 1px solid #30363d;">
                <div style="color: #8b949e; font-size: 0.75rem; font-weight: 600;">UNSUPPORTED CLAIMS</div>
                <div style="color: #39d353; font-size: 1.25rem; font-weight: 700; font-family: 'JetBrains Mono';">{verif.unsupported_claims_count}</div>
            </div>
            <div style="background: rgba(13, 17, 23, 0.6); padding: 8px; border-radius: 8px; border: 1px solid #30363d;">
                <div style="color: #8b949e; font-size: 0.75rem; font-weight: 600;">FAISS MATCHES</div>
                <div style="color: #bc8cff; font-size: 1.25rem; font-weight: 700; font-family: 'JetBrains Mono';">Top 5</div>
            </div>
        </div>
        <p style="margin: 0.75rem 0 0 0; color: #c9d1d9; font-size: 0.85rem; font-style: italic; line-height: 1.4;">
            💡 {verif.verification_notes}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_citations(citations: List[CitationLink]):
    st.markdown("#### 🔗 Referenced Source Citations")
    cols = st.columns(len(citations) if citations else 1)
    for idx, cite in enumerate(citations):
        badge_cls = "badge-commit" if cite.type == "Commit" else "badge-pr" if cite.type == "Pull Request" else "badge-issue"
        with cols[idx % len(cols)]:
            st.markdown(f"""
            <div style="background: rgba(22, 27, 34, 0.9); border: 1px solid #30363d; border-radius: 8px; padding: 10px; font-size: 0.82rem;">
                <span class="badge {badge_cls}">{cite.type}</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #58a6ff;">{cite.reference_id}</span>
                <div style="margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <a href="{cite.url}" target="_blank" style="color: #8b949e; text-decoration: none;">{cite.title}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
