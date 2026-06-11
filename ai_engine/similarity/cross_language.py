from ai_engine.embeddings.codebert import CodeEmbeddingService
from plagiarism_core.semantic_similarity.embedding_similarity import cosine_similarity


class CrossLanguageSimilarity:
    def __init__(self) -> None:
        self.embeddings = CodeEmbeddingService()

    def compare(self, left: str, right: str) -> float:
        return cosine_similarity(self.embeddings.embed(left), self.embeddings.embed(right))

