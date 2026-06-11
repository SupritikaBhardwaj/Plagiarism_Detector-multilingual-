from compiler_engine.ast.ast_builder import ASTNode


def ast_similarity(left: ASTNode, right: ASTNode) -> float:
    left_kinds = _preorder(left)
    right_kinds = _preorder(right)
    overlap = len(set(left_kinds) & set(right_kinds))
    union = len(set(left_kinds) | set(right_kinds)) or 1
    shape_score = overlap / union
    size_penalty = 1 - abs(len(left_kinds) - len(right_kinds)) / max(len(left_kinds), len(right_kinds), 1)
    return max(0.0, min(1.0, (shape_score * 0.7) + (size_penalty * 0.3)))


def _preorder(node: ASTNode) -> list[str]:
    result = [node.kind]
    for child in node.children:
        result.extend(_preorder(child))
    return result

