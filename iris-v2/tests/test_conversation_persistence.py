import os

from memory.conversation_store import ConversationStore


def main():
    path = "memory/test_conversation.json"

    store = ConversationStore(path)

    history = [
        {
            "role": "user",
            "content": "My name is Nitin."
        },
        {
            "role": "assistant",
            "content": "Nice to meet you, Nitin."
        }
    ]

    store.save(history)

    print("Saved conversation.")

    loaded = store.load()

    print("\nLoaded conversation:")
    print(loaded)

    print("\nMessages:", len(loaded))

    store.clear()

    print("\nFile exists after clear:", os.path.exists(path))


if __name__ == "__main__":
    main()