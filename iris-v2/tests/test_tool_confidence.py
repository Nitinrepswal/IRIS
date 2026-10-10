
import unittest

from core.tool_confidence import ToolConfidenceScorer


class TestToolConfidenceScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ToolConfidenceScorer()

    def test_high_confidence(self):
        result = self.scorer.score(
            "browser",
            {"browser": 90, "none": 10}
        )
        self.assertTrue(result["confident"])
        self.assertEqual(result["confidence"], 0.9)

    def test_low_confidence(self):
        result = self.scorer.score(
            "browser",
            {"browser": 40, "none": 60}
        )
        self.assertFalse(result["confident"])
        self.assertEqual(result["confidence"], 0.4)

    def test_equal_scores(self):
        result = self.scorer.score(
            "browser",
            {"browser": 50, "none": 50}
        )
        self.assertEqual(result["confidence"], 0.5)

    def test_all_zero_scores(self):
        result = self.scorer.score(
            "browser",
            {"browser": 0, "none": 0}
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["confidence"], 0.0)
        self.assertFalse(result["confident"])

    def test_selected_tool_missing(self):
        result = self.scorer.score(
            "terminal",
            {"browser": 10}
        )
        self.assertFalse(result["valid"])

    def test_empty_scores(self):
        result = self.scorer.score("browser", {})
        self.assertFalse(result["valid"])

    def test_negative_score(self):
        result = self.scorer.score(
            "browser",
            {"browser": -1, "none": 2}
        )
        self.assertFalse(result["valid"])

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            ToolConfidenceScorer(threshold=1.5)

    def test_custom_threshold(self):
        scorer = ToolConfidenceScorer(threshold=0.8)
        result = scorer.score(
            "browser",
            {"browser": 70, "none": 30}
        )
        self.assertFalse(result["confident"])
        self.assertEqual(result["threshold"], 0.8)

    def test_invalid_score_type(self):
        result = self.scorer.score(
            "browser",
            {"browser": "high"}
        )
        self.assertFalse(result["valid"])


if __name__ == "__main__":
    unittest.main()
