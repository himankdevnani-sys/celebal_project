"""
PatchContext Configuration Module
Reads configuration settings from environment variables with safe fallbacks.
Defaults USE_MOCK to False to ensure real vector search and RAG execution.
"""
import os
import logging
from dataclasses import dataclass
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger("PatchContext.Config")

def str_to_bool(val: str, default: bool = False) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in ("true", "1", "yes", "on", "t")

@dataclass
class Config:
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    USE_MOCK: bool = str_to_bool(os.getenv("USE_MOCK", "False"), False)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.20"))
    MMR_LAMBDA: float = float(os.getenv("MMR_LAMBDA", "0.70"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "700"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    RETRIEVER_TYPE: str = os.getenv("RETRIEVER_TYPE", "Hybrid BM25 + FAISS + CrossEncoder")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "BACKEND_URL": self.BACKEND_URL,
            "USE_MOCK": self.USE_MOCK,
            "MODEL_NAME": self.MODEL_NAME,
            "EMBEDDING_MODEL": self.EMBEDDING_MODEL,
            "TOP_K": self.TOP_K,
            "SIMILARITY_THRESHOLD": self.SIMILARITY_THRESHOLD,
            "MMR_LAMBDA": self.MMR_LAMBDA,
            "TEMPERATURE": self.TEMPERATURE,
            "CHUNK_SIZE": self.CHUNK_SIZE,
            "CHUNK_OVERLAP": self.CHUNK_OVERLAP,
            "RETRIEVER_TYPE": self.RETRIEVER_TYPE,
        }

config = Config()
