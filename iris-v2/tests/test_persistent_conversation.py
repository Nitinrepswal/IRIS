
import os
import tempfile

from core.persistent_conversation import PersistentConversation


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        conversation = PersistentConversation(path=path)
        conversation.intelligence.add_user_message(
            "Tell me about Python."
        )
        conversation.intelligence.add_assistant_message(
            "Python is a programming language."
        )
        conversation.intelligence.set_topic("Python")

        conversation.save()
        assert os.path.exists(path)

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        context = restored.get_context()

        assert context["messages"] == [
            {"role": "user", "content": "Tell me about Python."},
            {
                "role": "assistant",
                "content": "Python is a programming language."
            }
        ]
        assert context["topic"] == "Python"
        assert context["turn_count"] == 1
        assert context["last_response"] == (
            "Python is a programming language."
        )

        restored.clear()
        assert restored.get_context()["messages"] == []
        assert not os.path.exists(path)

        missing = PersistentConversation(
            path=os.path.join(directory, "missing.json")
        )
        assert missing.load() is False

    print("PERSISTENT CONVERSATION TEST: PASS")


if __name__ == "__main__":
    main()
