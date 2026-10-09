
from core.tool_capabilities import ToolCapabilityRegistry


class ToolSelector:
    ALLOWED_TOOLS = {
        "none",
        "filesystem_search",
        "filesystem_edit",
        "memory",
        "terminal",
        "browser",
        "application",
        "system"
    }

    INTENT_TOOLS = {
        "chat": ["none"],
        "information": ["none", "browser", "system"],
        "filesystem": ["filesystem_search", "filesystem_edit"],
        "memory": ["memory"],
        "terminal": ["terminal"]
    }

    def __init__(self, model):
        self.model = model
        self.registry = ToolCapabilityRegistry()

    def score_candidates(self, message, intent, suggested_tool=None):
        scores = {}

        preferred_tools = self.INTENT_TOOLS.get(
            intent,
            ["none"]
        )

        for name in self.registry.list_tools():
            capability = self.registry.get(name)

            score = 0.0

            if name in preferred_tools:
                score += 50.0

            if name == suggested_tool:
                score += 40.0

            message_words = set(
                message.lower().replace("?", "").replace(".", "").split()
            )

            action_matches = 0

            for action in capability["actions"]:
                action_words = set(action.lower().split())
                if action_words and action_words.issubset(message_words):
                    action_matches += 1

            score += min(action_matches * 10.0, 20.0)

            if capability["risk"] == "high":
                score -= 10.0
            elif capability["risk"] == "medium":
                score -= 3.0

            if capability["requires_confirmation"]:
                score -= 5.0

            scores[name] = round(max(0.0, score), 2)

        return dict(
            sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    def select(self, message, intent):
        if not isinstance(message, str) or not message.strip():
            return {
                "tool": "none",
                "reason": "No usable request was provided.",
                "scores": self.score_candidates("", intent)
            }

        prompt = f"""
You are IRIS's natural-language tool detector.

Choose the single best tool for the user's request.

AVAILABLE TOOLS:
- none: conversation and general questions
- filesystem_search: find, search, list, or read files
- filesystem_edit: create, edit, modify, or delete files
- memory: remember, recall, update, or forget personal information
- terminal: run commands, programs, or scripts
- browser: search the web or open webpages
- application: open or control supported applications
- system: retrieve operating system information

RULES:
- Choose based on the requested action.
- Do not claim to execute a tool.
- Do not choose a tool outside the available list.
- For ambiguous requests, choose none.
- Prefer filesystem_search for locating files.
- Prefer filesystem_edit for modifying files.
- Prefer memory for personal memory requests.
- Prefer terminal for explicitly running commands.

Detected intent: {intent}

User request:
{message}

Return ONLY valid JSON:
{{
    "tool": "none | filesystem_search | filesystem_edit | memory | terminal | browser | application | system",
    "reason": "brief explanation"
}}
"""

        try:
            result = self.model.structured_chat([
                {"role": "user", "content": prompt}
            ])

            if not isinstance(result, dict):
                raise ValueError("Model result must be a dictionary.")

            tool = result.get("tool")

            if not isinstance(tool, str):
                raise ValueError("Missing tool.")

            tool = tool.strip().lower()

            if tool not in self.ALLOWED_TOOLS:
                raise ValueError("Unknown tool.")

            reason = result.get("reason", "")
            if not isinstance(reason, str):
                reason = ""

            scores = self.score_candidates(
                message,
                intent,
                suggested_tool=tool
            )

            return {
                "tool": tool,
                "reason": reason,
                "scores": scores
            }

        except Exception:
            scores = self.score_candidates(message, intent)

            return {
                "tool": "none",
                "reason": "Tool detection failed; no tool selected.",
                "scores": scores
            }
