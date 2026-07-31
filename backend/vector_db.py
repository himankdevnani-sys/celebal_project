"""
FAISS Vector Store Manager
Indexes document embeddings using FAISS FlatIP/FlatL2, persists index to disk, and reloads automatically.
"""
import faiss
import os
import json
import numpy as np
import logging
from typing import List, Dict, Any, Tuple
from backend.embeddings import embedding_engine

logger = logging.getLogger("PatchContext.VectorDB")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.json")

class FAISSVectorDB:
    def __init__(self):
        self.index = None
        self.chunks: List[Dict[str, Any]] = []

    def build_or_load(self, dataset: List[Dict[str, Any]]):
        """Builds index from dataset or loads from disk if available."""
        os.makedirs(DATA_DIR, exist_ok=True)

        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            try:
                logger.info("Loading existing FAISS index and metadata from disk...")
                self.index = faiss.read_index(FAISS_INDEX_PATH)
                with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                    self.chunks = json.load(f)
                logger.info(f"Loaded {self.index.ntotal} vectors from disk.")
                return
            except Exception as e:
                logger.warning(f"Error loading index from disk ({e}). Rebuilding index...")

        logger.info(f"Building FAISS index over {len(dataset)} chunks...")
        self.chunks = dataset
        texts = [f"{c['title']} {c['content']}" for c in self.chunks]
        embeddings = embedding_engine.encode(texts)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for normalized embeddings (cosine similarity)
        self.index.add(embeddings)

        # Save to disk
        try:
            faiss.write_index(self.index, FAISS_INDEX_PATH)
            with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.chunks, f, indent=2)
            logger.info("FAISS index and metadata successfully persisted to disk.")
        except Exception as e:
            logger.error(f"Failed to persist FAISS index: {e}")

    def search(self, query_vector: np.ndarray, top_k: int = 20) -> List[Tuple[Dict[str, Any], float]]:
        """Performs dense vector search and returns (chunk, similarity_score) pairs."""
        if self.index is None or self.index.ntotal == 0:
            return []

        scores, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(self.chunks):
                results.append((self.chunks[idx], float(score)))

        return results

# Singleton instance
vector_db = FAISSVectorDB()
