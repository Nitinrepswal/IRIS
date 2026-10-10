
import json
from collections import defaultdict
from pathlib import Path

from models.llm_model import LLMModel
from core.tool_selector import ToolSelector


def main():
    dataset_path = Path("data/routing_evaluation.json")

    with dataset_path.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("Routing dataset must be a non-empty JSON list.")

    required_fields = {
        "id",
        "message",
        "expected_intent",
        "expected_tool",
    }

    for index, case in enumerate(dataset):
        if not isinstance(case, dict):
            raise ValueError(f"Dataset entry {index} must be a dictionary.")

        missing = required_fields - case.keys()
        if missing:
            raise ValueError(
                f"Dataset entry {index} is missing: {sorted(missing)}"
            )

    model = LLMModel()
    selector = ToolSelector(model)

    total = 0
    correct = 0
    per_tool = defaultdict(lambda: {"total": 0, "correct": 0})
    failures = []

    print("\nIRIS DAY 233 — ROUTING BENCHMARK")
    print("=" * 45)

    for case in dataset:
        case_id = case["id"]
        message = case["message"]
        intent = case["expected_intent"]
        expected = case["expected_tool"]

        try:
            result = selector.select(message, intent)

            if not isinstance(result, dict):
                raise ValueError("Selector returned a non-dictionary result.")

            predicted = result.get("tool", "none")

        except Exception as error:
            predicted = "ERROR"
            print(f"\nError on case {case_id}: {error}")

        passed = predicted == expected
        total += 1
        per_tool[expected]["total"] += 1

        if passed:
            correct += 1
            per_tool[expected]["correct"] += 1
        else:
            failures.append(
                {
                    "id": case_id,
                    "message": message,
                    "expected": expected,
                    "predicted": predicted,
                }
            )

        status = "PASS" if passed else "FAIL"
        print(
            f"[{status}] {case_id}: "
            f"expected={expected}, predicted={predicted}"
        )

    accuracy = correct / total * 100

    print("\n" + "=" * 45)
    print("OVERALL RESULTS")
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2f}%")

    print("\nPER-TOOL RESULTS")
    for tool in sorted(per_tool):
        stats = per_tool[tool]
        count = stats["total"]
        tool_accuracy = stats["correct"] / count * 100

        print(
            f"{tool}: {stats['correct']}/{count} "
            f"({tool_accuracy:.2f}%)"
        )

    print("\nFAILED CASES")
    if failures:
        for failure in failures:
            print(
                f"#{failure['id']}: {failure['message']}\n"
                f"  Expected: {failure['expected']}\n"
                f"  Predicted: {failure['predicted']}"
            )
    else:
        print("None — every case passed.")

    print("\nBenchmark finished. No tools were executed.")


if __name__ == "__main__":
    main()
