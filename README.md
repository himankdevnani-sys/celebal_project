# PatchContext ⚡

> *"Understand why FastAPI evolved the way it did."*

**PatchContext** is an AI-powered Retrieval-Augmented Generation (RAG) web application designed to analyze and explain the architectural design decisions, commit history, pull request discussions, and issue evolution of the [FastAPI](https://github.com/fastapi/fastapi) repository.

---

## 🌟 Key Features

- 🏠 **Repository Insights Dashboard**: Real-time stats on commits, PRs, issues, discussions, and vector embeddings indexed.
- 💬 **Semantic Codebase Search**: Ask natural language architectural questions (e.g. *"Why was APIRouter introduced?"*, *"Why was dependency injection redesigned?"*).
- 📚 **Retrieved Evidence Explorer**: Inspect exact commit SHAs, PR discussions, and issues with similarity scores and code diffs.
- 🧠 **AI Answer Engine with Citations**: Structured AI explanations with verifiable inline citations linking back to GitHub source entries.
- 🛡️ **Hallucination & NLI Verification**: Real-time Natural Language Inference (NLI) scoring and faithfulness verification.
- 📈 **Repository Timeline**: Visual evolutionary timeline tracking changes from issue proposal to pull request, review, merge, and release.
- ⚡ **Interactive RAG Pipeline Visualization**: Step-by-step pipeline execution flow diagram (Repository → Chunking → FAISS → MMR → LLM → NLI).
- 📊 **RAGAs Evaluation Dashboard**: Comprehensive metrics tracking Context Precision, Context Recall, Faithfulness, Answer Relevancy, Latency, and Token costs.
- ⚙️ **Configurable RAG Settings**: Dynamic control over retriever types, vector search thresholds, temperature, and top-k parameters.

---

## 🛠️ Architecture

```
project/
├── app.py                      # Main application entry point & router
├── components/                 # Reusable UI widgets
│   ├── sidebar.py              # Dark themed navigation sidebar
│   ├── header.py               # Hero headers & badges
│   ├── cards.py                # Glassmorphism cards & stat displays
│   ├── timeline.py             # Visual timeline renderer
│   ├── charts.py               # Plotly dashboard charts
│   └── pipeline.py             # RAG workflow diagram component
├── pages/                      # Application view pages
│   ├── home.py
│   ├── ask_repository.py
│   ├── retrieved_evidence.py
│   ├── ai_answer.py
│   ├── verification.py
│   ├── timeline_page.py
│   ├── pipeline_page.py
│   ├── evaluation.py
│   ├── settings.py
│   └── about.py
├── services/                   # Service layer decoupled from UI
│   ├── api.py                  # API router choosing mock vs real backend
│   └── mock_service.py         # Realistic mock data provider
├── models/                     # Type-safe Pydantic models
│   ├── answer.py
│   ├── evidence.py
│   └── timeline.py
├── styles/                     # Design System & Styling
│   └── custom_css.py           # GitHub Dark theme & Glassmorphism CSS
├── utils/                      # Configurations & Utilities
│   ├── config.py               # Environment variable loader
│   └── helpers.py              # Formatting & logging utilities
└── tests/                      # Automated test suite
    └── test_app.py
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set `USE_MOCK=True` to run the application in standalone mock mode without needing a backend server running.

### 3. Run Application

```bash
streamlit run app.py
```

---

## 🔌 Connecting a Real FastAPI Backend

To connect PatchContext to a live FastAPI backend:

1. Update `.env`:
   ```env
   USE_MOCK=False
   BACKEND_URL=http://localhost:8000
   ```
2. Ensure your backend exposes the following REST endpoints:
   - `GET /health`
   - `POST /search`
   - `POST /ask`
   - `GET /timeline`
   - `GET /evaluation`
   - `GET /settings`

---

## 📄 License

MIT License. Designed with ♥ for the FastAPI Community.
