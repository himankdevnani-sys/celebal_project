"""
Query Understanding & Expansion Module
Expands domain concepts (async, APIRouter, Pydantic v2, lifespan, dependency injection, BackgroundTasks, Starlette, OpenAPI)
to maximize BM25 and vector retrieval precision.
"""
from typing import List

EXPANSION_DICTIONARY = {
    "async": ["async", "await", "ASGI", "Starlette", "concurrency", "performance", "event loop", "threadpool", "run_in_threadpool", "sync def"],
    "apirouter": ["APIRouter", "router", "include_router", "prefix", "tags", "modular", "routing", "sub-application", "Blueprint"],
    "pydantic": ["Pydantic v2", "pydantic-core", "Rust", "BaseModel", "migration", "validation", "performance", "speedup", "schema"],
    "lifespan": ["lifespan", "asynccontextmanager", "startup", "shutdown", "on_event", "context manager", "yield", "Starlette"],
    "dependency": ["dependency injection", "Depends", "yield dependency", "request scope", "teardown", "contextmanager", "SolveDependencies"],
    "backgroundtasks": ["BackgroundTasks", "BackgroundTask", "post-response", "celery", "async task", "non-blocking", "Starlette"],
    "starlette": ["Starlette", "ASGI", "toolkit", "requests", "responses", "routing", "middleware", "WebSocket"],
    "openapi": ["OpenAPI", "Swagger", "ReDoc", "schema", "JSON Schema", "OAuth2", "security", "documentation", "spec"]
}

def expand_query(query: str) -> str:
    """Returns an expanded query string enriched with domain synonyms."""
    query_lower = query.lower()
    terms = [query]
    
    for key, synonyms in EXPANSION_DICTIONARY.items():
        if key in query_lower:
            terms.extend(synonyms[:4])  # add top synonyms
            
    return " ".join(dict.fromkeys(terms))  # deduplicate preserving order
