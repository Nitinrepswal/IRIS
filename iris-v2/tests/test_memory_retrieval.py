from models.llm_model import LLMModel
from core.memory_retriever import MemoryRetriever


def main():
    model = LLMModel()

    memories = [
        "User's name is Nitin.",
        "User prefers C++ for programming.",
        "User is building an AI assistant called IRIS.",
        "User likes working on machine learning projects."
    ]

    retriever = MemoryRetriever(
        model,
        memories
    )

    queries = [
        "What programming language does the user prefer?",
        "What AI project is the user building?"
    ]

    for query in queries:
        print("\nQuery:", query)

        results = retriever.retrieve(
            query,
            top_k=2
        )

        for result in results:
            print(
                f"{result['score']:.4f} - "
                f"{result['memory']}"
            )


if __name__ == "__main__":
    main()