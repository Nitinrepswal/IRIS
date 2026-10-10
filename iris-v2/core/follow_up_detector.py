
import re


class FollowUpDetector:
    def __init__(self):
        self.reference_words = {
            "it", "its", "they", "them", "their",
            "this", "that", "these", "those"
        }

        self.follow_up_phrases = {
            "what about",
            "tell me more",
            "explain more",
            "why is that",
            "how about",
            "and then",
            "what else",
            "go deeper"
        }

    def _words(self, message):
        return set(re.findall(r"\b[a-z]+\b", message.lower()))

    def _has_follow_up_phrase(self, message):
        text = message.lower().strip()
        return any(
            text.startswith(phrase)
            for phrase in self.follow_up_phrases
        )

    def detect(self, message, history):
        if not isinstance(message, str) or not message.strip():
            return {
                "type": "uncertain",
                "confidence": 0.0,
                "reason": "Empty message"
            }

        if not isinstance(history, list) or not history:
            return {
                "type": "uncertain",
                "confidence": 0.0,
                "reason": "No conversation history"
            }

        words = self._words(message)
        has_reference = bool(words.intersection(self.reference_words))
        has_phrase = self._has_follow_up_phrase(message)

        if has_reference or has_phrase:
            return {
                "type": "follow_up",
                "confidence": 0.8,
                "reason": "Follow-up wording detected"
            }

        if len(words) >= 3:
            return {
                "type": "new_topic",
                "confidence": 0.6,
                "reason": "No supported follow-up wording detected"
            }

        return {
            "type": "uncertain",
            "confidence": 0.3,
            "reason": "Message is too short to classify reliably"
        }

