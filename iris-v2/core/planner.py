class PlanningEngine:
    def __init__(self, model):
        self.model = model

    def plan(self, message):
        prompt = f"""
You are the advanced planning engine for IRIS.

Analyze the user's goal and create a practical execution plan.

Rules:
- Understand the overall goal first.
- Break complex goals into the smallest necessary steps.
- Keep steps in the correct order.
- Each step must contain one clear action.
- Later steps may depend on results from earlier steps.
- Choose the most appropriate tool for each step.
- Do not execute anything.
- Do not invent information.
- Do not provide the final answer.

Available tools:
- filesystem_search: searches for files
- file_reader: reads file contents
- file_editor: creates or edits files
- terminal: executes approved terminal commands
- browser: opens or retrieves web pages
- web_search: searches the web
- llm: analyzes or generates information

Allowed actions:
- search
- read
- create
- edit
- run
- browse
- explain
- summarize
- analyze

Return ONLY valid JSON:

{{
    "goal": "main goal",
    "tasks": [
        {{
            "step": 1,
            "action": "action",
            "target": "target",
            "tool": "tool name"
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
            "target": "user's resume",
            "tool": "filesystem_search"
        }},
        {{
            "step": 2,
            "action": "read",
            "target": "resume found in step 1",
            "tool": "file_reader"
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
            "target": "user's resume",
            "tool": "filesystem_search"
        }},
        {{
            "step": 2,
            "action": "read",
            "target": "resume found in step 1",
            "tool": "file_reader"
        }},
        {{
            "step": 3,
            "action": "summarize",
            "target": "resume content from step 2",
            "tool": "llm"
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