import re

from core.computer_control import ComputerControl


class AppControl:
    def __init__(self):
        self.computer = ComputerControl()

        self.applications = {
            "calculator": "Calculator",
            "textedit": "TextEdit",
            "text edit": "TextEdit",
            "safari": "Safari"
        }

    def detect_application(self, message):
        text = message.lower().strip()

        for name, application in self.applications.items():
            if name not in text:
                continue

            if re.search(
                r"\b(open|launch|start|run)\b",
                text
            ):
                return application

        return None

    def execute(self, message):
        application = self.detect_application(message)

        if application is None:
            return None

        result = self.computer.launch_application(
            application
        )

        if result["success"]:
            return result["message"]

        return result["message"]