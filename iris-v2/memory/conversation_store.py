import json
import os


class ConversationStore:
    def __init__(self, path="memory/conversation.json"):
        self.path = path

    def save(self, history):
        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.path, "w") as file:
            json.dump(history, file, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r") as file:
            return json.load(file)

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)