from models.llm_model import LLMModel
from core.iris_brain import IRISBrain


def main():
    model = LLMModel()
    brain = IRISBrain(model)

    messages = [
        "Hello IRIS.",
        "Find my resume.",
        "What is machine learning?",
        "Remember that I am building IRIS."
    ]

    for message in messages:
        result = brain.process(message)

        print("\nUser:", message)
        print("Intent:", result["intent"])
        print("Tool:", result["tool"])
        print("Response:", result["response"])


if __name__ == "__main__":
    main()