import json
import os
from datetime import datetime


class IRISLogger:
    def __init__(self, path="logs/iris.json"):
        self.path = path

        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

    def log(self, event, details=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        logs = []

        if os.path.exists(self.path):
            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:
                try:
                    logs = json.load(file)
                except json.JSONDecodeError:
                    logs = []

        logs.append(entry)

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                logs,
                file,
                indent=2
            )

    def get_logs(self):
        if not os.path.exists(self.path):
            return []

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)