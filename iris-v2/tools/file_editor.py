from tools.tool import Tool


class FileEditorTool(Tool):
    def __init__(self):
        super().__init__(
            name="file_editor",
            description="Creates and edits files."
        )

    def execute(self, path, content):
        with open(path, "w") as file:
            file.write(content)

        return f"File written successfully: {path}"