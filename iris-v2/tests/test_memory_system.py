from memory.memory_system import MemorySystem


def main():
    memory = MemorySystem()

    memory.clear()

    memory.remember(
        "User prefers C++ for programming."
    )

    memory.remember(
        "User is building an AI assistant called IRIS."
    )

    memory.remember(
        "User is learning machine learning."
    )

    print("Stored memories:")

    for item in memory.get_all():
        print("-", item)

    print("\nRecall:")

    results = memory.recall(
        "What programming language does the user prefer?",
        top_k=2,
        threshold=0.5
    )

    for result in results:
        print(
            f"{result['score']:.4f} - "
            f"{result['memory']}"
        )

    updated = memory.update(
        "User prefers C++ for programming.",
        "User prefers Python for programming."
    )

    print("\nUpdate successful:", updated)

    forgotten = memory.forget(
        "User is learning machine learning."
    )

    print("Forget successful:", forgotten)

    print("\nFinal memories:")

    for item in memory.get_all():
        print("-", item)

    memory.clear()


if __name__ == "__main__":
    main()