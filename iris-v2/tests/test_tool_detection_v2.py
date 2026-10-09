
from core.tool_selector import ToolSelector


class MockModel:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def structured_chat(self, messages):
        if self.error:
            raise self.error

        return self.result


def main():
    print("IRIS DAY 217 TOOL DETECTION TEST")
    print("=" * 55)

    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    cases = [
        ("Where did I save my resume?", "filesystem_search"),
        ("What did I tell you about my project?", "memory"),
        ("Please run my Python script", "terminal"),
        ("Explain how Python works", "none"),
    ]

    for message, expected in cases:
        model = MockModel({
            "tool": expected,
            "reason": "Mock classification"
        })

        selector = ToolSelector(model)
        result = selector.select(message, "test")

        check(
            f"{message} -> {expected}",
            result["tool"] == expected
        )

    selector = ToolSelector(
        MockModel({
            "tool": "delete_everything",
            "reason": "Invalid tool"
        })
    )

    result = selector.select("Clean up my files", "filesystem")

    check(
        "Unknown tool rejected",
        result["tool"] == "none"
    )

    selector = ToolSelector(
        MockModel(error=RuntimeError("Model unavailable"))
    )

    result = selector.select("Run my script", "terminal")

    check(
        "Model failure handled safely",
        result["tool"] == "none"
    )

    selector = ToolSelector(MockModel())
    result = selector.select("", "chat")

    check(
        "Empty request handled",
        result["tool"] == "none"
    )

    print("\n" + "=" * 55)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL DETECTION V2: PASS")
    else:
        print("TOOL DETECTION V2: FAIL")


if __name__ == "__main__":
    main()
