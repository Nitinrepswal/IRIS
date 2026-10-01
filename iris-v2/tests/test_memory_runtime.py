from core.iris_core import IRISCore
from memory.memory_system import MemorySystem


def main():
    core = IRISCore()
    memory = MemorySystem()

    memory.clear()

    core.set_memory(memory)

    print("Memory connected:", core.memory is memory)

    core.memory.remember(
        "User is building an AI assistant called IRIS."
    )

    print("\nStored memories:")
    for item in core.memory.get_all():
        print("-", item)

    core.memory.forget(
        "User is building an AI assistant called IRIS."
    )

    print("\nAfter forget:")
    print(core.memory.get_all())

    core.memory.clear()


if __name__ == "__main__":
    main()
