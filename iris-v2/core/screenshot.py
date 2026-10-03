import os
import subprocess


class ScreenshotTool:
    def __init__(self, directory="sandbox/screenshots"):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def capture(self, filename="screenshot.png"):
        path = os.path.join(self.directory, filename)

        result = subprocess.run(
            [
                "screencapture",
                "-x",
                path
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
            "path": path
        }

    def execute(self, filename="screenshot.png"):
        return self.capture(filename)