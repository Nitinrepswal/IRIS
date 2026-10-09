
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
    print("IRIS DAY 219 TOOL SELECTION SCORING TEST")
    print("=" * 55)

    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    selector = ToolSelector(
        MockModel({
            "tool": "filesystem_search",
            "reason": "The request asks to find a file."
        })
    )

    result = selector.select(
        "Where did I save my resume?",
        "filesystem"
    )

    check("Existing selection interface works",
          result["tool"] == "filesystem_search")

    check("Scores returned for candidates",
          isinstance(result["scores"], dict)
          and "terminal" in result["scores"])

    check("Scores sorted from highest to lowest",
          list(result["scores"].values())
          == sorted(result["scores"].values(), reverse=True))

    check("Suggested tool receives a scoring bonus",
          result["scores"]["filesystem_search"]
          > result["scores"]["filesystem_edit"])

    scores = selector.score_candidates(
        "Run my Python script",
        "terminal"
    )

    check("Terminal ranks first for terminal intent",
          max(scores, key=scores.get) == "terminal")

    check("High-risk tools require confirmation",
          selector.registry.get("terminal")["requires_confirmation"]
          is True)

    invalid_selector = ToolSelector(
        MockModel({
            "tool": "delete_everything",
            "reason": "Invalid tool"
        })
    )

    invalid_result = invalid_selector.select(
        "Clean up my files",
        "filesystem"
    )

    check("Unknown tool rejected",
          invalid_result["tool"] == "none")

    failed_selector = ToolSelector(
        MockModel(error=RuntimeError("Model unavailable"))
    )

    failed_result = failed_selector.select(
        "Run my script",
        "terminal"
    )

    check("Model failure handled safely",
          failed_result["tool"] == "none")

    empty_result = selector.select("", "chat")

    check("Empty request handled",
          empty_result["tool"] == "none")

    print("\n" + "=" * 55)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("TOOL SELECTION SCORING: PASS")
    else:
        print("TOOL SELECTION SCORING: FAIL")


if __name__ == "__main__":
    main()
