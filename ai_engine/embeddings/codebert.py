import hashlib
import math
import re


class CodeEmbeddingService:
    """CodeBERT adapter with a deterministic local fallback.

    In production, load `microsoft/codebert-base` or a SentenceTransformer model.
    The fallback keeps tests and demos fast without downloading large models.
    """

    def embed(self, source: str, dimensions: int = 64) -> list[float]:
        vector = [0.0] * dimensions
        tokens = re.findall(r"[A-Za-z_]\w*|\d+|[^\s]", source.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

