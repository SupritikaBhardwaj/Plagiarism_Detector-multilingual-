class ModelRegistry:
    models = {
        "codebert": "microsoft/codebert-base",
        "sentence_transformer": "sentence-transformers/all-MiniLM-L6-v2",
        "unixcoder": "microsoft/unixcoder-base",
    }

    def get(self, key: str) -> str:
        return self.models[key]

