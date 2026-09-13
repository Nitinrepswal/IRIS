class ToolSelector:
    def __init__(self, model):
        self.model = model

    def select(self, message, intent):
        prompt = f"""
You are selecting a tool for IRIS.

Available tools:
1. none
2. filesystem_search
3. memory
4. terminal

Choose exactly ONE tool.

Rules:

- Choose "filesystem_search" ONLY when the user wants to find, search,
  locate, list, read, create, or modify a file.
- Choose "memory" ONLY when the user wants IRIS to remember, recall,
  update, or forget personal information.
- Choose "terminal" ONLY when the user explicitly wants to run a command,
  program, or script.
- Choose "none" for questions, explanations, general conversation,
  calculations, or requests that do not require one of the tools above.

Examples:

User: Find my resume.
Tool: filesystem_search

User: Remember that I am building IRIS.
Tool: memory

User: What did I tell you yesterday?
Tool: memory

User: Run the Python script.
Tool: terminal

User: What is machine learning?
Tool: none

User: Explain recursion.
Tool: none

User: Hello IRIS.
Tool: none

Return ONLY valid JSON:
{{
    "tool": "one of: none, filesystem_search, memory, terminal",
    "reason": "brief explanation"
}}

User message:
{message}

Detected intent:
{intent}
"""

        return self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])