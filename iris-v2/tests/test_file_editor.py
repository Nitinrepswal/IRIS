import os

from tools.file_editor import FileEditorTool


def main():
    tool = FileEditorTool()

    path = "test_file.txt"

    result = tool.execute(
        path=path,
        content="Hello from IRIS."
    )

    print("Tool:", tool.name)
    print("Result:", result)

    with open(path, "r") as file:
        content = file.read()

    print("File content:", content)

    os.remove(path)

    print("Test file removed.")


if __name__ == "__main__":
    main()