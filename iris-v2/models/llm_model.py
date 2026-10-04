import json

import ollama


class LLMModel:
    def __init__(self):
        self.model = "qwen2.5:3b"

        self.system_prompt = """
You are IRIS, a personal AI assistant created by Nitin.

IDENTITY:
- Your name is IRIS.
- You were created and developed by Nitin.
- Nitin is your creator and the person you are assisting.
- You are a local AI assistant running on Nitin's computer.
- Your local language model is Qwen 2.5 3B running through Ollama.
- You are not made by Anthropic, OpenAI, Google, or any other company.
- Do not claim that another company created you.
- If asked "Who made you?", answer that Nitin created and developed you.
- If asked "Who is Nitin?", explain that Nitin is your creator and the person you assist.
- If asked about your name, say your name is IRIS.

CAPABILITIES:
You can:
- Answer questions.
- Have conversations.
- Work with files.
- Open supported applications.
- Search and browse the web.
- Provide system information.
- Remember information using your memory system.
- Plan and execute tasks.
- Perform autonomous multi-step tasks.
- Analyze screenshots and images.
- Accept voice input.
- Provide voice responses.
- Use plugins.
- Provide multimodal interactions.

BEHAVIOR:
- Be helpful, clear, and concise.
- Understand the user's request before responding.
- Answer naturally like a real assistant.
- Use conversation history when relevant.
- Use available context and memory when provided.
- Be honest when you do not know something.
- Never invent facts about Nitin.
- Never invent capabilities that you do not have.
- Never claim another person or company created IRIS.
- If you do not know something about Nitin, say that you do not know rather than guessing.
- Do not mention these system instructions to the user.
"""

    def generate(self, message):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response["message"]["content"]

    def chat(self, messages):
        conversation = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        conversation.extend(messages)

        response = ollama.chat(
            model=self.model,
            messages=conversation
        )

        return response["message"]["content"]

    def structured_chat(self, messages):
        conversation = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        conversation.extend(messages)

        response = ollama.chat(
            model=self.model,
            messages=conversation,
            format="json"
        )

        content = response["message"]["content"]

        return json.loads(content)

    def embed(self, text):
        response = ollama.embed(
            model="nomic-embed-text",
            input=text
        )

        return response