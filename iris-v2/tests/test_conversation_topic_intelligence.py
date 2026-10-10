
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
            "Python is used for machine learning."
        )
        conversation.intelligence.add_user_message(
            "Explain database indexing."
        )
        conversation.intelligence.add_assistant_message(
            "Database indexing improves database query performance."
        )

        results = conversation.search_history(
            "database",
            topic_aware=True
        )

        assert len(results) >= 1
        assert results[0]["topic_score"] >= 1

        normal_results = conversation.search_history(
            "database",
            topic_aware=False
        )

        assert len(normal_results) >= 1
        assert all(
            "topic_score" not in result
            for result in normal_results
        )

        conversation.save()

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        restored_results = restored.search_history(
            "database",
            topic_aware=True
        )

        assert len(restored_results) >= 1
        assert restored_results[0]["topic_score"] >= 1

    print("CONVERSATION TOPIC INTELLIGENCE TEST: PASS")


if __name__ == "__main__":
    main()
