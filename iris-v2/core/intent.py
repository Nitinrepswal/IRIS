class IntentDetector:
    def __init__(self, model):
        self.model = model

    def detect(self, message):
        prompt = f"""
You are the intent classifier for IRIS.

Choose exactly ONE intent.

Allowed intents:
- chat
- information
- filesystem
- memory
- terminal

Rules:

- "chat" = greetings, casual conversation, or conversation with IRIS.
- "information" = asking for explanations, facts, definitions, or general knowledge.
- "filesystem" = finding, locating, searching, reading, creating, or modifying files.
- "memory" = asking IRIS to remember, recall, update, or forget personal information.
- "terminal" = asking IRIS to run a command, program, or script.

Examples:

"Hello IRIS" → chat
"How are you?" → chat
"What is machine learning?" → information
"Explain recursion" → information
"Find my resume" → filesystem
"Open my resume" → filesystem
"Remember that I am building IRIS" → memory
"What do you remember about my project?" → memory
"Run the Python script" → terminal
"Execute this command" → terminal

Return ONLY valid JSON:
{{
    "intent": "one of: chat, information, filesystem, memory, terminal",
    "reason": "brief explanation"
}}

User message:
{message}
"""

        return self.model.structured_chat([
            {
                "role": "user",
                "content": prompt
            }
        ])