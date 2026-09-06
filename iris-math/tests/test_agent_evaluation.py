class AgentEvaluator:
    def __init__(self):
        self.results = []

    def evaluate(self, test_name, actual, expected):
        passed = actual == expected

        self.results.append({
            "test": test_name,
            "actual": actual,
            "expected": expected,
            "passed": passed
        })

        print(f"Test: {test_name}")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")
        print(f"Passed: {passed}")
        print("-" * 40)

    def summary(self):
        total = len(self.results)
        passed = sum(result["passed"] for result in self.results)

        accuracy = passed / total if total else 0

        print("AGENT EVALUATION")
        print("================")
        print(f"Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Accuracy: {accuracy:.2f}")


def detect_intent(message):
    message = message.lower()

    if "weather" in message:
        return "weather"

    if "resume" in message or "file" in message:
        return "file"

    if "calculate" in message:
        return "calculation"

    if "what is" in message:
        return "question"

    return "unknown"


def select_tool(intent):
    tools = {
        "weather": "weather_tool",
        "file": "file_tool",
        "calculation": "calculator_tool",
        "question": "knowledge_tool",
        "unknown": "no_tool"
    }

    return tools.get(intent, "no_tool")


def evaluate_agent():
    evaluator = AgentEvaluator()

    test_cases = [
        {
            "name": "Weather intent",
            "message": "What's the weather in Delhi?",
            "expected_intent": "weather",
            "expected_tool": "weather_tool"
        },
        {
            "name": "File intent",
            "message": "Open my resume.",
            "expected_intent": "file",
            "expected_tool": "file_tool"
        },
        {
            "name": "Calculation intent",
            "message": "Calculate 25 multiplied by 4.",
            "expected_intent": "calculation",
            "expected_tool": "calculator_tool"
        },
        {
            "name": "Question intent",
            "message": "What is machine learning?",
            "expected_intent": "question",
            "expected_tool": "knowledge_tool"
        }
    ]

    for case in test_cases:
        actual_intent = detect_intent(case["message"])

        evaluator.evaluate(
            case["name"] + " - Intent",
            actual_intent,
            case["expected_intent"]
        )

        actual_tool = select_tool(actual_intent)

        evaluator.evaluate(
            case["name"] + " - Tool",
            actual_tool,
            case["expected_tool"]
        )

    evaluator.summary()


evaluate_agent()