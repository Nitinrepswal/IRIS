from agent.agent_memory import AgentMemory


def main():
    memory = AgentMemory()

    memory.clear()

    memory.remember(
        "User is building an AI assistant called IRIS."
    )

    memory.remember(
        "User prefers Python for programming."
    )

    memory.remember(
        "IRIS uses Ollama for local language models."
    )

    print("Agent memories:")

    for item in memory.get_all():
        print("-", item)

    print("\nAgent recall:")

    results = memory.recall(
        "What technology does IRIS use for its language model?",
        top_k=2,
        threshold=0.5
    )

    for result in results:
        print(
            f"{result['score']:.4f} - "
            f"{result['memory']}"
        )

    updated = memory.update(
        "User prefers Python for programming.",
        "User prefers C++ for programming."
    )

    print("\nMemory update:", updated)

    forgotten = memory.forget(
        "IRIS uses Ollama for local language models."
    )

    print("Memory forget:", forgotten)

    print("\nFinal agent memories:")

    for item in memory.get_all():
        print("-", item)

    memory.clear()


if __name__ == "__main__":
    main()