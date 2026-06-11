# Installation Guide

## Docker

```bash
docker compose up --build
```

## Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload
```

## Frontend

```bash
scripts/check_frontend_env.sh
cd frontend
npm install
npm run dev
```

### WSL 1 Node/npm Issue

If `npm --version` prints `WSL 1 is not supported`, the project is not the
problem. The Linux shell is picking up Windows npm from `/mnt/c/Program Files`
without a Linux `node` binary.

Supported fixes:

- Upgrade the distro to WSL 2 and install Linux Node.js 20+.
- Run frontend commands from Windows PowerShell inside `frontend/`.
- Use Docker with `docker compose up --build frontend`.

Useful checks:

```bash
which node
which npm
scripts/check_frontend_env.sh
```

## Testing

```bash
.venv/bin/pytest
cd frontend && npm run build
```

## Production Hardening Checklist

- Replace demo auth with persisted users and refresh tokens.
- Run parser jobs inside a container sandbox with CPU and memory limits.
- Add PostgreSQL migrations with Alembic.
- Add real Transformer inference workers or model-serving endpoints.
- Configure object storage for uploaded submissions.
- Enable structured logging, tracing, and metrics.
