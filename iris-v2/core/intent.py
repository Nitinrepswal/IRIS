
class IntentDetector:
    ALLOWED_INTENTS = {
        "chat",
        "information",
        "filesystem",
        "memory",
        "terminal"
    }

    def __init__(self, model):
        self.model = model

    def detect(self, message):
        if not isinstance(message, str) or not message.strip():
            return {
                "intent": "chat",
                "reason": "Empty or invalid message.",
                "confidence": 0.0
            }

        prompt = f"""
You are IRIS's intent classifier.

Classify the user's request into exactly ONE intent.

INTENTS:
- chat: greetings, casual conversation, or direct conversation with IRIS.
- information: questions asking for facts, explanations, definitions, or general knowledge.
- filesystem: finding, reading, creating, editing, or locating files.
- memory: remembering, recalling, correcting, or forgetting personal information.
- terminal: running commands, scripts, or programs.

DECISION RULES:
- Classify the requested action, not just individual keywords.
- Requests to remember or recall personal details use memory.
- Requests to locate or read files use filesystem.
- Requests to execute a command or script use terminal.
- Questions seeking general knowledge use information.
- Greetings and ordinary conversation use chat.
- If a request is ambiguous, choose the most likely intent and lower confidence.
- Do not invent a new intent category.

EXAMPLES:
"Hi IRIS" -> chat
"What is an operating system?" -> information
"Find my Python project" -> filesystem
"Forget my old preference" -> memory
"Run app.py" -> terminal
"Explain this code" -> information
"Open my notes file" -> filesystem
"Remember my project deadline" -> memory

Return ONLY valid JSON:
{{
    "intent": "chat | information | filesystem | memory | terminal",
    "reason": "brief explanation",
    "confidence": 0.0
}}

Confidence must be a number between 0.0 and 1.0.

User request:
{message}
"""

        try:
            result = self.model.structured_chat([
                {
                    "role": "user",
                    "content": prompt
                }
            ])

            if not isinstance(result, dict):
                raise ValueError("Model result must be a dictionary.")

            intent = result.get("intent")

            if not isinstance(intent, str):
                raise ValueError("Missing intent.")

            intent = intent.strip().lower()

            if intent not in self.ALLOWED_INTENTS:
                raise ValueError("Unknown intent.")

            reason = result.get("reason", "")
            confidence = result.get("confidence", 0.5)

            if not isinstance(reason, str):
                reason = ""

            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = 0.5

            confidence = max(0.0, min(1.0, confidence))

            return {
                "intent": intent,
                "reason": reason,
                "confidence": confidence
            }

        except Exception:
            return {
                "intent": "information",
                "reason": "Classification failed; using safe fallback.",
                "confidence": 0.0
            }
