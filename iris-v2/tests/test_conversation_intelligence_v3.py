
import os
import tempfile

from core.conversation_intelligence_v3 import ConversationIntelligenceV3


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        iris = ConversationIntelligenceV3(
            path=path,
            context_budget=200
        )

        iris.add_user_message("Tell me about Python.")
        iris.add_assistant_message(
            "Python is widely used in machine learning."
        )
        iris.add_user_message("Explain database indexing.")
        iris.add_assistant_message(
            "Database indexing improves query performance."
        )

        search_results = iris.search("database")

        assert len(search_results) >= 1

        retrieval_result = iris.retrieve("database indexing")

        assert retrieval_result["count"] >= 1

        context_result = iris.build_context("database indexing")

        assert context_result["query"] == "database indexing"
        assert context_result["count"] >= 1
        assert context_result["context"]
        assert context_result["character_count"] <= 200
        assert (
            context_result["character_count"]
            == len(context_result["context"])
        )

        iris.save()

        restored = ConversationIntelligenceV3(
            path=path,
            context_budget=200
        )

        assert restored.load() is True

        restored_results = restored.search("database")

        assert len(restored_results) >= 1

        restored_context = restored.build_context("database indexing")

        assert restored_context["count"] >= 1
        assert restored_context["character_count"] <= 200

        restored.clear()

        assert restored.get_context()["turn_count"] == 0

    print("CONVERSATION INTELLIGENCE V3 TEST: PASS")


if __name__ == "__main__":
    main()
