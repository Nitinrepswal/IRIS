
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

        detection = self.detector.detect(message, self.history)
        extracted_topic = self._extract_topic(message)

        if not self.current_topic:
            if extracted_topic:
                self.current_topic = extracted_topic
                result_type = "new_topic"
            else:
                result_type = "uncertain"

        elif (
            extracted_topic
            and extracted_topic.lower() != self.current_topic.lower()
        ):
            self.current_topic = extracted_topic
            self.topic_changes += 1
            result_type = "new_topic"

        elif detection["type"] == "follow_up":
            result_type = "follow_up"

        elif extracted_topic:
            result_type = "same_topic"

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

    def export_state(self):
        return {
            "current_topic": self.current_topic,
            "history": [dict(item) for item in self.history],
            "topic_changes": self.topic_changes
        }

    def restore_state(self, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid topic tracker state")

        topic = data.get("current_topic", "")
        history = data.get("history", [])
        changes = data.get("topic_changes", 0)

        if not isinstance(topic, str):
            raise ValueError("Topic must be a string")

        if not isinstance(history, list):
            raise ValueError("Topic history must be a list")

        if type(changes) is not int or changes < 0:
            raise ValueError(
                "Topic changes must be a non-negative integer"
            )

        validated_history = []

        for item in history:
            if not isinstance(item, dict):
                raise ValueError("Invalid topic history entry")

            if item.get("role") != "user":
                raise ValueError(
                    "Topic history must contain user messages"
                )

            content = item.get("content")

            if not isinstance(content, str):
                raise ValueError(
                    "Topic history content must be a string"
                )

            validated_history.append({
                "role": "user",
                "content": content
            })

        self.current_topic = topic
        self.history = validated_history
        self.topic_changes = changes
