
from core.follow_up_detector import FollowUpDetector


class ConversationTopicTracker:
    def __init__(self):
        self.detector = FollowUpDetector()
        self.current_topic = ""
        self.history = []
        self.topic_changes = 0

    def _extract_topic(self, message):
        text = message.strip().rstrip("?.!")

        prefixes = (
            "tell me about ",
            "explain ",
            "describe ",
            "what is ",
            "who is ",
            "teach me about ",
            "let's discuss "
        )

        lowered = text.lower()

        for prefix in prefixes:
            if lowered.startswith(prefix):
                topic = text[len(prefix):].strip()
                if topic:
                    return topic

        return ""

    def update(self, message):
        if not isinstance(message, str) or not message.strip():
            return {
                "updated": False,
                "topic": self.current_topic,
                "type": "uncertain",
                "reason": "Empty message"
            }

        detection = self.detector.detect(
            message,
            self.history
        )

        extracted_topic = self._extract_topic(message)

        if not self.current_topic:
            if extracted_topic:
                self.current_topic = extracted_topic
                result_type = "new_topic"
            else:
                result_type = "uncertain"

        elif detection["type"] == "follow_up":
            result_type = "follow_up"

        elif extracted_topic:
            if extracted_topic.lower() != self.current_topic.lower():
                self.current_topic = extracted_topic
                self.topic_changes += 1
                result_type = "new_topic"
            else:
                result_type = "same_topic"

        elif detection["type"] == "new_topic":
            result_type = "uncertain"

        else:
            result_type = "uncertain"

        self.history.append({
            "role": "user",
            "content": message
        })

        return {
            "updated": bool(extracted_topic),
            "topic": self.current_topic,
            "type": result_type,
            "topic_changes": self.topic_changes,
            "reason": detection["reason"]
        }

    def get_topic(self):
        return self.current_topic

    def clear(self):
        self.current_topic = ""
        self.history.clear()
        self.topic_changes = 0

