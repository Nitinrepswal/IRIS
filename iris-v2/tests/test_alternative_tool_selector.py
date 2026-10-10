
import unittest

from core.alternative_tool_selector import AlternativeToolSelector


class TestAlternativeToolSelector(unittest.TestCase):
    def setUp(self):
        self.selector = AlternativeToolSelector()

    def test_filesystem_search_alternative(self):
        result = self.selector.select(
            "filesystem_search",
            "timeout"
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["alternative"], "browser")
        self.assertFalse(result["execute"])

    def test_terminal_alternative(self):
        result = self.selector.select(
            "terminal",
            "connection_error"
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["alternative"], "browser")

    def test_permission_failure_stops_fallback(self):
        result = self.selector.select(
            "filesystem_edit",
            "permission_denied"
        )
        self.assertIsNone(result["alternative"])

    def test_invalid_arguments_stop_fallback(self):
        result = self.selector.select(
            "filesystem_search",
            "invalid_arguments"
        )
        self.assertIsNone(result["alternative"])

    def test_unknown_failure_stops_fallback(self):
        result = self.selector.select(
            "terminal",
            "unknown_error"
        )
        self.assertIsNone(result["alternative"])

    def test_unavailable_alternative(self):
        result = self.selector.select(
            "filesystem_search",
            "timeout",
            available_tools=["none", "filesystem_search"]
        )
        self.assertIsNone(result["alternative"])

    def test_unknown_failure_category(self):
        result = self.selector.select(
            "terminal",
            "brand_new_error"
        )
        self.assertFalse(result["valid"])

    def test_invalid_tool_name(self):
        result = self.selector.select("", "timeout")
        self.assertFalse(result["valid"])

    def test_invalid_available_tools(self):
        result = self.selector.select(
            "terminal",
            "timeout",
            available_tools="browser"
        )
        self.assertFalse(result["valid"])

    def test_no_fallback_for_memory(self):
        result = self.selector.select(
            "memory",
            "timeout"
        )
        self.assertIsNone(result["alternative"])


if __name__ == "__main__":
    unittest.main()
