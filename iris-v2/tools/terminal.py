import subprocess

from tools.tool import Tool


class TerminalTool(Tool):
    def __init__(self):
        super().__init__(
            name="terminal",
            description="Executes approved terminal commands."
        )

        self.allowed_commands = {
            "pwd",
            "ls",
            "echo",
            "python"
        }

    def execute(self, command):
        parts = command.split()

        if not parts:
            return "No command provided."

        if parts[0] not in self.allowed_commands:
            return f"Command not allowed: {parts[0]}"

        result = subprocess.run(
            parts,
            capture_output=True,
            text=True
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }