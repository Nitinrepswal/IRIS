
import os
import tempfile

from core.conversation_intelligence_v3 import ConversationIntelligenceV3


def main():
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "context.json")

        iris = ConversationIntelligenceV3(path=path)

        # Process a complete conversation.
        first = iris.process_user_message(
            "Tell me about Python programming."
        )
        iris.add_assistant_message(
            "Python is a programming language."
        )

        second = iris.process_user_message(
            "Explain Python functions."
        )
        iris.add_assistant_message(
            "Functions are reusable blocks of code."
        )

        assert isinstance(first, dict)
        assert isinstance(second, dict)

        # Verify conversation analysis.
        analysis = iris.analyze_message(
            "Can you explain Python functions again?"
        )
        assert isinstance(analysis, dict)

        # Verify search and retrieval.
        results = iris.search("Python")
        assert isinstance(results, list)
        assert len(results) > 0

        retrieved = iris.retrieve("Python")
        assert isinstance(retrieved, dict)
        assert retrieved["count"] > 0

        # Verify context construction.
        context = iris.build_context("Python")
        assert isinstance(context, dict)
        assert isinstance(context["context"], str)
        assert context["count"] > 0

        # Save the complete conversation and flow.
        expected_flow = iris.get_flow_state()
        iris.save()

        assert os.path.exists(path)
        assert os.path.exists(path + ".flow.json")

        # Recover everything in a fresh instance.
        restored = ConversationIntelligenceV3(path=path)

        assert restored.load() is True
        assert restored.get_flow_state() == expected_flow

        restored_results = restored.search("Python")
        assert len(restored_results) > 0

        restored_context = restored.build_context("Python")
        assert restored_context["count"] > 0

        # Verify cleanup.
        restored.clear()

        assert restored.get_flow_state()["transitions"] == []
        assert restored.get_flow_state()["current_topic"] == ""
        assert not os.path.exists(path + ".flow.json")

    print("CONVERSATION INTELLIGENCE V2 INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
