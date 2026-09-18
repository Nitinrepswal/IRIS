from models.llm_model import LLMModel
from core.planner import PlanningEngine


def main():
    model = LLMModel()
    planner = PlanningEngine(model)

    messages = [
        "Find my resume.",
        "Find my resume and read it.",
        "Find my resume, read it, and summarize it."
    ]

    for message in messages:
        result = planner.plan(message)

        print("\nUser:", message)
        print("Goal:", result["goal"])
        print("Steps:")

        for index, step in enumerate(
            result["steps"],
            start=1
        ):
            print(f"{index}. {step}")


if __name__ == "__main__":
    main()