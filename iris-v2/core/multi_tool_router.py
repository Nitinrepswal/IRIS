
class MultiToolRouter:
    ALLOWED_TOOLS = {
        "filesystem_search",
        "file_reader",
        "file_editor",
        "terminal",
        "browser",
        "web_search",
        "llm"
    }

    def __init__(self, model):
        self.model = model

    def route(self, message):
        if not isinstance(message, str) or not message.strip():
            return self._error("Request must not be empty.")

        prompt = f"""
You are IRIS's multi-tool routing planner.

Break the user's request into the minimum necessary ordered steps.
Do not execute any tools.

Allowed tools:
- filesystem_search
- file_reader
- file_editor
- terminal
- browser
- web_search
- llm

Rules:
- Use one step for a single-tool request.
- Use multiple steps only when the request genuinely needs them.
- Each step must have an integer step number starting at 1.
- Each step must include action, target, and tool as strings.
- Mention dependencies only through explicit references such as "step 1".
- Do not invent file paths, commands, or user-provided content.
- If the request is unclear, return an empty steps list and a clarification question.
- Return JSON only.

User request:
{message}

Return:
{{
  "steps": [
    {{
      "step": 1,
      "action": "search",
      "target": "the user's requested target",
      "tool": "filesystem_search"
    }}
  ],
  "needs_clarification": false,
  "question": ""
}}
"""

        try:
            result = self.model.structured_chat([
                {"role": "user", "content": prompt}
            ])

            if not isinstance(result, dict):
                raise ValueError("Model result must be a dictionary.")

            steps = result.get("steps")
            needs_clarification = result.get("needs_clarification", False)
            question = result.get("question", "")

            if not isinstance(steps, list):
                raise ValueError("Steps must be a list.")

            if not isinstance(needs_clarification, bool):
                raise ValueError("Clarification flag must be a boolean.")

            if not isinstance(question, str):
                raise ValueError("Question must be a string.")

            if needs_clarification:
                if steps:
                    raise ValueError("Clarification plans must not contain steps.")

                return {
                    "valid": True,
                    "steps": [],
                    "needs_clarification": True,
                    "question": question or "Could you clarify your request?",
                    "reason": "The request needs clarification."
                }

            validated = []
            seen_steps = set()

            for step in steps:
                if not isinstance(step, dict):
                    raise ValueError("Each step must be a dictionary.")

                number = step.get("step")
                action = step.get("action")
                target = step.get("target")
                tool = step.get("tool")

                if (
                    not isinstance(number, int)
                    or isinstance(number, bool)
                    or number < 1
                ):
                    raise ValueError("Step number must be a positive integer.")

                if number in seen_steps:
                    raise ValueError("Duplicate step number.")

                if not all(
                    isinstance(value, str) and value.strip()
                    for value in (action, target, tool)
                ):
                    raise ValueError("Step fields must be non-empty strings.")

                if tool not in self.ALLOWED_TOOLS:
                    raise ValueError("Unsupported tool.")

                seen_steps.add(number)
                validated.append({
                    "step": number,
                    "action": action.strip(),
                    "target": target.strip(),
                    "tool": tool
                })

            if not validated:
                raise ValueError("A valid plan must contain at least one step.")

            validated.sort(key=lambda item: item["step"])

            if [item["step"] for item in validated] != list(
                range(1, len(validated) + 1)
            ):
                raise ValueError("Step numbers must be consecutive.")

            return {
                "valid": True,
                "steps": validated,
                "needs_clarification": False,
                "question": "",
                "reason": "Tool plan created. No tools were executed."
            }

        except Exception:
            return self._error(
                "Routing failed or returned an invalid plan."
            )

    def _error(self, reason):
        return {
            "valid": False,
            "steps": [],
            "needs_clarification": False,
            "question": "",
            "reason": reason
        }
