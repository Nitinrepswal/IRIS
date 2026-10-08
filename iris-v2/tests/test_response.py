from core.response import IRISResponse


def main():
    print("IRIS V3.1 UNIFIED RESPONSE TEST")
    print("=" * 50)

    success = IRISResponse.success_response(
        "Hello from IRIS.",
        source="llm"
    )

    error = IRISResponse.error_response(
        "IRIS could not complete the request.",
        source="tool",
        error="ToolExecutionError"
    )

    print("\nSuccess response:")
    print(success.to_dict())

    print("\nError response:")
    print(error.to_dict())

    success_data = success.to_dict()
    error_data = error.to_dict()

    passed = (
        success.success
        and success.response_type == "text"
        and success.source == "llm"
        and success_data["content"] == "Hello from IRIS."
        and not error.success
        and error.response_type == "error"
        and error.source == "tool"
        and error.error == "ToolExecutionError"
    )

    print("\n" + "=" * 50)

    if passed:
        print("UNIFIED RESPONSE TEST: PASS")
    else:
        print("UNIFIED RESPONSE TEST: FAIL")


if __name__ == "__main__":
    main()