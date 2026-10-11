from core.visual_action_planner import VisualActionPlanner
from core.action_observer import ActionObserver


class FakeScreenshotTool:
    def capture(self, filename):
        return {"success": True, "path": "fake.png"}


class FakeVisionEngine:
    def understand_screen(self, path):
        return {
            "success": True,
            "application": "Browser",
            "screen_summary": "A search page is open",
            "visible_elements": [
                {"type": "text_field", "description": "Search field"},
                {"type": "button", "description": "Submit button"}
            ],
            "suggested_actions": []
        }


def main():
    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool(),
        vision_engine=FakeVisionEngine()
    )

    planner = VisualActionPlanner()
    observation = observer.observe()

    assert observation["success"] is True

    plan = planner.plan(
        "Find the search field",
        observation["visible_elements"]
    )

    assert plan["success"] is True
    assert len(plan["steps"]) == 1
    assert plan["steps"][0]["target"]["description"] == "Search field"

    print("COMPUTER CONTROL V2 INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()