from compiler_engine.ast.ast_builder import ASTNode


class PDGBuilder:
    """Approximates a Program Dependence Graph from AST structure.

    A production parser would resolve definitions and uses precisely. This scaffold
    keeps the API stable and documents the compiler concept for extension.
    """

    def build(self, ast_root: ASTNode) -> dict:
        nodes: list[dict] = []
        edges: list[dict] = []

        def visit(node: ASTNode, control_parent: int | None = None) -> int:
            node_id = len(nodes)
            nodes.append({"id": node_id, "label": node.kind, "detail": node.value})
            if control_parent is not None:
                edges.append({"source": control_parent, "target": node_id, "type": "control-dependence"})
            for child in node.children:
                child_id = visit(child, node_id)
                if node.kind in {"Assign", "AnnAssign", "AugAssign"}:
                    edges.append({"source": node_id, "target": child_id, "type": "data-dependence"})
            return node_id

        visit(ast_root)
        return {"nodes": nodes, "edges": edges}
