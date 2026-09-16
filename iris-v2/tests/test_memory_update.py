from core.memory_manager import MemoryManager


def main():
    manager = MemoryManager([
        "User's name is Nitin.",
        "User prefers C++ for programming.",
        "User is building an AI assistant called IRIS."
    ])

    print("Initial memories:")

    for memory in manager.get_all():
        print("-", memory)

    old_memory = "User prefers C++ for programming."
    new_memory = "User prefers Python for programming."

    updated = manager.update(
        old_memory,
        new_memory
    )

    print("\nUpdate successful:", updated)

    print("\nUpdated memories:")

    for memory in manager.get_all():
        print("-", memory)


if __name__ == "__main__":
    main()