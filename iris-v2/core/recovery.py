
from core.tool_failure_classifier import ToolFailureClassifier


class RecoveryEngine:
    def __init__(self, max_retries=2, classifier=None):
        self.max_retries = max(0, max_retries)
        self.classifier = classifier or ToolFailureClassifier()

    def recover(self, execute_function, tool_name, arguments):
        attempts = 0

        while True:
            try:
                result = execute_function(tool_name, arguments)
            except Exception as error:
                result = {
                    "success": False,
                    "error": "execution_error",
                    "exception_type": type(error).__name__,
                    "message": str(error)
                }

            attempts += 1

            if not isinstance(result, dict):
                return {
                    "success": False,
                    "attempts": attempts,
                    "result": {
                        "success": False,
                        "error": "invalid_result",
                        "message": "Tool returned an invalid result."
                    }
                }

            if result.get("success") is True:
                return {
                    "success": True,
                    "attempts": attempts,
                    "result": result
                }

            failure = self.classifier.classify(result)

            if not failure["valid"] or not failure["retryable"]:
                return {
                    "success": False,
                    "attempts": attempts,
                    "result": result,
                    "failure": failure
                }

            if attempts > self.max_retries:
                return {
                    "success": False,
                    "attempts": attempts,
                    "result": result,
                    "failure": failure
                }
