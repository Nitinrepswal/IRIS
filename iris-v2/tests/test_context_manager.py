from core.context_manager import ContextManager


def main():
    print("IRIS V3.1 CONTEXT WINDOW TEST")
    print("=" * 55)

    manager = ContextManager(
        max_messages=4,
        max_characters=100
    )

    messages = [
        {
            "role": "user",
            "content": "Message one"
        },
        {
            "role": "assistant",
            "content": "Response one"
        },
        {
            "role": "user",
            "content": "Message two"
        },
        {
            "role": "assistant",
            "content": "Response two"
        },
        {
            "role": "user",
            "content": "Message three"
        },
        {
            "role": "assistant",
            "content": "Response three"
        }
    ]

    trimmed = manager.trim_messages(messages)

    print("\nOriginal messages:")
    print(len(messages))

    print("\nTrimmed messages:")
    print(len(trimmed))

    for message in trimmed:
        print(message)

    print("\nUsage:")
    print(manager.get_usage(trimmed))

    passed = (
        len(trimmed) <= 4
        and len(trimmed) > 0
        and trimmed[-1]["content"] == "Response three"
        and manager.get_message_count(trimmed)
        == len(trimmed)
    )

    print("\n" + "=" * 55)

    if passed:
        print("CONTEXT WINDOW TEST: PASS")
    else:
        print("CONTEXT WINDOW TEST: FAIL")


if __name__ == "__main__":
    main()