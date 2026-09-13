class ToolExecutor:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def execute(self, tool_name, arguments):
        if tool_name not in self.tools:
            return {
                "success": False,
                "result": f"Tool not found: {tool_name}"
            }

        try:
            result = self.tools[tool_name].execute(**arguments)

            return {
                "success": True,
                "result": result
            }

        except Exception as error:
            return {
                "success": False,
                "result": str(error)
            }