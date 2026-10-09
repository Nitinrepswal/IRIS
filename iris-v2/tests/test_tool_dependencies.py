
from core.tool_dependencies import ToolDependencyDetector


def main():
    print("IRIS DAY 223 TOOL DEPENDENCY TEST")
    print("=" * 50)

    detector = ToolDependencyDetector()
    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "user's resume"
        },
        {
            "step": 2,
            "action": "read",
            "target": "resume found in step 1"
        },
        {
            "step": 3,
            "action": "summarize",
            "target": "resume content from step 2"
        }
    ]

    result = detector.detect(tasks)

    check("Valid task plan accepted", result["valid"])
    check(
        "Read depends on search",
        result["dependencies"][1]["depends_on"] == [1]
    )
    check(
        "Summarize depends on read",
        result["dependencies"][2]["depends_on"] == [2]
    )
    check(
        "First task has no dependencies",
        result["dependencies"][0]["depends_on"] == []
    )

    result = detector.detect("not a task list")

    check("Invalid task list rejected", result["valid"] is False)

    result = detector.detect([
        {"step": 1, "action": "search", "target": "resume"},
        {"step": 1, "action": "read", "target": "resume"}
    ])

    check("Duplicate step numbers rejected", result["valid"] is False)

    result = detector.detect([
        {"step": "one", "action": "search", "target": "resume"}
    ])

    check("Invalid step number rejected", result["valid"] is False)

    result = detector.detect([
        {"step": 1, "action": "search", "target": "resume"},
        {"step": 2, "action": "read", "target": "resume"}
    ])

    check(
        "Independent tasks stay independent without explicit references",
        result["dependencies"][1]["depends_on"] == []
    )

    print("\n" + "=" * 50)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL DEPENDENCY DETECTION: PASS")
    else:
        print("TOOL DEPENDENCY DETECTION: FAIL")


if __name__ == "__main__":
    main()
