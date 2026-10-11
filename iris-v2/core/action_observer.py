
from core.screenshot import ScreenshotTool
from core.vision import VisionEngine


class ActionObserver:
    def __init__(self, screenshot_tool=None, vision_engine=None):
        self.screenshot_tool = screenshot_tool or ScreenshotTool()
        self.vision_engine = vision_engine or VisionEngine()

    def observe(self, filename="action_observation.png"):
        screenshot = self.screenshot_tool.capture(filename)

        if not isinstance(screenshot, dict) or not screenshot.get("success"):
            return {
                "success": False,
                "message": (
                    screenshot.get("message", "Screenshot capture failed")
                    if isinstance(screenshot, dict)
                    else "Invalid screenshot result"
                )
            }

        path = screenshot.get("path")

        if not isinstance(path, str) or not path:
            return {
                "success": False,
                "message": "Screenshot path is missing"
            }

        screen = self.vision_engine.understand_screen(path)

        if not isinstance(screen, dict) or not screen.get("success"):
            return {
                "success": False,
                "message": (
                    screen.get("message", "Screen analysis failed")
                    if isinstance(screen, dict)
                    else "Invalid screen analysis result"
                ),
                "screenshot_path": path
            }

        return {
            "success": True,
            "screenshot_path": path,
            "application": screen.get("application"),
            "screen_summary": screen.get("screen_summary"),
            "visible_elements": screen.get("visible_elements", []),
            "suggested_actions": screen.get("suggested_actions", [])
        }
