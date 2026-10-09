
from core.missing_arguments import MissingArgumentDetector


def main():
    print("IRIS DAY 221 MISSING ARGUMENT DETECTION TEST")
    print("=" * 55)

    detector = MissingArgumentDetector()
    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    result = detector.detect(
        "filesystem_search",
        {"directory": ".", "query": "resume"}
    )

    check("Complete search arguments accepted", result["valid"])
    check("No missing arguments reported", result["missing"] == [])

    result = detector.detect(
        "file_reader",
        {}
    )

    check("Missing file path detected", result["missing"] == ["path"])
    check("File path clarification generated", len(result["questions"]) == 1)

    result = detector.detect(
        "filesystem_search",
        {"directory": ".", "query": ""}
    )

    check("Empty search query detected", result["missing"] == ["query"])

    result = detector.detect(
        "file_editor",
        {"path": "hello.txt", "content": ""}
    )

    check("Missing file content detected", result["missing"] == ["content"])

    result = detector.detect(
        "terminal",
        {"command": "   "}
    )

    check("Whitespace-only command detected", result["missing"] == ["command"])

    result = detector.detect("unknown_tool", {})

    check("Unsupported tool rejected", result["valid"] is False)

    result = detector.detect("file_reader", None)

    check("Invalid argument structure handled", result["valid"] is False)

    result = detector.detect(
        "terminal",
        {"command": "ls"}
    )

    check("Complete terminal arguments accepted", result["valid"])

    print("\n" + "=" * 55)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("MISSING ARGUMENT DETECTION: PASS")
    else:
        print("MISSING ARGUMENT DETECTION: FAIL")


if __name__ == "__main__":
    main()
