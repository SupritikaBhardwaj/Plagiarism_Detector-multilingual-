from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from backend.routes import analysis, auth, reports

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PlagiaScope AI API",
    version="0.1.0",
    description="Compiler-aware plagiarism detection APIs for code and documents.",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "PlagiaScope AI API",
        "docs": "/docs",
        "health": "/health",
        "frontend": "http://127.0.0.1:5173",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "plagiascope-api"}
