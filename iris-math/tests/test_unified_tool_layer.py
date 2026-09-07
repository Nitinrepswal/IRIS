import os
import platform
import subprocess
from urllib.request import urlopen


class UnifiedToolLayer:
    def filesystem(self, action):
        if action == "list_files":
            return os.listdir(".")

        return "Filesystem action not supported"

    def terminal(self, action):
        commands = {
            "python_version": ["python", "--version"],
            "current_directory": ["pwd"]
        }

        if action not in commands:
            return "Terminal action not supported"

        result = subprocess.run(
            commands[action],
            capture_output=True,
            text=True
        )

        return result.stdout.strip() or result.stderr.strip()

    def system(self, action):
        if action == "info":
            return {
                "os": platform.system(),
                "machine": platform.machine(),
                "python": platform.python_version()
            }

        return "System action not supported"

    def browser(self, action):
        if action == "open_example":
            with urlopen("https://example.com", timeout=10) as response:
                content = response.read().decode("utf-8")

            return f"Webpage loaded: {len(content)} characters"

        return "Browser action not supported"

    def execute(self, tool, action):
        if tool == "filesystem":
            return self.filesystem(action)

        if tool == "terminal":
            return self.terminal(action)

        if tool == "system":
            return self.system(action)

        if tool == "browser":
            return self.browser(action)

        return "Tool not supported"


class IRISUnifiedAgent:
    def __init__(self):
        self.tools = UnifiedToolLayer()

    def run(self):
        requests = [
            ("filesystem", "list_files"),
            ("terminal", "python_version"),
            ("system", "info"),
            ("browser", "open_example")
        ]

        for tool, action in requests:
            print("\nTOOL")
            print(tool)

            print("ACTION")
            print(action)

            print("OBSERVATION")
            print(self.tools.execute(tool, action))


agent = IRISUnifiedAgent()

print("=" * 40)
print("IRIS UNIFIED TOOL LAYER")
print("=" * 40)

agent.run()