from memory.working_memory import WorkingMemory


def main():
    memory = WorkingMemory(max_items=3)

    memory.add("User is building IRIS.")
    memory.add("IRIS uses Ollama.")
    memory.add("Current phase is tool development.")

    print("Working memory:")
    print(memory.get_all())

    memory.add("Next phase is agent development.")

    print("\nAfter adding another item:")
    print(memory.get_all())

    print("\nNumber of items:", len(memory.get_all()))

    memory.clear()

    print("\nAfter clear:")
    print(memory.get_all())


if __name__ == "__main__":
    main()