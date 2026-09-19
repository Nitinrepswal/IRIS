import subprocess

from tools.tool import Tool


class ApplicationTool(Tool):
    def __init__(self):
        super().__init__(
            name="application",
            description="Launches approved macOS applications."
        )

        self.allowed_applications = {
            "Calculator",
            "TextEdit",
            "Safari"
        }

    def execute(self, application):
        if application not in self.allowed_applications:
            return {
                "success": False,
                "message": f"Application not allowed: {application}"
            }

        result = subprocess.run(
            [
                "open",
                "-a",
                application
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "message": result.stderr.strip()
            }

        return {
            "success": True,
            "application": application,
            "message": f"{application} launched successfully."
        }