import os
import re

from tools.filesystem import FilesystemSearchTool
from tools.file_reader import FileReaderTool
from tools.file_editor import FileEditorTool


class FileControl:
    def __init__(self):
        self.search_tool = FilesystemSearchTool()
        self.reader_tool = FileReaderTool()
        self.editor_tool = FileEditorTool()

    def search(self, directory, query):
        return self.search_tool.execute(
            directory,
            query
        )

    def read(self, path):
        return self.reader_tool.execute(
            path
        )

    def write(self, path, content):
        return self.editor_tool.execute(
            path,
            content
        )

    def execute(self, message):
        text = message.strip()
        lower = text.lower()

        if lower.startswith("find file "):
            query = text[10:].strip()

            if not query:
                return None

            matches = self.search(
                "sandbox",
                query
            )

            if not matches:
                return f"No files found for: {query}"

            return "\n".join(matches)

        if lower.startswith("read file "):
            path = text[10:].strip()

            if not path:
                return None

            if not os.path.exists(path):
                return f"File not found: {path}"

            return self.read(path)

        match = re.match(
            r"create file (.+?) with (.+)",
            text,
            re.IGNORECASE
        )

        if match:
            path = match.group(1).strip()
            content = match.group(2).strip()

            return self.write(
                path,
                content
            )

        return None