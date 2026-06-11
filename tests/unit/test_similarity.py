from compiler_engine.lexer.tokenizer import SourceTokenizer
from plagiarism_core.token_matching.text_similarity import lcs_similarity, normalized_levenshtein
from plagiarism_core.token_matching.winnowing import fingerprint_similarity, winnow


def test_text_similarity_detects_related_strings() -> None:
    assert normalized_levenshtein("abcdef", "abcxef") > 0.7
    assert lcs_similarity("abcdef", "abqdef") > 0.7


def test_winnowing_detects_renamed_variables() -> None:
    tokenizer = SourceTokenizer()
    left = tokenizer.tokenize("def add(a, b):\n    return a + b", "python")
    right = tokenizer.tokenize("def sum(x, y):\n    return x + y", "python")
    assert fingerprint_similarity(winnow(left, 3, 2), winnow(right, 3, 2)) > 0.4

