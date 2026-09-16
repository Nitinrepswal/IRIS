from memory.knowledge_base import KnowledgeBase


def main():
    knowledge = KnowledgeBase()

    knowledge.clear()

    knowledge.add(
        "User prefers C++ for programming."
    )

    knowledge.add(
        "User is building an AI assistant called IRIS."
    )

    knowledge.add(
        "User is learning machine learning."
    )

    print("Knowledge base:")

    for memory in knowledge.get_all():
        print("-", memory)

    print("\nSearch results:")

    results = knowledge.retrieve(
        "What programming language does the user prefer?",
        top_k=2,
        threshold=0.5
    )

    for result in results:
        print(
            f"{result['score']:.4f} - "
            f"{result['memory']}"
        )

    deleted = knowledge.delete(
        "User is learning machine learning."
    )

    print("\nDeletion successful:", deleted)

    print("\nFinal knowledge base:")

    for memory in knowledge.get_all():
        print("-", memory)

    knowledge.clear()


if __name__ == "__main__":
    main()