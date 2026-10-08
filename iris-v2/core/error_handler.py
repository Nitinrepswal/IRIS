import traceback
from datetime import datetime


class ErrorHandler:
    def __init__(self, logger=None):
        self.logger = logger
        self.errors = []

    def handle(self, error, context=""):
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "type": type(error).__name__,
            "message": str(error)
        }

        self.errors.append(error_entry)

        if self.logger is not None:
            try:
                self.logger.log(
                    "ERROR",
                    error_entry
                )
            except Exception:
                pass

        return {
            "success": False,
            "message": self.user_message(error),
            "error_type": type(error).__name__
        }

    def user_message(self, error):
        if isinstance(error, TimeoutError):
            return "IRIS timed out while performing that operation."

        if isinstance(error, FileNotFoundError):
            return "IRIS could not find the requested file."

        if isinstance(error, PermissionError):
            return "IRIS does not have permission to perform that action."

        if isinstance(error, ConnectionError):
            return "IRIS could not connect to the required service."

        return "IRIS encountered an unexpected error while performing that operation."

    def get_errors(self):
        return self.errors.copy()

    def clear(self):
        self.errors.clear()

    def format_traceback(self, error):
        return "".join(
            traceback.format_exception(
                type(error),
                error,
                error.__traceback__
            )
        )