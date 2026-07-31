"""
Timeline & Evaluation Data Models
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TimelineEvent:
    id: str
    stage: str  # "Issue Created", "Discussion", "Pull Request", "Code Review", "Merge", "Bug Fix", "Refactor"
    title: str
    description: str
    author: str
    date: str
    reference_id: str
    url: str
    icon: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RAGEvaluationMetrics:
    context_precision: float
    context_recall: float
    faithfulness: float
    answer_relevancy: float
    ragas_score: float
    avg_retrieval_latency_ms: float
    avg_llm_latency_ms: float
    avg_prompt_tokens: int
    avg_completion_tokens: int
    total_cost_usd: float
    historical_benchmark: List[Dict[str, Any]] = field(default_factory=list)
