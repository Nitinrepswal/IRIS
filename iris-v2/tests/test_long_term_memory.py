from memory.long_term_memory import LongTermMemory


def main():
    path = "memory/test_long_term.json"

    memory = LongTermMemory(path)

    memory.add("User is building IRIS.")
    memory.add("IRIS uses Ollama.")

    print("Stored memories:")
    print(memory.get_all())

    new_memory = LongTermMemory(path)

    print("\nMemories after creating a new instance:")
    print(new_memory.get_all())

    new_memory.clear()

    print("\nAfter clear:")
    print(new_memory.get_all())


if __name__ == "__main__":
    main()