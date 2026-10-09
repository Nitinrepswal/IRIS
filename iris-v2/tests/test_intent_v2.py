
from core.intent import IntentDetector


class MockModel:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def structured_chat(self, messages):
        if self.error:
            raise self.error
        return self.result


def main():
    print("IRIS V2 INTENT CLASSIFICATION TEST")
    print("=" * 55)

    results = []

    def check(name, condition):
        results.append(bool(condition))
        print(f"{'PASS' if condition else 'FAIL'}: {name}")

    detector = IntentDetector(
        MockModel({
            "intent": "filesystem",
            "reason": "The user wants to find a file.",
            "confidence": 0.95
        })
    )

    result = detector.detect("Find my project")

    check("Valid intent is returned", result["intent"] == "filesystem")
    check("Reason is preserved", bool(result["reason"]))
    check("Confidence is preserved", result["confidence"] == 0.95)

    detector = IntentDetector(
        MockModel({
            "intent": "unknown_action",
            "reason": "Invalid category",
            "confidence": 0.9
        })
    )

    result = detector.detect("Do something")

    check("Unknown intent uses fallback", result["intent"] == "information")
    check("Fallback confidence is zero", result["confidence"] == 0.0)

    detector = IntentDetector(
        MockModel({
            "intent": "memory",
            "reason": "Remembering information",
            "confidence": 4
        })
    )

    result = detector.detect("Remember my project")

    check("Confidence is bounded", result["confidence"] == 1.0)

    detector = IntentDetector(
        MockModel(error=RuntimeError("Model unavailable"))
    )

    result = detector.detect("Run a command")

    check("Model failure is handled", result["intent"] == "information")
    check("Failure confidence is zero", result["confidence"] == 0.0)

    result = detector.detect("")

    check("Empty input is handled", result["confidence"] == 0.0)

    print("\n" + "=" * 55)
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("INTENT CLASSIFICATION V2: PASS")
    else:
        print("INTENT CLASSIFICATION V2: FAIL")


if __name__ == "__main__":
    main()
