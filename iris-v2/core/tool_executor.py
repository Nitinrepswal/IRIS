class ToolExecutor:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def execute(self, tool_name, arguments):
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": "tool_not_found",
                "message": f"Tool not found: {tool_name}",
                "retry": False
            }

        try:
            result = self.tools[tool_name].execute(**arguments)

            return {
                "success": True,
                "result": result,
                "retry": False
            }

        except Exception as error:
            return {
                "success": False,
                "error": "execution_error",
                "message": str(error),
                "retry": True
            }