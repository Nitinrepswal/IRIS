from models.llm_model import LLMModel
from core.tool_selector import ToolSelector


def main():
    model = LLMModel()
    selector = ToolSelector(model)

    tests = [
        {
            "message": "Find my resume.",
            "intent": "filesystem"
        },
        {
            "message": "Remember that I am building IRIS.",
            "intent": "memory"
        },
        {
            "message": "Run the Python script.",
            "intent": "terminal"
        },
        {
            "message": "What is machine learning?",
            "intent": "information"
        }
    ]

    for test in tests:
        result = selector.select(
            test["message"],
            test["intent"]
        )

        print("\nUser:", test["message"])
        print("Intent:", test["intent"])
        print("Tool:", result["tool"])
        print("Reason:", result.get("reason", "No reason provided"))


if __name__ == "__main__":
    main()