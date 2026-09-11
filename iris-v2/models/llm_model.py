import ollama


class LLMModel:
    def __init__(self):
        self.model = "qwen2.5:3b"

    def generate(self, message):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response["message"]["content"]

    def chat(self, messages):
        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]