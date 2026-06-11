# PlagiaScope AI

PlagiaScope AI is a full-stack, modular plagiarism detection platform for source code and documents. It combines compiler design techniques, static analysis, graph analysis, NLP, and explainable AI scoring.

## Architecture

- `frontend/` - React + TypeScript UI with Tailwind, Framer Motion, Recharts, and Monaco integration points.
- `backend/` - FastAPI REST and WebSocket APIs, authentication, reporting, persistence boundaries.
- `compiler_engine/` - lexical analysis, parsing adapters, AST, CFG, PDG, IR, and semantic analysis.
- `plagiarism_core/` - token, text, tree, graph, semantic, and score-fusion algorithms.
- `ai_engine/` - embeddings, stylometry, transformer adapters, and AI-generated code classifiers.
- `docs/` - API, database schema, architecture notes, and installation guide.
- `tests/` - focused unit and integration tests.

## Quick Start

```bash
docker compose up --build
```

Backend: `http://localhost:8000`

Frontend: `http://localhost:5173`

For local backend development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload
```

For local frontend development:

```bash
cd frontend
npm install
npm run dev
```

If you are on WSL 1 and see `WSL 1 is not supported`, the shell is trying
to use Windows npm from `/mnt/c`. Use WSL 2, run the frontend commands from
Windows PowerShell, or use Docker. You can check the environment with:

```bash
scripts/check_frontend_env.sh
```

## Detection Strategies

The system fuses independent evidence from:

- Exact and normalized text similarity
- Token fingerprints, n-grams, and Winnowing
- AST shape similarity and tree edit approximations
- CFG/PDG structural similarity
- Embedding-based semantic similarity
- Stylometry features
- AI-generation probability

## Report Exports

Reports are available as JSON, CSV, and PDF-ready structured payloads. The backend exposes report generation boundaries so a production deployment can plug in WeasyPrint, ReportLab, or a document service.

## Production Notes

This repository is intentionally modular. Heavy production integrations such as CodeBERT, Elasticsearch indexing, PostgreSQL migrations, MongoDB persistence, and Redis queues are represented with clean services and configuration seams so the project can run locally while still being ready for enterprise hardening.
