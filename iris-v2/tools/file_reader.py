from tools.tool import Tool


class FileReaderTool(Tool):
    def __init__(self):
        super().__init__(
            name="file_reader",
            description="Reads the contents of a file."
        )

    def execute(self, path):
        with open(path, "r") as file:
            return file.read()