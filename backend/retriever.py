"""
Hybrid Retrieval Engine
Combines FAISS dense vector search with rank_bm25 sparse keyword search, fusing candidate scores to retrieve Top 20 chunks.
"""
import logging
from typing import List, Tuple, Dict, Any
from rank_bm25 import BM25Okapi
from backend.embeddings import embedding_engine
from backend.vector_db import vector_db

logger = logging.getLogger("PatchContext.Retriever")

class HybridRetriever:
    def __init__(self):
        self.bm25 = None
        self.bm25_corpus: List[Dict[str, Any]] = []

    def build_bm25(self, chunks: List[Dict[str, Any]]):
        self.bm25_corpus = chunks
        tokenized_corpus = [f"{c['title']} {c['content']}".lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.info(f"Initialized BM25 index over {len(chunks)} chunks.")

    def retrieve(self, query: str, top_k: int = 20) -> List[Tuple[Dict[str, Any], float]]:
        """Executes hybrid BM25 + FAISS vector search and returns top_k fused candidate chunks."""
        if not vector_db.chunks:
            return []

        if self.bm25 is None:
            self.build_bm25(vector_db.chunks)

        # 1. Vector Search
        query_emb = embedding_engine.encode([query])
        vector_results = vector_db.search(query_emb, top_k=top_k)

        # 2. BM25 Search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Max-normalize BM25 scores
        max_bm25 = max(bm25_scores) if len(bm25_scores) > 0 and max(bm25_scores) > 0 else 1.0

        # Fusion dict: chunk_id -> {chunk, vector_score, bm25_score, combined_score}
        fusion: Dict[str, Dict[str, Any]] = {}

        for chunk, score in vector_results:
            cid = chunk["id"]
            fusion[cid] = {
                "chunk": chunk,
                "vector_score": max(0.0, score),
                "bm25_score": 0.0
            }

        for idx, b_score in enumerate(bm25_scores):
            chunk = self.bm25_corpus[idx]
            cid = chunk["id"]
            norm_bm25 = b_score / max_bm25
            if cid in fusion:
                fusion[cid]["bm25_score"] = norm_bm25
            else:
                fusion[cid] = {
                    "chunk": chunk,
                    "vector_score": 0.0,
                    "bm25_score": norm_bm25
                }

        # Hybrid Fusion Formula (60% Dense Vector + 40% BM25)
        combined_results = []
        for cid, data in fusion.items():
            final_score = (0.60 * data["vector_score"]) + (0.40 * data["bm25_score"])
            combined_results.append((data["chunk"], final_score))

        # Sort descending by combined score
        combined_results.sort(key=lambda x: x[1], reverse=True)
        return combined_results[:top_k]

# Singleton instance
retriever = HybridRetriever()
