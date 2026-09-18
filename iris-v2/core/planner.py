class PlanningEngine:
    def __init__(self, model):
        self.model = model

    def plan(self, message):
        prompt = f"""
You are the planning engine for IRIS.

Break the user's request into a sequence of clear steps.

Rules:
- Create the smallest number of steps needed.
- Each step must describe one action.
- Keep steps in the correct order.
- Do not execute anything.
- Do not invent information.
- Do not choose tools.
- Do not provide the final answer.
- If the request needs only one action, return one step.

Return ONLY valid JSON:

{{
    "goal": "the user's main goal",
    "steps": [
        "step 1",
        "step 2"
    ]
}}

Examples:

User: Find my resume.
{{
    "goal": "Find the user's resume",
    "steps": [
        "Search for the user's resume"
    ]
}}

User: Find my resume and read it.
{{
    "goal": "Find and read the user's resume",
    "steps": [
        "Search for the user's resume",
        "Read the resume"
    ]
}}

User: Find my resume, read it, and summarize it.
{{
    "goal": "Find and summarize the user's resume",
    "steps": [
        "Search for the user's resume",
        "Read the resume",
        "Summarize the resume"
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