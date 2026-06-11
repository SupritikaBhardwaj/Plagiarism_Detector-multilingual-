from compiler_engine.ast.ast_builder import ASTNode


class CFGBuilder:
    """Creates a compact control-flow graph for visualization and graph matching."""

    BRANCH_NODES = {"If", "IfExp", "While", "For", "AsyncFor", "Branch", "Loop"}

    def build(self, ast_root: ASTNode) -> dict:
        nodes: list[dict] = []
        edges: list[dict] = []

        def visit(node: ASTNode, parent_id: int | None = None) -> int:
            node_id = len(nodes)
            nodes.append({
                "id": node_id,
                "label": node.kind,
                "detail": node.value,
                "type": "branch" if node.kind in self.BRANCH_NODES else "statement",
            })
            if parent_id is not None:
                edges.append({"source": parent_id, "target": node_id, "type": "control"})
            for child in node.children:
                visit(child, node_id)
            return node_id

        visit(ast_root)
        return {"nodes": nodes, "edges": edges}
