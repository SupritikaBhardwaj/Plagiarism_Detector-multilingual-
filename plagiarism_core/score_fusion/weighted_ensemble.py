class WeightedScoreFusion:
    """Explainable ensemble over heterogeneous similarity signals."""

    weights = {
        "text": 0.10,
        "token": 0.20,
        "ast": 0.20,
        "graph": 0.15,
        "semantic": 0.25,
        "stylometry": 0.05,
        "ai_generated_probability": 0.05,
    }

    def combine(self, breakdown: object) -> float:
        if hasattr(breakdown, "model_dump"):
            scores = breakdown.model_dump()
        elif isinstance(breakdown, dict):
            scores = breakdown
        else:
            scores = vars(breakdown)
        return round(sum(scores[name] * weight for name, weight in self.weights.items()), 4)
