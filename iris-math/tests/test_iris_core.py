from pathlib import Path


class IRISCore:
    def __init__(self):
        self.memory = []
        self.tools = {
            "list_files": self.list_files,
            "system_info": self.system_info
        }

    def remember(self, message):
        self.memory.append(message)

    def retrieve_memory(self):
        return self.memory[-5:]

    def detect_intent(self, message):
        message = message.lower()

        if "remember" in message:
            return "memory"

        if "files" in message or "folder" in message:
            return "filesystem"

        if "system" in message or "os" in message:
            return "system"

        return "chat"

    def list_files(self):
        files = [item.name for item in Path(".").iterdir()]
        return files[:10]

    def system_info(self):
        import platform

        return {
            "system": platform.system(),
            "architecture": platform.machine()
        }

    def execute_tool(self, tool_name):
        tool = self.tools.get(tool_name)

        if tool is None:
            return "Tool not available"

        return tool()

    def process(self, message):
        intent = self.detect_intent(message)

        self.remember(message)

        if intent == "memory":
            return {
                "intent": intent,
                "memory": self.retrieve_memory()
            }

        if intent == "filesystem":
            result = self.execute_tool("list_files")
            return {
                "intent": intent,
                "tool": "list_files",
                "result": result
            }

        if intent == "system":
            result = self.execute_tool("system_info")
            return {
                "intent": intent,
                "tool": "system_info",
                "result": result
            }

        return {
            "intent": "chat",
            "response": f"IRIS received: {message}"
        }


if __name__ == "__main__":
    iris = IRISCore()

    tests = [
        "Hello IRIS",
        "What files are here?",
        "What system am I using?",
        "Remember that I am learning AI engineering"
    ]

    for message in tests:
        print(f"\nUser: {message}")

        result = iris.process(message)

        print("IRIS:", result)