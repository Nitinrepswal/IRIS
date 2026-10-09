
class MissingArgumentDetector:
    TOOL_ARGUMENTS = {
        "filesystem_search": ["directory", "query"],
        "file_editor": ["path", "content"],
        "file_reader": ["path"],
        "terminal": ["command"]
    }

    QUESTIONS = {
        "directory": "Which directory should I use?",
        "query": "What should I search for?",
        "path": "Which file path should I use?",
        "content": "What content should I put in the file?",
        "command": "Which command do you want to run?"
    }

    def detect(self, tool, arguments):
        if tool not in self.TOOL_ARGUMENTS:
            return {
                "valid": False,
                "missing": [],
                "questions": [],
                "reason": "Unsupported tool."
            }

        if not isinstance(arguments, dict):
            return {
                "valid": False,
                "missing": self.TOOL_ARGUMENTS[tool].copy(),
                "questions": [
                    self.QUESTIONS[key]
                    for key in self.TOOL_ARGUMENTS[tool]
                ],
                "reason": "Arguments must be a dictionary."
            }

        missing = [
            key
            for key in self.TOOL_ARGUMENTS[tool]
            if not isinstance(arguments.get(key), str)
            or not arguments.get(key, "").strip()
        ]

        return {
            "valid": not missing,
            "missing": missing,
            "questions": [
                self.QUESTIONS[key] for key in missing
            ],
            "reason": (
                "All required arguments are present."
                if not missing
                else "Some required arguments are missing."
            )
        }
