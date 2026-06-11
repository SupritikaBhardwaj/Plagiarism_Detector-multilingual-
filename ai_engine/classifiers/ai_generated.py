import re


class AIGeneratedDetector:
    """Heuristic classifier placeholder for an explainable AI-code detector."""

    MARKERS = [
        "as an ai",
        "generated",
        "helper function",
        "edge case",
        "time complexity",
        "space complexity",
    ]

    def predict_probability(self, source: str) -> float:
        lowered = source.lower()
        marker_score = sum(marker in lowered for marker in self.MARKERS) / len(self.MARKERS)
        comment_density = len(re.findall(r"#|//|/\*", source)) / max(len(source.splitlines()), 1)
        regularity = 1.0 if self._line_lengths_are_regular(source) else 0.2
        return max(0.0, min(1.0, (marker_score * 0.5) + (comment_density * 0.2) + (regularity * 0.3)))

    def _line_lengths_are_regular(self, source: str) -> bool:
        lengths = [len(line.strip()) for line in source.splitlines() if line.strip()]
        return len(lengths) > 4 and (max(lengths) - min(lengths)) < 60

