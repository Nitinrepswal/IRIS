class TaskDecomposer:
    def __init__(self, model):
        self.model = model

    def decompose(self, message):
        prompt = f"""
You are the task decomposition engine for IRIS.

Break the user's request into precise executable subtasks.

Rules:
- Create the smallest number of necessary subtasks.
- Keep them in the correct order.
- Each subtask must contain one clear action.
- The action must describe what needs to happen.
- The target must describe what the action operates on.
- Later steps may depend on the result of earlier steps.
- Do not execute anything.
- Do not choose tools.
- Do not invent information.

Allowed actions:
- search
- read
- create
- edit
- run
- explain
- summarize

Return ONLY valid JSON:

{{
    "goal": "main goal",
    "tasks": [
        {{
            "step": 1,
            "action": "action",
            "target": "target"
        }}
    ]
}}

Example:

User:
Find my resume and read it.

Return:

{{
    "goal": "Find and read the user's resume",
    "tasks": [
        {{
            "step": 1,
            "action": "search",
            "target": "user's resume"
        }},
        {{
            "step": 2,
            "action": "read",
            "target": "resume found in step 1"
        }}
    ]
}}

User:
Find my resume, read it, and summarize it.

Return:

{{
    "goal": "Find, read, and summarize the user's resume",
    "tasks": [
        {{
            "step": 1,
            "action": "search",
            "target": "user's resume"
        }},
        {{
            "step": 2,
            "action": "read",
            "target": "resume found in step 1"
        }},
        {{
            "step": 3,
            "action": "summarize",
            "target": "resume content from step 2"
        }}
    ]
}}

User request:
{message}
"""

        return self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])