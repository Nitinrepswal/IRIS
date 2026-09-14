class MemoryExtractor:
    def __init__(self, model):
        self.model = model

    def extract(self, message):
        prompt = f"""
You are the memory extractor for IRIS.

Identify explicit personal information that could be useful
to remember about the user in future conversations.

Good memories include:
- User's name
- User's preferences
- User's projects
- User's goals
- User's skills
- User explicitly stated facts about themselves

Do NOT extract:
- Questions the user asks
- Requests the user makes
- Topics the user is asking about
- Temporary tasks
- General knowledge
- Information about other people
- Information that was not explicitly stated

Do not invent or infer information.

Examples:

"My name is Nitin."
→ "User's name is Nitin."

"I prefer C++ for programming."
→ "User prefers C++ for programming."

"I am building an AI assistant called IRIS."
→ "User is building an AI assistant called IRIS."

"What is machine learning?"
→ []

"Find my resume."
→ []

Return ONLY valid JSON:

{{
    "memories": []
}}

or:

{{
    "memories": [
        "explicit personal memory"
    ]
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