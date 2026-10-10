
from core.conversation_intelligence import ConversationIntelligence


def main():
    intelligence = ConversationIntelligence(
        max_messages=4,
        max_characters=100
    )

    intelligence.add_user_message("Hello IRIS")
    intelligence.add_assistant_message("Hello! How can I help?")
    intelligence.add_user_message("Tell me about Python")
    intelligence.add_assistant_message("Python is a programming language.")
    intelligence.add_user_message("What about its uses?")

    context = intelligence.get_context()

    assert context["last_user_message"] == "What about its uses?"
    assert context["turn_count"] == 3
    assert len(context["messages"]) <= 4
    assert context["character_count"] <= 100

    intelligence.set_topic("Python")
    assert intelligence.get_context()["topic"] == "Python"

    intelligence.clear()
    context = intelligence.get_context()

    assert context["messages"] == []
    assert context["turn_count"] == 0
    assert context["topic"] == ""

    try:
        intelligence.add_user_message("   ")
        raise AssertionError("Empty message should be rejected")
    except ValueError:
        pass

    print("CONVERSATION INTELLIGENCE TEST: PASS")


if __name__ == "__main__":
    main()
