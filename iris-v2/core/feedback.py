import json
import os
from datetime import datetime


class FeedbackSystem:
    def __init__(self, path="logs/feedback.json"):
        self.path = path
        self._ensure_directory()
        self.feedback = self._load()

    def _ensure_directory(self):
        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

    def _load(self):
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.feedback, file, indent=2)

    def add(self, message, rating, comment=""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "rating": rating,
            "comment": comment
        }

        self.feedback.append(entry)
        self._save()

        return entry

    def get_all(self):
        return self.feedback

    def get_average_rating(self):
        if not self.feedback:
            return 0

        total = sum(
            entry["rating"]
            for entry in self.feedback
        )

        return round(total / len(self.feedback), 2)

    def clear(self):
        self.feedback = []

        if os.path.exists(self.path):
            os.remove(self.path)