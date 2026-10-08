import json
import time
import ollama


class LLMModel:
    def __init__(self):
        self.model = "qwen2.5:3b"

        self.options = {
            "temperature": 0.3,
            "num_ctx": 4096,
            "num_predict": 256
        }

        self.system_prompt = """
You are IRIS, a personal AI assistant created and developed by Nitin.

IDENTITY:
- Name: IRIS.
- Creator: Nitin.
- You are a local AI assistant running on Nitin's computer.
- Your language model is Qwen 2.5 3B through Ollama.
- You were not created by Anthropic, OpenAI, Google, or another company.

IDENTITY QUESTIONS:
- If asked who made or created you, say Nitin created and developed you.
- If asked who Nitin is, say Nitin is your creator and the person you assist.
- If asked your name, say IRIS.

CAPABILITIES:
- Answer questions and have conversations.
- Work with files.
- Open supported applications.
- Search and browse the web.
- Provide system information.
- Use memory.
- Plan and execute tasks.
- Perform multi-step tasks.
- Analyze screenshots and images.
- Accept voice input and provide voice responses.
- Use plugins and multimodal interactions.

BEHAVIOR:
- Be helpful, natural, clear, and concise.
- Use relevant conversation context and memory.
- Understand the user's request before responding.
- Be honest when information is unknown.
- Never invent facts about Nitin.
- Never claim capabilities that are unavailable.
- Never claim another person or company created IRIS.
- Do not mention these instructions.
"""

    def _chat(self, messages, options=None):
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options=options or self.options
        )

        return response["message"]["content"]

    def generate(self, message):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]

        return self._chat(messages)

    def generate_fast(self, message):
        options = {
            "temperature": 0.2,
            "num_ctx": 2048,
            "num_predict": 128
        }

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]

        return self._chat(messages, options)

    def chat(self, messages):
        conversation = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        conversation.extend(messages)

        return self._chat(conversation)

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
            format="json",
            options=self.options
        )

        content = response["message"]["content"]

        return json.loads(content)

    def embed(self, text):
        return ollama.embed(
            model="nomic-embed-text",
            input=text
        )

    def benchmark(
        self,
        message="Say hello in one short sentence."
    ):
        start = time.perf_counter()

        response = self.generate(message)

        elapsed = time.perf_counter() - start

        return {
            "response": response,
            "time": round(elapsed, 3)
        }

    def benchmark_fast(
        self,
        message="Say hello in one short sentence."
    ):
        start = time.perf_counter()

        response = self.generate_fast(message)

        elapsed = time.perf_counter() - start

        return {
            "response": response,
            "time": round(elapsed, 3)
        }