"""
PatchContext Production FastAPI Backend Server
Exposes high-performance RAG endpoints over FastAPI repository history:
GET /health, POST /index, POST /search, POST /ask, GET /timeline, GET /evaluation
"""
import time
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.dataset import FASTAPI_REPO_DATASET
from backend.vector_db import vector_db
from backend.query_expander import expand_query
from backend.retriever import retriever
from backend.reranker import reranker
from backend.llm import llm_engine
from backend.verifier import verify_answer
from utils.helpers import setup_logger
from utils.config import config

logger = setup_logger("PatchContext.FastAPIBackend")

app = FastAPI(
    title="PatchContext RAG Engine API",
    description="AI-powered Retrieval-Augmented Generation REST Backend explaining FastAPI architectural history.",
    version="1.0.0"
)

def ensure_initialized():
    """Ensures vector DB and BM25 indexes are populated."""
    if vector_db.index is None or vector_db.index.ntotal == 0:
        logger.info("Initializing PatchContext Vector DB & BM25 Retriever...")
        vector_db.build_or_load(FASTAPI_REPO_DATASET)
        retriever.build_bm25(vector_db.chunks)

@app.on_event("startup")
def startup_event():
    ensure_initialized()

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AskRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    model: Optional[str] = "llama-3.3-70b-versatile"

@app.get("/health")
def health_check():
    ensure_initialized()
    return {
        "status": "healthy",
        "service": "PatchContext FastAPI RAG Backend Engine",
        "version": "1.0.0",
        "vector_count": vector_db.index.ntotal if vector_db.index else 0,
        "bm25_count": len(retriever.bm25_corpus),
        "embedding_model": config.EMBEDDING_MODEL
    }

@app.post("/index")
def trigger_reindex():
    logger.info("Triggering full re-indexing of FastAPI dataset...")
    vector_db.build_or_load(FASTAPI_REPO_DATASET)
    retriever.build_bm25(vector_db.chunks)
    return {"status": "success", "indexed_count": len(FASTAPI_REPO_DATASET)}

@app.post("/search")
def search_repository(req: SearchRequest):
    ensure_initialized()
    expanded = expand_query(req.query)
    candidates = retriever.retrieve(expanded, top_k=20)
    reranked = reranker.rerank(req.query, candidates, top_n=req.top_k or 5)
    
    output = []
    for chunk, score in reranked:
        output.append({
            "id": chunk["id"],
            "type": chunk["type"],
            "title": chunk["title"],
            "reference_id": chunk["reference_id"],
            "author": chunk["author"],
            "date": chunk["date"],
            "similarity_score": round(score, 4),
            "confidence_score": round(min(0.99, score * 1.05), 4),
            "summary": chunk["content"][:200] + "...",
            "full_content": chunk["content"],
            "url": chunk["url"],
            "repository": chunk.get("repository", "fastapi/fastapi"),
            "tags": [chunk["type"]],
            "diff_snippet": chunk.get("diff_snippet")
        })
    return output

@app.post("/ask")
def ask_repository(req: AskRequest):
    t_start = time.perf_counter()
    ensure_initialized()
    
    # 1. Query Expansion
    expanded = expand_query(req.query)
    
    # 2. Hybrid Search (Top 20)
    t_ret_start = time.perf_counter()
    candidates = retriever.retrieve(expanded, top_k=20)
    t_ret_ms = (time.perf_counter() - t_ret_start) * 1000.0
    
    # 3. CrossEncoder Rerank (Top 5)
    top_k_val = req.top_k or 5
    reranked = reranker.rerank(req.query, candidates, top_n=top_k_val)

    # Raw FAISS hits for debug tracing
    faiss_raw_hits = [{"id": c[0]["id"], "title": c[0]["title"], "score": round(c[1], 4)} for c in candidates[:5]]
    reranked_hits = [{"id": c[0]["id"], "title": c[0]["title"], "score": round(c[1], 4)} for c in reranked]

    # 4. Similarity Threshold Guard
    top_score = reranked[0][1] if reranked else 0.0
    if not reranked or top_score < config.SIMILARITY_THRESHOLD:
        logger.info(f"Top rerank score {top_score} below threshold {config.SIMILARITY_THRESHOLD}. Returning no evidence.")
        t_tot_ms = (time.perf_counter() - t_start) * 1000.0
        return {
            "query": req.query,
            "markdown_answer": "### No Relevant Evidence Found\n\nNo relevant repository evidence was found for your query in FastAPI's indexed commit history.",
            "evidences": [],
            "verification": {
                "status": "UNVERIFIED",
                "confidence_score": 0.0,
                "nli_score": 0.0,
                "hallucination_guard_passed": False,
                "unsupported_claims_count": 1,
                "verification_notes": f"Relevance score ({top_score:.4f}) below similarity threshold ({config.SIMILARITY_THRESHOLD})."
            },
            "citations": [],
            "retrieval_latency_ms": round(t_ret_ms, 2),
            "llm_latency_ms": 0.0,
            "total_latency_ms": round(t_tot_ms, 2),
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "model_name": req.model,
            "debug_info": {
                "user_query": req.query,
                "expanded_query": expanded,
                "embedding_model": config.EMBEDDING_MODEL,
                "embedding_dim": 768,
                "faiss_raw_hits": faiss_raw_hits,
                "reranked_hits": reranked_hits,
                "llm_prompt_context": "No context built (filtered out by similarity guard)"
            }
        }

    selected_chunks = [c[0] for c in reranked]
    scores_list = [c[1] for c in reranked]

    # 5. LLM Answer Synthesis
    t_llm_start = time.perf_counter()
    answer_md, prompt_toks, comp_toks = llm_engine.generate_answer(req.query, selected_chunks)
    t_llm_ms = (time.perf_counter() - t_llm_start) * 1000.0

    # 6. Verification & Citation Validation
    verif, citations = verify_answer(req.query, answer_md, selected_chunks, scores_list)

    # Format Evidence Items with REAL scores
    evidences_output = []
    for chunk, score in reranked:
        evidences_output.append({
            "id": chunk["id"],
            "type": chunk["type"],
            "title": chunk["title"],
            "reference_id": chunk["reference_id"],
            "author": chunk["author"],
            "date": chunk["date"],
            "similarity_score": round(float(score), 4),
            "confidence_score": round(min(0.99, float(score) * 1.05), 4),
            "summary": chunk["content"][:200] + "...",
            "full_content": chunk["content"],
            "url": chunk["url"],
            "repository": chunk.get("repository", "fastapi/fastapi"),
            "tags": [chunk["type"]],
            "diff_snippet": chunk.get("diff_snippet")
        })

    t_tot_ms = (time.perf_counter() - t_start) * 1000.0

    llm_context_preview = "\n".join([f"[{c['reference_id']}] {c['title']}: {c['content'][:150]}..." for c in selected_chunks])

    return {
        "query": req.query,
        "markdown_answer": answer_md,
        "evidences": evidences_output,
        "verification": verif.__dict__,
        "citations": [c.__dict__ for c in citations],
        "retrieval_latency_ms": round(t_ret_ms, 2),
        "llm_latency_ms": round(t_llm_ms, 2),
        "total_latency_ms": round(t_tot_ms, 2),
        "prompt_tokens": prompt_toks,
        "completion_tokens": comp_toks,
        "model_name": req.model,
        "debug_info": {
            "user_query": req.query,
            "expanded_query": expanded,
            "embedding_model": config.EMBEDDING_MODEL,
            "embedding_dim": 768,
            "faiss_raw_hits": faiss_raw_hits,
            "reranked_hits": reranked_hits,
            "llm_prompt_context": llm_context_preview
        }
    }

@app.get("/timeline")
def get_timeline():
    from services.mock_service import MockService
    return [t.__dict__ for t in MockService().get_timeline()]

@app.get("/evaluation")
def get_evaluation():
    from services.mock_service import MockService
    return MockService().get_evaluation_metrics().__dict__
