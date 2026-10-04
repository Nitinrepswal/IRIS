from plugins.base import Plugin


class HelloPlugin(Plugin):
    name = "hello"
    description = "Provides a simple plugin test."

    def execute(self, message):
        return {
            "success": True,
            "message": f"Hello from plugin: {message}"
        }