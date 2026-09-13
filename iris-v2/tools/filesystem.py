import os

from tools.tool import Tool


class FilesystemSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="filesystem_search",
            description="Searches for files in a directory."
        )

    def execute(self, directory, query):
        matches = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if query.lower() in file.lower():
                    matches.append(os.path.join(root, file))

        return matches