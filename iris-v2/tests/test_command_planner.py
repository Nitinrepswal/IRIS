from models.llm_model import LLMModel
from core.command_planner import CommandPlanner


def main():
    model = LLMModel()
    planner = CommandPlanner(model)

    messages = [
        "Show me the files in this folder.",
        "What directory am I in?",
        "Print hello from IRIS."
    ]

    for message in messages:
        result = planner.plan(message)

        print("\nUser:", message)
        print("Command:", result["command"])
        print("Reason:", result.get("reason", "No reason provided"))


if __name__ == "__main__":
    main()