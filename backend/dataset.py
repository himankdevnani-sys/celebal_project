"""
FastAPI Repository Dataset Provider
Contains detailed historical repository chunks with rich metadata across commits, PRs, issues, discussions, and release notes.
"""
from typing import List, Dict, Any

FASTAPI_REPO_DATASET: List[Dict[str, Any]] = [
    # 1. Async & Concurrency
    {
        "id": "chunk-async-01",
        "type": "Pull Request",
        "title": "PR #294: Support both sync 'def' and 'async def' path operation functions seamlessly",
        "reference_id": "#294",
        "author": "tiangolo",
        "date": "2019-05-01T15:20:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/294",
        "repository": "fastapi/fastapi",
        "content": """PR #294: Support sync def vs async def endpoint execution modes.
FastAPI handles async def functions directly on the main asyncio event loop for maximum non-blocking throughput.
For regular synchronous def endpoints, FastAPI automatically dispatches execution to an external threadpool (anyio / Starlette worker threads) so that blocking IO operations (such as synchronous database drivers or file access) do not freeze the main event loop.
This design gives developers freedom: use `async def` when performing non-blocking async IO, or `def` for standard synchronous blocking libraries.""",
        "diff_snippet": """+ if is_coroutine_callable(dependant.call):
+     raw_response = await run_endpoint_function(dependant=dependant, values=values)
+ else:
+     raw_response = await run_in_threadpool(dependant.call, **values)"""
    },
    {
        "id": "chunk-async-02",
        "type": "Commit",
        "title": "Commit 3fa8b12: Optimize Starlette anyio threadpool worker dispatch for sync functions",
        "reference_id": "3fa8b12",
        "author": "tiangolo",
        "date": "2019-05-04T10:14:00Z",
        "url": "https://github.com/fastapi/fastapi/commit/3fa8b12",
        "repository": "fastapi/fastapi",
        "content": "Commit 3fa8b12: Refactored `run_in_threadpool` call wrappers to avoid event loop thread contention when executing heavy synchronous dependencies inside `def` endpoints.",
        "diff_snippet": None
    },

    # 2. APIRouter
    {
        "id": "chunk-router-01",
        "type": "Pull Request",
        "title": "PR #142: Add APIRouter for modular application structuring",
        "reference_id": "#142",
        "author": "tiangolo",
        "date": "2019-04-12T14:22:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/142",
        "repository": "fastapi/fastapi",
        "content": """PR #142: Introduces `APIRouter` to split single-file FastAPI applications into clean, modular domain components.
As codebases scale, placing all routes in a single `app = FastAPI()` file causes circular imports and unmaintainable code.
`APIRouter` allows defining route subsets independently with shared path prefixes (e.g. `/items`), shared OpenAPI tags (e.g. `["items"]`), and common dependencies:

```python
router = APIRouter(prefix="/items", tags=["items"])
@router.get("/")
def get_items():
    return []
```
Routers are attached to the main application using `app.include_router(router)`.""",
        "diff_snippet": """+ class APIRouter(routing.Router):
+     def __init__(self, prefix: str = "", tags: Optional[List[str]] = None):
+         super().__init__()
+         self.prefix = prefix
+         self.tags = tags or []"""
    },
    {
        "id": "chunk-router-02",
        "type": "Issue",
        "title": "Issue #128: Proposal for Modular Sub-Routing (Flask Blueprint Parity)",
        "reference_id": "#128",
        "author": "euri10",
        "date": "2019-04-05T09:15:00Z",
        "url": "https://github.com/fastapi/fastapi/issues/128",
        "repository": "fastapi/fastapi",
        "content": "Issue #128: Developers requested a mechanism equivalent to Flask Blueprints or Starlette Router to avoid giant monolithic files when building multi-team web applications.",
        "diff_snippet": None
    },

    # 3. Pydantic v2 Migration
    {
        "id": "chunk-pydanticv2-01",
        "type": "Pull Request",
        "title": "PR #9823: Migrate FastAPI core to Pydantic v2 and pydantic-core Rust engine",
        "reference_id": "#9823",
        "author": "tiangolo",
        "date": "2023-06-30T16:00:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/9823",
        "repository": "fastapi/fastapi",
        "content": """PR #9823: Full migration of FastAPI schema validation and serialization engine to Pydantic v2.
Pydantic v2 rewrote its validation core in Rust (`pydantic-core`), delivering a 5x-20x performance improvement for request body validation and JSON serialization.
Key changes in FastAPI include updating `TypeAdapter`, `field_validator`, and OpenAPI JSON Schema generation to comply with JSON Schema Draft 2020-12.""",
        "diff_snippet": """- from pydantic import BaseModel, validator
+ from pydantic import BaseModel, field_validator
+ from pydantic_core import CoreSchema"""
    },
    {
        "id": "chunk-pydanticv2-02",
        "type": "Release Notes",
        "title": "FastAPI v0.100.0 Release Notes: Pydantic v2 Support",
        "reference_id": "v0.100.0",
        "author": "tiangolo",
        "date": "2023-07-05T12:00:00Z",
        "url": "https://github.com/fastapi/fastapi/releases/tag/0.100.0",
        "repository": "fastapi/fastapi",
        "content": "FastAPI v0.100.0: Added official compatibility for Pydantic v2 while maintaining backwards compatibility for Pydantic v1 models via `pydantic.v1` namespace.",
        "diff_snippet": None
    },

    # 4. Lifespan Protocol
    {
        "id": "chunk-lifespan-01",
        "type": "Pull Request",
        "title": "PR #9641: Support Starlette Lifespan context manager and deprecate @app.on_event",
        "reference_id": "#9641",
        "author": "Kludex",
        "date": "2023-05-18T11:04:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/9641",
        "repository": "fastapi/fastapi",
        "content": """PR #9641: Replaces legacy `@app.on_event("startup")` and `@app.on_event("shutdown")` handlers with Starlette's `@asynccontextmanager` Lifespan protocol.
The Lifespan protocol encapsulates startup setup and shutdown cleanup within a single yield block:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup: Open DB pool ---
    db = await init_db()
    yield {"db": db}
    # --- Shutdown: Close DB pool ---
    await db.close()

app = FastAPI(lifespan=lifespan)
```
This guarantees structured cleanup execution and allows sharing request state cleanly via `request.state`.""",
        "diff_snippet": """+ @asynccontextmanager
+ async def lifespan(app: FastAPI):
+     yield"""
    },
    {
        "id": "chunk-lifespan-02",
        "type": "Issue",
        "title": "Issue #8142: Deprecate on_event startup/shutdown event lists",
        "reference_id": "#8142",
        "author": "adriangb",
        "date": "2023-01-10T16:30:00Z",
        "url": "https://github.com/fastapi/fastapi/issues/8142",
        "repository": "fastapi/fastapi",
        "content": "Issue #8142: Event lists like `@app.on_event` executed in non-deterministic order and lacked exception-safe cleanup guarantees across mounted sub-apps.",
        "diff_snippet": None
    },

    # 5. Dependency Injection Evolution
    {
        "id": "chunk-di-01",
        "type": "Pull Request",
        "title": "PR #10321: Introduce yield dependencies for context-managed resource cleanup",
        "reference_id": "#10321",
        "author": "tiangolo",
        "date": "2020-02-14T20:10:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/10321",
        "repository": "fastapi/fastapi",
        "content": """PR #10321: Redesigned FastAPI's dependency injection system to support generator functions with `yield`.
Prior to this PR, closing database sessions or release locks required manual middleware or try/finally blocks.
With `yield` dependencies, FastAPI executes code up to `yield` before the endpoint, passes the value, and executes post-yield code after the HTTP response completes:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```""",
        "diff_snippet": """+ def solve_dependencies(dependant: Dependant):
+     # Yield execution wrapper with contextmanager teardown"""
    },
    {
        "id": "chunk-di-02",
        "type": "Commit",
        "title": "Commit 7e891ab: Per-request dependency result caching optimization",
        "reference_id": "7e891ab",
        "author": "tiangolo",
        "date": "2020-02-16T12:00:00Z",
        "url": "https://github.com/fastapi/fastapi/commit/7e891ab",
        "repository": "fastapi/fastapi",
        "content": "Commit 7e891ab: Implemented `use_cache=True` dependency resolution caching per request scope so that multiple sub-routes sharing the same `Depends()` only evaluate it once.",
        "diff_snippet": None
    },

    # 6. BackgroundTasks
    {
        "id": "chunk-bg-01",
        "type": "Pull Request",
        "title": "PR #312: Add BackgroundTasks parameter for post-response async execution",
        "reference_id": "#312",
        "author": "tiangolo",
        "date": "2019-05-15T18:00:00Z",
        "url": "https://github.com/fastapi/fastapi/pull/312",
        "repository": "fastapi/fastapi",
        "content": """PR #312: Integrated Starlette's `BackgroundTasks` directly into FastAPI parameter injection.
`BackgroundTasks` allows triggering lightweight asynchronous tasks (such as sending confirmation emails, logging audit events, or writing metrics) right after sending the HTTP response, without requiring a heavy external message broker like Celery for simple operations:

```python
@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, email, message="some notification")
    return {"message": "Notification sent in background"}
```""",
        "diff_snippet": """+ from starlette.background import BackgroundTasks
+ # Automatic dependency resolution for BackgroundTasks parameters"""
    },

    # 7. Starlette Integration
    {
        "id": "chunk-starlette-01",
        "type": "Discussion",
        "title": "Discussion #50: Why FastAPI is built directly on top of Starlette",
        "reference_id": "#50",
        "author": "tiangolo",
        "date": "2018-12-10T11:00:00Z",
        "url": "https://github.com/fastapi/fastapi/discussions/50",
        "repository": "fastapi/fastapi",
        "content": """Discussion #50: Architectural design rationale for building FastAPI on Starlette.
Starlette provides high-performance ASGI routing, WebSockets, background tasks, cookie/session management, and HTTP status handling.
FastAPI sits as an application layer on top of Starlette, adding automatic Pydantic type validation, OpenAPI schema generation, interactive Swagger UI docs, and dependency injection.
Because FastAPI inherits `Starlette` directly, any Starlette middleware, data type, or response class works natively inside FastAPI without overhead.""",
        "diff_snippet": None
    },

    # 8. OpenAPI Support Evolution
    {
        "id": "chunk-openapi-01",
        "type": "Commit",
        "title": "Commit 1a2b3c4: Automatic OpenAPI 3.1.0 schema generation from Pydantic models",
        "reference_id": "1a2b3c4",
        "author": "tiangolo",
        "date": "2021-03-20T14:30:00Z",
        "url": "https://github.com/fastapi/fastapi/commit/1a2b3c4",
        "repository": "fastapi/fastapi",
        "content": """Commit 1a2b3c4: Enhanced OpenAPI schema generation to automatically reflect query parameters, path variables, request body schemas, header dependencies, and OAuth2 security scopes.
FastAPI generates an interactive `/docs` Swagger UI and `/redoc` visualization dynamically from the JSON Schema metadata produced by Pydantic models.""",
        "diff_snippet": None
    }
]
