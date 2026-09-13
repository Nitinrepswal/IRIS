from core.tool_executor import ToolExecutor
from tools.file_reader import FileReaderTool


def main():
    executor = ToolExecutor()

    executor.register(FileReaderTool())

    result = executor.execute(
        "file_reader",
        {
            "path": "does_not_exist.txt"
        }
    )

    print("Failed tool execution:")
    print(result)

    missing_tool = executor.execute(
        "unknown_tool",
        {}
    )

    print("\nMissing tool:")
    print(missing_tool)


if __name__ == "__main__":
    main()