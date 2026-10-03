from core.screenshot import ScreenshotTool
from core.vision import VisionEngine


class MultiModalInput:
    def __init__(self):
        self.screenshot = ScreenshotTool()
        self.vision = VisionEngine()

    def process_text(self, text):
        return {
            "type": "text",
            "content": text
        }

    def process_voice(self, text):
        return {
            "type": "voice",
            "content": text
        }

    def process_image(self, image_path, prompt=None):
        result = self.vision.execute(
            image_path,
            prompt
        )

        if not result["success"]:
            return {
                "type": "image",
                "success": False,
                "message": result["message"]
            }

        return {
            "type": "image",
            "success": True,
            "path": image_path,
            "content": result["description"]
        }

    def capture_screen(self, prompt=None):
        result = self.screenshot.capture(
            "multimodal_screen.png"
        )

        if not result["success"]:
            return {
                "type": "screenshot",
                "success": False,
                "message": result["message"]
            }

        return self.process_image(
            result["path"],
            prompt
        )

    def execute(self, input_type, content=None, prompt=None):
        if input_type == "text":
            return self.process_text(content)

        if input_type == "voice":
            return self.process_voice(content)

        if input_type == "image":
            return self.process_image(
                content,
                prompt
            )

        if input_type == "screenshot":
            return self.capture_screen(
                prompt
            )

        return {
            "success": False,
            "message": f"Unknown input type: {input_type}"
        }