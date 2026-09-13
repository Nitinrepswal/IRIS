from core.tool_layer import ToolLayer


def main():
    tools = ToolLayer()

    print("Registered tools:")

    for tool in tools.list_tools():
        print(f"- {tool.name}: {tool.description}")

    result = tools.execute(
        "filesystem_search",
        {
            "directory": ".",
            "query": "test"
        }
    )

    print("\nFilesystem result:")
    print(result)

    result = tools.execute(
        "terminal",
        {
            "command": "echo IRIS Tools V1"
        }
    )

    print("\nTerminal result:")
    print(result)


if __name__ == "__main__":
    main()