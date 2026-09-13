import json


class IntentDetector:
    def __init__(self, model):
        self.model = model

    def detect(self, message):
        prompt = f"""
Determine the user's primary intent.

Choose exactly one intent from:
- chat
- information
- filesystem
- memory
- terminal

Return only a JSON object with exactly these fields:
intent
reason

The intent must be one of the five allowed values.

Do not execute anything.
Do not invent information.

User message:
{message}
"""

        result = self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])

        return result