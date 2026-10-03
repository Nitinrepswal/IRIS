from core.autonomous_task import AutonomousTaskEngine
from core.tool_layer import ToolLayer


def main():
    tool_layer = ToolLayer()

    engine = AutonomousTaskEngine(
        tool_layer,
        max_retries=2
    )

    tasks = [
        {
            "step": 1,
            "action": "search",
            "target": "advanced_planning",
            "tool": "filesystem_search"
        },
        {
            "step": 2,
            "action": "search",
            "target": "task_state",
            "tool": "filesystem_search"
        }
    ]

    result = engine.execute(
        "Find files related to planning and task state",
        tasks
    )

    print("Autonomous task result:")
    print(result)

    print("\nStep results:")

    for item in result["results"]:
        print(
            f"Step {item['step']}: "
            f"{item['status'] if 'status' in item else item['success']}"
        )


if __name__ == "__main__":
    main()