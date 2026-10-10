
class ToolConfidenceScorer:
    def __init__(self, threshold=0.60):
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
            raise ValueError("Threshold must be a number.")

        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1.")

        self.threshold = float(threshold)

    def score(self, selected_tool, scores):
        if not isinstance(selected_tool, str) or not selected_tool.strip():
            return self._error("Selected tool must be a non-empty string.")

        if not isinstance(scores, dict) or not scores:
            return self._error("Scores must be a non-empty dictionary.")

        cleaned = {}

        for tool, value in scores.items():
            if not isinstance(tool, str) or not tool.strip():
                return self._error("Tool names must be non-empty strings.")

            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or value < 0
            ):
                return self._error("Scores must be non-negative numbers.")

            cleaned[tool] = float(value)

        selected_tool = selected_tool.strip()

        if selected_tool not in cleaned:
            return self._error("Selected tool is missing from scores.")

        total = sum(cleaned.values())

        if total <= 0:
            return {
                "valid": True,
                "tool": selected_tool,
                "confidence": 0.0,
                "threshold": self.threshold,
                "confident": False,
                "reason": "All candidate scores are zero."
            }

        confidence = cleaned[selected_tool] / total
        confidence = round(confidence, 4)

        return {
            "valid": True,
            "tool": selected_tool,
            "confidence": confidence,
            "threshold": self.threshold,
            "confident": confidence >= self.threshold,
            "reason": (
                "Selection meets the confidence threshold."
                if confidence >= self.threshold
                else "Selection is below the confidence threshold."
            )
        }

    def _error(self, reason):
        return {
            "valid": False,
            "tool": None,
            "confidence": 0.0,
            "threshold": self.threshold,
            "confident": False,
            "reason": reason
        }
