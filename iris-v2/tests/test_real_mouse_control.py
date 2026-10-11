
import pyautogui

from core.mouse_keyboard import MouseKeyboardController


def main():
    controller = MouseKeyboardController(
        screen_width=1440,
        screen_height=900,
        dry_run=False
    )

    start_position = pyautogui.position()

    print("Current mouse position:", start_position)
    print("Screen size:", pyautogui.size())
    print("Testing a small mouse movement in 3 seconds...")

    import time
    time.sleep(3)

    x = min(max(start_position.x + 10, 0), 1439)
    y = min(max(start_position.y + 10, 0), 899)

    result = controller.move_mouse(x, y)
    print("Movement result:", result)

    if result.get("success"):
        print("REAL MOUSE MOVEMENT TEST: PASS")
    else:
        print("REAL MOUSE MOVEMENT TEST: FAIL")


if __name__ == "__main__":
    main()
