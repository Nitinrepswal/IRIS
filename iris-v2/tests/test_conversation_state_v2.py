from core.conversation_state import ConversationState


def main():
    print("IRIS V3.1 CONVERSATION STATE V2 TEST")
    print("=" * 55)

    state = ConversationState()

    state.set_topic("IRIS development")

    state.add_user_message(
        "How can I improve IRIS?"
    )

    state.add_assistant_message(
        "We can improve its reasoning and memory."
    )

    state.add_user_message(
        "What should I work on next?"
    )

    state.add_assistant_message(
        "Focus on conversation context."
    )

    print("\nMessages:")

    for message in state.get_messages():
        print(message)

    print("\nRecent messages:")
    print(
        state.get_recent_messages(2)
    )

    print("\nConversation context:")
    print(
        state.get_context()
    )

    print("\nTurn count:")
    print(
        state.get_turn_count()
    )

    context = state.get_context()

    passed = (
        len(state.get_messages()) == 4
        and len(state.get_recent_messages(2)) == 2
        and context["topic"] == "IRIS development"
        and context["last_user_message"]
        == "What should I work on next?"
        and context["last_response"]
        == "Focus on conversation context."
        and context["turn_count"] == 2
    )

    state.clear()

    passed = (
        passed
        and len(state.get_messages()) == 0
        and state.get_turn_count() == 0
        and state.get_context()["topic"] == ""
    )

    print("\n" + "=" * 55)

    if passed:
        print("CONVERSATION STATE V2 TEST: PASS")
    else:
        print("CONVERSATION STATE V2 TEST: FAIL")


if __name__ == "__main__":
    main()