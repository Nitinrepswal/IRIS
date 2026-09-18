class RecoveryEngine:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries

    def recover(self, execute_function, tool_name, arguments):
        attempts = 0

        while attempts <= self.max_retries:
            result = execute_function(
                tool_name,
                arguments
            )

            if result["success"]:
                return {
                    "success": True,
                    "attempts": attempts + 1,
                    "result": result
                }

            if not result.get("retry", False):
                return {
                    "success": False,
                    "attempts": attempts + 1,
                    "result": result
                }

            attempts += 1

        return {
            "success": False,
            "attempts": attempts,
            "result": result
        }