from core.tool_layer import ToolLayer
from core.multi_step_executor import MultiStepExecutor


def main():
    tool_layer = ToolLayer()
    executor = MultiStepExecutor(tool_layer)

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "test"
        },
        {
            "step": 2,
            "action": "read",
            "target": "tools/tool.py"
        },
        {
            "step": 3,
            "action": "unknown",
            "target": "something"
        }
    ]

    results = executor.execute(tasks)

    print("Execution results:")

    for result in results:
        print("\nStep:", result["step"])

        if "action" in result:
            print("Action:", result["action"])

        if "target" in result:
            print("Target:", result["target"])

        print("Result:", result)


if __name__ == "__main__":
    main()