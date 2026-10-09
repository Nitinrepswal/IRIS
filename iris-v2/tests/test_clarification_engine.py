
from core.clarification_engine import ClarificationEngine


def main():
    print("IRIS DAY 222 CLARIFICATION ENGINE TEST")
    print("=" * 50)

    engine = ClarificationEngine()
    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    result = engine.generate([])

    check(
        "No question when arguments are complete",
        result["valid"] and not result["needs_clarification"]
    )

    result = engine.generate(["path"])

    check(
        "Single missing argument creates a question",
        result["needs_clarification"]
        and "file path" in result["question"]
    )

    result = engine.generate(["directory", "query"])

    check(
        "Multiple missing arguments create questions",
        result["needs_clarification"]
        and len(result["missing_arguments"]) == 2
        and "directory" in result["question"].lower()
        and "search" in result["question"].lower()
    )

    result = engine.generate(["path", "path"])

    check(
        "Duplicate arguments are removed",
        result["missing_arguments"] == ["path"]
    )

    result = engine.generate(["unknown"])

    check(
        "Unknown argument rejected",
        result["valid"] is False
    )

    result = engine.generate("path")

    check(
        "Invalid input type handled",
        result["valid"] is False
    )

    result = engine.generate(["command"])

    check(
        "Terminal command clarification generated",
        result["question"] == "Which command do you want to run?"
    )

    print("\n" + "=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("CLARIFICATION ENGINE: PASS")
    else:
        print("CLARIFICATION ENGINE: FAIL")


if __name__ == "__main__":
    main()
