
class ToolArgumentGenerator:
    TOOL_ARGUMENTS = {
        "filesystem_search": ["directory", "query"],
        "file_editor": ["path", "content"],
        "file_reader": ["path"],
        "terminal": ["command"]
    }

    def __init__(self, model):
        self.model = model

    def generate(self, message, tool):
        if not isinstance(message, str) or not message.strip():
            return self._error(tool, "Request must not be empty.")

        if not isinstance(tool, str) or tool not in self.TOOL_ARGUMENTS:
            return self._error(tool, "Unsupported tool.")

        required = self.TOOL_ARGUMENTS[tool]

        prompt = f"""
You extract arguments for an IRIS tool.
Do not execute any tools or commands.

SUPPORTED ARGUMENTS:
filesystem_search: directory, query
file_editor: path, content
file_reader: path
terminal: command

RULES:
- Extract only arguments for the selected tool.
- Do not invent filenames, paths, content, or commands.
- If information is missing, use an empty string for that value.
- Include every required argument.
- All argument values must be strings.
- Do not add unsupported arguments.
- Return only valid JSON.

Selected tool: {tool}
Required arguments: {required}

User request:
{message}

Return this structure:
{{
    "tool": "{tool}",
    "arguments": {{}},
    "reason": "brief explanation"
}}
"""

        try:
            result = self.model.structured_chat([
                {
                    "role": "user",
                    "content": prompt
                }
            ])

            if not isinstance(result, dict):
                raise ValueError("Model response must be a dictionary.")

            if result.get("tool") != tool:
                raise ValueError("Response tool does not match request.")

            arguments = result.get("arguments")

            if not isinstance(arguments, dict):
                raise ValueError("Arguments must be a dictionary.")

            if any(key not in required for key in arguments):
                raise ValueError("Unexpected argument returned.")

            cleaned = {}

            for key in required:
                value = arguments.get(key, "")

                if not isinstance(value, str):
                    raise ValueError(
                        "Argument values must be strings."
                    )

                cleaned[key] = value.strip()

            # Resolve explicit references to the current directory.
            if tool == "filesystem_search":
                message_lower = message.lower()

                if (
                    "current directory" in message_lower
                    or "current folder" in message_lower
                    or "this folder" in message_lower
                ):
                    cleaned["directory"] = "."

            reason = result.get("reason", "")

            if not isinstance(reason, str):
                reason = ""

            missing = [
                key
                for key, value in cleaned.items()
                if not value
            ]

            return {
                "tool": tool,
                "arguments": cleaned,
                "reason": reason,
                "missing_arguments": missing,
                "valid": not missing
            }

        except Exception:
            return self._error(
                tool,
                "Argument extraction failed; review the request and try again."
            )

    def _error(self, tool, reason):
        return {
            "tool": tool if isinstance(tool, str) else "none",
            "arguments": {},
            "reason": reason,
            "missing_arguments": [],
            "valid": False
        }
