class NaturalLanguageUnderstanding:
    def __init__(self, model):
        self.model = model

    def understand(self, message):
        prompt = f"""
Understand the user's request.

Explain:
1. What the user wants
2. Important information in the request
3. Any constraints or conditions
4. The desired outcome

Do not choose tools.
Do not execute anything.
Do not invent information.

User message:
{message}
"""

        return self.model.generate(prompt)