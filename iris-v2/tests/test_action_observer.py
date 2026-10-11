
from core.action_observer import ActionObserver


class FakeScreenshotTool:
    def __init__(self, result=None):
        self.result = result or {
            "success": True,
            "path": "fake_screen.png"
        }

    def capture(self, filename):
        return self.result


class FakeVisionEngine:
    def __init__(self, result=None):
        self.result = result or {
            "success": True,
            "application": "TextEdit",
            "screen_summary": "A document is open.",
            "visible_elements": [
                {"type": "text", "description": "IRIS DAY 279"}
            ],
            "suggested_actions": []
        }

    def understand_screen(self, path):
        return self.result


def main():
    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool(),
        vision_engine=FakeVisionEngine()
    )

    result = observer.observe()
    assert result["success"] is True
    assert result["application"] == "TextEdit"

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool({"success": False, "message": "Capture denied"}),
        vision_engine=FakeVisionEngine()
    )

    result = observer.observe()
    assert result["success"] is False
    assert "Capture denied" in result["message"]

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool(),
        vision_engine=FakeVisionEngine({"success": False, "message": "Analysis failed"})
    )

    result = observer.observe()
    assert result["success"] is False
    assert "Analysis failed" in result["message"]

    print("ACTION OBSERVER FAILURE TEST: PASS")


if __name__ == "__main__":
    main()
