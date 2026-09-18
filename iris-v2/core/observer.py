class ObservationEngine:
    def observe(self, result):
        if not result["success"]:
            return {
                "status": "failure",
                "message": result.get(
                    "message",
                    "Tool execution failed."
                )
            }

        tool_result = result.get("result")

        if isinstance(tool_result, list):
            if len(tool_result) == 0:
                return {
                    "status": "empty",
                    "message": "The tool returned no results."
                }

            return {
                "status": "success",
                "message": f"Found {len(tool_result)} result(s)."
            }

        if isinstance(tool_result, dict):
            return {
                "status": "success",
                "message": "Tool completed successfully."
            }

        if isinstance(tool_result, str):
            if not tool_result.strip():
                return {
                    "status": "empty",
                    "message": "The tool returned an empty result."
                }

            return {
                "status": "success",
                "message": "Tool completed successfully."
            }

        return {
            "status": "success",
            "message": "Tool completed successfully."
        }