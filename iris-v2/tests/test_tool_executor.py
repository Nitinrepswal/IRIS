from core.tool_executor import ToolExecutor
from tools.filesystem import FilesystemSearchTool
from tools.file_reader import FileReaderTool


def main():
    executor = ToolExecutor()

    executor.register(FilesystemSearchTool())
    executor.register(FileReaderTool())

    search_result = executor.execute(
        "filesystem_search",
        {
            "directory": ".",
            "query": "resume"
        }
    )

    print("Filesystem search:")
    print(search_result)

    reader_result = executor.execute(
        "file_reader",
        {
            "path": "tools/test_tool.py"
        }
    )

    print("\nFile reader:")
    print(reader_result)


if __name__ == "__main__":
    main()