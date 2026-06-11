from compiler_engine.ast.ast_builder import ASTBuilder, ASTNode


class ParserAdapter:
    """Facade for Tree-sitter/ANTLR/custom parser backends."""

    def __init__(self) -> None:
        self.ast_builder = ASTBuilder()

    def parse(self, source: str, language: str) -> ASTNode:
        return self.ast_builder.build(source, language)

