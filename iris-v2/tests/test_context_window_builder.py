
import os
import tempfile

from core.persistent_conversation import PersistentConversation
from core.conversation_retrieval import ConversationRetrieval
from core.context_window_builder import ContextWindowBuilder


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

        retrieval = ConversationRetrieval(conversation)
        builder = ContextWindowBuilder(
            retrieval,
            max_characters=100
        )

        result = builder.build("database indexing")

        assert result["query"] == "database indexing"
        assert result["count"] >= 1
        assert result["character_count"] <= 100
        assert result["character_count"] == len(result["context"])
        assert result["context"]
        assert len(result["messages"]) == result["count"]

        for message in result["messages"]:
            assert message["role"] in ("user", "assistant")
            assert isinstance(message["content"], str)

        small_builder = ContextWindowBuilder(
            retrieval,
            max_characters=20
        )

        small_result = small_builder.build("database indexing")

        assert small_result["character_count"] <= 20

        empty_result = builder.build("")

        assert empty_result["context"] == ""
        assert empty_result["count"] == 0

        try:
            ContextWindowBuilder(retrieval, max_characters=0)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid character limit should fail")

    print("CONTEXT WINDOW BUILDER TEST: PASS")


if __name__ == "__main__":
    main()
