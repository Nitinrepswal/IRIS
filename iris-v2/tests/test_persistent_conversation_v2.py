
import json
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
        conversation.intelligence.add_user_message(
            "Explain database indexing."
        )
        conversation.intelligence.set_topic("Database indexing")

        conversation.save()

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        tracker = restored.intelligence.topic_tracker
        assert tracker.get_topic().lower() == "database indexing"
        assert tracker.topic_changes == 1
        assert len(tracker.history) == 2

        assert restored.get_context()["turn_count"] == 2

        # Invalid JSON must not replace current state.
        with open(path, "w", encoding="utf-8") as file:
            file.write("{broken")

        try:
            restored.load()
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Malformed JSON should be rejected"
            )

        assert restored.get_context()["turn_count"] == 2

        # Unsupported versions must be rejected.
        with open(path, "w", encoding="utf-8") as file:
            json.dump({"version": 99}, file)

        try:
            restored.load()
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Unsupported version should be rejected"
            )

        assert restored.get_context()["turn_count"] == 2

    print("PERSISTENT CONVERSATION V2 TEST: PASS")


if __name__ == "__main__":
    main()
