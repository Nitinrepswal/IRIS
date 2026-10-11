from core.action_observer import ActionObserver
from core.action_verification import ActionVerifier


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
                {"type": "text_field", "description": "Search field"}
            ],
            "suggested_actions": []
        }


def main():
    observer = ActionObserver(
        screenshot_tool=FakeScreenshotTool(),
        vision_engine=FakeVisionEngine()
    )

    verifier = ActionVerifier()
    observation = observer.observe()

    assert observation["success"] is True

    result = verifier.verify_observation(
        {"type": "click"},
        {"success": True, "dry_run": False},
        observation
    )

    assert result["status"] == "unverified", result
    assert result["verified"] is False

    dry_run_result = verifier.verify(
        {"type": "click"},
        {"success": True, "dry_run": True},
        {}
    )

    assert dry_run_result["status"] == "dry_run"
    assert dry_run_result["verified"] is False

    print("DAY 295 COMPUTER CONTROL VERIFICATION TEST: PASS")


if __name__ == "__main__":
    main()