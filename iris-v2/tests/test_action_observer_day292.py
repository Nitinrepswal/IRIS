from core.action_observer import ActionObserver


class FakeScreenshotTool:
    def __init__(self, result):
        self.result = result

    def capture(self, filename):
        return self.result


class FakeVisionEngine:
    def __init__(self, result):
        self.result = result

    def understand_screen(self, path):
        return self.result


def main():
    cases = [
        (None, None, "Invalid screenshot result"),
        ({"success": True}, None, "Screenshot path is missing"),
        ({"success": True, "path": "screen.png"}, None, None),
    ]

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool(None),
        vision_engine=FakeVisionEngine(None)
    )
    result = observer.observe()
    assert result["success"] is False
    assert result["message"] == "Invalid screenshot result"

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool({"success": True}),
        vision_engine=FakeVisionEngine(None)
    )
    result = observer.observe()
    assert result["success"] is False
    assert result["message"] == "Screenshot path is missing"

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool({
            "success": True,
            "path": "screen.png"
        }),
        vision_engine=FakeVisionEngine(None)
    )
    result = observer.observe()
    assert result["success"] is False
    assert result["message"] == "Invalid screen analysis result"
    assert result["screenshot_path"] == "screen.png"

    print("DAY 292 ACTION OBSERVER EDGE TEST: PASS")


if __name__ == "__main__":
    main()