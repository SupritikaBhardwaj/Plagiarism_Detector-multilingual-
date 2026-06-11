from compiler_engine.ast.ast_builder import ASTNode


class ThreeAddressGenerator:
    def generate(self, root: ASTNode) -> list[str]:
        instructions: list[str] = []

        def walk(node: ASTNode) -> None:
            if node.kind in {"Assign", "Return", "Call", "Statement"}:
                instructions.append(f"t{len(instructions)} = {node.kind}")
            for child in node.children:
                walk(child)

        walk(root)
        return instructions

