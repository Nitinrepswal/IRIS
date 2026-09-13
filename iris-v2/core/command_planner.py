class CommandPlanner:
    def __init__(self, model):
        self.model = model

    def plan(self, message):
        prompt = f"""
You are the command planner for IRIS.

Convert the user's request into ONE terminal command.

Allowed commands:
- pwd
- ls
- echo
- python

Rules:
- Return only a safe command using the allowed commands.
- Do not use pipes.
- Do not use redirects.
- Do not use shell operators.
- Do not use rm, mv, cp, sudo, chmod, or other commands.
- Do not execute the command.
- If the request cannot be safely represented, return "UNSUPPORTED".

Examples:

User: Show me the files here.
Command: ls

User: What directory am I in?
Command: pwd

User: Print hello.
Command: echo hello

User request:
{message}

Return ONLY valid JSON:
{{
    "command": "command here",
    "reason": "brief explanation"
}}
"""

        return self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])