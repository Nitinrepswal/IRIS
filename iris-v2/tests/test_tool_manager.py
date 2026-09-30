from core.tool_manager import ToolManager


def main():
    manager = ToolManager()

    tests = [
        "open calculator",
        "system information",
        "find file e2e_test",
        "open youtube.com"
    ]

    for message in tests:
        print("Command:", message)
        result = manager.execute(message)
        print("Result:", result)
        print()


if __name__ == "__main__":
    main()