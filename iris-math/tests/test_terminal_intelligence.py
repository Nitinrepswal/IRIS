import subprocess


class TerminalTool:
    def run_command(self, command):
        allowed_commands = {
            "pwd": ["pwd"],
            "python_version": ["python", "--version"],
            "list_files": ["ls"],
        }

        if command not in allowed_commands:
            return "Command not allowed"

        result = subprocess.run(
            allowed_commands[command],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return result.stderr.strip()

        return result.stdout.strip() or result.stderr.strip()


class IRISTerminalAgent:
    def __init__(self):
        self.terminal = TerminalTool()

    def run(self, request):
        print("USER")
        print(request)

        if "python version" in request.lower():
            command = "python_version"

        elif "files" in request.lower():
            command = "list_files"

        elif "directory" in request.lower() or "path" in request.lower():
            command = "pwd"

        else:
            command = "unknown"

        print("\nCOMMAND")
        print(command)

        result = self.terminal.run_command(command)

        print("\nOBSERVATION")
        print(result)

        print("\nFINAL ANSWER")
        print(result)


agent = IRISTerminalAgent()

print("=" * 40)
print("IRIS TERMINAL INTELLIGENCE")
print("=" * 40)

agent.run("What Python version am I using?")