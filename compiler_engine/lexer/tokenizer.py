import io
import re
import tokenize
from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedToken:
    type: str
    value: str
    line: int
    column: int


class SourceTokenizer:
    """Normalizes lexical tokens so superficial edits become comparable."""

    KEYWORDS = {
        "if", "else", "for", "while", "return", "def", "class", "int", "float",
        "void", "public", "private", "static", "function", "const", "let", "var",
    }

    def tokenize(self, source: str, language: str) -> list[str]:
        if language == "python":
            return [token.value for token in self._python_tokens(source)]
        return [token.value for token in self._generic_tokens(source)]

    def _python_tokens(self, source: str) -> list[NormalizedToken]:
        result: list[NormalizedToken] = []
        stream = io.StringIO(source)
        for token in tokenize.generate_tokens(stream.readline):
            token_type = tokenize.tok_name[token.type]
            if token_type in {"COMMENT", "NL", "NEWLINE", "INDENT", "DEDENT", "ENCODING", "ENDMARKER"}:
                continue
            value = self._normalize_value(token.string, token_type)
            result.append(NormalizedToken(token_type, value, token.start[0], token.start[1]))
        return result

    def _generic_tokens(self, source: str) -> list[NormalizedToken]:
        without_comments = re.sub(r"//.*?$|/\*.*?\*/|#.*?$", "", source, flags=re.MULTILINE | re.DOTALL)
        pieces = re.findall(r"[A-Za-z_]\w*|\d+(?:\.\d+)?|==|!=|<=|>=|&&|\|\||[^\s]", without_comments)
        tokens: list[NormalizedToken] = []
        for index, piece in enumerate(pieces):
            token_type = "KEYWORD" if piece in self.KEYWORDS else "IDENTIFIER" if re.match(r"[A-Za-z_]\w*$", piece) else "LITERAL" if piece[0].isdigit() else "SYMBOL"
            tokens.append(NormalizedToken(token_type, self._normalize_value(piece, token_type), 0, index))
        return tokens

    def _normalize_value(self, value: str, token_type: str) -> str:
        if token_type in {"NAME", "IDENTIFIER"} and value not in self.KEYWORDS:
            return "ID"
        if token_type in {"NUMBER", "STRING", "LITERAL"}:
            return "LIT"
        return value.strip()

