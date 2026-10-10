
from core.conversation_flow_manager import ConversationFlowManager


def main():
    manager = ConversationFlowManager()

    first = manager.process("Tell me about Python.")

    assert first["action"] == "new_topic"
    assert first["topic"] == "Python"

    second = manager.process("Explain database indexing.")

    assert second["action"] == "new_topic"
    assert second["previous_topic"] == "Python"
    assert second["topic"] == "database indexing"

    state = manager.get_state()

    assert state["current_topic"] == "database indexing"
    assert len(state["transitions"]) == 2
    assert state["transitions"][0]["from"] == ""
    assert state["transitions"][0]["to"] == "Python"
    assert state["transitions"][1]["from"] == "Python"
    assert state["transitions"][1]["to"] == "database indexing"

    empty = manager.process("")

    assert empty["action"] == "clarify"
    assert manager.get_state()["current_topic"] == "database indexing"

    manager.clear()

    state = manager.get_state()

    assert state["current_topic"] == ""
    assert state["last_action"] == "start"
    assert state["transitions"] == []

    print("CONVERSATION FLOW MANAGER TEST: PASS")


if __name__ == "__main__":
    main()
