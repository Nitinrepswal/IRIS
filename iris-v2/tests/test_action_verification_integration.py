
from core.action_observer import ActionObserver
from core.action_verification import ActionVerifier


class FakeScreenshotTool:
    def capture(self, filename):
        return {
            "success": True,
            "path": "fake_screen.png"
        }


class FakeVisionEngine:
    def understand_screen(self, path):
        return {
            "success": True,
            "application": "TextEdit",
            "screen_summary": "A document is open.",
            "visible_elements": [
                {"type": "text", "description": "IRIS DAY 279"}
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

    result = verifier.verify_observation(
        {"type": "type", "text": "IRIS DAY 279"},
        {"success": True, "dry_run": False},
        observation
    )

    assert observation["success"] is True
    assert result["status"] == "unverified"
    assert result["verified"] is False

    print("ACTION VERIFICATION INTEGRATION TEST: PASS")


if __name__ == "__main__":
    main()
