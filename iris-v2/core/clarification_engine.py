
class ClarificationEngine:
    QUESTIONS = {
        "directory": "Which directory should I use?",
        "query": "What should I search for?",
        "path": "Which file path should I use?",
        "content": "What content should I put in the file?",
        "command": "Which command do you want to run?"
    }

    def generate(self, missing_arguments):
        if not isinstance(missing_arguments, list):
            return {
                "needs_clarification": False,
                "question": "",
                "missing_arguments": [],
                "valid": False,
                "reason": "Missing arguments must be provided as a list."
            }

        if not all(
            isinstance(argument, str) and argument in self.QUESTIONS
            for argument in missing_arguments
        ):
            return {
                "needs_clarification": False,
                "question": "",
                "missing_arguments": [],
                "valid": False,
                "reason": "Unknown or invalid argument."
            }

        missing = list(dict.fromkeys(missing_arguments))

        if not missing:
            return {
                "needs_clarification": False,
                "question": "",
                "missing_arguments": [],
                "valid": True,
                "reason": "No clarification is required."
            }

        questions = [
            self.QUESTIONS[argument]
            for argument in missing
        ]

        return {
            "needs_clarification": True,
            "question": " ".join(questions),
            "missing_arguments": missing,
            "valid": True,
            "reason": "More information is required from the user."
        }
