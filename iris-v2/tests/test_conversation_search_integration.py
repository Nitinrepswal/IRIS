import os
import tempfile

from core.persistent_conversation import PersistentConversation


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")
        conversation = PersistentConversation(path=path)

        conversation.intelligence.add_user_message(
            "Tell me about Python programming."
        )
        conversation.intelligence.add_assistant_message(
            "Python is useful for machine learning."
        )
        conversation.intelligence.add_user_message(
            "Explain database indexing."
        )
        conversation.intelligence.add_assistant_message(
            "Database indexing improves query performance."
        )

        results = conversation.search_history("Python")

        assert len(results) == 2
        assert all(
            "python" in result["content"].lower()
            for result in results
        )

        conversation.save()

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        results = restored.search_history("database indexing")

        assert len(results) >= 1
        assert results[0]["phrase_match"] is True
        assert results[0]["score"] == 2

        results = restored.search_history(
            "Python",
            limit=1
        )

        assert len(results) == 1

        assert restored.search_history("quantum physics") == []

    print("CONVERSATION SEARCH INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()