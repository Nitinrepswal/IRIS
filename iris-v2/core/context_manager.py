class ContextManager:
    def __init__(self, max_messages=20, max_characters=6000):
        self.max_messages = max_messages
        self.max_characters = max_characters

    def trim_messages(self, messages):
        if not messages:
            return []

        selected = []
        characters = 0

        for message in reversed(messages):
            content = str(message.get("content", ""))
            message_size = len(content)

            if selected and (
                len(selected) >= self.max_messages
                or characters + message_size > self.max_characters
            ):
                break

            selected.append(message)
            characters += message_size

        selected.reverse()

        return selected

    def get_character_count(self, messages):
        return sum(
            len(str(message.get("content", "")))
            for message in messages
        )

    def get_message_count(self, messages):
        return len(messages)

    def get_usage(self, messages):
        character_count = self.get_character_count(messages)
        message_count = self.get_message_count(messages)

        return {
            "messages": message_count,
            "characters": character_count,
            "max_messages": self.max_messages,
            "max_characters": self.max_characters,
            "message_usage": round(
                message_count / self.max_messages, 2
            ),
            "character_usage": round(
                character_count / self.max_characters, 2
            )
        }

    def clear(self):
        return None