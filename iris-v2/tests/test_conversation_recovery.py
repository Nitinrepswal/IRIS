
import json
import os
import tempfile

from core.conversation_intelligence_v3 import ConversationIntelligenceV3


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")
        flow_path = path + ".flow.json"

        iris = ConversationIntelligenceV3(path=path)
        iris.process_user_message("Tell me about Python.")
        iris.process_user_message("Explain database indexing.")
        iris.save()

        expected = iris.get_flow_state()

        # Normal recovery restores the exact flow state.
        restored = ConversationIntelligenceV3(path=path)
        assert restored.load() is True
        assert restored.get_flow_state() == expected

        # Legacy recovery works without a flow-state file.
        os.remove(flow_path)

        legacy = ConversationIntelligenceV3(path=path)
        assert legacy.load() is True
        assert legacy.get_flow_state()["current_topic"] == (
            expected["current_topic"]
        )
        assert legacy.get_flow_state()["transitions"] == (
            expected["transitions"]
        )

        # Corrupted flow data must not replace live conversation state.
        protected = ConversationIntelligenceV3(path=path)
        protected.add_user_message("Keep this conversation.")
        before = protected.get_context()

        with open(flow_path, "w", encoding="utf-8") as file:
            file.write("{invalid json")

        try:
            protected.load()
            raise AssertionError("Corrupted flow file was accepted")
        except ValueError:
            pass

        assert protected.get_context() == before

    print("CONVERSATION RECOVERY TEST: PASS")


if __name__ == "__main__":
    main()
