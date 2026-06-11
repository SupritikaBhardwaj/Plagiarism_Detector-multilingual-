import ast
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    kind: str
    value: str | None = None
    children: list["ASTNode"] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "value": self.value,
            "children": [child.to_dict() for child in self.children],
        }


class ASTBuilder:
    """Builds language-neutral AST shapes from real parsers or fallback grammars."""

    def build(self, source: str, language: str) -> ASTNode:
        if language == "python":
            try:
                return self._from_python_ast(ast.parse(source))
            except SyntaxError:
                pass
        return self._fallback_tree(source)

    def _from_python_ast(self, node: ast.AST) -> ASTNode:
        current = ASTNode(type(node).__name__)
        for child in ast.iter_child_nodes(node):
            current.children.append(self._from_python_ast(child))
        return current

    def _fallback_tree(self, source: str) -> ASTNode:
        root = ASTNode("Program")
        for line_number, line in enumerate(source.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue
            kind = self._classify_statement(stripped)
            root.children.append(ASTNode(kind, f"line {line_number}"))
        return root

    def _classify_statement(self, statement: str) -> str:
        if re.match(r"#\s*include\b|import\b", statement):
            return "Include"
        if re.search(r"\b(def|function)\s+\w+\s*\(|\b\w+\s+\w+\s*\([^;]*\)\s*\{?", statement):
            return "Function"
        if re.match(r"(for|while)\b", statement):
            return "Loop"
        if re.match(r"(if|else if|switch)\b", statement):
            return "Branch"
        if re.match(r"return\b", statement):
            return "Return"
        if re.search(r"\b(printf|scanf|cout|cin|System\.out\.println)\b", statement):
            return "Call"
        if re.match(r"(int|float|double|char|long|short|bool|string|auto|const)\b", statement):
            return "Declaration"
        if "=" in statement:
            return "Assignment"
        return "Statement"
