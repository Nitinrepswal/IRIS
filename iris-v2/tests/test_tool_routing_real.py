
from models.llm_model import LLMModel
from core.intent import IntentDetector


def main():
    print("IRIS REAL INTENT ROUTING EVALUATION")
    print("=" * 55)

    detector = IntentDetector(LLMModel())

    test_cases = [
        ("Hello IRIS", "chat"),
        ("How are you?", "chat"),
        ("What is machine learning?", "information"),
        ("Explain recursion", "information"),
        ("Find my resume", "filesystem"),
        ("Open my resume", "filesystem"),
        ("Remember that I am building IRIS", "memory"),
        ("What do you remember about my project?", "memory"),
        ("Run the Python script", "terminal"),
        ("Execute this command", "terminal"),
    ]

    passed = 0
    failed = 0

    for message, expected in test_cases:
        try:
            result = detector.detect(message)
            actual = result.get("intent", "")

            success = actual == expected

            passed += int(success)
            failed += int(not success)

            print(f"\nRequest:  {message}")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual}")
            print(f"Result:   {'PASS' if success else 'FAIL'}")

        except Exception as error:
            failed += 1
            print(f"\nRequest: {message}")
            print(f"Error: {type(error).__name__}: {error}")
            print("Result: FAIL")

    total = len(test_cases)

    print("\n" + "=" * 55)
    print(f"Total: {total}")
    print(f"Correct: {passed}")
    print(f"Incorrect/errors: {failed}")
    print(f"Accuracy: {passed / total * 100:.1f}%")
    print("REAL MODEL EVALUATION FINISHED")


if __name__ == "__main__":
    main()
