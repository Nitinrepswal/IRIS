
import os
import tempfile

from core.conversation_intelligence_v3 import ConversationIntelligenceV3


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        iris = ConversationIntelligenceV3(path=path)

        first = iris.process_user_message("Tell me about Python.")

        assert first["action"] == "new_topic"
        assert first["topic"] == "Python"

        second = iris.process_user_message(
            "Explain database indexing."
        )

        assert second["action"] == "new_topic"
        assert second["previous_topic"] == "Python"
        assert second["topic"] == "database indexing"

        context = iris.get_context()
        assert context["turn_count"] == 2

        state = iris.get_flow_state()
        assert state["current_topic"] == "database indexing"
        assert len(state["transitions"]) == 2

        search_results = iris.search("database")

        assert len(search_results) >= 1

        iris.clear()

        assert iris.get_context()["turn_count"] == 0
        assert iris.get_flow_state()["current_topic"] == ""
        assert iris.get_flow_state()["transitions"] == []

    print("CONVERSATION FLOW INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
