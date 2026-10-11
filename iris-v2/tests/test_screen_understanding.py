
import json

from core.vision import VisionEngine


class TestVisionEngine(VisionEngine):
    def analyze(self, image_path, prompt=None):
        return json.dumps({
            "application": "Visual Studio Code",
            "screen_summary": "A Python file is open in the editor.",
            "visible_elements": [
                {
                    "type": "editor",
                    "description": "Python source code editor"
                },
                {
                    "type": "sidebar",
                    "description": "File explorer"
                }
            ],
            "suggested_actions": [
                "Inspect the open file"
            ]
        })


def main():
    vision = TestVisionEngine()

    result = vision.understand_screen("dummy.png")

    assert result["success"] is True
    assert result["application"] == "Visual Studio Code"
    assert "Python file" in result["screen_summary"]
    assert len(result["visible_elements"]) == 2
    assert result["visible_elements"][0]["type"] == "editor"
    assert result["suggested_actions"] == ["Inspect the open file"]

    print("SCREEN UNDERSTANDING TEST: PASS")


if __name__ == "__main__":
    main()
