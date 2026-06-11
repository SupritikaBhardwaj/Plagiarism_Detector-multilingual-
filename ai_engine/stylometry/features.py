import statistics


class StylometryAnalyzer:
    def compare(self, left: str, right: str) -> float:
        left_features = self.extract(left)
        right_features = self.extract(right)
        diffs = [abs(left_features[key] - right_features[key]) for key in left_features]
        return max(0.0, 1.0 - statistics.mean(diffs))

    def extract(self, source: str) -> dict[str, float]:
        lines = source.splitlines() or [""]
        lengths = [len(line) for line in lines]
        indent_counts = [len(line) - len(line.lstrip(" ")) for line in lines]
        snake_case = source.count("_") / max(len(source), 1)
        return {
            "avg_line_length": min(statistics.mean(lengths) / 120, 1.0),
            "avg_indent": min(statistics.mean(indent_counts) / 12, 1.0),
            "snake_case_density": min(snake_case * 20, 1.0),
        }

