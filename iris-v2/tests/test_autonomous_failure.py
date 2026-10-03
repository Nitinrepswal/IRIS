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
            "target": "anything",
            "tool": "unknown_tool"
        }
    ]

    result = engine.execute(
        "Test autonomous failure recovery",
        tasks
    )

    print("Failure test result:")
    print(result)

    print("\nStatus:", result["status"])
    print("Current step:", result["current_step"])
    print("Attempts:", result["results"][0]["attempts"])


if __name__ == "__main__":
    main()