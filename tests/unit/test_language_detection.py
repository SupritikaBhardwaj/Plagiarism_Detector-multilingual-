import pytest

from backend.models.schemas import AnalysisRequest, Language, Submission
from backend.utils.language_detection import detect_language_hint, validate_declared_languages


def test_detects_cpp_source() -> None:
    source = '#include <iostream>\nint main() { std::cout << "hi"; }\n'
    assert detect_language_hint(source) == Language.cpp


def test_detects_c_source_with_include() -> None:
    source = '#include <stdio.h>\nint main() { printf("hi"); return 0; }\n'
    assert detect_language_hint(source) == Language.c


def test_accepts_c_file_declared_as_c() -> None:
    payload = AnalysisRequest(
        left=Submission(name="left.c", language=Language.c, content='#include <stdio.h>\nint main() { printf("hi"); }\n'),
        right=Submission(name="right.c", language=Language.c, content='#include <stdio.h>\nint main() { printf("hello"); }\n'),
    )
    validate_declared_languages(payload)


def test_rejects_cpp_file_declared_as_python() -> None:
    payload = AnalysisRequest(
        left=Submission(name="left.cpp", language=Language.python, content="#include <iostream>\nint main() {}\n"),
        right=Submission(name="right.cpp", language=Language.python, content="#include <iostream>\nint main() {}\n"),
    )
    with pytest.raises(ValueError, match="looks like .cpp"):
        validate_declared_languages(payload)
