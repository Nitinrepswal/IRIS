from core.tool_layer import ToolLayer
from core.recovery import RecoveryEngine


def main():
    tool_layer = ToolLayer()
    recovery = RecoveryEngine(max_retries=2)

    print("Successful execution:")

    result = recovery.recover(
        tool_layer.execute,
        "terminal",
        {
            "command": "echo IRIS"
        }
    )

    print(result)

    print("\nFailed execution:")

    result = recovery.recover(
        tool_layer.execute,
        "file_reader",
        {
            "path": "does_not_exist.txt"
        }
    )

    print(result)

    print("\nNon-retryable failure:")

    result = recovery.recover(
        tool_layer.execute,
        "unknown_tool",
        {}
    )

    print(result)


if __name__ == "__main__":
    main()