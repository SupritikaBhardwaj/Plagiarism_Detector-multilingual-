from compiler_engine.ast.ast_builder import ASTBuilder
from compiler_engine.cfg.builder import CFGBuilder
from compiler_engine.pdg.builder import PDGBuilder


def test_ast_cfg_pdg_are_constructed() -> None:
    ast = ASTBuilder().build("def f(x):\n    return x + 1\n", "python")
    cfg = CFGBuilder().build(ast)
    pdg = PDGBuilder().build(ast)
    assert ast.kind == "Module"
    assert len(cfg["nodes"]) > 0
    assert len(pdg["nodes"]) > 0

