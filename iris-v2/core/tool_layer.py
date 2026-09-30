from core.tool_registry import ToolRegistry
from core.tool_executor import ToolExecutor

from tools.filesystem import FilesystemSearchTool
from tools.file_editor import FileEditorTool
from tools.file_reader import FileReaderTool
from tools.terminal import TerminalTool


class ToolLayer:
    def __init__(self):
        self.registry = ToolRegistry()
        self.executor = ToolExecutor()

        self._register_tools()

    def _register_tools(self):
        tools = [
            FilesystemSearchTool(),
            FileEditorTool(),
            FileReaderTool(),
            TerminalTool()
        ]

        for tool in tools:
            self.registry.register(tool)
            self.executor.register(tool)

    def execute(self, tool_name, arguments):
        return self.executor.execute(
            tool_name,
            arguments
        )

    def list_tools(self):
        return self.registry.list_tools()

    def tool_names(self):
        return [
            tool.name
            for tool in self.registry.list_tools()
        ]

    def tool_status(self):
        return {
            tool.name: {
                "available": True,
                "description": tool.description
            }
            for tool in self.registry.list_tools()
        }