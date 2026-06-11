import re
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect

from backend.models.schemas import AnalysisReport, AnalysisRequest, Language, Submission
from backend.services.analysis_service import AnalysisService
from backend.utils.file_validation import validate_source_upload
from backend.utils.language_detection import validate_declared_languages, detect_language_hint, LANGUAGE_EXTENSIONS

router = APIRouter()
service = AnalysisService()

def detect_language_heuristically(content: str, filename: str = "") -> Language:
    """
    Wrapper around the unified hint detector with filename fallback.
    """
    # 1. Try filename extension if it's not a generic placeholder
    suffix = Path(filename).suffix.lower()
    placeholders = {"left.py", "right.py", "code.py", "untitled.py", "left", "right"}
    if suffix and filename.lower() not in placeholders:
        for lang, exts in LANGUAGE_EXTENSIONS.items():
            if suffix in exts:
                return lang

    # 2. Try content hint
    hint = detect_language_hint(content)
    if hint:
        return hint

    return Language.python

def ensure_language(submission: Submission):
    """
    Applies detection if language is not explicitly set or is default.
    If an extension already exists that matches a known language, we respect it.
    """
    if submission.content and (not submission.language or submission.language == Language.python):
        detected = detect_language_heuristically(submission.content, submission.name)
        # Only override if we found something meaningful or if the user stayed on default Python
        submission.language = detected
            
    # Always sync extension for generic placeholders to match the language (detected or manual)
    # This prevents validation errors when a user types C++ code into a 'left.py' field.
    generic_placeholders = {"left.py", "right.py", "code.py", "untitled.py", "left", "right"}
    is_placeholder = submission.name.lower() in generic_placeholders
    if is_placeholder:
        ext_map = {
            Language.cpp: ".cpp",
            Language.c: ".c",
            Language.java: ".java",
            Language.python: ".py",
            Language.javascript: ".js",
            Language.typescript: ".ts",
            Language.text: ".txt"
        }
        base = submission.name.rsplit(".", 1)[0]
        # Update extension to match language to satisfy the extension validator
        new_ext = ext_map.get(submission.language, ".txt")
        submission.name = f"{base}{new_ext}"

def validate_and_unify_request(payload: AnalysisRequest):
    """Orchestrates language detection and ensures consistency across both files."""
    ensure_language(payload.left)
    ensure_language(payload.right)
    
    # Enforce consistency: If one was detected/selected as a specific language 
    # but the other stayed as Python (fallback), unify them to the specific language.
    if payload.left.language != payload.right.language:
        if payload.left.language == Language.python:
            payload.left.language = payload.right.language
        elif payload.right.language == Language.python:
            payload.right.language = payload.left.language

    validate_declared_languages(payload)
    validate_language_consistency(payload)

def persist_submissions(payload: AnalysisRequest):
    """Saves the content of submissions to the local 'uploads' directory."""
    try:
        # Use an absolute path or a path relative to the project root for consistency
        save_dir = Path(__file__).parent.parent.parent / "uploads"
        save_dir.mkdir(parents=True, exist_ok=True)
        
        for sub in [payload.left, payload.right]:
            if sub.content:
                safe_name = Path(sub.name).name
                with open(save_dir / safe_name, "w", encoding="utf-8") as f:
                    f.write(sub.content)
    except Exception:
        # Do not block analysis if local file persistence fails
        pass

def validate_language_consistency(payload: AnalysisRequest):
    """Ensures both submissions are of the same language to prevent invalid comparisons."""
    left_lang = payload.left.language
    right_lang = payload.right.language

    # Allow C and C++ to be compared as they are often syntactically compatible
    is_compatible = (left_lang == right_lang) or \
                    (left_lang in [Language.c, Language.cpp] and right_lang in [Language.c, Language.cpp])

    if not is_compatible:
        raise ValueError(
            f"Language mismatch: '{payload.left.name}' is {left_lang.value} "
            f"but '{payload.right.name}' is {right_lang.value}. "
            "Cross-language comparison is not currently supported."
        )

@router.post("/compare", response_model=AnalysisReport)
async def compare(payload: AnalysisRequest) -> AnalysisReport:
    # Store the typed code in files
    persist_submissions(payload)
    
    try:
        validate_and_unify_request(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return await service.compare(payload)


@router.post("/upload-compare", response_model=AnalysisReport)
async def upload_compare(
    left: UploadFile = File(...),
    right: UploadFile = File(...),
    language: Language = Language.python,
) -> AnalysisReport:
    left_text = await validate_source_upload(left)
    right_text = await validate_source_upload(right)
    payload = AnalysisRequest(
        left=Submission(name=left.filename or "left", language=language, content=left_text),
        right=Submission(name=right.filename or "right", language=language, content=right_text),
    )

    try:
        validate_and_unify_request(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return await service.compare(payload)


@router.websocket("/live")
async def live_analysis(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            await websocket.send_json({"phase": "queued", "progress": 10})
            request = AnalysisRequest.model_validate(payload)
            validate_and_unify_request(request)
            persist_submissions(request)
            report = await service.compare(request)
            await websocket.send_json({"phase": "complete", "progress": 100, "report": report.model_dump()})
    except ValueError as exc:
        await websocket.send_json({"phase": "error", "progress": 0, "detail": str(exc)})
    except WebSocketDisconnect:
        return
