
import re


class ReferenceResolver:
    def __init__(self):
        self.reference_words = {
            "it",
            "its",
            "they",
            "them",
            "their",
            "this",
            "that",
            "these",
            "those"
        }

    def _find_subject(self, message):
        text = message.strip().rstrip("?.!")
        patterns = [
            r"^(?:tell me about|explain|describe|what is|who is)\s+(.+)$",
            r"^(?:how does|how do)\s+(.+?)\s+(?:work|works|help|helps)$",
            r"^(?:show me|find|open|summarize)\s+(.+)$"
        ]

        for pattern in patterns:
            match = re.match(pattern, text, re.IGNORECASE)

            if match:
                subject = match.group(1).strip()
                if subject:
                    return subject

        return ""

    def resolve(self, message, history):
        if not isinstance(message, str) or not message.strip():
            return {
                "resolved": False,
                "message": message,
                "reference": "",
                "subject": "",
                "reason": "Empty message"
            }

        if not isinstance(history, list):
            raise ValueError("History must be a list")

        words = set(
            re.findall(r"\b[a-z]+\b", message.lower())
        )
        references = words.intersection(self.reference_words)

        if not references:
            return {
                "resolved": False,
                "message": message,
                "reference": "",
                "subject": "",
                "reason": "No supported reference found"
            }

        subject = ""

        for item in reversed(history):
            if not isinstance(item, dict):
                continue

            if item.get("role") != "user":
                continue

            content = item.get("content", "")

            if isinstance(content, str):
                subject = self._find_subject(content)

            if subject:
                break

        if not subject:
            return {
                "resolved": False,
                "message": message,
                "reference": sorted(references)[0],
                "subject": "",
                "reason": "Previous subject not found"
            }

        return {
            "resolved": True,
            "message": message,
            "reference": sorted(references)[0],
            "subject": subject,
            "resolved_message": message,
            "reason": "Previous subject identified"
        }

