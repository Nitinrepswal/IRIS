
import re

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

    FAST_RULES = [
        (
            "memory",
            re.compile(
                r"\b(remember that|remember this|don't forget|"
                r"do you remember|what do you remember|"
                r"recall my|forget that|forget my|update my memory)\b",
                re.IGNORECASE
            )
        ),
        (
            "filesystem_search",
            re.compile(
                r"\b(find|search|list|locate)\b.{0,80}\b"
                r"(file|folder|directory|resume|document|notes)\b|"
                r"\b(read|open)\b.{0,80}\b"
                r"(file|resume|document|notes)\b",
                re.IGNORECASE
            )
        ),
        (
            "filesystem_edit",
            re.compile(
                r"\b(create|edit|modify|delete|rename)\b.{0,80}\b"
                r"(file|folder|directory|document|script)\b",
                re.IGNORECASE
            )
        ),
        (
            "terminal",
            re.compile(
                r"\b(run|execute)\b.{0,60}\b"
                r"(command|script|program|terminal|python|shell)\b",
                re.IGNORECASE
            )
        ),
        (
            "system",
            re.compile(
                r"\b(show|get|check|display)\b.{0,40}\b"
                r"(os version|system information|system info)\b",
                re.IGNORECASE
            )
        ),
        (
            "application",
            re.compile(
                r"\b(open|launch)\b.{0,40}\b"
                r"(calculator|calendar|notes app|text editor)\b",
                re.IGNORECASE
            )
        ),
        (
            "browser",
            re.compile(
                r"\b(search the web|search online|browse the web|"
                r"open this url|open this website|search the internet)\b",
                re.IGNORECASE
            )
        )
    ]

    def __init__(self, model):
        self.model = model
        self.registry = ToolCapabilityRegistry()

    def score_candidates(self, message, intent, suggested_tool=None):
        scores = {}
        preferred_tools = self.INTENT_TOOLS.get(intent, ["none"])
        message_words = set(
            message.lower().replace("?", "").replace(".", "").split()
        )

        for name in self.registry.list_tools():
            capability = self.registry.get(name)
            score = 0.0

            if name in preferred_tools:
                score += 50.0

            if name == suggested_tool:
                score += 40.0

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
                key=lambda item: (-item[1], item[0])
            )
        )

    def _fast_select(self, message, intent):
        text = message.strip()

        if intent == "chat" and re.fullmatch(
            r"(hi|hello|hey|good morning|good afternoon|good evening)"
            r"[!. ]*",
            text,
            re.IGNORECASE
        ):
            return "none", "Recognized a simple greeting."

        matches = [
            tool
            for tool, pattern in self.FAST_RULES
            if pattern.search(text)
        ]

        if len(matches) != 1:
            return None

        tool = matches[0]

        compatible_intents = {
            "memory": {"memory"},
            "filesystem_search": {"filesystem"},
            "filesystem_edit": {"filesystem"},
            "terminal": {"terminal"},
            "system": {"information"}
        }

        allowed_intents = compatible_intents.get(tool)

        if allowed_intents and intent not in allowed_intents:
            return None

        return tool, "Matched one unambiguous routing rule."

    def select(self, message, intent):
        if not isinstance(message, str) or not message.strip():
            return {
                "tool": "none",
                "reason": "No usable request was provided.",
                "scores": self.score_candidates("", intent),
                "route": "empty_input"
            }

        fast_result = self._fast_select(message, intent)

        if fast_result is not None:
            tool, reason = fast_result
            return {
                "tool": tool,
                "reason": reason,
                "scores": self.score_candidates(
                    message, intent, suggested_tool=tool
                ),
                "route": "fast"
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

            return {
                "tool": tool,
                "reason": reason,
                "scores": self.score_candidates(
                    message, intent, suggested_tool=tool
                ),
                "route": "model"
            }

        except Exception:
            return {
                "tool": "none",
                "reason": "Tool detection failed; no tool selected.",
                "scores": self.score_candidates(message, intent),
                "route": "fallback"
            }
