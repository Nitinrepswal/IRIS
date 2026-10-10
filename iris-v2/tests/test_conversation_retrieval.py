
import os
import tempfile

from core.persistent_conversation import PersistentConversation
from core.conversation_retrieval import ConversationRetrieval


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")
        conversation = PersistentConversation(path=path)

        conversation.intelligence.add_user_message(
            "Tell me about Python."
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

        retrieval = ConversationRetrieval(conversation)

        result = retrieval.retrieve("database indexing")

        assert result["query"] == "database indexing"
        assert result["count"] >= 1
        assert len(result["messages"]) == result["count"]
        assert result["topic"] == conversation.intelligence.topic_tracker.get_topic()
        assert result["messages"][0]["score"] == 2

        for message in result["messages"]:
            assert message["role"] in ("user", "assistant")
            assert isinstance(message["content"], str)

        empty_result = retrieval.retrieve("")

        assert empty_result["count"] == 0
        assert empty_result["messages"] == []

        conversation.save()

        restored = PersistentConversation(path=path)
        assert restored.load() is True

        restored_retrieval = ConversationRetrieval(restored)
        restored_result = restored_retrieval.retrieve(
            "database indexing"
        )

        assert restored_result["count"] >= 1
        assert restored_result["messages"][0]["score"] == 2

    print("CONVERSATION RETRIEVAL TEST: PASS")


if __name__ == "__main__":
    main()
