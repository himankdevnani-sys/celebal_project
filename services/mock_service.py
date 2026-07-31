"""
Mock Service Provider for PatchContext
Delivers realistic, production-quality mock data for FastAPI repository history, RAG answers, evidence, timeline, and evaluations.
Covers all core FastAPI architectural topics (async, APIRouter, Pydantic v2, lifespan, dependency injection, BackgroundTasks, Starlette, OpenAPI).
"""
import time
from typing import List, Dict, Any
from models.evidence import EvidenceItem
from models.answer import RAGAnswer, VerificationResult, CitationLink
from models.timeline import TimelineEvent, RAGEvaluationMetrics

class MockService:
    def __init__(self):
        pass

    def get_health(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "service": "PatchContext RAG Engine",
            "version": "1.0.0",
            "vector_db": "FAISS (84,500 vectors loaded)",
            "llm": "llama-3.3-70b-versatile (Groq)",
            "uptime_seconds": 14290
        }

    def get_repo_stats(self) -> Dict[str, Any]:
        return {
            "commits_indexed": 5420,
            "pull_requests": 4850,
            "issues": 12100,
            "discussions": 3900,
            "embeddings": 84500,
            "documents": 26200,
            "repository": "fastapi/fastapi",
            "last_updated": "2026-07-28T18:30:00Z"
        }

    def get_sample_queries(self) -> List[Dict[str, str]]:
        return [
            {"id": "q1", "question": "Why does FastAPI support async endpoints?", "tag": "Concurrency", "summary": "Threadpool execution for sync def vs non-blocking async def"},
            {"id": "q2", "question": "Why was APIRouter introduced?", "tag": "Architecture", "summary": "Modular router breakdown for scaling large FastAPI codebases"},
            {"id": "q3", "question": "Why did FastAPI migrate to Pydantic v2?", "tag": "Performance", "summary": "5x-20x speedup with pydantic-core Rust engine"},
            {"id": "q4", "question": "Explain the lifespan protocol.", "tag": "Deprecation", "summary": "Replacing on_event startup/shutdown with ASGI Lifespan context managers"},
            {"id": "q5", "question": "How did dependency injection evolve?", "tag": "Core Design", "summary": "Yield context managers and request-scoped dependency caching"},
            {"id": "q6", "question": "Why was BackgroundTasks added?", "tag": "Async Tasks", "summary": "Post-response lightweight task execution without external brokers"},
            {"id": "q7", "question": "Why does FastAPI use Starlette?", "tag": "Foundation", "summary": "ASGI web framework foundation for high-performance routing"},
            {"id": "q8", "question": "How did OpenAPI support evolve?", "tag": "Documentation", "summary": "Automatic Swagger/ReDoc schema generation from Pydantic models"}
        ]

    def get_evidence_by_query(self, query: str) -> List[EvidenceItem]:
        q = query.lower()

        # 1. Async
        if "async" in q:
            return [
                EvidenceItem(
                    id="ev-async-1",
                    type="Pull Request",
                    title="PR #294: Support both sync 'def' and 'async def' path operation functions",
                    reference_id="#294",
                    author="tiangolo",
                    date="2019-05-01T15:20:00Z",
                    similarity_score=0.96,
                    confidence_score=0.98,
                    summary="FastAPI handles async def directly on the main non-blocking event loop and runs sync def in worker threadpools.",
                    full_content="PR #294: Synchronous def endpoints are run via anyio/Starlette run_in_threadpool worker threads so blocking IO operations do not freeze the main event loop.",
                    url="https://github.com/fastapi/fastapi/pull/294",
                    tags=["Async", "Threadpool", "Concurrency"],
                    diff_snippet="+ raw_response = await run_in_threadpool(dependant.call, **values)"
                ),
                EvidenceItem(
                    id="ev-async-2",
                    type="Commit",
                    title="Commit 3fa8b12: Optimize Starlette anyio threadpool worker dispatch",
                    reference_id="3fa8b12",
                    author="tiangolo",
                    date="2019-05-04T10:14:00Z",
                    similarity_score=0.91,
                    confidence_score=0.93,
                    summary="Refactored threadpool worker dispatch to prevent event loop thread contention.",
                    full_content="Commit 3fa8b12: Prevents blocking IO operations inside def endpoints from locking up main event loop.",
                    url="https://github.com/fastapi/fastapi/commit/3fa8b12",
                    tags=["Performance", "Async"]
                )
            ]

        # 2. APIRouter
        elif "apirouter" in q or "router" in q:
            return [
                EvidenceItem(
                    id="ev-router-1",
                    type="Pull Request",
                    title="PR #142: Add APIRouter for modular application structuring",
                    reference_id="#142",
                    author="tiangolo",
                    date="2019-04-12T14:22:00Z",
                    similarity_score=0.95,
                    confidence_score=0.97,
                    summary="Introduces APIRouter to split single-file FastAPI applications into clean modular components with shared prefixes and tags.",
                    full_content="PR #142: Solves giant single-file codebases by introducing APIRouter class mounted via app.include_router(router).",
                    url="https://github.com/fastapi/fastapi/pull/142",
                    tags=["APIRouter", "Modularity"],
                    diff_snippet="+ class APIRouter(routing.Router):"
                ),
                EvidenceItem(
                    id="ev-router-2",
                    type="Issue",
                    title="Issue #128: Proposal for Modular Sub-Routing (Flask Blueprint Parity)",
                    reference_id="#128",
                    author="euri10",
                    date="2019-04-05T09:15:00Z",
                    similarity_score=0.89,
                    confidence_score=0.92,
                    summary="Developer proposal for route modularization to avoid single monolithic application files.",
                    full_content="Issue #128: Developers requested a mechanism equivalent to Flask Blueprints or Starlette Router.",
                    url="https://github.com/fastapi/fastapi/issues/128",
                    tags=["Feature Request", "Routing"]
                )
            ]

        # 3. Pydantic v2
        elif "pydantic" in q:
            return [
                EvidenceItem(
                    id="ev-pyd-1",
                    type="Pull Request",
                    title="PR #9823: Migrate FastAPI core to Pydantic v2 and pydantic-core Rust engine",
                    reference_id="#9823",
                    author="tiangolo",
                    date="2023-06-30T16:00:00Z",
                    similarity_score=0.97,
                    confidence_score=0.99,
                    summary="Full migration to Pydantic v2 delivering 5x-20x validation speedups powered by pydantic-core in Rust.",
                    full_content="PR #9823: Replaced Pydantic v1 validation logic with pydantic-core Rust validation engine and updated JSON Schema generation to Draft 2020-12.",
                    url="https://github.com/fastapi/fastapi/pull/9823",
                    tags=["Pydantic v2", "Rust", "Performance"],
                    diff_snippet="- from pydantic import validator\n+ from pydantic import field_validator"
                )
            ]

        # 4. Lifespan
        elif "lifespan" in q:
            return [
                EvidenceItem(
                    id="ev-life-1",
                    type="Pull Request",
                    title="PR #9641: Support Starlette Lifespan context manager and deprecate @app.on_event",
                    reference_id="#9641",
                    author="Kludex",
                    date="2023-05-18T11:04:00Z",
                    similarity_score=0.96,
                    confidence_score=0.98,
                    summary="Replaces legacy on_event startup/shutdown handlers with Starlette asynccontextmanager Lifespan protocol.",
                    full_content="PR #9641: Encapsulates setup and teardown within a single asynccontextmanager yield block for structured resource lifetimes.",
                    url="https://github.com/fastapi/fastapi/pull/9641",
                    tags=["Lifespan", "Deprecation"],
                    diff_snippet="+ @asynccontextmanager\n+ async def lifespan(app: FastAPI):\n+     yield"
                )
            ]

        # 5. BackgroundTasks
        elif "background" in q:
            return [
                EvidenceItem(
                    id="ev-bg-1",
                    type="Pull Request",
                    title="PR #312: Add BackgroundTasks parameter for post-response async execution",
                    reference_id="#312",
                    author="tiangolo",
                    date="2019-05-15T18:00:00Z",
                    similarity_score=0.94,
                    confidence_score=0.96,
                    summary="Integrates BackgroundTasks parameter injection to run lightweight async tasks right after sending HTTP responses.",
                    full_content="PR #312: Enables post-response async execution (like sending emails or writing audit logs) without external Celery workers.",
                    url="https://github.com/fastapi/fastapi/pull/312",
                    tags=["BackgroundTasks", "Async"],
                    diff_snippet="+ from starlette.background import BackgroundTasks"
                )
            ]

        # 6. Starlette
        elif "starlette" in q:
            return [
                EvidenceItem(
                    id="ev-starlette-1",
                    type="Discussion",
                    title="Discussion #50: Why FastAPI is built directly on top of Starlette",
                    reference_id="#50",
                    author="tiangolo",
                    date="2018-12-10T11:00:00Z",
                    similarity_score=0.95,
                    confidence_score=0.97,
                    summary="Architectural rationale for building FastAPI on Starlette for high-performance ASGI routing and WebSockets.",
                    full_content="Discussion #50: Starlette provides high-performance ASGI web routing while FastAPI adds Pydantic validation and OpenAPI docs.",
                    url="https://github.com/fastapi/fastapi/discussions/50",
                    tags=["Starlette", "ASGI"]
                )
            ]

        # 7. OpenAPI
        elif "openapi" in q or "swagger" in q or "redoc" in q:
            return [
                EvidenceItem(
                    id="ev-openapi-1",
                    type="Commit",
                    title="Commit 1a2b3c4: Automatic OpenAPI 3.1.0 schema generation from Pydantic models",
                    reference_id="1a2b3c4",
                    author="tiangolo",
                    date="2021-03-20T14:30:00Z",
                    similarity_score=0.93,
                    confidence_score=0.95,
                    summary="Automatic OpenAPI schema and Swagger UI / ReDoc generation from Pydantic type signatures.",
                    full_content="Commit 1a2b3c4: Dynamically builds OpenAPI specifications reflecting path operations, security schemes, and schemas.",
                    url="https://github.com/fastapi/fastapi/commit/1a2b3c4",
                    tags=["OpenAPI", "Swagger"]
                )
            ]

        # Default / Dependency Injection
        return [
            EvidenceItem(
                id="ev-di-1",
                type="Pull Request",
                title="PR #10321: Redesign Dependency Injection with yield context managers",
                reference_id="#10321",
                author="tiangolo",
                date="2020-02-14T20:10:00Z",
                similarity_score=0.96,
                confidence_score=0.98,
                summary="Introduced yield dependencies allowing request-scoped setup and automatic teardown post-response.",
                full_content="PR #10321: Dependency injection redesigned using generator yield functions for automatic resource cleanup.",
                url="https://github.com/fastapi/fastapi/pull/10321",
                tags=["Dependency Injection", "Yield"],
                diff_snippet="+ def solve_dependencies(dependant: Dependant):"
            )
        ]

    def ask_repository(self, query: str, top_k: int = 5) -> RAGAnswer:
        start_time = time.time()
        evidences = self.get_evidence_by_query(query)
        q = query.lower()

        if "async" in q:
            ans_md = """### Architectural Analysis: Why FastAPI Supports Async Endpoints

FastAPI was built from day one to support both **`async def`** and standard synchronous **`def`** path operation functions (**PR #294**).

#### 1. The Core Concurrency Problem
Standard Python WSGI frameworks (like Flask or Django) process requests sequentially in synchronous worker threads. When an application performs IO-bound tasks (network calls, database queries), thread execution blocks, limiting throughput.

#### 2. FastAPI's Dual-Execution Model
- **`async def` Endpoints**: Executed directly on the main non-blocking **asyncio event loop**. Ideal for async database drivers (`asyncpg`, `motor`) and async HTTP clients (`httpx`).
- **`def` Endpoints**: Automatically offloaded to an external worker threadpool via **`anyio / Starlette run_in_threadpool`**. This guarantees that blocking synchronous code (e.g. `requests`, `sqlalchemy` sync) will not freeze the main event loop.

#### 3. Key Evolution Evidence
- **PR #294**: Added automatic threadpool dispatching for synchronous endpoints.
- **Commit 3fa8b12**: Optimized threadpool context switching to eliminate event loop thread contention.
"""
            citations = [
                CitationLink("PR #294 - Sync vs Async Endpoint Support", "Pull Request", "#294", "https://github.com/fastapi/fastapi/pull/294"),
                CitationLink("Commit 3fa8b12 - Threadpool Worker Optimization", "Commit", "3fa8b12", "https://github.com/fastapi/fastapi/commit/3fa8b12")
            ]

        elif "apirouter" in q or "router" in q:
            ans_md = """### Architectural Analysis: Why APIRouter Was Introduced

FastAPI introduced **`APIRouter`** in **PR #142** to provide modular route organization for scaling large codebases.

#### 1. The Core Problem
In early FastAPI releases (v0.1.0 - v0.10.0), all endpoints had to be defined directly on a single `FastAPI()` application instance, causing circular imports when splitting code across multiple files.

#### 2. Design Rationale
`APIRouter` acts as a virtual, modular routing tree:
- **Hierarchical Route Inclusion**: Routers are mounted into the main application via `app.include_router(router)`.
- **Inherited Prefixes & Tags**: Common path prefixes (e.g. `/items`) and OpenAPI tags are declared once at the router level.
- **Dependency Propagation**: Router-level dependencies apply automatically to all mounted child endpoints.

#### 3. Key Evolution Evidence
- **PR #142**: Added `APIRouter` class with prefix and tags inheritance.
- **Issue #128**: Community proposal establishing parity with Flask Blueprints.
"""
            citations = [
                CitationLink("PR #142 - Add APIRouter", "Pull Request", "#142", "https://github.com/fastapi/fastapi/pull/142"),
                CitationLink("Issue #128 - Modular Routing Proposal", "Issue", "#128", "https://github.com/fastapi/fastapi/issues/128")
            ]

        elif "pydantic" in q:
            ans_md = """### Architectural Analysis: Why FastAPI Migrated to Pydantic v2

FastAPI migrated its core validation engine to **Pydantic v2** in **PR #9823** (FastAPI v0.100.0).

#### 1. Performance Motivation
Pydantic v2 rewrote its core validation logic in Rust (`pydantic-core`), delivering a **5x to 20x performance speedup** in request body validation and JSON serialization.

#### 2. Schema Evolution
- Replaced legacy `@validator` methods with `@field_validator`.
- Adopted JSON Schema Draft 2020-12 specification.
- Maintained backwards compatibility for Pydantic v1 models via `pydantic.v1`.

#### 3. Key Evolution Evidence
- **PR #9823**: Core migration to Pydantic v2 and `pydantic-core`.
- **Release v0.100.0**: Official FastAPI release bundling Pydantic v2 support.
"""
            citations = [
                CitationLink("PR #9823 - Pydantic v2 Migration", "Pull Request", "#9823", "https://github.com/fastapi/fastapi/pull/9823"),
                CitationLink("Release v0.100.0 - Pydantic v2 Release", "Release Notes", "v0.100.0", "https://github.com/fastapi/fastapi/releases/tag/0.100.0")
            ]

        elif "lifespan" in q:
            ans_md = """### Architectural Analysis: The Lifespan Protocol Adoption

FastAPI adopted **Starlette Lifespan context managers** in **PR #9641** to replace legacy event handlers.

#### 1. Why `@app.on_event` Was Deprecated
- Legacy `@app.on_event("startup")` and `@app.on_event("shutdown")` executed in non-deterministic order.
- Global variables were required to pass database connections initialized during startup down to endpoint routes.

#### 2. Lifespan Context Manager Pattern
Using `@asynccontextmanager`, startup logic runs before `yield` and shutdown logic runs after `yield` within a single exception-safe block:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await init_db()
    yield {"db": db}
    await db.close()
```

#### 3. Key Evolution Evidence
- **PR #9641**: Added Lifespan context manager support.
- **Issue #8142**: Discussion detailing on_event deprecation rationale.
"""
            citations = [
                CitationLink("PR #9641 - Lifespan Protocol Support", "Pull Request", "#9641", "https://github.com/fastapi/fastapi/pull/9641"),
                CitationLink("Issue #8142 - Deprecate on_event Handlers", "Issue", "#8142", "https://github.com/fastapi/fastapi/issues/8142")
            ]

        elif "background" in q:
            ans_md = """### Architectural Analysis: Why BackgroundTasks Was Added

FastAPI integrated **`BackgroundTasks`** in **PR #312** to enable post-response asynchronous task execution.

#### 1. Core Motivation
Developers often need to execute lightweight asynchronous operations (such as sending confirmation emails, recording audit metrics, or logging analytics) right after returning an HTTP response to the client.

#### 2. Design Rationale
Rather than forcing developers to set up heavy external task brokers like Celery or Redis Queue for simple tasks, FastAPI integrated Starlette's `BackgroundTasks` directly into parameter injection.

#### 3. Key Evolution Evidence
- **PR #312**: Direct integration of `BackgroundTasks` parameter dependency injection.
"""
            citations = [
                CitationLink("PR #312 - Add BackgroundTasks Parameter", "Pull Request", "#312", "https://github.com/fastapi/fastapi/pull/312")
            ]

        elif "starlette" in q:
            ans_md = """### Architectural Analysis: Why FastAPI Is Built On Starlette

FastAPI was intentionally designed as an application layer built directly on top of the **Starlette** ASGI framework (**Discussion #50**).

#### 1. Core Rationale
Starlette provides high-performance ASGI routing, WebSockets, background tasks, cookie sessions, and HTTP response handling.

#### 2. FastAPI's Added Value
FastAPI extends Starlette by adding automatic Pydantic type validation, OpenAPI schema generation, Swagger UI interactive documentation, and a type-hint-driven dependency injection system.

#### 3. Key Evolution Evidence
- **Discussion #50**: Detailed architectural rationale by `@tiangolo`.
"""
            citations = [
                CitationLink("Discussion #50 - Starlette Framework Integration", "Discussion", "#50", "https://github.com/fastapi/fastapi/discussions/50")
            ]

        elif "openapi" in q or "swagger" in q:
            ans_md = """### Architectural Analysis: How OpenAPI Support Evolved

FastAPI automatically generates **OpenAPI 3.1.0** specifications from Python type signatures and Pydantic models (**Commit 1a2b3c4**).

#### 1. Core Rationale
Manual API documentation gets out of sync with actual backend code. FastAPI uses Pydantic JSON Schema metadata to generate interactive `/docs` (Swagger UI) and `/redoc` documentation automatically.

#### 2. Key Evolution Evidence
- **Commit 1a2b3c4**: Automatic OpenAPI 3.1.0 schema reflection and OAuth2 security scheme integration.
"""
            citations = [
                CitationLink("Commit 1a2b3c4 - OpenAPI Schema Generation", "Commit", "1a2b3c4", "https://github.com/fastapi/fastapi/commit/1a2b3c4")
            ]

        else:
            ans_md = """### Architectural Analysis: FastAPI Dependency Injection System

FastAPI's **Dependency Injection (DI)** mechanism was designed around Python type annotations and generator context managers (**PR #10321**).

#### 1. Core Motivation
FastAPI built DI directly on top of Python's `Depends()` and type hints:
- **Automatic Request Scope**: Dependencies are evaluated per request and cached during request lifetime (`use_cache=True`).
- **Hierarchical Teardown**: Using `yield` inside dependencies allows automatic setup (e.g., DB session open) and teardown (e.g., DB session commit/close).

#### 2. Key Evolution Evidence
- **PR #10321**: Added `yield` context manager dependencies for teardown.
- **Commit 7e891ab**: Per-request dependency tree caching optimization.
"""
            citations = [
                CitationLink("PR #10321 - Yield Dependencies", "Pull Request", "#10321", "https://github.com/fastapi/fastapi/pull/10321"),
                CitationLink("Commit 7e891ab - Dependency Tree Caching", "Commit", "7e891ab", "https://github.com/fastapi/fastapi/commit/7e891ab")
            ]

        verif = VerificationResult(
            status="VERIFIED",
            confidence_score=0.96,
            nli_score=0.94,
            hallucination_guard_passed=True,
            unsupported_claims_count=0,
            verification_notes="Claims verified against retrieved FastAPI repository evidence. Entailment check passed."
        )

        total_ms = (time.time() - start_time) * 1000 + 120.0

        return RAGAnswer(
            query=query,
            markdown_answer=ans_md,
            evidences=evidences,
            verification=verif,
            citations=citations,
            retrieval_latency_ms=35.0,
            llm_latency_ms=85.0,
            total_latency_ms=total_ms,
            prompt_tokens=1250,
            completion_tokens=380,
            model_name="llama-3.3-70b-versatile (Groq)"
        )

    def get_timeline(self) -> List[TimelineEvent]:
        from backend.dataset import FASTAPI_REPO_DATASET
        events = []
        for idx, item in enumerate(FASTAPI_REPO_DATASET[:7]):
            events.append(
                TimelineEvent(
                    id=f"t-{idx}",
                    stage=item.get("type", "Event"),
                    title=item.get("title", ""),
                    description=item.get("content", "")[:150] + "...",
                    author=item.get("author", "tiangolo"),
                    date=item.get("date", "2019-04-12")[:10],
                    reference_id=item.get("reference_id", "N/A"),
                    url=item.get("url", "https://github.com/fastapi/fastapi"),
                    icon="📌",
                    details={"type": item.get("type")}
                )
            )
        return events

    def get_evaluation_metrics(self) -> RAGEvaluationMetrics:
        return RAGEvaluationMetrics(
            context_precision=0.942,
            context_recall=0.915,
            faithfulness=0.985,
            answer_relevancy=0.960,
            ragas_score=0.950,
            avg_retrieval_latency_ms=35.2,
            avg_llm_latency_ms=85.4,
            avg_prompt_tokens=1250,
            avg_completion_tokens=380,
            total_cost_usd=0.00035,
            historical_benchmark=[
                {"version": "v1.0 Naive RAG", "precision": 0.72, "recall": 0.68, "faithfulness": 0.81, "ragas": 0.73},
                {"version": "v1.5 MMR FAISS", "precision": 0.84, "recall": 0.82, "faithfulness": 0.90, "ragas": 0.85},
                {"version": "v2.0 PatchContext + NLI", "precision": 0.942, "recall": 0.915, "faithfulness": 0.985, "ragas": 0.950}
            ]
        )
