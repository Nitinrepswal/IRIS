from core.multi_step_executor import MultiStepExecutor
from core.tool_layer import ToolLayer


def main():
    tool_layer = ToolLayer()
    executor = MultiStepExecutor(tool_layer)

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "test",
            "tool": "filesystem_search"
        }
    ]

    results = executor.execute(tasks)

    print("Execution results:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()