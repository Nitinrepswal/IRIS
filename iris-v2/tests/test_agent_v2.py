from models.llm_model import LLMModel
from core.tool_layer import ToolLayer
from agent.iris_agent import IRISAgent


def main():
    model = LLMModel()
    tool_layer = ToolLayer()

    agent = IRISAgent(
        model,
        tool_layer
    )

    result = agent.run(
        "Find files with 'test' in their filename."
    )

    print("Goal:")
    print(result["goal"])

    print("\nPlan:")
    print(result["plan"])

    print("\nTasks:")

    for task in result["tasks"]:
        print(
            f"{task['step']}. "
            f"{task['action']} → "
            f"{task['target']}"
        )

    print("\nExecution results:")

    for item in result["results"]:
        print(item)

    print("\nGoal state:")
    print(result["goal_state"])

    print("\nEvaluation:")
    print(result["evaluation"])


if __name__ == "__main__":
    main()