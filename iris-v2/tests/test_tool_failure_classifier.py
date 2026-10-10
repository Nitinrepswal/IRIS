
import unittest

from core.tool_failure_classifier import ToolFailureClassifier


class TestToolFailureClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = ToolFailureClassifier()

    def test_success(self):
        result = self.classifier.classify({"success": True})
        self.assertFalse(result["failed"])
        self.assertIsNone(result["category"])

    def test_tool_not_found(self):
        result = self.classifier.classify({
            "success": False,
            "error": "tool_not_found",
            "message": "Tool not found"
        })
        self.assertEqual(result["category"], "tool_not_found")
        self.assertFalse(result["retryable"])

    def test_missing_arguments(self):
        result = self.classifier.classify({
            "success": False,
            "error": "missing_arguments"
        })
        self.assertEqual(result["category"], "missing_arguments")

    def test_invalid_arguments(self):
        result = self.classifier.classify({
            "success": False,
            "error": "invalid_arguments"
        })
        self.assertEqual(result["category"], "invalid_arguments")

    def test_permission_denied(self):
        result = self.classifier.classify({
            "success": False,
            "exception_type": "PermissionError",
            "message": "Access denied"
        })
        self.assertEqual(result["category"], "permission_denied")
        self.assertFalse(result["retryable"])

    def test_file_not_found(self):
        result = self.classifier.classify({
            "success": False,
            "exception_type": "FileNotFoundError",
            "message": "File not found"
        })
        self.assertEqual(result["category"], "file_not_found")

    def test_timeout_is_retryable(self):
        result = self.classifier.classify({
            "success": False,
            "exception_type": "TimeoutError",
            "message": "Operation timed out"
        })
        self.assertEqual(result["category"], "timeout")
        self.assertTrue(result["retryable"])

    def test_connection_error_is_retryable(self):
        result = self.classifier.classify({
            "success": False,
            "error": "connection_error"
        })
        self.assertEqual(result["category"], "connection_error")
        self.assertTrue(result["retryable"])

    def test_execution_error_is_retryable(self):
        result = self.classifier.classify({
            "success": False,
            "error": "execution_error",
            "message": "Unexpected failure"
        })
        self.assertEqual(result["category"], "execution_error")
        self.assertTrue(result["retryable"])

    def test_unknown_error(self):
        result = self.classifier.classify({
            "success": False,
            "error": "some_new_error"
        })
        self.assertEqual(result["category"], "unknown_error")
        self.assertFalse(result["retryable"])

    def test_invalid_result(self):
        result = self.classifier.classify("invalid")
        self.assertFalse(result["valid"])
        self.assertEqual(result["category"], "invalid_result")


if __name__ == "__main__":
    unittest.main()
