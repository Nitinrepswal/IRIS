
import os

from tools.tool import Tool


class FilesystemSearchTool(Tool):
    SKIP_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".Trash",
        "Library",
    }

    def __init__(self):
        super().__init__(
            name="filesystem_search",
            description="Searches for files in a directory.",
        )

    def execute(self, directory, query):
        query = query.strip().casefold()
        if not query:
            return []

        if directory == "sandbox":
            directory = os.path.expanduser("~")
        else:
            directory = os.path.abspath(
                os.path.expanduser(directory)
            )

        if not os.path.isdir(directory):
            return []

        matches = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                name for name in dirs
                if name not in self.SKIP_DIRS
            ]

            for filename in files:
                if query in filename.casefold():
                    matches.append(
                        os.path.join(root, filename)
                    )

                    if len(matches) >= 100:
                        return matches

        return matches
