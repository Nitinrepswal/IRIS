
from models.llm_model import LLMModel
from core.intent import IntentDetector
from core.conversation_state import ConversationState
from core.response import IRISResponse


def main():
    print("IRIS V3.1 REAL-WORLD USAGE TEST")
    print("=" * 55)

    model = LLMModel()
    detector = IntentDetector(model)
    state = ConversationState()

    cases = [
        ("Hey IRIS, how are you?", "chat"),
        ("Explain what an API is", "information"),
        ("Find my project notes", "filesystem"),
        ("Remember that I am building IRIS", "memory"),
        ("Run the Python script", "terminal"),
    ]

    passed = 0
    failed = 0

    for message, expected in cases:
        print(f"\nRequest: {message}")

        try:
            result = detector.detect(message)
            actual = result.get("intent", "")

            state.add_user_message(message)

            if actual == expected:
                answer = f"Intent identified: {actual}"
                response = IRISResponse.success_response(
                    answer,
                    source="intent"
                )
                state.add_assistant_message(response.content)
                passed += 1
                print(f"Intent: {actual}")
                print("Result: PASS")
            else:
                failed += 1
                print(f"Expected: {expected}")
                print(f"Actual: {actual}")
                print("Result: FAIL")

        except Exception as error:
            failed += 1
            print(f"Error: {type(error).__name__}: {error}")
            print("Result: FAIL")

    print("\n" + "=" * 55)
    print(f"Total scenarios: {len(cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Conversation turns: {state.get_turn_count()}")
    print(f"Stored messages: {len(state.get_messages())}")

    if failed == 0:
        print("REAL-WORLD USAGE TEST: PASS")
    else:
        print("REAL-WORLD USAGE TEST: NEEDS REVIEW")


if __name__ == "__main__":
    main()
