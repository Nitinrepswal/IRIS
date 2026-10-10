
from core.conversation_intelligence import ConversationIntelligence


def main():
    intelligence = ConversationIntelligence()

    intelligence.add_user_message("Tell me about Python.")
    intelligence.add_assistant_message(
        "Python is a programming language."
    )

    result = intelligence.analyze_message("What are its uses?")

    assert result["follow_up"]["type"] == "follow_up"
    assert result["reference"]["resolved"] is True
    assert result["reference"]["subject"] == "Python"
    assert result["current_topic"] == "Python"

    intelligence.add_user_message("What are its uses?")
    intelligence.add_assistant_message(
        "Python is used for automation and data analysis."
    )

    context = intelligence.get_context()
    assert context["turn_count"] == 2
    assert context["message_count"] == 4

    intelligence.clear()

    context = intelligence.get_context()
    assert context["messages"] == []
    assert context["turn_count"] == 0
    assert intelligence.topic_tracker.get_topic() == ""

    try:
        intelligence.analyze_message("")
        raise AssertionError("Empty messages should be rejected")
    except ValueError:
        pass

    print("CONVERSATION INTELLIGENCE V2 TEST: PASS")


if __name__ == "__main__":
    main()
