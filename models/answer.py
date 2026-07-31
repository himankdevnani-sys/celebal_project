"""
RAG Answer & Verification Data Models
Includes debug tracing metadata for full transparency.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from models.evidence import EvidenceItem

@dataclass
class VerificationResult:
    status: str  # "VERIFIED", "PARTIALLY_VERIFIED", "UNVERIFIED"
    confidence_score: float
    nli_score: float
    hallucination_guard_passed: bool
    unsupported_claims_count: int
    verification_notes: str

@dataclass
class CitationLink:
    title: str
    type: str
    reference_id: str
    url: str

@dataclass
class DebugInfo:
    user_query: str
    expanded_query: str
    embedding_model: str
    embedding_dim: int
    faiss_raw_hits: List[Dict[str, Any]] = field(default_factory=list)
    reranked_hits: List[Dict[str, Any]] = field(default_factory=list)
    llm_prompt_context: str = ""

@dataclass
class RAGAnswer:
    query: str
    markdown_answer: str
    evidences: List[EvidenceItem]
    verification: VerificationResult
    citations: List[CitationLink]
    retrieval_latency_ms: float
    llm_latency_ms: float
    total_latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    model_name: str
    debug_info: Optional[DebugInfo] = None
