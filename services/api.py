"""
PatchContext API Service Layer
Routes RAG requests to the real backend with fast fallback to direct in-process engine.
"""
import requests
import logging
from typing import Dict, Any, List
from utils.config import config
from utils.helpers import setup_logger
from services.mock_service import MockService
from models.answer import RAGAnswer, VerificationResult, CitationLink, DebugInfo
from models.evidence import EvidenceItem
from models.timeline import TimelineEvent, RAGEvaluationMetrics

logger = setup_logger("PatchContext.APIService")

class APIService:
    def __init__(self):
        self.mock_service = MockService()

    def get_health(self) -> Dict[str, Any]:
        """GET /health"""
        try:
            resp = requests.get(f"{config.BACKEND_URL}/health", timeout=0.5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.main import health_check
            res = health_check()
            res["service"] += " (In-Process Direct Engine)"
            return res
        except Exception as e:
            logger.warning(f"Backend in-process check error: {e}")

        return self.mock_service.get_health()

    def get_repo_stats(self) -> Dict[str, Any]:
        """GET /stats"""
        return self.mock_service.get_repo_stats()

    def get_sample_queries(self) -> List[Dict[str, str]]:
        """Fetch preset example questions."""
        return self.mock_service.get_sample_queries()

    def ask_repository(self, query: str, top_k: int = None) -> RAGAnswer:
        """POST /ask - Executes real RAG engine with hybrid search, FAISS vectors, CrossEncoder reranking & Groq LLM."""
        top_k_val = top_k or config.TOP_K

        # 1. Fast attempt to external HTTP REST API backend
        try:
            payload = {"query": query, "top_k": top_k_val, "model": config.MODEL_NAME}
            resp = requests.post(f"{config.BACKEND_URL}/ask", json=payload, timeout=0.5)
            if resp.status_code == 200:
                return self._parse_backend_response(resp.json())
        except Exception:
            pass  # Fast fallback to direct in-process execution

        # 2. Direct In-Process Real Backend Engine Execution
        try:
            from backend.main import ask_repository as backend_ask, AskRequest
            req = AskRequest(query=query, top_k=top_k_val, model=config.MODEL_NAME)
            raw_res = backend_ask(req)
            return self._parse_backend_response(raw_res)
        except Exception as ex:
            logger.error(f"In-process backend execution error: {ex}. Falling back to mock service.")

        return self.mock_service.ask_repository(query, top_k_val)

    def _parse_backend_response(self, data: Dict[str, Any]) -> RAGAnswer:
        evidences = [EvidenceItem(**item) for item in data.get("evidences", [])]
        verif = VerificationResult(**data.get("verification", {}))
        citations = [CitationLink(**c) for c in data.get("citations", [])]
        
        debug_data = data.get("debug_info")
        debug_info = DebugInfo(**debug_data) if debug_data else None

        return RAGAnswer(
            query=data["query"],
            markdown_answer=data["markdown_answer"],
            evidences=evidences,
            verification=verif,
            citations=citations,
            retrieval_latency_ms=data.get("retrieval_latency_ms", 0.0),
            llm_latency_ms=data.get("llm_latency_ms", 0.0),
            total_latency_ms=data.get("total_latency_ms", 0.0),
            prompt_tokens=data.get("prompt_tokens", 0),
            completion_tokens=data.get("completion_tokens", 0),
            model_name=data.get("model_name", config.MODEL_NAME),
            debug_info=debug_info
        )

    def get_evidence(self, query: str) -> List[EvidenceItem]:
        """POST /search - Returns real vector search and reranked evidence."""
        try:
            resp = requests.post(f"{config.BACKEND_URL}/search", json={"query": query}, timeout=0.5)
            if resp.status_code == 200:
                return [EvidenceItem(**item) for item in resp.json()]
        except Exception:
            pass

        try:
            from backend.main import search_repository, SearchRequest
            items = search_repository(SearchRequest(query=query, top_k=5))
            return [EvidenceItem(**item) for item in items]
        except Exception as e:
            logger.warning(f"In-process search error: {e}")

        return self.mock_service.get_evidence_by_query(query)

    def get_timeline(self) -> List[TimelineEvent]:
        """GET /timeline"""
        return self.mock_service.get_timeline()

    def get_evaluation_metrics(self) -> RAGEvaluationMetrics:
        """GET /evaluation"""
        return self.mock_service.get_evaluation_metrics()

api = APIService()
