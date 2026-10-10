
from core.context_manager import ContextManager
from core.conversation_state import ConversationState
from core.reference_resolver import ReferenceResolver
from core.follow_up_detector import FollowUpDetector
from core.conversation_topic_tracker import ConversationTopicTracker


class ConversationIntelligence:
    def __init__(
        self,
        max_messages=20,
        max_characters=6000
    ):
        self.state = ConversationState()
        self.context_manager = ContextManager(
            max_messages=max_messages,
            max_characters=max_characters
        )
        self.reference_resolver = ReferenceResolver()
        self.follow_up_detector = FollowUpDetector()
        self.topic_tracker = ConversationTopicTracker()

    def add_user_message(self, message):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message cannot be empty")

        self.state.add_user_message(message)
        self.topic_tracker.update(message)

    def add_assistant_message(self, message):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Response cannot be empty")

        self.state.add_assistant_message(message)

    def set_topic(self, topic):
        if not isinstance(topic, str):
            raise ValueError("Topic must be a string")

        self.state.set_topic(topic.strip())

    def analyze_message(self, message):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message cannot be empty")

        history = self.state.get_messages()

        follow_up = self.follow_up_detector.detect(
            message,
            history
        )

        reference = self.reference_resolver.resolve(
            message,
            history
        )

        tracked_messages = self.topic_tracker.history
        already_tracked = (
            tracked_messages
            and tracked_messages[-1]["content"] == message
        )

        if not already_tracked:
            topic = self.topic_tracker.update(message)
        else:
            topic = {
                "updated": False,
                "topic": self.topic_tracker.get_topic(),
                "type": "already_tracked",
                "topic_changes": self.topic_tracker.topic_changes,
                "reason": "Message was already tracked"
            }

        return {
            "follow_up": follow_up,
            "reference": reference,
            "topic": topic,
            "current_topic": self.topic_tracker.get_topic()
        }

    def get_context(self):
        messages = self.context_manager.trim_messages(
            self.state.get_messages()
        )

        return {
            **self.state.get_context(),
            "messages": messages,
            "message_count": len(messages),
            "character_count": (
                self.context_manager.get_character_count(messages)
            )
        }

    def clear(self):
        self.state.clear()
        self.topic_tracker.clear()
