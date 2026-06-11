from pathlib import Path
import re

from backend.models.schemas import AnalysisRequest, Language, Submission

LANGUAGE_EXTENSIONS: dict[Language, set[str]] = {
    Language.python: {".py"},
    Language.javascript: {".js", ".jsx"},
    Language.typescript: {".ts", ".tsx"},
    Language.java: {".java"},
    Language.cpp: {".cpp", ".cc", ".cxx", ".hpp", ".hxx", ".h", ".c"},
    Language.c: {".c", ".h", ".cpp", ".cc", ".cxx"},
    Language.text: {".txt", ".md", ".rst"},
}


def validate_declared_languages(request: AnalysisRequest) -> None:
    _validate_submission(request.left)
    _validate_submission(request.right)


def _validate_submission(submission: Submission) -> None:
    suffix = Path(submission.name).suffix.lower()
    allowed_suffixes = LANGUAGE_EXTENSIONS.get(submission.language, set())

    # 1. Trust generic or missing extensions (common for pasted code)
    if not suffix or suffix in {".txt", ".md", ".rst"}:
        return
    
    # 2. Allow 'text' mode to accept any extension
    if submission.language == Language.text:
        return

    # 3. Only block if the extension is explicitly known for another language
    all_code_suffixes = set().union(*LANGUAGE_EXTENSIONS.values())
    if suffix in all_code_suffixes and suffix not in allowed_suffixes:
        allowed = ", ".join(sorted(allowed_suffixes))
        raise ValueError(
            f"File '{submission.name}' has extension '{suffix}', which is not "
            f"allowed for {submission.language.value}. Expected: {allowed}"
        )

    # We removed the 'detected != submission.language' check.
    # Heuristics should assist detection, not block user-declared intent.


def detect_language_hint(source: str) -> Language | None:
    trimmed = source.strip()
    if not trimmed:
        return None

    if re.search(
        r"\bstd::|\bcout\s*<<|\bcin\s*>>|#\s*include\s*<"
        r"(iostream|vector|string|map|unordered_map|set|algorithm|bits/stdc\+\+\.h)>"
        r"|\btemplate\s*<|\bnamespace\s+\w+|\busing\s+namespace\s+std\b",
        source,
    ):
        return Language.cpp
    if re.search(r"\bpublic\s+class\s+\w+|\bSystem\.out\.println\s*\(", source):
        return Language.java
    if re.search(r"\bdef\s+\w+\s*\(|^\s*import\s+\w+|^\s*from\s+\w+\s+import\s+", source, re.MULTILINE):
        return Language.python
    # Added more specific TS indicators to avoid C++ template confusion
    if re.search(r"\binterface\s+\w+|:\s*(string|number|boolean)\b|type\s+\w+\s*=", source):
        return Language.typescript
    if re.search(r"\bfunction\s+\w+\s*\(|\bconst\s+\w+\s*=|\blet\s+\w+\s*=", source):
        return Language.javascript
    if re.search(r"\bint\s+main\s*\(|\bprintf\s*\(|\bscanf\s*\(|#\s*include\s*<(stdio|stdlib|string|math)\.h>", source):
        return Language.c
    return None
