from models.llm_model import LLMModel
from core.memory_extractor import MemoryExtractor


def main():
    model = LLMModel()
    extractor = MemoryExtractor(model)

    messages = [
        "My name is Nitin and I am building an AI assistant called IRIS.",
        "I prefer C++ for programming.",
        "What is machine learning?",
        "Find my resume."
    ]

    for message in messages:
        result = extractor.extract(message)

        print("\nUser:", message)
        print("Memories:", result["memories"])


if __name__ == "__main__":
    main()