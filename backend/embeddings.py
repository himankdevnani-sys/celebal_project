"""
SentenceTransformer Embedding Module
Encodes text chunks using BAAI/bge-large-en-v1.5 or BAAI/bge-base-en-v1.5 / all-MiniLM-L6-v2 with L2 normalization.
"""
import numpy as np
import logging
from typing import List

logger = logging.getLogger("PatchContext.Embeddings")

class EmbeddingEngine:
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(f"Failed to load {self.model_name}: {e}. Falling back to 'all-MiniLM-L6-v2'.")
                from sentence_transformers import SentenceTransformer
                self.model_name = "all-MiniLM-L6-v2"
                self._model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encodes texts into L2-normalized numpy float32 embeddings."""
        self._load_model()
        embeddings = self._model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.astype(np.float32)

# Singleton instance
embedding_engine = EmbeddingEngine()
