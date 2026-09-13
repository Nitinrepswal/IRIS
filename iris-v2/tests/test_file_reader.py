import os

from tools.file_editor import FileEditorTool
from tools.file_reader import FileReaderTool


def main():
    editor = FileEditorTool()
    reader = FileReaderTool()

    path = "test_file.txt"

    editor.execute(
        path=path,
        content="IRIS can read files."
    )

    content = reader.execute(path)

    print("Tool:", reader.name)
    print("Description:", reader.description)
    print("File content:", content)

    os.remove(path)

    print("Test file removed.")


if __name__ == "__main__":
    main()