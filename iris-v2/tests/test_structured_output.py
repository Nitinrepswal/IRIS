from models.llm_model import LLMModel


def main():
    model = LLMModel()

    messages = [
        {
            "role": "user",
            "content": """
Return a JSON object with exactly two fields:
response and reasoning.

The response should answer:
What is machine learning?

The reasoning field should briefly explain what the answer contains.
"""
        }
    ]

    result = model.structured_chat(messages)

    print("Structured output:")
    print(result)

    print("\nType:", type(result))
    print("Response:", result["response"])
    print("Reasoning:", result["reasoning"])


if __name__ == "__main__":
    main()