from core.memory_manager import MemoryManager


def main():
    manager = MemoryManager([
        "User's name is Nitin.",
        "User prefers Python for programming.",
        "User is building an AI assistant called IRIS."
    ])

    print("Initial memories:")

    for memory in manager.get_all():
        print("-", memory)

    memory_to_delete = "User prefers Python for programming."

    deleted = manager.delete(
        memory_to_delete
    )

    print("\nDeletion successful:", deleted)

    print("\nRemaining memories:")

    for memory in manager.get_all():
        print("-", memory)


if __name__ == "__main__":
    main()