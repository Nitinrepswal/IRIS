from models.llm_model import LLMModel
from core.intent import IntentDetector


def main():
    model = LLMModel()
    detector = IntentDetector(model)

    messages = [
        "Hello IRIS, how are you?",
        "What is machine learning?",
        "Find my resume.",
        "Remember that I am working on IRIS.",
        "Run the Python script."
    ]

    for message in messages:
        result = detector.detect(message)

        print("\nUser:", message)
        print("Intent:", result["intent"])
        print("Reason:", result["reason"])


if __name__ == "__main__":
    main()