import json
import os
from datetime import datetime


class Logger:
    def __init__(self, path="logs/iris.json"):
        self.path = path
        self._ensure_directory()

    def _ensure_directory(self):
        directory = os.path.dirname(self.path)

        if directory:
            os.makedirs(directory, exist_ok=True)

    def _write(self, level, message, context=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": str(message)
        }

        if context is not None:
            entry["context"] = context

        try:
            logs = self._load()

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

        except Exception:
            pass

        return entry

    def _load(self):
        if not os.path.exists(self.path):
            return []

        try:
            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return []

    def debug(self, message, context=None):
        return self._write(
            "DEBUG",
            message,
            context
        )

    def info(self, message, context=None):
        return self._write(
            "INFO",
            message,
            context
        )

    def warning(self, message, context=None):
        return self._write(
            "WARNING",
            message,
            context
        )

    def error(self, message, context=None):
        return self._write(
            "ERROR",
            message,
            context
        )

    def get_logs(self):
        return self._load()

    def get_by_level(self, level):
        return [
            entry
            for entry in self._load()
            if entry.get("level") == level
        ]

    def clear(self):
        try:
            if os.path.exists(self.path):
                os.remove(self.path)
        except OSError:
            pass