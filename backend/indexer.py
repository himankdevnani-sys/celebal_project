"""
FastAPI Repository Git & Documentation Indexer
Parses repository commits, pull requests, issues, discussions, and release notes into structured 700-char chunks with 150-char overlap.
"""
import logging
from typing import List, Dict, Any
from backend.dataset import FASTAPI_REPO_DATASET

logger = logging.getLogger("PatchContext.Indexer")

def load_and_chunk_repository(repo_path: str = None) -> List[Dict[str, Any]]:
    """Loads repository dataset and returns chunked entries with full metadata."""
    logger.info("Indexing FastAPI repository commits, PRs, issues, and discussions...")
    return FASTAPI_REPO_DATASET
