
from core.context_manager import ContextManager


def main():
    print("IRIS V3.1 BUG FIX TESTS")
    print("=" * 55)

    results = []

    def check(name, condition):
        results.append((name, bool(condition)))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    manager = ContextManager(
        max_messages=3,
        max_characters=10
    )

    oversized = [
        {"role": "user", "content": "A" * 30}
    ]

    trimmed = manager.trim_messages(oversized)

    check(
        "Oversized message respects character limit",
        manager.get_character_count(trimmed) <= 10
    )

    check(
        "Newest message content is preserved",
        trimmed[-1]["content"] == "A" * 10
    )

    messages = [
        {"role": "user", "content": "1234"},
        {"role": "assistant", "content": "5678"},
        {"role": "user", "content": "90AB"}
    ]

    trimmed = manager.trim_messages(messages)

    check(
        "Character limit is respected",
        manager.get_character_count(trimmed) <= 10
    )

    check(
        "Message count limit is respected",
        manager.get_message_count(trimmed) <= 3
    )

    check(
        "Newest message is retained",
        trimmed[-1]["content"] == "90AB"
    )

    empty = manager.trim_messages([])

    check(
        "Empty conversation is handled",
        empty == []
    )

    safe_manager = ContextManager(
        max_messages=0,
        max_characters=0
    )

    check(
        "Invalid limits are made safe",
        safe_manager.max_messages == 1
        and safe_manager.max_characters == 1
    )

    print("\n" + "=" * 55)

    passed = sum(success for _, success in results)
    failed = len(results) - passed

    print(f"Total: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print(
        "BUG FIX TESTS: "
        + ("PASS" if failed == 0 else "FAIL")
    )


if __name__ == "__main__":
    main()
