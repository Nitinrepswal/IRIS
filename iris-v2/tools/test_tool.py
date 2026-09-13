from tools.tool import Tool


class EchoTool(Tool):
    def __init__(self):
        super().__init__(
            name="echo",
            description="Returns the provided message."
        )

    def execute(self, message):
        return message