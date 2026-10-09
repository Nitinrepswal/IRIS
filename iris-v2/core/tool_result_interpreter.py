
class ToolResultInterpreter:
    def __init__(self, model=None):
        self.model = model

    def interpret(self, tool_name, result):
        if not isinstance(tool_name, str) or not tool_name.strip():
            return self._error("Tool name must be a non-empty string.")

        if not isinstance(result, dict):
            return self._error("Tool result must be a dictionary.")

        success = result.get("success")

        if not isinstance(success, bool):
            return self._error("Tool result must contain a boolean success field.")

        if not success:
            message = result.get("message", "Tool execution failed.")
            error = result.get("error", "unknown_error")

            if not isinstance(message, str):
                message = "Tool execution failed."

            if not isinstance(error, str):
                error = "unknown_error"

            return {
                "valid": True,
                "success": False,
                "tool": tool_name,
                "summary": message,
                "data": None,
                "error": error,
                "retry": result.get("retry", False),
                "reason": "The tool reported a failure."
            }

        data = result.get("result")

        if self.model is None:
            return {
                "valid": True,
                "success": True,
                "tool": tool_name,
                "summary": self._summarize(data),
                "data": data,
                "error": None,
                "retry": False,
                "reason": "Tool result normalized without an LLM."
            }

        try:
            response = self.model.structured_chat([
                {
                    "role": "user",
                    "content": f"""
Interpret this tool result for IRIS.

Tool: {tool_name}
Result data: {data!r}

Rules:
- Describe only what the result supports.
- Do not invent facts or claim unperformed actions.
- If the result is empty, say that no data was returned.
- Keep the summary concise.

Return only valid JSON:
{{
    "summary": "concise interpretation"
}}
"""
                }
            ])

            if not isinstance(response, dict):
                raise ValueError("Model response must be a dictionary.")

            summary = response.get("summary")

            if not isinstance(summary, str) or not summary.strip():
                raise ValueError("Missing interpretation summary.")

            summary = summary.strip()

        except Exception:
            summary = self._summarize(data)

        return {
            "valid": True,
            "success": True,
            "tool": tool_name,
            "summary": summary,
            "data": data,
            "error": None,
            "retry": False,
            "reason": "Tool result interpreted."
        }

    def _summarize(self, data):
        if data is None:
            return "The tool returned no data."

        if isinstance(data, str):
            return data if data else "The tool returned an empty string."

        if isinstance(data, (list, tuple, set)):
            if not data:
                return "The tool returned an empty collection."
            return f"The tool returned {len(data)} item(s)."

        if isinstance(data, dict):
            if not data:
                return "The tool returned an empty dictionary."
            return f"The tool returned {len(data)} field(s)."

        return f"The tool returned data of type {type(data).__name__}."

    def _error(self, reason):
        return {
            "valid": False,
            "success": False,
            "tool": None,
            "summary": "",
            "data": None,
            "error": "invalid_result",
            "retry": False,
            "reason": reason
        }
