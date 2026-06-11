from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Language(str, Enum):
    python = "python"
    javascript = "javascript"
    typescript = "typescript"
    java = "java"
    cpp = "cpp"
    c = "c"
    text = "text"


class Submission(BaseModel):
    name: str
    language: Language
    content: str = Field(min_length=1)


class AnalysisRequest(BaseModel):
    left: Submission
    right: Submission
    enable_ai: bool = True


class SimilarityBreakdown(BaseModel):
    text: float
    token: float
    ast: float
    graph: float
    semantic: float
    stylometry: float
    ai_generated_probability: float


class EvidenceItem(BaseModel):
    kind: str
    message: str
    confidence: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class AnalysisReport(BaseModel):
    report_id: str
    overall_similarity: float
    risk_level: str
    breakdown: SimilarityBreakdown
    evidence: list[EvidenceItem]
    highlighted_regions: list[dict[str, Any]]
    ast: dict[str, Any]
    cfg: dict[str, Any]
    pdg: dict[str, Any]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

