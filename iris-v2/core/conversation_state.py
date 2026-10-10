
import time


class ConversationState:
    def __init__(self):
        self.messages = []
        self.topic = ""
        self.last_user_message = ""
        self.last_response = ""
        self.turn_count = 0

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message,
            "timestamp": time.time()
        })

        self.last_user_message = message
        self.turn_count += 1

    def add_assistant_message(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message,
            "timestamp": time.time()
        })

        self.last_response = message

    def set_topic(self, topic):
        self.topic = topic

    def get_messages(self):
        return self.messages.copy()

    def get_recent_messages(self, limit=10):
        if limit <= 0:
            return []

        return self.messages[-limit:]

    def get_context(self):
        return {
            "topic": self.topic,
            "last_user_message": self.last_user_message,
            "last_response": self.last_response,
            "turn_count": self.turn_count
        }

    def get_turn_count(self):
        return self.turn_count

    def clear(self):
        self.messages.clear()
        self.topic = ""
        self.last_user_message = ""
        self.last_response = ""
        self.turn_count = 0
