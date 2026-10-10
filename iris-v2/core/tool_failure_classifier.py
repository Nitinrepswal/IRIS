
class ToolFailureClassifier:
    FAILURE_TYPES = {
        "tool_not_found",
        "missing_arguments",
        "invalid_arguments",
        "permission_denied",
        "file_not_found",
        "timeout",
        "connection_error",
        "execution_error",
        "unknown_error"
    }

    def classify(self, result):
        if not isinstance(result, dict):
            return self._failure(
                "invalid_result",
                "Tool result must be a dictionary."
            )

        if result.get("success") is True:
            return {
                "valid": True,
                "failed": False,
                "category": None,
                "message": "Tool executed successfully.",
                "retryable": False
            }

        error = result.get("error", "unknown_error")
        message = result.get("message", "")

        if not isinstance(error, str):
            error = "unknown_error"

        if not isinstance(message, str):
            message = ""

        error = error.strip().lower()
        message_lower = message.lower()

        if error == "tool_not_found":
            category = "tool_not_found"
        elif isinstance(result.get("missing_arguments"), list) and result["missing_arguments"]:
            category = "missing_arguments"
        elif error in {"missing_arguments", "missing_argument"}:
            category = "missing_arguments"
        elif error in {"invalid_arguments", "invalid_argument"}:
            category = "invalid_arguments"
        elif isinstance(result.get("exception_type"), str) and result["exception_type"] == "PermissionError":
            category = "permission_denied"
        elif error == "permission_denied" or "permission denied" in message_lower:
            category = "permission_denied"
        elif isinstance(result.get("exception_type"), str) and result["exception_type"] == "FileNotFoundError":
            category = "file_not_found"
        elif error == "file_not_found" or "no such file" in message_lower:
            category = "file_not_found"
        elif isinstance(result.get("exception_type"), str) and result["exception_type"] == "TimeoutError":
            category = "timeout"
        elif error in {"timeout", "timed_out"}:
            category = "timeout"
        elif isinstance(result.get("exception_type"), str) and result["exception_type"] == "ConnectionError":
            category = "connection_error"
        elif error in {"connection_error", "connection_failed"}:
            category = "connection_error"
        elif error == "execution_error":
            category = "execution_error"
        else:
            category = "unknown_error"

        retryable = category in {
            "timeout",
            "connection_error",
            "execution_error"
        }

        return {
            "valid": True,
            "failed": True,
            "category": category,
            "message": message or "The tool failed without an error message.",
            "retryable": retryable
        }

    def _failure(self, category, message):
        return {
            "valid": False,
            "failed": True,
            "category": category,
            "message": message,
            "retryable": False
        }
