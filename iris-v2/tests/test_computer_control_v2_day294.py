from core.action_observer import ActionObserver
from core.visual_action_planner import VisualActionPlanner


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
    planner = VisualActionPlanner()

    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool({
            "success": False,
            "message": "Capture failed"
        }),
        vision_engine=FakeVisionEngine({"success": True})
    )

    observation = observer.observe()
    assert observation["success"] is False
    assert observation["message"] == "Capture failed"

    plan = planner.plan("Find search", [])
    assert plan["success"] is True
    assert plan["steps"] == []

    plan = planner.plan("Find search", [{"type": "button"}])
    assert plan["success"] is False

    print("DAY 294 COMPUTER CONTROL INTEGRATION EDGE TEST: PASS")


if __name__ == "__main__":
    main()