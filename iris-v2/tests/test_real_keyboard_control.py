
from core.mouse_keyboard import MouseKeyboardController


def main():
    controller = MouseKeyboardController(
        screen_width=1440,
        screen_height=900,
        dry_run=False
    )

    print("In 3 seconds, IRIS will type IRIS DAY 278 into TextEdit.")
    import time
    time.sleep(3)

    result = controller.type_text("IRIS DAY 278")
    print("Typing result:", result)

    if not result.get("success"):
        print("REAL KEYBOARD TEST: FAIL")
        return

    result = controller.press_key("enter")
    print("Enter result:", result)

    if result.get("success"):
        print("REAL KEYBOARD TEST: PASS")
    else:
        print("REAL KEYBOARD TEST: FAIL")


if __name__ == "__main__":
    main()
