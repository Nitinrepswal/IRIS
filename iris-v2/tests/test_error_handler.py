from core.error_handler import ErrorHandler


def main():
    print("IRIS V3.1 ERROR HANDLER TEST")
    print("=" * 50)

    handler = ErrorHandler()

    errors = [
        FileNotFoundError("missing.txt"),
        PermissionError("access denied"),
        TimeoutError("operation timed out"),
        ConnectionError("connection failed"),
        ValueError("unexpected value")
    ]

    passed = 0

    for error in errors:
        result = handler.handle(
            error,
            context="Day 202 test"
        )

        print("\nError:", type(error).__name__)
        print("Response:", result["message"])

        if not result["success"]:
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{len(errors)}")

    if passed == len(errors):
        print("ERROR HANDLER TEST: PASS")
    else:
        print("ERROR HANDLER TEST: FAIL")


if __name__ == "__main__":
    main()