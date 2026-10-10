
import unittest

from core.recovery import RecoveryEngine


class TestAutomaticRecovery(unittest.TestCase):
    def setUp(self):
        self.engine = RecoveryEngine(max_retries=2)

    def test_success_first_attempt(self):
        def execute(tool, arguments):
            return {"success": True, "result": "done"}

        result = self.engine.recover(execute, "demo", {})

        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 1)

    def test_retry_then_success(self):
        calls = {"count": 0}

        def execute(tool, arguments):
            calls["count"] += 1

            if calls["count"] == 1:
                return {
                    "success": False,
                    "error": "timeout",
                    "message": "Timed out"
                }

            return {"success": True, "result": "recovered"}

        result = self.engine.recover(execute, "demo", {})

        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 2)

    def test_non_retryable_failure_stops(self):
        calls = {"count": 0}

        def execute(tool, arguments):
            calls["count"] += 1
            return {
                "success": False,
                "error": "tool_not_found",
                "message": "Tool not found"
            }

        result = self.engine.recover(execute, "missing", {})

        self.assertFalse(result["success"])
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(calls["count"], 1)

    def test_retries_exhausted(self):
        calls = {"count": 0}

        def execute(tool, arguments):
            calls["count"] += 1
            return {
                "success": False,
                "error": "connection_error",
                "message": "Connection failed"
            }

        result = self.engine.recover(execute, "demo", {})

        self.assertFalse(result["success"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(calls["count"], 3)

    def test_exception_recovery(self):
        calls = {"count": 0}

        def execute(tool, arguments):
            calls["count"] += 1

            if calls["count"] == 1:
                raise TimeoutError("Temporary timeout")

            return {"success": True, "result": "recovered"}

        result = self.engine.recover(execute, "demo", {})

        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 2)

    def test_invalid_result_stops(self):
        result = self.engine.recover(
            lambda tool, arguments: "invalid",
            "demo",
            {}
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["attempts"], 1)

    def test_zero_retries(self):
        engine = RecoveryEngine(max_retries=0)
        calls = {"count": 0}

        def execute(tool, arguments):
            calls["count"] += 1
            return {
                "success": False,
                "error": "timeout",
                "message": "Timed out"
            }

        result = engine.recover(execute, "demo", {})

        self.assertFalse(result["success"])
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(calls["count"], 1)


if __name__ == "__main__":
    unittest.main()
