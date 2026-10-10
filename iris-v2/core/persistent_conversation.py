
import json
import math
import os

from core.conversation_intelligence import ConversationIntelligence
from core.conversation_search import ConversationSearch


class PersistentConversation:
    VERSION = 2

    def __init__(
        self,
        path="memory/intelligence_context.json",
        max_messages=20,
        max_characters=6000
    ):
        self.path = path
        self.intelligence = ConversationIntelligence(
            max_messages=max_messages,
            max_characters=max_characters
        )
        self.search = ConversationSearch()

    def save(self):
        context = self.intelligence.get_context()
        internal_messages = (
            self.intelligence.context_manager.trim_messages(
                self.intelligence.state.get_messages()
            )
        )

        context["messages"] = internal_messages

        data = {
            "version": self.VERSION,
            "context": context,
            "topic_tracker": (
                self.intelligence.topic_tracker.export_state()
            )
        }

        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def load(self):
        if not os.path.exists(self.path):
            return False

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(
                "Saved conversation is not valid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError("Invalid saved conversation")

        if data.get("version") != self.VERSION:
            raise ValueError("Unsupported conversation save version")

        context = data.get("context")
        tracker_state = data.get("topic_tracker")

        if not isinstance(context, dict):
            raise ValueError("Invalid conversation context")

        messages = context.get("messages")
        topic = context.get("topic", "")

        if not isinstance(messages, list):
            raise ValueError("Conversation messages must be a list")

        if not isinstance(topic, str):
            raise ValueError("Conversation topic must be a string")

        for message in messages:
            if (
                not isinstance(message, dict)
                or message.get("role") not in ("user", "assistant")
                or not isinstance(message.get("content"), str)
            ):
                raise ValueError("Invalid conversation message")

            timestamp = message.get("timestamp")

            if timestamp is not None and (
                isinstance(timestamp, bool)
                or not isinstance(timestamp, (int, float))
                or not math.isfinite(timestamp)
                or timestamp < 0
            ):
                raise ValueError("Invalid message timestamp")

        tracker_check = self.intelligence.topic_tracker.__class__()
        tracker_check.restore_state(tracker_state)

        new_intelligence = ConversationIntelligence(
            max_messages=self.intelligence.context_manager.max_messages,
            max_characters=self.intelligence.context_manager.max_characters
        )

        for message in messages:
            if message["role"] == "user":
                new_intelligence.add_user_message(message["content"])
            else:
                new_intelligence.add_assistant_message(message["content"])

            saved_timestamp = message.get("timestamp")

            if saved_timestamp is not None:
                new_intelligence.state.messages[-1]["timestamp"] = (
                    saved_timestamp
                )
            else:
                new_intelligence.state.messages[-1].pop(
                    "timestamp", None
                )

        new_intelligence.set_topic(topic)
        new_intelligence.topic_tracker.restore_state(tracker_state)

        self.intelligence = new_intelligence
        return True

    def search_history(self, query, limit=5, topic_aware=True):
        messages = self.intelligence.state.get_messages()
        messages = self.intelligence.context_manager.trim_messages(
            messages
        )

        search_limit = len(messages) if topic_aware else limit

        results = self.search.search(
            query=query,
            messages=messages,
            limit=search_limit
        )

        if not topic_aware:
            return results[:limit]

        topic = self.intelligence.topic_tracker.get_topic()

        if not topic.strip():
            return results[:limit]

        topic_words = set(topic.lower().split())

        for result in results:
            content_words = set(result["content"].lower().split())
            result["topic_score"] = len(topic_words & content_words)

        results.sort(
            key=lambda item: (
                item["topic_score"],
                item["phrase_match"],
                item["score"]
            ),
            reverse=True
        )

        return results[:limit]

    def get_context(self):
        return self.intelligence.get_context()

    def clear(self):
        self.intelligence.clear()

        if os.path.exists(self.path):
            os.remove(self.path)
