import pytest
from backend.routes.analysis import detect_language_heuristically
from backend.models.schemas import Language

def test_detect_cpp_from_content():
    content = "#include <iostream>\nint main() { return 0; }"
    # Even with a .py filename, content should win
    assert detect_language_heuristically(content, "left.py") == Language.cpp

def test_detect_java_from_content():
    content = "public class Main { public static void main(String[] args) {} }"
    assert detect_language_heuristically(content, "code.py") == Language.java

def test_detect_python_from_content():
    content = "def my_func():\n    print('hello')"
    assert detect_language_heuristically(content, "untitled.py") == Language.python

def test_fallback_to_extension_for_specific_filenames():
    # Non-generic filename with ambiguous content
    content = "x = 10" 
    assert detect_language_heuristically(content, "logic.cpp") == Language.cpp
    assert detect_language_heuristically(content, "script.py") == Language.python

def test_generic_filename_defaulting():
    # Ambiguous content with generic filename
    content = "x = 10"
    assert detect_language_heuristically(content, "left.py") == Language.python

def test_java_indicators():
    content = "System.out.println(\"test\");"
    assert detect_language_heuristically(content, "left.py") == Language.java

def test_cpp_indicators():
    content = "using namespace std;"
    assert detect_language_heuristically(content, "left.py") == Language.cpp

if __name__ == "__main__":
    # Run manually if pytest is not used
    test_detect_cpp_from_content()
    test_detect_java_from_content()
    print("All detection tests passed!")