import json
import os
from datetime import datetime


class ConversationStore:
    def __init__(self, path="memory/conversation.json"):
        self.path = path

    def save(self, history):
        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_document(self):
        """Return the conversation document while preserving legacy history."""
        history = self.load()

        if isinstance(history, dict) and isinstance(
            history.get("conversations"), list
        ):
            return {
                "version": history.get("version", 1),
                "conversations": history["conversations"],
            }

        if isinstance(history, list):
            if not history:
                return {"version": 1, "conversations": []}

            timestamp = datetime.now().isoformat(timespec="seconds")
            return {
                "version": 1,
                "conversations": [
                    {
                        "id": "legacy-conversation",
                        "title": "Previous conversation",
                        "created_at": timestamp,
                        "updated_at": timestamp,
                        "messages": history,
                    }
                ],
            }

        return {"version": 1, "conversations": []}

    def save_document(self, document):
        self.save(document)

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)
