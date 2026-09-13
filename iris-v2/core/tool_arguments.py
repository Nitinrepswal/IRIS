class ToolArgumentGenerator:
    def __init__(self, model):
        self.model = model

    def generate(self, message, tool):
        prompt = f"""
You generate arguments for an IRIS tool.

Available tools and their arguments:

filesystem_search:
- directory
- query

file_editor:
- path
- content

file_reader:
- path

terminal:
- command

Rules:
- Generate arguments only for the selected tool.
- Do not execute anything.
- Do not invent information.
- Use the user's request to determine the arguments.
- Return ONLY valid JSON.

Selected tool:
{tool}

User request:
{message}

Return JSON in this format:
{{
    "tool": "{tool}",
    "arguments": {{}},
    "reason": "brief explanation"
}}
"""

        return self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])