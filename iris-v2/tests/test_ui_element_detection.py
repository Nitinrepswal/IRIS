
from core.vision import VisionEngine


def main():
    vision = VisionEngine()

    screen = {
        "success": True,
        "application": "VS Code",
        "screen_summary": "Python file open.",
        "visible_elements": [
            {
                "type": "button",
                "description": "Run Python file",
                "bbox": [100, 50, 150, 80]
            },
            {
                "type": "text field",
                "description": "Search files"
            },
            {
                "type": "editor",
                "description": "Python source editor",
                "bbox": [200, 100, 800, 600]
            }
        ],
        "suggested_actions": []
    }

    elements = vision.detect_ui_elements(screen)

    assert len(elements) == 3
    assert elements[0]["type"] == "button"
    assert elements[0]["bbox"] == [100, 50, 150, 80]
    assert elements[1]["type"] == "text_field"
    assert elements[1]["bbox"] is None
    assert elements[2]["type"] == "editor"

    print("UI ELEMENT DETECTION TEST: PASS")


if __name__ == "__main__":
    main()
