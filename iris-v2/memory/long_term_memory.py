import json
import os


class LongTermMemory:
    def __init__(self, path="memory/long_term.json"):
        self.path = path
        self.memories = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r") as file:
            return json.load(file)

    def _save(self):
        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.path, "w") as file:
            json.dump(self.memories, file, indent=2)

    def add(self, memory):
        self.memories.append(memory)
        self._save()

    def get_all(self):
        return self.memories

    def clear(self):
        self.memories = []

        if os.path.exists(self.path):
            os.remove(self.path)