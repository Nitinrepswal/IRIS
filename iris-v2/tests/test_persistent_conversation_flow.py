
import os
import tempfile

from core.conversation_intelligence_v3 import ConversationIntelligenceV3


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        iris = ConversationIntelligenceV3(path=path)

        iris.process_user_message("Tell me about Python.")
        iris.process_user_message("Explain database indexing.")

        expected_state = iris.get_flow_state()

        iris.save()

        assert os.path.exists(path)
        assert os.path.exists(path + ".flow.json")

        restored = ConversationIntelligenceV3(path=path)

        assert restored.load() is True
        assert restored.get_flow_state() == expected_state
        assert (
            restored.get_flow_state()["current_topic"]
            == "database indexing"
        )
        assert len(restored.get_flow_state()["transitions"]) == 2

        restored.clear()

        assert restored.get_flow_state()["current_topic"] == ""
        assert restored.get_flow_state()["transitions"] == []
        assert not os.path.exists(path + ".flow.json")

    print("PERSISTENT CONVERSATION FLOW TEST: PASS")


if __name__ == "__main__":
    main()
