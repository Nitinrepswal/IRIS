
from core.mouse_keyboard import MouseKeyboardController


class FakeController(MouseKeyboardController):
    def __init__(self):
        super().__init__(screen_width=1440, screen_height=900, dry_run=True)
        self.actions = []

    def _move_mouse(self, x, y):
        self.actions.append(("move", x, y))
        return {"success": True}

    def _click_mouse(self, x, y, button):
        self.actions.append(("click", x, y, button))
        return {"success": True}

    def _type_text(self, text):
        self.actions.append(("type", text))
        return {"success": True}

    def _press_key(self, key):
        self.actions.append(("press", key))
        return {"success": True}

    def _perform(self, action, *args):
        if action == "move":
            return self._move_mouse(*args)

        if action == "click":
            return self._click_mouse(*args)

        if action == "type":
            return self._type_text(*args)

        if action == "press":
            return self._press_key(*args)

        return {"success": False, "message": "Unsupported action"}


def main():
    controller = FakeController()

    assert controller.move_mouse(100, 200)["success"]
    assert controller.click_mouse(100, 200)["success"]
    assert controller.type_text("Hello IRIS")["success"]
    assert controller.press_key("enter")["success"]

    assert controller.actions == [
        ("move", 100, 200),
        ("move", 100, 200),
        ("click", 100, 200, "left"),
        ("type", "Hello IRIS"),
        ("press", "enter"),
    ], controller.actions

    invalid_results = [
        controller.move_mouse(-1, 100),
        controller.click_mouse(100, -1),
        controller.type_text(""),
        controller.press_key(""),
    ]

    assert all(result["success"] is False for result in invalid_results)

    print("MOUSE KEYBOARD CONTROL TEST: PASS")


if __name__ == "__main__":
    main()
