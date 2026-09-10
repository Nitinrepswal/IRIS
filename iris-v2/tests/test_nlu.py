from models.llm_model import LLMModel
from core.nlu import NaturalLanguageUnderstanding


def main():
    model = LLMModel()
    nlu = NaturalLanguageUnderstanding(model)

    messages = [
        "Find my latest resume and tell me what I should improve.",
        "I want to learn machine learning in three months.",
        "Remind me what project I was working on."
    ]

    for message in messages:
        print("\nUser:", message)

        understanding = nlu.understand(message)

        print("\nIRIS understanding:")
        print(understanding)


if __name__ == "__main__":
    main()