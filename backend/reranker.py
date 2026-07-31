"""
CrossEncoder Reranker Module
Reranks top 20 hybrid search candidates down to top 5 using CrossEncoder (cross-encoder/ms-marco-MiniLM-L-6-v2).
"""
import logging
from typing import List, Tuple, Dict, Any

logger = logging.getLogger("PatchContext.Reranker")

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
                logger.info(f"Loading CrossEncoder model: {self.model_name}")
                self._model = CrossEncoder(self.model_name)
            except Exception as e:
                logger.warning(f"Could not load CrossEncoder {self.model_name}: {e}. Falling back to heuristic reranker.")
                self._model = "fallback"

    def rerank(self, query: str, candidate_chunks: List[Tuple[Dict[str, Any], float]], top_n: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Reranks candidate chunks and returns top_n items with reranked scores."""
        if not candidate_chunks:
            return []

        self._load_model()

        if self._model != "fallback":
            try:
                pairs = [[query, f"{c[0]['title']} {c[0]['content']}"] for c in candidate_chunks]
                scores = self._model.predict(pairs)
                
                # Normalize scores to [0, 1] range using sigmoid if needed
                import numpy as np
                norm_scores = 1.0 / (1.0 + np.exp(-scores))
                
                reranked = []
                for idx, (chunk, orig_score) in enumerate(candidate_chunks):
                    # Blend 70% CrossEncoder + 30% original hybrid score
                    blended_score = float((0.70 * norm_scores[idx]) + (0.30 * orig_score))
                    reranked.append((chunk, blended_score))

                reranked.sort(key=lambda x: x[1], reverse=True)
                return reranked[:top_n]
            except Exception as e:
                logger.warning(f"CrossEncoder prediction failed: {e}. Returning original ranking.")

        # Fallback heuristic ranking
        candidate_chunks.sort(key=lambda x: x[1], reverse=True)
        return candidate_chunks[:top_n]

# Singleton instance
reranker = CrossEncoderReranker()
