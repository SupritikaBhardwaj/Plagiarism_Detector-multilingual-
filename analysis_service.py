from uuid import uuid4

from ai_engine.classifiers.ai_generated import AIGeneratedDetector
from ai_engine.embeddings.codebert import CodeEmbeddingService
from ai_engine.stylometry.features import StylometryAnalyzer
from backend.models.schemas import AnalysisReport, AnalysisRequest, EvidenceItem, SimilarityBreakdown
from compiler_engine.ast.ast_builder import ASTBuilder
from compiler_engine.cfg.builder import CFGBuilder
from compiler_engine.lexer.tokenizer import SourceTokenizer
from compiler_engine.pdg.builder import PDGBuilder
from compiler_engine.semantic_analysis.symbol_table import SymbolTableBuilder
from plagiarism_core.graph_matching.graph_similarity import graph_similarity
from plagiarism_core.score_fusion.weighted_ensemble import WeightedScoreFusion
from plagiarism_core.semantic_similarity.embedding_similarity import cosine_similarity
from plagiarism_core.token_matching.text_similarity import lcs_similarity, normalized_levenshtein
from plagiarism_core.token_matching.winnowing import fingerprint_similarity, winnow
from plagiarism_core.tree_similarity.tree_edit import ast_similarity


class AnalysisService:
    def __init__(self) -> None:
        self.tokenizer = SourceTokenizer()
        self.ast_builder = ASTBuilder()
        self.cfg_builder = CFGBuilder()
        self.pdg_builder = PDGBuilder()
        self.symbols = SymbolTableBuilder()
        self.embeddings = CodeEmbeddingService()
        self.stylometry = StylometryAnalyzer()
        self.ai_detector = AIGeneratedDetector()
        self.fusion = WeightedScoreFusion()

    async def compare(self, request: AnalysisRequest) -> AnalysisReport:
        left_tokens = self.tokenizer.tokenize(request.left.content, request.left.language.value)
        right_tokens = self.tokenizer.tokenize(request.right.content, request.right.language.value)

        left_ast = self.ast_builder.build(request.left.content, request.left.language.value)
        right_ast = self.ast_builder.build(request.right.content, request.right.language.value)
        
        # Optional structural analysis: wrap in try-except to avoid total failure on fallback ASTs
        left_cfg, right_cfg = {}, {}
        left_pdg, right_pdg = {}, {}
        graph_score = 0.0
        
        try:
            left_cfg = self.cfg_builder.build(left_ast)
            right_cfg = self.cfg_builder.build(right_ast)
            left_pdg = self.pdg_builder.build(left_ast)
            right_pdg = self.pdg_builder.build(right_ast)
            graph_score = (graph_similarity(left_cfg, right_cfg) + graph_similarity(left_pdg, right_pdg)) / 2
        except Exception:
            # Structural analysis is currently most stable for Python; 
            # other languages using fallback trees may skip this step.
            pass

        text_score = (normalized_levenshtein(request.left.content, request.right.content) + lcs_similarity(request.left.content, request.right.content)) / 2
        token_score = fingerprint_similarity(winnow(left_tokens), winnow(right_tokens))
        tree_score = ast_similarity(left_ast, right_ast)

        left_vec = self.embeddings.embed(request.left.content)
        right_vec = self.embeddings.embed(request.right.content)
        semantic_score = cosine_similarity(left_vec, right_vec)
        style_score = self.stylometry.compare(request.left.content, request.right.content)
        ai_probability = max(
            self.ai_detector.predict_probability(request.left.content),
            self.ai_detector.predict_probability(request.right.content),
        )

        breakdown = SimilarityBreakdown(
            text=text_score,
            token=token_score,
            ast=tree_score,
            graph=graph_score,
            semantic=semantic_score,
            stylometry=style_score,
            ai_generated_probability=ai_probability,
        )
        overall = self.fusion.combine(breakdown)
        evidence = self._build_evidence(breakdown)

        return AnalysisReport(
            report_id=str(uuid4()),
            overall_similarity=overall,
            risk_level=self._risk_level(overall),
            breakdown=breakdown,
            evidence=evidence,
            highlighted_regions=self._highlight_regions(request.left.content, request.right.content),
            ast={"left": left_ast.to_dict(), "right": right_ast.to_dict()},
            cfg={"left": left_cfg, "right": right_cfg},
            pdg={"left": left_pdg, "right": right_pdg},
        )

    def _risk_level(self, score: float) -> str:
        if score >= 0.8:
            return "critical"
        if score >= 0.6:
            return "high"
        if score >= 0.4:
            return "medium"
        return "low"

    def _build_evidence(self, breakdown: SimilarityBreakdown) -> list[EvidenceItem]:
        items: list[EvidenceItem] = []
        if breakdown.token > 0.7:
            items.append(EvidenceItem(kind="token", message="High token fingerprint overlap indicates possible copied structure.", confidence=breakdown.token))
        if breakdown.ast > 0.65:
            items.append(EvidenceItem(kind="ast", message="AST shape similarity suggests variable renaming or formatting changes.", confidence=breakdown.ast))
        if breakdown.graph > 0.6:
            items.append(EvidenceItem(kind="graph", message="Control/dependence graph similarity suggests algorithm-level overlap.", confidence=breakdown.graph))
        if breakdown.semantic > 0.7:
            items.append(EvidenceItem(kind="semantic", message="Embedding similarity indicates semantic equivalence beyond syntax.", confidence=breakdown.semantic))
        if breakdown.ai_generated_probability > 0.65:
            items.append(EvidenceItem(kind="ai", message="One or both submissions exhibit AI-generated code patterns.", confidence=breakdown.ai_generated_probability))
        return items

    def _highlight_regions(self, left: str, right: str) -> list[dict]:
        left_lines = left.splitlines()
        right_lines = set(line.strip() for line in right.splitlines() if line.strip())
        return [
            {"side": "left", "line": index + 1, "text": line, "reason": "Exact normalized line match"}
            for index, line in enumerate(left_lines)
            if line.strip() in right_lines
        ]
