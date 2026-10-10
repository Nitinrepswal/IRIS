
import unittest

from core.ambiguity_handler import AmbiguityHandler


class TestAmbiguityHandler(unittest.TestCase):
    def setUp(self):
        self.handler = AmbiguityHandler()

    def test_clear_request(self):
        result = self.handler.analyze("Search for my resume")
        self.assertTrue(result["valid"])
        self.assertFalse(result["needs_clarification"])

    def test_vague_request(self):
        result = self.handler.analyze("Do it")
        self.assertTrue(result["needs_clarification"])
        self.assertEqual(result["reason"], "vague_request")

    def test_multiple_interpretations(self):
        result = self.handler.analyze(
            "Open my project",
            candidates=["Open the project folder", "Launch the project application"]
        )
        self.assertTrue(result["needs_clarification"])
        self.assertEqual(len(result["candidates"]), 2)

    def test_single_interpretation(self):
        result = self.handler.analyze(
            "Search for my resume",
            candidates=["Search the documents folder"]
        )
        self.assertFalse(result["needs_clarification"])

    def test_duplicate_interpretations(self):
        result = self.handler.analyze(
            "Open my project",
            candidates=["Open the folder", "Open the folder"]
        )
        self.assertFalse(result["needs_clarification"])

    def test_empty_request(self):
        result = self.handler.analyze("")
        self.assertFalse(result["valid"])
        self.assertTrue(result["needs_clarification"])

    def test_invalid_candidates(self):
        result = self.handler.analyze("Open my project", candidates="folder")
        self.assertFalse(result["valid"])

    def test_missing_context(self):
        result = self.handler.analyze("Fix this")
        self.assertTrue(result["needs_clarification"])
        self.assertEqual(result["reason"], "missing_context")

    def test_normalized_vague_phrase(self):
        result = self.handler.analyze("  MAKE   IT BETTER ")
        self.assertTrue(result["needs_clarification"])

    def test_no_candidates(self):
        result = self.handler.analyze("Explain machine learning")
        self.assertFalse(result["needs_clarification"])


if __name__ == "__main__":
    unittest.main()
